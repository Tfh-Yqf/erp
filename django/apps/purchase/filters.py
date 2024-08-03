from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.purchase.models import *


class PurchaseOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseOrder
        fields = ['number', 'warehouse', 'supplier', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


class PurchaseReturnOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseReturnOrder
        fields = ['number', 'purchase_order', 'warehouse', 'supplier', 'handler',
                  'is_void', 'creator', 'start_date', 'end_date']


__all__ = [
    'PurchaseOrderFilter', 'PurchaseReturnOrderFilter',
]
