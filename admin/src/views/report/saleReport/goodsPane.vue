<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="pagination" @change="tableChange" :loading="loading">
      <div slot="avg_retail_price" slot-scope="value">{{NP.round(value, 2)}}</div>
    </a-table>
  </div>
</template>

<script>
  import NP from 'number-precision'

  export default {
    name: 'GoodsPane',
    props: ['items', 'loading', 'pagination'],
    data() {
      return {
        NP,
        columns: [
          {
            title: '产品编号',
            dataIndex: 'goods_number',
            key: 'goods_number',
          },
          {
            title: '产品名称',
            dataIndex: 'goods_name',
            key: 'goods_name',
          },
          {
            title: '规格',
            dataIndex: 'goods_spec',
            key: 'goods_spec',
          },
          {
            title: '单位',
            dataIndex: 'unit_name',
            key: 'unit_name',
          },
          {
            title: '销售总数量',
            dataIndex: 'total_sales_quantity',
            key: 'total_sales_quantity',
          },
          {
            title: '销售总金额',
            dataIndex: 'total_sales_amount',
            key: 'total_sales_amount',
          },
          {
            title: '最低销售价',
            dataIndex: 'min_sales_price',
            key: 'min_sales_price',
          },
          {
            title: '平均销售价',
            dataIndex: 'avg_sales_price',
            key: 'avg_sales_price',
          },
          {
            title: '最高销售价',
            dataIndex: 'max_sales_price',
            key: 'max_sales_price',
          },
        ],
      };
    },
    methods: {
      tableChange(pagination, filters, sorter) {
        this.$emit('tableChange', pagination, filters, sorter)
      },
    }
  }
</script>