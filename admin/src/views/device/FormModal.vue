<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "编辑设备" : "新增设备" }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="number" label="编号">
            <a-input v-model="form.number" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="name" label="名称">
            <a-input v-model="form.name" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="model" label="型号">
            <a-input v-model="form.model" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="serial_number" label="序列号">
            <a-input v-model="form.serial_number" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="account_ownership" label="账号归属">
            <a-input v-model="form.account_ownership" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { deviceCreate, deviceUpdate } from "@/api/manage";

export default {
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules: {
        number: [{ required: true, message: "请输入编号", trigger: "change" }],
        name: [{ required: true, message: "请输入名称", trigger: "change" }],
      },
      loading: false,
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          let func = this.form.id ? deviceUpdate : deviceCreate;
          func(this.form)
            .then((data) => {
              this.$message.success(this.form.id ? "修改成功" : "新增成功");
              this.$emit(this.form.id ? "update" : "create", data);
              this.cancel();
            })
            .catch((error) => {
              this.$message.error(error.response.data.detial);
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    cancel() {
      this.$emit("cancel", false);
      this.$refs.form.resetFields();
    },
  },
};
</script>

<style scoped></style>
