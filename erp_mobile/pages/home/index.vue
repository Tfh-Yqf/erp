<template>
  <view style="background-color: #f8f8f8; height: 100vh;">
    <view>
      <u-row style="background-color: #3c9cff; color: #ffffff; height: 72rpx; padding-right: 16rpx;">
        <u-col span="3" @click="showPicker = true" style="text-align: left;  float: left;">
          <u-icon name="arrow-down" :label="currentWarehouseName" labelPos="left" color="#ffffff" labelColor="#ffffff"
            space="6px" style="font-weight: 600; text-align: left; float: left;"></u-icon>
        </u-col>
        <u-col offset="6" span="3" @click="showActionSheet = true">
          <u-icon name="arrow-down" :label="userItem.name" labelPos="left" color="#ffffff" labelColor="#ffffff"
            space="6px" style="font-weight: 600;"></u-icon>
        </u-col>
      </u-row>

      <u-action-sheet :actions="actionList" :show="showActionSheet" :closeOnClickOverlay="true"
        @close="showActionSheet = false" @select="selectAction"></u-action-sheet>
      <u-picker :show="showPicker" :columns="[warehouseItems]" keyName="name" :closeOnClickOverlay="true"
        @close="showPicker = false" @cancel="showPicker = false" @confirm="changeCurrentWarehouse"></u-picker>
    </view>

    <u-row style="background-color: #fff;">
      <u-col span="4">
        <view
          style="color: #666; text-align: center; border-bottom: 1px solid #8888; border-right: 1px solid #8888; padding: 20rpx 0;">
          <view>待入库</view>
          <view style="color: #398ade;">{{ item.stock_in_task_count }}</view>
        </view>
      </u-col>
      <u-col span="4">
        <view style="color: #666; text-align: center; border-bottom: 1px solid #8888; padding: 20rpx 0;">
          <view>待出库</view>
          <view style="color: #53c21d;">{{ item.stock_out_task_count }}</view>
        </view>
      </u-col>
      <u-col span="4">
        <view
          style="color: #666; text-align: center; border-bottom: 1px solid #8888; border-left: 1px solid #8888;padding: 20rpx 0;">
          <view>临期预警</view>
          <view style="color: #e45656;">{{ item.expiration_warning_count }}</view>
        </view>
      </u-col>
    </u-row>

    <u-grid :border="false" @click="onClickGrid">
      <u-grid-item v-for="(item, index) in funcList" :key="index"
        style="padding: 36rpx 0; border-right:1px solid #8888; border-bottom: 1px solid #8888;">
        <image :src="item.image" style="width: 100rpx; height: 100rpx" />
        <view style="margin-top: 16rpx;">
          <text style="font-size: 28rpx;">{{item.title}}</text>
        </view>
      </u-grid-item>
    </u-grid>
  </view>
</template>

<script>
  import { getInfo, homeOverview } from 'api/system.js';
  import { warehouseOption } from 'api/option.js';
  import { mapState, mapMutations } from 'vuex';

  export default {
    data() {
      return {
        funcList: [
          {
            title: '产品管理',
            path: '/pages/productList/index',
            image: '../../static/product.png',
          },
          {
            title: '批次报表',
            path: '/pages/batchReport/index',
            image: '../../static/func6.png',
          },
          {
            title: '入库',
            path: '/pages/stockInTask/index',
            image: '../../static/func1.png',
          },
          {
            title: '出库',
            path: '/pages/stockOutTask/index',
            image: '../../static/func8.png',
          },
          {
            title: '盘点',
            path: '/pages/stockCheckForm/index',
            image: '../../static/func9.png',
          },
        ],
        showActionSheet: false,
        showPicker: false,
        actionList: [
          { code: 'logout', name: '退出登录' }
        ],
        item: {},
      }
    },
    computed: {
      ...mapState({
        userItem: (state) => state.system.userItem,
        warehouseItems: (state) => state.system.warehouseItems,
        currentWarehouse: (state) => state.system.currentWarehouse,
      }),
      currentWarehouseName() {
        for (let item of this.warehouseItems) {
          if (item.id == this.currentWarehouse) {
            return item.name;
          }
        }
        return '所有仓库';
      },
    },
    methods: {
      ...mapMutations(['setUserItem', 'setWarehouseItems', 'setCurrentWarehouse']),
      initData() {
        getInfo().then((data) => {
          console.log(data)
          this.setUserItem(data);
        });

        warehouseOption().then((data) => {
          let warehouseItems = [{ id: undefined, name: '所有仓库' }, ...data.results];
          this.setWarehouseItems(warehouseItems);
          if (!this.currentWarehouse) {
            this.setCurrentWarehouse(warehouseItems[0].id);
          }
        });

        homeOverview().then((data) => {
          this.item = data;
        });
      },
      onClickGrid(index) {
        uni.navigateTo({ url: this.funcList[index].path });
      },
      changeCurrentWarehouse(item) {
        this.showPicker = false;
        this.setCurrentWarehouse(this.warehouseItems[item.indexs[0]].id);
      },
      selectAction(item) {
        this.showActionSheet = false;

        if (item.code == 'logout') {
          uni.removeStorageSync('access');
          uni.removeStorageSync('refresh');
          uni.redirectTo({ url: '../login/index' });
        }
      },
    },
    onShow() {
      this.initData();
    },
  }
</script>

<style>

</style>
