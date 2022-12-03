from extensions.routers import *
from apps.option.views import *


router = BaseRouter()

# System
router.register('roles/options', RoleOptionViewSet, 'role_option')
router.register('users/options', UserOptionViewSet, 'user_option')

# Data
router.register('warehouses/options', WarehouseOptionViewSet, 'warehouse_option')
router.register('clients/options', ClientOptionViewSet, 'client_option')
router.register('suppliers/options', SupplierOptionViewSet, 'supplier_option')
router.register('accounts/options', AccountOptionViewSet, 'account_option')
router.register('charge_items/options', ChargeItemOptionViewSet, 'charge_item_option')

# Goods
router.register('goods_categories/options', GoodsCategoryOptionViewSet, 'goods_category_option')
router.register('goods_units/options', GoodsUnitOptionViewSet, 'goods_unit_option')
router.register('goods/options', GoodsOptionViewSet, 'goods_option')
router.register('batchs/options', BatchOptionViewSet, 'batch_option')
router.register('inventories/options', InventoryOptionViewSet, 'inventory_option')

# Purchase
router.register('purchase_orders/options', PurchaseOrderOptionViewSet, 'purchase_order_option')

# Sales
router.register('sales_orders/options', SalesOrderOptionViewSet, 'sales_order_option')

# Finance
router.register('client_arrears/options', ClientArrearsOptionViewSet, 'client_arrear_option')
router.register('supplier_arrears/options', SupplierArrearsOptionViewSet, 'supplier_arrear_option')

urlpatterns = router.urls
