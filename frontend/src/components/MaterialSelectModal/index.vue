<template>
  <div>
    <a-modal v-model="visible" title="物料选择" width="750px" :footer="null" @cancel="onCloseModel">
      <a-row gutter="16">
        <a-col :span="24" style="width: 256px;">
          <a-input v-model="searchForm.search" placeholder="产品名称, 编码, 条码" allowClear @pressEnter="search" />
        </a-col>
        <a-space>
          <a-button type="primary" icon="search" @click="search">查询</a-button>
        </a-space>
      </a-row>

      <div style="margin-top: 12px;">
        <a-table :data-source="items" rowKey="id" :columns="columns" :loading="loading" :pagination="pagination"
          @change="onChangeTable">
          <div slot="action" slot-scope="value, item, index">
            <a-button size="small" @click="select(item)">选择</a-button>
          </div>
        </a-table>
      </div>

    </a-modal>
  </div>
</template>

<script>
  import { inventoriesOption } from '@/api/option';
  import { columns } from './columns';

  export default {
    props: ['visible', 'warehouse'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        columns,
        pagination: {},
        searchForm: { search: '' },
        loading: false,
        items: [],
      }
    },
    methods: {
      onCloseModel() {
        this.$emit('cancel', false);
      },
      onChangeTable(pagination, filters, sorter) {
        this.pagination = pagination;
        this.searchForm.page = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      search() {
        this.pagination.current = 1;
        this.searchForm.page = 1;
        this.list();
      },
      list() {
        this.loading = true;
        inventoriesOption(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      select(item) {
        this.$emit('select', item);
        this.onCloseModel();
      },
      resetModel() {
        this.pagination = { current: 1, total: 0, pageSize: 16, showTotal: total => `共 ${total} 条` };
        this.searchForm = { page: 1, warehouse: this.warehouse, is_active: true };
        this.items = [];
      },
    },
    watch: {
      visible(status) {
        if (status) {
          this.resetModel();
          this.list();
        }
      },
    },
  }
</script>