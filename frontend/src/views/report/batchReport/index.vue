<template>
  <div>
    <a-card title="批次报表">
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
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table
          size="small"
          :columns="columns"
          :dataSource="items"
          rowKey="id"
          :loading="loading"
          :pagination="pagination"
          @change="tableChange"
        >
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{ value ? "激活" : "冻结" }}</a-tag>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
import { warehousesOption } from '@/api/option'
import { batchsReportList,  } from '@/api/report'

export default {
  name: "Warehouse",
  components: {
  },
  data() {
    return {
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          width: 60,
          customRender: (value, item, index) => {
            return index + 1;
          },
        },
        {
          title: "编号",
          dataIndex: "number",
        },
        {
          title: "批次数量",
          dataIndex: "total_quantity",
        },
        {
          title: "批次剩余数量",
          dataIndex: "remain_quantity",
        },
        {
          title: "产品编号",
          dataIndex: "goods_number",
        },
        {
          title: "产品名称",
          dataIndex: "goods_name",
          sorter: true,
        },
        {
          title: "仓库",
          dataIndex: "warehouse_name",
        },
        {
          title: "仓库编号",
          dataIndex: "warehouse_number",
        },
        {
          title: "库存状态",
          dataIndex: "has_stock",
          customRender: (value, item, index) => {
            return item.has_stock ? '有' : '无'
          },
        },
      ],
      searchForm: { search: "", page: 1, page_size: 16 },
      pagination: { current: 1, total: 0, pageSize: 16 },
      loading: false,
      items: [],
    };
  },
  computed: {},
  methods: {
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      batchsReportList(this.searchForm)
        .then((data) => {
          this.pagination.total = data.count;
          this.items = data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    search() {
      this.searchForm.page = 1;
      this.pagination.current = 1;
      this.list();
    },
    tableChange(pagination, filters, sorter) {
      this.searchForm.page = pagination.current;
      this.pagination.current = pagination.current;
      this.searchForm.ordering = `${sorter.order == "descend" ? "-" : ""}${sorter.field}`;
      this.list();
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>
