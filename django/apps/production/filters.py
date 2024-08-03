from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.production.models import *


class ProductionOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = ProductionOrder
        fields = ['sales_order', 'goods', 'status', 'creator', 'start_date', 'end_date']


class ProductionRecordFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = ProductionRecord
        fields = ['production_order', 'goods', 'creator', 'start_date', 'end_date']


__all__ = [
    'ProductionOrderFilter', 'ProductionRecordFilter',
]
