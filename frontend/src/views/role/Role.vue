<template>
  <div>
    <a-card title="角色管理">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="名称, 备注" allowClear @search="search" />
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">新增角色</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" rowKey="id" :columns="columns" :dataSource="items" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="openFormModal(item)">编辑</a-button>
              <a-popconfirm title="确定删除吗" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>

    <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
  </div>
</template>

<script>
  import { roleList, roleDestroy } from '@/api/account'
  import { permissionList } from '@/api/system';
  import { permissions } from '@/permissions.js'
  import columns from './columns.js'

  export default {
    name: 'Role',
    components: {
      FormModal: () => import('./FormModal.vue'),
    },
    data() {
      return {
        columns,
        permissions,
        searchForm: { search: '', page: 1, ordering: undefined, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],

        visible: false,
        targetItem: {},
        form: {},

        permissionItems: [],
      };
    },
    methods: {
      initialize() {
        this.list();

        permissionList().then(data => {
          this.permissionItems = data;
        });
      },
      list() {
        this.loading = true;
        roleList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      create(item) {
        // this.items.splice(0, 0, item);
        this.list();
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      destroy(id) {
        roleDestroy({ id }).then(() => {
          // this.items.splice(this.items.findIndex(item => item.id == id), 1);
          this.$message.success('删除成功');
          this.list();
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
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      openFormModal(item) {
        this.targetItem = { ...item };
        this.visible = true;
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>