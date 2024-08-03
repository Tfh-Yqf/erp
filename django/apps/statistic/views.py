from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from extensions.models import *
from apps.statistic.serializers import *
from apps.statistic.permissions import *
from apps.statistic.filters import *
from apps.statistic.schemas import *
from apps.statistic.models import *
from apps.purchase.models import *
from apps.sales.models import *
from apps.finance.models import *
from apps.stock_in.models import *
from apps.stock_out.models import *
from apps.goods.models import *
from apps.data.models import *


class PurchaseReportViewSet(BaseViewSet):
    """采购报表"""

    permission_classes = [IsAuthenticated, PurchaseReportPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PurchaseReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = PurchaseGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(purchase_order__is_void=False)

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportStatisticResponse})
    @action(detail=False, methods=['get'])
    def statistics(self, request, *args, **kwargs):
        """统计"""

        queryset = self.filter_queryset(self.get_queryset())
        result = queryset.aggregate(
            total_count=Count('purchase_order', distinct=True),
            total_quantity=Coalesce(Sum('purchase_quantity'), Value(0.0)),
            total_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField()))
        )

        return Response(data=result, status=status.HTTP_200_OK)

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportDetialSerializer})
    @action(detail=False, methods=['get'])
    def detials(self, request, *args, **kwargs):
        """明细"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit', 'purchase_order',
                                           'purchase_order__warehouse', 'purchase_order__supplier',
                                           'purchase_order__creator')
        queryset = self.paginate_queryset(queryset)

        serializer = PurchaseReportDetialSerializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportGroupByGoodsResponse})
    @action(detail=False, methods=['get'])
    def group_by_goods(self, request, *args, **kwargs):
        """产品汇总"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_purchase_quantity=Coalesce(Sum('purchase_quantity'), Value(0.0)),
            total_purchase_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
            min_purchase_price=Min('purchase_price'), avg_purchase_price=Avg('purchase_price'),
            max_purchase_price=Max('purchase_price')
        )
        queryset = self.paginate_queryset(queryset)

        return self.get_paginated_response(queryset)


class SalesReportViewSet(BaseViewSet):
    """销售报表"""

    permission_classes = [IsAuthenticated, SalesReportPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SalesReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = SalesGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(sales_order__is_void=False)

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportStatisticResponse})
    @action(detail=False, methods=['get'])
    def statistics(self, request, *args, **kwargs):
        """统计"""

        queryset = self.filter_queryset(self.get_queryset())
        result = queryset.aggregate(
            total_count=Count('sales_order', distinct=True),
            total_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
            total_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField()))
        )

        return Response(data=result, status=status.HTTP_200_OK)

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportDetialSerializer})
    @action(detail=False, methods=['get'])
    def detials(self, request, *args, **kwargs):
        """明细"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit', 'sales_order',
                                           'sales_order__warehouse', 'sales_order__client',
                                           'sales_order__creator')
        queryset = self.paginate_queryset(queryset)

        serializer = SalesReportDetialSerializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportGroupByGoodsResponse})
    @action(detail=False, methods=['get'])
    def group_by_goods(self, request, *args, **kwargs):
        """产品汇总"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_sales_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
            min_sales_price=Min('sales_price'), avg_sales_price=Avg('sales_price'),
            max_sales_price=Max('sales_price')
        )
        queryset = self.paginate_queryset(queryset)

        return self.get_paginated_response(queryset)


class SalesHotGoodsViewSet(BaseViewSet, ListModelMixin):
    """销售前十产品"""

    permission_classes = [IsAuthenticated, SalesHotGoodsPermission]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesHotGoodsFilter
    queryset = SalesGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(sales_order__is_void=False)

    @extend_schema(parameters=[SalesHotGoodsParameter], responses={200: SalesHotGoodsResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_sales_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
        ).order_by('-total_sales_quantity')[:10]

        return Response(data=queryset, status=status.HTTP_200_OK)


class SalesTrendViewSet(BaseViewSet, ListModelMixin):
    """销售走势"""

    permission_classes = [IsAuthenticated, SalesTrendPermission]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesTrendFilter
    queryset = SalesOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)

    @extend_schema(parameters=[SalesTrendParameter], responses={200: SalesTrendResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('warehouse')
        queryset = queryset.extra(select={'date': connection.ops.date_trunc_sql('day', 'create_time')})
        queryset = queryset.values('warehouse', 'date').annotate(
            warehouse_number=F('warehouse__number'), warehouse_name=F('warehouse__name'),
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
        )

        return Response(data=queryset, status=status.HTTP_200_OK)


class FinanceStatisticViewSet(FunctionViewSet):
    """收支统计"""

    @extend_schema(parameters=[FinanceStatisticParameter], responses={200: FinanceStatisticResponse})
    def list(self, request, *args, **kwargs):
        serializer = FinanceStatisticParameter(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_filters = (
            Q(create_time__gte=serializer.data['start_date']) &
            Q(create_time__lt=serializer.data['end_date']) &
            Q(is_void=False) & Q(team=self.team)
        )

        result = {}
        result |= SalesOrder.objects.filter(query_filters).aggregate(
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= SalesReturnOrder.objects.filter(query_filters).aggregate(
            total_sales_reutrn_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= PurchaseOrder.objects.filter(query_filters).aggregate(
            total_purchase_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= PurchaseReturnOrder.objects.filter(query_filters).aggregate(
            total_purchase_return_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= ChargeOrder.objects.filter(query_filters).filter(type=ChargeOrder.Type.INCOME).aggregate(
            total_income_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= ChargeOrder.objects.filter(query_filters).filter(type=ChargeOrder.Type.EXPENDITURE).aggregate(
            total_expenditure_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))

        return Response(data=result, status=status.HTTP_200_OK)


class PaymentOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """付款明细"""

    serializer_class = PaymentOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentOrderDetialFilter
    queryset = PaymentOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class CollectionOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """收款明细"""

    serializer_class = CollectionOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionOrderDetialFilter
    queryset = CollectionOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class IncomeChargeOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """收入费用明细"""

    serializer_class = IncomeChargeOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeChargeOrderDetialFilter
    queryset = ChargeOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(type=ChargeOrder.Type.INCOME, is_void=False)


class ExpenditureChargeOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """支出费用明细"""

    serializer_class = ExpenditureChargeOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenditureChargeOrderDetialFilter
    queryset = ChargeOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(type=ChargeOrder.Type.EXPENDITURE, is_void=False)


class PurchasePaymentDetialViewSet(BaseViewSet, ListModelMixin):
    """采购付款明细"""

    serializer_class = PurchasePaymentDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchasePaymentDetialFilter
    queryset = PurchaseOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class PurchaseReturnCollectionDetialViewSet(BaseViewSet, ListModelMixin):
    """采购退货收款明细"""

    serializer_class = PurchaseReturnCollectionDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseReturnCollectionDetialFilter
    queryset = PurchaseReturnOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class SalesCollectionDetialViewSet(BaseViewSet, ListModelMixin):
    """销售收款明细"""

    serializer_class = SalesCollectionDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesCollectionDetialFilter
    queryset = SalesOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class SalesReturnPaymentDetialViewSet(BaseViewSet, ListModelMixin):
    """销售退货付款明细"""

    serializer_class = SalesReturnPaymentDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesReturnPaymentDetialFilter
    queryset = SalesReturnOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class HomeOverviewViewSet(BaseViewSet, ListModelMixin):
    """首页概览"""

    @extend_schema(responses={200: HomeViewResponse})
    def list(self, request, *args, **kwargs):
        start_time = pendulum.today().to_datetime_string()
        end_time = pendulum.tomorrow().to_datetime_string()
        data = {
            "sales_count": 0,
            "sales_amount": 0,
            "purchase_count": 0,
            "stock_in_task_count": 0,
            "stock_out_task_count": 0,
            "inventory_warning_count": 0,
            "arrears_receivable_amount": 0,
            "arrears_payable_amount": 0,
        }

        # 销售
        queryset = SalesOrder.objects.filter(create_time__gte=start_time, create_time__lt=end_time,
                                             is_void=False, team=self.team)
        result = queryset.aggregate(sales_count=Count('id'), sales_amount=Sum('total_amount'))
        if result['sales_count'] is not None:
            data['sales_count'] = result['sales_count']

        if result['sales_amount'] is not None:
            data['sales_amount'] = result['sales_amount']

        # 采购
        queryset = PurchaseOrder.objects.filter(create_time__gte=start_time, create_time__lt=end_time,
                                                is_void=False, team=self.team)
        result = queryset.aggregate(purchase_count=Count('id'))
        if result['purchase_count'] is not None:
            data['purchase_count'] = result['purchase_count']

        # 入库
        queryset = StockInOrder.objects.filter(is_completed=False, is_void=False, team=self.team)
        result = queryset.aggregate(stock_in_task_count=Count('id'))
        if result['stock_in_task_count'] is not None:
            data['stock_in_task_count'] = result['stock_in_task_count']

        # 出库
        queryset = StockOutOrder.objects.filter(is_completed=False, is_void=False, team=self.team)
        result = queryset.aggregate(stock_out_task_count=Count('id'))
        if result['stock_out_task_count'] is not None:
            data['stock_out_task_count'] = result['stock_out_task_count']

        # 库存预警
        queryset = Inventory.objects.filter(team=self.team, goods__enable_inventory_warning=True,
                                            total_quantity__gt=F('goods__inventory_upper'),
                                            total_quantity__lt=F('goods__inventory_lower'))
        result = queryset.aggregate(inventory_warning_count=Count('id'))
        if result['inventory_warning_count'] is not None:
            data['inventory_warning_count'] = result['inventory_warning_count']

        # 临期预警
        today_date = pendulum.today().to_date_string()
        queryset = Batch.objects.filter(team=self.team, has_stock=True, goods__enable_batch_control=True,
                                        goods__is_active=True, production_date__isnull=False,
                                        warning_date__lte=today_date, expiration_date__gte=today_date)
        result = queryset.aggregate(expiration_warning_count=Count('id'))
        if result['expiration_warning_count'] is not None:
            data['expiration_warning_count'] = result['expiration_warning_count']

        # 应收欠款
        queryset = Client.objects.filter(is_active=True, has_arrears=True, team=self.team)
        result = queryset.aggregate(arrears_receivable_amount=Sum('arrears_amount'))
        if result['arrears_receivable_amount'] is not None:
            data['arrears_receivable_amount'] = result['arrears_receivable_amount']

        # 应付欠款
        queryset = Supplier.objects.filter(is_active=True, has_arrears=True, team=self.team)
        result = queryset.aggregate(arrears_payable_amount=Sum('arrears_amount'))
        if result['arrears_payable_amount'] is not None:
            data['arrears_payable_amount'] = result['arrears_payable_amount']

        return Response(data=data, status=status.HTTP_200_OK)


__all__ = [
    'PurchaseReportViewSet', 'SalesReportViewSet', 'SalesHotGoodsViewSet',
    'SalesTrendViewSet', 'FinanceStatisticViewSet',
    'PaymentOrderDetialViewSet', 'CollectionOrderDetialViewSet',
    'IncomeChargeOrderDetialViewSet', 'ExpenditureChargeOrderDetialViewSet',
    'PurchasePaymentDetialViewSet', 'PurchaseReturnCollectionDetialViewSet',
    'SalesCollectionDetialViewSet', 'SalesReturnPaymentDetialViewSet',
]
