import request from "@/utils/request.js";

// 入库任务
export function stockInTaskList(data) {
  return request({ url: `/stock_in_orders/`, method: 'get', data });
}

// 入库记录
export function stockInRecordCreate(data) {
  return request({ url: `/stock_in_records/`, method: 'post', data });
}
