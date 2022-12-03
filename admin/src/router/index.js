import VueRouter from "vue-router";
import user from "./user";

const index = {
  path: "/",
  component: () => import("@/layouts/BaseLayout"),
  redirect: "/team",
  children: [
    {
      path: "/team",
      component: () => import("@/views/team/index"),
    },
    {
      path: "/device",
      component: () => import("@/views/device/index"),
    },
  ],
};

const routes = [index, user];

export default new VueRouter({ mode: "history", routes });
