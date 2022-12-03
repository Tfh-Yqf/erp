import request from '@/utils/request';

// 销售开单
export function saleOrderCreate(data) {
  return request({ url: `/sales_orders/`, method: 'post', data })
}

// 销售记录
export function saleOrderList(params) {
  return request({ url: `/sales_orders/`, method: 'get', params })
}

// 销售记录详情
export function saleOrderDetail(params) {
  return request({ url: `/sales_orders/${params.id}/`, method: 'get', params })
}

// 销售记录录作废
export function saleOrdersVoid(data) {
  return request({ url: `/sales_orders/${data.id}/void/`, method: 'post', data })
}

// 销售退货
export function saleReturnOrderCreate(data) {
  return request({ url: `/sales_return_orders/`, method: 'post', data })
}

// 销售退货记录
export function saleReturnOrderList(params) {
  return request({ url: `/sales_return_orders/`, method: 'get', params })
}

// 销售退货详情
export function saleReturnOrderDetail(params) {
  return request({ url: `/sales_return_orders/${params.id}/`, method: 'get', params })
}

// 销售任务
export function saleTaskList(params) {
  return request({ url: `/sales_tasks/`, method: 'get', params })
}

// 销售任务新增
export function saleTaskCreate(data) {
  return request({ url: `/sales_tasks/`, method: 'post', data })
}


// 销售任务删除
export function saleTaskDestroy(data) {
  return request({ url: `/sales_tasks/${data.id}/`, method: 'delete', data })
}