import request from "@/utils/request.js";


// Product
export function productList(data) {
  return request({ url: '/goods/', method: 'get', data });
}

export function productCreate(data) {
  return request({ url: '/goods/', method: 'post', data });
}

export function productUpdate(data) {
  return request({ url: `/goods/${data.id}/`, method: 'put', data });
}

export function productDestroy(data) {
  return request({ url: `/goods/${data.id}/`, method: 'delete', data });
}

export function productNumber(data) {
  return request({ url: '/goods/number/', method: 'get', data });
}
