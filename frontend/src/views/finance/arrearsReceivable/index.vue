<template>
  <div>
    <a-card title="应收欠款">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="编号" allowClear @search="search" />
        </a-col>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="action" slot-scope="value, item">
            <a-button-group size="small">
              <a-button size="small" @click="detial(item)">详情</a-button>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import { arrearsReceivableList } from '@/api/finance'

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
            fixed: 'left',
            customRender: (value, item, index) => {
              return index + 1
            },
            width: 45
          },
          {
            title: '编号',
            dataIndex: 'number',
            fixed: 'left',
          },
          {
            title: '初期欠款金额(元)',
            dataIndex: 'initial_arrears_amount',
          },
          {
            title: '欠款金额(元)',
            dataIndex: 'arrears_amount',
          },
          {
            title: '欠款状态',
            dataIndex: 'has_arrears',
          },
          {
            title: '名称',
            dataIndex: 'name',
          },
          {
            title: '等级',
            dataIndex: 'level_display',
          },
          {
            title: '联系人',
            dataIndex: 'contact',
          },
          {
            title: '手机号',
            dataIndex: 'phone',
          },
          {
            title: '邮箱',
            dataIndex: 'email',
          },
          {
            title: '地址',
            dataIndex: 'address',
          },
          {
            title: '备注',
            dataIndex: 'remark',
          },
          {
            title: '激活状态',
            dataIndex: 'is_active',
          },
        ],
        searchForm: { page: 1,has_arrears: true, page_size: 16 },
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
        arrearsReceivableList(this.searchForm).then(data => {
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
        this.$router.push({ path: '/finance/flow_detail', query: { item: JSON.stringify(item) } });
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>