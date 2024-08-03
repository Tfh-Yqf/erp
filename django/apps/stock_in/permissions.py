from extensions.permissions import ModelPermission


class StockInPermission(ModelPermission):
    code = 'stock_in'


__all__ = [
    'StockInPermission',
]
