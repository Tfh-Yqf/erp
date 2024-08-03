from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.purchase.serializers import *
from apps.purchase.permissions import *
from apps.purchase.filters import *
from apps.purchase.schemas import *
from apps.purchase.models import *
from apps.goods.models import *
from apps.flow.models import *
from apps.stock_in.models import *
from apps.stock_out.models import *


class PurchaseOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """采购单据"""

    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, PurchaseOrderPermission]
    filterset_class = PurchaseOrderFilter
    search_fields = ['number', 'supplier__number', 'supplier__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['warehouse', 'supplier', 'handler', 'creator']
    prefetch_related_fields = ['purchase_goods_set', 'purchase_goods_set__goods',
                               'purchase_goods_set__goods__unit',
                               'purchase_accounts', 'purchase_accounts__account']
    queryset = PurchaseOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        purchase_order = serializer.save()

        if purchase_order.enable_auto_stock_in:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_order.warehouse,
                                                  goods=purchase_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_goods.purchase_quantity
                quantity_after = NP.plus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_order.warehouse, goods=purchase_goods.goods,
                    type=InventoryFlow.Type.PURCHASE, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    purchase_order=purchase_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 创建入库通知单据
            stock_in_order_number = StockInOrder.get_number(team=self.team)
            stock_in_order = StockInOrder.objects.create(
                number=stock_in_order_number, warehouse=purchase_order.warehouse,
                type=StockInOrder.Type.PURCHASE, purchase_order=purchase_order,
                total_quantity=purchase_order.total_quantity,
                remain_quantity=purchase_order.total_quantity,
                creator=self.user, team=self.team
            )

            # 创建入库产品
            stock_in_goods_set = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                stock_in_goods_set.append(StockInGoods(
                    stock_in_order=stock_in_order, goods=purchase_goods.goods,
                    stock_in_quantity=purchase_goods.purchase_quantity,
                    remain_quantity=purchase_goods.purchase_quantity, team=self.team
                ))
            else:
                StockInGoods.objects.bulk_create(stock_in_goods_set)

        # 同步欠款
        supplier = purchase_order.supplier
        supplier.arrears_amount = NP.plus(supplier.arrears_amount, purchase_order.arrears_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步账户, 流水
        if purchase_order.payment_amount > 0:
            finance_flows = []
            for purchase_account in purchase_order.purchase_accounts.all():
                account = purchase_account.account
                amount_before = account.balance_amount
                amount_change = purchase_account.payment_amount
                amount_after = NP.minus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.PURCHASE, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after, purchase_order=purchase_order,
                    creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'结算账户[{account.name}]余额不足')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PurchaseOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: PurchaseOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        purchase_order = self.get_object()
        if purchase_order.is_void:
            raise ValidationError(f'采购单据[{purchase_order.number}]已作废, 无法再次作废')

        # 同步采购单据, 采购产品
        purchase_order.is_void = True
        purchase_order.save(update_fields=['is_void'])

        if purchase_order.enable_auto_stock_in:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_order.warehouse,
                                                  goods=purchase_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_goods.purchase_quantity
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_order.warehouse, goods=purchase_goods.goods,
                    type=InventoryFlow.Type.VOID_PURCHASE, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_purchase_order=purchase_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 作废入库通知单据
            stock_in_order = purchase_order.stock_in_order
            if stock_in_order.total_quantity != stock_in_order.remain_quantity:
                raise ValidationError(f'采购单据[{purchase_order.number}]无法作废, 已存在入库记录')

            stock_in_order.is_void = True
            stock_in_order.save(update_fields=['is_void'])

        # 同步欠款
        supplier = purchase_order.supplier
        supplier.arrears_amount = NP.minus(supplier.arrears_amount, purchase_order.arrears_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步账户, 流水
        if purchase_order.payment_amount > 0:
            finance_flows = []
            for purchase_account in purchase_order.purchase_accounts.all():
                account = purchase_account.account
                amount_before = account.balance_amount
                amount_change = purchase_account.payment_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.VOID_PURCHASE, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    void_purchase_order=purchase_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'结算账户[{account.name}]余额不足')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = PurchaseOrderSerializer(instance=purchase_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PurchaseReturnOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """采购退货单据"""

    serializer_class = PurchaseReturnOrderSerializer
    permission_classes = [IsAuthenticated, PurchaseReturnOrderPermission]
    filterset_class = PurchaseReturnOrderFilter
    search_fields = ['number', 'purchase_order__number', 'supplier__number', 'supplier__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['purchase_order', 'warehouse', 'supplier', 'handler', 'creator']
    prefetch_related_fields = ['purchase_return_goods_set', 'purchase_return_goods_set__goods',
                               'purchase_return_goods_set__goods__unit',
                               'purchase_return_accounts', 'purchase_return_accounts__account']
    queryset = PurchaseReturnOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        purchase_return_order = serializer.save()

        if purchase_return_order.enable_auto_stock_out:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_return_goods in purchase_return_order.purchase_return_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_return_order.warehouse,
                                                  goods=purchase_return_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_return_goods.return_quantity
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_return_order.warehouse, goods=purchase_return_goods.goods,
                    type=InventoryFlow.Type.PURCHASE_RETURN, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    purchase_return_order=purchase_return_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 创建出库通知单据
            stock_out_order_number = StockOutOrder.get_number(team=self.team)
            stock_out_order = StockOutOrder.objects.create(
                number=stock_out_order_number, warehouse=purchase_return_order.warehouse,
                type=StockInOrder.Type.PURCHASE, purchase_return_order=purchase_return_order,
                total_quantity=purchase_return_order.total_quantity,
                remain_quantity=purchase_return_order.total_quantity,
                creator=self.user, team=self.team
            )

            # 创建出库产品
            stock_out_goods_set = []
            for purchase_return_goods in purchase_return_order.purchase_return_goods_set.all():
                stock_out_goods_set.append(StockOutGoods(
                    stock_out_order=stock_out_order, goods=purchase_return_goods.goods,
                    stock_out_quantity=purchase_return_goods.return_quantity, team=self.team,
                    remain_quantity=purchase_return_order.total_quantity
                ))
            else:
                StockOutGoods.objects.bulk_create(stock_out_goods_set)

        # 同步欠款
        supplier = purchase_return_order.supplier
        supplier.arrears_amount = NP.minus(supplier.arrears_amount, purchase_return_order.arrears_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步账户, 流水
        if purchase_return_order.collection_amount > 0:
            finance_flows = []
            for purchase_return_account in purchase_return_order.purchase_return_accounts.all():
                account = purchase_return_account.account
                amount_before = account.balance_amount
                amount_change = purchase_return_account.collection_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.PURCHASE_RETURN, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    purchase_return_order=purchase_return_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'结算账户[{account.name}]余额不足')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PurchaseReturnOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: PurchaseReturnOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        purchase_return_order = self.get_object()
        if purchase_return_order.is_void:
            raise ValidationError(f'采购退货单据[{purchase_return_order.number}]已作废, 无法再次作废')

        # 同步采购退货单据, 采购退货产品
        purchase_return_order.is_void = True
        purchase_return_order.save(update_fields=['is_void'])

        if purchase_return_order.enable_auto_stock_out:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_return_goods in purchase_return_order.purchase_return_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_return_order.warehouse,
                                                  goods=purchase_return_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_return_goods.return_quantity
                quantity_after = NP.plus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_return_order.warehouse, goods=purchase_return_goods.goods,
                    type=InventoryFlow.Type.VOID_PURCHASE_RETURN, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_purchase_return_order=purchase_return_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'产品[{inventory.goods.name}]库存不足')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])

                # 同步采购产品退货数量
                if purchase_goods := purchase_return_goods.purchase_goods:
                    purchase_goods.return_quantity = NP.minus(purchase_goods.return_quantity,
                                                              purchase_return_goods.return_quantity)
                    purchase_goods.save(update_fields=['return_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 作废出库通知单据
            stock_out_order = purchase_return_order.stock_out_order
            if stock_out_order.total_quantity != stock_out_order.remain_quantity:
                raise ValidationError(f'采购退货单据[{purchase_return_order.number}]无法作废, 已存在出库记录')

            stock_out_order.is_void = True
            stock_out_order.save(update_fields=['is_void'])

        # 同步欠款
        supplier = purchase_return_order.supplier
        supplier.arrears_amount = NP.plus(supplier.arrears_amount, purchase_return_order.arrears_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        if purchase_return_order.collection_amount > 0:
            # 同步账户, 流水
            finance_flows = []
            for purchase_return_account in purchase_return_order.purchase_return_accounts.all():
                account = purchase_return_account.account
                amount_before = account.balance_amount
                amount_change = purchase_return_account.collection_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.VOID_PURCHASE_RETURN, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    void_purchase_return_order=purchase_return_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'结算账户[{account.name}]余额不足')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = PurchaseReturnOrderSerializer(instance=purchase_return_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'PurchaseOrderViewSet', 'PurchaseReturnOrderViewSet',
]
