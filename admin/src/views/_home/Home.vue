<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24">
        <sales-trend />
        <sales-goods style="margin-top: 12px;"/>
      </a-col>
      <a-col :span="24">
        <a-col :span="12">
          <stock-out-task style="margin-top: 12px;"/>
        </a-col>
        <a-col :span="12">
          <stock-in-task style="margin-top: 12px;"/>
        </a-col>
        <a-col :span="12">
          <inventory-warnings style="margin-top: 12px;"/>
        </a-col>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    components: {
      SalesTrend: () => import('./salesTrend.vue'),
      StockOutTask: () => import('./stockOutTask.vue'),
      StockInTask: () => import('./stockInTask.vue'),
      SalesGoods: () => import('./salesGoods.vue'),
      InventoryWarnings: () => import('./inventoryWarnings.vue'),
    },
  }
</script>