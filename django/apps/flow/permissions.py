from extensions.permissions import ModelPermission


class InventoryFlowPermission(ModelPermission):
    code = 'inventory_flow'


class FinanceFlowPermission(ModelPermission):
    code = 'finance_flow'


__all__ = [
    'InventoryFlowPermission', 'FinanceFlowPermission',
]
