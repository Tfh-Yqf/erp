<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">生产</div>
      <div>
        <a-form-model ref="form" :model="dataForm" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="production_quantity" label="生产数量">
            <a-input-number v-model="dataForm.production_quantity" style="width: 100%;" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { productionRecordCreate } from "@/api/production";

export default {
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules: {
        production_quantity: [{ required: true, message: "请输入生产数量", trigger: "change" }],
      },
      loading: false,
      dataForm: {},
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          productionRecordCreate(this.dataForm)
            .then((data) => {
              this.$message.success("生产成功");
              this.$emit("create", data);
              this.cancel();
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
  watch: {
    visible(value) {
      if (value) {
        this.dataForm = {
          production_order: this.form.id,
          production_quantity: this.form.remain_quantity,
        }
      }
    },
  },
};
</script>

<style scoped></style>
