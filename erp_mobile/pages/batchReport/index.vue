<template>
  <view>
    <view style="padding: 12rpx;">
      <u-search placeholder="请扫描商品条码" :focus="true" searchIcon="scan" v-model="searchForm.search" shape="square"
        :clearabled="true" :show-action="false" @search="searchData">
      </u-search>
    </view>

    <view>
      <u-cell v-for="(item, index) in dataItems" :key="index">
        <view class="cell-title" slot="title">{{ item.goods_number }}</view>
        <view class="cell-label" slot="label">
          <u-row class="cell-label-row">
            <u-col span="6">商品名称: {{ item.goods_name }}</u-col>
            <u-col span="6">批次: {{ item.number }}</u-col>
          </u-row>
          <u-row class="cell-label-row">
            <u-col span="6">仓库: {{ item.warehouse_name }}</u-col>
            <u-col span="6">数量: {{ item.remain_quantity }}</u-col>
          </u-row>
        </view>
      </u-cell>
    </view>

    <view style="padding: 12rpx 0;">
      <u-loadmore :status="loadMoreStatus" loading-text="正在加载中" loadmore-text="加载更多" nomore-text="没有更多了"
        @loadmore="loadMoreData" />
    </view>
  </view>
</template>

<script>
  import { batchReportList } from '@/api/report.js';
  import { mapState } from 'vuex';

  export default {
    data() {
      return {
        searchForm: { page: 1, page_size: 6, has_stock: true },
        dataLoading: false,
        dataItems: [],
        dataCount: 0,
      }
    },
    computed: {
      ...mapState({
        currentWarehouse: (state) => state.system.currentWarehouse,
      }),
      loadMoreStatus() {
        if (this.dataLoading) {
          return 'loading';
        }

        if (this.dataItems.length == this.dataCount) {
          return 'nomore';
        }

        return 'loadmore';
      },
    },
    methods: {
      initData() {
        this.searchForm.warehouse = this.currentWarehouse;
        this.searchForm.page = 1;
        this.list();
      },
      list() {
        if (this.searchForm.page == 1) {
          uni.showLoading({ title: '加载中' });
        }

        this.dataLoading = true;
        batchReportList(this.searchForm).then((data) => {
          console.log('-----------------------BatchReportStart-----------------------')
          this.dataCount = data.count;
          if (this.searchForm.page == 1) {
            this.dataItems = data.results;
          } else {
            this.dataItems = this.dataItems.concat(data.results);
          }
        }).finally(() => {
          console.log('-----------------------BatchReportEnd-----------------------')
          uni.stopPullDownRefresh();
          uni.hideLoading();
          this.dataLoading = false;
        });
      },
      loadMoreData() {
        if (this.dataItems.length < this.dataCount) {
          this.searchForm.page += 1;
          this.list();
        }
      },
      searchData() {
        this.searchForm.page = 1;
        this.list();
      },
    },
    onShow() {
      this.initData();
    },
    onPullDownRefresh() {
      this.searchData();
    },
  }
</script>

<style scoped>
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
