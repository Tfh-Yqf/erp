from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.stock_out.models import *


class StockOutOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = StockOutOrder
        fields = ['number', 'warehouse', 'type', 'is_completed', 'is_void', 'creator',
                  'start_date', 'end_date']


class StockOutRecordFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = StockOutRecord
        fields = ['stock_out_order', 'warehouse', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


__all__ = [
    'StockOutOrderFilter', 'StockOutRecordFilter',
]
