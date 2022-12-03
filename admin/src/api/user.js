import request from '@/utils/request';


// GetToken
export function getToken(data) {
  return request({ url: `/user/get_token/`, method: 'post', data }, false)
}

// RefreshToken
export function refreshToken(data) {
  return request({ url: `/user/refresh_token/`, method: 'post', data })
}

// GetInfo
export function getInfo(params) {
  return request({ url: `/user/info/`, method: 'get', params })
}

// SetPassword
export function setPassword(data) {
  return request({ url: `/user/set_password/`, method: 'post', data })
}

// 常用功能
export function getCommonFunctions(params) {
  return request({ url: `/user/common_functions/`, method: 'get', params })
}

// 设置常用功能
export function setCommonFunctions(data) {
  return request({ url: `/user/set_common_functions/`, method: 'post', data })
}