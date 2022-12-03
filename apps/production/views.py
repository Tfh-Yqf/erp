from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.production.serializers import *
from apps.production.permissions import *
from apps.production.filters import *
from apps.production.schemas import *
from apps.production.models import *


class ProductionOrderViewSet(ModelViewSet):
    """生产单据"""

    serializer_class = ProductionOrderSerializer
    permission_classes = [IsAuthenticated, ProductionOrderPermission]
    filterset_class = ProductionOrderFilter
    search_fields = ['number', 'sales_order__number', 'goods__number', 'goods__name']
    ordering_fields = ['number', 'total_quantity', 'quantity_produced', 'remain_quantity',
                       'start_time', 'end_time', 'create_time']
    select_related_fields = ['sales_order', 'goods', 'creator']
    prefetch_related_fields = ['sales_order__sales_goods_set']
    queryset = ProductionOrder.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.status != ProductionOrder.Status.IN_PLAN:
            raise ValidationError(f'工单{instance.number}{instance.get_status_display()}, 无法编辑')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.status != ProductionOrder.Status.IN_PLAN:
            raise ValidationError(f'工单{instance.number}{instance.get_status_display()}, 无法删除')
        return super().perform_destroy(instance)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = ProductionOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: ProductionOrderSerializer})
    @action(detail=True, methods=['post'])
    def issue(self, request, *args, **kwargs):
        """发布工单"""

        instance = self.get_object()
        if instance.status != ProductionOrder.Status.IN_PLAN:
            raise ValidationError(f'工单{instance.number}{instance.get_status_display()}, 无法发布工单')

        instance.status = ProductionOrder.Status.IN_PROGRESS
        instance.save(update_fields=['status'])

        serializer = ProductionOrderSerializer(instance=instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: ProductionOrderSerializer})
    @action(detail=True, methods=['post'])
    def close(self, request, *args, **kwargs):
        """关闭工单"""

        instance = self.get_object()
        if instance.status != ProductionOrder.Status.IN_PROGRESS:
            raise ValidationError(f'工单{instance.number}{instance.get_status_display()}, 无法关闭工单')

        instance.status = ProductionOrder.Status.CLOSED
        instance.save(update_fields=['status'])

        serializer = ProductionOrderSerializer(instance=instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductionRecordViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """生产记录"""

    serializer_class = ProductionRecordSerializer
    permission_classes = [IsAuthenticated, ProductionRecordPermission]
    filterset_class = ProductionRecordFilter
    search_fields = ['production_order__number', 'goods__number', 'goods__name']
    ordering_fields = ['production_quantity', 'create_time']
    select_related_fields = ['production_order', 'goods', 'creator']
    queryset = ProductionRecord.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        production_order = validated_data['production_order']
        production_quantity = validated_data['production_quantity']

        if production_order.remain_quantity < production_quantity:
            raise ValidationError('生产数量错误')

        production_order.quantity_produced = NP.plus(production_order.quantity_produced, production_quantity)
        production_order.remain_quantity = NP.minus(production_order.remain_quantity, production_quantity)
        if production_order.remain_quantity == 0:
            production_order.status = ProductionOrder.Status.COMPLETED
        production_order.save(update_fields=['quantity_produced', 'remain_quantity', 'status'])

        serializer.save()


__all__ = [
    'ProductionOrderViewSet', 'ProductionRecordViewSet',
]
