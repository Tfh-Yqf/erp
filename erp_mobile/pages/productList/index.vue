<template>
  <view style="margin-bottom: 100rpx;">
    <view style="padding: 12rpx;">
      <u-search placeholder="请扫描物料条码" :focus="true" searchIcon="scan" v-model="searchForm.search" shape="square"
        :clearabled="true" :show-action="false" @search="searchData">
      </u-search>
    </view>

    <view>
      <u-cell v-for="(item, index) in dataItems" :key="index">
        <view class="cell-title" slot="title">{{ item.name }}</view>
        <view class="cell-label" slot="label">
          <u-row class="cell-label-row">
            <u-col span="6">编号: {{ item.number }}</u-col>
            <u-col span="6">分类: {{ item.category_name }}</u-col>
          </u-row>
          <u-row class="cell-label-row">
            <u-col span="6">规格: {{ item.spec }}</u-col>
            <u-col span="6">备注: {{ item.remark }}</u-col>
          </u-row>

          <u-row gutter="16" style="margin-top: 24rpx;">
            <u-col span="4">
              <u-button type="primary" text="编辑" @click="toUpdateForm(item)"></u-button>
            </u-col>
            <u-col span="4">
              <u-button type="error" text="删除" @click="openDestroyModal(item)"></u-button>
            </u-col>
            <u-col span="4">
              <u-button type="success" text="打印" @click="openPrintModal(item)"></u-button>
            </u-col>
          </u-row>
        </view>
      </u-cell>
    </view>

    <view style="position: fixed; bottom: 0; width: 100%;">
      <u-button type="primary" size="large" text="新增物料" @click="toCreateForm">
      </u-button>
    </view>

    <view style="padding: 12rpx 0;">
      <u-loadmore :status="loadMoreStatus" loading-text="正在加载中" loadmore-text="加载更多" nomore-text="没有更多了"
        @loadmore="loadMoreData" />
    </view>

    <u-modal :show="showDestroyModal" title="确定删除吗?" :showCancelButton="true" @cancel="showDestroyModal = false"
      @confirm="destroy" />
    <print-material-modal :show="showPrintModal" :number="printItem.number" :name="printItem.name"
      @cancel="showPrintModal = false" />
  </view>
</template>

<script>
  import PrintMaterialModal from '@/components/PrintMaterialModal/index';
  import { productList, productDestroy } from '@/api/product.js';
  import { mapState } from 'vuex';

  export default {
    components: {
      PrintMaterialModal,
    },
    data() {
      return {
        searchForm: { page: 1, page_size: 8 },
        dataLoading: false,
        dataItems: [],
        dataCount: 0,

        showPrintModal: false,
        printItem: {},

        showDestroyModal: false,
        destroyItem: {},
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
        this.searchForm.page = 1;
        this.list();
      },
      list() {
        if (this.searchForm.page == 1) {
          uni.showLoading({ title: '加载中' });
        }

        this.dataLoading = true;
        productList(this.searchForm).then((data) => {
          this.dataCount = data.count;
          if (this.searchForm.page == 1) {
            this.dataItems = data.results;
          } else {
            this.dataItems = this.dataItems.concat(data.results);
          }
        }).finally(() => {
          uni.stopPullDownRefresh();
          uni.hideLoading();
          this.dataLoading = false;
        });
      },
      destroy() {
        productDestroy({ id: this.destroyItem.id }).then(() => {
          this.dataItems.splice(this.dataItems.findIndex(item => item.id == this.destroyItem.id), 1);
          uni.showToast({ title: '删除成功', duration: 2000 });
          this.showDestroyModal = false;
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
      openDestroyModal(item) {
        this.destroyItem = { ...item };
        this.showDestroyModal = true;
      },
      openPrintModal(item) {
        this.printItem = item;
        this.showPrintModal = true;
      },
      toCreateForm() {
        uni.navigateTo({
          url: '../productCreateForm/index',
          events: {
            onCreate(item) {
              this.dataItems.splice(0, 0, item);
            },
          },
        });
      },
      toUpdateForm(item) {
        uni.navigateTo({
          url: '../productUpdateForm/index?item=' + encodeURIComponent(JSON.stringify(item)),
          events: {
            onUpdate(item) {
              let index = this.dataItems.findIndex((dataItem) => dataItem.id === item.id);
              if (index !== -1) {
                this.dataItems.splice(index, 1, item);
              }
            },
          },
        });
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
