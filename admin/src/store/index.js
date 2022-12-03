import system from "./modules/system";
import user from "./modules/user";
import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    system,
  },
});
