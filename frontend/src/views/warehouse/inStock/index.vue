<template>
  <div>
    <a-card :tab-list="tabList" :active-tab-key="currentTab" @tabChange="tabChange">
      <div v-if="currentTab == 'inStockOrder'">
        <in-stock-order></in-stock-order>
      </div>
      <div v-else-if="currentTab == 'inStockRecord'">
        <in-stock-record></in-stock-record>
      </div>
    </a-card>
  </div>
</template>

<script>
  export default {
    components: {
      InStockOrder: () => import('./inStockOrder'),
      InStockRecord: () => import('./inStockRecord'),
    },
    data() {
      return {
        tabList: [
          {
            key: 'inStockOrder',
            tab: '入库通知单',
          },
          {
            key: 'inStockRecord',
            tab: '入库记录',
          },
        ],
        currentTab: undefined,
      }
    },
    methods: {
      initData() {
        let currentTab = this.$route.query.currentTab;
        if (currentTab) {
          this.currentTab = currentTab;
        } else {
          this.currentTab = this.tabList[0].key;
          this.$router.push({ query: { currentTab: this.currentTab } });
        }
      },
      tabChange(key) {
        this.currentTab = key;
        this.$router.push({ query: { currentTab: this.currentTab } });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>