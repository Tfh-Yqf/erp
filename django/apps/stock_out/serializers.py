from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_out.models import *
from apps.goods.models import *
from apps.system.models import *


class StockOutOrderSerializer(BaseSerializer):
    """出库通知单据"""

    class StockOutGoodsItemSerializer(BaseSerializer):
        """出库产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
        enable_batch_control = BooleanField(source='goods.enable_batch_control',
                                            read_only=True, label='启用批次控制')

        class Meta:
            model = StockOutGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'stock_out_quantity',
                      'remain_quantity', 'unit_name', 'enable_batch_control', 'is_completed']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    type_display = CharField(source='get_type_display', read_only=True, label='出库类型')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='销售单据编号')
    purchase_return_order_number = CharField(source='purchase_return_order.number',
                                             read_only=True, label='采购退货单据编号')
    stock_transfer_order_number = CharField(source='stock_transfer_order.number',
                                            read_only=True, label='调拨单据编号')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_out_goods_items = StockOutGoodsItemSerializer(
        source='stock_out_goods_set', many=True, label='出库产品')

    class Meta:
        model = StockOutOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'type',
                  'type_display', 'sales_order', 'sales_order_number', 'purchase_return_order',
                  'purchase_return_order_number', 'stock_transfer_order', 'stock_transfer_order_number',
                  'total_quantity', 'remain_quantity', 'is_completed', 'is_void', 'creator',
                  'creator_name', 'create_time', 'stock_out_goods_items']


class StockOutRecordSerializer(BaseSerializer):
    """出库记录"""

    class StockOutRecordGoodsSerializer(BaseSerializer):
        """出库记录产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
        enable_batch_control = BooleanField(source='goods.enable_batch_control',
                                            read_only=True, label='启用批次控制')
        batch_number = CharField(source='batch.number', read_only=True, label='批次编号')

        class Meta:
            model = StockOutRecordGoods
            read_only_fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'unit_name',
                                'enable_batch_control', 'batch_number']
            fields = ['stock_out_goods', 'stock_out_quantity', 'batch', *read_only_fields]

        def validate_stock_out_goods(self, instance):
            instance = self.validate_foreign_key(StockOutGoods, instance, message='出库产品不存在')
            if instance.is_completed:
                raise ValidationError(f'出库产品[{instance.goods.name}]已完成')
            return instance

        def validate_stock_out_quantity(self, value):
            if value <= 0:
                raise ValidationError('出库数量小于或等于零')
            return value

        def validate_batch(self, instance):
            instance = self.validate_foreign_key(Batch, instance, message='批次不存在')
            if instance and not instance.has_stock:
                raise ValidationError(f'批次[{instance.number}]库存不足')
            return instance

        def validate(self, attrs):
            stock_out_goods = attrs['stock_out_goods']

            goods = stock_out_goods.goods

            if stock_out_goods.remain_quantity < attrs['stock_out_quantity']:
                raise ValidationError(f'产品[{goods.name}]出库数量错误')

            if goods.enable_batch_control:
                if not (batch := attrs.get('batch')):
                    raise ValidationError(f'产品[{goods.name}]未选择批次')

                if batch.goods != attrs['stock_out_goods'].goods:
                    raise ValidationError(f'批次[{batch.number}]选择错误')

                if batch.remain_quantity < attrs['stock_out_quantity']:
                    raise ValidationError(f'批次[{batch.number}]库存不足')

            return super().validate(attrs)

    stock_out_order_number = CharField(source='stock_out_order.number', read_only=True, label='出库通知单据编号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_out_record_goods_items = StockOutRecordGoodsSerializer(source='stock_out_record_goods_set',
                                                                 many=True, label='出库记录产品')

    class Meta:
        model = StockOutRecord
        read_only_fields = ['id', 'stock_out_order_number', 'warehouse', 'warehouse_number',
                            'warehouse_name', 'handler_name', 'total_quantity', 'is_void', 'creator',
                            'creator_name', 'create_time']
        fields = ['stock_out_order', 'handler', 'handle_time', 'remark', 'stock_out_record_goods_items',
                  *read_only_fields]

    def validate_stock_out_order(self, instance):
        instance = self.validate_foreign_key(StockOutOrder, instance, message='出库通知单据不存在')
        if instance.is_void:
            raise ValidationError(f'出库通知单据[{instance.number}]已作废')

        if instance.is_completed:
            raise ValidationError(f'出库通知单据[{instance.number}]已完成')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    @transaction.atomic
    def create(self, validated_data):
        stock_out_record_goods_items = validated_data.pop('stock_out_record_goods_set')

        stock_out_order = validated_data['stock_out_order']
        validated_data['warehouse'] = stock_out_order.warehouse
        validated_data['creator'] = self.user
        stock_out_record = super().create(validated_data)

        total_stock_out_quantity = 0

        # 创建出库记录产品
        stock_out_record_goods_set = []
        for stock_out_record_goods_item in stock_out_record_goods_items:
            stock_out_goods = stock_out_record_goods_item['stock_out_goods']
            if stock_out_goods.stock_out_order != stock_out_order:
                raise ValidationError('出库产品错误')

            stock_out_quantity = stock_out_record_goods_item['stock_out_quantity']
            batch = stock_out_record_goods_item.get('batch')
            goods = stock_out_goods.goods

            stock_out_record_goods_set.append(StockOutRecordGoods(
                stock_out_record=stock_out_record, stock_out_goods=stock_out_goods, goods=goods,
                stock_out_quantity=stock_out_quantity, batch=batch, team=self.team
            ))

            total_stock_out_quantity = NP.plus(total_stock_out_quantity, stock_out_quantity)
        else:
            StockOutRecordGoods.objects.bulk_create(stock_out_record_goods_set)
            stock_out_record.total_quantity = total_stock_out_quantity
            stock_out_record.save(update_fields=['total_quantity'])

        return stock_out_record


__all__ = [
    'StockOutOrderSerializer', 'StockOutRecordSerializer',
]
