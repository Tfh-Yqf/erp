export default {
  username: [{ required: true, message: '请输入用户名', trigger: 'change' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'change' }],
  phone: [
    { max: 32, message: '超出最大长度 (32)', trigger: 'change' },
  ],
  email: [
    { max: 256, message: '超出最大长度 (256)', trigger: 'change' },
  ],
  sex: [{ required: true, message: '请输选择性别', trigger: 'change' }],
}