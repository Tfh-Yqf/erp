from extensions.common.base import *
from extensions.models import *


class StockCheckOrder(Model):
    """盘点单据"""

    class Status(TextChoices):
        """盘点状态"""

        SURPLUS = ('surplus', '盘盈')
        LOSS = ('loss', '盘亏')
        UNCHANGED = ('unchanged', '无变化')

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_check_orders', verbose_name='仓库')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_check_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    status = CharField(max_length=32, choices=Status.choices, null=True, verbose_name='盘点状态')
    total_book_quantity = FloatField(null=True, verbose_name='账面总数量')
    total_actual_quantity = FloatField(null=True, verbose_name='实际总数量')
    total_surplus_quantity = FloatField(null=True, verbose_name='盘盈总数量')
    total_surplus_amount = AmountField(null=True, verbose_name='盘盈总金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_check_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_orders')

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
            number = 'PD' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockCheckGoods(Model):
    """盘点产品"""

    class Status(TextChoices):
        """盘点状态"""

        SURPLUS = ('surplus', '盘盈')
        LOSS = ('loss', '盘亏')
        UNCHANGED = ('unchanged', '无变化')

    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE,
                                   related_name='stock_check_goods_set', verbose_name='盘点单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_check_goods_set', verbose_name='产品')
    book_quantity = FloatField(verbose_name='账面数量')
    actual_quantity = FloatField(verbose_name='实际数量')
    surplus_quantity = FloatField(verbose_name='盘盈数量')
    purchase_price = FloatField(verbose_name='采购单价')
    surplus_amount = AmountField(verbose_name='盘盈金额')
    status = CharField(max_length=32, choices=Status.choices, verbose_name='盘点状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_goods_set')

    class Meta:
        unique_together = [('stock_check_order', 'goods')]


class StockCheckBatch(Model):
    """盘点批次"""

    class Status(TextChoices):
        """盘点状态"""

        SURPLUS = ('surplus', '盘盈')
        LOSS = ('loss', '盘亏')
        UNCHANGED = ('unchanged', '无变化')

    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE,
                                   related_name='stock_check_batchs', verbose_name='盘点单据')
    stock_check_goods = ForeignKey('stock_check.StockCheckGoods', on_delete=CASCADE,
                                   related_name='stock_check_batchs', verbose_name='盘点产品')
    batch_number = CharField(max_length=32, verbose_name='批次编号')
    production_date = DateField(null=True, verbose_name='生产日期')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_check_batchs', verbose_name='产品')
    book_quantity = FloatField(verbose_name='账面数量')
    actual_quantity = FloatField(verbose_name='实际数量')
    surplus_quantity = FloatField(verbose_name='盘盈数量')
    status = CharField(max_length=32, choices=Status.choices, verbose_name='盘点状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_batchs')

    class Meta:
        unique_together = [('stock_check_goods', 'batch_number')]


__all__ = [
    'StockCheckOrder', 'StockCheckGoods', 'StockCheckBatch',
]
