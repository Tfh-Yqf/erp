<template>
  <div>
    <a-card title="入库记录详情">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />打印</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="入库编号">
              {{ info.stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="经手人">
              {{ info.handler_name }}
            </a-descriptions-item>
            <a-descriptions-item label="经手日期">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="仓库">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="处理日期">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="备注">
              {{ info.remark }}
            </a-descriptions-item>
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">产品信息</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columns"
            :data-source="info.stock_in_record_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockInRecordDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'
  import NP from 'number-precision'

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
            title: '入库数量',
            dataIndex: 'stock_in_quantity',
            key: 'stock_in_quantity',
            width: 120,
          },
          {
            title: '编号批次',
            dataIndex: 'batch_number',
            key: 'batch_number',
            width: 120,
          },
          {
            title: '生产日期',
            dataIndex: 'production_date',
            key: 'production_date',
            width: 120,
          },
          {
            title: '过期日期',
            dataIndex: 'expiration_date',
            key: 'expiration_date',
            width: 120,
          },
          {
            title: '保质期天数',
            dataIndex: 'shelf_life_days',
            key: 'shelf_life_days',
            width: 120,
          },
          // {
          //   title: '金额',
          //   dataIndex: 'totalAmount',
          //   key: 'totalAmount',
          //   width: 200,
          //   customRender: (value, item) => {
          //     if (item.isTotal) return value;
          //     value = NP.times(item.stock_in_quantity, item.purchase_price);
          //     return item.id ? NP.round(value, 2) : ''
          //   },
          // }
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
        stockInRecordDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_in_record_goods_items = [
            ...this.info.stock_in_record_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_in_quantity: this.info.total_quantity,
            },
          ];
          this.getJsBarcode(data.stock_in_order_number)
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
