from extensions.routers import *
from apps.message.views import *


router = BaseRouter()
router.register('inventory_warnings', InventoryWarningViewSet, 'inventory_warning')
router.register('stock_in_order_reminders', StockInOrderReminderViewSet, 'stock_in_order_reminder')
router.register('stock_out_order_reminders', StockOutOrderReminderViewSet, 'stock_out_order_reminder')
urlpatterns = router.urls
