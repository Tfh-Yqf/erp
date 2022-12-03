from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.finance.serializers import *
from apps.finance.permissions import *
from apps.finance.filters import *
from apps.finance.schemas import *
from apps.finance.models import *
from apps.flow.models import *
from apps.data.models import *


class ClientArrearsViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """应收欠款"""

    serializer_class = ClientArrearsSerializer
    permission_classes = [IsAuthenticated, ClientArrearsPermission]
    filterset_fields = ['level', 'is_active', 'has_arrears']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'initial_arrears_amount', 'arrears_amount']
    ordering = ['id']
    queryset = Client.objects.all()


class SupplierArrearsViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """应付欠款"""

    serializer_class = SupplierArrearsSerializer
    permission_classes = [IsAuthenticated, SupplierArrearsPermission]
    filterset_fields = ['is_active', 'has_arrears']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'initial_arrears_amount', 'arrears_amount']
    ordering = ['id']
    queryset = Supplier.objects.all()


class PaymentOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """付款单据"""

    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated, PaymentOrderPermission]
    filterset_class = PaymentOrderFilter
    search_fields = ['number', 'supplier__number', 'supplier__name', 'remark']
    ordering_fields = ['id', 'number', 'total_amount', 'create_time']
    select_related_fields = ['supplier', 'handler', 'creator']
    prefetch_related_fields = ['payment_accounts', 'payment_accounts__account']
    queryset = PaymentOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        payment_order = serializer.save()

        # 同步欠款
        supplier = payment_order.supplier
        supplier.arrears_amount = NP.minus(supplier.arrears_amount, payment_order.total_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步余额, 流水
        finance_flows = []
        for payment_account in payment_order.payment_accounts.all():
            account = payment_account.account
            amount_before = account.balance_amount
            amount_change = payment_account.payment_amount
            amount_after = NP.minus(amount_before, amount_change)

            finance_flows.append(FinanceFlow(
                account=account, type=FinanceFlow.Type.PAYMENT, amount_before=amount_before,
                amount_change=amount_change, amount_after=amount_after, payment_order=payment_order,
                creator=self.user, team=self.team
            ))

            account.balance_amount = amount_after
            if account.balance_amount < 0:
                raise ValidationError(f'结算账户[{account.name}]余额不足')
            account.has_balance = account.balance_amount > 0
            account.save(update_fields=['balance_amount', 'has_balance'])
        else:
            FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PaymentOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: PaymentOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        payment_order = self.get_object()
        payment_order.is_void = True
        payment_order.save(update_fields=['is_void'])

        # 同步欠款
        supplier = payment_order.supplier
        supplier.arrears_amount = NP.plus(supplier.arrears_amount, payment_order.total_amount)
        supplier.has_arrears = supplier.arrears_amount > 0
        supplier.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步余额, 流水
        finance_flows = []
        for payment_account in payment_order.payment_accounts.all():
            account = payment_account.account
            amount_before = account.balance_amount
            amount_change = payment_account.payment_amount
            amount_after = NP.plus(amount_before, amount_change)

            finance_flows.append(FinanceFlow(
                account=account, type=FinanceFlow.Type.VOID_PAYMENT, amount_before=amount_before,
                amount_change=amount_change, amount_after=amount_after, void_payment_order=payment_order,
                creator=self.user, team=self.team
            ))

            account.balance_amount = amount_after
            if account.balance_amount < 0:
                raise ValidationError(f'结算账户[{account.name}]余额不足')
            account.has_balance = account.balance_amount > 0
            account.save(update_fields=['balance_amount', 'has_balance'])
        else:
            FinanceFlow.objects.bulk_create(finance_flows)

        serializer = PaymentOrderSerializer(instance=payment_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CollectionOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """付款单据"""

    serializer_class = CollectionOrderSerializer
    permission_classes = [IsAuthenticated, CollectionOrderPermission]
    filterset_class = CollectionOrderFilter
    search_fields = ['number', 'client__number', 'client__name', 'remark']
    ordering_fields = ['id', 'number', 'total_amount', 'create_time']
    select_related_fields = ['client', 'handler', 'creator']
    prefetch_related_fields = ['collection_accounts', 'collection_accounts__account']
    queryset = CollectionOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        collection_order = serializer.save()

        # 同步欠款
        client = collection_order.client
        client.arrears_amount = NP.minus(client.arrears_amount, collection_order.total_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步余额, 流水
        finance_flows = []
        for collection_account in collection_order.collection_accounts.all():
            account = collection_account.account
            amount_before = account.balance_amount
            amount_change = collection_account.collection_amount
            amount_after = NP.plus(amount_before, amount_change)

            finance_flows.append(FinanceFlow(
                account=account, type=FinanceFlow.Type.COLLECTION, amount_before=amount_before,
                amount_change=amount_change, amount_after=amount_after, collection_order=collection_order,
                creator=self.user, team=self.team
            ))

            account.balance_amount = amount_after
            if account.balance_amount < 0:
                raise ValidationError(f'结算账户[{account.name}]余额不足')
            account.has_balance = account.balance_amount > 0
            account.save(update_fields=['balance_amount', 'has_balance'])
        else:
            FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PaymentOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: CollectionOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        collection_order = self.get_object()
        collection_order.is_void = True
        collection_order.save(update_fields=['is_void'])

        # 同步欠款
        client = collection_order.client
        client.arrears_amount = NP.plus(client.arrears_amount, collection_order.total_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 同步余额, 流水
        finance_flows = []
        for collection_account in collection_order.collection_accounts.all():
            account = collection_account.account
            amount_before = account.balance_amount
            amount_change = collection_account.collection_amount
            amount_after = NP.minus(amount_before, amount_change)

            finance_flows.append(FinanceFlow(
                account=account, type=FinanceFlow.Type.VOID_COLLECTION, amount_before=amount_before,
                amount_change=amount_change, amount_after=amount_after, void_collection_order=collection_order,
                creator=self.user, team=self.team
            ))

            account.balance_amount = amount_after
            if account.balance_amount < 0:
                raise ValidationError(f'结算账户[{account.name}]余额不足')
            account.has_balance = account.balance_amount > 0
            account.save(update_fields=['balance_amount', 'has_balance'])
        else:
            FinanceFlow.objects.bulk_create(finance_flows)

        serializer = CollectionOrderSerializer(instance=collection_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChargeOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """收支单据"""

    serializer_class = ChargeOrderSerializer
    permission_classes = [IsAuthenticated, ChargeOrderPermission]
    filterset_class = ChargeOrderFilter
    search_fields = ['number', 'supplier__number', 'supplier__name', 'client__number',
                     'client__name', 'remark']
    ordering_fields = ['id', 'number', 'total_amount', 'charge_amount', 'create_time']
    select_related_fields = ['supplier', 'client', 'handler', 'creator']
    queryset = ChargeOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        charge_order = serializer.save()

        account = charge_order.account
        amount_before = account.balance_amount
        arrears_amount = NP.minus(charge_order.total_amount, charge_order.charge_amount)
        if charge_order.type == ChargeOrder.Type.INCOME:
            amount_change = charge_order.charge_amount

            # 同步欠款
            if supplier := charge_order.supplier:
                supplier.arrears_amount = NP.minus(supplier.arrears_amount, arrears_amount)
                supplier.has_arrears = supplier.arrears_amount > 0
                supplier.save(update_fields=['arrears_amount', 'has_arrears'])
            elif client := charge_order.client:
                client.arrears_amount = NP.plus(client.arrears_amount, arrears_amount)
                client.has_arrears = client.arrears_amount > 0
                client.save(update_fields=['arrears_amount', 'has_arrears'])
        elif charge_order.type == ChargeOrder.Type.EXPENDITURE:
            amount_change = -charge_order.charge_amount

            # 同步欠款
            if supplier := charge_order.supplier:
                supplier.arrears_amount = NP.plus(supplier.arrears_amount, arrears_amount)
                supplier.has_arrears = supplier.arrears_amount > 0
                supplier.save(update_fields=['arrears_amount', 'has_arrears'])
            elif client := charge_order.client:
                client.arrears_amount = NP.minus(client.arrears_amount, arrears_amount)
                client.has_arrears = client.arrears_amount > 0
                client.save(update_fields=['arrears_amount', 'has_arrears'])

        amount_after = NP.plus(amount_before, amount_change)
        FinanceFlow.objects.create(
            account=account, type=FinanceFlow.Type.CHARGE, amount_before=amount_before,
            amount_change=amount_change, amount_after=amount_after, charge_order=charge_order,
            creator=self.user, team=self.team
        )

        account.balance_amount = amount_after
        if account.balance_amount < 0:
            raise ValidationError(f'结算账户[{account.name}]余额不足')
        account.has_balance = account.balance_amount > 0
        account.save(update_fields=['balance_amount', 'has_balance'])

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = ChargeOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: ChargeOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        charge_order = self.get_object()
        charge_order.is_void = True
        charge_order.save(update_fields=['is_void'])

        account = charge_order.account
        amount_before = account.balance_amount
        arrears_amount = NP.minus(charge_order.total_amount, charge_order.charge_amount)
        if charge_order.type == ChargeOrder.Type.INCOME:
            amount_change = charge_order.charge_amount

            # 同步欠款
            if supplier := charge_order.supplier:
                supplier.arrears_amount = NP.plus(supplier.arrears_amount, arrears_amount)
                supplier.has_arrears = supplier.arrears_amount > 0
                supplier.save(update_fields=['arrears_amount', 'has_arrears'])
            elif client := charge_order.client:
                client.arrears_amount = NP.minus(client.arrears_amount, arrears_amount)
                client.has_arrears = client.arrears_amount > 0
                client.save(update_fields=['arrears_amount', 'has_arrears'])
        elif charge_order.type == ChargeOrder.Type.EXPENDITURE:
            amount_change = -charge_order.charge_amount

            # 同步欠款
            if supplier := charge_order.supplier:
                supplier.arrears_amount = NP.minus(supplier.arrears_amount, arrears_amount)
                supplier.has_arrears = supplier.arrears_amount > 0
                supplier.save(update_fields=['arrears_amount', 'has_arrears'])
            elif client := charge_order.client:
                client.arrears_amount = NP.plus(client.arrears_amount, arrears_amount)
                client.has_arrears = client.arrears_amount > 0
                client.save(update_fields=['arrears_amount', 'has_arrears'])

        amount_after = NP.minus(amount_before, amount_change)
        FinanceFlow.objects.create(
            account=account, type=FinanceFlow.Type.VOID_CHARGE, amount_before=amount_before,
            amount_change=amount_change, amount_after=amount_after, void_charge_order=charge_order,
            creator=self.user, team=self.team
        )

        account.balance_amount = amount_after
        if account.balance_amount < 0:
            raise ValidationError(f'结算账户[{account.name}]余额不足')

        account.has_balance = account.balance_amount > 0
        account.save(update_fields=['balance_amount', 'has_balance'])

        serializer = ChargeOrderSerializer(instance=charge_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AccountTransferRecordViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """结算账户转账记录"""

    serializer_class = AccountTransferRecordSerializer
    permission_classes = [IsAuthenticated, AccountTransferRecordPermission]
    filterset_class = AccountTransferRecordFilter
    search_fields = ['out_account__number', 'out_account__name', 'in_account__number',
                     'in_account__name', 'remark']
    ordering_fields = ['id', 'transfer_out_time', 'transfer_in_time', 'create_time']
    select_related_fields = ['out_account', 'in_account', 'handler', 'creator']
    queryset = AccountTransferRecord.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        account_transfer_record = serializer.save()

        out_account = account_transfer_record.out_account
        transfer_out_amount = account_transfer_record.transfer_amount
        in_account = account_transfer_record.in_account
        transfer_in_amount = account_transfer_record.transfer_amount

        service_charge_payer = account_transfer_record.service_charge_payer
        if service_charge_payer == AccountTransferRecord.ServiceChargePayer.TRANSFER_IN:
            transfer_in_amount = NP.minus(transfer_in_amount,
                                          account_transfer_record.service_charge_amount)
        elif service_charge_payer == AccountTransferRecord.ServiceChargePayer.TRANSFER_OUT:
            transfer_out_amount = NP.minus(transfer_out_amount,
                                           account_transfer_record.service_charge_amount)

        # 同步账户余额
        finance_flows = []
        amount_before = out_account.balance_amount
        amount_change = transfer_out_amount
        amount_after = NP.minus(amount_before, transfer_out_amount)
        finance_flows.append(FinanceFlow(
            account=out_account, type=FinanceFlow.Type.ACCOUNT_TRANSFER_OUT,
            amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
            account_transfer_record=account_transfer_record, creator=self.user, team=self.team
        ))

        out_account.balance_amount = amount_after
        if out_account.balance_amount < 0:
            raise ValidationError(f'结算账户[{out_account.name}]余额不足')
        out_account.has_balance = out_account.balance_amount > 0
        out_account.save(update_fields=['balance_amount', 'has_balance'])

        amount_before = in_account.balance_amount
        amount_change = transfer_in_amount
        amount_after = NP.plus(amount_before, transfer_in_amount)
        finance_flows.append(FinanceFlow(
            account=in_account, type=FinanceFlow.Type.ACCOUNT_TRANSFER_IN,
            amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
            account_transfer_record=account_transfer_record, creator=self.user, team=self.team
        ))

        in_account.balance_amount = amount_after
        if in_account.balance_amount < 0:
            raise ValidationError(f'结算账户[{in_account.name}]余额不足')
        in_account.has_balance = in_account.balance_amount > 0
        in_account.save(update_fields=['balance_amount', 'has_balance'])

    @transaction.atomic
    @extend_schema(request=None, responses={200: AccountTransferRecordSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        account_transfer_record = self.get_object()
        account_transfer_record.is_void = True
        account_transfer_record.save(update_fields=['is_void'])

        out_account = account_transfer_record.out_account
        transfer_out_amount = account_transfer_record.transfer_amount
        in_account = account_transfer_record.in_account
        transfer_in_amount = account_transfer_record.transfer_amount

        service_charge_payer = account_transfer_record.service_charge_payer
        if service_charge_payer == AccountTransferRecord.ServiceChargePayer.TRANSFER_IN:
            transfer_in_amount = NP.minus(transfer_in_amount,
                                          account_transfer_record.service_charge_amount)
        elif service_charge_payer == AccountTransferRecord.ServiceChargePayer.TRANSFER_OUT:
            transfer_out_amount = NP.minus(transfer_out_amount,
                                           account_transfer_record.service_charge_amount)

        # 同步账户余额
        finance_flows = []
        amount_before = out_account.balance_amount
        amount_change = transfer_out_amount
        amount_after = NP.plus(amount_before, transfer_out_amount)
        finance_flows.append(FinanceFlow(
            account=out_account, type=FinanceFlow.Type.VOID_ACCOUNT_TRANSFER_OUT,
            amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
            void_account_transfer_record=account_transfer_record, creator=self.user, team=self.team
        ))

        out_account.balance_amount = amount_after
        if out_account.balance_amount < 0:
            raise ValidationError(f'结算账户[{out_account.name}]余额不足')
        out_account.has_balance = out_account.balance_amount > 0
        out_account.save(update_fields=['balance_amount', 'has_balance'])

        amount_before = in_account.balance_amount
        amount_change = transfer_in_amount
        amount_after = NP.minus(amount_before, transfer_in_amount)
        finance_flows.append(FinanceFlow(
            account=in_account, type=FinanceFlow.Type.VOID_ACCOUNT_TRANSFER_IN,
            amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
            void_account_transfer_record=account_transfer_record, creator=self.user, team=self.team
        ))

        in_account.balance_amount = amount_after
        if in_account.balance_amount < 0:
            raise ValidationError(f'结算账户[{in_account.name}]余额不足')
        in_account.has_balance = in_account.balance_amount > 0
        in_account.save(update_fields=['balance_amount', 'has_balance'])

        serializer = AccountTransferRecordSerializer(instance=account_transfer_record)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'ClientArrearsViewSet', 'SupplierArrearsViewSet',
    'PaymentOrderViewSet', 'CollectionOrderViewSet',
    'ChargeOrderViewSet', 'AccountTransferRecordViewSet',
]
