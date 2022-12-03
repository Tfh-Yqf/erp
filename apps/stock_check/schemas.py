from extensions.serializers import *


class NumberResponse(Serializer):
    number = CharField(label='编号')


__all__ = [
    'NumberResponse',
]
