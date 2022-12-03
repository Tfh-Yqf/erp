from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *
from apps.finance.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *


class PurchaseOrderSerializer(BaseSerializer):
    """采购单据"""

    class PurchaseGoodsItemSerializer(BaseSerializer):
        """采购产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = PurchaseGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'purchase_quantity', 'purchase_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
            if not instance.is_active:
                raise ValidationError(f'产品[{instance.name}]未激活')
            return instance

        def validate_purchase_quantity(self, value):
            if value <= 0:
                raise ValidationError('采购数量小于或等于零')
            return value

        def validate_purchase_price(self, value):
            if value <= 0:
                raise ValidationError('采购单价小于或等于零')
            return value

    class PurchaseAccountItemSerializer(BaseSerializer):
        """采购结算账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = PurchaseAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'payment_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='账户不存在')
            if not instance.is_active:
                raise ValidationError(f'账户[{instance.name}]未激活')
            return instance

        def validate_payment_amount(self, value):
            if value <= 0:
                raise ValidationError('付款金额小于或等于零')
            return value

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    purchase_goods_items = PurchaseGoodsItemSerializer(
        source='purchase_goods_set', many=True, label='采购产品Item')
    purchase_account_items = PurchaseAccountItemSerializer(
        source='purchase_accounts', required=False, many=True, label='采购结算账户Item')

    class Meta:
        model = PurchaseOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'supplier_number',
                            'supplier_name', 'handler_name', 'total_quantity', 'total_amount',
                            'payment_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_in', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'supplier', 'handler', 'handle_time', 'remark', 'other_amount',
                  'purchase_goods_items', 'purchase_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='供应商不存在')
        if not instance.is_active:
            raise ValidationError(f'供应商[{instance.name}]未激活')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate_other_amount(self, value):
        if value < 0:
            raise ValidationError('其他费用小于零')
        return value

    @transaction.atomic
    def create(self, validated_data):
        purchase_goods_items = validated_data.pop('purchase_goods_set')
        purchase_account_items = validated_data.pop('purchase_accounts', [])

        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        purchase_order = super().create(validated_data)

        total_purchase_quantity = 0
        total_purchase_amount = 0

        # 创建采购产品
        purchase_goods_set = []
        for purchase_goods_item in purchase_goods_items:
            purchase_quantity = purchase_goods_item['purchase_quantity']
            purchase_price = purchase_goods_item['purchase_price']
            total_amount = NP.times(purchase_quantity, purchase_price)
            purchase_goods_set.append(PurchaseGoods(
                purchase_order=purchase_order, goods=purchase_goods_item['goods'],
                purchase_quantity=purchase_quantity, purchase_price=purchase_price,
                total_amount=total_amount, team=self.team
            ))

            total_purchase_quantity = NP.plus(total_purchase_quantity, purchase_quantity)
            total_purchase_amount = NP.plus(total_purchase_amount, total_amount)
        else:
            PurchaseGoods.objects.bulk_create(purchase_goods_set)
            total_purchase_amount = NP.plus(total_purchase_amount, purchase_order.other_amount)
            purchase_order.total_quantity = total_purchase_quantity
            purchase_order.total_amount = total_purchase_amount

        total_payment_amount = 0

        if purchase_account_items:
            # 创建采购结算账户
            purchase_accounts = []
            for purchase_account_item in purchase_account_items:
                payment_amount = purchase_account_item['payment_amount']
                purchase_accounts.append(PurchaseAccount(
                    purchase_order=purchase_order, account=purchase_account_item['account'],
                    payment_amount=payment_amount, team=self.team
                ))

                total_payment_amount = NP.plus(total_payment_amount, payment_amount)
            else:
                PurchaseAccount.objects.bulk_create(purchase_accounts)

        purchase_order.payment_amount = total_payment_amount
        purchase_order.arrears_amount = NP.minus(total_purchase_amount, total_payment_amount)
        purchase_order.save(update_fields=['total_quantity', 'total_amount', 'payment_amount',
                                           'arrears_amount'])

        return purchase_order


class PurchaseReturnOrderSerializer(BaseSerializer):
    """采购退货单据"""

    class PurchaseReturnGoodsItemSerializer(BaseSerializer):
        """采购退货产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = PurchaseReturnGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode',
                                'total_amount', 'unit_name']
            fields = ['purchase_goods', 'goods', 'return_quantity', 'return_price', *read_only_fields]

        def validate_purchase_goods(self, instance):
            instance = self.validate_foreign_key(PurchaseGoods, instance, message='采购产品不存在')
            return instance

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
            if not instance.is_active:
                raise ValidationError(f'产品[{instance.name}]未激活')
            return instance

        def validate_return_quantity(self, value):
            if value <= 0:
                raise ValidationError('退货数量小于或等于零')
            return value

        def validate_return_price(self, value):
            if value <= 0:
                raise ValidationError('退货单价小于或等于零')
            return value

    class PurchaseReturnAccountItemSerializer(BaseSerializer):
        """采购退货结算账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = PurchaseReturnAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'collection_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='账户不存在')
            if not instance.is_active:
                raise ValidationError(f'账户[{instance.name}]未激活')
            return instance

        def validate_collection_amount(self, value):
            if value <= 0:
                raise ValidationError('收款金额小于或等于零')
            return value

    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单据编号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    purchase_return_goods_items = PurchaseReturnGoodsItemSerializer(
        source='purchase_return_goods_set', many=True, label='采购退货产品Item')
    purchase_return_account_items = PurchaseReturnAccountItemSerializer(
        source='purchase_return_accounts', required=False, many=True, label='采购退货结算账户Item')

    class Meta:
        model = PurchaseReturnOrder
        read_only_fields = ['id', 'purchase_order_number', 'warehouse_number', 'warehouse_name',
                            'supplier_number', 'supplier_name', 'handler_name', 'total_quantity',
                            'total_amount', 'collection_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_out', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'purchase_order', 'warehouse', 'supplier', 'handler', 'handle_time',
                  'remark', 'other_amount', 'purchase_return_goods_items',
                  'purchase_return_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_purchase_order(self, instance):
        instance = self.validate_foreign_key(PurchaseOrder, instance, message='采购单据不存在')
        if instance.is_void:
            raise ValidationError(f'采购单据[{instance.name}]已作废')
        return instance

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='供应商不存在')
        if not instance.is_active:
            raise ValidationError(f'供应商[{instance.name}]未激活')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate(self, attrs):
        if purchase_order := attrs.get('purchase_order'):
            if purchase_order.warehouse != attrs['warehouse']:
                raise ValidationError(f'采购单据[{purchase_order.number}]选择错误')

            if purchase_order.supplier != attrs['supplier']:
                raise ValidationError(f'采购单据[{purchase_order.number}]选择错误')

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        purchase_return_goods_items = validated_data.pop('purchase_return_goods_set')
        purchase_return_account_items = validated_data.pop('purchase_return_accounts', [])

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['creator'] = self.user
        purchase_return_order = super().create(validated_data)

        total_return_quantity = 0
        total_return_amount = 0

        # 创建采购退货产品
        purchase_return_goods_set = []
        for purchase_return_goods_item in purchase_return_goods_items:
            goods = purchase_return_goods_item['goods']
            return_quantity = purchase_return_goods_item['return_quantity']

            purchase_goods = None
            if purchase_order := purchase_return_order.purchase_order:
                if not (purchase_goods := purchase_return_goods_item.get('purchase_goods')):
                    raise ValidationError(f'采购单据[{purchase_order.number}]不存在产品[{goods.name}]')

                purchase_goods.return_quantity = NP.plus(purchase_goods.return_quantity, return_quantity)
                if purchase_goods.return_quantity > purchase_goods.purchase_quantity:
                    raise ValidationError(f'退货产品[{goods.name}]退货数量错误')

                # 同步采购产品退货数量
                purchase_goods.save(update_fields=['return_quantity'])

            return_price = purchase_return_goods_item['return_price']
            total_amount = NP.times(return_quantity, return_price)
            purchase_return_goods_set.append(PurchaseReturnGoods(
                purchase_return_order=purchase_return_order, purchase_goods=purchase_goods,
                goods=goods, return_quantity=return_quantity, return_price=return_price,
                total_amount=total_amount, team=self.team
            ))

            total_return_quantity = NP.plus(total_return_quantity, return_quantity)
            total_return_amount = NP.plus(total_return_amount, total_amount)
        else:
            PurchaseReturnGoods.objects.bulk_create(purchase_return_goods_set)
            total_return_amount = NP.plus(total_return_amount, purchase_return_order.other_amount)
            purchase_return_order.total_quantity = total_return_quantity
            purchase_return_order.total_amount = total_return_amount

        total_collection_amount = 0

        if purchase_return_account_items:
            # 创建采购退货结算账户
            purchase_return_accounts = []
            for purchase_return_account_item in purchase_return_account_items:
                collection_amount = purchase_return_account_item['collection_amount']
                purchase_return_accounts.append(PurchaseReturnAccount(
                    purchase_return_order=purchase_return_order,
                    account=purchase_return_account_item['account'],
                    collection_amount=collection_amount, team=self.team
                ))

                total_collection_amount = NP.plus(total_collection_amount, collection_amount)
            else:
                PurchaseReturnAccount.objects.bulk_create(purchase_return_accounts)

        purchase_return_order.collection_amount = total_collection_amount
        purchase_return_order.arrears_amount = NP.minus(total_return_amount, total_collection_amount)
        purchase_return_order.save(update_fields=['total_quantity', 'total_amount', 'collection_amount',
                                                  'arrears_amount'])

        return purchase_return_order


__all__ = [
    'PurchaseOrderSerializer', 'PurchaseReturnOrderSerializer',
]
