<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "编辑账户" : "新增账户" }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="number" label="公司编号">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="expiry_time" label="到期时间">
            <a-date-picker v-model="form.expiry_time" showTime valueFormat="YYYY-MM-DD HH:mm:ss" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="user_quantity" label="子账户数量">
            <a-input v-model="form.user_quantity" />
          </a-form-model-item>
          <a-form-model-item v-if="!form.id" prop="username" label="用户名">
            <a-input v-model="form.username" />
          </a-form-model-item>
          <a-form-model-item v-if="!form.id" prop="password" label="密码">
            <a-input v-model="form.password" />
          </a-form-model-item>
          <a-form-model-item v-if="!form.id" prop="name" label="客户名称">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="备注">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { teamCreate, teamUpdate } from "@/api/manage";

export default {
  name: "FormModal",
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules: {
        number: [{ required: true, message: "请输入编号", trigger: "change" }],
        expiry_time: [{ required: true, message: "请选择到期时间", trigger: "change" }],
        user_quantity: [{ required: true, message: "请输入用户数量", trigger: "change" }],
        username: [{ required: true, message: "请输入用户名", trigger: "change" }],
        password: [{ required: true, message: "请输入密码", trigger: "change" }],
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
          let func = this.form.id ? teamUpdate : teamCreate;
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
