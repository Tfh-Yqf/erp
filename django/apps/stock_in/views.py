from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.stock_in.serializers import *
from apps.stock_in.permissions import *
from apps.stock_in.filters import *
from apps.stock_in.schemas import *
from apps.stock_in.models import *
from apps.goods.models import *
from apps.flow.models import *


class StockInOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """入库通知单据"""

    serializer_class = StockInOrderSerializer
    permission_classes = [IsAuthenticated, StockInPermission]
    filterset_class = StockInOrderFilter
    search_fields = ['number', 'warehouse__number', 'warehouse__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'create_time']
    select_related_fields = ['warehouse', 'purchase_order', 'sales_return_order',
                             'stock_transfer_order', 'creator']
    prefetch_related_fields = ['stock_in_goods_set', 'stock_in_goods_set__goods',
                               'stock_in_goods_set__goods__unit']
    queryset = StockInOrder.objects.all()


class StockInRecordViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """入库记录"""

    serializer_class = StockInRecordSerializer
    permission_classes = [IsAuthenticated, StockInPermission]
    filterset_class = StockInRecordFilter
    search_fields = ['stock_in_order__number', 'warehouse__number', 'warehouse__name', 'remark']
    ordering_fields = ['id', 'total_quantity', 'create_time']
    select_related_fields = ['stock_in_order', 'warehouse', 'handler', 'creator']
    prefetch_related_fields = ['stock_in_record_goods_set', 'stock_in_record_goods_set__goods',
                               'stock_in_record_goods_set__goods__unit',
                               'stock_in_record_goods_set__batch']
    queryset = StockInRecord.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        stock_in_record = serializer.save()

        # 同步库存, 流水
        inventory_flows = []
        for stock_in_record_goods in stock_in_record.stock_in_record_goods_set.all():
            inventory = Inventory.objects.get(warehouse=stock_in_record.warehouse,
                                              goods=stock_in_record_goods.goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = stock_in_record_goods.stock_in_quantity
            quantity_after = NP.plus(quantity_before, quantity_change)

            inventory_flows.append(InventoryFlow(
                warehouse=stock_in_record.warehouse, goods=stock_in_record_goods.goods,
                type=InventoryFlow.Type.STOCK_IN, quantity_before=quantity_before,
                quantity_change=quantity_change, quantity_after=quantity_after,
                stock_in_order=stock_in_record.stock_in_order, creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            inventory.save(update_fields=['total_quantity', 'has_stock'])

            # 同步入库产品
            stock_in_goods = stock_in_record_goods.stock_in_goods
            stock_in_goods.remain_quantity = NP.minus(stock_in_goods.remain_quantity, quantity_change)
            stock_in_goods.save(update_fields=['remain_quantity'])
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            stock_in_order = stock_in_record.stock_in_order
            stock_in_order.remain_quantity = NP.minus(stock_in_order.remain_quantity,
                                                      stock_in_record.total_quantity)
            stock_in_order.is_completed = stock_in_order.remain_quantity == 0
            stock_in_order.save(update_fields=['remain_quantity', 'is_completed'])

    @transaction.atomic
    @extend_schema(request=None, responses={200: StockInRecordSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        stock_in_record = self.get_object()
        if stock_in_record.is_void:
            raise ValidationError(f'入库记录已作废, 无法再次作废')

        # 同步入库记录, 入库记录产品
        stock_in_record.is_void = True
        stock_in_record.save(update_fields=['is_void'])

        # 同步库存, 流水
        inventory_flows = []
        for stock_in_record_goods in stock_in_record.stock_in_record_goods_set.all():
            inventory = Inventory.objects.get(warehouse=stock_in_record.warehouse,
                                              goods=stock_in_record_goods.goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = stock_in_record_goods.stock_in_quantity
            quantity_after = NP.minus(quantity_before, quantity_change)

            inventory_flows.append(InventoryFlow(
                warehouse=stock_in_record.warehouse, goods=stock_in_record_goods.goods,
                type=InventoryFlow.Type.VOID_STOCK_IN, quantity_before=quantity_before,
                quantity_change=quantity_change, quantity_after=quantity_after,
                stock_in_order=stock_in_record.stock_in_order, creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            inventory.save(update_fields=['total_quantity', 'has_stock'])

            # 同步批次
            if batch := stock_in_record_goods.batch:
                batch.total_quantity = NP.minus(batch.total_quantity, stock_in_record_goods.stock_in_quantity)
                batch.remain_quantity = NP.minus(batch.remain_quantity, stock_in_record_goods.stock_in_quantity)
                batch.has_stock = batch.remain_quantity > 0
                batch.save(update_fields=['total_quantity', 'remain_quantity', 'has_stock'])

            # 同步入库产品
            stock_in_goods = stock_in_record_goods.stock_in_goods
            stock_in_goods.remain_quantity = NP.plus(stock_in_goods.remain_quantity, quantity_change)
            stock_in_goods.save(update_fields=['remain_quantity'])
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            stock_in_order = stock_in_record.stock_in_order
            stock_in_order.remain_quantity = NP.plus(stock_in_order.remain_quantity,
                                                     stock_in_record.total_quantity)
            stock_in_order.is_completed = stock_in_order.remain_quantity == 0
            stock_in_order.save(update_fields=['remain_quantity', 'is_completed'])

        serializer = StockInRecordSerializer(instance=stock_in_record)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'StockInOrderViewSet', 'StockInRecordViewSet',
]
