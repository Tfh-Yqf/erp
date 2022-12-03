from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    invalid_page_message = '无效页面'


class LimitedPagination(BasePagination):
    max_page_size = 16
    page_size = 16


class InfinitePagination(BasePagination):
    max_page_size = 999999
    page_size = 999999


__all__ = [
    'LimitedPagination', 'InfinitePagination',
]
