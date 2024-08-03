from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *
from apps.sales.models import *
from apps.finance.models import *


class PurchaseReportDetialSerializer(BaseSerializer):
    """采购明细"""

    goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
    goods_spec = CharField(source='goods.spec', read_only=True, label='产品规格')
    category_name = CharField(source='goods.category.name', read_only=True, label='分类名称')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单号')
    warehouse_number = CharField(source='purchase_order.warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='purchase_order.warehouse.name', read_only=True, label='仓库名称')
    supplier_number = CharField(source='purchase_order.supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='purchase_order.supplier.name', read_only=True, label='供应商名称')
    creator_name = CharField(source='purchase_order.creator.name', read_only=True, label='创建人名称')
    create_time = DateTimeField(source='purchase_order.create_time', read_only=True, label='创建时间')

    class Meta:
        model = PurchaseGoods
        fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'goods_spec',
                  'purchase_quantity', 'category_name', 'unit_name', 'purchase_price', 'total_amount',
                  'purchase_order', 'purchase_order_number', 'warehouse_number', 'warehouse_name',
                  'supplier_number', 'supplier_name', 'creator_name', 'create_time']


class SalesReportDetialSerializer(BaseSerializer):
    """销售明细"""

    goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
    goods_spec = CharField(source='goods.spec', read_only=True, label='产品规格')
    category_name = CharField(source='goods.category.name', read_only=True, label='分类名称')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='采购单号')
    warehouse_number = CharField(source='sales_order.warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='sales_order.warehouse.name', read_only=True, label='仓库名称')
    client_number = CharField(source='sales_order.supplier.number', read_only=True, label='供应商编号')
    client_name = CharField(source='sales_order.supplier.name', read_only=True, label='供应商名称')
    creator_name = CharField(source='sales_order.creator.name', read_only=True, label='创建人名称')
    create_time = DateTimeField(source='sales_order.create_time', read_only=True, label='创建时间')

    class Meta:
        model = SalesGoods
        fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'goods_spec',
                  'sales_quantity', 'category_name', 'unit_name', 'sales_price', 'total_amount',
                  'sales_order', 'sales_order_number', 'warehouse_number', 'warehouse_name',
                  'client_number', 'client_name', 'creator_name', 'create_time']


class PaymentOrderDetialSerializer(BaseSerializer):
    """付款明细"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')

    class Meta:
        model = PaymentOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'discount_amount',
                  'total_amount', 'create_time']


class CollectionOrderDetialSerializer(BaseSerializer):
    """收款单据"""

    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')

    class Meta:
        model = CollectionOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'discount_amount',
                  'total_amount', 'create_time']


class IncomeChargeOrderDetialSerializer(BaseSerializer):
    """收入费用明细"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')

    class Meta:
        model = ChargeOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'supplier',
                  'supplier_number', 'supplier_name', 'charge_item_name', 'total_amount',
                  'charge_amount', 'create_time']


class ExpenditureChargeOrderDetialSerializer(BaseSerializer):
    """支出费用明细"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')

    class Meta:
        model = ChargeOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'supplier',
                  'supplier_number', 'supplier_name', 'charge_item_name', 'total_amount',
                  'charge_amount', 'create_time']


class PurchasePaymentDetialSerializer(BaseSerializer):
    """采购付款明细"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'total_amount',
                  'payment_amount', 'create_time']


class PurchaseReturnCollectionDetialSerializer(BaseSerializer):
    """采购退货收款明细"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')

    class Meta:
        model = PurchaseReturnOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'total_amount',
                  'collection_amount', 'create_time']


class SalesCollectionDetialSerializer(BaseSerializer):
    """销售收款明细"""

    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')

    class Meta:
        model = SalesOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'total_amount',
                  'collection_amount', 'create_time']


class SalesReturnPaymentDetialSerializer(BaseSerializer):
    """销售退货付款明细"""

    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')

    class Meta:
        model = SalesReturnOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'total_amount',
                  'payment_amount', 'create_time']


__all__ = [
    'PurchaseReportDetialSerializer', 'SalesReportDetialSerializer',
    'PaymentOrderDetialSerializer', 'CollectionOrderDetialSerializer',
    'IncomeChargeOrderDetialSerializer', 'ExpenditureChargeOrderDetialSerializer',
    'PurchasePaymentDetialSerializer', 'PurchaseReturnCollectionDetialSerializer',
    'SalesCollectionDetialSerializer', 'SalesReturnPaymentDetialSerializer',
]
