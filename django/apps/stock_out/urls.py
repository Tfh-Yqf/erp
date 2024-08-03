from extensions.routers import *
from apps.stock_out.views import *


router = BaseRouter()
router.register('stock_out_orders', StockOutOrderViewSet, 'stock_out_order')
router.register('stock_out_records', StockOutRecordViewSet, 'stock_out_record')
urlpatterns = router.urls
