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
    dataIndex: 'number',
    key: 'number',
  },
  {
    title: '产品名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]