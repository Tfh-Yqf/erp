from rest_framework.permissions import BasePermission
from extensions.exceptions import ValidationError
from apps.system.models import User
from apps.manage.models import SuperUser
import pendulum


class IsSuperUser(BasePermission):
    message = '未登陆验证'

    def has_permission(self, request, view):
        if not isinstance(request.user, SuperUser):
            return False

        return True


class IsAuthenticated(BasePermission):
    message = '未登陆验证'

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        if (expiry_time := request.user.team.expiry_time) < pendulum.now():
            raise ValidationError(f'已到期, 到期日期: {expiry_time}')

        if not (request.user.is_manager or request.user.is_active):
            raise ValidationError('账号未激活, 无法执行任何操作')

        return True


class IsManagerPermission(BasePermission):
    message = '非管理员账号'

    def has_permission(self, request, view):
        return request.user.is_manager


class ModelPermission(BasePermission):
    message = '未添加操作权限'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class FunctionPermission(BasePermission):
    """功能权限"""

    message = '未添加操作权限'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class DataPermission:
    """数据权限"""

    @classmethod
    def has_permission(cls, request):
        if request.user.is_manager:
            return True

        if cls.code in request.user.permissions:
            return True
        return False


__all__ = [
    'IsSuperUser', 'IsAuthenticated', 'IsManagerPermission',
    'ModelPermission', 'FunctionPermission', 'DataPermission',
]
