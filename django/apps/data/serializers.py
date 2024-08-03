from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.data.models import *
from apps.system.models import *


class WarehouseSerializer(BaseSerializer):
    manager_name = CharField(source='manager.name', read_only=True, label='管理员名称')

    class Meta:
        model = Warehouse
        read_only_fields = ['id', 'manager_name']
        fields = ['number', 'name', 'manager', 'phone', 'address', 'remark', 'is_active',
                  *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_manager(self, instance):
        instance = self.validate_foreign_key(User, instance, message='管理员不存在')
        if instance and not instance.is_active:
            raise ValidationError(f'管理员[{instance.name}]未激活')
        return instance


class WarehouseImportExportSerializer(BaseSerializer):
    number = CharField(label='仓库编号(必填唯一)')
    name = CharField(label='仓库名称(必填唯一)')
    manager = CharField(source='manager.name', required=False, label='管理员')
    phone = CharField(required=False, label='电话')
    address = CharField(required=False, label='地址')
    remark = CharField(required=False, label='备注')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager', 'phone', 'address', 'remark',
                  'is_active']


class ClientSerializer(BaseSerializer):
    level_display = CharField(source='get_level_display', read_only=True, label='等级')

    class Meta:
        model = Client
        read_only_fields = ['id', 'level_display']
        fields = ['number', 'name', 'level', 'contact', 'phone', 'email', 'address',
                  'remark', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        validated_data['has_arrears'] = validated_data['arrears_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])
            validated_data['has_arrears'] = validated_data['arrears_amount'] > 0

        return super().update(instance, validated_data)


class ClientImportExportSerializer(BaseSerializer):
    number = CharField(label='客户编号(必填唯一)')
    name = CharField(label='客户名称(必填唯一)')
    level = CharField(required=False, label='等级[0/1/2/3](默认: 0)')
    contact = CharField(required=False, label='联系人')
    phone = CharField(required=False, label='手机号')
    email = CharField(required=False, label='邮箱')
    address = CharField(required=False, label='地址')
    remark = CharField(required=False, label='备注')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Client
        fields = ['number', 'name', 'level', 'contact', 'phone', 'email', 'address', 'remark',
                  'is_active']


class SupplierSerializer(BaseSerializer):

    class Meta:
        model = Supplier
        read_only_fields = ['id']
        fields = ['number', 'name', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        validated_data['has_arrears'] = validated_data['arrears_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])
            validated_data['has_arrears'] = validated_data['arrears_amount'] > 0

        return super().update(instance, validated_data)


class SupplierImportExportSerializer(BaseSerializer):
    number = CharField(label='供应商编号(必填唯一)')
    name = CharField(label='供应商名称(必填唯一)')
    contact = CharField(required=False, label='联系人')
    phone = CharField(required=False, label='手机号')
    email = CharField(required=False, label='邮箱')
    address = CharField(required=False, label='地址')
    bank_account = CharField(required=False, label='银行账户')
    bank_name = CharField(required=False, label='开户行')
    remark = CharField(required=False, label='备注')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Supplier
        fields = ['number', 'name', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'is_active']


class AccountSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='账户类型')

    class Meta:
        model = Account
        read_only_fields = ['id', 'type_display', 'balance_amount', 'has_balance']
        fields = ['number', 'name', 'type', 'holder', 'card_number', 'remark', 'is_active',
                  'initial_balance_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['balance_amount'] = validated_data.get('initial_balance_amount', 0)
        validated_data['has_balance'] = validated_data['balance_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_balance_amount = validated_data.get('initial_arrears_amount')
        if initial_balance_amount is not None and instance.initial_balance_amount != initial_balance_amount:
            balance_amount = NP.minus(instance.balance_amount, instance.initial_balance_amount)
            validated_data['balance_amount'] = NP.plus(balance_amount, validated_data['initial_balance_amount'])
            validated_data['has_balance'] = validated_data['balance_amount'] > 0

        return super().update(instance, validated_data)


class AccountImportExportSerializer(BaseSerializer):
    number = CharField(label='账户编号(必填唯一)')
    name = CharField(label='账户名称(必填唯一)')
    type = CharField(required=False, label='账户类型[cash/alipay/wechat/bank_account/other](默认: cash)')
    holder = CharField(required=False, label='开户人')
    card_number = CharField(required=False, label='开户账号')
    remark = CharField(required=False, label='备注')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Account
        fields = ['number', 'name', 'type', 'holder', 'card_number', 'remark', 'is_active']


class ChargeItemSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='收支类型')

    class Meta:
        model = ChargeItem
        read_only_fields = ['id', 'type_display']
        fields = ['name', 'type', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class ChargeItemImportExportSerializer(BaseSerializer):
    name = CharField(label='收支项目(必填唯一)')
    type = CharField(label='收支类型[income/expenditure](必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = ChargeItem
        fields = ['name', 'type', 'remark']


__all__ = [
    'WarehouseSerializer', 'WarehouseImportExportSerializer',
    'ClientSerializer', 'ClientImportExportSerializer',
    'SupplierSerializer', 'SupplierImportExportSerializer',
    'AccountSerializer', 'AccountImportExportSerializer',
    'ChargeItemSerializer', 'ChargeItemImportExportSerializer',
]
