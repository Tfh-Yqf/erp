import Cookies from 'js-cookie'
import axios from 'axios'


// 客户
export function clientExport(params) {
  return axios({
    url: '/api/clients/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 供应商
export function supplierExport(params) {
  return axios({
    url: '/api/suppliers/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 仓库
export function warehouseExport(params) {
  return axios({
    url: '/api/warehouses/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 结算账户
export function settlementAccountExport(params) {
  return axios({
    url: '/api/accounts/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 收支项目
export function revenueExpenditureItemsExport(params) {
  return axios({
    url: '/api/charge_items/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品分类
export function goodsClassificationExport(params) {
  return axios({
    url: '/api/goods_categories/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品信息
export function goodsInformationExport(params) {
  return axios({
    url: '/api/goods/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 产品单位
export function goodsUnitExport(params) {
  return axios({
    url: '/api/goods_units/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// // 原料字典
// export function materialDictExport(params) {
//   return axios({
//     url: '/api/materials/export/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 成品字典
// export function productsDictExport(params) {
//   return axios({
//     url: '/api/products/export/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

