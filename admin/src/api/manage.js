import Cookies from "js-cookie";
import axios from "axios";

export function getCSRFToken(data) {
  return axios({
    url: "/api/super_user/get_csrf_token/",
    method: "get",
    data,
  });
}

// SuperUSer
export function superUserLogin(data) {
  return axios({
    url: "/api/super_user/login/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "post",
    data,
  });
}

export function superUserLogout(data) {
  return axios({
    url: "/api/super_user/logout/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "post",
    data,
  });
}

export function superUserInfo(params) {
  return axios({
    url: "/api/super_user/info/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "get",
    params,
  });
}


// Team
export function teamList(params) {
  return axios({
    url: "/api/teams/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "get",
    params,
  });
}

export function teamCreate(data) {
  return axios({
    url: "/api/teams/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "post",
    data,
  });
}

export function teamUpdate(data) {
  return axios({
    url: `/api/teams/${data.id}/`,
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "put",
    data,
  });
}

export function teamDestroy(data) {
  return axios({
    url: `/api/teams/${data.id}/`,
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "delete",
  });
}

// Device
export function deviceList(params) {
  return axios({
    url: "/api/devices/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "get",
    params,
  });
}

export function deviceCreate(data) {
  return axios({
    url: "/api/devices/",
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "post",
    data,
  });
}

export function deviceUpdate(data) {
  return axios({
    url: `/api/devices/${data.id}/`,
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "put",
    data,
  });
}

export function deviceDestroy(data) {
  return axios({
    url: `/api/devices/${data.id}/`,
    headers: { "X-CSRFToken": Cookies.get("csrftoken") },
    method: "delete",
  });
}
