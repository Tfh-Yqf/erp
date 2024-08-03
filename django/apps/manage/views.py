from rest_framework.viewsets import ViewSet, ModelViewSet
from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.paginations import *
from apps.manage.serializers import *
from apps.manage.schemas import *
from apps.manage.models import *
from apps.system.models import *
from django.contrib import auth
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password


class SuperUserActionViewSet(ViewSet):
    """管理员操作"""

    @extend_schema(responses={200: CSRFTokenResponse})
    @action(detail=False, methods=['get'])
    def get_csrf_token(self, request, *args, **kwargs):
        """获取csrf令牌"""

        return Response({'token': get_token(request)})

    @extend_schema(request=LoginRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """登录"""

        serializer = LoginRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']

        if not (super_user := auth.authenticate(username=username, password=password)):
            raise ValidationError('账号密码错误')

        auth.login(request, super_user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        """登出"""

        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={200: SuperUserInfoResponse})
    @action(detail=False, methods=['get'], permission_classes=[IsSuperUser])
    def info(self, request, *args, **kwargs):
        """用户信息"""

        warning_date = pendulum.today().add(days=30).to_datetime_string()
        results = Team.objects.filter(expiry_time__lte=warning_date).values('number', 'expiry_time',
                                                                            'create_time', 'remark')

        serializer = SuperUserInfoResponse(instance=request.user)
        data = serializer.data
        data['warning_list'] = results

        return Response(data=data, status=status.HTTP_200_OK)


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    pagination_class = LimitedPagination
    permission_classes = [IsSuperUser]
    search_fields = ['number', 'remark']
    ordering_fields = ['id', 'number', 'expiry_time', 'create_time']
    queryset = Team.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        team_serializer = TeamCreateRequest(data=self.request.data)
        team_serializer.is_valid(raise_exception=True)

        validated_data = team_serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']
        password = make_password(password)
        name = validated_data['name']

        team = serializer.save()
        User.objects.create(username=username, password=password, name=name, is_manager=True, team=team)

    @extend_schema(request=TeamCreateRequest, responses={200: TeamSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    pagination_class = LimitedPagination
    permission_classes = [IsSuperUser]
    search_fields = ['number', 'name', 'serial_number']
    ordering_fields = ['id', 'number', 'name', 'serial_number']
    queryset = Device.objects.all()


__all__ = [
    'SuperUserActionViewSet', 'TeamViewSet', 'DeviceViewSet',
]
