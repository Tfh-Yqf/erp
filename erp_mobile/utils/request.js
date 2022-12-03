import { refreshToken } from "@/api/system.js"

const GET_TOKEN_URL = '/user/get_token/';
const REFRESH_TOKEN_URL = '/user/refresh_token/';
const BASE_URL = 'http://114.218.158.78:12223/api';
// const BASE_URL = 'http://114.218.158.78:12224/api';


let requestQueue = [];
let isRefreshing = false;
export default function request(item) {
  console.log('======================Request======================')
  if (!item.url.includes(GET_TOKEN_URL) && !item.url.includes(REFRESH_TOKEN_URL)) {
    let access_token = uni.getStorageSync('access');
    item.header = {
      'Authorization': 'Bearer ' + access_token,
    };
  }

  console.log('请求地址:', item.url);
  console.log('令牌:', item.header.Authorization);

  return new Promise((resolve, reject) => {
    return uni.request({
      url: BASE_URL + item.url,
      method: item.method,
      header: item.header,
      data: item.data,
      success: (response) => {
        console.log('返回结果:', response.data);

        if (response.statusCode >= 200 && response.statusCode < 300) {
          return resolve(response.data);
        } else if (response.statusCode >= 500) {
          uni.showToast({ title: '服务器错误', icon: 'error', duration: 1000 });
          return reject({ message: '服务器错误' });
        } else if (response.statusCode == 401 && !item.url.includes(REFRESH_TOKEN_URL)) {
          if (isRefreshing) {
            return new Promise((resolve) => {
              requestQueue.push(() => {
                return resolve(request(item));
              });
            });
          } else {
            let refresh_token = uni.getStorageSync('refresh');
            if (refreshToken && refresh_token != '') {
              isRefreshing = true;
              return refreshToken({ refresh: refresh_token }).then((data) => {
                uni.setStorageSync('access', data.access)
                requestQueue.forEach(fn => fn());
                requestQueue = [];
                return resolve(request(item));
              }).catch(() => {
                redirectLogin();
                uni.showToast({ title: '未登录', icon: 'none', duration: 1000 });
                return reject({ message: '未登录' });
              }).finally(() => {
                isRefreshing = false;
              });
            } else {
              redirectLogin();
              uni.showToast({ title: '未登录', icon: 'none', duration: 1000 });
              return reject({ message: '未登录' });
            }
          }
        } else {
          uni.showToast({ title: response.data.detail, icon: 'none', duration: 1000 });
          return reject({ message: response.data.detail });
        }
      },
      fail: (error) => {
        console.log('Error:', error);
        uni.showToast({ title: '无法连接', icon: 'none', duration: 1000 });
        return reject(error)
      },
    })
  })
}


function redirectLogin() {
  requestQueue = [];
  uni.redirectTo({ url: '/pages/login/index' });
}
