<template>
  <div>
    <a-card title="账户转账">
      <a-row gutter="16">
        <a-col :span="24" :md="6" :xl="4" style="max-width: 256px; margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="名称, 备注" allowClear @search="search" />
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">新增账户转账</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{value ? '激活' : '冻结'}}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-popconfirm title="确定作废吗?" @confirm="voidItem(item)">
                <a-button type="danger" size="small" :disabled="item.is_void">{{ item.is_void ? '已作废' : '作废'}}</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
    <form-modal v-model="visible" :form="targetItem" :handlerItems="handlerItems" :accountsItems="accountsItems" @create="create" @update="update" />
  </div>
</template>

<script>
  import { userOption, accountsOption } from '@/api/option'
  import { accountTransferOrdersList, accountTransferOrdersVoid } from '@/api/finance'

  export default {
    name: 'Warehouse',
    components: {
      FormModal: () => import('./FormModal.vue'),
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
          },
          {
            title: '转出账户',
            dataIndex: 'out_account_name',
          },
          {
            title: '转出时间',
            dataIndex: 'transfer_out_time'
          },
          {
            title: '转入账户',
            dataIndex: 'in_account_name'
          },
          {
            title: '转入时间',
            dataIndex: 'transfer_in_time'
          },
          {
            title: '转账金额',
            dataIndex: 'transfer_amount'
          },
          {
            title: '手续费金额',
            dataIndex: 'service_charge_amount'
          },
          {
            title: '手续费支付方',
            dataIndex: 'service_charge_payer_display'
          },
          {
            title: '经手人',
            dataIndex: 'handler_name'
          },
          {
            title: '处理时间',
            dataIndex: 'handle_time'
          },
          {
            title: '备注',
            dataIndex: 'remark'
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px'
          },
        ],
        searchForm: { search: '', page: 1, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],
        handlerItems: [],
        accountsItems: [],
        visible: false,
        targetItem: {},
        form: {},
        importLoading: false,
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
        accountTransferOrdersList(this.searchForm).then(data => {
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
      create(item) {
        // this.items.splice(0, 0, item);
        this.list();
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      openFormModal(item) {
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.handlerItems = data.results;
        });
        accountsOption({ page_size: 999999, is_active: true }).then(data => {
          this.accountsItems = data.results;
        });
        this.targetItem = { ...item };
        this.visible = true;
      },
      voidItem(item) {
        accountTransferOrdersVoid({ id: item.id }).then(() => {
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