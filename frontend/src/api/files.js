import Cookies from 'js-cookie'
import axios from 'axios'

// 上传产品图片
export function contractOriginalFiles(data) {
  return axios({
    url: '/api/goods_images/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// // 上传原件
// export function contractOriginalFiles(data) {
//   return axios({
//     url: '/api/contract_original_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // 上传复印件
// export function contractCopyFiles(data) {
//   return axios({
//     url: '/api/contract_copy_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // 上传图纸
// export function contractDrawingFiles(data) {
//   return axios({
//     url: '/api/drawing_files/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }