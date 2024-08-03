from extensions.permissions import ModelPermission


class StockOutPermission(ModelPermission):
    code = 'stock_out'


__all__ = [
    'StockOutPermission',
]
