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
import 'ant-design-vue/dist/antd.css';

Vue.config.productionTip = false;
Vue.prototype.$functions = functions;
Vue.use(VueRouter);
Vue.use(Viser);
Vue.use(Antd);
Vue.use(Print);
Vue.use(htmlToPdf);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
