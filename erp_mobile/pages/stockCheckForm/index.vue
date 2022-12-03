<template>
  <view>
    <view style="padding: 0 24rpx; margin-bottom: 100rpx;">
      <u--form labelWidth="75">
        <u-form-item label="盘点单号:" borderBottom>
          <u--input v-model="form.number" border="none"></u--input>
        </u-form-item>
        <u-form-item label="仓库:" borderBottom @click="showWarehousePicker = true">
          <u--input :value="form.warehouse_name" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="经手人:" borderBottom @click="showUserPicker = true">
          <u--input :value="form.handler_name" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="处理日期:" borderBottom @click="showDatePicker = true">
          <u--input :value="form.handle_time" border="none" :disabled="true"></u--input>
        </u-form-item>
        <u-form-item label="备注:" borderBottom>
          <u--input v-model="form.remark" border="none"></u--input>
        </u-form-item>
        <u-form-item label="产品编号:" borderBottom>
          <u--input border="none" :focus="inputFocus1" @focus="inputFocus1 = true" @blur="inputFocus1 = false"
            suffixIcon="scan" selectionStart="0" selectionEnd="999" placeholder="请扫描产品条形码" @confirm="scanGoods">
          </u--input>
        </u-form-item>
      </u--form>

      <u-cell v-for="(item, index) in stockCheckGoodsItems">
        <view class="cell-title" slot="title">{{ item.goods_number }}</view>
        <view class="cell-label" slot="label">
          <u-row class="cell-label-row">
            <u-col span="6">产品名称: {{ item.goods_name }}</u-col>
            <u-col span="6">产品条码: {{ item.goods_barcode }}</u-col>
          </u-row>

          <view v-if="item.enable_batch_control">
            <view v-for="_item in item.stock_check_batch_items" style="border: 1px solid #999; margin-top: 8rpx;">
              <u-row class="cell-label-row">
                <u-col span="6">批次编号: {{ _item.batch_number }}</u-col>
              </u-row>
              <u-row class="cell-label-row">
                <u-col span="6">账面数量: {{ _item.book_quantity }}</u-col>
                <u-col span="6">实际数量: {{ _item.actual_quantity }}</u-col>
              </u-row>
            </view>
          </view>
          <view v-else>
            <u-row class="cell-label-row">
              <u-col span="6">账面数量: {{ item.book_quantity }}</u-col>
              <u-col span="6">实际数量: {{ item.actual_quantity }}</u-col>
            </u-row>
          </view>
        </view>
      </u-cell>
    </view>

    <view style="position: fixed; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="确认盘点" :disabled="createLoading" :loading="createLoading"
        @click="create">
      </u-button>
    </view>

    <u-datetime-picker :show="showDatePicker" mode="date" :closeOnClickOverlay="true" @close="showDatePicker = false"
      @cancel="showDatePicker = false" @confirm="selectDatePicker">
    </u-datetime-picker>
    <u-picker :show="showWarehousePicker" :columns="[warehouseItems]" keyName="name" :closeOnClickOverlay="true"
      @close="showWarehousePicker = false" @cancel="showWarehousePicker = false" @confirm="selectWarehouse"></u-picker>
    <u-picker :show="showUserPicker" :columns="[userItems]" keyName="name" :closeOnClickOverlay="true"
      @close="showUserPicker = false" @cancel="showUserPicker = false" @confirm="selectUser"></u-picker>
    <u-picker :show="showBatchPicker" :columns="[batchItems]" keyName="number" :closeOnClickOverlay="true"
      @close="showBatchPicker = false" @cancel="showBatchPicker = false" @confirm="selectBatch"></u-picker>

    <u-toast ref="uToast"></u-toast>
  </view>
</template>

<script>
  import { userOption, warehouseOption, batchOption, inventoryOption } from '@/api/option.js';
  import { stockCheckNumber, stockCheckCreate } from '@/api/stockCheck.js';

  export default {
    data() {
      return {
        eventChannel: null,
        showWarehousePicker: false,
        showUserPicker: false,
        showDatePicker: false,
        showBatchPicker: false,
        inputFocus1: false,

        warehouseItems: [],
        userItems: [],
        form: {},
        stockCheckGoodsItems: [],
        batchItems: [],
        goodsItem: {},
        createLoading: false,
      }
    },
    methods: {
      initData() {
        warehouseOption({ page_size: 999999, is_active: true }).then(data => {
          this.warehouseItems = data.results;
        });
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.userItems = data.results;
        });
        stockCheckNumber().then(data => {
          this.form.number = data.number;
        });
      },
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
      selectWarehouse(item) {
        let index = item.indexs[0];
        let warehouseItem = this.warehouseItems[index];
        this.form.warehouse = warehouseItem.id;
        this.form.warehouse_name = warehouseItem.name;
        this.showWarehousePicker = false;
      },
      selectUser(item) {
        let index = item.indexs[0];
        let userItem = this.userItems[index];
        this.form.handler = userItem.id;
        this.form.handler_name = userItem.name;
        this.showUserPicker = false;
      },
      selectDatePicker(item) {
        this.form.handle_time = this.formatDate(item.value);
        this.showDatePicker = false;
      },
      scanGoods(value) {
        if (!this.form.warehouse) {
          this.$refs.uToast.show({ message: `请选择仓库` });
          return;
        }

        for (let stockCheckGoodsItem of this.stockCheckGoodsItems) {
          if (value == stockCheckGoodsItem.goods_number) {
            if (stockCheckGoodsItem.enable_batch_control) {
              this.batchItems = stockCheckGoodsItem.batchItems;
              if (this.batchItems.length == 1) {
                let stockCheckBatchItem = stockCheckGoodsItem.stock_check_batch_items[0];
                stockCheckBatchItem.actual_quantity += 1;
                stockCheckGoodsItem.actual_quantity += 1;
              } else {
                this.showBatchPicker = true;
                return;
              }
            } else {
              stockCheckGoodsItem.actual_quantity += 1;
            }

            setTimeout(() => {
              this.inputFocus1 = true;
            }, 500);
            return;
          }
        }

        let searchForm = {
          goods_number: value,
          page: 1,
          page_size: 6,
          is_active: true,
          warehouse: this.form.warehouse,
        };

        inventoryOption(searchForm).then((data) => {
          if (data.results.length == 1) {
            let goodsItem = data.results[0];
            this.goodsItem = goodsItem;
            if (goodsItem.enable_batch_control) {
              this.getBatch(goodsItem);
              return;
            } else {
              this.stockCheckGoodsItems.push({
                goods: goodsItem.goods,
                goods_number: goodsItem.goods_number,
                goods_name: goodsItem.goods_name,
                goods_barcode: goodsItem.goods_barcode,
                enable_batch_control: goodsItem.enable_batch_control,
                book_quantity: goodsItem.total_quantity,
                actual_quantity: 1,
                stock_check_batch_items: [],
              });
              setTimeout(() => {
                this.inputFocus1 = true;
              }, 500);
            }
          } else {
            this.$refs.uToast.show({ message: `产品不存在或库存为零` });
          }
        });
      },
      getBatch(goodsItem) {
        let searchForm = {
          page: 1,
          page_size: 999999,
          has_stock: true,
          warehouse: this.form.warehouse,
          goods: goodsItem.goods,
        };

        batchOption(searchForm).then((data) => {
          this.batchItems = data.results;
          if (this.batchItems.length == 0) {
            this.$refs.uToast.show({ message: `产品不存在或库存为零` });
          } else {
            if (this.batchItems.length == 1) {
              let batchItem = this.batchItems[0];
              this.stockCheckGoodsItems.push({
                goods: goodsItem.goods,
                goods_number: goodsItem.goods_number,
                goods_name: goodsItem.goods_name,
                goods_barcode: goodsItem.goods_barcode,
                enable_batch_control: goodsItem.enable_batch_control,
                book_quantity: goodsItem.total_quantity,
                actual_quantity: 1,
                stock_check_batch_items: [{
                  id: batchItem.id,
                  batch_number: batchItem.number,
                  book_quantity: batchItem.remain_quantity,
                  actual_quantity: 1,
                }],
                batchItems: [...this.batchItems],
              });
            } else {
              this.showBatchPicker = true;
            }
          }
        });
      },
      selectBatch(item) {
        this.showBatchPicker = false;
        let batchItem = this.batchItems[item.indexs[0]];
        let index = this.stockCheckGoodsItems.findIndex((item) => item.goods == batchItem.goods);
        if (index == -1) {
          this.stockCheckGoodsItems.push({
            goods: this.goodsItem.goods,
            goods_number: this.goodsItem.goods_number,
            goods_name: this.goodsItem.goods_name,
            goods_barcode: this.goodsItem.goods_barcode,
            enable_batch_control: this.goodsItem.enable_batch_control,
            book_quantity: this.goodsItem.total_quantity,
            actual_quantity: 1,
            stock_check_batch_items: [{
              id: batchItem.id,
              batch_number: batchItem.number,
              book_quantity: batchItem.remain_quantity,
              actual_quantity: 1,
            }],
            batchItems: [...this.batchItems],
          });
        } else {
          let goodsItem = this.stockCheckGoodsItems[index];
          goodsItem.actual_quantity += 1;
          let batchIndex = goodsItem.stock_check_batch_items.findIndex((item) => item.id == batchItem.id);
          if (batchIndex == -1) {
            goodsItem.stock_check_batch_items.push({
              id: batchItem.id,
              batch_number: batchItem.number,
              book_quantity: batchItem.remain_quantity,
              actual_quantity: 1,
            });
          } else {
            let stockCheckBatchItem = goodsItem.stock_check_batch_items[batchIndex];
          }
        }

        setTimeout(() => {
          this.inputFocus1 = true;
        }, 500);
      },
      formatDate(datetime) {
        let date = new Date(datetime);
        let year = date.getFullYear(),
          month = ("0" + (date.getMonth() + 1)).slice(-2),
          sdate = ("0" + date.getDate()).slice(-2);
        return year + "-" + month + "-" + sdate;
      },
      create() {
        if (!this.form.handler) {
          this.$refs.uToast.show({ message: '请选择经手人' });
          return
        }
        
        if (!this.form.handle_time) {
          this.$refs.uToast.show({ message: '请选择处理日期' });
          return
        }

        if (this.stockCheckGoodsItems.length == 0) {
          this.$refs.uToast.show({ message: '请盘点物料' });
          return
        }

        let createForm = {
          ...this.form,
          stock_check_goods_Items: this.stockCheckGoodsItems,
        };
        
        console.log('===', createForm)

        uni.showLoading({ title: '创建中' });
        this.createLoading = true;
        stockCheckCreate(createForm).then(() => {
          uni.redirectTo({ url: '../stockCheckForm/index' });
        }).finally(() => {
          this.createLoading = false;
          uni.hideLoading();
        });
      },
    },
    mounted() {
      this.form = {};
      this.initData();
    }
  }
</script>


<style scoped>

</style>
