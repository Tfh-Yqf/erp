import request from "@/utils/request.js";

// 出库任务
export function stockOutTaskList(data) {
  return request({ url: `/stock_out_orders/`, method: 'get', data });
}

// 出库记录
export function stockOutRecordCreate(data) {
  return request({ url: `/stock_out_records/`, method: 'post', data });
}
