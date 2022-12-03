<template>
  <div>
    <a-card title="库存流水详情">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section id="pdfDom">
        <a-spin :spinning="loading">
          <a-descriptions bordered>
            <a-descriptions-item label="创建人">
              {{ info.creator_name }}
            </a-descriptions-item>
            <a-descriptions-item label="创建时间">
              {{ info.create_time }}
            </a-descriptions-item>
            <a-descriptions-item label="仓库">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="产品名称">
              {{ info.goods_name }}
            </a-descriptions-item>
            <a-descriptions-item label="产品编号">
              {{ info.goods_number }}
            </a-descriptions-item>
            <a-descriptions-item label="单位名称">
              {{ info.unit_name }}
            </a-descriptions-item>
            <a-descriptions-item label="流水类型">
              {{ info.type_display }}
            </a-descriptions-item>
            <a-descriptions-item label="变化之前数量">
              {{ info.quantity_before }}
            </a-descriptions-item>
            <a-descriptions-item label="变化数量">
              {{ info.quantity_change }}
            </a-descriptions-item>
            <a-descriptions-item label="变化之后数量">
              {{ info.quantity_after }}
            </a-descriptions-item>
            <a-descriptions-item label="采购单号">
              {{ info.purchase_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废采购单号">
              {{ info.void_purchase_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="采购退货单号">
              {{ info.purchase_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废采购退货单号">
              {{ info.void_purchase_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="销售单号">
              {{ info.sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废销售单号">
              {{ info.void_sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="销售退货单号">
              {{ info.sales_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废销售退货单号">
              {{ info.void_sales_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="入库通知单号">
              {{ info.stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废入库通知单号">
              {{ info.void_stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="出库通知单号">
              {{ info.stock_out_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废出库通知单号">
              {{ info.void_stock_out_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="盘点单号">
              {{ info.stock_check_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废盘点单号">
              {{ info.void_stock_check_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="调拨单号">
              {{ info.stock_transfer_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废调拨单号">
              {{ info.void_stock_transfer_order_number }}
            </a-descriptions-item>
          </a-descriptions>
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { inventoryFlowsDetail } from '@/api/warehouse'
  
  export default {
    data() {
      return {
        loading: false,
        info: {},
      }
    },
    created(){
      this.initData();
    },
    methods: {
      initData() {
        this.info = JSON.parse(this.$route.query.item);
        // this.loading = true;
        // inventoryFlowsDetail({ id: this.$route.query.id }).then(data => {
        //   this.info = data;
        // }).finally(() => {
        //   this.loading = false;
        // });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
