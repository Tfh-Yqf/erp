from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_transfer.models import *
from apps.data.models import*
from apps.goods.models import *
from apps.system.models import *


class StockTransferOrderSerializer(BaseSerializer):
    """调拨单据"""

    class StockTransferGoodsItemSerializer(BaseSerializer):
        """调拨产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = StockTransferGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'unit_name']
            fields = ['goods', 'stock_transfer_quantity', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
            if not instance.is_active:
                raise ValidationError(f'入库产品[{instance.goods.name}]已作废')
            return instance

        def validate_stock_transfer_quantity(self, value):
            if value <= 0:
                raise ValidationError('调拨数量小于或等于零')
            return value

    out_warehouse_number = CharField(source='out_warehouse.number', read_only=True, label='出库仓库编号')
    out_warehouse_name = CharField(source='out_warehouse.name', read_only=True, label='出库仓库名称')
    in_warehouse_number = CharField(source='in_warehouse.number', read_only=True, label='入库库仓库编号')
    in_warehouse_name = CharField(source='in_warehouse.name', read_only=True, label='入库库仓库名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_transfer_goods_items = StockTransferGoodsItemSerializer(
        source='stock_transfer_goods_set', many=True, label='调拨产品')

    class Meta:
        model = StockTransferOrder
        read_only_fields = ['id', 'out_warehouse_number', 'out_warehouse_name', 'in_warehouse_number',
                            'in_warehouse_name', 'handler_name', 'total_quantity', 'is_void',
                            'enable_auto_stock_out', 'enable_auto_stock_in', 'creator', 'creator_name',
                            'create_time']
        fields = ['number', 'out_warehouse', 'in_warehouse', 'handler', 'handle_time',
                  'remark', 'stock_transfer_goods_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_out_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='出库仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_in_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='入库仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate(self, attrs):
        if attrs['out_warehouse'] == attrs['in_warehouse']:
            raise ValidationError('出库仓库和入库仓库相同')

        return super().validate(attrs)

    def create(self, validated_data):
        stock_transfer_goods_items = validated_data.pop('stock_transfer_goods_set')

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        stock_transfer_order = super().create(validated_data)

        total_stock_transfer_quantity = 0

        # 创建调拨产品
        stock_transfer_goods_set = []
        for stock_transfer_goods_item in stock_transfer_goods_items:
            goods = stock_transfer_goods_item['goods']
            stock_transfer_quantity = stock_transfer_goods_item['stock_transfer_quantity']

            stock_transfer_goods_set.append(StockTransferGoods(
                stock_transfer_order=stock_transfer_order, goods=goods,
                stock_transfer_quantity=stock_transfer_quantity, team=self.team
            ))

            total_stock_transfer_quantity = NP.plus(total_stock_transfer_quantity, stock_transfer_quantity)
        else:
            StockTransferGoods.objects.bulk_create(stock_transfer_goods_set)
            stock_transfer_order.total_quantity = total_stock_transfer_quantity
            stock_transfer_order.save(update_fields=['total_quantity'])

        return stock_transfer_order


__all__ = [
    'StockTransferOrderSerializer',
]
