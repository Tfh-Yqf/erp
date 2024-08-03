from extensions.common.base import *
from extensions.models import *


class GoodsCategory(Model):
    """产品分类"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_categories')

    class Meta:
        unique_together = [('name', 'team')]


class GoodsUnit(Model):
    """产品单位"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_units')

    class Meta:
        unique_together = [('name', 'team')]


class Goods(Model):
    """产品"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    barcode = CharField(max_length=32, null=True, blank=True, verbose_name='条码')
    category = ForeignKey('goods.GoodsCategory', on_delete=SET_NULL, null=True,
                          related_name='goods_set', verbose_name='产品分类')
    unit = ForeignKey('goods.GoodsUnit', on_delete=SET_NULL, null=True,
                      related_name='goods_set', verbose_name='产品单位')
    spec = CharField(max_length=64, null=True, blank=True, verbose_name='规格')
    enable_batch_control = BooleanField(default=False, verbose_name='启用批次控制')
    shelf_life_days = IntegerField(null=True, verbose_name='保质期天数')
    shelf_life_warning_days = IntegerField(default=0, verbose_name='保质期预警天数')
    enable_inventory_warning = BooleanField(default=False, verbose_name='启用库存警告')
    inventory_upper = FloatField(null=True, verbose_name='库存上限')
    inventory_lower = FloatField(null=True, verbose_name='库存下限')
    purchase_price = FloatField(default=0, verbose_name='采购价')
    retail_price = FloatField(default=0, verbose_name='零售价')
    level_price1 = FloatField(default=0, verbose_name='等级价一')
    level_price2 = FloatField(default=0, verbose_name='等级价二')
    level_price3 = FloatField(default=0, verbose_name='等级价三')

    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_set')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'G000000000001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class GoodsImage(Model):
    """产品图片"""

    goods = ForeignKey('goods.Goods', on_delete=SET_NULL, null=True,
                       related_name='goods_images', verbose_name='产品')
    file = ImageField(verbose_name='文件')
    name = CharField(max_length=256, verbose_name='文件名称')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_images')


class Batch(Model):
    """批次"""

    number = CharField(max_length=32, verbose_name='编号')
    inventory = ForeignKey('goods.Inventory', on_delete=CASCADE, related_name='batchs', verbose_name='库存')
    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='batchs', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='batchs', verbose_name='产品')
    initial_quantity = FloatField(default=0, verbose_name='初始库存')
    total_quantity = FloatField(verbose_name='批次数量')
    remain_quantity = FloatField(verbose_name='批次剩余数量')
    production_date = DateField(null=True, verbose_name='生产日期')
    shelf_life_days = IntegerField(null=True, verbose_name='保质期天数')
    warning_date = DateField(null=True, verbose_name='预警日期')
    expiration_date = DateField(null=True, verbose_name='过期日期')
    has_stock = BooleanField(default=True, verbose_name='库存状态')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='batchs')

    class Meta:
        unique_together = [('number', 'warehouse', 'goods', 'team')]


class Inventory(Model):
    """库存"""

    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='inventories', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='inventories', verbose_name='产品')
    initial_quantity = FloatField(default=0, verbose_name='初始库存')
    total_quantity = FloatField(default=0, verbose_name='库存总数')
    has_stock = BooleanField(default=False, verbose_name='库存状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventories')

    class Meta:
        unique_together = [('warehouse', 'goods', 'team')]


__all__ = [
    'GoodsCategory', 'GoodsUnit', 'Goods', 'GoodsImage',
    'Batch', 'Inventory',
]
