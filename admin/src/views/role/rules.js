export default {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'change' },
    { max: 64, message: '超出最大长度 (64)', trigger: 'change' },
  ],
  remark: [{ max: 256, message: '超出最大长度 (256)', trigger: 'change' }],
}