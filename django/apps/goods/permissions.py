from extensions.permissions import ModelPermission


class GoodsCategoryPermission(ModelPermission):
    code = 'goods_category'


class GoodsUnitPermission(ModelPermission):
    code = 'goods_unit'


class GoodsPermission(ModelPermission):
    code = 'goods'


class BatchPermission(ModelPermission):
    code = 'batch'


class InventoryPermission(ModelPermission):
    code = 'inventory'


__all__ = [
    'GoodsCategoryPermission', 'GoodsUnitPermission', 'GoodsPermission',
    'BatchPermission', 'InventoryPermission',
]
