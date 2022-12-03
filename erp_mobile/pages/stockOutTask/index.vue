<template>
  <view>
    <view style="padding: 0 24rpx;">
      <u--form labelWidth="110">
        <u-form-item label="出库单号:" borderBottom>
          <u--input border="none" :focus="inputFocus1" @focus="inputFocus1 = true" @blur="inputFocus1 = false"
            suffixIcon="scan" selectionStart="0" selectionEnd="999" placeholder="请扫描出库单条形码" @confirm="getStockOutOrder">
          </u--input>
        </u-form-item>
        <u-form-item label="应出数量:" borderBottom>
          <u--input :value="totalQuantity" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="已出数量:" borderBottom>
          <u--input :value="outBoundQuantity" border="none" :disabled="true"></u--input>
        </u-form-item>

        <u-form-item label="产品编号:" borderBottom>
          <u--input border="none" :focus="inputFocus2" @focus="inputFocus2 = true" @blur="inputFocus2 = false"
            suffixIcon="scan" selectionStart="0" selectionEnd="999" placeholder="请扫描产品条形码" @confirm="scanGoods">
          </u--input>
        </u-form-item>
      </u--form>

      <u-cell v-for="(item, index) in stockOutGoodsItems" isLink @click="goGoodsForm(item)">
        <view class="cell-title" slot="title">{{ item.goods_number }}</view>
        <view class="cell-label" slot="label">
          <u-row class="cell-label-row">
            <u-col span="6">产品名称: {{ item.goods_name }}</u-col>
            <u-col span="6">产品条码: {{ item.goods_barcode }}</u-col>
          </u-row>
          <u-row class="cell-label-row">
            <u-col span="6">应收数量: {{ item.remain_quantity }}</u-col>
            <u-col span="6">已收数量: {{ item.stockOutQuantity }}</u-col>
          </u-row>
        </view>
      </u-cell>
    </view>

    <view style="position: absolute; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="确认出库" :disabled="createLoading" :loading="createLoading"
        @click="create">
      </u-button>
    </view>

    <u-toast ref="uToast"></u-toast>
    <u-picker :show="showPicker" :columns="[batchItems]" keyName="batch_number" :closeOnClickOverlay="true"
      @close="showPicker = false" @cancel="showPicker = false" @confirm="selectBatch"></u-picker>

  </view>
</template>

<script>
  import { stockOutTaskList, stockOutRecordCreate } from '@/api/stockOut.js';
  import { mapState, mapMutations } from 'vuex';

  export default {
    data() {
      return {
        stockOutOrderItem: {},
        stockOutGoodsItems: [],
        createLoading: false,
        batchItems: [],
        showPicker: false,
        createLoading: false,
        inputFocus1: true,
        inputFocus2: false,
      }
    },
    computed: {
      ...mapState({
        userItem: (state) => state.system.userItem,
        warehouseItems: (state) => state.system.warehouseItems,
        currentWarehouse: (state) => state.system.currentWarehouse,
      }),
      totalQuantity() {
        let totalQuantity = 0;
        for (let item of this.stockOutGoodsItems) {
          totalQuantity += Number(item.remain_quantity);
        }
        return totalQuantity
      },
      outBoundQuantity() {
        let outBoundQuantity = 0;
        for (let item of this.stockOutGoodsItems) {
          outBoundQuantity += Number(item.stockOutQuantity);
        }
        return outBoundQuantity
      },
    },
    methods: {
      getStockOutOrder(value) {
        let searchForm = {
          search: value,
          page: 1,
          page_size: 6,
          is_completed: false,
          is_void: false
        };

        uni.showLoading({ title: '查询中' });
        stockOutTaskList(searchForm).then((data) => {
          if (data.count == 1) {
            this.stockOutOrderItem = data.results[0];
            let stockOutGoodsItems = [];
            for (let item of this.stockOutOrderItem.stock_out_goods_items) {
              item.stockOutQuantity = 0;
              item.isConfirmed = false;
              item.warehouse = this.stockOutOrderItem.warehouse;
              stockOutGoodsItems.push(item);
            }
            this.stockOutGoodsItems = stockOutGoodsItems;
            this.inputFocus2 = true;
          } else {
            this.$refs.uToast.show({ message: `出库通知单号[${value}]不存在` });
            setTimeout(() => {
              this.inputFocus1 = true;
            }, 500);
          }
        }).finally(() => {
          uni.hideLoading();
        });
      },
      goGoodsForm(stockOutGoodsItem) {
        const updateReceivedGoods = (item) => {
          let index = this.stockOutGoodsItems.findIndex(_item => _item.id == item.id);
          if (index == -1) {
            this.stockOutGoodsItems.splice(0, 0, item);
          } else {
            this.stockOutGoodsItems.splice(index, 1, item);
          }
        }

        uni.navigateTo({
          url: '../stockOutForm/index?item=' + encodeURIComponent(JSON.stringify(stockOutGoodsItem)),
          events: {
            confirm(item) {
              updateReceivedGoods(item);
            },
          },
        });
      },
      scanGoods(value) {
        let batchItems = [];
        for (let item of this.stockOutGoodsItems) {
          if (item.goods_number == value) {
            batchItems.push(item);
          }
        }

        if (batchItems.length == 0) {
          this.$refs.uToast.show({ message: `物料[${value}]不存在` });
          setTimeout(() => {
            this.inputFocus2 = true;
          }, 500);

        } else if (batchItems.length == 1) {
          let batchItem = batchItems[0];
          this.goGoodsForm(batchItem);
        } else {
          this.batchItems = batchItems;
          this.showPicker = true;
        }
      },
      selectBatch(item) {
        this.showPicker = false;
        let batchItem = this.batchItems[item.indexs[0]];
        this.goGoodsForm(batchItem);
      },
      getTime() {
        let date = new Date(),
        year = date.getFullYear(),
        month = date.getMonth() + 1,
        day = date.getDate(),
        hour = date.getHours() < 10 ? "0" + date.getHours() : date.getHours(),
        minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes(),
        second = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
        month >= 1 && month <= 9 ? (month = "0" + month) : "";
        day >= 0 && day <= 9 ? (day = "0" + day) : "";
        let timer = year + '-' + month + '-' + day;
        return timer;
      },
      create() {
        let createForm = {
          stock_out_order: this.stockOutOrderItem.id,
          handler: this.userItem.id,
          handle_time: this.getTime(),
          stock_out_record_goods_items: [],
        };

        for (let item of this.stockOutGoodsItems) {
          if (item.isConfirmed && item.stockOutQuantity > 0) {
            createForm.stock_out_record_goods_items.push({
              stock_out_goods: item.id,
              batch: item.batch,
              stock_out_quantity: item.stockOutQuantity,
            });
          }
        }

        if (createForm.stock_out_record_goods_items.length == 0) {
          this.$refs.uToast.show({ message: '请添加收货物料' });
          return
        }

        uni.showLoading({ title: '创建中' });
        this.createLoading = true;
        stockOutRecordCreate(createForm).then(() => {
          uni.redirectTo({ url: '../stockOutTask/index' });
        }).finally(() => {
          this.createLoading = false;
          uni.hideLoading();
        });
      },
    },
    onShow() {
      if (this.stockOutGoodsItems.length > 0) {
        setTimeout(() => {
          this.inputFocus2 = true;
        }, 500);
      }
    },
  }
</script>

<style>
  .cell-title {
    font-size: 32rpx;
    font-weight: 500;
    margin-bottom: 12rpx;
  }

  .cell-label {
    font-size: 24rpx;
    color: #0005;
  }

  .cell-label-row {
    margin-bottom: 8rpx;
  }
</style>
