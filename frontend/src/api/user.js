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


