from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from extensions.exceptions import NotAuthenticated
from apps.system.models import User
from django.conf import settings


class BaseAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # if settings.DEBUG:
        #     return User.objects.all().first(), {}

        if (header := self.get_header(request)) is None:
            return None

        if (raw_token := self.get_raw_token(header)) is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = User.objects.get(id=validated_token['user_id'])
        except KeyError:
            raise NotAuthenticated('令牌不包含用户标识')
        except User.DoesNotExist:
            raise NotAuthenticated('用户不存在')
        except InvalidToken:
            raise NotAuthenticated('令牌无效')

        return user, validated_token


__all__ = [
    'BaseAuthentication',
]
