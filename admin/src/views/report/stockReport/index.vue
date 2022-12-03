<template>
  <div>
    <a-card title="库存报表">
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
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import { warehousesOption } from '@/api/option'
  import { inventoryReportList } from '@/api/report'

  export default {
    name: 'Warehouse',
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
            title: '产品条码',
            dataIndex: 'goods_barcode',
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
          // {
          //   title: '操作',
          //   dataIndex: 'action',
          //   scopedSlots: { customRender: 'action' },
          //   width: 147
          // },
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
        inventoryReportList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
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
    },
    mounted() {
      this.initialize();
    },
  }
</script>