<template>
  <div>
    <a-card title="销售预期">
      <a-row gutter="16">
        <a-col :span="24" :md="6" :xl="4" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="产品编号/名称" allowClear @search="search" />
        </a-col>
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-select v-model="searchForm.warehouse" placeholder="仓库" allowClear style="width: 100%;" @change="search">
            <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">{{item.name}}
            </a-select-option>
          </a-select>
        </a-col>
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-select v-model="searchForm.has_stock" placeholder="库存状态" allowClear style="width: 100%;" @change="search">
            <a-select-option  :value="true">有库存</a-select-option>
            <a-select-option  :value="false">无库存</a-select-option>
          </a-select>
        </a-col>
        <!-- <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-range-picker @change="onChangePicker" />
        </a-col> -->
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small"
                 rowKey="id"
                 :columns="columns"
                 :dataSource="items"
                 :loading="loading"
                 :pagination="pagination"
                 @change="tableChange">
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="openFormModal(item)">编辑</a-button>
            </a-button-group>
          </div>
        </a-table>
      </a-row>

      <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
    </a-card>
  </div>
</template>

<script>
import { warehousesOption } from '@/api/option';
import { inventoryReportList } from '@/api/report';
import * as echarts from 'echarts';
import {} from '@/views/Echarts/echarts1'
import {get_predict} from '@/api/new'

export default {
  name: 'Warehouse',
  components: {
    FormModal: () => import('./FormModal.vue')
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
          title: '仓库',
          dataIndex: 'warehouse_name',
        },
        {
          title: '仓库编号',
          dataIndex: 'warehouse_number',
        },
        {
          title: '产品名称',
          dataIndex: 'goods_name',
        },
        {
          title: '产品编号',
          dataIndex: 'goods_number',
        },
        {
          title: '库存总数',
          dataIndex: 'total_quantity',
        },
        {
          title: '单位',
          dataIndex: 'unit_name',
          width: 80
        },
        {
          title: '库存状态',
          dataIndex: 'has_stock',
          customRender: (value, item, index) => {
            return item.has_stock ? '有' : '无'
          },
        },
        {
          title: '计划销售数量',
          dataIndex: 'predict_number'
        },
        {
          title: '计划销售金额(元)',
          dataIndex: 'predict_price'
        },
        {
          title: '操作',
          dataIndex: 'action',
          scopedSlots: { customRender: 'action' },
          width: 147
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
      warehousesOption({ page_size: 99999 }).then(resp => {
        this.warehouseItems = resp.results;
      });
      this.list();

    },
    list() {
      this.loading = true;
      //test
      // var data = {"count":6,"next":null,"previous":null,"results":[{"predict_number":10,"id":6,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":6,"goods_number":"G006","goods_name":"钉子","goods_barcode":null,"total_quantity":30.0,"unit_name":"个","has_stock":true},{"id":5,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":5,"goods_number":"G005","goods_name":"水泥","goods_barcode":null,"total_quantity":20.0,"unit_name":"个","has_stock":true},{"id":4,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":4,"goods_number":"G004","goods_name":"建筑木条","goods_barcode":null,"total_quantity":18.0,"unit_name":"个","has_stock":true},{"id":3,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":3,"goods_number":"G003","goods_name":"钢筋","goods_barcode":null,"total_quantity":10.0,"unit_name":"个","has_stock":true},{"id":2,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":2,"goods_number":"G002","goods_name":"石灰","goods_barcode":null,"total_quantity":100.0,"unit_name":"个","has_stock":true},{"id":1,"warehouse":1,"warehouse_number":"W001","warehouse_name":"默认仓库","goods":1,"goods_number":"G001","goods_name":"产品A","goods_barcode":null,"total_quantity":111.0,"unit_name":"个","has_stock":true}]};
      // this.pagination.total = data.count;



      inventoryReportList(this.searchForm).then(data => {
        this.pagination.total = data.count;

        get_predict({}).then(res=>{
          var temp = data.results;
          for(var i=0;i<temp.length;i++){
            for(var j=0;j<res.length;j++){
              if(temp[i].id==res[j].id){
                temp[i] = {
                  ...temp[i],
                  predict_price:res[j].predict_price,
                  predict_number:res[j].predict_number
                };
                break;
              }
            }
          }
          this.items = temp;
        });
      }).finally(() => {
        this.loading = false;
      });
    },
    tableChange(pagination, filters, sorter) {
      console.log(pagination)
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
    init_echart(data){
      var myChart = echarts.init(document.getElementById('kucun_echarts'));
      myChart.setOption(kucun_echarts_data(data));
    },
    openFormModal(item) {
      this.targetItem = { ...item };
      this.visible = true;
    },
    update(item) {
      this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
    },
    create(item) {
      // this.items.splice(0, 0, item);
      this.list();
    },
  },
  mounted() {
    this.initialize();
  },
}
</script>