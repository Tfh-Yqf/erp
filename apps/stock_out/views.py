from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.stock_out.serializers import *
from apps.stock_out.permissions import *
from apps.stock_out.filters import *
from apps.stock_out.schemas import *
from apps.stock_out.models import *
from apps.goods.models import *
from apps.flow.models import *


class StockOutOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """出库通知单据"""

    serializer_class = StockOutOrderSerializer
    permission_classes = [IsAuthenticated, StockOutPermission]
    filterset_class = StockOutOrderFilter
    search_fields = ['number', 'warehouse__number', 'warehouse__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'create_time']
    select_related_fields = ['warehouse', 'sales_order', 'purchase_return_order',
                             'stock_transfer_order', 'creator']
    prefetch_related_fields = ['stock_out_goods_set', 'stock_out_goods_set__goods',
                               'stock_out_goods_set__goods__unit']
    queryset = StockOutOrder.objects.all()


class StockOutRecordViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """出库记录"""

    serializer_class = StockOutRecordSerializer
    permission_classes = [IsAuthenticated, StockOutPermission]
    filterset_class = StockOutRecordFilter
    search_fields = ['stock_out_order__number', 'warehouse__number', 'warehouse__name', 'remark']
    ordering_fields = ['id', 'total_quantity', 'create_time']
    select_related_fields = ['stock_out_order', 'warehouse', 'handler', 'creator']
    prefetch_related_fields = ['stock_out_record_goods_set', 'stock_out_record_goods_set__goods',
                               'stock_out_record_goods_set__goods__unit',
                               'stock_out_record_goods_set__batch']
    queryset = StockOutRecord.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        stock_out_record = serializer.save()

        # 同步库存, 流水
        inventory_flows = []
        for stock_out_record_goods in stock_out_record.stock_out_record_goods_set.all():
            inventory = Inventory.objects.get(warehouse=stock_out_record.warehouse,
                                              goods=stock_out_record_goods.goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = stock_out_record_goods.stock_out_quantity
            quantity_after = NP.minus(quantity_before, quantity_change)

            inventory_flows.append(InventoryFlow(
                warehouse=stock_out_record.warehouse, goods=stock_out_record_goods.goods,
                type=InventoryFlow.Type.STOCK_OUT, quantity_before=quantity_before,
                quantity_change=quantity_change, quantity_after=quantity_after,
                stock_out_order=stock_out_record.stock_out_order, creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            inventory.save(update_fields=['total_quantity', 'has_stock'])

            # 同步批次
            if batch := stock_out_record_goods.batch:
                batch.remain_quantity = NP.minus(batch.remain_quantity, quantity_change)
                batch.has_stock = batch.remain_quantity > 0
                batch.save(update_fields=['remain_quantity', 'has_stock'])

            # 同步出库产品
            stock_out_goods = stock_out_record_goods.stock_out_goods
            stock_out_goods.remain_quantity = NP.minus(stock_out_goods.remain_quantity, quantity_change)
            stock_out_goods.save(update_fields=['remain_quantity'])
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            stock_out_order = stock_out_record.stock_out_order
            stock_out_order.remain_quantity = NP.minus(stock_out_order.remain_quantity,
                                                       stock_out_record.total_quantity)
            stock_out_order.is_completed = stock_out_order.remain_quantity == 0
            stock_out_order.save(update_fields=['remain_quantity', 'is_completed'])

    @transaction.atomic
    @extend_schema(request=None, responses={200: StockOutRecordSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        stock_out_record = self.get_object()
        if stock_out_record.is_void:
            raise ValidationError(f'出库记录已作废, 无法再次作废')

        # 同步出库记录, 出库记录产品
        stock_out_record.is_void = True
        stock_out_record.save(update_fields=['is_void'])

        # 同步库存, 流水
        inventory_flows = []
        for stock_out_record_goods in stock_out_record.stock_out_record_goods_set.all():
            inventory = Inventory.objects.get(warehouse=stock_out_record.warehouse,
                                              goods=stock_out_record_goods.goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = stock_out_record_goods.stock_out_quantity
            quantity_after = NP.plus(quantity_before, quantity_change)

            inventory_flows.append(InventoryFlow(
                warehouse=stock_out_record.warehouse, goods=stock_out_record_goods.goods,
                type=InventoryFlow.Type.VOID_STOCK_OUT, quantity_before=quantity_before,
                quantity_change=quantity_change, quantity_after=quantity_after,
                stock_out_order=stock_out_record.stock_out_order, creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            inventory.save(update_fields=['total_quantity', 'has_stock'])

            # 同步批次
            if batch := stock_out_record_goods.batch:
                batch.total_quantity = NP.minus(batch.total_quantity, stock_out_record_goods.stock_out_quantity)
                batch.remain_quantity = NP.minus(batch.remain_quantity, stock_out_record_goods.stock_out_quantity)
                batch.has_stock = batch.remain_quantity > 0
                batch.save(update_fields=['total_quantity', 'remain_quantity', 'has_stock'])

            # 同步出库产品
            stock_out_goods = stock_out_record_goods.stock_out_goods
            stock_out_goods.remain_quantity = NP.plus(stock_out_goods.remain_quantity, quantity_change)
            stock_out_goods.save(update_fields=['remain_quantity'])
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            stock_out_order = stock_out_record.stock_out_order
            stock_out_order.remain_quantity = NP.plus(stock_out_order.remain_quantity,
                                                      stock_out_record.total_quantity)
            stock_out_order.is_completed = stock_out_order.remain_quantity == 0
            stock_out_order.save(update_fields=['remain_quantity', 'is_completed'])

        serializer = StockOutRecordSerializer(instance=stock_out_record)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'StockOutOrderViewSet', 'StockOutRecordViewSet',
]
