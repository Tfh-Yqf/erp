from extensions.permissions import ModelPermission


class ProductionOrderPermission(ModelPermission):
    code = 'production_order'


class ProductionRecordPermission(ModelPermission):
    code = 'production_record'


__all__ = [
    'ProductionOrderPermission', 'ProductionRecordPermission',
]
