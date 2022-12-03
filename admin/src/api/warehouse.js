import request from '@/utils/request';

// 入库任务
export function stockInOrdersList(params) {
  return request({ url: `/stock_in_orders/`, method: 'get', params })
}
// 入库通知单据
export function stockInOrderDetail(params) {
  return request({ url: `/stock_in_orders/${params.id}/`, method: 'get', params })
}
// 入库记录
export function stockInRecordsList(params) {
  return request({ url: `/stock_in_records/`, method: 'get', params })
}
// 入库
export function stockInCreate(data) {
  return request({ url: `/stock_in_records/`, method: 'post', data })
}
// 入库记录详情
export function stockInRecordDetail(params) {
  return request({ url: `/stock_in_records/${params.id}/`, method: 'get', params })
}

// 入库记录作废
export function stockInOrdersVoid(data) {
  return request({ url: `/stock_in_records/${data.id}/void/`, method: 'post', data })
}

// 出库任务
export function stockOutOrdersList(params) {
  return request({ url: `/stock_out_orders/`, method: 'get', params })
}
// 出库通知单据
export function stockOutOrderDetail(params) {
  return request({ url: `/stock_out_orders/${params.id}/`, method: 'get', params })
}
// 出库
export function stockOutCreate(data) {
  return request({ url: `/stock_out_records/`, method: 'post', data })
}
// 出库记录
export function stockOutRecordsList(params) {
  return request({ url: `/stock_out_records/`, method: 'get', params })
}
// 出库记录详情
export function stockOutRecordDetail(params) {
  return request({ url: `/stock_out_records/${params.id}/`, method: 'get', params })
}
// 出库记录作废
export function stockOutOrdersVoid(data) {
  return request({ url: `/stock_out_records/${data.id}/void/`, method: 'post', data })
}

// 调拨
export function stockTransferOrdersList(params) {
  return request({ url: `/stock_transfer_orders/`, method: 'get', params })
}
// 调拨记录作废
export function stockTransferOrdersVoid(data) {
  return request({ url: `/stock_transfer_orders/${data.id}/void/`, method: 'post', data })
}
// 调拨
export function stockTransferCreate(data) {
  return request({ url: `/stock_transfer_orders/`, method: 'post', data })
}
// 调拨详情
export function stockTransferDetail(params) {
  return request({ url: `/stock_transfer_orders/${params.id}/`, method: 'get', params })
}

// 盘点
export function stockCheckOrdersList(params) {
  return request({ url: `/stock_check_orders/`, method: 'get', params })
}
// 盘点记录作废
export function stockCheckOrdersVoid(data) {
  return request({ url: `/stock_check_orders/${data.id}/void/`, method: 'post', data })
}
// 盘点
export function stockCheckCreate(data) {
  return request({ url: `/stock_check_orders/`, method: 'post', data })
}
// 调拨详情
export function stockCheckDetail(params) {
  return request({ url: `/stock_check_orders/${params.id}/`, method: 'get', params })
}

// 库存流水
export function inventoryFlowsList(params) {
  return request({ url: `/inventory_flows/`, method: 'get', params })
}
// 库存流水详情
export function inventoryFlowsDetail(params) {
  return request({ url: `/inventory_flows/${params.id}/`, method: 'get', params })
}
// export function materialStockInCreate(data) {
//   return request({ url: `/material_stock_in_orders/`, method: 'post', data })
// }

// export function materialStockInUpdate(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'put', data })
// }

// export function materialStockInDestroy(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'delete', data })
// }

// export function materialStockInDetail(params) {
//   return request({ url: `/material_stock_in_orders/${params.id}/`, method: 'get', params })
// }

// export function materialStockInConfirm(data) {
//   return request({ url: `/material_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 原料出库
// export function materialStockOutList(params) {
//   return request({ url: `/material_stock_out_orders/`, method: 'get', params })
// }

// export function materialStockOutCreate(data) {
//   return request({ url: `/material_stock_out_orders/`, method: 'post', data })
// }

// export function materialStockOutUpdate(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'put', data })
// }

// export function materialStockOutDestroy(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'delete', data })
// }

// export function materialStockOutDetail(params) {
//   return request({ url: `/material_stock_out_orders/${params.id}/`, method: 'get', params })
// }

// export function materialStockOutConfirm(data) {
//   return request({ url: `/material_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 原料库存
// export function materialInventoriesList(params) {
//   return request({ url: `/material_inventories/`, method: 'get', params })
// }

// // 原料出入库明细
// export function materialInventoryFlowsList(params) {
//   return request({ url: `/material_inventory_flows/`, method: 'get', params })
// }

// // 成品入库
// export function productStockInList(params) {
//   return request({ url: `/product_stock_in_orders/`, method: 'get', params })
// }

// export function productStockInCreate(data) {
//   return request({ url: `/product_stock_in_orders/`, method: 'post', data })
// }

// export function productStockInUpdate(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'put', data })
// }

// export function productStockInDestroy(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'delete', data })
// }

// export function productStockInDetail(params) {
//   return request({ url: `/product_stock_in_orders/${params.id}/`, method: 'get', params })
// }

// export function productStockInConfirm(data) {
//   return request({ url: `/product_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 成品出库
// export function productStockOutList(params) {
//   return request({ url: `/product_stock_out_orders/`, method: 'get', params })
// }

// export function productStockOutCreate(data) {
//   return request({ url: `/product_stock_out_orders/`, method: 'post', data })
// }

// export function productStockOutUpdate(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'put', data })
// }

// export function productStockOutDestroy(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'delete', data })
// }

// export function productStockOutDetail(params) {
//   return request({ url: `/product_stock_out_orders/${params.id}/`, method: 'get', params })
// }

// export function productStockOutConfirm(data) {
//   return request({ url: `/product_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
// }

// // 成品库存
// export function productInventoriesList(params) {
//   return request({ url: `/product_inventories/`, method: 'get', params })
// }

// // 成品出入库明细
// export function productInventoryFlowsList(params) {
//   return request({ url: `/product_inventory_flows/`, method: 'get', params })
// }