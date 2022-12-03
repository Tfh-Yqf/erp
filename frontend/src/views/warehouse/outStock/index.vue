<template>
  <div>
    <a-card :tab-list="tabList" :active-tab-key="currentTab" @tabChange="tabChange">
      <div v-if="currentTab == 'outStockOrder'">
        <out-stock-order></out-stock-order>
      </div>
      <div v-else-if="currentTab == 'outStockRecord'">
        <out-stock-record></out-stock-record>
      </div>
    </a-card>
  </div>
</template>

<script>
  export default {
    components: {
      outStockOrder: () => import('./outStockOrder'),
      outStockRecord: () => import('./outStockRecord'),
    },
    data() {
      return {
        tabList: [
          {
            key: 'outStockOrder',
            tab: '出库通知单',
          },
          {
            key: 'outStockRecord',
            tab: '出库记录',
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