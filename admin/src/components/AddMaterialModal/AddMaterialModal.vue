<template>
  <div>
    <a-modal v-model="visible" title="选择产品" :footer="null" :maskClosable="false" @cancel="cancel">
      <div>
        <a-input-search v-model="searchForm.search" placeholder="输入查询..." @search="search" />
      </div>
      <div style="margin-top: 12px;">
        <a-table :columns="columns" :data-source="items" :loading="loading" size="small" :pagination="pagination">
          <div slot="action" slot-scope="value, item">
            <a-button size="small" @click="select(item)">选择</a-button>
          </div>
        </a-table>
      </div>
    </a-modal>

    <a-modal v-model="formVisible" :maskClosable="false" okText="确定" cancelText="取消" :title="targetItem.name"
      @ok="confirm">
      <a-form-model ref="form" :model="targetItem" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
        <a-form-model-item prop="quantity" label="产品数量">
          <a-input-number v-model="targetItem.quantity" :min="0" style="width: 100%;" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { materialList } from '@/api/manage'
  import columns from './columns.js'

  export default {
    name: 'AddMaterialModal',
    props: ['visible', 'order', 'addOrderMaterial'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        columns,
        searchForm: { search: '', page: 1, ordering: undefined, page_size: 10 },
        pagination: { current: 1, total: 0, pageSize: 10 },
        loading: false,
        items: [],
        formVisible: false,
        targetItem: {},
        rules: {
          quantity: [
            { required: true, message: '请输入产品数量', trigger: 'change' },
            { validator: this.validateQuantity, trigger: 'change' },
          ],
        },
      };
    },
    methods: {
      list() {
        this.loading = true;
        materialList(this.searchForm)
          .then(resp => {
            this.pagination.total = resp.data.count;
            this.items = resp.data.results;
          })
          .catch(err => {
            this.$message.error(err.response.data.message);
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
      select(item) {
        this.targetItem = { ...item };
        this.formVisible = true;
      },
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.targetItem.order = this.order;
            this.targetItem.material = this.targetItem.id;
            this.addOrderMaterial(this.targetItem)
              .then(resp => {
                this.$message.success('添加成功');
                this.$emit('confirm', resp.data);
                this.cancel();
              })
              .catch(err => {
                this.$message.error(err.response.data.error);
              })
              .finally(() => {
                this.loading = false;
              });
          }
        });
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
      cancel() {
        this.formVisible = false;
        this.$emit('cancel', false);
        this.$refs.form.resetFields();
        this.items = [];
        this.searchForm = { search: '', page: 1, ordering: undefined, page_size: 10 };
        this.pagination = { current: 1, total: 0, pageSize: 16 };
      },
      validateQuantity(rule, value, callback) {
        return value > 0 ? callback() : callback(new Error('产品数量需要大于0'))
      },
    },
    watch: {
      visible(value) {
        if (value) {
          this.list();
        }
      },
    },
  }
</script>

<style scoped>
</style>