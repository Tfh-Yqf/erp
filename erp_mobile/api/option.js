import request from "@/utils/request.js";

// UserOption
export function userOption(data) {
  return request({ url: `/users/options/`, method: 'get', data })
}

// Warehouse
export function warehouseOption(data) {
  return request({ url: `/warehouses/options/`, method: 'get', data })
}

// BatchOption
export function batchOption(data) {
  return request({ url: `/batchs/options/`, method: 'get', data })
}

// InventoryOption
export function inventoryOption(data) {
  return request({ url: `/inventories/options/`, method: 'get', data })
}

// Category
export function categoryOption(data) {
  return request({ url: `/goods_categories/options/`, method: 'get', data })
}

// Unit
export function unitOption(data) {
  return request({ url: `/goods_units/options/`, method: 'get', data })
}
