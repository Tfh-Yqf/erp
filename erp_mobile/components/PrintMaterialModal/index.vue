<template>
  <u-modal :show="show" title="打印次数" :showCancelButton="true" confirmText="打印" @cancel="cancel" @confirm="confirm">
    <view class="slot-content">
      <view>
        <u--input type="digit" border="surround" :focus="true" v-model="printTimes"></u--input>
      </view>
    </view>
  </u-modal>
</template>

<script>
  const printer = uni.requireNativePlugin('LcPrinter');

  export default {
    props: ["show", "number", "name"],
    data() {
      return {
        printTimes: 1,
      }
    },
    methods: {
      initPrinter() {
        printer.initPrinter({});
        printer.printEnableMark({ enable: true });
        printer.setFontSize({ fontSize: 8 });
      },
      confirm() {
        if (printer === undefined) {
          uni.showToast({
            title: '打印失败，请联系软件厂商购买指定型号PDA',
            duration: 2000
          });
        }

        for (let index = 0; index < this.printTimes; index++) {
          printer.printLine({ line_length: 1 })
          printer.printBarcode2({
            offset: 1,
            text: this.number,
            height: 150,
            barcodeType: 73,
            hriPosition: 1,
          });
          printer.printLine({ line_length: 1 })
          printer.printText2({
            offset: 2,
            fontSize: 3,
            isBold: false,
            isUnderLine: false,
            content: `编号: ${this.number}\n`
          });
          printer.printText2({
            offset: 2,
            fontSize: 3,
            isBold: false,
            isUnderLine: false,
            content: `名称: ${this.name}`
          });
          printer.printGoToNextMark();
        }
        this.cancel();
      },
      cancel() {
        this.printTimes = 1;
        this.$emit("cancel", false);
      },
    },
    mounted() {
      this.initPrinter();
    },
  }
</script>

<style>
</style>
