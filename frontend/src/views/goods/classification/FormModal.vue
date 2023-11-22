<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑产品分类' : '新增产品分类' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item  label="分类名称">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item  label="备注">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
          <a-form-model-item  label="均价">
            <a-input v-model="form.average_price" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { goodsClassificationCreate, goodsClassificationUpdate } from '@/api/goods'
  import {add_average} from '@/api/new'
  export default {
    name: 'FormModal',
    props: ['visible', 'form'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '请输入分类名称', trigger: 'change' }]
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            // test
            // add_average(this.form).then(res=>{
            //   console.log(res);
            //   this.$message.success('联级修改成功');
            // }).finally(re=>{
            //
            // })
            this.loading = true;
            let func = this.form.id ? goodsClassificationUpdate : goodsClassificationCreate;
            func(this.form).then(data => {
              console.log(data);
              this.$message.success(this.form.id ? '修改成功' : '新增成功');


              var temp = {...data,...this.form};
              console.log(temp);
              add_average(temp).then(res=>{
                console.log(res);
                // this.$message.success('联级修改成功');
                this.cancel();
                this.$emit(this.form.id ? 'update' : 'create', data);
              }).finally(re=>{

              })
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