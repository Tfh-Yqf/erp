<template>
  <div>
    <a-card :tab-list="tabList" :active-tab-key="currentTab" @tabChange="changeTab">
      <a-row gutter="24">
        <a-col :span="10">
          <a-form-model-item :wrapper-col="{ span: 24 }">
            <a-radio-group v-model="radioValue" button-style="solid" @change="changeRadio" style="width: 100%;">
              <a-radio-button value="0" style="width: 25%;">今日</a-radio-button>
              <a-radio-button value="1" style="width: 25%;">昨天</a-radio-button>
              <a-radio-button value="-6" style="width: 25%;">近7天</a-radio-button>
              <a-radio-button value="-29" style="width: 25%;">近30天</a-radio-button>
            </a-radio-group>
          </a-form-model-item>
        </a-col>
        <a-col :span="8">
          <a-form-model-item label="自定义时间" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
            <a-range-picker v-model="searchForm.dateRange" @change="changeDate" style="width: 100%;" />
          </a-form-model-item>
        </a-col>
        <a-col :span="6">
          <a-form-model-item label="分类" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-select v-model="searchForm.category" allowClear style="width: 100%;" @change="changeCategory">
              <a-select-option v-for="item in categoryItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-col>
      </a-row>

      <a-descriptions :column="{ xxl: 4, xl: 4, lg: 4, md: 2, sm: 2, xs: 1 }" style="text-align: center;">
        <a-descriptions-item label="采购次数"><span class="total">{{totalCount}}</span></a-descriptions-item>
        <a-descriptions-item label="采购数量"><span class="total">{{totalQuantity}}</span></a-descriptions-item>
        <a-descriptions-item label="采购金额"><span class="total">{{totalAmount}}</span></a-descriptions-item>
      </a-descriptions>

      <div>
        <flow-pane v-show="currentTab === 'flow'" :items="items" :loading="loading" :pagination="pagination" @tableChange="tableChange" />
        <goods-pane v-show="currentTab === 'goods'" :items="items" :loading="loading" :pagination="pagination" @tableChange="tableChange" />
      </div>
      <div style="text-align: center; margin-top: 12px;">
        <a-spin :spinning="loading && searchForm.page > 1" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { purchaseReportStatistics, purchaseReportDetialsList, purchaseReportByGoodsList } from '@/api/report'
  import { goodsClassificationOption } from '@/api/option'
  import NP from 'number-precision'
  import moment from 'moment'

  export default {
    name: 'SalesReport',
    components: {
      FlowPane: () => import('./flowPane'),
      GoodsPane: () => import('./goodsPane'),
    },
    data() {
      return {
        NP,
        currentTab: 'flow',
        radioValue: '0',
        tabList: [
          {
            key: 'flow',
            tab: '采购明细',
          },
          {
            key: 'goods',
            tab: '按产品汇总',
          },
        ],
        searchForm: {
          dateRange: [moment().startOf('day'), moment().startOf('day')],
          category: null,
          page: 1,
          page_size: 16
        },
        loading: true,
        categoryItems: [],
        total: {
          quantity: 0,
          cost: 0,
          amount: 0,
        },
        items: [],
        pagination: { current: 1, total: 0, pageSize: 16 },
      };
    },
    computed: {
      totalCount() {
        return this.total.total_count ? this.total.total_count : 0
      },
      totalQuantity() {
        return this.total.total_quantity ? this.total.total_quantity : 0
      },
      totalAmount() {
        return this.total.total_amount ? NP.round(this.total.total_amount, 2) : 0
      },
    },
    methods: {
      initailize() {
        if (this.$route.query.type) {
          this.currentTab = this.$route.query.type;
        } else {
          this.$router.replace({ query: { type: this.currentTab } })
        }
        this.list();
        goodsClassificationOption({ page_size: 99999 }).then(resp => {
          this.categoryItems = resp.results;
        });
      },
      list() {
        let form = {
          start_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[0].format('YYYY-MM-DD') : null,
          end_date: this.searchForm.dateRange.length > 0 ? this.searchForm.dateRange[1].format('YYYY-MM-DD') : null,
          category: this.searchForm.category,
          page: this.searchForm.page,
          page_size: this.searchForm.page_size,
        };

        if (form.end_date) {
          form.end_date = moment(form.end_date).add(1, 'days').format('YYYY-MM-DD');
        }

        this.loading = true;
        purchaseReportStatistics(form).then(resp => {
          this.total = resp;
        })
        if (this.currentTab === 'flow') {
          purchaseReportDetialsList(form).then(resp => {
            this.items = resp.results;
            this.pagination.total = resp.count;
          }).finally(() => {
            this.loading = false;
          });
        } else {
          purchaseReportByGoodsList(form).then(resp => {
            this.items = resp.results;
            this.pagination.total = resp.count;
          }).finally(() => {
            this.loading = false;
          });
        }
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      changeTab(key) {
        this.currentTab = key;
        this.$router.replace({ query: { type: this.currentTab } })
        this.resetForm();
        this.search();
      },
      changeRadio(evt) {
        let value = evt.target.value;
        if (value < 0) {
          this.searchForm.dateRange = [moment().startOf('day').add(value, 'day'), moment().startOf('day')]
        } else {
          this.searchForm.dateRange = [moment().startOf('day').subtract(value, 'day'), moment().startOf('day').subtract(value, 'day'),]
        }
        this.search();
      },
      changeDate() {
        this.radioValue = null;
        this.search();
      },
      changeCategory() {
        this.search();
      },
      resetForm() {
        this.radioValue = '0';
        this.searchForm = {
          dateRange: [moment().startOf('day'), moment().startOf('day')],
          category: null,
          page: 1,
          page_size: 16
        };
      },
    },
    mounted() {
      this.initailize();
    },
  }
</script>

<style scoped>
  .total {
    color: #a94442;
  }
</style>