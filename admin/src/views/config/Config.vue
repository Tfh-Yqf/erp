<template>
  <div>
    <a-card title="配置管理">
      <a-spin :spinning="loading">
        <a-descriptions bordered>
          <a-descriptions-item label="激活入库" :span="3">
            <a-switch v-model="form.enable_auto_stock_in" @change="update" />
            <Helper :message="'激活后无需到库存管理页面手动确认入库。'" style="margin-left:20px;"></Helper>
          </a-descriptions-item>
          <a-descriptions-item label="激活出库" :span="3">
            <a-switch v-model="form.enable_auto_stock_out" @change="update" />
             <Helper :message="'激活后无需到库存管理页面手动确认出库。'" style="margin-left:20px;"></Helper>
          </a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </a-card>
  </div>
</template>

<script>
  import { configInfo, configUpdate } from '@/api/system'

  export default {
    name: 'Config',
    components:{
       Helper: () => import("@/components/Helper/Helper"),
    },
    data() {
      return {
        loading: false,
        form: {},
      };
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        configInfo().then(resp => {
          this.form = resp;
        }).catch(err => {
          this.$message.error(err.response.data.error);
        }).finally(() => {
          this.loading = false;
        });
      },
      update() {
        this.loading = true;
        configUpdate(this.form).then(resp => {
          this.form = resp;
          this.$message.success('保存成功');
        }).finally(() => {
          this.loading = false;
        });
      }
    },
    mounted() {
      this.initialize();
    },
  }
</script>

<style scoped>
</style>