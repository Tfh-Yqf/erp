import request from '@/utils/request';

// Permission
export function permissionList(params) {
  return request({ url: `/permission_groups/`, method: 'get', params })
}

// 系统配置
export function configInfo(params) {
  return request({ url: `/system/configs/`, method: 'get', params })
}

// 系统配置-更新
export function configUpdate(data) {
  return request({ url: `/system/set_configs/`, method: 'post', data })
}

// 库存预警
export function inventoryWarningsList(params) {
  return request({ url: `/inventory_warnings/`, method: 'get', params })
}

// 入库任务提醒
export function stockInList(params) {
  return request({ url: `/stock_in_order_reminders/`, method: 'get', params })
}
// 出库任务提醒
export function stockOutList(params) {
  return request({ url: `/stock_out_order_reminders/`, method: 'get', params })
}
// 销售前十产品
export function salesTopTenList(params) {
  return request({ url: `/sales_hot_goods/`, method: 'get', params })
}
// 销售走势
export function salesTrendList(params) {
  return request({ url: `/sales_trends/`, method: 'get', params })
}
