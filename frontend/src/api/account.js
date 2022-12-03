import request from '@/utils/request';


// Role
export function roleList(params) {
  return request({ url: `/roles/`, method: 'get', params })
}

export function roleCreate(data) {
  return request({ url: `/roles/`, method: 'post', data })
}

export function roleUpdate(data) {
  return request({ url: `/roles/${data.id}/`, method: 'put', data })
}

export function roleDestroy(data) {
  return request({ url: `/roles/${data.id}/`, method: 'delete', data })
}


// User
export function userList(params) {
  return request({ url: `/users/`, method: 'get', params })
}

export function userCreate(data) {
  return request({ url: `/users/`, method: 'post', data })
}

export function userUpdate(data) {
  return request({ url: `/users/${data.id}/`, method: 'put', data })
}

export function userDestroy(data) {
  return request({ url: `/users/${data.id}/`, method: 'delete', data })
}

export function userResetPassword(data) {
  return request({ url: `/users/${data.id}/reset_password/`, method: 'post', data })
}
