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
          <u--input :value="stockOutGoodsItem.goods_name" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item v-if="stockOutGoodsItem.enable_batch_control" label="批次编号:" borderBottom
          @click="showPicker = true;">
          <u--input :value="stockOutGoodsItem.batch_number" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="剩余数量:" borderBottom>
          <u--input :value="stockOutGoodsItem.remain_quantity" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="出库数量:" borderBottom>
          <u--input v-model="stockOutGoodsItem.stockOutQuantity" border="none"></u--input>
        </u-form-item>
      </u--form>
    </view>

    <view style="position: absolute; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="确定" @click="confirm"></u-button>
    </view>

    <u-picker :show="showPicker" :columns="[batchItems]" keyName="number" :closeOnClickOverlay="true"
      @close="showPicker = false" @cancel="showPicker = false" @confirm="selectPicker"></u-picker>

    <u-toast ref="uToast"></u-toast>
  </view>
</template>

<script>
  import { batchOption } from '@/api/option.js';

  export default {
    data() {
      return {
        eventChannel: null,
        stockOutGoodsItem: {},
        showDatePicker: false,
        showPicker: false,
        inputFocus1: true,
        batchItems: []
      }
    },
    methods: {
      validateGoods(value) {
        if (this.stockOutGoodsItem.goods_number == value) {
          this.stockOutGoodsItem.stockOutQuantity += 1;
          this.$refs.uToast.show({ message: '扫码成功' });
        } else {
          this.$refs.uToast.show({ message: '产品错误' });
        }

        setTimeout(() => {
          this.inputFocus1 = true;
        }, 500);
      },
      confirm() {
        if (this.stockOutGoodsItem.enable_batch_control && !this.stockOutGoodsItem.batch) {
          this.$refs.uToast.show({ message: '请选择批次' });
          return;
        }

        this.stockOutGoodsItem.isConfirmed = true;
        this.eventChannel.emit('confirm', this.stockOutGoodsItem);
        uni.navigateBack();
      },
      selectPicker(item) {
        let index = item.indexs[0];
        let batchItem = this.batchItems[index];
        this.stockOutGoodsItem.batch = batchItem.id;
        this.stockOutGoodsItem.batch_number = `${batchItem.number} | 库存: ${batchItem.remain_quantity}`;
        this.showPicker = false;
      },
      getBatch() {
        let searchForm = {
          page: 1,
          page_size: 999999,
          has_stock: true,
          warehouse: this.stockOutGoodsItem.warehouse,
          goods: this.stockOutGoodsItem.goods,
        };

        batchOption(searchForm).then((data) => {
          this.batchItems = data.results;
          console.log('---------', this.batchItems)
        });
      },
    },
    onLoad(option) {
      this.eventChannel = this.getOpenerEventChannel();
      this.stockOutGoodsItem = JSON.parse(decodeURIComponent(option.item));
      if (this.stockOutGoodsItem.enable_batch_control) {
        this.getBatch();
      }
    },
  }
</script>


<style scoped>

</style>
