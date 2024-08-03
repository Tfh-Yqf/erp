from extensions.permissions import ModelPermission


class StockTransferPermission(ModelPermission):
    code = 'stock_transfer'


__all__ = [
    'StockTransferPermission',
]
