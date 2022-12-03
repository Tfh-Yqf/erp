import { message } from "ant-design-vue";
import Cookies from "js-cookie";
import router from "@/router";
import axios from "axios";

const GET_TOKEN_URL = "/user/get_token/";
const REFRESH_TOKEN_URL = "/user/refresh_token/";
const LOGIN_PATH = "/user/login";
let requestQueue = [],
  isRefreshing = false;

const instance = axios.create({
  baseURL: "/admin/",
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

instance.interceptors.request.use(
  (config) => {
    if (!config.url.includes(GET_TOKEN_URL) && !config.url.includes(REFRESH_TOKEN_URL)) {
      config.headers.Authorization = "Bearer " + Cookies.get("access");
    }

    console.info("Send request:", config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (!error.response) return Promise.reject(error);
    console.error("Request error:", error.response);

    if (error.response.status >= 500) {
      message.error("服务器错误");
      return Promise.reject(error);
    }

    if (error.response.status == 401 && !error.config.url.includes(REFRESH_TOKEN_URL)) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          requestQueue.push(() => {
            resolve(instance(error.config));
          });
        });
      } else {
        isRefreshing = true;
        return refreshToken()
          .then((data) => {
            Cookies.set("access", data.access);
            requestQueue.forEach((fn) => fn());
            requestQueue = [];

            return instance(error.config);
          })
          .catch((error) => {
            if (error.response.status == 401) {
              redirectLogin();
              message.error("令牌过期, 请重新登录");
            }
            return Promise.reject(error);
          })
          .finally(() => {
            isRefreshing = false;
          });
      }
    }

    message.error(error.response.data.detail);
    return Promise.reject(error);
  }
);

function refreshToken() {
  return request({ url: REFRESH_TOKEN_URL, method: "post", data: { refresh: Cookies.get("refresh") } });
}

function redirectLogin() {
  requestQueue = [];
  router.push(LOGIN_PATH);
}

export default function request(item) {
  let { data = {} } = item;
  for (let key in data) {
    if (data[key] == undefined) delete data[key];
  }

  return instance(item);
}
