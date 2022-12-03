from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.sales.models import *


class SalesOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesOrder
        fields = ['number', 'warehouse', 'client', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


class SalesReturnOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesReturnOrder
        fields = ['number', 'sales_order', 'warehouse', 'client', 'handler',
                  'is_void', 'creator', 'start_date', 'end_date']


__all__ = [
    'SalesOrderFilter', 'SalesReturnOrderFilter',
]
