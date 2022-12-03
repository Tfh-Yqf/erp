<template>

  <div  class="background" style="display: flex;flex-direction: column;justify-content: center;width: 100%;">
    <div style="background-color: #fff;border-radius: 10px;width: 300px;margin-left: 70%">
      <div style="text-align: center; padding-top: 16px">
        <img :src="logo" width="100" style="cursor: pointer; margin-top: 16px" @click="backIndex" />
      </div>
      <div class="title" style="margin-top: 16px">
        <span style="cursor: pointer; font-size: 24px" >Build Storage</span>
      </div>
      <div style="text-align: center; font-size: 16px; color: #1890ff; margin-top: 8px; margin-bottom: 24px">
        <span>建筑仓储管理系统</span>
      </div>
      <div style="width: 100%;display: flex;flex-direction: row;justify-content: center;margin-bottom: 30px;">
        <a-button @click="jump_login" type="primay" size="large" style="background-color: #3c9cff;color:#FFF">立即开始</a-button>
      </div>


    </div>

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
  width: 480px;
  border-radius: 8px;
  padding-bottom: 64px;
  margin: auto;
}

.background {
  min-height: 100%;
  padding: 10vh 0;
  background: url("https://vkceyugu.cdn.bspapp.com/VKCEYUGU-c84ba6b8-76a1-4911-86f7-95839ee7bd57/eb70a786-4162-441b-b497-49a6ce8caa0d.jpg") ;
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
