<template>
  <div>
    <a-card title="销售记录">
      <div style="display: flex;flex-direction: row;">
        <div id="sales_predict_echarts" style="width: 100%;height: 250px;"></div>
      </div>
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="单号,供应商编号/名称" allowClear @search="search" />
        </a-col>
        <!-- <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-range-picker @change="onChangePicker" />
        </a-col> -->
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="action" slot-scope="value, item">
            <a-button-group size="small">
              <a-button size="small" @click="detial(item)">详情</a-button>
              <a-popconfirm title="确定作废吗" @confirm="voidItem(item)">
                <a-button type="danger" icon="delete" size="small">作废</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import { saleOrderList, saleOrdersVoid } from '@/api/sale'
  import { sales_predict_echarts} from '@/views/Echarts/echarts1'
  import * as echarts from "echarts";
  import {get_predict_duibi} from '@/api/new'

  export default {
    name: 'SaleRecord',
    components: {
    },
    data() {
      return {
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
            width: 45
          },
          {
            title: '销售编号',
            dataIndex: 'number',
            sorter: true,
          },
          {
            title: '客户',
            dataIndex: 'client_name',
          },
          {
            title: '经手人',
            dataIndex: 'handler_name',
          },
          {
            title: '处理日期',
            dataIndex: 'handle_time',
            width: 150
          },
          {
            title: '销售总数量',
            dataIndex: 'total_quantity',
            width: 120
          },
          {
            title: '销售总金额',
            dataIndex: 'total_amount',
            width: 120
          },
          {
            title: '收款金额',
            dataIndex: 'collection_amount',
            width: 120
          },
          {
            title: '其他费用',
            dataIndex: 'other_amount',
            width: 120
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: 200
          },
        ],
        searchForm: { page: 1, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],
        visible: false,
        targetItem: {},
        form: {},
      };
    },
    computed: {
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        saleOrderList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      onChangePicker(date, dateString) {
        let startDate = date[0], endDate = date[1];
        this.searchForm.start_date = startDate ? startDate.format('YYYY-MM-DD') : undefined;
        this.searchForm.end_date = endDate ? endDate.add(1, 'days').format('YYYY-MM-DD') : undefined;
        this.search();
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      detial(item) {
        this.$router.push({ path: '/sale/sale_record_detail', query: { id: item.id } });
      },
      voidItem(item) {
        saleOrdersVoid({ id: item.id }).then(() => {
          this.$message.success('作废成功');
          this.list();
        });
      },
      init_echart(data){
        var data = [{"name":"产品A","id":1,"predict_price":50.0,"predict_number":5.0,"sales_price":20.0,"sales_quantity":17.0},{"name":"产品A","id":1,"predict_price":50.0,"predict_number":5.0,"sales_price":20.0,"sales_quantity":1.0},{"name":"石灰","id":2,"predict_price":30.0,"predict_number":3.0,"sales_price":null,"sales_quantity":null},{"name":"钢筋","id":3,"predict_price":30.0,"predict_number":4.0,"sales_price":null,"sales_quantity":null},{"name":"建筑木条","id":4,"predict_price":50.0,"predict_number":5.0,"sales_price":null,"sales_quantity":null},{"name":"水泥","id":5,"predict_price":100.0,"predict_number":10.0,"sales_price":null,"sales_quantity":null},{"name":"钉子","id":6,"predict_price":30.0,"predict_number":3.0,"sales_price":20.0,"sales_quantity":970.0}];
        var myChart = echarts.init(document.getElementById('sales_predict_echarts'));
        myChart.setOption(sales_predict_echarts(data));


        get_predict_duibi({}).then(res=>{
          var myChart = echarts.init(document.getElementById('sales_predict_echarts'));
          myChart.setOption(sales_predict_echarts(res));
        })
      }
    },
    mounted() {
      this.initialize();
      this.init_echart();
    },
  }
</script>