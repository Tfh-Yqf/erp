<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="pagination" @change="tableChange" :loading="loading">
      <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      <div slot="relation_order" slot-scope="value">
        <a-button type="link" @click="openInvoice(value)">查看</a-button>
      </div>
    </a-table>
  </div>
</template>

<script>
  import moment from 'moment'

  export default {
    name: 'FlowPane',
    props: ['items', 'loading', 'pagination'],
    data() {
      return {
        moment,
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
            title: '分类名称',
            dataIndex: 'category_name',
            key: 'category_name',
          },
          {
            title: '单位',
            dataIndex: 'unit_name',
            key: 'unit_name',
          },
          {
            title: '采购单价',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
          },
          {
            title: '总金额',
            dataIndex: 'total_amount',
            key: 'total_amount',
          },
          {
            title: '采购单号',
            dataIndex: 'purchase_order_number',
            key: 'purchase_order_number',
          },
          {
            title: '仓库',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '供应商',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
          {
            title: '创建人',
            dataIndex: 'creator_name',
            key: 'creator_name',
          },
          {
            title: '创建时间',
            dataIndex: 'create_time',
            key: 'create_time',
          },
        ],
      };
    },
    methods: {
      openInvoice(id) {
        window.open(`/invoice/sales?id=${id}`);
      },
      tableChange(pagination, filters, sorter) {
        this.$emit('tableChange', pagination, filters, sorter)
      },
    },
  }
</script>