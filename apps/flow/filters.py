from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.flow.models import *


class InventoryFlowFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = InventoryFlow
        fields = ['warehouse', 'goods', 'type', 'creator', 'start_date', 'end_date']


class FinanceFlowFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = FinanceFlow
        fields = ['account', 'type', 'creator', 'start_date', 'end_date']


__all__ = [
    'InventoryFlowFilter', 'FinanceFlowFilter',
]
