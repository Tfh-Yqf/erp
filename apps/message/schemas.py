from extensions.serializers import *


class InventoryWarningResponse(Serializer):
    goods = IntegerField(label='产品ID')
    goods_number = CharField(label='产品编号')
    goods_name = CharField(label='产品名称')
    goods_barcode = CharField(label='产品条码')
    unit_name = CharField(label='单位名称')
    inventory_upper = FloatField(label='库存上限')
    inventory_lower = FloatField(label='库存下限')
    total_quantity = FloatField(label='库存数量')


__all__ = [
    'InventoryWarningResponse',
]
