from extensions.common.base import *
from extensions.models import *


class SalesOrder(Model):
    """销售单据"""

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_orders', verbose_name='仓库')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(null=True, verbose_name='销售总数量')
    discount = FloatField(default=1, verbose_name='整单折扣')
    other_amount = AmountField(default=0, verbose_name='其他费用')
    total_amount = AmountField(null=True, verbose_name='销售总金额')
    collection_amount = AmountField(null=True, verbose_name='收款金额')
    arrears_amount = AmountField(null=True, verbose_name='欠款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='启用自动出库')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_orders')

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
            number = 'XS' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class SalesGoods(Model):
    """销售产品"""

    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE,
                             related_name='sales_goods_set', verbose_name='销售单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_goods_set', verbose_name='产品')
    sales_quantity = FloatField(verbose_name='销售数量')
    sales_price = FloatField(verbose_name='销售单价')
    total_amount = AmountField(verbose_name='总金额')
    return_quantity = FloatField(default=0, verbose_name='退货数量')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_goods_set')

    class Meta:
        unique_together = [('sales_order', 'goods')]


class SalesAccount(Model):
    """销售结算账户"""

    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE,
                             related_name='sales_accounts', verbose_name='销售单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='sales_accounts', verbose_name='结算账户')
    collection_amount = AmountField(verbose_name='收款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_accounts')

    class Meta:
        unique_together = [('sales_order', 'account')]


class SalesReturnOrder(Model):
    """销售退货单据"""

    number = CharField(max_length=32, verbose_name='编号')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='sales_return_orders', verbose_name='销售单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='仓库')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(null=True, verbose_name='退货总数量')
    other_amount = AmountField(default=0, verbose_name='其他费用')
    total_amount = AmountField(null=True, verbose_name='退货总金额')
    payment_amount = AmountField(null=True, verbose_name='付款金额')
    arrears_amount = AmountField(null=True, verbose_name='欠款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='启用自动入库')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_return_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_orders')

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
            number = 'SR' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class SalesReturnGoods(Model):
    """销售退货产品"""

    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE,
                                    related_name='sales_return_goods_set', verbose_name='销售退货单据')
    sales_goods = ForeignKey('sales.SalesGoods', on_delete=CASCADE, null=True,
                             related_name='sales_return_goods_set', verbose_name='销售产品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_return_goods_set', verbose_name='产品')
    return_quantity = FloatField(verbose_name='退货数量')
    return_price = FloatField(verbose_name='退货单价')
    total_amount = AmountField(verbose_name='总金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_goods_set')

    class Meta:
        unique_together = [('sales_return_order', 'goods')]


class SalesReturnAccount(Model):
    """销售退货结算账户"""

    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE,
                                    related_name='sales_return_accounts', verbose_name='销售退货单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='sales_return_accounts', verbose_name='结算账户')
    payment_amount = AmountField(verbose_name='付款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_accounts')

    class Meta:
        unique_together = [('sales_return_order', 'account')]


__all__ = [
    'SalesOrder', 'SalesGoods', 'SalesAccount',
    'SalesReturnOrder', 'SalesReturnGoods', 'SalesReturnAccount',
]
