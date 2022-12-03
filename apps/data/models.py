from extensions.common.base import *
from extensions.models import *


class Warehouse(Model):
    """仓库"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    manager = ForeignKey('system.User', on_delete=CASCADE, null=True,
                         related_name='warehouses', verbose_name='管理员')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='电话')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='warehouses')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'W001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class Client(Model):
    """客户"""

    class Level(TextChoices):
        """等级"""

        LEVEL0 = ('0', '普通客户')
        LEVEL1 = ('1', '一级客户')
        LEVEL2 = ('2', '二级客户')
        LEVEL3 = ('3', '三级客户')

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    level = CharField(max_length=32, choices=Level.choices, default=Level.LEVEL0, verbose_name='等级')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    email = CharField(max_length=256, null=True, blank=True, verbose_name='邮箱')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期欠款金额')
    arrears_amount = AmountField(default=0, verbose_name='欠款金额')
    has_arrears = BooleanField(default=False, verbose_name='欠款状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='clients')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'C001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class Supplier(Model):
    """供应商"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    email = CharField(max_length=256, null=True, blank=True, verbose_name='邮箱')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    bank_account = CharField(max_length=64, null=True, blank=True, verbose_name='银行账户')
    bank_name = CharField(max_length=64, null=True, blank=True, verbose_name='开户行')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期欠款金额')
    arrears_amount = AmountField(default=0, verbose_name='欠款金额')
    has_arrears = BooleanField(default=False, verbose_name='欠款状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='suppliers')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'S001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class Account(Model):
    """结算账户"""

    class Type(TextChoices):
        """账户类型"""

        CASH = ('cash', '现金')
        ALIPAY = ('alipay', '支付宝')
        WECHAT = ('wechat', '微信')
        BANK_ACCOUNT = ('bank_account', '银行账户')
        OTHER = ('other', '其他')

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, default=Type.CASH, verbose_name='账户类型')
    holder = CharField(max_length=64, null=True, blank=True, verbose_name='开户人')
    card_number = CharField(max_length=64, null=True, blank=True, verbose_name='开户账号')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_balance_amount = AmountField(default=0, verbose_name='初期余额')
    balance_amount = AmountField(default=0, verbose_name='余额')
    has_balance = BooleanField(default=False, verbose_name='余额状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='accounts')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'A001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class ChargeItem(Model):
    """收支项目"""

    class Type(TextChoices):
        """收支类型"""

        INCOME = ('income', '收入')
        EXPENDITURE = ('expenditure', '支出')

    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='收支类型')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='charge_items')

    class Meta:
        unique_together = [('name', 'team')]


__all__ = [
    'Warehouse', 'Client', 'Supplier', 'Account', 'ChargeItem',
]
