from extensions.serializers import *


class NumberResponse(Serializer):
    number = CharField(label='编号')


class DownloadResponse(Serializer):
    file = FileField(label='Excel文件')


class UploadRequest(Serializer):
    file = FileField(label='Excel文件')


__all__ = [
    'NumberResponse', 'DownloadResponse', 'UploadRequest',
]
