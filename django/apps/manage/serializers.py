from extensions.common.base import *
from extensions.exceptions import *
from apps.manage.models import *
from apps.system.models import *
from rest_framework.serializers import ModelSerializer


class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        read_only_fields = ['id', 'create_time']
        fields = ['number', 'expiry_time', 'user_quantity', 'remark', *read_only_fields]

    def validate_number(self, value):
        queryset = Team.objects.filter(number=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise ValidationError(f'公司编号[{value}]已存在')
        return value


class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        read_only_fields = ['id']
        fields = ['number', 'name', 'model', 'serial_number', 'account_ownership', *read_only_fields]


__all__ = [
    'TeamSerializer', 'DeviceSerializer',
]
