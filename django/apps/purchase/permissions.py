from extensions.permissions import ModelPermission


class PurchaseOrderPermission(ModelPermission):
    code = 'purchase_order'


class PurchaseReturnOrderPermission(ModelPermission):
    code = 'purchase_return_order'


__all__ = [
    'PurchaseOrderPermission', 'PurchaseReturnOrderPermission',
]
