<template>
  <div>
    <a-card style="height: calc(50vh - 40px);">
      <div slot="title">
        <span>销售前十产品</span>
        <a-range-picker v-model="dateRange" :ranges="ranges" :disabled="salesLoading" :allowClear="false"
          @change="changeDateRange" style="float: right;" />
        <div id="salesGoods" style="margin-top: 36px;"></div>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { salesTopTenList } from '@/api/system'
  import moment from 'moment'

  export default {
    name: 'SalesGoods',
    data() {
      return {
        ranges: {
          '7天': [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
          '15天': [moment().add(-15, 'days').startOf('day'), moment().startOf('day')],
          '30天': [moment().add(-30, 'days').startOf('day'), moment().startOf('day')],
        },
        dateRange: [moment().add(-7, 'days').startOf('day'), moment().startOf('day')],
        chart: null,
        loading: false,
      };
    },
    methods: {
      initialize() {
        let height = window.innerHeight / 2 - 141;
        this.chart = new window.G2.Chart({ container: 'salesGoods', autoFit: true, height });
        this.chart.scale('total_sales_quantity', { alias: '销量' });
        this.chart.interval().position('goods_name*total_sales_quantity');
        this.list();
      },
      list() {
        let form = {
          start_date: this.dateRange[0].format('YYYY-MM-DD'),
          end_date: this.dateRange[1].format('YYYY-MM-DD'),
        };

        if (form.end_date) {
          form.end_date = moment(form.end_date).add(1, 'days').format('YYYY-MM-DD');
        }

        this.loading = true;
        salesTopTenList(form).then(resp => {
          this.chart.changeData(resp);
          this.chart.forceFit();
        }).finally(() => {
          this.loading = false;
        });
      },
      changeDateRange(dateRange) {
        this.dateRange = dateRange;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>