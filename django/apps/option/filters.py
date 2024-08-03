from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.goods.models import *
from apps.purchase.models import *
from apps.sales.models import *


# Goods
class BatchOptionFilter(FilterSet):
    warehouse = NumberFilter(field_name='warehouse', required=True, label='仓库')
    goods = NumberFilter(field_name='goods', required=True, label='产品')

    class Meta:
        model = Batch
        fields = ['warehouse', 'goods', 'has_stock']


class InventoryOptionFilter(FilterSet):
    warehouse = NumberFilter(field_name='warehouse', required=True, label='仓库')
    category = NumberFilter(field_name='goods__category', label='产品分类')
    is_active = BooleanFilter(field_name='goods__is_active', label='产品激活状态')
    goods_number = CharFilter(field_name='goods__number', label='产品编号')

    class Meta:
        model = Inventory
        fields = ['warehouse', 'category', 'is_active', 'has_stock', 'goods_number']


# Purchase
class PurchaseOrderOptionFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseOrder
        fields = ['number', 'warehouse', 'supplier', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


# Sales
class SalesOrderOptionFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='结束日期')

    class Meta:
        model = SalesOrder
        fields = ['number', 'warehouse', 'client', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


__all__ = [
    'BatchOptionFilter', 'InventoryOptionFilter',
    'PurchaseOrderOptionFilter',
    'SalesOrderOptionFilter',
]
