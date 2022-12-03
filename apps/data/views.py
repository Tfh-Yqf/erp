from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.data.serializers import *
from apps.data.permissions import *
from apps.data.filters import *
from apps.data.schemas import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *


class WarehouseViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """仓库"""

    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['manager', 'is_active']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name']
    ordering = ['number']
    select_related_fields = ['manager']
    queryset = Warehouse.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        warehouse = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for goods in Goods.objects.filter(team=self.team)])

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Warehouse.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(WarehouseImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(WarehouseImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], WarehouseImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        warehouse_items = import_serializer.validated_data

        manager_names = {item['manager']['name'] for item in warehouse_items if 'manager' in item}
        manager_set = User.objects.filter(name__in=manager_names, team=self.team)

        warehouse_numbers = {item['number'] for item in warehouse_items}
        warehouse_set = Warehouse.objects.filter(number__in=warehouse_numbers, team=self.team)

        create_warehouse_set = []
        update_warehouse_set = []
        for warehouse_item in warehouse_items:
            warehouse_item['team'] = self.team

            manager_item = warehouse_item.pop('manager', None)
            if manager_item:
                for manager in manager_set:
                    if manager.name == manager_item['name']:
                        warehouse_item['manager'] = manager
                        break
                else:
                    raise ValidationError(f'管理员缺失[{manager_item["name"]}]')

            for warehouse in warehouse_set:
                if warehouse.number == warehouse_item['number']:
                    update_warehouse_set.append(warehouse)
                    for key, value in warehouse_item.items():
                        setattr(warehouse, key, value)
                    break
            else:
                create_warehouse_set.append(Warehouse(**warehouse_item))
        else:
            try:
                Warehouse.objects.bulk_create(create_warehouse_set)
                Warehouse.objects.bulk_update(update_warehouse_set,
                                              WarehouseImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('编号, 名称重复')

        new_warehouse_numbers = [instance.number for instance in create_warehouse_set]
        new_warehouse_set = Warehouse.objects.filter(number__in=new_warehouse_numbers, team=self.team)
        goods_set = Goods.objects.filter(team=self.team)
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for warehouse in new_warehouse_set
                                       for goods in goods_set])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """客户"""

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    filterset_fields = ['level', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name']
    ordering = ['id']
    queryset = Client.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Client.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(ClientImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(ClientImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], ClientImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        client_items = import_serializer.validated_data
        client_numbers = {item['number'] for item in client_items}
        client_set = Client.objects.filter(number__in=client_numbers, team=self.team)

        create_client_set = []
        update_client_set = []
        for client_item in client_items:
            client_item['team'] = self.team

            for client in client_set:
                if client.number == client_item['number']:
                    update_client_set.append(client)
                    for key, value in client_item.items():
                        setattr(client, key, value)
                    break
            else:
                create_client_set.append(Client(**client_item))
        else:
            try:
                Client.objects.bulk_create(create_client_set)
                Client.objects.bulk_update(update_client_set,
                                           ClientImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('编号, 名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplierViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """供应商"""

    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermission]
    filterset_fields = ['is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name']
    ordering = ['id']
    queryset = Supplier.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Supplier.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(SupplierImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(SupplierImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], SupplierImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        supplier_items = import_serializer.validated_data
        supplier_numbers = {item['number'] for item in supplier_items}
        supplier_set = Supplier.objects.filter(number__in=supplier_numbers, team=self.team)

        create_supplier_set = []
        update_supplier_set = []
        for supplier_item in supplier_items:
            supplier_item['team'] = self.team

            for supplier in supplier_set:
                if supplier.number == supplier_item['number']:
                    update_supplier_set.append(supplier)
                    for key, value in supplier_item.items():
                        setattr(supplier, key, value)
                    break
            else:
                create_supplier_set.append(Supplier(**supplier_item))
        else:
            try:
                Supplier.objects.bulk_create(create_supplier_set)
                Supplier.objects.bulk_update(update_supplier_set,
                                             SupplierImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('编号, 名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """结算账户"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]
    filterset_fields = ['type', 'is_active']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name']
    ordering = ['id']
    queryset = Account.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Account.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(AccountImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(AccountImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], AccountImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        account_items = import_serializer.validated_data
        account_numbers = {item['number'] for item in account_items}
        account_set = Account.objects.filter(number__in=account_numbers, team=self.team)

        create_account_set = []
        update_account_set = []
        for account_item in account_items:
            account_item['team'] = self.team

            for account in account_set:
                if account.number == account_item['number']:
                    update_account_set.append(account)
                    for key, value in account_item.items():
                        setattr(account, key, value)
                    break
            else:
                create_account_set.append(Account(**account_item))
        else:
            try:
                Account.objects.bulk_create(create_account_set)
                Account.objects.bulk_update(update_account_set,
                                            AccountImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('编号, 名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChargeItemViewSet(ModelViewSet, ExportMixin, ImportMixin):
    """收支项目"""

    serializer_class = ChargeItemSerializer
    permission_classes = [IsAuthenticated, ChargeItemPermission]
    filterset_fields = ['type']
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ChargeItem.objects.all()

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        """导出"""

        return self.get_export_response(ChargeItemImportExportSerializer)

    @extend_schema(responses={200: DownloadResponse})
    @action(detail=False, methods=['get'])
    def import_template(self, request, *args, **kwargs):
        """导入模板"""

        return self.get_template_response(ChargeItemImportExportSerializer)

    @extend_schema(request=UploadRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        request_serializer = UploadRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        import_serializer = self.load_data(validated_data['file'], ChargeItemImportExportSerializer)
        if not import_serializer.is_valid(raise_exception=False):
            raise ValidationError('数据错误')

        charge_item_items = import_serializer.validated_data
        charge_item_names = {item['name'] for item in charge_item_items}
        charge_item_set = ChargeItem.objects.filter(name__in=charge_item_names, team=self.team)

        create_charge_item_set = []
        update_charge_item_set = []
        for charge_item_item in charge_item_items:
            charge_item_item['team'] = self.team

            for charge_item in charge_item_set:
                if charge_item.name == charge_item_item['name']:
                    update_charge_item_set.append(charge_item)
                    for key, value in charge_item_item.items():
                        setattr(charge_item, key, value)
                    break
            else:
                create_charge_item_set.append(ChargeItem(**charge_item_item))
        else:
            try:
                ChargeItem.objects.bulk_create(create_charge_item_set)
                ChargeItem.objects.bulk_update(update_charge_item_set,
                                               ChargeItemImportExportSerializer.Meta.fields)
            except IntegrityError:
                raise ValidationError('名称重复')

        return Response(status=status.HTTP_204_NO_CONTENT)


__all__ = [
    'WarehouseViewSet', 'ClientViewSet', 'SupplierViewSet',
    'AccountViewSet', 'ChargeItemViewSet',
]
