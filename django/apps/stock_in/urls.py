from extensions.routers import *
from apps.stock_in.views import *


router = BaseRouter()
router.register('stock_in_orders', StockInOrderViewSet, 'stock_in_order')
router.register('stock_in_records', StockInRecordViewSet, 'stock_in_record')
urlpatterns = router.urls
