<template>
  <div>
    <a-card title="盘点单详情">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />打印</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="盘点编号">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="盘点状态">
              {{ info.status_display }}
            </a-descriptions-item>
            <a-descriptions-item label="仓库">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="账面总数量">
              {{ info.total_book_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="实际总数量">
              {{ info.total_actual_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="盘盈总数量">
              {{ info.total_surplus_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="盘盈总金额">
              {{ info.total_surplus_amount }}
            </a-descriptions-item>
            <a-descriptions-item label="经手人">
              {{ info.handler_name }}
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
            :data-source="info.stock_check_goods_Items"
            :pagination="false">
            <div slot="batch" slot-scope="value, item">
              <a-button v-if="item.enable_batch_control" type="primary" size="small" @click="batchDetial(item)">查看批次</a-button>
            </div>
          </a-table>
        </a-spin>
      </section>
    </a-card>
    <!-- 批次 -->
    <a-modal
      :title="batchTitle"
      v-model="batchVisible"
      width="750px"
      cancelText="关闭"
      :maskClosable="false"
      @cancel="batchVisible=false"
      @ok="confirmChoosed">
      <a-table
        rowkey="id"
        :columns="columnsBatch"
        :data-source="stockCheckBatchItems"
        :pagination="false"
        style="width: 100%">
      </a-table>
    </a-modal>
  </div>
</template>

<script>
  import { stockCheckDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
        receiptOrder: undefined,
        batchTitle: '',
        batchVisible: false,
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
            title: '批次控制',
            dataIndex: 'enable_batch_control',
            key: 'enable_batch_control',
            width: 80,
            customRender: (value, item, index) => {
              return item.isTotal ? '' : (item.enable_batch_control ? '开启' : '未开启')
            },
          },
          {
            title: '实际数量',
            dataIndex: 'actual_quantity',
            key: 'actual_quantity',
            width: 120,
          },
          {
            title: '批次',
            dataIndex: 'batch',
            scopedSlots: { customRender: 'batch' },
            width: 80
          },
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
            dataIndex: 'payment_amount',
            key: 'payment_amount',
            width: 200,
          }
        ],
        columnsBatch: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
          },
          {
            title: "编号",
            dataIndex: "batch_number",
            key: "batch_number",
          },
          {
            title: "实际数量",
            dataIndex: "actual_quantity",
            key: "actual_quantity",
          },
          {
            title: "生产日期",
            dataIndex: "production_date",
            key: "production_date",
          }
        ],
        stockCheckBatchItems: []
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
        stockCheckDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_check_goods_Items = [
            ...this.info.stock_check_goods_Items,
            {
              id: '-1',
              isTotal: true,
              actual_quantity: this.info.total_actual_quantity,
            },
          ];
          this.getJsBarcode(data.number)
        }).finally(() => {
          this.loading = false;
        });
      },
      batchDetial(item,) {
        console.log(item,)
        this.batchTitle = '管理批次';
        this.stockCheckBatchItems = item.stock_check_batch_items;
        this.batchVisible = true;
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
