<template>
  <div>
    <a-card title="员工账号">
      <a-row gutter="16">
        <a-col :span="24" :md="8" :xl="6" style="margin-bottom: 12px;">
          <a-input-search v-model="searchForm.search" placeholder="用户名, 名称, 电话" allowClear @search="search" />
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="targetItem = {...form}; visible = true;">
            新增账号</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table rowKey="id" size="small" :columns="columns" :dataSource="items" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="status" slot-scope="value">
            <template v-if="value">
              <a-badge status="success" />
              <span>启用</span>
            </template>
            <template v-else>
              <a-badge status="error" />
              <span>禁用</span>
            </template>
          </div>
          <div slot="role_names" slot-scope="roleNames">
            <a-tag v-for="role in roleNames" :key="role" color="#2db7f5">
              {{role}}
            </a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="targetItem = {...item}; visible = true;">编辑</a-button>
              <a-popconfirm title="确定重置吗? 密码: 123456" @confirm="resetPassword(item.id)">
                <a-button size="small" type="primary" icon="sync">重置密码</a-button>
              </a-popconfirm>
              <a-popconfirm title="确定删除吗?" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">删除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
          <!-- <div slot="expandedRowRender" slot-scope="item">
            <div style="font-weight: bold; font-size: 15px;">拥有权限:</div>
            <a-row>
              <a-col v-for="key in item.permissions" :key="key" :span="4">{{permissions[key]}}</a-col>
            </a-row>
          </div> -->
        </a-table>
      </a-row>
    </a-card>

    <form-modal v-model="visible" :form="targetItem" :roleItems="roleItems" @create="create" @update="update" />
  </div>
</template>

<script>
  import { userList, userDestroy, userResetPassword } from '@/api/account'
  import { roleOption } from '@/api/option'
  import { permissions } from '@/permissions.js'
  import columns from './columns.js'

  export default {
    name: 'Account',
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
        roleItems: [],
        visible: false,
        targetItem: {},
        form: {},
      };
    },
    methods: {
      initialize() {
        this.list();

        roleOption({ page_size: 999999 }).then(data => {
          this.roleItems = data.results;
        });
      },
      list() {
        this.loading = true;
        userList(this.searchForm).then(data => {
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
        userDestroy({ id }).then(() => {
          // this.items.splice(this.items.findIndex(item => item.id == id), 1);
          this.$message.success('删除成功');
          this.list();
        });
      },
      resetPassword(id) {
        userResetPassword({ id }).then(() => {
          this.$message.success('重置成功');
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