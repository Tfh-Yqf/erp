import request from '@/utils/request';

// 付款
export function paymentOrdersList(params) {
  return request({ url: `/payment_orders/`, method: 'get', params })
}
// 付款记录作废
export function paymentOrdersVoid(data) {
  return request({ url: `/payment_orders/${data.id}/void/`, method: 'post', data })
}
// 付款新增
export function paymentOrderCreate(data) {
  return request({ url: `/payment_orders/`, method: 'post', data })
}
// 付款详情
export function paymentOrderDetail(params) {
  return request({ url: `/payment_orders/${params.id}/`, method: 'get', params })
}

// 收款
export function collectionOrdersList(params) {
  return request({ url: `/collection_orders/`, method: 'get', params })
}
// 收款记录作废
export function collectionOrdersVoid(data) {
  return request({ url: `/collection_orders/${data.id}/void/`, method: 'post', data })
}
// 收款新增
export function collectionOrderCreate(data) {
  return request({ url: `/collection_orders/`, method: 'post', data })
}
// 收款详情
export function collectioOrderDetail(params) {
  return request({ url: `/collection_orders/${params.id}/`, method: 'get', params })
}

// 应付欠款
export function arrearsPayableList(params) {
  return request({ url: `/supplier_arrears/`, method: 'get', params })
}
// 应收欠款
export function arrearsReceivableList(params) {
  return request({ url: `/client_arrears/`, method: 'get', params })
}

// 账户转账
export function accountTransferOrdersList(params) {
  return request({ url: `/account_transfer_records/`, method: 'get', params })
}
// 账户转账记录作废
export function accountTransferOrdersVoid(data) {
  return request({ url: `/account_transfer_records/${data.id}/void/`, method: 'post', data })
}
// 账户转账新增
export function accountTransferOrderCreate(data) {
  return request({ url: `/account_transfer_records/`, method: 'post', data })
}

// 日常收支
export function chargeOrdersList(params) {
  return request({ url: `/charge_orders/`, method: 'get', params })
}
// 日常收支记录作废
export function chargeOrdersVoid(data) {
  return request({ url: `/charge_orders/${data.id}/void/`, method: 'post', data })
}
// 日常收支新增
export function chargeOrderCreate(data) {
  return request({ url: `/charge_orders/`, method: 'post', data })
}

// 资金流水
export function financeFlowsList(params) {
  return request({ url: `/finance_flows/`, method: 'get', params })
}
// 资金流水详情
export function financeFlowDetail(params) {
  return request({ url: `/finance_flows/${params.id}/`, method: 'get', params })
}

// // 采购记录作废
// export function purchaseOrdersVoid(data) {
//   return request({ url: `/purchase_orders/${data.id}/void/`, method: 'post', data })
// }

// // 采购退货单
// export function purchaseReturnOrderCreate(data) {
//   return request({ url: `/purchase_return_orders/`, method: 'post', data })
// }

// // 退货记录
// export function purchaseReturnOrdersList(params) {
//   return request({ url: `/purchase_return_orders/`, method: 'get', params })
// }