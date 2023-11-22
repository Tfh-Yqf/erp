<template>
    <div>
        <a-row :gutter="8" style="margin-top:8px;">
            <a-col :span="6">
                <a-card hoverable>
                    <a-statistic title="销售总金额(元)" :value="statistics.total_sales_amount" :loading="loading" />
                </a-card>
            </a-col>
            <a-col :span="6">
                <a-card hoverable>
                    <a-statistic title="采购总金额(元)" :value="statistics.total_purchase_amount" :loading="loading" />
                </a-card>
            </a-col>

            <a-col :span="6">
                <a-card hoverable>
                    <a-statistic title="现收金额(元)" :value="statistics.total_collection" :loading="loading" />
                </a-card>
            </a-col>

            <a-col :span="6">
                <a-card hoverable>
                    <a-statistic title="现付金额(元)" :value="statistics.total_payment" :loading="loading" />
                </a-card>
            </a-col>


        </a-row>

        <a-row style="margin-top: 12px;">
            <a-col :span="24">
                <a-card title="收款业务">
                    <a-table size="small" :columns="collection.columns" :dataSource="collection.items" rowKey="id"
                        :loading="collection.loading" :pagination="collection.pagination" @change="collection_tableChange">
                        <div slot="action" slot-scope="value, item">
                            <a-button-group size="small">
                                <a-button size="small" @click="collection_detial(item)">详情</a-button>
                                <a-popconfirm title="确定作废吗?" @confirm="collection_voidItem(item)">
                                    <a-button type="danger" :disabled="item.is_void">{{ item.is_void ? '已作废' : '作废'
                                    }}</a-button>
                                </a-popconfirm>
                            </a-button-group>
                        </div>
                    </a-table>
                    <div>收款金额合计：<span style="color: red;">{{ collection.total_amount.toFixed(2) }}</span>（元）</div>
                </a-card>
            </a-col>
        </a-row>

        <a-row style="margin-top: 12px;">
            <a-card title="付款业务">
                <a-table size="small" :columns="payment.columns" :dataSource="payment.items" rowKey="id"
                    :loading="payment.loading" :pagination="payment.pagination" @change="payment_tableChange">
                    <div slot="action" slot-scope="value, item">
                        <a-button-group size="small">
                            <a-button size="small" @click="payment_detial(item)">详情</a-button>
                            <a-popconfirm title="确定作废吗?" @confirm="payment_payment_voidItem(item)">
                                <a-button type="danger" :disabled="item.is_void">{{ item.is_void ? '已作废' : '作废'
                                }}</a-button>
                            </a-popconfirm>
                        </a-button-group>
                    </div>
                </a-table>
                <div>付款金额合计：<span style="color: red;">{{ payment.total_amount.toFixed(2) }}</span>（元）</div>
            </a-card>

        </a-row>
    </div>
</template>

<script>
import { paymentOrdersList, paymentOrdersVoid } from '@/api/finance'
import { purchasePaymentRecord } from '@/api/report'
import { collectionOrdersList, collectionOrdersVoid } from '@/api/finance'
import { financialStatistics } from "@/api/report";
import { salesPaymentRecord } from '@/api/report'
export default {
    data() {
        return {
            loading: true,
            statistics: {
                total_collection: 0,
                total_payment: 0
            },
            collection: {
                columns: [
                    {
                        title: '序号',
                        dataIndex: 'index',
                        key: 'index',
                        customRender: (value, item, index) => {
                            return index + 1
                        },
                        width: 45
                    },
                    {
                        title: '收款编号',
                        dataIndex: 'number',
                        sorter: true,
                    },
                    {
                        title: '客户',
                        dataIndex: 'client_name',
                    },
                    {
                        title: '经手人',
                        dataIndex: 'handler_name',
                    },
                    {
                        title: '处理日期',
                        dataIndex: 'create_time',
                        width: 170
                    },
                    {
                        title: '付款金额(元)',
                        dataIndex: 'total',
                    },
                    {
                        title: '备注',
                        dataIndex: 'remark',
                    },
                    {
                        title: '操作',
                        dataIndex: 'action',
                        scopedSlots: { customRender: 'action' },
                        width: 147
                    },
                ],
                searchForm: { page: 1, page_size: 16 },
                pagination: { current: 1, total: 0, pageSize: 16 },
                loading: false,
                items: [],
                visible: false,
                targetItem: {},
                form: {},
                total_amount: 0
            },
            payment: {
                columns: [
                    {
                        title: '序号',
                        dataIndex: 'index',
                        key: 'index',
                        customRender: (value, item, index) => {
                            return index + 1
                        },
                        width: 45
                    },
                    {
                        title: '单号',
                        dataIndex: 'number',
                        sorter: true,
                    },
                    {
                        title: '供应商',
                        dataIndex: 'supplier_name',
                    },
                    {
                        title: '经手人',
                        dataIndex: 'handler_name',
                    },
                    {
                        title: '处理日期',
                        dataIndex: 'create_time',
                        width: 170
                    },
                    {
                        title: '付款金额(元)',
                        dataIndex: 'total',
                    },
                    {
                        title: '备注',
                        dataIndex: 'remark',
                    },
                    {
                        title: '操作',
                        dataIndex: 'action',
                        scopedSlots: { customRender: 'action' },
                        width: 147
                    },
                ],
                searchForm: { page: 1, page_size: 16 },
                pagination: { current: 1, total: 0, pageSize: 16 },
                loading: false,
                items: [],
                visible: false,
                targetItem: {},
                form: {},
                total_amount: 0
            }
        }

    },
    methods: {
        statistics_initialize() {
            let form = {
                start_date: '2000-01-01',
                end_date: '2100-01-01',
                page: 1,
            }
            financialStatistics(form).then((resp) => {
                this.statistics = { ...resp, ...this.statistics };
                this.statistics.total_sales_amount =  this.statistics.total_sales_amount.toFixed(2);
                this.statistics.total_purchase_amount = this.statistics.total_purchase_amount.toFixed(2);
            }).finally(() => {

            });

            purchasePaymentRecord(form).then(resp => {
                for (var i = 0; i < resp.results.length; i++) {
                    this.statistics.total_payment += parseFloat(resp.results[i].payment_amount);
                }
                this.statistics.total_payment = this.statistics.total_payment.toFixed(2);
            }).finally(() => {
                this.loading = false;
            });

            salesPaymentRecord(form).then(resp => {
                for (var i = 0; i < resp.results.length; i++) {
                    this.statistics.total_collection += parseFloat(resp.results[i].collection_amount);
                }
                this.statistics.total_collection = this.statistics.total_collection.toFixed(2);
            }).finally(() => {
                this.loading = false;
            });
        },
        collection_initialize() {
            this.collection_list();
        },
        collection_list() {
            this.collection.loading = true;
            collectionOrdersList(this.searchForm).then(data => {
                this.collection.pagination.total = data.count;
                this.collection.items = data.results;
                for (var i = 0; i < this.collection.items.length; i++) {
                    var temp = 0;
                    for (var j = 0; j < this.collection.items[i].collection_account_items.length; j++) {
                        temp += parseFloat(this.collection.items[i].collection_account_items[j].collection_amount);
                    }
                    this.collection.items[i].total = temp;
                    this.collection.total_amount += temp;
                }
            }).finally(() => {
                this.collection.loading = false;
            });
        },
        collection_tableChange(pagination, filters, sorter) {
            this.collection.searchForm.page = pagination.current;
            this.collection.pagination.current = pagination.current;
            this.collection.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
            this.collection_list();
        },
        collection_handelAdd(item) {
            this.$router.push({ path: '/finance/collection_create' });
        },
        collection_detial(item) {
            this.$router.push({ path: '/finance/collection_detail', query: { id: item.id } });
        },
        collection_voidItem(item) {
            collectionOrdersVoid({ id: item.id }).then(() => {
                this.$message.success('作废成功');
                this.collection_list();
            });
        },
        payment_initialize() {
            this.payment_list();
        },
        payment_list() {
            this.payment.loading = true;
            paymentOrdersList(this.searchForm).then(data => {
                this.payment.pagination.total = data.count;
                this.payment.items = data.results;
                console.log(this.payment.items)
                for (var i = 0; i < this.payment.items.length; i++) {
                    var temp = 0;
                    for (var j = 0; j < this.payment.items[i].payment_account_items.length; j++) {
                        temp += parseFloat(this.payment.items[i].payment_account_items[j].payment_amount);
                    }
                    this.payment.items[i].total = temp;
                    this.payment.total_amount += temp;
                }
            }).finally(() => {
                this.payment.loading = false;
            });
        },
        payment_tableChange(pagination, filters, sorter) {
            this.payment.searchForm.page = pagination.current;
            this.payment.pagination.current = pagination.current;
            this.payment.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
            this.payment_list();
        },

        payment_handelAdd(item) {
            this.$router.push({ path: '/finance/payment_create' });
        },
        payment_detial(item) {
            this.$router.push({ path: '/finance/payment_detail', query: { id: item.id } });
        },
        payment_voidItem(item) {
            paymentOrdersVoid({ id: item.id }).then(() => {
                this.$message.success('作废成功');
                this.payment_list();
            });
        },
    },
    mounted() {
        this.collection_initialize();
        this.payment_initialize();
        this.statistics_initialize();
    },
}
</script>