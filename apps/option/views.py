from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.option.serializers import *
from apps.option.permissions import *
from apps.option.filters import *
from apps.option.schemas import *
from apps.system.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.purchase.models import *
from apps.sales.models import *


# System
class RoleOptionViewSet(InfiniteOptionViewSet):
    serializer_class = RoleOptionSerializer
    permission_classes = [IsAuthenticated, RoleOptionPermission]
    search_fields = ['name']
    queryset = Role.objects.all()


class UserOptionViewSet(InfiniteOptionViewSet):
    serializer_class = UserOptionSerializer
    permission_classes = [IsAuthenticated, UserOptionPermission]
    filterset_fields = ['is_active']
    search_fields = ['username', 'name']
    queryset = User.objects.all()


# Data
class WarehouseOptionViewSet(InfiniteOptionViewSet):
    serializer_class = WarehouseOptionSerializer
    permission_classes = [IsAuthenticated, WarehouseOptionPermission]
    filterset_fields = ['manager', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number']
    ordering = ['number', 'id']
    queryset = Warehouse.objects.all()


class ClientOptionViewSet(InfiniteOptionViewSet):
    serializer_class = ClientOptionSerializer
    permission_classes = [IsAuthenticated, ClientOptionPermission]
    filterset_fields = ['level', 'has_arrears', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number']
    ordering = ['number', 'id']
    queryset = Client.objects.all()


class SupplierOptionViewSet(InfiniteOptionViewSet):
    serializer_class = SupplierOptionSerializer
    permission_classes = [IsAuthenticated, SupplierOptionPermission]
    filterset_fields = ['has_arrears', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number']
    ordering = ['number', 'id']
    queryset = Supplier.objects.all()


class AccountOptionViewSet(InfiniteOptionViewSet):
    serializer_class = AccountOptionSerializer
    permission_classes = [IsAuthenticated, AccountOptionPermission]
    filterset_fields = ['is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number']
    ordering = ['number', 'id']
    queryset = Account.objects.all()


class ChargeItemOptionViewSet(InfiniteOptionViewSet):
    serializer_class = ChargeItemOptionSerializer
    permission_classes = [IsAuthenticated, ChargeItemOptionPermission]
    search_fields = ['name']
    queryset = ChargeItem.objects.all()


# Goods
class GoodsCategoryOptionViewSet(InfiniteOptionViewSet):
    serializer_class = GoodsCategoryOptionSerializer
    permission_classes = [IsAuthenticated, GoodsCategoryOptionPermission]
    search_fields = ['name']
    queryset = GoodsCategory.objects.all()


class GoodsUnitOptionViewSet(InfiniteOptionViewSet):
    serializer_class = GoodsUnitOptionSerializer
    permission_classes = [IsAuthenticated, GoodsUnitOptionPermission]
    search_fields = ['name']
    queryset = GoodsUnit.objects.all()


class GoodsOptionViewSet(LimitedOptionViewSet):
    serializer_class = GoodsOptionSerializer
    permission_classes = [IsAuthenticated, GoodsOptionPermission]
    filterset_fields = ['category', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number']
    ordering = ['number', 'id']
    queryset = Goods.objects.all()


class BatchOptionViewSet(InfiniteOptionViewSet):
    serializer_class = BatchOptionSerializer
    permission_classes = [IsAuthenticated, BatchOptionPermission]
    filterset_class = BatchOptionFilter
    ordering_fields = ['id', 'number']
    ordering = ['-number', 'id']
    select_related_fields = ['goods__unit']
    queryset = Batch.objects.all()


class InventoryOptionViewSet(LimitedOptionViewSet):
    serializer_class = InventoryOptionSerializer
    permission_classes = [IsAuthenticated, InventoryOptionPermission]
    filterset_class = InventoryOptionFilter
    search_fields = ['goods__name', 'goods__number']
    ordering_fields = ['id', 'total_quantity']
    ordering = ['id']
    select_related_fields = ['goods__unit']
    queryset = Inventory.objects.all()


# Purchase
class PurchaseOrderOptionViewSet(LimitedOptionViewSet):
    serializer_class = PurchaseOrderOptionSerializer
    permission_classes = [IsAuthenticated, PurchaseOrderOptionPermission]
    filterset_class = PurchaseOrderOptionFilter
    ordering_fields = ['id', 'number']
    ordering = ['-number', 'id']
    select_related_fields = ['warehouse', 'supplier', 'handler', 'creator']
    prefetch_related_fields = ['purchase_goods_set', 'purchase_goods_set__goods',
                               'purchase_goods_set__goods__unit',
                               'purchase_accounts', 'purchase_accounts__account']
    queryset = PurchaseOrder.objects.all()


# Sales
class SalesOrderOptionViewSet(LimitedOptionViewSet):
    serializer_class = SalesOrderOptionSerializer
    permission_classes = [IsAuthenticated, SalesOrderOptionPermission]
    filterset_class = SalesOrderOptionFilter
    ordering_fields = ['id', 'number']
    ordering = ['-number', 'id']
    select_related_fields = ['warehouse', 'client', 'handler', 'creator']
    prefetch_related_fields = ['sales_goods_set', 'sales_goods_set__goods',
                               'sales_goods_set__goods__unit',
                               'sales_accounts', 'sales_accounts__account']
    queryset = SalesOrder.objects.all()


# Finance
class ClientArrearsOptionViewSet(InfiniteOptionViewSet):
    serializer_class = ClientArrearsOptionSerializer
    permission_classes = [IsAuthenticated, ClientArrearsOptionPermission]
    filterset_fields = ['level', 'is_active', 'has_arrears']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'arrears_amount']
    ordering = ['id']
    queryset = Client.objects.all()


class SupplierArrearsOptionViewSet(InfiniteOptionViewSet):
    serializer_class = SupplierArrearsOptionSerializer
    permission_classes = [IsAuthenticated, SupplierArrearsOptionPermission]
    filterset_fields = ['is_active', 'has_arrears']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'arrears_amount']
    ordering = ['id']
    queryset = Supplier.objects.all()


__all__ = [
    'RoleOptionViewSet', 'UserOptionViewSet',
    'WarehouseOptionViewSet', 'ClientOptionViewSet', 'SupplierOptionViewSet',
    'AccountOptionViewSet', 'ChargeItemOptionViewSet',
    'GoodsCategoryOptionViewSet', 'GoodsUnitOptionViewSet', 'GoodsOptionViewSet',
    'BatchOptionViewSet', 'InventoryOptionViewSet',
    'PurchaseOrderOptionViewSet',
    'SalesOrderOptionViewSet',
    'ClientArrearsOptionViewSet', 'SupplierArrearsOptionViewSet',
]
