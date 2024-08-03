from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.flow.serializers import *
from apps.flow.permissions import *
from apps.flow.filters import *
from apps.flow.schemas import *
from apps.flow.models import *


class InventoryFlowViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """库存流水"""

    serializer_class = InventoryFlowSerializer
    permission_classes = [IsAuthenticated, InventoryFlowPermission]
    filterset_class = InventoryFlowFilter
    search_fields = ['goods__number', 'goods__name', 'purchase_order__number', 'void_purchase_order__number',
                     'purchase_return_order__number', 'void_purchase_return_order__number',
                     'sales_order__number', 'void_sales_order__number', 'sales_return_order__number',
                     'void_sales_return_order__number', 'stock_in_order__number', 'void_stock_in_order__number',
                     'stock_out_order__number', 'void_stock_out_order__number', 'stock_check_order__number',
                     'void_stock_check_order__number', 'stock_transfer_order__number', 'void_stock_transfer_order__number']
    select_related_fields = ['warehouse', 'goods', 'purchase_order', 'void_purchase_order',
                             'purchase_return_order', 'void_purchase_return_order', 'sales_order',
                             'void_sales_order', 'sales_return_order', 'void_sales_return_order',
                             'stock_in_order', 'void_stock_in_order', 'stock_out_order',
                             'void_stock_out_order', 'stock_check_order', 'void_stock_check_order',
                             'stock_transfer_order', 'void_stock_transfer_order', 'creator']
    queryset = InventoryFlow.objects.all()


class FinanceFlowViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """财务流水"""

    serializer_class = FinanceFlowSerializer
    permission_classes = [IsAuthenticated, FinanceFlowPermission]
    filterset_class = FinanceFlowFilter
    search_fields = ['account__number', 'account__name', 'purchase_order__number', 'void_purchase_order__number',
                     'purchase_return_order__number', 'void_purchase_return_order__number', 'sales_order__number',
                     'void_sales_order__number', 'sales_return_order__number', 'void_sales_return_order__number',
                     'payment_order__number', 'void_payment_order__number', 'collection_order__number',
                     'void_collection_order__number', 'charge_order__number', 'void_charge_order__number']
    select_related_fields = ['account', 'purchase_order', 'void_purchase_order',
                             'purchase_return_order', 'void_purchase_return_order', 'sales_order',
                             'void_sales_order', 'sales_return_order', 'void_sales_return_order',
                             'payment_order', 'void_payment_order', 'collection_order',
                             'void_collection_order', 'charge_order', 'void_charge_order', 'creator']
    queryset = FinanceFlow.objects.all()


__all__ = [
    'InventoryFlowViewSet', 'FinanceFlowViewSet',
]
