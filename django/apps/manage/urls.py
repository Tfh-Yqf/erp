from extensions.routers import *
from apps.manage.views import *


router = BaseRouter()
router.register('super_user', SuperUserActionViewSet, 'super_user_action')
router.register('teams', TeamViewSet, 'team')
router.register('devices', DeviceViewSet, 'device')
urlpatterns = router.urls
