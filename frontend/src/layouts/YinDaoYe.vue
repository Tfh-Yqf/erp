<template>

  <div  class="background" >
    <a-card class="card" :title="ProjectName">
      <div style="text-align: center; padding-top: 16px">
        <img :src="logo" width="120" style="cursor: pointer; margin-top: 16px"/>
      </div>

      <div style="width: 100%;display: flex;flex-direction: row;justify-content: center;margin-bottom: 30px;">
        <a-button @click="jump_login" type="primay" size="large" style="background-color: #50799e;color:#FFF;width: 200px;">立即开始</a-button>
      </div>
    </a-card>
 

  </div>
</template>

<script>
export default {
  name: "yindao",
  data() {
    return {
      logo: require("@/assets/logo.png")
    };
  },
  methods: {
    jump_login(){
      this.$router.push('/user/login');
    }
  },
};
</script>

<style scoped>
.card {
  width: 450px;
  border-radius: 8px;
  padding-bottom: 64px;
  margin: auto;
}

.background {
  min-height: 100%;
  padding: 10vh 0;
  background: url("https://pic2.ziyuan.wang/user/tanfuhua/2024/08/v2-e2d0fa9819c540732a4e7e980d5b48a9_r_26ba0cd0fea17.jpg") ;
  background-size: 100% 100%;
}

.title {
  text-align: center;
  font-size: 32px;
  color: #1890ff;
  margin-top: 8px;
  font-weight: bold;
}
</style>
