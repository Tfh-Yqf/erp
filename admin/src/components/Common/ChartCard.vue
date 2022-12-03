<template>
  <a-card :loading="loading" :body-style="{ padding: '0px 0px 8px' }" :bordered="false">
    <div class="chart-card-header">
      <div class="meta" :style="{background: bgr}">
        <a-icon :style="{color: color,marginRight: '8px'}" :type="icon" />
        <span class="chart-card-title" :style="{color: color}">{{ title }}</span>
      </div>
      <div v-show="type !== 2" class="task">
        <a-row :gutter="24">
          <a-col v-if="type == 0" :span="24">
            <span class="number">{{ finished }}</span>
            <span class="intro">今日已完成</span>
          </a-col>
          <a-col v-if="type == 0" :span="24">
            <span class="number" style="color: #FFC107;">{{ total }}</span>
            <span class="intro">待入库</span>
          </a-col>
          <a-col v-if="type == 1" :span="24">
            <span class="number" style="color: #FFC107;">{{ occupy }}</span>
            <span class="intro">占用</span>
          </a-col>
          <a-col v-if="type == 1" :span="24">
            <span class="percent">{{ percent }}</span>
            <span>
              <mini-progress color="rgb(19, 194, 194)" :percentage="percent" :height="8" />
            </span>
          </a-col>
        </a-row>
      </div>
      <div class="chart-card-content">
        <div class="content-fix">
          <slot></slot>
        </div>
      </div>
    </div>
  </a-card>
</template>

<script>
import MiniProgress from './MiniProgress'

  export default {
    name: "ChartCard",
    props: {
      type: {
        type: String,
        default: '0'
      },
      icon: {
        type: String,
        default: ''
      },
      title: {
        type: String,
        default: ''
      },
      finished: {
        type: String,
        default: ''
      },
      total: {
        type: String,
        default: ''
      },
      bgr: {
        type: String,
        default: 'rgba(253, 236, 234, 1)'
      },
      color: {
        type: String,
        default: 'rgba(25, 23, 23, 1)'
      },
      occupy: {
        type: String,
        default: ''
      },
      percent: {
        type: Number,
        default: 0
      },
      loading: {
        type: Boolean,
        default: false
      }
    },
    components: {
      MiniProgress
    },
  }
</script>

<style lang="less" scoped>
  .chart-card-header {
    position: relative;
    overflow: hidden;
    width: 100%;
    .meta {
      position: relative;
      overflow: hidden;
      width: 100%;
      color: rgba(0, 0, 0, .45);
      font-size: 14px;
      line-height: 22px;
      padding: 6px;
    }
  }
  .task{
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-all;
    white-space: nowrap;
    color: #000;
    margin-top: 8px;
    margin-bottom: 8px;
    // height: 68px;
    span{
      text-align: center;
      display: block;
    }
    .number{
      font-size: 30px;
      font-weight: bold;
    }
    .intro{
      font-size: 14px;
      color: #666;
    }
    .percent{
      height: 45px;
      line-height: 45px;
      font-size: 26px;
      text-align: left;
      color: #f44336;
      &::before{
        content:"占用率:";
        font-size: 12px;
      }
      &::after{
        content:"%";
        font-size: 12px;
      }
    }
  }
</style>