from apps.statistic.views import HomeOverviewViewSet
from extensions.routers import *
from apps.statistic.views import *


router = BaseRouter()
router.register('purchase_reports', PurchaseReportViewSet, 'purchase_report')
router.register('sales_reports', SalesReportViewSet, 'sales_report')
router.register('sales_hot_goods', SalesHotGoodsViewSet, 'sales_hot_goods')
router.register('sales_trends', SalesTrendViewSet, 'sales_trend')
router.register('finance_statistics', FinanceStatisticViewSet, 'finance_statistic')
router.register('payment_order_detials', PaymentOrderDetialViewSet, 'payment_order_detial')
router.register('collection_order_detials', CollectionOrderDetialViewSet, 'collection_order_detial')
router.register('income_charge_order_detials', IncomeChargeOrderDetialViewSet, 'income_charge_order_detial')
router.register('expenditure_charge_order_detials', ExpenditureChargeOrderDetialViewSet, 'expenditure_charge_order_detial')
router.register('purchase_payment_detials', PurchasePaymentDetialViewSet, 'purchase_payment_detial')
router.register('purchase_return_collection_detials', PurchaseReturnCollectionDetialViewSet, 'purchase_return_collection_detial')
router.register('sales_collection_detials', SalesCollectionDetialViewSet, 'sales_collection_detial')
router.register('sales_return_payment_detials', SalesReturnPaymentDetialViewSet, 'sales_return_payment_detial')
router.register('home_overview', HomeOverviewViewSet, 'home_overview')
urlpatterns = router.urls
