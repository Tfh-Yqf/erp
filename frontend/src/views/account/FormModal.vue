<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑账号' : '新增账号' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="username" label="用户名">
            <a-input v-model="form.username" />
          </a-form-model-item>
          <a-form-model-item prop="name" label="员工姓名">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="phone" label="手机号">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="email" label="邮箱">
            <a-input v-model="form.email" />
          </a-form-model-item>
          <a-form-model-item prop="sex" label="性别">
          <a-select
            default-value="man"
            style="width: 100%"
            v-model="form.sex">
            <a-select-option value="man"> 男 </a-select-option>
            <a-select-option value="woman"> 女 </a-select-option>
          </a-select>
        </a-form-model-item>
          <a-form-model-item prop="is_active" label="状态">
            <a-select v-model="form.is_active" style="width: 100%;">
              <a-select-option :value="true">启用</a-select-option>
              <a-select-option :value="false">禁用</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="roles" label="角色">
            <a-select v-model="form.roles" mode="multiple" allowClear style="width: 100%;">
              <a-select-option v-for="item in roleItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>

        <div v-if="!form.id" style="color: rgb(255, 77, 79); text-align: center;">
          默认初始密码为: 123456, 登录后请修改密码
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { userCreate, userUpdate } from '@/api/account'
  import rules from './rules.js'

  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'roleItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules,
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? userUpdate : userCreate;
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