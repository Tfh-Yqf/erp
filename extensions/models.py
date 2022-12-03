from django.db.models import CharField, DateField, DateTimeField, JSONField, FileField, ImageField
from django.db.models import BooleanField, IntegerField, FloatField, DecimalField
from django.db.models import Sum, Count, Min, Avg, Max, Value, F, Q, Prefetch
from django.db.models.deletion import CASCADE, SET_NULL, SET_DEFAULT, PROTECT
from django.db.models import OneToOneField, ForeignKey, ManyToManyField
from django.db.models import Model, IntegerChoices, TextChoices
from django.db.models.functions import Coalesce
from django.db import connection


class AmountField(DecimalField):
    """金额字段"""

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_digits'], kwargs['decimal_places'] = 16, 2
        super().__init__(verbose_name, name, **kwargs)


__all__ = [
    'Model', 'IntegerChoices', 'TextChoices',
    'CASCADE', 'SET_NULL', 'SET_DEFAULT', 'PROTECT',
    'OneToOneField', 'ForeignKey', 'ManyToManyField',
    'BooleanField', 'IntegerField', 'FloatField', 'AmountField',
    'CharField', 'DateField', 'DateTimeField', 'JSONField', 'FileField', 'ImageField',
    'Sum', 'Count', 'Min', 'Avg', 'Max', 'Value', 
    'F', 'Q', 'Prefetch', 'Coalesce', 'connection',
]
