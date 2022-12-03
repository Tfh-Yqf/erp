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
    title: '名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '编号',
    dataIndex: 'number',
    key: 'number',
  },
  {
    title: '条码',
    dataIndex: 'barcode',
    key: 'barcode',
  },
  {
    title: '单位名称',
    dataIndex: 'unit_name',
    key: 'unit_name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]