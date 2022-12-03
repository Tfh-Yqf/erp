from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.finance.models import *
from apps.data.models import *
from apps.system.models import *


class ClientArrearsSerializer(BaseSerializer):
    """应收欠款"""

    level_display = CharField(source='get_level_display', read_only=True, label='等级')

    class Meta:
        model = Client
        fields = ['id', 'number', 'name', 'level', 'level_display',
                  'contact', 'phone', 'email', 'address', 'remark', 'is_active',
                  'initial_arrears_amount', 'arrears_amount', 'has_arrears']


class SupplierArrearsSerializer(BaseSerializer):
    """应付欠款"""


    class Meta:
        model = Supplier
        fields = ['id', 'number', 'name', 'contact', 'phone', 'email',
                  'address', 'bank_account', 'bank_name', 'remark', 'is_active',
                  'initial_arrears_amount', 'arrears_amount', 'has_arrears']


class PaymentOrderSerializer(BaseSerializer):
    """付款单据"""

    class PaymentAccountSerializer(BaseSerializer):
        """付款账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = PaymentAccount
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

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    payment_account_items = PaymentAccountSerializer(source='payment_accounts', many=True, label='付款账户')

    class Meta:
        model = PaymentOrder
        read_only_fields = ['id', 'supplier_number', 'supplier_name', 'handler_name', 'is_void',
                            'creator', 'handler_name', 'creator_name', 'create_time']
        fields = ['number', 'supplier', 'handler', 'handle_time', 'remark', 'discount_amount',
                  'payment_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

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

    @transaction.atomic
    def create(self, validated_data):
        payment_account_items = validated_data.pop('payment_accounts')

        validated_data['creator'] = self.user
        payment_order = super().create(validated_data)

        total_payment_amount = 0

        # 创建付款账户
        payment_accounts = []
        for payment_account_item in payment_account_items:
            payment_amount = payment_account_item['payment_amount']
            payment_accounts.append(PaymentAccount(
                payment_order=payment_order, account=payment_account_item['account'],
                payment_amount=payment_amount, team=self.team
            ))

            total_payment_amount = NP.plus(total_payment_amount, payment_amount)
        else:
            PaymentAccount.objects.bulk_create(payment_accounts)
            total_payment_amount = NP.plus(total_payment_amount, payment_order.discount_amount)
            payment_order.total_amount = total_payment_amount
            payment_order.save(update_fields=['total_amount'])

        return payment_order


class CollectionOrderSerializer(BaseSerializer):
    """收款单据"""

    class CollectionAccountSerializer(BaseSerializer):
        """收款账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = CollectionAccount
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

    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    collection_account_items = CollectionAccountSerializer(
        source='collection_accounts', many=True, label='收款账户')

    class Meta:
        model = CollectionOrder
        read_only_fields = ['id', 'client_number', 'client_name', 'handler_name', 'is_void',
                            'creator', 'handler_name', 'creator_name', 'create_time']
        fields = ['number', 'client', 'handler', 'handle_time', 'remark', 'discount_amount',
                  'collection_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

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

    @transaction.atomic
    def create(self, validated_data):
        collection_account_items = validated_data.pop('collection_accounts')

        validated_data['creator'] = self.user
        collection_order = super().create(validated_data)

        total_collection_amount = 0

        # 创建收款账户
        collection_accounts = []
        for collection_account_item in collection_account_items:
            collection_amount = collection_account_item['collection_amount']
            collection_accounts.append(CollectionAccount(
                collection_order=collection_order, account=collection_account_item['account'],
                collection_amount=collection_amount, team=self.team
            ))

            total_collection_amount = NP.plus(total_collection_amount, collection_amount)
        else:
            CollectionAccount.objects.bulk_create(collection_accounts)
            total_collection_amount = NP.plus(total_collection_amount, collection_order.discount_amount)
            collection_order.total_amount = total_collection_amount
            collection_order.save(update_fields=['total_amount'])

        return collection_order


class ChargeOrderSerializer(BaseSerializer):
    """收支单据"""

    type_display = CharField(source='get_type_display', read_only=True, label='收支类型')
    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    account_number = CharField(source='account.number', read_only=True, label='账户编号')
    account_name = CharField(source='account.name', read_only=True, label='账户名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = ChargeOrder
        read_only_fields = ['id', 'type_display', 'supplier_number', 'supplier_name', 'client_number',
                            'client_name', 'handler_name', 'charge_item_name', 'account_number',
                            'account_name', 'is_void', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'type', 'client', 'supplier', 'handler', 'handle_time', 'charge_item',
                  'account', 'total_amount', 'charge_amount', 'remark', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='供应商不存在')
        if not instance.is_active:
            raise ValidationError(f'供应商[{instance.name}]未激活')
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

    def validate_charge_item(self, instance):
        instance = self.validate_foreign_key(ChargeItem, instance, message='收支项目不存在')
        return instance

    def validate_account(self, instance):
        instance = self.validate_foreign_key(Account, instance, message='结算账户不存在')
        if not instance.is_active:
            raise ValidationError(f'结算账户[{instance.name}]未激活')
        return instance

    def validate(self, attrs):
        supplier = attrs.get('supplier')
        client = attrs.get('client')
        if (supplier and client) or not (supplier or client):
            raise ValidationError('供应商或客户选择重复')

        if attrs['type'] != attrs['charge_item'].type:
            raise ValidationError('收支类型与收支项目不匹配')

        if attrs['charge_amount'] > attrs['total_amount']:
            raise ValidationError('实收/付金额大于应收/付金额')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['charge_item_name'] = validated_data['charge_item'].name
        validated_data['creator'] = self.user

        return super().create(validated_data)


class AccountTransferRecordSerializer(BaseSerializer):
    """收支单据"""

    out_account_number = CharField(source='out_account.number', read_only=True, label='转出账户编号')
    out_account_name = CharField(source='out_account.name', read_only=True, label='转出账户名称')
    in_account_number = CharField(source='out_account.number', read_only=True, label='转入账户编号')
    in_account_name = CharField(source='out_account.name', read_only=True, label='转入账户名称')
    service_charge_payer_display = CharField(
        source='get_service_charge_payer_display', read_only=True, label='手续费支付方')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = AccountTransferRecord
        read_only_fields = ['id', 'out_account_number', 'out_account_name', 'in_account_number',
                            'in_account_name', 'service_charge_payer_display', 'handler_name',
                            'is_void', 'creator', 'creator_name', 'create_time']
        fields = ['out_account', 'transfer_out_time', 'in_account', 'transfer_in_time',
                  'transfer_amount', 'service_charge_amount', 'service_charge_payer', 'handler',
                  'handle_time', 'remark', *read_only_fields]

    def validate_out_account(self, instance):
        instance = self.validate_foreign_key(Account, instance, message='转出账户不存在')
        if not instance.is_active:
            raise ValidationError(f'转出账户[{instance.name}]未激活')
        return instance

    def validate_in_account(self, instance):
        instance = self.validate_foreign_key(Account, instance, message='转入账户不存在')
        if not instance.is_active:
            raise ValidationError(f'转入账户[{instance.name}]未激活')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate(self, attrs):
        if attrs['out_account'] == attrs['in_account']:
            raise ValidationError('转出转入账户相同')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['creator'] = self.user

        return super().create(validated_data)


__all__ = [
    'ClientArrearsSerializer', 'SupplierArrearsSerializer',
    'PaymentOrderSerializer', 'CollectionOrderSerializer',
    'ChargeOrderSerializer', 'AccountTransferRecordSerializer',
]
