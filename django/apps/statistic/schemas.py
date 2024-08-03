from extensions.common.schema import *
from extensions.serializers import *


class PurchaseReportParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')
    category = IntegerField(required=False, label='产品分类')


class PurchaseReportStatisticResponse(Serializer):
    total_count = IntegerField(label='采购次数')
    total_quantity = FloatField(label='采购数量')
    total_amount = AmountField(label='采购金额')


class PurchaseReportGroupByGoodsResponse(Serializer):
    goods = IntegerField(label='产品ID')
    goods_number = CharField(label='产品编号')
    goods_name = CharField(label='产品名称')
    goods_barcode = CharField(label='产品条码')
    goods_spec = CharField(label='产品规格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_purchase_quantity = FloatField(label='采购总数量')
    total_purchase_amount = AmountField(label='采购总金额')
    min_purchase_price = FloatField(label='最低采购价')
    avg_purchase_price = FloatField(label='平均采购价')
    max_purchase_price = FloatField(label='最高采购价')


class SalesReportParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')
    category = IntegerField(required=False, label='产品分类')


class SalesReportStatisticResponse(Serializer):
    total_count = IntegerField(label='销售次数')
    total_quantity = FloatField(label='销售数量')
    total_amount = AmountField(label='销售金额')


class SalesReportGroupByGoodsResponse(Serializer):
    goods = IntegerField(label='产品ID')
    goods_number = CharField(label='产品编号')
    goods_name = CharField(label='产品名称')
    goods_barcode = CharField(label='产品条码')
    goods_spec = CharField(label='产品规格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_sales_quantity = FloatField(label='销售总数量')
    total_sales_amount = AmountField(label='销售总金额')
    min_sales_price = FloatField(label='最低销售价')
    avg_sales_price = FloatField(label='平均销售价')
    max_sales_price = FloatField(label='最高销售价')


class SalesHotGoodsParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')


class SalesHotGoodsResponse(Serializer):
    goods = IntegerField(label='产品ID')
    goods_number = CharField(label='产品编号')
    goods_name = CharField(label='产品名称')
    goods_barcode = CharField(label='产品条码')
    goods_spec = CharField(label='产品规格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_sales_quantity = FloatField(label='销售总数量')


class SalesTrendParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')


class SalesTrendResponse(Serializer):
    warehouse = IntegerField(label='仓库ID')
    warehouse_number = CharField(label='产品编号')
    warehouse_name = CharField(label='产品名称')
    total_sales_amount = AmountField(label='销售总金额')
    date = DateField(label='日期')


class FinanceStatisticParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')


class FinanceStatisticResponse(Serializer):
    total_sales_amount = AmountField(label='销售金额')
    total_sales_reutrn_amount = AmountField(label='销售退货金额')
    total_purchase_amount = AmountField(label='采购金额')
    total_purchase_return_amount = AmountField(label='采购退货金额')
    total_income_amount = AmountField(label='收入金额')
    total_expenditure_amount = AmountField(label='支出金额')


class HomeViewResponse(Serializer):
    sales_count = IntegerField(label='销售笔数')
    sales_amount = AmountField(label='销售额')
    purchase_count = IntegerField(label='采购笔数')
    stock_in_task_count = IntegerField(label='待入库')
    stock_out_task_count = IntegerField(label='待出库')
    inventory_warning_count = IntegerField(label='库存预警')
    arrears_receivable_amount = AmountField(label='应收欠款')
    arrears_payable_amount = AmountField(label='应付欠款')


__all__ = [
    'PurchaseReportParameter', 'PurchaseReportStatisticResponse', 'PurchaseReportGroupByGoodsResponse',
    'SalesReportParameter', 'SalesReportStatisticResponse', 'SalesReportGroupByGoodsResponse',
    'SalesHotGoodsParameter', 'SalesHotGoodsResponse', 'SalesTrendParameter', 'SalesTrendResponse',
    'FinanceStatisticParameter', 'FinanceStatisticResponse', 'HomeViewResponse',
]
