from extensions.common.base import *
from extensions.models import *


class PaymentOrder(Model):
    """付款单据"""

    number = CharField(max_length=32, verbose_name='编号')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='payment_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='payment_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(null=True, verbose_name='总金额')
    discount_amount = AmountField(default=0, verbose_name='优惠金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_payment_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='payment_orders')

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
            number = 'FK' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class PaymentAccount(Model):
    """付款账户"""

    payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE,
                               related_name='payment_accounts', verbose_name='付款单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='payment_accounts', verbose_name='结算账户')
    payment_amount = AmountField(verbose_name='付款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='payment_accounts')

    class Meta:
        unique_together = [('payment_order', 'account')]


class CollectionOrder(Model):
    """收款单据"""

    number = CharField(max_length=32, verbose_name='编号')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='collection_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='collection_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(null=True, verbose_name='总金额')
    discount_amount = AmountField(default=0, verbose_name='优惠金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_collection_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='collection_orders')

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
            number = 'CK' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class CollectionAccount(Model):
    """收款账户"""

    collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE,
                                  related_name='collection_accounts', verbose_name='收款单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='collection_accounts', verbose_name='结算账户')
    collection_amount = AmountField(verbose_name='收款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='collection_accounts')

    class Meta:
        unique_together = [('collection_order', 'account')]


class ChargeOrder(Model):
    """收支单据"""

    class Type(TextChoices):
        """收支类型"""

        INCOME = ('income', '收入')
        EXPENDITURE = ('expenditure', '支出')

    number = CharField(max_length=32, verbose_name='编号')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='收支类型')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, null=True,
                          related_name='charge_orders', verbose_name='供应商')
    client = ForeignKey('data.Client', on_delete=PROTECT, null=True,
                        related_name='charge_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='charge_orders', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    charge_item = ForeignKey('data.ChargeItem', on_delete=SET_NULL, null=True,
                             related_name='charge_orders', verbose_name='收支项目')
    charge_item_name = CharField(max_length=64, verbose_name='收支项目名称')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='charge_orders', verbose_name='结算账户')
    total_amount = AmountField(verbose_name='应收/付金额')
    charge_amount = AmountField(verbose_name='实收/付金额')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_charge_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='charge_orders')

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
            number = 'SZ' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class AccountTransferRecord(Model):
    """结算账户转账记录"""

    class ServiceChargePayer(TextChoices):
        """手续费支付方"""

        TRANSFER_IN = ('transfer_in', '转入方')
        TRANSFER_OUT = ('transfer_out', '转出方')

    out_account = ForeignKey('data.Account', on_delete=PROTECT,
                             related_name='out_account_transfer_records', verbose_name='转出账户')
    transfer_out_time = DateTimeField(verbose_name='转出时间')
    in_account = ForeignKey('data.Account', on_delete=PROTECT,
                                     related_name='in_account_transfer_records', verbose_name='转入账户')
    transfer_in_time = DateTimeField(verbose_name='转入时间')
    transfer_amount = AmountField(verbose_name='转账金额')
    service_charge_amount = AmountField(default=0, verbose_name='手续费金额')
    service_charge_payer = CharField(max_length=32, choices=ServiceChargePayer.choices,
                                     default=ServiceChargePayer.TRANSFER_OUT, verbose_name='手续费支付方')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='account_transfer_records', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_account_transfer_records', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='account_transfer_records')


__all__ = [
    'PaymentOrder', 'PaymentAccount',
    'CollectionOrder', 'CollectionAccount',
    'ChargeOrder', 'AccountTransferRecord',
]
