from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.goods.serializers import *
from apps.goods.permissions import *
from apps.goods.filters import *
from apps.goods.schemas import *
from apps.goods.models import *
from apps.data.models import *


class GoodsCategoryViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """产品分类"""

    serializer_class = GoodsCategorySerializer
    permission_classes = [IsAuthenticated, GoodsCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsCategory.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(GoodsCategoryImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(GoodsCategoryImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], GoodsCategoryImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        goods_category_items = import_serializer.validated_data
        goods_category_names = {item['name'] for item in goods_category_items}
        goods_category_set = GoodsCategory.objects.filter(name__in=goods_category_names, team=self.team)

        create_goods_category_set = []
        update_goods_category_set = []
        for goods_category_item in goods_category_items:
            goods_category_item['team'] = self.team

            for goods_category in goods_category_set:
                if goods_category.name == goods_category_item['name']:
                    update_goods_category_set.append(goods_category)
                    for key, value in goods_category_item.items():
                        setattr(goods_category, key, value)
                    break
            else:
                create_goods_category_set.append(GoodsCategory(**goods_category_item))
        else:
            try:
                GoodsCategory.objects.bulk_create(create_goods_category_set)
                GoodsCategory.objects.bulk_update(update_goods_category_set,
                                                  GoodsCategoryImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoodsUnitViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """产品单位"""

    serializer_class = GoodsUnitSerializer
    permission_classes = [IsAuthenticated, GoodsUnitPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsUnit.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(GoodsUnitImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(GoodsUnitImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], GoodsUnitImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        goods_unit_items = import_serializer.validated_data
        goods_unit_names = {item['name'] for item in goods_unit_items}
        goods_unit_set = GoodsUnit.objects.filter(name__in=goods_unit_names, team=self.team)

        create_goods_unit_set = []
        update_goods_unit_set = []
        for goods_unit_item in goods_unit_items:
            goods_unit_item['team'] = self.team

            for goods_unit in goods_unit_set:
                if goods_unit.name == goods_unit_item['name']:
                    update_goods_unit_set.append(goods_unit)
                    for key, value in goods_unit_item.items():
                        setattr(goods_unit, key, value)
                    break
            else:
                create_goods_unit_set.append(GoodsUnit(**goods_unit_item))
        else:
            try:
                GoodsUnit.objects.bulk_create(create_goods_unit_set)
                GoodsUnit.objects.bulk_update(update_goods_unit_set,
                                              GoodsUnitImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoodsViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """产品"""

    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, GoodsPermission]
    filterset_fields = ['number', 'category', 'is_active']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name']
    ordering = ['id']
    select_related_fields = ['category', 'unit']
    prefetch_related_fields = ['inventories', 'inventories__warehouse', 'inventories__batchs', 'goods_images']
    queryset = Goods.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Goods.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(GoodsImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(GoodsImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], GoodsImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        goods_items = import_serializer.validated_data
        category_names = {item['category']['name'] for item in goods_items if 'category' in item}
        category_set = GoodsCategory.objects.filter(name__in=category_names, team=self.team)

        unit_names = {item['unit']['name'] for item in goods_items if 'unit' in item}
        unit_set = GoodsUnit.objects.filter(name__in=unit_names, team=self.team)

        goods_numbers = {item['number'] for item in goods_items}
        goods_set = Goods.objects.filter(number__in=goods_numbers, team=self.team)

        create_goods_set = []
        update_goods_set = []
        for goods_item in goods_items:
            goods_item['team'] = self.team

            category_item = goods_item.pop('category', None)
            if category_item:
                for category in category_set:
                    if category.name == category_item['name']:
                        goods_item['category'] = category
                        break
                else:
                    raise ValidationError(f'分类缺失[{category_item["name"]}]')

            unit_item = goods_item.pop('unit', None)
            if unit_item:
                for unit in unit_set:
                    if unit.name == unit_item['name']:
                        goods_item['unit'] = unit
                        break
                else:
                    raise ValidationError(f'单位缺失[{unit_item["name"]}]')

            for goods in goods_set:
                if goods.number == goods_item['number']:
                    update_goods_set.append(goods)
                    for key, value in goods_item.items():
                        setattr(goods, key, value)
                    break
            else:
                create_goods_set.append(Goods(**goods_item))
        else:
            try:
                Goods.objects.bulk_create(create_goods_set)
                Goods.objects.bulk_update(update_goods_set,
                                          GoodsImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('编号重复')

        new_goods_numbers = [instance.number for instance in create_goods_set]
        new_goods_set = Goods.objects.filter(number__in=new_goods_numbers, team=self.team)
        warehouse_set = Warehouse.objects.filter(team=self.team)
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for goods in new_goods_set
                                       for warehouse in warehouse_set])

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoodsImageViewSet(ModelViewSet):
    """产品图片"""

    serializer_class = GoodsImageSerializer
    permission_classes = [IsAuthenticated, GoodsPermission]
    search_fields = ['name']
    queryset = GoodsImage.objects.all()


class BatchViewSet(BaseViewSet, ReadOnlyMixin):
    """批次"""

    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated, BatchPermission]
    filterset_class = BatchFilter
    search_fields = ['number', 'goods__number', 'goods__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'production_date',
                       'expiration_date', 'create_time']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Batch.objects.all()


class InventoryViewSet(BaseViewSet, ReadOnlyMixin):
    """库存"""

    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission]
    filterset_fields = ['warehouse', 'goods', 'has_stock']
    search_fields = ['goods__number', 'goods__name']
    ordering_fields = ['id', 'total_quantity']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Inventory.objects.all()


__all__ = [
    'GoodsCategoryViewSet', 'GoodsUnitViewSet', 'GoodsViewSet', 'GoodsImageViewSet',
    'BatchViewSet', 'InventoryViewSet',
]
