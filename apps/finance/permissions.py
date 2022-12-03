from extensions.permissions import ModelPermission


class ClientArrearsPermission(ModelPermission):
    code = 'client_arrears'


class SupplierArrearsPermission(ModelPermission):
    code = 'supplier_arrears'


class PaymentOrderPermission(ModelPermission):
    code = 'payment_order'


class CollectionOrderPermission(ModelPermission):
    code = 'collection_order'


class ChargeOrderPermission(ModelPermission):
    code = 'charge_order'


class AccountTransferRecordPermission(ModelPermission):
    code = 'account_transfer_record'


__all__ = [
    'ClientArrearsPermission', 'SupplierArrearsPermission',
    'PaymentOrderPermission', 'CollectionOrderPermission',
    'ChargeOrderPermission', 'AccountTransferRecordPermission',
]
