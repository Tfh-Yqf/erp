<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">编辑产品预期销售 </div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="产品名称">
            <a-input v-model="form.goods_name" disabled="true"/>
          </a-form-model-item>
          <a-form-model-item prop="remark" label="产品库存数量">
            <a-input v-model="form.total_quantity" allowClear disabled="true" />
          </a-form-model-item>
          <a-form-model-item prop="average_price" label="预期销售数量">
            <a-input v-model="form.predict_number" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="average_price" label="预期销售金额">
            <a-input v-model="form.predict_price" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
      <div style="width: 100%;text-align: center">
        <a style="color: red">{{warn}}</a>
      </div>

    </a-modal>
  </div>
</template>

<script>
  import { update_predict} from '@/api/new'

  export default {
    name: 'FormModal',
    props: ['visible', 'form'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
        },
        loading: false,
        warn:''
      };
    },
    methods: {
      confirm() {
        if(this.form.predict_number==null||this.form.predict_price==null){
          this.warn = '不能为空！';
          return;
        }
        this.loading = true;

        update_predict(this.form).then(data => {
          console.log(data);
          this.$message.success( '修改成功' );
          this.$emit(this.form.id ? 'update' : 'create', data);
          this.cancel();

        }).finally(() => {
          this.loading = false;
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