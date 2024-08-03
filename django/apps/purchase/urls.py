from extensions.routers import *
from apps.purchase.views import *


router = BaseRouter()
router.register('purchase_orders', PurchaseOrderViewSet, 'purchase_order')
router.register('purchase_return_orders', PurchaseReturnOrderViewSet, 'purchase_return_order')
urlpatterns = router.urls
