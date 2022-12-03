<template>
  <div v-if="!is_zhuce">
    <div style="">
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
          <a-form-model-item prop="username" label="用户名">
            <a-input size="large" v-model="form.username" />
          </a-form-model-item>
          <a-form-model-item prop="password" label="密码">
            <a-input-password size="large" v-model="form.password" />
          </a-form-model-item>
        </a-form-model>
      </div>

      <a-row>
        <a-col :span="14" offset="5">
          <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @tap="login">登录</a-button>
        </a-col>
      </a-row>

      <div @click="change_zhuce" style="display: flex;flex-direction: row;width: 100%;justify-content: center;margin-top: 20px;">
        <a style="font-size: 15px">没有账户？去注册</a>
      </div>

    </div>
  </div>
  <div v-else style="display: flex;flex-direction: column;">
      <div style="display: flex;flex-direction: row;width: 70%;margin-left: 10%;align-items: center">
        <a style="width: 100px;">用户名:</a>
        <a-input size="large" v-model="reg.username" />
      </div>

    <div style="display: flex;flex-direction: row;width: 70%;margin-left: 10%;align-items: center;margin-top: 20px;">
      <a style="width: 100px;">邮箱:</a>
      <a-input size="large" v-model="reg.email" />
    </div>

    <div style="display: flex;flex-direction: row;width: 70%;margin-left: 10%;align-items: center;margin-top: 20px">
      <a style="width: 100px;">验证码:</a>
      <div style="display: flex;flex-direction: row;margin-left: 5px;">
        <a-input size="large" v-model="reg.code" />
        <a-button v-if="!is_send" @click="send_email" type="primary" size="large"  style="width: 100px;margin-left: 20px;" >发送</a-button>
        <a-button v-else type="primary" size="large"  style="width: 100px;margin-left: 20px;background-color: #FFFFFF;color:black;" >{{second}}</a-button>
      </div>

    </div>

    <div style="display: flex;flex-direction: row;width: 70%;margin-left: 10%;align-items: center;margin-top: 20px">
      <a style="width: 100px;">密码:</a>
      <a-input size="large" v-model="reg.password" />
    </div>
    <div style="width: 100%;display: flex;flex-direction: row;justify-content: center;margin-top: 40px;">
      <a-button type="primary" size="large" :loading="isLoading" style="width: 200px;" @click="register_user">注册</a-button>
    </div>

    <div @click="change_zhuce" style="display: flex;flex-direction: row;width: 100%;justify-content: center;margin-top: 20px;">
      <a style="font-size: 15px">已有账户？去登录</a>
    </div>

    <div  style="display: flex;flex-direction: row;width: 100%;justify-content: center;margin-top: 20px;color: red">
      <a style="font-size: 15px;color: red">{{warn}}</a>
    </div>
  </div>
</template>

<script>
  import { getToken,reg,sendemail } from '@/api/user';
  import Cookies from 'js-cookie';

  export default {
    name: 'Login',
    data() {
      return {
        wechatCustomerService: require('@/assets/wechat_customer_service.png'),
        isLoading: false,
        form: {
          number: '1',
          username: '',
          password: '',
        },
        reg:{
          email:'',
          password:'',
          code:'',
          username:''
        },
        rules: {
          number: [
            { required: true, message: '请输入公司编号', trigger: 'change' },
          ],
          username: [
            { required: true, message: '请输入用户名', trigger: 'change' },
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'change' },
          ],
        },
        is_zhuce:false,
        second:60,
        is_send:false,
        warn:'',
        code_interval:null
      };
    },
    mounted() {
      // this.$router.push('/home');
    },
    methods: {
      send_email(){
        if(this.reg.email==''){
          this.warn = '邮箱不能为空！';
          return;
        }
        this.is_send=true;
        this.second=60;
        var that = this;
        this.code_interval = setInterval(function (){
          if(that.second==0){
            that.is_send=false;
            clearInterval(that.code_interval);
          }else{
            that.second--;
          }
        },1000);
        sendemail(this.reg.email).then(data=>{
          console.log(data);
        }).finally((res)=>{
          console.log(res);
        });
      },
      register_user(){
        if(this.reg.email==''||this.reg.code==''||this.reg.password==''||this.reg.username==''){
          this.warn = '未填写完整';
          return;
        }
        var that = this;
        reg(this.reg).then(data => {
          console.log(data);
          if(data.code==0){
            that.warn="注册成功！";
            that.change_zhuce();
          }else{
            that.warn = data.msg;
            that.reg.code='';
          }
        }).finally((res) => {
          console.log(res);

        });
      },
      change_zhuce(){
        this.is_zhuce=!this.is_zhuce;
      },
      initialize() {
        document.onkeypress = (e) => {
          let code = document.all ? event.keyCode : e.which;
          if (code == 13) {
            this.login();
            return false;
          }
        }
      },
      login() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.isLoading = true;
            console.log(this.form);
            getToken(this.form).then(data => {
              Cookies.set('access', data.access);
              Cookies.set('refresh', data.refresh);
              this.$router.push('/home');
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
  .reg_group{

  }
</style>