import request from "@/utils/request.js";


export function stockCheckNumber(params) {
  return request({ url: `/stock_check_orders/number/`, method: 'get', params })
}

export function stockCheckCreate(data) {
  return request({ url: `/stock_check_orders/`, method: 'post', data })
}