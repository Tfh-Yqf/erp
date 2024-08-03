from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.flow.models import *


class InventoryFlowSerializer(BaseSerializer):
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    goods_number = CharField(source='goods.number', read_only=True, label='产品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='产品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='产品条码')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
    type_display = CharField(source='get_type_display', read_only=True, label='流水类型')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单号')
    void_purchase_order_number = CharField(source='void_purchase_order.number',
                                           read_only=True, label='作废采购单号')
    purchase_return_order_number = CharField(source='purchase_return_order.number',
                                             read_only=True, label='采购退货单号')
    void_purchase_return_order_number = CharField(source='void_purchase_return_order.number',
                                                  read_only=True, label='作废采购退货单号')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='销售单号')
    void_sales_order_number = CharField(source='void_sales_order.number',
                                        read_only=True, label='作废销售单号')
    sales_return_order_number = CharField(source='sales_return_order.number',
                                          read_only=True, label='销售退货单号')
    void_sales_return_order_number = CharField(source='void_sales_return_order.number',
                                               read_only=True, label='作废销售退货单号')
    stock_in_order_number = CharField(source='stock_in_order.number', read_only=True, label='入库通知单号')
    void_stock_in_order_number = CharField(source='void_stock_in_order.number',
                                           read_only=True, label='作废入库通知单号')
    stock_out_order_number = CharField(source='stock_out_order.number', read_only=True, label='出库通知单号')
    void_stock_out_order_number = CharField(source='void_stock_out_order.number',
                                            read_only=True, label='作废出库通知单号')
    stock_check_order_number = CharField(source='stock_check_order.number', read_only=True, label='盘点单号')
    void_stock_check_order_number = CharField(source='void_stock_check_order.number',
                                              read_only=True, label='作废盘点单号')
    stock_transfer_order_number = CharField(source='stock_transfer_order.number',
                                            read_only=True, label='调拨单号')
    void_stock_transfer_order_number = CharField(source='void_stock_transfer_order.number',
                                                 read_only=True, label='作废调拨单号')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = InventoryFlow
        fields = ['warehouse', 'warehouse_number', 'warehouse_name', 'goods', 'goods_number',
                  'goods_name', 'goods_barcode', 'unit_name', 'type_display', 'quantity_before',
                  'quantity_change', 'quantity_after', 'purchase_order', 'purchase_order_number',
                  'void_purchase_order', 'void_purchase_order_number', 'purchase_return_order',
                  'purchase_return_order_number', 'void_purchase_return_order',
                  'void_purchase_return_order_number', 'sales_order', 'sales_order_number',
                  'void_sales_order', 'void_sales_order_number', 'sales_return_order',
                  'sales_return_order_number', 'void_sales_return_order', 'void_sales_return_order_number',
                  'stock_in_order', 'stock_in_order_number', 'void_stock_in_order',
                  'void_stock_in_order_number', 'stock_out_order', 'stock_out_order_number',
                  'void_stock_out_order', 'void_stock_out_order_number', 'stock_check_order',
                  'stock_check_order_number', 'void_stock_check_order', 'void_stock_check_order_number',
                  'stock_transfer_order', 'stock_transfer_order_number', 'void_stock_transfer_order',
                  'void_stock_transfer_order_number', 'creator', 'creator_name', 'create_time']


class FinanceFlowSerializer(BaseSerializer):
    account_number = CharField(source='account.number', read_only=True, label='结算账户编号')
    account_name = CharField(source='account.name', read_only=True, label='结算账户名称')
    type_display = CharField(source='get_type_display', read_only=True, label='流水类型')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单号')
    void_purchase_order_number = CharField(source='void_purchase_order.number',
                                           read_only=True, label='作废采购单号')
    purchase_return_order_number = CharField(source='purchase_return_order.number',
                                             read_only=True, label='采购退货单号')
    void_purchase_return_order_number = CharField(source='void_purchase_return_order.number',
                                                  read_only=True, label='作废采购退货单号')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='销售单号')
    void_sales_order_number = CharField(source='void_sales_order.number',
                                        read_only=True, label='作废销售单号')
    sales_return_order_number = CharField(source='sales_return_order.number',
                                          read_only=True, label='销售退货单号')
    void_sales_return_order_number = CharField(source='void_sales_return_order.number',
                                               read_only=True, label='作废销售退货单号')

    payment_order_number = CharField(source='payment_order.number', read_only=True, label='付款单据')
    void_payment_order_number = CharField(source='void_payment_order.number',
                                          read_only=True, label='作废付款单据')
    collection_order_number = CharField(source='collection_order.number', read_only=True, label='收款单据')
    void_collection_order_number = CharField(source='void_collection_order.number',
                                             read_only=True, label='作废收款单据')
    charge_order_number = CharField(source='charge_order.number', read_only=True, label='收支单据')
    void_charge_order_number = CharField(source='void_charge_order.number',
                                         read_only=True, label='作废收支单据')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')

    class Meta:
        model = FinanceFlow
        fields = ['account', 'account_number', 'account_name', 'type_display', 'purchase_order',
                  'purchase_order_number', 'void_purchase_order', 'void_purchase_order_number',
                  'purchase_return_order', 'purchase_return_order_number', 'void_purchase_return_order',
                  'void_purchase_return_order_number', 'sales_order', 'sales_order_number',
                  'void_sales_order', 'void_sales_order_number', 'sales_return_order',
                  'sales_return_order_number', 'void_sales_return_order', 'void_sales_return_order_number',
                  'payment_order', 'payment_order_number', 'void_payment_order',
                  'void_payment_order_number', 'collection_order', 'collection_order_number',
                  'void_collection_order', 'void_collection_order_number', 'charge_order',
                  'charge_order_number', 'void_charge_order', 'void_charge_order_number',
                  'account_transfer_record', 'void_account_transfer_record',
                  'creator', 'creator_name', 'create_time']


__all__ = [
    'InventoryFlowSerializer', 'FinanceFlowSerializer',
]
