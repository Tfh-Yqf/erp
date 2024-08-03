from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import APIException
from django.db.utils import IntegrityError
from rest_framework import status


class AuthenticationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '身份验证失败'
    default_code = 'authentication_failed'


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '未通过身份验证'
    default_code = 'not_authenticated'


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '无效请求'
    default_code = 'invalid'


class ParseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '格式错误'
    default_code = 'parse_error'


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '无权限执行操作.'
    default_code = 'permission_denied'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '数据不存在'
    default_code = 'not_found'


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '服务器错误'
    default_code = 'server_error'


__all__ = [
    'ProtectedError', 'IntegrityError',
    'AuthenticationFailed', 'NotAuthenticated', 'ValidationError', 'ParseError',
    'PermissionDenied', 'NotFound', 'ServerError',
]
