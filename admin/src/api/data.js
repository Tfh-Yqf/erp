import request from '@/utils/request';


// 仓库
export function getWarehouseNumber(params) {
  return request({ url: `/warehouses/number/`, method: 'get', params })
}

// 供应商
export function getSupplierNumber(params) {
  return request({ url: `/suppliers/number/`, method: 'get', params })
}

// 客户
export function getClientNumber(params) {
  return request({ url: `/clients/number/`, method: 'get', params })
}

// 结算账户
export function getSettlementAccountNumber(params) {
  return request({ url: `/accounts/number/`, method: 'get', params })
}

// 产品信息
export function getGoodsNumber(params) {
  return request({ url: `/goods/number/`, method: 'get', params })
}


// 日常采购
export function getPurchaseNumber(params) {
  return request({ url: `/purchase_requisitions/number/`, method: 'get', params })
}

// 采购单
export function getPurchaseOrderNumber(params) {
  return request({ url: `/purchase_orders/number/`, method: 'get', params })
}

// 采购退货单
export function getPurchaseReturnOrderNumber(params) {
  return request({ url: `/purchase_return_orders/number/`, method: 'get', params })
}

// 销售开单
export function getSaleOrderNumber(params) {
  return request({ url: `/sales_orders/number/`, method: 'get', params })
}

// 销售退货
export function getSaleReturnOrderNumber(params) {
  return request({ url: `/sales_return_orders/number/`, method: 'get', params })
}

// 调拨单
export function getStockTransferOrderNumber(params) {
  return request({ url: `/stock_transfer_orders/number/`, method: 'get', params })
}

// 盘点单
export function getStockCheckOrderNumber(params) {
  return request({ url: `/stock_check_orders/number/`, method: 'get', params })
}

// 付款单
export function getPaymentOrderNumber(params) {
  return request({ url: `/payment_orders/number/`, method: 'get', params })
}

// 收款单
export function getCollectionOrderNumber(params) {
  return request({ url: `/collection_orders/number/`, method: 'get', params })
}

// 日常收支
export function getChargeOrderNumber(params) {
  return request({ url: `/charge_orders/number/`, method: 'get', params })
}

// // 装箱清单
// export function getPackingNumber(params) {
//   return request({ url: `/packing_orders/number/`, method: 'get', params })
// }

// // 原料入库
// export function getMaterialStockInNumber(params) {
//   return request({ url: `/material_stock_in_orders/number/`, method: 'get', params })
// }

// // 原料出库
// export function getMaterialStockOutNumber(params) {
//   return request({ url: `/material_stock_out_orders/number/`, method: 'get', params })
// }

// // 成品入库
// export function getProductStockInNumber(params) {
//   return request({ url: `/product_stock_in_orders/number/`, method: 'get', params })
// }

// // 成品出库
// export function getProductStockOutNumber(params) {
//   return request({ url: `/product_stock_out_orders/number/`, method: 'get', params })
// }

// // 原料字典
// export function getmaterialDictNumber(params) {
//   return request({ url: `/materials/number/`, method: 'get', params })
// }

// // 成品字典
// export function getproductsDictNumber(params) {
//   return request({ url: `/products/number/`, method: 'get', params })
// }


// // Client
// export function clientList(params) {
//   return request({ url: `/clients/`, method: 'get', params })
// }

// export function clientCreate(data) {
//   return request({ url: `/clients/`, method: 'post', data })
// }

// export function clientUpdate(data) {
//   return request({ url: `/clients/${data.id}/`, method: 'put', data })
// }

// export function clientDestroy(data) {
//   return request({ url: `/clients/${data.id}/`, method: 'delete', data })
// }

// // Unit
// export function unitList(params) {
//   return request({ url: `/units/`, method: 'get', params })
// }

// export function unitCreate(data) {
//   return request({ url: `/units/`, method: 'post', data })
// }

// export function unitUpdate(data) {
//   return request({ url: `/units/${data.id}/`, method: 'put', data })
// }

// export function unitDestroy(data) {
//   return request({ url: `/units/${data.id}/`, method: 'delete', data })
// }
