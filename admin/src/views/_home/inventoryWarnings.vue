<template>
  <div>
    <a-card title="库存预警" style="height: calc(50vh - 48px);">
      <a-table :columns="columns" :data-source="items" size="small" :pagination="false" :loading="loading"
        :scroll="{y: tableHeight}" />
      <div style="text-align: center; margin-top: 16px;">
        <a-pagination v-model="searchForm.page" :total="totalRows" :pageSize="perPage" show-less-items
          @change="changePage" />
      </div>
    </a-card>
  </div>
</template>

<script>
  import { inventoryWarningsList } from '@/api/system'
  import moment from 'moment'

  export default {
    data() {
      return {
        searchForm: {
          page: 1,
          page_size: 10,
          datetime: moment().format('YYYY-MM-DD'),
        },
        perPage: 16,
        totalRows: 0,
        loading: false,
        columns: [
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '产品名称',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '库存上限',
            dataIndex: 'inventory_upper',
            key: 'inventory_upper',
          },
          {
            title: '库存下限',
            dataIndex: 'inventory_lower',
            key: 'inventory_lower',
          },
          {
            title: '库存数量',
            dataIndex: 'total_quantity',
            key: 'total_quantity',
          },
        ],
        items: [],
        tableHeight: window.innerHeight / 2 - 240,
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        inventoryWarningsList(this.searchForm).then(resp => {
          this.totalRows = resp.count;
          this.items = resp.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      changePage(value) {
        this.searchForm.page = value;
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