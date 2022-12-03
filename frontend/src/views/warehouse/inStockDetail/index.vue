<template>
  <div>
    <a-card title="入库通知单详情">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />打印</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="入库编号">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="入库类型">
              {{ info.type_display }}
            </a-descriptions-item>
            <a-descriptions-item label="仓库">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item :label="info.type === 'purchase' ? '采购单据' : (info.type === 'sales_return' ? '销售退货单据' : '调拨单据')">
              {{ info.type === 'purchase' ? info.purchase_order_number : (info.type === 'sales_return' ? info.sales_return_order_number : info.stock_transfer_order_number) }}
            </a-descriptions-item>
            <!-- <a-descriptions-item label="处理日期">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="其他费用">
              {{ info.other_amount }}
            </a-descriptions-item>
            <a-descriptions-item label="备注">
              {{ info.remark }}
            </a-descriptions-item> -->
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">产品信息</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columns"
            :data-source="info.stock_in_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockInOrderDetail } from '@/api/warehouse'
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
            title: '入库总数',
            dataIndex: 'stock_in_quantity',
            key: 'stock_in_quantity',
            width: 120,
          },
          {
            title: '入库剩余数量',
            dataIndex: 'remain_quantity',
            key: 'remain_quantity',
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
        stockInOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_in_goods_items = [
            ...this.info.stock_in_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_in_quantity: this.info.total_quantity,
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
