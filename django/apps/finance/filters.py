from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.finance.models import *


class PaymentOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = PaymentOrder
        fields = ['number', 'supplier', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


class CollectionOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = CollectionOrder
        fields = ['number', 'client', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


class ChargeOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = ChargeOrder
        fields = ['number', 'type', 'supplier', 'client', 'handler', 'charge_item',
                  'account', 'is_void', 'creator', 'start_date', 'end_date']


class AccountTransferRecordFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = AccountTransferRecord
        fields = ['out_account', 'in_account', 'handler', 'is_void',
                  'start_date', 'end_date']


__all__ = [
    'PaymentOrderFilter', 'CollectionOrderFilter',
    'ChargeOrderFilter', 'AccountTransferRecordFilter',
]
