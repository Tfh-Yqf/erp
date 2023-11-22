import request from '@/utils/request';


// Role
export function get_goodscategory(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/get_goodscategory`, method: 'get' })
}

export function add_average(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/average_price?id=`+params.id+'&price='+params.average_price, method: 'get' })
}

export function get_predict(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/get_predict`, method: 'get' })
}

export function update_predict(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/update_predict?id=`+params.id+'&predict_price='+params.predict_price+'&predict_number='+params.predict_number, method: 'get' })
}

export function get_predict_duibi(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/get_predict_duibi`, method: 'get' })
}

export function get_moeny(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/get_money`, method: 'get' })
}

export function update_moeny(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/update_money?id=`+params.id+'&money='+params.balance_amount, method: 'get' })
}

export function get_caigou_bishu(params) {
    return request({ url: `https://xingqianli.tanfuhua.com/get_caigou_bishu`, method: 'get' })
}