<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑收支项目' : '新增收支项目' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="收支项目">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="type" label="收支类型">
            <a-select v-model="form.type" style="width: 100%;">
              <a-select-option value="income">收入</a-select-option>
              <a-select-option value="expenditure">支出</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="remark" label="备注">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { revenueExpenditureItemsCreate, revenueExpenditureItemsUpdate } from '@/api/basicData'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'roleName'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '请输入收支项目', trigger: 'change' }],
          type: [{ required: true, message: '请选择收支类型', trigger: 'change' }]
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? revenueExpenditureItemsUpdate : revenueExpenditureItemsCreate;
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