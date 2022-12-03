from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_check.models import *
from apps.system.models import *
from apps.data.models import *
from apps.goods.models import *


class StockCheckOrderSerializer(BaseSerializer):
    """盘点单据"""

    class StockCheckGoodsItemSerializer(BaseSerializer):
        """盘点产品"""

        class StockCheckBatchItemSerializer(BaseSerializer):
            """盘点批次"""

            status_display = CharField(source='get_status_display', read_only=True, label='盘点状态')

            class Meta:
                model = StockCheckBatch
                read_only_fields = ['id', 'book_quantity', 'surplus_quantity', 'status', 'status_display']
                fields = ['batch_number', 'production_date', 'actual_quantity', *read_only_fields]

            def validate_actual_quantity(self, value):
                if value < 0:
                    raise ValidationError('盘点数量小于零')
                return value

        goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
        enable_batch_control = BooleanField(source='goods.enable_batch_control',
                                            read_only=True, label='启用批次控制')
        status_display = CharField(source='get_status_display', read_only=True, label='盘点状态')
        stock_check_batch_items = StockCheckBatchItemSerializer(
            source='stock_check_batchs', required=False, many=True, label='盘点批次')

        class Meta:
            model = StockCheckGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'unit_name',
                                'enable_batch_control', 'book_quantity', 'surplus_quantity',
                                'purchase_price', 'surplus_amount', 'status', 'status_display']
            fields = ['goods', 'actual_quantity', 'stock_check_batch_items', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='产品不存在')
            if not instance.is_active:
                raise ValidationError(f'产品[{instance.name}]未激活')
            return instance

        def validate_actual_quantity(self, value):
            if value < 0:
                raise ValidationError('盘点数量小于零')
            return value

        def validate(self, attrs):
            goods = attrs['goods']
            if goods.enable_batch_control:
                if not (stock_check_batch_items := attrs.get('stock_check_batchs')):
                    raise ValidationError(f'产品[{goods.name}]批次为空')

                total_actual_quantity = reduce(lambda total, item: NP.plus(total, item['actual_quantity']),
                                               stock_check_batch_items, 0)

                if total_actual_quantity != attrs['actual_quantity']:
                    raise ValidationError(f'产品[{goods.name}]盘点数量错误')

            return super().validate(attrs)

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    status_display = CharField(source='get_status_display', read_only=True, label='盘点状态')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_check_goods_Items = StockCheckGoodsItemSerializer(
        source='stock_check_goods_set', many=True, label='盘点产品')

    class Meta:
        model = StockCheckOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'handler_name', 'creator_name',
                            'status', 'status_display', 'total_book_quantity', 'total_actual_quantity',
                            'total_surplus_quantity', 'total_surplus_amount', 'is_void', 'creator',
                            'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'handler', 'handle_time', 'remark',
                  'stock_check_goods_Items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    @transaction.atomic
    def create(self, validated_data):
        stock_check_goods_items = validated_data.pop('stock_check_goods_set')

        validated_data['creator'] = self.user
        stock_check_order = super().create(validated_data)

        warehouse = stock_check_order.warehouse
        total_book_quantity = 0
        total_actual_quantity = 0
        total_surplus_amount = 0

        # 创建盘点产品
        stock_check_batchs = []
        for stock_check_goods_item in stock_check_goods_items:
            goods = stock_check_goods_item['goods']
            inventory = Inventory.objects.get(warehouse=warehouse, goods=goods, team=self.team)
            book_quantity = inventory.total_quantity
            actual_quantity = stock_check_goods_item['actual_quantity']
            surplus_quantity = NP.minus(actual_quantity, book_quantity)
            purchase_price = goods.purchase_price
            surplus_amount = NP.times(surplus_quantity, purchase_price)

            if surplus_quantity > 0:
                status = StockCheckGoods.Status.SURPLUS
            elif surplus_quantity < 0:
                status = StockCheckGoods.Status.LOSS
            else:
                status = StockCheckGoods.Status.UNCHANGED

            stock_check_goods = StockCheckGoods.objects.create(
                stock_check_order=stock_check_order, goods=goods, book_quantity=book_quantity,
                actual_quantity=actual_quantity, surplus_quantity=surplus_quantity,
                purchase_price=purchase_price, surplus_amount=surplus_amount,
                status=status, team=self.team
            )

            total_book_quantity = NP.plus(total_book_quantity, book_quantity)
            total_actual_quantity = NP.plus(total_actual_quantity, actual_quantity)
            total_surplus_amount = NP.plus(total_surplus_amount, surplus_amount)

            # 创建盘点批次
            if goods.enable_batch_control:
                for stock_check_batch_item in stock_check_goods_item['stock_check_batchs']:
                    batch_number = stock_check_batch_item['batch_number']
                    batch = Batch.objects.filter(number=batch_number, warehouse=warehouse,
                                                 goods=goods, team=self.team).first()

                    if not batch:
                        production_date = stock_check_batch_item.get('production_date')
                        expiration_date = None
                        warning_date = None

                        if production_date and goods.shelf_life_days:
                            expiration_date = pendulum.parse(str(production_date)) \
                                .add(days=goods.shelf_life_days).to_date_string()
                            warning_date = pendulum.parse(str(production_date)) \
                                .add(days=goods.shelf_life_days - goods.shelf_life_warning_days).to_date_string()

                        inventory = Inventory.objects.get(warehouse=warehouse, goods=goods, team=self.team)
                        batch = Batch.objects.create(
                            number=batch_number, inventory=inventory, warehouse=warehouse, goods=goods,
                            total_quantity=0, remain_quantity=0, production_date=production_date,
                            shelf_life_days=goods.shelf_life_days, expiration_date=expiration_date,
                            warning_date=warning_date, has_stock=False, team=self.team
                        )

                    book_quantity = batch.remain_quantity
                    actual_quantity = stock_check_batch_item['actual_quantity']
                    surplus_quantity = NP.minus(actual_quantity, book_quantity)

                    if surplus_quantity > 0:
                        status = StockCheckGoods.Status.SURPLUS
                    elif surplus_quantity < 0:
                        status = StockCheckGoods.Status.LOSS
                    else:
                        status = StockCheckGoods.Status.UNCHANGED

                    stock_check_batchs.append(StockCheckBatch(
                        stock_check_order=stock_check_order, stock_check_goods=stock_check_goods,
                        batch_number=batch_number, goods=goods, book_quantity=book_quantity,
                        actual_quantity=actual_quantity, surplus_quantity=surplus_quantity,
                        status=status, team=self.team
                    ))
        else:
            StockCheckBatch.objects.bulk_create(stock_check_batchs)
            stock_check_order.total_book_quantity = total_book_quantity
            stock_check_order.total_actual_quantity = total_actual_quantity
            stock_check_order.total_surplus_quantity = NP.minus(total_actual_quantity, total_book_quantity)
            stock_check_order.total_surplus_amount = total_surplus_amount
            if stock_check_order.total_surplus_quantity > 0:
                stock_check_order.status = StockCheckGoods.Status.SURPLUS
            elif stock_check_order.total_surplus_quantity < 0:
                stock_check_order.status = StockCheckGoods.Status.LOSS
            else:
                stock_check_order.status = StockCheckGoods.Status.UNCHANGED

            stock_check_order.save(update_fields=['total_book_quantity', 'total_actual_quantity',
                                                  'total_surplus_quantity', 'total_surplus_amount', 'status'])

        return stock_check_order


__all__ = [
    'StockCheckOrderSerializer',
]
