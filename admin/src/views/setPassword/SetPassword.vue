<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" />
        </a-form-model-item>
        <a-form-model-item prop="old_password" label="旧密码">
          <a-input-password size="large" v-model="form.old_password" />
        </a-form-model-item>
        <a-form-model-item prop="new_password" label="新密码">
          <a-input-password size="large" v-model="form.new_password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="确认密码">
          <a-input-password size="large" v-model="form.confirm" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="link" style="float: left; padding: 0;" @click="$router.push('/user/login')">返回登录</a-button>
      </a-col>
    </a-row>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="setPassword">修改密码
        </a-button>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { setPassword } from '@/api/user'

  export default {
    name: 'SetPassword',
    data() {
      return {
        isLoading: false,
        form: {
          username: '',
          old_password: '',
          new_password: '',
          confirm: '',
        },
        rules: {
          username: [{ required: true, message: '请输入手机号', trigger: 'change' }],
          old_password: [{ required: true, message: '请输入旧密码', trigger: 'change' }],
          new_password: [{ required: true, message: '请输入新密码', trigger: 'change' }],
          confirm: [
            { required: true, message: '请再次输入新密码', trigger: 'change' },
            { validator: this.validateConfirm, trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      validateConfirm(rule, value, callback) {
        return value === this.form.new_password ? callback() : callback(new Error('两次输入密码不一致'))
      },
      setPassword() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.isLoading = true;
            setPassword(this.form)
              .then(() => {
                this.$message.success('设置成功');
                this.$router.push('/user/login');
              })
              .catch(err => {
                this.$message.error(err.response.data.error);
              })
              .finally(() => {
                this.isLoading = false;
              });
          }
        });
      },
    },
  }
</script>