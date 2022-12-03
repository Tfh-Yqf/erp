from extensions.routers import *
from apps.flow.views import *


router = BaseRouter()
router.register('inventory_flows', InventoryFlowViewSet, 'inventory_flow')
router.register('finance_flows', FinanceFlowViewSet, 'finance_flow')
urlpatterns = router.urls
