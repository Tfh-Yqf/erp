<template>
  <div class="panel">
    <a-card title="采购支出明细">
      <a-table :columns="columns" :data-source="items" :loading="loading" :pagination="false" size="small"
        @change="changeOrder" :scroll="{}">
      </a-table>
      <div style="text-align: right; margin-top: 16px;">
        <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" size="small" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { purchasePaymentRecord } from '@/api/report'
  import moment from 'moment'

  export default {
    name: 'PurchaseDetail',
    props: ['start_date', 'end_date'],
    data() {
      return {
        moment,
        searchForm: { page: 1, is_return: false, ordering: '-date' },
        totalRows: 0,
        perPage: 5,
        loading: false,
        items: [],
        columns: [
          {
            title: '单号',
            dataIndex: 'number',
            key: 'number',
            width: 130
          },
          {
            title: '供应商',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
          {
            title: '采购总金额',
            dataIndex: 'total_amount',
            key: 'total_amount',
            width: 100,
          },
          {
            title: '付款金额',
            dataIndex: 'payment_amount',
            key: 'payment_amount',
            width: 100,
          },
          // {
          //   title: '创建日期',
          //   dataIndex: 'create_time',
          //   key: 'create_time',
          //   width: 100,
          //   customRender:function (text) {
          //     return !text?"":(text.length>10?text.substr(0,10):text)
          //   }
          // },
        ],
        tableHeight: window.innerHeight / 2 - 256,
      };
    },
    methods: {
      initialize(start_date, end_date) {
        this.list(start_date, end_date);
      },
      list(start_date, end_date) {
        this.loading = true;
        let form =  {...this.searchForm, ...{ start_date, end_date }};
        if (form.end_date) {
          form.end_date = moment(form.end_date).add(1, 'days').format('YYYY-MM-DD');
        }

        purchasePaymentRecord(form).then(resp => {
          this.totalRows = resp.count;
          this.items = resp.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      changePage(value) {
        this.searchForm.page = value;
        this.list();
      },
      changeOrder(pagination, filters, sorter) {
        this.searchForm.ordering = `${sorter.order == 'ascend' ? '' : '-'}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize(moment().format('YYYY-MM-DD'), moment().format('YYYY-MM-DD'));
    },
  }
</script>

<style>

</style>