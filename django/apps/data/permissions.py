from extensions.permissions import ModelPermission


class WarehousePermission(ModelPermission):
    code = 'warehouse'


class ClientPermission(ModelPermission):
    code = 'client'


class SupplierPermission(ModelPermission):
    code = 'supplier'


class AccountPermission(ModelPermission):
    code = 'account'


class ChargeItemPermission(ModelPermission):
    code = 'charge_item'


__all__ = [
    'WarehousePermission', 'ClientPermission', 'SupplierPermission', 'AccountPermission',
    'ChargeItemPermission',
]
