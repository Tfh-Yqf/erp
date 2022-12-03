<template>
  <div>
    <a-card title="账户管理">
      <a-row gutter="16">
        <a-col :span="24" style="max-width: 200px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="公司编号" allowClear @pressEnter="search" />
        </a-col>
        <a-col :span="24" style="width: 100px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="search">查询</a-button>
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal({})">新增账户</a-button>
        </div>
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
    <a-modal v-model="importLoading" :footer="null" :maskClosable="false" :closable="false">
      <div><a-spin style="margin-right: 12px;" />正在导入中, 请等待...</div>
    </a-modal>
  </div>
</template>

<script>
import { teamList, teamDestroy } from "@/api/manage";

export default {
  name: "Warehouse",
  components: {
    FormModal: () => import("./FormModal.vue"),
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
          title: "公司编号",
          dataIndex: "number",
        },
        {
          title: "到期时间",
          dataIndex: "expiry_time",
        },
        {
          title: "用户数量",
          dataIndex: "user_quantity",
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
        },
        {
          title: "备注",
          dataIndex: "remark",
        },
        {
          title: "操作",
          dataIndex: "action",
          scopedSlots: { customRender: "action" },
          width: "156px",
        },
      ],
      searchForm: { search: "", page: 1, page_size: 16 },
      pagination: { current: 1, total: 0, pageSize: 16 },
      loading: false,
      items: [],
      visible: false,
      targetItem: {},
    };
  },
  computed: {},
  methods: {
    initialize() {
      this.list();
    },
    list() {
      this.loading = true;
      teamList(this.searchForm)
        .then((response) => {
          this.pagination.total = response.data.count;
          this.items = response.data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    create(item) {
      this.list();
    },
    update(item) {
      this.list();
    },
    search() {
      this.searchForm.page = 1;
      this.pagination.current = 1;
      this.list();
    },
    openFormModal(item) {
      this.targetItem = { ...item };
      this.visible = true;
    },
    destroy(id) {
      teamDestroy({ id }).then(() => {
        let index = this.items.findIndex((item) => item.id == id);
        if (index !== -1) {
          this.items.splice(index, 1);
        }

        this.$message.success("删除成功");
      });
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
