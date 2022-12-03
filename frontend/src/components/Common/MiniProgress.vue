<template>
  <div class="chart-mini-progress">
    <div class="progress-wrapper">
      <div class="progress" :style="{ backgroundColor: color, width: percentage + '%', height: height+'px' }"></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'MiniProgress',
    props: {
      height: {
        type: Number,
        default: 10
      },
      color: {
        type: String,
        default: '#13C2C2'
      },
      percentage: {
        type: Number,
        default: 0
      }
    }
  }
</script>

<style lang="less" scoped>
  .chart-mini-progress {
    padding: 5px 0;
    position: relative;
    width: 100%;
    .progress-wrapper {
      background-color: #f5f5f5;
      position: relative;
      .progress {
        transition: all .4s cubic-bezier(.08, .82, .17, 1) 0s;
        border-radius: 1px 0 0 1px;
        background-color: #1890ff;
        width: 0;
        height: 100%;
      }
    }
  }
</style>