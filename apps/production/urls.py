from extensions.routers import *
from apps.production.views import *


router = BaseRouter()
router.register('production_orders', ProductionOrderViewSet, 'production_order')
router.register('production_records', ProductionRecordViewSet, 'production_record')
urlpatterns = router.urls
