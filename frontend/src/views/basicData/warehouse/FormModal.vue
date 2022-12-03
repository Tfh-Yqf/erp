<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑仓库' : '新增仓库' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="仓库名称">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="仓库编号">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="manager" label="管理员">
            <a-select v-model="form.manager" style="width: 100%">
              <a-select-option v-for="item in usersOptions" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="phone" label="手机号">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="address" label="地址">
            <a-input v-model="form.address" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="备注">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="is_active" label="状态">
            <a-select v-model="form.is_active" style="width: 100%;">
              <a-select-option :value="true">激活</a-select-option>
              <a-select-option :value="false">冻结</a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { warehouseCreate, warehouseUpdate } from '@/api/basicData'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'usersOptions'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '请输入仓库名称', trigger: 'change' }],
          number: [{ required: true, message: '请输入仓库编号', trigger: 'change' }],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? warehouseUpdate : warehouseCreate;
            func(this.form).then(data => {
              this.$message.success(this.form.id ? '修改成功' : '新增成功');
              this.$emit(this.form.id ? 'update' : 'create', data);
              this.cancel();
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.$refs.form.resetFields();
      },
    },
  }
</script>

<style scoped>
</style>