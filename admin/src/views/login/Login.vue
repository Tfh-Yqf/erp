<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="username" label="用户名">
          <a-input size="large" v-model="form.username" @pressEnter="login" />
        </a-form-model-item>
        <a-form-model-item prop="password" label="密码">
          <a-input-password size="large" v-model="form.password" @pressEnter="login" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="login">登录</a-button>
      </a-col>
    </a-row>

    <div style="text-align: center; width: 100%; margin-top: 24px;">
      <div>
        试用，购买或问题咨询请扫描下方客户经理二维码
      </div>
      <div>
        <img :src="wechatCustomerService" width="100" style="margin-top: 8px;" />
      </div>
    </div>
  </div>
</template>

<script>
import { superUserLogin } from "@/api/manage";

export default {
  name: "Login",
  data() {
    return {
      wechatCustomerService: require("@/assets/wechat_customer_service.png"),
      isLoading: false,
      form: {
        username: "",
        password: "",
      },
      rules: {
        username: [{ required: true, message: "请输入用户名", trigger: "change" }],
        password: [{ required: true, message: "请输入密码", trigger: "change" }],
      },
    };
  },
  methods: {
    login() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.isLoading = true;
          superUserLogin(this.form)
            .then((data) => {
              this.$router.push("/");
            })
            .finally(() => {
              this.isLoading = false;
            });
        }
      });
    },
  },
};
</script>
