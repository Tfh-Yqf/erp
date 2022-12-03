from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.sales.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *
from apps.finance.models import *


class SalesOrderSerializer(BaseSerializer):
    """销售单据"""

    class SalesGoodsItemSerializer(BaseSerializer):
        """销售产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = SalesGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'sales_quantity', 'sales_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
            if not instance.is_active:
                raise ValidationError(f'产品[{instance.name}]未激活')
            return instance

        def validate_sales_quantity(self, value):
            if value <= 0:
                raise ValidationError('销售数量小于或等于零')
            return value

        def validate_sales_price(self, value):
            if value <= 0:
                raise ValidationError('销售单价小于或等于零')
            return value

    class SalesAccountItemSerializer(BaseSerializer):
        """销售结算账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = SalesAccount
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

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    sales_goods_items = SalesGoodsItemSerializer(
        source='sales_goods_set', many=True, label='销售产品Item')
    sales_account_items = SalesAccountItemSerializer(
        source='sales_accounts', required=False, many=True, label='销售结算账户Item')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'client_number', 'client_name',
                            'handler_name', 'total_quantity', 'total_amount', 'collection_amount',
                            'arrears_amount', 'is_void', 'enable_auto_stock_out', 'creator',
                            'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'client', 'handler', 'handle_time', 'discount', 'other_amount',
                  'remark', 'sales_goods_items', 'sales_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_client(self, instance):
        instance = self.validate_foreign_key(Client, instance, message='客户不存在')
        if not instance.is_active:
            raise ValidationError(f'客户[{instance.name}]未激活')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate_discount(self, value):
        if value <= 0:
            raise ValidationError('整单折扣小于或等于零')
        return value

    def validate_other_amount(self, value):
        if value < 0:
            raise ValidationError('其他费用小于零')
        return value

    @transaction.atomic
    def create(self, validated_data):
        sales_goods_items = validated_data.pop('sales_goods_set')
        sales_account_items = validated_data.pop('sales_accounts', [])

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['creator'] = self.user
        sales_order = super().create(validated_data)

        total_sales_quantity = 0
        total_sales_amount = 0

        # 创建销售产品
        sales_goods_set = []
        for sales_goods_item in sales_goods_items:
            sales_quantity = sales_goods_item['sales_quantity']
            sales_price = sales_goods_item['sales_price']
            total_amount = NP.times(sales_quantity, sales_price)
            sales_goods_set.append(SalesGoods(
                sales_order=sales_order, goods=sales_goods_item['goods'], sales_quantity=sales_quantity,
                sales_price=sales_price, total_amount=total_amount, team=self.team
            ))

            total_sales_quantity = NP.plus(total_sales_quantity, sales_quantity)
            total_sales_amount = NP.plus(total_sales_amount, total_amount)
        else:
            SalesGoods.objects.bulk_create(sales_goods_set)
            total_sales_amount = NP.times(total_sales_amount, sales_order.discount, 0.01)
            total_sales_amount = NP.plus(total_sales_amount, sales_order.other_amount)
            sales_order.total_quantity = total_sales_quantity
            sales_order.total_amount = total_sales_amount

        total_collection_amount = 0

        if sales_account_items:
            # 创建销售结算账户
            sales_accounts = []
            for sales_account_item in sales_account_items:
                collection_amount = sales_account_item['collection_amount']
                sales_accounts.append(SalesAccount(
                    sales_order=sales_order, account=sales_account_item['account'],
                    collection_amount=collection_amount, team=self.team
                ))

                total_collection_amount = NP.plus(total_collection_amount, collection_amount)
            else:
                SalesAccount.objects.bulk_create(sales_accounts)

        sales_order.collection_amount = total_collection_amount
        sales_order.arrears_amount = NP.minus(total_sales_amount, total_collection_amount)
        sales_order.save(update_fields=['total_quantity', 'total_amount', 'collection_amount',
                                        'arrears_amount'])
        return sales_order


class SalesReturnOrderSerializer(BaseSerializer):
    """销售退货单据"""

    class SalesReturnGoodsItemSerializer(BaseSerializer):
        """销售退货产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = SalesReturnGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode',
                                'total_amount', 'unit_name']
            fields = ['sales_goods', 'goods', 'return_quantity', 'return_price', *read_only_fields]

        def validate_sales_goods(self, instance):
            instance = self.validate_foreign_key(SalesGoods, instance, message='销售产品不存在')
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

    class SalesReturnAccountItemSerializer(BaseSerializer):
        """销售退货结算账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = SalesReturnAccount
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

    sales_order_number = CharField(source='sales_order.number', read_only=True, label='销售单据编号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    sales_return_goods_items = SalesReturnGoodsItemSerializer(
        source='sales_return_goods_set', many=True, label='销售退货产品')
    sales_return_account_items = SalesReturnAccountItemSerializer(
        source='sales_return_accounts', required=False, many=True, label='销售退货结算账户')

    class Meta:
        model = SalesReturnOrder
        read_only_fields = ['id', 'sales_order_number', 'warehouse_number', 'warehouse_name',
                            'client_number', 'client_name', 'handler_name', 'total_quantity',
                            'total_amount', 'payment_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_in', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'sales_order', 'warehouse', 'client', 'handler', 'handle_time',
                  'remark', 'other_amount', 'sales_return_goods_items',
                  'sales_return_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_sales_order(self, instance):
        instance = self.validate_foreign_key(SalesOrder, instance, message='销售单据不存在')
        if instance.is_void:
            raise ValidationError(f'销售单据[{instance.name}]已作废')
        return instance

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_client(self, instance):
        instance = self.validate_foreign_key(Client, instance, message='客户不存在')
        if not instance.is_active:
            raise ValidationError(f'客户[{instance.name}]未激活')
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

    def validate(self, attrs):
        if sales_order := attrs.get('sales_order'):
            if sales_order.warehouse != attrs['warehouse']:
                raise ValidationError(f'销售单据[{sales_order.number}]选择错误')

            if sales_order.client != attrs['client']:
                raise ValidationError(f'销售单据[{sales_order.number}]选择错误')

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        sales_return_goods_items = validated_data.pop('sales_return_goods_set')
        sales_return_account_items = validated_data.pop('sales_return_accounts', [])

        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        sales_return_order = super().create(validated_data)

        total_return_quantity = 0
        total_return_amount = 0

        # 创建销售退货产品
        sales_return_goods_set = []
        for sales_return_goods_item in sales_return_goods_items:
            goods = sales_return_goods_item['goods']
            return_quantity = sales_return_goods_item['return_quantity']

            sales_goods = None
            if sales_order := sales_return_order.sales_order:
                if not (sales_goods := sales_return_goods_item.get('sales_goods')):
                    raise ValidationError(f'销售单据[{sales_order.number}]不存在产品[{goods.name}]')

                sales_goods.return_quantity = NP.plus(sales_goods.return_quantity, return_quantity)
                if sales_goods.return_quantity > sales_goods.sales_quantity:
                    raise ValidationError(f'退货产品[{goods.name}]退货数量错误')

                # 同步销售产品退货数量
                sales_goods.save(update_fields=['return_quantity'])

            return_price = sales_return_goods_item['return_price']
            total_amount = NP.times(return_quantity, return_price)
            sales_return_goods_set.append(SalesReturnGoods(
                sales_return_order=sales_return_order, sales_goods=sales_goods,
                goods=goods, return_quantity=return_quantity, return_price=return_price,
                total_amount=total_amount, team=self.team
            ))

            total_return_quantity = NP.plus(total_return_quantity, return_quantity)
            total_return_amount = NP.plus(total_return_amount, total_amount)
        else:
            SalesReturnGoods.objects.bulk_create(sales_return_goods_set)
            total_return_amount = NP.plus(total_return_amount, sales_return_order.other_amount)
            sales_return_order.total_quantity = total_return_quantity
            sales_return_order.total_amount = total_return_amount

        total_payment_amount = 0

        if sales_return_account_items:
            # 创建销售退货结算账户
            sales_return_accounts = []
            for sales_return_account_item in sales_return_account_items:
                payment_amount = sales_return_account_item['payment_amount']
                sales_return_accounts.append(SalesReturnAccount(
                    sales_return_order=sales_return_order, account=sales_return_account_item['account'],
                    payment_amount=payment_amount, team=self.team
                ))

                total_payment_amount = NP.plus(total_payment_amount, payment_amount)
            else:
                SalesReturnAccount.objects.bulk_create(sales_return_accounts)

        sales_return_order.payment_amount = total_payment_amount
        sales_return_order.arrears_amount = NP.minus(total_return_amount, total_payment_amount)
        sales_return_order.save(update_fields=['total_quantity', 'total_amount', 'payment_amount',
                                               'arrears_amount'])

        return sales_return_order


__all__ = [
    'SalesOrderSerializer', 'SalesReturnOrderSerializer',
]
