import request from '@/utils/request';
import Cookies from 'js-cookie'
import axios from 'axios'


// 客户模板
export function clientTemplate(params) {
  return axios({
    url: '/api/clients/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 客户导入
export function clientImport(data) {
  return axios({
    url: '/api/clients/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 供应商模板
export function supplierTemplate(params) {
  return axios({
    url: '/api/suppliers/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 供应商导入
export function supplierImport(data) {
  return axios({
    url: '/api/suppliers/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 仓库模板
export function warehouseTemplate(params) {
  return axios({
    url: '/api/warehouses/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 仓库导入
export function warehouseImport(data) {
  return axios({
    url: '/api/warehouses/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 结算账户模板
export function settlementAccountTemplate(params) {
  return axios({
    url: '/api/accounts/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 结算账户导入
export function settlementAccountImport(data) {
  return axios({
    url: '/api/accounts/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 收支项目模板
export function revenueExpenditureItemsTemplate(params) {
  return axios({
    url: '/api/charge_items/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 收支项目导入
export function revenueExpenditureItemsImport(data) {
  return axios({
    url: '/api/charge_items/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 产品分类模板
export function goodsClassificationTemplate(params) {
  return axios({
    url: '/api/goods_categories/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品分类导入
export function goodsClassificationImport(data) {
  return axios({
    url: '/api/goods_categories/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 产品信息模板
export function goodsInformationTemplate(params) {
  return axios({
    url: '/api/goods/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品信息导入
export function goodsInformationImport(data) {
  return axios({
    url: '/api/goods/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 产品单位模板
export function goodsUnitTemplate(params) {
  return axios({
    url: '/api/goods_units/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品单位导入
export function goodsUnitImport(data) {
  return axios({
    url: '/api/goods_units/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// // 原料字典模板
// export function materialDictTemplate(params) {
//   return axios({
//     url: '/api/materials/import_template/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 原料字典导入
// export function materialDictImport(data) {
//   return axios({
//     url: '/api/materials/import_data/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // 成品字典模板
// export function productsDictTemplate(params) {
//   return axios({
//     url: '/api/products/import_template/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 成品字典导入
// export function productsDictImport(data) {
//   return axios({
//     url: '/api/products/import_data/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

