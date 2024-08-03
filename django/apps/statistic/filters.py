from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.purchase.models import *
from apps.sales.models import *
from apps.finance.models import *


class PurchaseReportFilter(FilterSet):
    category = NumberFilter(field_name='goods__category', label='产品分类')
    creator = NumberFilter(field_name='sales_order__creator', label='创建人')
    start_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseGoods
        fields = ['category', 'creator', 'start_date', 'end_date']


class SalesReportFilter(FilterSet):
    category = NumberFilter(field_name='goods__category', label='产品分类')
    creator = NumberFilter(field_name='sales_order__creator', label='创建人')
    start_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesGoods
        fields = ['category', 'creator', 'start_date', 'end_date']


class SalesHotGoodsFilter(FilterSet):
    start_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='sales_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesGoods
        fields = ['start_date', 'end_date']


class SalesTrendFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesOrder
        fields = ['start_date', 'end_date']


class PaymentOrderDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PaymentOrder
        fields = ['start_date', 'end_date']


class CollectionOrderDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = CollectionOrder
        fields = ['start_date', 'end_date']


class IncomeChargeOrderDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = ChargeOrder
        fields = ['start_date', 'end_date']


class ExpenditureChargeOrderDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = ChargeOrder
        fields = ['start_date', 'end_date']


class PurchasePaymentDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseOrder
        fields = ['start_date', 'end_date']


class PurchaseReturnCollectionDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseReturnOrder
        fields = ['start_date', 'end_date']


class SalesCollectionDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesOrder
        fields = ['start_date', 'end_date']


class SalesReturnPaymentDetialFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesReturnOrder
        fields = ['start_date', 'end_date']


__all__ = [
    'PurchaseReportFilter', 'SalesReportFilter',
    'SalesHotGoodsFilter', 'SalesTrendFilter',
    'PaymentOrderDetialFilter', 'CollectionOrderDetialFilter',
    'IncomeChargeOrderDetialFilter', 'ExpenditureChargeOrderDetialFilter',
    'PurchasePaymentDetialFilter', 'PurchaseReturnCollectionDetialFilter',
    'SalesCollectionDetialFilter', 'SalesReturnPaymentDetialFilter',
]
