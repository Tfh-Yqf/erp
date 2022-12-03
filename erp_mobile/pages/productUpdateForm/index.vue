<template>
  <view>
    <view style="padding: 0 24rpx; margin-bottom: 100rpx;">
      <u--form labelWidth="100">
        <u-form-item label="编号:" required borderBottom>
          <u--input v-model="dataForm.number" border="none" />
        </u-form-item>
        <u-form-item label="名称:" required borderBottom>
          <u--input v-model="dataForm.name" border="none" />
        </u-form-item>
        <u-form-item label="条码:" borderBottom>
          <u--input v-model="dataForm.barcode" border="none" />
        </u-form-item>
        </u-form-item>
        <u-form-item label="分类:" borderBottom @click="showCategoryPicker = true">
          <u--input :value="dataForm.category_name" disabled disabledColor="#ffffff" border="none" />
        </u-form-item>
        <u-form-item label="单位:" borderBottom @click="showUnitPicker = true">
          <u--input :value="dataForm.unit_name" disabled disabledColor="#ffffff" border="none" />
        </u-form-item>
        <u-form-item label="规格:" borderBottom>
          <u--input v-model="dataForm.spec" border="none" />
        </u-form-item>

        <u-form-item label="采购价:" borderBottom>
          <u--input v-model="dataForm.purchase_price" type="number" border="none" />
        </u-form-item>
        <u-form-item label="零售价:" borderBottom>
          <u--input v-model="dataForm.retail_price" type="number" border="none" />
        </u-form-item>
        <u-form-item label="等级价一:" borderBottom>
          <u--input v-model="dataForm.level_price1" type="number" border="none" />
        </u-form-item>
        <u-form-item label="等级价二:" borderBottom>
          <u--input v-model="dataForm.level_price2" type="number" border="none" />
        </u-form-item>
        <u-form-item label="等级价三:" borderBottom>
          <u--input v-model="dataForm.level_price3" type="number" border="none" />
        </u-form-item>

        <u-form-item label="启用批次控制:" borderBottom>
          <u-switch v-model="dataForm.enable_batch_control" />
        </u-form-item>
        <u-form-item v-if="dataForm.enable_batch_control" label="保质期(天):" borderBottom>
          <u--input v-model="dataForm.shelf_life_days" border="none" />
        </u-form-item>
        <u-form-item v-if="dataForm.enable_batch_control" label="预警天数:" borderBottom>
          <u--input v-model="dataForm.shelf_life_warning_days" border="none" />
        </u-form-item>
        <u-form-item label="库存预警:" borderBottom>
          <u-switch v-model="dataForm.enable_inventory_warning" />
        </u-form-item>
        <u-form-item v-if="dataForm.enable_inventory_warning" label="库存上限:" borderBottom>
          <u--input v-model="dataForm.inventory_upper" border="none" />
        </u-form-item>
        <u-form-item v-if="dataForm.enable_inventory_warning" label="库存下限:" borderBottom>
          <u--input v-model="dataForm.inventory_lower" border="none" />
        </u-form-item>
        <u-form-item label="状态:" borderBottom>
          <u-switch v-model="dataForm.is_active" />
        </u-form-item>
        <u-form-item label="备注:" borderBottom>
          <u--input v-model="dataForm.remark" border="none" />
        </u-form-item>
      </u--form>
    </view>

    <view style="position: fixed; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="保存" @click="update"></u-button>
    </view>

    <u-toast ref="uToast"></u-toast>
    <u-picker :show="showCategoryPicker" :columns="[categoryItems]" keyName="name" :closeOnClickOverlay="true"
      @close="showCategoryPicker = false" @cancel="showCategoryPicker = false" @confirm="changeCategory" />
    <u-picker :show="showUnitPicker" :columns="[unitItems]" keyName="name" :closeOnClickOverlay="true"
      @close="showUnitPicker = false" @cancel="showUnitPicker = false" @confirm="changeUnit" />
  </view>
</template>

<script>
  import { productUpdate } from '@/api/product.js';
  import { categoryOption, unitOption } from '@/api/option.js';

  export default {
    data() {
      return {
        dataForm: {
          number: '',
          name: '',
          barcode: '',
          unit: null,
          unit_name: '',
          category: null,
          category_name: '',
          spec: '',

          length: null,
          width: null,
          height: null,
          volume: null,
          weight: null,
          spec: '',
          unit: '',
          enable_shelf_life: false,
          shelf_life_days: null,
          shelf_life_warning_days: 0,
          enable_inventory_warning: false,
          inventory_upper: null,
          inventory_lower: null,
          is_active: true,
          remark: '',
        },
        showUnitPicker: false,
        showCategoryPicker: false,
        unitItems: [],
        categoryItems: [],
      }
    },
    methods: {
      update() {
        if (!this.dataForm.number) {
          this.$refs.uToast.show({ message: '请填写编号' });
          return
        }

        if (!this.dataForm.name) {
          this.$refs.uToast.show({ message: '请填写名称' });
          return
        }

        productUpdate(this.dataForm).then((data) => {
          uni.showToast({ title: '保存成功', duration: 2000 });
          uni.navigateBack();
          this.eventChannel.emit('onUpdate', data);
        });
      },
      changeUnit(item) {
        this.showUnitPicker = false;
        this.dataForm.unit = this.unitItems[item.indexs[0]].id;
        this.dataForm.unit_name = this.unitItems[item.indexs[0]].name;
      },
      changeCategory(item) {
        this.showCategoryPicker = false;
        this.dataForm.category = this.categoryItems[item.indexs[0]].id;
        this.dataForm.category_name = this.categoryItems[item.indexs[0]].name;
      },
    },
    onShow() {
      unitOption({ page: 1, page_size: 999999 }).then((data) => {
        this.unitItems = data.results;
      });

      categoryOption({ page: 1, page_size: 999999 }).then((data) => {
        this.categoryItems = data.results;
      });
    },
    onLoad(option) {
      this.eventChannel = this.getOpenerEventChannel();
      this.dataForm = { ...JSON.parse(decodeURIComponent(option.item)) };
    },
  }
</script>

<style scoped>

</style>
