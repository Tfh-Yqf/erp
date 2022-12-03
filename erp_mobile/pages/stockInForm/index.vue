<template>
  <view>
    <view style="padding: 0 24rpx;">
      <u--form labelWidth="75">
        <u-form-item label="产品编号:" borderBottom>
          <u--input border="none" :focus="inputFocus1" @focus="inputFocus1 = true" @blur="inputFocus1 = false"
            suffixIcon="scan" selectionStart="0" selectionEnd="999" placeholder="请扫描产品条形码" @confirm="validateGoods">
          </u--input>
        </u-form-item>
        <u-form-item label="产品名称:" borderBottom>
          <u--input :value="stockInGoodsItem.goods_name" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item v-if="stockInGoodsItem.enable_batch_control" label="批次编号:" borderBottom
          @click="showPicker = true;">
          <u--input :value="stockInGoodsItem.batch_number" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="剩余数量:" borderBottom>
          <u--input :value="stockInGoodsItem.remain_quantity" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="出库数量:" borderBottom>
          <u--input v-model="stockInGoodsItem.stockInQuantity" border="none"></u--input>
        </u-form-item>
        <u-form-item v-if="stockInGoodsItem.enable_batch_control" label="批次编号:" borderBottom>
          <u--input :value="stockInGoodsItem.batch_number" border="none"></u--input>
        </u-form-item>
        <u-form-item v-if="stockInGoodsItem.enable_batch_control" label="生产日期:" borderBottom
          @click="showDatePicker = true">
          <u--input :value="stockInGoodsItem.production_date" border="none" :disabled="true"></u--input>
        </u-form-item>
      </u--form>
    </view>

    <view style="position: absolute; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="确定" @click="confirm"></u-button>
    </view>

    <u-datetime-picker :show="showDatePicker" mode="date" :closeOnClickOverlay="true" @close="showDatePicker = false"
      @cancel="showDatePicker = false" @confirm="selectDatePicker">
    </u-datetime-picker>

    <u-toast ref="uToast"></u-toast>
  </view>
</template>

<script>
  import { batchOption } from '@/api/option.js';

  export default {
    data() {
      return {
        eventChannel: null,
        stockInGoodsItem: {},
        showDatePicker: false,
        showPicker: false,
        inputFocus1: true,
        batchItems: []
      }
    },
    methods: {
      validateGoods(value) {
        if (this.stockInGoodsItem.goods_number == value) {
          this.stockInGoodsItem.stockInQuantity += 1;
          this.$refs.uToast.show({ message: '扫码成功' });
        } else {
          this.$refs.uToast.show({ message: '产品错误' });
        }

        setTimeout(() => {
          this.inputFocus1 = true;
        }, 500);
      },
      confirm() {
        if (this.stockInGoodsItem.enable_batch_control && !this.stockInGoodsItem.batch_number &&
          this.stockInGoodsItem.batch_number.length == 0) {
          this.$refs.uToast.show({ message: '请输入批次' });
          return;
        }

        this.stockInGoodsItem.isConfirmed = true;
        this.eventChannel.emit('confirm', this.stockInGoodsItem);
        uni.navigateBack();
      },
      selectDatePicker(item) {
        this.stockInGoodsItem.production_date = this.formatDate(item.value);
        this.showDatePicker = false;
      },
      formatDate(datetime) {
        let date = new Date(datetime);
        let year = date.getFullYear(),
          month = ("0" + (date.getMonth() + 1)).slice(-2),
          sdate = ("0" + date.getDate()).slice(-2);
        return year + "-" + month + "-" + sdate;
      },
    },
    onLoad(option) {
      this.eventChannel = this.getOpenerEventChannel();
      this.stockInGoodsItem = JSON.parse(decodeURIComponent(option.item));
      if (this.stockInGoodsItem.enable_batch_control) {
        this.getBatch();
      }
    },
  }
</script>


<style scoped>

</style>
