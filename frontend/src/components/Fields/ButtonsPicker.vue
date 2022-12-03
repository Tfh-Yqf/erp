<template>
  <a-row  align="middle" style="margin:0px;padding:0px;">
    <a-col :span="12">
      <a-form-model-item :wrapper-col="{ span: 24 }" style="margin:0px;">
        <a-radio-group
          v-model="radioValue"
          button-style="solid"
          @change="changeRadio"
          style="width: 100%"
        >
          <a-radio-button value="0" style="width: 25%">今日</a-radio-button>
          <!-- <a-radio-button value="1" style="width: 25%">昨天</a-radio-button> -->
          <a-radio-button value="-6" style="width: 25%">近7天</a-radio-button>
          <a-radio-button value="-29" style="width: 25%">近30天</a-radio-button>
          <a-radio-button value="-364" style="width: 25%">近一年</a-radio-button>
        </a-radio-group>
      </a-form-model-item>
    </a-col>
    <a-col :span="12">
      <a-form-model-item
        label="自定义时间"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-range-picker
          v-model="dateRange"
          @change="changeDate"
          style="width: 100%"
        />
      </a-form-model-item>
    </a-col>
  </a-row>
</template>

<script>
import moment from "moment";
export default {
  props: ["radioValue",'dateRange'],
  data() {
    return {
      moment,
    };
  },
  methods: {
      changeRadio(evt){
        this.changeDate(evt);
        let value = evt.target.value;
        this.$emit('aRadioGroupChange',value);
      },
    changeDate(evt) {
      if (evt.target) {
        let value = evt.target.value;
        if (value < 0) {
          this.$emit('aRangePickerChange',[
            moment().startOf("day").add(value, "day"),
            moment().startOf("day"),
          ]);
        } else {
           this.$emit('aRangePickerChange',[
              moment().startOf("day").subtract(value, "day"),
            moment().startOf("day").subtract(value, "day"),
          ]);
        }
        
      } else {
         this.$emit('aRangePickerChange',evt);
      }
    },
  },
};
</script>

<style scoped>
.ant-row:after, .ant-row:before{
  content:none;
}
</style>