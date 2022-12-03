import request from "@/utils/request";

// 生产计划
export function productionOrderList(params) {
  return request({ url: `/production_orders/`, method: "get", params });
}

export function productionOrderDetail(params) {
  return request({ url: `/production_orders/${params.id}/`, method: "get", params });
}

export function productionOrderCreate(data) {
  return request({ url: `/production_orders/`, method: "post", data });
}

export function productionOrderUpdate(data) {
  return request({ url: `/production_orders/${data.id}/`, method: "put", data });
}

export function productionOrderDelete(data) {
  return request({ url: `/production_orders/${data.id}/`, method: "delete", data });
}

export function productionOrderNumber(params) {
  return request({ url: `/production_orders/number/`, method: "get", params });
}

export function productionOrderIssue(data) {
  return request({ url: `/production_orders/${data.id}/issue/`, method: "post", data });
}

export function productionOrderClose(data) {
  return request({ url: `/production_orders/${data.id}/close/`, method: "post", data });
}

// 生产记录
export function productionRecordList(params) {
  return request({ url: `/production_records/`, method: "get", params });
}

export function productionRecordDetail(params) {
  return request({ url: `/production_records/${params.id}/`, method: "get", params });
}

export function productionRecordCreate(data) {
  return request({ url: `/production_records/`, method: "post", data });
}
