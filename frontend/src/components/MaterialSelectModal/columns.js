export const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    customRender: (value, item, index) => {
      return index + 1
    },
  },
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
    title: '库存数量',
    dataIndex: 'total_quantity',
    key: 'total_quantity',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]