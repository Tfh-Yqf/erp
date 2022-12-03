<template>
  <div>
    <a-card title="收款单详情">
       <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />打印</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="采购编号">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="客户">
              {{ info.client_name }}
            </a-descriptions-item>
            <a-descriptions-item label="经手人">
              {{ info.handler_name }}
            </a-descriptions-item>
            <a-descriptions-item label="处理日期">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="优惠金额">
              {{ info.discount_amount }}
            </a-descriptions-item>
            <a-descriptions-item label="备注">
              {{ info.remark }}
            </a-descriptions-item>
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">结算账户信息</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columnsAccount"
            :data-source="info.collection_account_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { collectioOrderDetail } from '@/api/finance'
  import JsBarcode from 'jsbarcode'
  import NP from 'number-precision'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
        receiptOrder: undefined,
        info: {},
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: 45,
            customRender: (value, item, index) => {
              return item.isTotal ? '合计' : (index + 1)
            },
          },
          {
            title: '产品名称',
            dataIndex: 'goods_name',
            key: 'goods_name',
            width: 150,
          },
          {
            title: '产品编号',
            dataIndex: 'goods_number',
            key: 'goods_number',
            width: 150,
          },
          {
            title: '单位',
            dataIndex: 'unit_name',
            key: 'unit_name',
            width: 80,
          },
          {
            title: '采购数量',
            dataIndex: 'purchase_quantity',
            key: 'purchase_quantity',
            width: 120,
          },
          {
            title: '采购单价(元)',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            width: 120,
          },
          {
            title: '金额',
            dataIndex: 'totalAmount',
            key: 'totalAmount',
            width: 200,
            customRender: (value, item) => {
              if (item.isTotal) return value;
              value = NP.times(item.purchase_quantity, item.purchase_price);
              return item.id ? NP.round(value, 2) : ''
            },
          }
        ],
        columnsAccount: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: 45,
            customRender: (value, item, index) => {
              return item.isTotal ? '合计' : (index + 1)
            },
          },
          {
            title: '结算账户',
            dataIndex: 'account_name',
            key: 'account_name',
            width: 200,
          },
          {
            title: '付款金额',
            dataIndex: 'collection_amount',
            key: 'collection_amount',
            width: 200,
          }
        ],
      }
    },
    created(){
      this.initData();
    },
    methods: {
      getJsBarcode(number) {
        JsBarcode("#barcode", number, {
          lineColor: '#000',
          width: 2,
          height: 40,
          displayValue: true
        });
      },
      initData() {
        let collectionAmount = 0;
        this.loading = true;
        collectioOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          data.collection_account_items.map(item => { collectionAmount += Number(item.collection_amount) });
          this.info.collection_account_items = [
            ...this.info.collection_account_items,
            {
              id: '-1',
              isTotal: true,
              collection_amount: collectionAmount,
            },
          ];
          this.getJsBarcode(data.number)
        }).finally(() => {
          this.loading = false;
        });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
