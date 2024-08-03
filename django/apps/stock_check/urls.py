from extensions.routers import *
from apps.stock_check.views import *


router = BaseRouter()
router.register('stock_check_orders', StockCheckOrderViewSet, 'stock_check_order')
urlpatterns = router.urls
