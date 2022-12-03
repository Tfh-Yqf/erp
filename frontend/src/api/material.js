import request from '@/utils/request';


// Material
export function materialList(params) {
  return request({ url: `/materials/`, method: 'get', params })
}

export function materialCreate(data) {
  return request({ url: `/materials/`, method: 'post', data })
}

export function materialUpdate(data) {
  return request({ url: `/materials/${data.id}/`, method: 'put', data })
}

export function materialDestroy(data) {
  return request({ url: `/materials/${data.id}/`, method: 'delete', data })
}


// Batch
export function batchList(params) {
  return request({ url: `/batchs/`, method: 'get', params })
}

// Inventory
export function inventoryList(params) {
  return request({ url: `/inventories/`, method: 'get', params })
}

// WarehouseInventory
export function warehouseInventoryList(params) {
  return request({ url: `/warehouse_inventories/`, method: 'get', params })
}