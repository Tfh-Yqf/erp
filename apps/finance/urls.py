from extensions.routers import *
from apps.finance.views import *


router = BaseRouter()
router.register('client_arrears', ClientArrearsViewSet, 'client_arrears')
router.register('supplier_arrears', SupplierArrearsViewSet, 'supplier_arrears')
router.register('payment_orders', PaymentOrderViewSet, 'payment_order')
router.register('collection_orders', CollectionOrderViewSet, 'collection_order')
router.register('charge_orders', ChargeOrderViewSet, 'charge_order')
router.register('account_transfer_records', AccountTransferRecordViewSet, 'account_transfer_record')
urlpatterns = router.urls
