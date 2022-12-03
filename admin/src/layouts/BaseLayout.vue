<template>
  <div>
    <a-layout>
      <a-layout-sider class="sidebar" width="256" v-model="collapsed" :trigger="null" collapsible>
        <sidebar :collapsed="collapsed" />
      </a-layout-sider>

      <a-layout v-if="isLogin">
        <a-layout-header class="headbar">
          <headbar :collapsed="collapsed" :username="username" @toggleCollapsed="toggleCollapsed" />
        </a-layout-header>

        <a-layout-content>
          <router-view v-if="isRouterAlive" style="padding: 8px;" />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import { superUserInfo } from "@/api/manage";
import moment from "moment";

export default {
  name: "BaseLayout",
  components: {
    Headbar: () => import("@/components/Headbar/Headbar"),
    Sidebar: () => import("@/components/Sidebar/Sidebar"),
  },
  provide() {
    return {
      reloadPage: () => {
        return this.reloadPage();
      },
    };
  },
  data() {
    return {
      isLogin: false,
      collapsed: false,
      isRouterAlive: true,
      username: "222",
    };
  },
  methods: {
    initialize() {
      superUserInfo()
        .then((response) => {
          this.isLogin = true;
          this.username = response.data.username;
          if (response.data.warning_list && response.data.warning_list.length > 0) {
            for (let item of response.data.warning_list) {
              let diffDay = moment(item.expiry_time).diff(moment(), "day");
              setTimeout(() => {
                this.$notification.warning({
                  message: `到期提醒: ${item.number}`,
                  description: `到期: ${moment(item.expiry_time).format("YYYY-MM-DD HH:mm:ss")}, 剩余: ${diffDay}天`,
                  duration: 0,
                });
              }, 500);
            }
          }
        })
        .catch((error) => {
          console.log(error.response);
          if (error.response.status == 401) {
            this.$router.push("/user/login");
          }
        });
    },
    toggleCollapsed() {
      this.collapsed = !this.collapsed;
    },
    reloadPage() {
      this.isRouterAlive = false;
      this.$nextTick(() => (this.isRouterAlive = true));
    },
  },
  mounted() {
    this.initialize();
  },
};
</script>

<style scoped>
.headbar {
  background: #fff;
  padding: 0;
  box-shadow: 0px 1px 10px #7774;
}

.sidebar {
  background: #fff;
  overflow: auto;
  box-shadow: 1px 0px 10px #7774;
}
</style>
