import request from "@/utils/request";

// HomeOverview
export function homeOverview(params) {
  return request({ url: `/home_overview/`, method: "get", params });
}
