from extensions.permissions import ModelPermission


class InventoryWarningPermission(ModelPermission):
    code = 'inventory_warning'


class ShelfLifeWarningPermission(ModelPermission):
    code = 'shelf_life_warning'


class StockInReminderPermission(ModelPermission):
    code = 'stock_in_reminder'


class StockOutReminderPermission(ModelPermission):
    code = 'stock_out_reminder'


__all__ = [
    'InventoryWarningPermission', 'ShelfLifeWarningPermission',
    'StockInReminderPermission', 'StockOutReminderPermission',
]
