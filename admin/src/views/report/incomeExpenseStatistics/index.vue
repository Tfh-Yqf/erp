<template>
  <div>
    <a-card style="padding-bottom:0px;">
      <a-row>
        <a-col :span="24">
          <ButtonsPicker
            :radioValue="radioValue"
            :dateRange="searchForm.dateRange"
            @aRangePickerChange="
              (value) => {
                $set(searchForm, 'dateRange', value);
                radioValue = null;
                search();
              }
            "
            @aRadioGroupChange="
              (value) => {
                radioValue = value;
              }
            "
          ></ButtonsPicker>
        </a-col>
      </a-row>
    </a-card>
    <a-row gutter="8" style="margin-top:8px;">
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="销售金额(元)"
            :value="statistics.total_sales_amount"
            :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="销售退货金额(元)"
            :value="statistics.total_sales_reutrn_amount"
            :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="采购金额(元)"
            :value="statistics.total_purchase_amount"
            :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="采购退货金额(元)"
            :value="statistics.total_purchase_return_amount"
            :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="收入金额(元)"
            :value="statistics.total_income_amount"
            :loading="loading" />
        </a-card>
      </a-col>
      <a-col :span="4">
        <a-card hoverable>
          <a-statistic
            title="支出金额(元)"
            :value="statistics.total_expenditure_amount"
            :loading="loading" />
        </a-card>
      </a-col>
    </a-row>

    <a-row gutter="8" style="margin-top: 8px;">
      <a-col :span="12">
        <sales-detail ref="salesDetail"  />
      </a-col>
      <a-col :span="12">
        <sales-return-detail ref="salesReturnDetail" />
      </a-col>
    </a-row>
    <a-row gutter="8" style="margin-top: 8px">
      <a-col :span="12">
        <purchase-detail ref="purchaseDetail" />
      </a-col>
      <a-col :span="12">
        <purchase-return-detail ref="purchaseReturnDetail" />
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { financialStatistics } from "@/api/report";
import moment from "moment";
export default {
  name: "FinancialStatistics",
  components: {
    SalesDetail: () => import("./salesDetail.vue"),
    SalesReturnDetail: () => import("./salesReturnDetail.vue"),
    PurchaseDetail: () => import("./purchaseDetail.vue"),
    PurchaseReturnDetail: () => import("./purchaseReturnDetail.vue"),
    ButtonsPicker: () => import("@/components/Fields/ButtonsPicker"),
  },
  data() {
    return {
      searchForm: {
        dateRange: [moment().startOf("day"), moment().startOf("day")],
        page: 1,
      },
      moment,
      radioValue: "0",
      loading: false,
      statistics: {},
    };
  },
  computed: {
    start_date() {
      return this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[0].format("YYYY-MM-DD") : null
    },
    end_date() {
      return this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[1].format("YYYY-MM-DD") : null
    }
  },
  methods: {
    search() {
      this.searchForm.page = 1;
      this.list();
      this.$refs.salesDetail.initialize(this.start_date, this.end_date);
      this.$refs.salesReturnDetail.initialize(this.start_date, this.end_date);
      this.$refs.purchaseDetail.initialize(this.start_date, this.end_date);
      this.$refs.purchaseReturnDetail.initialize(this.start_date, this.end_date);
    },
    changeDate() {
      this.radioValue = null;
      this.search();
    },
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      let form = {
        start_date:
          this.searchForm.dateRange.length > 0
            ? this.searchForm.dateRange[0].format("YYYY-MM-DD")
            : null,
        end_date:
          this.searchForm.dateRange.length > 0
            ? this.searchForm.dateRange[1].format("YYYY-MM-DD")
            : null,
        page: this.searchForm.page,
        type: this.currentTab,
      };
      if (form.end_date) {
          form.end_date = moment(form.end_date).add(1, 'days').format('YYYY-MM-DD');
        }
      
      financialStatistics(form).then((resp) => {
        this.statistics = resp;
      }).finally(() => {
        this.loading = false;
      });
  },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped>
</style>