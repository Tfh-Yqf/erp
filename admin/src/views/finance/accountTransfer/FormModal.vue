<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑账户转账' : '新增账户转账' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="out_account" label="转出账户">
            <a-select v-model="form.out_account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="transfer_out_time" label="转出时间">
            <a-date-picker v-model="form.transfer_out_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="in_account" label="转入账户">
            <a-select v-model="form.in_account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="transfer_in_time" label="转入时间">
            <a-date-picker v-model="form.transfer_in_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="transfer_amount" label="转账金额">
            <a-input-number v-model="form.transfer_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="service_charge_amount" label="手续费金额">
            <a-input-number v-model="form.service_charge_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="service_charge_payer" label="手续费支付方">
            <a-select v-model="form.service_charge_payer" style="width: 100%">
              <a-select-option v-for="item in chargeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="handler" label="经手人">
            <a-select v-model="form.handler" style="width: 100%">
              <a-select-option v-for="item in handlerItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="handle_time" label="处理时间">
            <a-date-picker v-model="form.handle_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
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
  import { accountTransferOrderCreate } from '@/api/finance'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'handlerItems', 'accountsItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        chargeItems: [
          { id: 'transfer_in', name: '转入账户支付' },
          { id: 'transfer_out', name: '转出账户支付' }
        ],
        rules: {
          out_account: [{ required: true, message: '请选择转出账户', trigger: 'change' }],
          transfer_out_time: [{ required: true, message: '请选择转出时间', trigger: 'change' }],
          in_account: [{ required: true, message: '请选择转入账户', trigger: 'change' }],
          transfer_in_time: [{ required: true, message: '请选择转入账户', trigger: 'change' }],
          transfer_amount: [
            { required: true, message: '请输入转账金额', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '转账金额格式不正确', trigger: 'change' }
          ],
          service_charge_amount: [
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '手续费金额格式不正确', trigger: 'change' }
          ],
          handler: [{ required: true, message: '请选择经手人', trigger: 'change' }],
          handle_time: [{ required: true, message: '请选择处理时间', trigger: 'change' }],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? accountTransferOrderCreate : accountTransferOrderCreate;
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