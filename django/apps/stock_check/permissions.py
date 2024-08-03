from extensions.permissions import ModelPermission


class StockCheckPermission(ModelPermission):
    code = 'stock_check'


__all__ = [
    'StockCheckPermission',
]
