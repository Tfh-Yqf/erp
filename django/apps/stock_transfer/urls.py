from extensions.routers import *
from apps.stock_transfer.views import *


router = BaseRouter()
router.register('stock_transfer_orders', StockTransferOrderViewSet, 'stock_transfer_order')
urlpatterns = router.urls
