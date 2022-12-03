<template>
  <a-tooltip placement="top">
        <template slot="title">
          <span>{{message}}</span>
        </template>
        <a-button  shape="circle" icon="question" />
      </a-tooltip>
</template>

<script>
export default {
    props:['message'],
}
</script>

<style>

</style>