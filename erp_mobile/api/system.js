import request from "@/utils/request.js";


// 获取令牌
export function getToken(data) {
  return request({ url: '/user/get_token/', method: 'post', header: {}, data });
}

// 获取用户信息
export function getInfo(data) {
  return request({ url: '/user/info/', method: 'get', data });
}

// 刷新令牌
export function refreshToken(data) {
  return request({ url: '/user/refresh_token/', method: 'post', header: {}, data });
}

// 首页概览
export function homeOverview(data) {
  return request({ url: `/home_overview/`, method: "get", data });
}
