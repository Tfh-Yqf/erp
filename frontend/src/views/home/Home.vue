<template>
  <div>
    <a-row :gutter="[8, 8]">
      <a-col :span="8">
        <a-card title="今日销售额(元)" size="small">
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
            {{ caigou_bishu }}
          </div>
        </a-card>
      </a-col>

      <a-col :span="24">
        <a-card title="待办事项" size="small">

          <a-card-grid style="width:25%; text-align:center; cursor: pointer;" @click="navigateTo('/warehouse/inStock')">
            <a-statistic title="待入库" :value="item.stock_in_task_count" />
          </a-card-grid>

          <a-card-grid
            style="width:25%; text-align:center; cursor: pointer;"
            @click="navigateTo('/warehouse/outStock')"
          >
            <a-statistic title="待出库" :value="item.stock_out_task_count" />
          </a-card-grid>


<!--          <a-card-grid-->
<!--            style="width:20%; text-align:center; cursor: pointer;"-->
<!--            @click="navigateTo('/report/stock_report')"-->
<!--          >-->
<!--            <a-statistic title="库存预警" :value="item.inventory_warning_count" />-->
<!--          </a-card-grid>-->


          <a-card-grid
            style="width:25%; text-align:center; cursor: pointer;"
            @click="navigateTo('/finance/arrears_receivable')"
          >
            <a-statistic title="应收欠款(元)" :value="item.arrears_receivable_amount" />
          </a-card-grid>


          <a-card-grid
            style="width:25%; text-align:center; cursor: pointer;"
            @click="navigateTo('/finance/arrears_payable')"
          >
            <a-statistic title="应付欠款(元)" :value="item.arrears_payable_amount" />
          </a-card-grid>


        </a-card>
      </a-col>

       <a-col :span="24">
        <a-card title="ERP操作快捷入口" size="small">
          <a-row gutter="0">
            <a-col :span="4" @click="jump_caigou">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;" >
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">采购开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4" @click="jump_xiaoshou">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">销售开单</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4" @click="jump_ruku">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">入库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4" @click="jump_chuku">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">出库</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4" @click="jump_pandia">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">盘点</div>
              </a-card-grid>
            </a-col>
            <a-col :span="4" @click="jump_diaobo">
              <a-card-grid style="width: 100%; cursor: pointer; text-align: center;">
                <a-icon type="profile" style="font-size: 40px; color: #1890ff;" />
                <div style="margin-top: 4px;">调拨</div>
              </a-card-grid>
            </a-col>
          </a-row>
        </a-card>
      </a-col>

      <a-col :span="12">
        <sales-trend />
      </a-col>

      <a-col :span="12">
        <sales-goods />
      </a-col>
      <div style="width: 100%;display: flex;flex-direction: row;"  @click="navigateTo('/report/stock_report')">
        <a-col :span="18">
          <Saleskucun />
        </a-col>
        <div style="background-color: #FFFFFF" @click="jump_chanpin_xinxi">
          <a-table  size="small" :columns="columns" :dataSource="yujing" rowKey="id"  :pagination="pagination">
          </a-table>
        </div>


      </div>

    </a-row>
  </div>
</template>

<script>
import { homeOverview } from "@/api/statistic";
import { kucun_yujing} from '@/api/user';
import {get_caigou_bishu} from '@/api/new'

export default {
  components: {
    SalesTrend: () => import("./salesTrend.vue"),
    SalesGoods: () => import("./salesGoods.vue"),
    Saleskucun:() => import("./saleskucun.vue")
  },
  data() {
    return {
      caigou_bishu:0,
      loading: false,
      item: {},
      yujing:[],
      columns: [
        {
          title: '产品名',
          dataIndex: 'name',
          key: 'name',
          width: 80
        },
        {
          title: '预警临界数量',
          dataIndex: 'inventory_lower',
          sorter: true,
          width: 150
        },
        {
          title: '库存数量',
          dataIndex: 'total_quantity',
          width: 80
        }]
    };
  },
  methods: {
    initialize() {
      this.list();
      kucun_yujing("test").then(res=>{
        console.log(res);
        this.yujing = res;
      }).finally(()=>{

      });

      get_caigou_bishu({}).then(res=>{
        this.caigou_bishu = res;
      })
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
    jump_caigou(){
      this.$router.push('/purchasing/purchase_create')
    },
    jump_xiaoshou(){
      this.$router.push('/sale/sale_record')
    },
    jump_ruku(){
      this.$router.push('/warehouse/inStock')
    },
    jump_chuku(){
      this.$router.push('/warehouse/outStock')
    },
    jump_pandia(){
      this.$router.push('/warehouse/inventory')
    },
    jump_diaobo(){
      this.$router.push('/warehouse/allocation')
    },
    jump_chanpin_xinxi(){
      this.$router.push('/sales/information')
    }
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped></style>
