<template>
  <div>
    <div style="float: left;">
      <a-icon class="trigger" :type="collapsed ? 'menu-unfold' : 'menu-fold'" @click="$emit('toggleCollapsed')" />
    </div>
    <div style="float: right;">
       <a-dropdown :trigger="['click']">
        <span class="trigger">
          {{currentWarehouse}}
          <a-icon type="down" />
        </span>
        <a-menu slot="overlay">
          <a-menu-item v-for="item in warehouseItems" :key="item.id" @click="onChangeWarehouse(item)">
            <span>{{item.name}}</span>
          </a-menu-item>
        </a-menu>
      </a-dropdown>

      <a-dropdown :trigger="['click']">
        <span class="trigger">
          {{username}}
          <a-icon type="down" />
        </span>
        <a-menu slot="overlay">
          <a-menu-item @click="$router.push('/user/set_password')">
            <span>修改密码</span>
          </a-menu-item>
          <a-menu-divider />
          <a-menu-item @click="logout">
            <span>退出登录</span>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
  // import { warehouseOption } from '@/api/option';
  import Cookies from 'js-cookie';

  export default {
    name: 'Headbar',
    props: ['collapsed', 'username'],
    inject: ['reloadPage'],
    data() {
      return {
        warehouseItems: [],
        currentWarehouse: '所有仓库',
      };
    },
    methods: {
      initData() {
        // warehouseOption({ page_size: 999999 }).then(data => {
        //   console.log(data.results)
        //   this.warehouseItems = [{ id: undefined, name: '所有仓库' }, ...data.results];
        // });
      },
      logout() {
        Cookies.remove('access');
        Cookies.remove('refresh');
        this.$router.push('/user/login');
      },
      onChangeWarehouse(item) {
        this.currentWarehouse = item.name;
        this.$store.commit('setWarehouse', item.id);
        this.reloadPage();
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>

<style scoped>
  .trigger {
    font-size: 18px;
    line-height: 64px;
    padding: 0 24px;
    cursor: pointer;
    transition: color 0.3s;
  }

  .trigger:hover {
    color: #1890ff;
  }
</style>