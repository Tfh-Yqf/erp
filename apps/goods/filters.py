from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.goods.models import *
import pendulum


class BatchFilter(FilterSet):
    is_expiration_warning = BooleanFilter(method='is_expiration_warning_filter')
    is_expiration = BooleanFilter(method='is_expiration_filter')

    class Meta:
        model = Batch
        fields = ['number', 'warehouse', 'goods', 'has_stock']

    def is_expiration_warning_filter(self, queryset, name, value):
        if value:
            today_date = pendulum.today().to_date_string()
            return queryset.filter(warning_date__lte=today_date, expiration_date__gte=today_date)
        return queryset

    def is_expiration_filter(self, queryset, name, value):
        if value:
            today_date = pendulum.today().to_date_string()
            return queryset.filter(expiration_date__gt=today_date)
        return queryset


__all__ = [
    'BatchFilter',
]
