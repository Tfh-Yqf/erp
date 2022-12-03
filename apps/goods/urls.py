from extensions.routers import *
from apps.goods.views import *


router = BaseRouter()
router.register('goods_categories', GoodsCategoryViewSet, 'goods_category')
router.register('goods_units', GoodsUnitViewSet, 'goods_unit')
router.register('goods', GoodsViewSet, 'goods')
router.register('goods_images', GoodsImageViewSet, 'goods_image')
router.register('batchs', BatchViewSet, 'batch')
router.register('inventories', InventoryViewSet, 'inventory')
urlpatterns = router.urls
