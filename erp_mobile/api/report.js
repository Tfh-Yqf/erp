import request from "@/utils/request.js";

// 批次报表
export function batchReportList(data) {
  return request({ url: `/batchs/`, method: 'get', data });
}
