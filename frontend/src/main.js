import functions from "@/utils/functions";
import VueRouter from "vue-router";
import router from "./router";
import store from "./store";
import App from "./App.vue";
import Vue from "vue";
import Viser from "viser-vue";
import Antd from "ant-design-vue/es";
import Print from "vue-print-nb";
import htmlToPdf from "@/utils/htmlToPdf";
import vuescroll from 'vuescroll';

import "ant-design-vue/dist/antd.less";

Vue.config.productionTip = false;
Vue.prototype.$functions = functions;
Vue.use(VueRouter);
Vue.use(Viser);
Vue.use(Antd);
Vue.use(Print);
Vue.use(htmlToPdf);
Vue.use(vuescroll, {
  ops: {
    mode: 'native',
    bar: {
      showDelay: 500,
      onlyShowBarOnScroll: false,//是否只有滚动的时候才显示滚动条
      keepShow: false,
      background: '#1AB063',
      opacity: 0.2,
      hoverStyle: false,
      specifyBorderRadius: false,
      minSize: false,
      size: '6px',
      disable: false,
'overflow-x': 'hidden',
    }
  }, // 在这里设置全局默认配置
  name: 'vueScroll' // 在这里自定义组件名字，默认是vueScroll
});

Vue.prototype.ProjectName='行千里进销存管理系统'
Vue.prototype.OnwerName='行千里'
Vue.prototype.JavaUrl='http://81.70.135.77:8089/'
Vue.prototype.DjangoUrl='http://127.0.0.1:8080/'

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");

