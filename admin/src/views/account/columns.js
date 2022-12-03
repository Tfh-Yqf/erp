export default [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    customRender: (value, item, index) => {
      return index + 1
    },
  },
  {
    title: '用户名',
    dataIndex: 'username',
    sorter: true,
  },
  {
    title: '员工姓名',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '手机号',
    dataIndex: 'phone',
  },
  {
    title: "状态",
    dataIndex: "status",
    key: "status",
    scopedSlots: { customRender: "status" },
  },
  {
    title: '角色',
    dataIndex: 'role_names',
    scopedSlots: { customRender: 'role_names' },
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
    width: '256px'
  },
]