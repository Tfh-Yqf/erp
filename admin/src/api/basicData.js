import request from '@/utils/request';

// 客户
export function clientList(params) {
  return request({ url: `/clients/`, method: 'get', params })
}

export function clientCreate(data) {
  return request({ url: `/clients/`, method: 'post', data })
}

export function clientUpdate(data) {
  return request({ url: `/clients/${data.id}/`, method: 'put', data })
}

export function clientDestroy(data) {
  return request({ url: `/clients/${data.id}/`, method: 'delete', data })
}

// 供应商
export function supplierList(params) {
  return request({ url: `/suppliers/`, method: 'get', params })
}

export function supplierCreate(data) {
  return request({ url: `/suppliers/`, method: 'post', data })
}

export function supplierUpdate(data) {
  return request({ url: `/suppliers/${data.id}/`, method: 'put', data })
}

export function supplierDestroy(data) {
  return request({ url: `/suppliers/${data.id}/`, method: 'delete', data })
}

// 仓库
export function warehouseList(params) {
  return request({ url: `/warehouses/`, method: 'get', params })
}

export function warehouseCreate(data) {
  return request({ url: `/warehouses/`, method: 'post', data })
}

export function warehouseUpdate(data) {
  return request({ url: `/warehouses/${data.id}/`, method: 'put', data })
}

export function warehouseDestroy(data) {
  return request({ url: `/warehouses/${data.id}/`, method: 'delete', data })
}

// 结算账户
export function settlementAccountList(params) {
  return request({ url: `/accounts/`, method: 'get', params })
}

export function settlementAccountCreate(data) {
  return request({ url: `/accounts/`, method: 'post', data })
}

export function settlementAccountUpdate(data) {
  return request({ url: `/accounts/${data.id}/`, method: 'put', data })
}

export function settlementAccountDestroy(data) {
  return request({ url: `/accounts/${data.id}/`, method: 'delete', data })
}

// 收支项目
export function revenueExpenditureItemsList(params) {
  return request({ url: `/charge_items/`, method: 'get', params })
}

export function revenueExpenditureItemsCreate(data) {
  return request({ url: `/charge_items/`, method: 'post', data })
}

export function revenueExpenditureItemsUpdate(data) {
  return request({ url: `/charge_items/${data.id}/`, method: 'put', data })
}

export function revenueExpenditureItemsDestroy(data) {
  return request({ url: `/charge_items/${data.id}/`, method: 'delete', data })
}

// // 原料字典
// export function materialDictList(params) {
//   return request({ url: `/materials/`, method: 'get', params })
// }

// export function materialDictCreate(data) {
//   return request({ url: `/materials/`, method: 'post', data })
// }

// export function materialDictUpdate(data) {
//   return request({ url: `/materials/${data.id}/`, method: 'put', data })
// }

// export function materialDictDestroy(data) {
//   return request({ url: `/materials/${data.id}/`, method: 'delete', data })
// }

// // 成品字典
// export function productsDictList(params) {
//   return request({ url: `/products/`, method: 'get', params })
// }

// export function productsDictCreate(data) {
//   return request({ url: `/products/`, method: 'post', data })
// }

// export function productsDictUpdate(data) {
//   return request({ url: `/products/${data.id}/`, method: 'put', data })
// }

// export function productsDictDestroy(data) {
//   return request({ url: `/products/${data.id}/`, method: 'delete', data })
// }

