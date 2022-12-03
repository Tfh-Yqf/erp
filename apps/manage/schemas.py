from extensions.serializers import *


class CSRFTokenResponse(Serializer):
    token = CharField(label='令牌')


class LoginRequest(Serializer):
    username = CharField(label='用户名')
    password = CharField(label='密码')


class SuperUserInfoResponse(Serializer):
    id = IntegerField(label='用户ID')
    username = CharField(label='用户名')


class TeamCreateRequest(Serializer):
    number = CharField(max_length=32, label='公司编号')
    expiry_time = DateTimeField(label='到期时间')
    user_quantity = IntegerField(label='用户数量')
    username = CharField(max_length=32, label='用户名')
    password = CharField(max_length=256, label='密码')
    name = CharField(max_length=64, label='名称')


__all__ = [
    'CSRFTokenResponse', 'LoginRequest', 'SuperUserInfoResponse', 'TeamCreateRequest',
]
