from rest_framework.fields import SerializerMethodField, ImageField, FileField, JSONField
from rest_framework.fields import IntegerField, FloatField, DecimalField, BooleanField
from rest_framework.fields import CharField, DateField, DateTimeField
from rest_framework.serializers import Serializer, ModelSerializer
from extensions.exceptions import ValidationError


class BaseSerializer(ModelSerializer):

    @property
    def request(self):
        return self.context['request']

    @property
    def team(self):
        return self.context['request'].user.team

    @property
    def user(self):
        return self.context['request'].user

    def validate_foreign_key(self, model, instance, message):
        if instance:
            if not (instance := model.objects.filter(id=instance.id, team=self.team).first()):
                raise ValidationError(message)
        return instance

    def validate_foreign_key_set(self, model, instances, message):
        if instances:
            instance_ids = [instance.id for instance in instances]
            instances = model.objects.filter(id__in=instance_ids, team=self.team)

            if len(instance_ids) != len(instances):
                raise ValidationError(message)
        return instances

    def validate_unique(self, fields, message):
        queryset = self.Meta.model.objects.filter(team=self.team, **fields)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise ValidationError(message)

    def create(self, validated_data):
        validated_data['team'] = self.team
        return super().create(validated_data)


class AmountField(DecimalField):
    """金额字段"""

    def __init__(self, coerce_to_string=None, max_value=None, min_value=None, localize=False,
                 rounding=None, **kwargs):

        kwargs['max_digits'], kwargs['decimal_places'] = 16, 2
        super().__init__(coerce_to_string=coerce_to_string, max_value=max_value, min_value=min_value,
                         localize=localize, rounding=rounding, **kwargs)


__all__ = [
    'Serializer', 'ModelSerializer', 'BaseSerializer',
    'SerializerMethodField', 'ImageField', 'FileField', 'JSONField',
    'BooleanField', 'IntegerField', 'FloatField', 'AmountField',
    'CharField', 'DateField', 'DateTimeField',
]
