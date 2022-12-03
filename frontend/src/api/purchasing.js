import request from '@/utils/request';

// 采购开单
export function purchaseOrderCreate(data) {
  return request({ url: `/purchase_orders/`, method: 'post', data })
}

// 采购记录
export function purchaseOrderList(params) {
  return request({ url: `/purchase_orders/`, method: 'get', params })
}

// 采购记录详情
export function purchaseOrderDetail(params) {
  return request({ url: `/purchase_orders/${params.id}/`, method: 'get', params })
}

// 采购记录作废
export function purchaseOrdersVoid(data) {
  return request({ url: `/purchase_orders/${data.id}/void/`, method: 'post', data })
}

// 采购退货单
export function purchaseReturnOrderCreate(data) {
  return request({ url: `/purchase_return_orders/`, method: 'post', data })
}

// 退货记录
export function purchaseReturnOrdersList(params) {
  return request({ url: `/purchase_return_orders/`, method: 'get', params })
}

// 退货记录详情
export function purchaseReturnOrderDetail(params) {
  return request({ url: `/purchase_return_orders/${params.id}/`, method: 'get', params })
}

// 退货记录作废
export function purchaseReturnOrdersVoid(data) {
  return request({ url: `/purchase_return_orders/${data.id}/void/`, method: 'post', data })
}

