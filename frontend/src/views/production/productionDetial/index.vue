<template>
  <div>
    <a-card title="生产计划详情">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'">
        <a-icon type="printer" />打印</a-button
      >
      <a-button
        slot="extra"
        type="primary"
        ghost
        @click="
          () => {
            this.$router.go(-1);
          }
        "
      >
        <a-icon type="left" />返回</a-button
      >
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="生产计划单号">
              {{ item.number }}
            </a-descriptions-item>
            <a-descriptions-item label="销售单号">
              {{ item.sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="状态">
              {{ item.status_display }}
            </a-descriptions-item>
            <a-descriptions-item label="产品编号">
              {{ item.goods_number }}
            </a-descriptions-item>
            <a-descriptions-item label="产品名称">
              {{ item.goods_name }}
            </a-descriptions-item>
            <a-descriptions-item label="计划数量">
              {{ item.total_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="完成数量">
              {{ item.quantity_produced }}
            </a-descriptions-item>
            <a-descriptions-item label="计划开始时间">
              {{ item.start_time }}
            </a-descriptions-item>
            <a-descriptions-item label="计划结束时间">
              {{ item.end_time }}
            </a-descriptions-item>
            <a-descriptions-item label="创建时间">
              {{ item.create_time }}
            </a-descriptions-item>
            <a-descriptions-item label="创建人">
              {{ item.creator_name }}
            </a-descriptions-item>
          </a-descriptions>
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
import { productionOrderDetail } from "@/api/production";
import JsBarcode from "jsbarcode";

export default {
  data() {
    return {
      loading: false,
      item: {},
    };
  },
  methods: {
    getJsBarcode(number) {
      JsBarcode("#barcode", number, {
        lineColor: "#000",
        width: 2,
        height: 40,
        displayValue: true,
      });
    },
    initData() {
      this.loading = true;
      productionOrderDetail({ id: this.$route.query.id })
        .then((data) => {
          this.item = data;
          this.getJsBarcode(data.number);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  mounted() {
    this.initData();
  },
};
</script>
<style></style>
