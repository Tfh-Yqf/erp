<template>
  <div>
    <a-card title="出库通知单详情">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />打印</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="出库编号">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="出库类型">
              {{ info.type_display }}
            </a-descriptions-item>
            <a-descriptions-item label="仓库">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item :label="info.type === 'purchase' ? '采购退货单据' : (info.type === 'sales' ? '销售单据' : '调拨单据')">
              {{ info.type === 'purchase' ? info.purchase_return_order_number : (info.type === 'sales' ? info.sales_order_number : info.stock_transfer_order_number) }}
            </a-descriptions-item>
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">产品信息</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columns"
            :data-source="info.stock_out_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockOutOrderDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
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
            title: '出库数量',
            dataIndex: 'stock_out_quantity',
            key: 'stock_out_quantity',
            width: 120,
          },
          {
            title: '出库剩余数量',
            dataIndex: 'remain_quantity',
            key: 'remain_quantity',
            width: 120,
          },
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
        this.loading = true;
        stockOutOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_out_goods_items = [
            ...this.info.stock_out_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_out_quantity: this.info.total_quantity,
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
