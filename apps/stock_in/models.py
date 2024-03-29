from extensions.common.base import *
from extensions.models import *


class StockInOrder(Model):
    """入库通知单据"""

    class Type(TextChoices):
        """入库类型"""

        PURCHASE = ('purchase', '采购')
        SALES_RETURN = ('sales_return', '销售退货')
        STOCK_TRANSFER = ('stock_transfer', '调拨')

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_in_orders', verbose_name='仓库')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='入库类型')
    purchase_order = OneToOneField('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                   related_name='stock_in_order', verbose_name='采购单据')
    sales_return_order = OneToOneField('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='stock_in_order', verbose_name='销售退货单据')
    stock_transfer_order = OneToOneField('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                         related_name='stock_in_order', verbose_name='调拨单据')
    total_quantity = FloatField(verbose_name='入库总数')
    remain_quantity = FloatField(default=0, verbose_name='入库剩余数量')
    is_completed = BooleanField(default=False, verbose_name='入库完成状态')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today(), pendulum.tomorrow()
        instance = cls.objects.filter(create_time__gte=start_date.format('YYYY-MM-DD HH:mm:ss'),
                                      create_time__lt=end_date.format('YYYY-MM-DD HH:mm:ss'), team=team).last()
        print(instance)

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'RK' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockInGoods(Model):
    """入库产品"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_goods_set', verbose_name='入库通知单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_in_goods_set', verbose_name='产品')
    stock_in_quantity = FloatField(verbose_name='入库总数')
    remain_quantity = FloatField(default=0, verbose_name='入库剩余数量')
    is_completed = BooleanField(default=False, verbose_name='完成状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_goods_set')

    class Meta:
        unique_together = [('stock_in_order', 'goods')]


class StockInRecord(Model):
    """入库记录"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_records', verbose_name='入库通知单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_in_records', verbose_name='仓库')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_in_records', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(null=True, verbose_name='入库总数')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_records', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_records')


class StockInRecordGoods(Model):
    """入库记录产品"""

    stock_in_record = ForeignKey('stock_in.StockInRecord', on_delete=CASCADE,
                                 related_name='stock_in_record_goods_set', verbose_name='入库记录')
    stock_in_goods = ForeignKey('stock_in.StockInGoods', on_delete=CASCADE,
                                related_name='stock_in_record_goods_set', verbose_name='入库产品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_in_record_goods_set', verbose_name='产品')
    stock_in_quantity = FloatField(verbose_name='入库数量')
    batch = ForeignKey('goods.Batch', on_delete=CASCADE, null=True,
                       related_name='stock_in_record_goods_set', verbose_name='批次')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_record_goods_set')

    class Meta:
        unique_together = [('stock_in_record', 'goods')]


__all__ = [
    'StockInOrder', 'StockInGoods',
    'StockInRecord', 'StockInRecordGoods',
]
