from extensions.common.base import *
from extensions.models import *


class PurchaseOrder(Model):
    """采购单据"""

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_orders', verbose_name='仓库')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(null=True, verbose_name='采购总数量')
    other_amount = AmountField(default=0, verbose_name='其他费用')
    total_amount = AmountField(null=True, verbose_name='采购总金额')
    payment_amount = AmountField(null=True, verbose_name='付款金额')
    arrears_amount = AmountField(null=True, verbose_name='欠款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='启用自动入库')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today().to_date_string(), pendulum.tomorrow().to_date_string()
        instance = cls.objects.filter(team=team, create_time__gte=start_date, create_time__lt=end_date).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'CG' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class PurchaseGoods(Model):
    """采购产品"""

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE,
                                related_name='purchase_goods_set', verbose_name='采购单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='purchase_goods_set', verbose_name='产品')
    purchase_quantity = FloatField(verbose_name='采购数量')
    purchase_price = FloatField(verbose_name='采购单价')
    total_amount = AmountField(verbose_name='总金额')
    return_quantity = FloatField(default=0, verbose_name='退货数量')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_goods_set')

    class Meta:
        unique_together = [('purchase_order', 'goods')]


class PurchaseAccount(Model):
    """采购结算账户"""

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE,
                                related_name='purchase_accounts', verbose_name='采购单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='purchase_accounts', verbose_name='结算账户')
    payment_amount = AmountField(verbose_name='付款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_accounts')

    class Meta:
        unique_together = [('purchase_order', 'account')]


class PurchaseReturnOrder(Model):
    """采购退货单据"""

    number = CharField(max_length=32, verbose_name='编号')
    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='purchase_return_orders', verbose_name='采购单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='仓库')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(null=True, verbose_name='退货总数量')
    other_amount = AmountField(default=0, verbose_name='其他费用')
    total_amount = AmountField(null=True, verbose_name='退货总金额')
    collection_amount = AmountField(null=True, verbose_name='收款金额')
    arrears_amount = AmountField(null=True, verbose_name='欠款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='启用自动出库')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_return_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today(), pendulum.tomorrow()
        instance = cls.objects.filter(team=team, create_time__gte=start_date.format('YYYY-MM-DD HH:mm:ss'), create_time__lt=end_date.format('YYYY-MM-DD HH:mm:ss')).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'CR' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class PurchaseReturnGoods(Model):
    """采购退货产品"""

    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE,
                                       related_name='purchase_return_goods_set', verbose_name='采购退货单据')
    purchase_goods = ForeignKey('purchase.PurchaseGoods', on_delete=CASCADE, null=True,
                                related_name='purchase_return_goods_set', verbose_name='采购产品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='purchase_return_goods_set', verbose_name='产品')
    return_quantity = FloatField(verbose_name='退货数量')
    return_price = FloatField(verbose_name='退货单价')
    total_amount = AmountField(verbose_name='总金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_goods_set')

    class Meta:
        unique_together = [('purchase_return_order', 'goods')]


class PurchaseReturnAccount(Model):
    """采购退货结算账户"""

    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE,
                                       related_name='purchase_return_accounts', verbose_name='采购退货单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='purchase_return_accounts', verbose_name='结算账户')
    collection_amount = AmountField(verbose_name='收款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_accounts')

    class Meta:
        unique_together = [('purchase_return_order', 'account')]


__all__ = [
    'PurchaseOrder', 'PurchaseGoods', 'PurchaseAccount',
    'PurchaseReturnOrder', 'PurchaseReturnGoods', 'PurchaseReturnAccount',
]
