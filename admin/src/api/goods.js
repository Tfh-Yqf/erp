import request from '@/utils/request';

// 产品分类
export function goodsClassificationList(params) {
  return request({ url: `/goods_categories/`, method: 'get', params })
}

export function goodsClassificationCreate(data) {
  return request({ url: `/goods_categories/`, method: 'post', data })
}

export function goodsClassificationUpdate(data) {
  return request({ url: `/goods_categories/${data.id}/`, method: 'put', data })
}

export function goodsClassificationDestroy(data) {
  return request({ url: `/goods_categories/${data.id}/`, method: 'delete', data })
}

// 产品信息
export function goodsInformationList(params) {
  return request({ url: `/goods/`, method: 'get', params })
}

export function goodsInformationCreate(data) {
  return request({ url: `/goods/`, method: 'post', data })
}

export function goodsInformationUpdate(data) {
  return request({ url: `/goods/${data.id}/`, method: 'put', data })
}

export function goodsInformationDestroy(data) {
  return request({ url: `/goods/${data.id}/`, method: 'delete', data })
}

// 产品单位
export function goodsUnitList(params) {
  return request({ url: `/goods_units/`, method: 'get', params })
}

export function goodsUnitCreate(data) {
  return request({ url: `/goods_units/`, method: 'post', data })
}

export function goodsUnitUpdate(data) {
  return request({ url: `/goods_units/${data.id}/`, method: 'put', data })
}

export function goodsUnitDestroy(data) {
  return request({ url: `/goods_units/${data.id}/`, method: 'delete', data })
}