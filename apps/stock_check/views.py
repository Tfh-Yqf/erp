from apps.goods.models import Inventory
from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.stock_check.serializers import *
from apps.stock_check.permissions import *
from apps.stock_check.filters import *
from apps.stock_check.schemas import *
from apps.stock_check.models import *
from apps.goods.models import *
from apps.flow.models import *


class StockCheckOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """盘点单据"""

    serializer_class = StockCheckOrderSerializer
    permission_classes = [IsAuthenticated, StockCheckPermission]
    filterset_class = StockCheckOrderFilter
    search_fields = ['number', 'remark']
    ordering_fields = ['id', 'number', 'total_surplus_quantity', 'total_surplus_amount', 'create_time']
    select_related_fields = ['warehouse', 'handler', 'creator']
    prefetch_related_fields = ['stock_check_goods_set', 'stock_check_goods_set__goods',
                               'stock_check_goods_set__goods__unit',
                               'stock_check_goods_set__stock_check_batchs']
    queryset = StockCheckOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        stock_check_order = serializer.save()
        warehouse = stock_check_order.warehouse

        inventory_flows = []
        update_inventories = []
        update_batchs = []
        for stock_check_goods in stock_check_order.stock_check_goods_set.all():
            goods = stock_check_goods.goods

            # 同步库存, 流水
            inventory = Inventory.objects.get(warehouse=warehouse, goods=goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = stock_check_goods.surplus_quantity
            quantity_after = stock_check_goods.actual_quantity

            inventory_flows.append(InventoryFlow(
                warehouse=warehouse, goods=goods, type=InventoryFlow.Type.STOCK_CHECK,
                quantity_before=quantity_before, quantity_change=quantity_change,
                quantity_after=quantity_after, stock_check_order=stock_check_order,
                creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            update_inventories.append(inventory)

            # 同步批次
            if goods.enable_batch_control:
                for stock_check_batch in stock_check_goods.stock_check_batchs.all():
                    batch = Batch.objects.get(number=stock_check_batch.batch_number, warehouse=warehouse,
                                              goods=goods, team=self.team)
                    batch.remain_quantity = stock_check_batch.actual_quantity
                    batch.has_stock = batch.remain_quantity > 0
                    update_batchs.append(batch)
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            Inventory.objects.bulk_update(update_inventories, ['total_quantity', 'has_stock'])
            Batch.objects.bulk_update(update_batchs, ['remain_quantity', 'has_stock'])

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = StockCheckOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: StockCheckOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        stock_check_order = self.get_object()
        warehouse = stock_check_order.warehouse
        
        if stock_check_order.is_void:
            raise ValidationError(f'盘点单据[{stock_check_order.number}]已作废, 无法再次作废')
        stock_check_order.is_void = True
        stock_check_order.save(update_fields=['is_void'])

        inventory_flows = []
        update_inventories = []
        update_batchs = []
        for stock_check_goods in stock_check_order.stock_check_goods_set.all():
            goods = stock_check_goods.goods

            # 同步库存, 流水
            inventory = Inventory.objects.get(warehouse=warehouse, goods=goods, team=self.team)
            quantity_before = inventory.total_quantity
            quantity_change = -stock_check_goods.surplus_quantity
            quantity_after = stock_check_goods.book_quantity

            inventory_flows.append(InventoryFlow(
                warehouse=warehouse, goods=goods, type=InventoryFlow.Type.STOCK_CHECK,
                quantity_before=quantity_before, quantity_change=quantity_change,
                quantity_after=quantity_after, stock_check_order=stock_check_order,
                creator=self.user, team=self.team
            ))

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
            inventory.has_stock = inventory.total_quantity > 0
            update_inventories.append(inventory)

            # 同步批次
            if goods.enable_batch_control:
                for stock_check_batch in stock_check_goods.stock_check_batchs.all():
                    batch = stock_check_batch.batch
                    batch.remain_quantity = stock_check_batch.book_quantity
                    batch.has_stock = batch.remain_quantity > 0
                    update_batchs.append(batch)
        else:
            InventoryFlow.objects.bulk_create(inventory_flows)
            Inventory.objects.bulk_update(update_inventories, ['total_quantity', 'has_stock'])
            Batch.objects.bulk_update(update_batchs, ['remain_quantity', 'has_stock'])


__all__ = [
    'StockCheckOrderViewSet',
]
