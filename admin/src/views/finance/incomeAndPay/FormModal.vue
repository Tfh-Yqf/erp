<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑日常收支' : '新增日常收支' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="number" label="编号">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="type" label="收支类型">
            <a-select v-model="form.type" style="width: 100%">
              <a-select-option v-for="item in typeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="client" label="客户">
            <a-select v-model="form.client" style="width: 100%">
              <a-select-option v-for="item in clientsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="supplier" label="供应商">
            <a-select v-model="form.supplier" style="width: 100%">
              <a-select-option v-for="item in suppliersItems" :key="item.id" :value="item.id">
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
          <a-form-model-item prop="charge_item" label="收支项目">
            <a-select v-model="form.charge_item" style="width: 100%">
              <a-select-option v-for="item in chargeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="account" label="结算账户">
            <a-select v-model="form.account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="total_amount" label="应收/付金额">
            <a-input-number v-model="form.total_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="charge_amount" label="实收/付金额">
            <a-input-number v-model="form.charge_amount" style="width: 100%;" />
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
  import { chargeOrderCreate } from '@/api/finance'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'clientsItems', 'suppliersItems', 'chargeItems', 'handlerItems', 'accountsItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        typeItems: [
          { id: 'income', name: '收入' },
          { id: 'expenditure', name: '支出' }
        ],
        rules: {
          number: [{ required: true, message: '请输入编号', trigger: 'change' }],
          type: [{ required: true, message: '请选择收支类型', trigger: 'change' }],
          account: [{ required: true, message: '请选择结算账户', trigger: 'change' }],
          total_amount: [
            { required: true, message: '请输入应收/付金额', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '应收/付金额格式不正确', trigger: 'change' }
          ],
          charge_amount: [
            { required: true, message: '请输入实收/付金额', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '实收/付金额格式不正确', trigger: 'change' }
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
            let func = this.form.id ? chargeOrderCreate : chargeOrderCreate;
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