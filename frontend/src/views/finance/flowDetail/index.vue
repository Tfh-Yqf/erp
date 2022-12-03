<template>
  <div>
    <a-card title="资金流水详情">
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
            <a-descriptions-item label="结算账户名称">
              {{ info.account_name }}
            </a-descriptions-item>
            <a-descriptions-item label="结算账户编号">
              {{ info.account_number }}
            </a-descriptions-item>
            <a-descriptions-item label="流水类型">
              {{ info.type_display }}
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
            <a-descriptions-item label="付款单据">
              {{ info.payment_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废付款单据">
              {{ info.void_payment_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="收款单据">
              {{ info.collection_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废收款单据">
              {{ info.void_collection_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="收支单据">
              {{ info.charge_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="作废收支单据">
              {{ info.void_charge_order_number }}
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
