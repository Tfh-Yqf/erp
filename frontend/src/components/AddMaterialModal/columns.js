export default [
  {
    title: '产品编号',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '产品名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '产品单位',
    dataIndex: 'unit_name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]