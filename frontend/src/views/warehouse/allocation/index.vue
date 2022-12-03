<template>
  <div>
    <a-card title="调拨">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="单号" allowClear @search="search" />
        </a-col>
        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="handelAdd(form)">新增调拨</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="action" slot-scope="value, item">
            <a-button-group size="small">
              <a-button size="small" @click="detial(item)">详情</a-button>
              <a-popconfirm title="确定作废吗?" @confirm="voidItem(item)">
                <a-button type="danger" :disabled="item.is_void">{{ item.is_void ? '已作废' : '作废'}}</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import { stockTransferOrdersList, stockTransferOrdersVoid } from '@/api/warehouse'

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
            title: '单号',
            dataIndex: 'number',
            sorter: true,
          },
          {
            title: '出库仓库',
            dataIndex: 'out_warehouse_name',
          },
          {
            title: '入库仓库',
            dataIndex: 'in_warehouse_name',
          },
          {
            title: '经手人',
            dataIndex: 'handler_name',
          },
          {
            title: '处理日期',
            dataIndex: 'handle_time',
          },
          {
            title: '备注',
            dataIndex: 'remark'
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
        this.list();
      },
      list() {
        this.loading = true;
        stockTransferOrdersList(this.searchForm).then(data => {
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
      handelAdd(item) {
        this.$router.push({ path: '/warehouse/allocation_create' });
      },
      detial(item) {
        this.$router.push({ path: '/warehouse/allocationDetail_detail', query: { id: item.id } });
      },
      voidItem(item) {
        stockTransferOrdersVoid({ id: item.id }).then(() => {
          this.$message.success('作废成功');
          this.list();
        });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>