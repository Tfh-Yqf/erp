<template>


  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username"/>
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password"/>
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="login">登录</a-button>
      </a-col>
    </a-row>


  </div>


</template>

<script>
import {getToken} from '@/api/user';
import Cookies from 'js-cookie';

export default {
  name: 'Login',
  data() {
    return {
      selectedKeys: ['login'],
      isLoading: false,
      form: {
        number: '2',
        username: '',
        password: '',
      },
      reg: {
        email: '',
        password: '',
        code: '',
        username: ''
      },
      rules: {
        number: [
          {required: true, message: '请输入公司编号', trigger: 'change'},
        ],
        username: [
          {required: true, message: '请输入用户名', trigger: 'change'},
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'change'},
        ],
      },
      second: 60,
      is_send: false,
      warn: '',
      code_interval: null
    };
  },
  methods: {

    initialize() {
      document.onkeypress = (e) => {
        let code = document.all ? event.keyCode : e.which;

      }
    },
    login() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.isLoading = true;
          console.log(this.form);
          getToken(this.form).then(data => {
            this.$message.success('登录成功');
            Cookies.set('access', data.access);
            Cookies.set('refresh', data.refresh);
            this.$router.push('/basicData/client');
          }).finally(() => {
            this.isLoading = false;
          });
        }
      });
    },
  },
  created() {
    this.initialize();
  },
}
</script>

<style>
.reg_group {
}
</style>