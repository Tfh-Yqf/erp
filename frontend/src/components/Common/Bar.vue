<template>
  <div :style="{ padding: '0' }">
    <h4 :style="{ marginTop: '20px', marginBottom: '10px', textAlign: 'center' }"><b>{{ title }}</b></h4>
    <v-chart :forceFit="true" :height="height" :data="dataSource" :scale="scale" :padding="padding">
      <span style="font-size: 12px;">{{ ytitle }}</span>
      <v-tooltip />
      <v-axis />
      <v-bar position="year*sales" />
    </v-chart>
  </div>
</template>

<script>
  export default {
    name: 'Bar',
    props: {
      title: {
        type: String,
        default: ''
      },
      ytitle: {
        type: String,
        default: ''
      },
      dataSource: {
        type: Array,
        default: () => [
          [
            { year: '1951 年', sales: 38 },
            { year: '1952 年', sales: 52 },
            { year: '1956 年', sales: 61 },
            { year: '1957 年', sales: 145 },
            { year: '1958 年', sales: 48 },
            { year: '1959 年', sales: 38 },
            { year: '1960 年', sales: 38 },
            { year: '1962 年', sales: 38 },
          ]
        ]
      },
      height: {
        type: Number,
        default: 150
      }
    },
    data() {
      return {
        padding: [20, 30, 40, 30],
        scale: [{
          dataKey: 'sales',
          tickInterval: 20,
        }]
      };
    }
  };
</script>