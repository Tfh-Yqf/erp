from extensions.models import *


class InventoryFlow(Model):
    """库存流水"""

    class Type(TextChoices):
        """流水类型"""

        PURCHASE = ('purchase', '采购')
        VOID_PURCHASE = ('void_purchase', '作废采购')
        PURCHASE_RETURN = ('purchase_return', '采购退货')
        VOID_PURCHASE_RETURN = ('void_purchase_return', '作废采购退货')
        SALES = ('sales', '销售')
        VOID_SALES = ('void_sales', '作废销售')
        SALES_RETURN = ('sales_return', '销售退货')
        VOID_SALES_RETURN = ('void_sales_return', '作废销售退货')
        STOCK_IN = ('stock_in', '入库')
        VOID_STOCK_IN = ('void_stock_in', '作废入库')
        STOCK_OUT = ('stock_out', '出库')
        VOID_STOCK_OUT = ('void_stock_out', '作废出库')
        STOCK_CHECK = ('stock_check', '盘点')
        VOID_STOCK_CHECK = ('void_stock_check', '作废盘点')
        STOCK_TRANSFER_OUT = ('stock_transfer_out', '调拨转出')
        VOID_STOCK_TRANSFER_OUT = ('void_stock_transfer_out', '作废调拨转出')
        STOCK_TRANSFER_IN = ('stock_transfer_in', '调拨转入')
        VOID_STOCK_TRANSFER_IN = ('void_stock_transfer_in', '作废调拨转入')

    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='inventory_flows', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='inventory_flows', verbose_name='产品')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='流水类型')
    quantity_before = FloatField(verbose_name='变化之前数量')
    quantity_change = FloatField(verbose_name='变化数量')
    quantity_after = FloatField(verbose_name='变化之后数量')

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='inventory_flows', verbose_name='采购单据')
    void_purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                     related_name='void_inventory_flows', verbose_name='作废采购单据')
    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='inventory_flows', verbose_name='采购退货单据')
    void_purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                            related_name='void_inventory_flows', verbose_name='作废采购退货单据')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='inventory_flows', verbose_name='销售单据')
    void_sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                                  related_name='void_inventory_flows', verbose_name='作废销售单据')
    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                    related_name='inventory_flows', verbose_name='销售退货单据')
    void_sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                         related_name='void_inventory_flows', verbose_name='作废销售退货单据')
    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE, null=True,
                                related_name='inventory_flows', verbose_name='入库通知单据')
    void_stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE, null=True,
                                     related_name='void_inventory_flows', verbose_name='作废入库通知单据')
    stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE, null=True,
                                 related_name='inventory_flows', verbose_name='出库通知单据')
    void_stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE, null=True,
                                      related_name='void_inventory_flows', verbose_name='作废出库通知单据')
    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE, null=True,
                                   related_name='inventory_flows', verbose_name='盘点单据')
    void_stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE, null=True,
                                        related_name='void_inventory_flows', verbose_name='作废盘点单据')
    stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                      related_name='inventory_flows', verbose_name='调拨单据')
    void_stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                           related_name='void_inventory_flows', verbose_name='作废调拨单据')

    creator = ForeignKey('system.User', on_delete=PROTECT, related_name='inventory_flows', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventory_flows')


class FinanceFlow(Model):
    """财务流水"""

    class Type(TextChoices):
        """流水类型"""

        PURCHASE = ('purchase', '采购')
        VOID_PURCHASE = ('void_purchase', '作废采购')
        PURCHASE_RETURN = ('purchase_return', '采购退货')
        VOID_PURCHASE_RETURN = ('void_purchase_return', '作废采购退货')
        SALES = ('sales', '销售')
        VOID_SALES = ('void_sales', '作废销售')
        SALES_RETURN = ('sales_return', '销售退货')
        VOID_SALES_RETURN = ('void_sales_return', '作废销售退货')

        PAYMENT = ('payment', '付款')
        VOID_PAYMENT = ('void_payment', '作废付款')
        COLLECTION = ('collection', '收款')
        VOID_COLLECTION = ('void_collection', '作废收款')
        CHARGE = ('charge', '收支')
        VOID_CHARGE = ('void_charge', '作废收支')
        ACCOUNT_TRANSFER_OUT = ('account_transfer_out', '转账转出')
        VOID_ACCOUNT_TRANSFER_OUT = ('void_account_transfer_out', '作废转账转出')
        ACCOUNT_TRANSFER_IN = ('account_transfer_in', '转账转入')
        VOID_ACCOUNT_TRANSFER_IN = ('void_account_transfer_in', '作废转账转入')

    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='finance_flows', verbose_name='结算账户')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='流水类型')
    amount_before = FloatField(verbose_name='变化之前余额')
    amount_change = FloatField(verbose_name='变化余额')
    amount_after = FloatField(verbose_name='变化之后余额')

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='finance_flows', verbose_name='采购单据')
    void_purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                     related_name='void_finance_flows', verbose_name='作废采购单据')
    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='finance_flows', verbose_name='采购退货单据')
    void_purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                            related_name='void_finance_flows', verbose_name='作废采购退货单据')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='finance_flows', verbose_name='销售单据')
    void_sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                                  related_name='void_finance_flows', verbose_name='作废销售单据')
    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                    related_name='finance_flows', verbose_name='销售退货单据')
    void_sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                         related_name='void_finance_flows', verbose_name='作废销售退货单据')

    payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE, null=True,
                               related_name='finance_flows', verbose_name='付款单据')
    void_payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE, null=True,
                                    related_name='void_finance_flows', verbose_name='作废付款单据')
    collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE, null=True,
                                  related_name='finance_flows', verbose_name='收款单据')
    void_collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE, null=True,
                                       related_name='void_finance_flows', verbose_name='作废收款单据')
    charge_order = ForeignKey('finance.ChargeOrder', on_delete=CASCADE, null=True,
                              related_name='finance_flows', verbose_name='收支单据')
    void_charge_order = ForeignKey('finance.ChargeOrder', on_delete=CASCADE, null=True,
                                   related_name='void_finance_flows', verbose_name='作废收支单据')
    account_transfer_record = ForeignKey('finance.AccountTransferRecord', on_delete=CASCADE, null=True,
                                         related_name='finance_flows', verbose_name='转账记录')
    void_account_transfer_record = ForeignKey('finance.AccountTransferRecord', on_delete=CASCADE, null=True,
                                              related_name='void_finance_flows', verbose_name='作废转账记录')

    creator = ForeignKey('system.User', on_delete=PROTECT, null=True,
                         related_name='finance_flows', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='finance_flows')


__all__ = [
    'InventoryFlow', 'FinanceFlow',
]
