from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.production.models import *
from apps.sales.models import *
from apps.goods.models import *


class ProductionOrderSerializer(BaseSerializer):
    """生产单据"""

    class SalesGoodsItemSerializer(ModelSerializer):
        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = SalesGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'sales_quantity',
                      'sales_price', 'total_amount', 'return_quantity', 'unit_name']

    sales_order_number = CharField(source='sales_order.number', read_only=True, label='销售单号')
    sales_goods_items = SalesGoodsItemSerializer(
        source='sales_order.sales_goods_set', many=True, read_only=True, label='销售产品Item')
    goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
    status_display = CharField(source='get_status_display', read_only=True, label='状态')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = ProductionOrder
        read_only_fields = ['id', 'sales_order_number', 'sales_goods_items', 'remain_quantity', 'goods_number',
                            'goods_name', 'quantity_produced', 'remain_quantity', 'status', 'status_display',
                            'creator', 'creator_name', 'create_time']
        fields = ['number', 'is_related', 'sales_order', 'goods', 'total_quantity',
                  'start_time', 'end_time', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_sales_order(self, instance):
        instance = self.validate_foreign_key(SalesOrder, instance, message='销售单不存在')
        return instance

    def validate_goods(self, instance):
        instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
        return instance

    def validate_total_quantity(self, value):
        if value <= 0:
            raise ValidationError('生产数量小于等于零')
        return value

    def validate(self, attrs):
        if attrs['is_related'] and not attrs['sales_order']:
            raise ValidationError('未关联销售单')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['quantity_produced'] = 0
        validated_data['creator'] = self.user
        return super().create(validated_data)

    def save(self, **kwargs):
        kwargs['remain_quantity'] = self.validated_data['total_quantity']
        return super().save(**kwargs)


class ProductionRecordSerializer(BaseSerializer):
    """生产记录"""

    production_order_number = CharField(source='production_order.number', read_only=True, label='生产单号')
    goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = ProductionRecord
        read_only_fields = ['id', 'production_order_number', 'goods', 'goods_number', 'goods_name', 'creator',
                            'creator_name', 'create_time']
        fields = ['production_order', 'production_quantity', *read_only_fields]

    def validate_production_order(self, instance):
        instance = self.validate_foreign_key(ProductionOrder, instance, message='生产单不存在')
        if instance.status != ProductionOrder.Status.IN_PROGRESS:
            raise ValidationError(f'工单{instance.number}{instance.get_status_display()}, 无法创建')
        return instance

    def validate_production_quantity(self, value):
        if value <= 0:
            raise ValidationError('生产数量小于等于零')
        return value

    def create(self, validated_data):
        validated_data['goods'] = validated_data['production_order'].goods
        validated_data['creator'] = self.user
        return super().create(validated_data)


__all__ = [
    'ProductionOrderSerializer', 'ProductionRecordSerializer',
]
