<template>
  <div>
    <a-row :gutter="[8, 8]">
      <a-col :span="8">
        <a-card title="今日销售额" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">
            {{ item.sales_amount }}
          </div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="今日销售笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">
            {{ item.sales_count }}
          </div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="今日采购笔数" size="small">
          <div style="text-align: center; font-size: 36px; font-weight: 600; color: #1890ff; margin: 12px 0;">
            {{ item.purchase_count }}
          </div>
        </a-card>
      </a-col>

      <a-col :span="24">
        <a-card title="待办事项" size="small">
          <a-card-grid style="width:20%; text-align:center; cursor: pointer;" @click="navigateTo('/warehouse/inStock')">
            <a-statistic title="待入库" :value="item.stock_in_task_count" />
          </a-card-grid>
          <a-card-grid
            style="width:20%; text-align:center; cursor: pointer;"
            @click="navigateTo('/warehouse/outStock')"
          >
            <a-statistic title="待出库" :value="item.stock_out_task_count" />
          </a-card-grid>
          <a-card-grid
            style="width:20%; text-align:center; cursor: pointer;"
            @click="navigateTo('/report/stock_report')"
          >
            <a-statistic title="库存预警" :value="item.inventory_warning_count" />
          </a-card-grid>
          <a-card-grid
            style="width:20%; text-align:center; cursor: pointer;"
            @click="navigateTo('/finance/arrears_receivable')"
          >
            <a-statistic title="应收欠款" :value="item.arrears_receivable_amount" />
          </a-card-grid>
          <a-card-grid
            style="width:20%; text-align:center; cursor: pointer;"
            @click="navigateTo('/finance/arrears_payable')"
          >
            <a-statistic title="应付欠款" :value="item.arrears_payable_amount" />
          </a-card-grid>
        </a-card>
      </a-col>

      <!-- <a-col :span="24">
        <a-card title="ERP操作快捷入口" size="small">
          <a-row gutter="0">
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">采购开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">销售开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">入库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">出库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">盘点</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">调拨</div>
              </a-card-grid>
            </a-col>
          </a-row>
        </a-card>
      </a-col> -->

      <a-col :span="12">
        <sales-trend />
      </a-col>

      <a-col :span="12">
        <sales-goods />
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { homeOverview } from "@/api/statistic";

export default {
  components: {
    SalesTrend: () => import("./salesTrend.vue"),
    SalesGoods: () => import("./salesGoods.vue"),
  },
  data() {
    return {
      loading: false,
      item: {},
    };
  },
  methods: {
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      homeOverview()
        .then((data) => {
          this.item = data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    navigateTo(pathName) {
      this.$router.push({ path: pathName });
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped></style>
