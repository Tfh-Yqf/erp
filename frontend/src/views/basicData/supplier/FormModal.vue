<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑供应商' : '新增供应商' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="供应商名称">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="供应商编号">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="contact" label="联系人">
            <a-input v-model="form.contact" />
          </a-form-model-item>
          <a-form-model-item prop="phone" label="手机号">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="email" label="邮箱">
            <a-input v-model="form.email" />
          </a-form-model-item>
          <a-form-model-item prop="address" label="地址">
            <a-input v-model="form.address" />
          </a-form-model-item>
          <a-form-model-item prop="bank_account" label="银行账户">
            <a-input v-model="form.bank_account" />
          </a-form-model-item>
          <a-form-model-item prop="bank_name" label="开户行">
            <a-input v-model="form.bank_name" />
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
          <a-form-model-item prop="initial_arrears_amount" label="初期欠款金额">
            <a-input-number v-model="form.initial_arrears_amount" style="width: 100%;" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>


<script>
  import { supplierCreate, supplierUpdate } from '@/api/basicData'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'suppliersClassificationOptions'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '请输入名称', trigger: 'change' }],
          number: [{ required: true, message: '请输入编号', trigger: 'change' }],
          initial_arrears_amount: [
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '初期欠款金额格式不正确', trigger: 'change' }
          ],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? supplierUpdate : supplierCreate;
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