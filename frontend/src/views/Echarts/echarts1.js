export const kucun_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        data_serios.push(data[i].total_quantity);
    }
    return {
        title: {
            text: '库存报表',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'产品名称'
        },
        yAxis: {
            name:'库存数量'
        },
        series: [
            {
                name: '库存',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}

export const caigou_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        if(data[i].purchase_price!=null&&data[i].purchase_price!=undefined)
            data_serios.push(data[i].purchase_price);
        else
            data_serios.push(data[i].total_purchase_amount);
    }
    return {
        title: {
            text: '采购明细',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'产品名称'
        },
        yAxis: {
            name:'采购价格'
        },
        series: [
            {
                name: '采购价格(元)',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}


export const xiaoshou_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        if(data[i].total_amount!=null&&data[i].total_amount!=undefined)
            data_serios.push(data[i].total_amount);
        else
            data_serios.push(data[i].total_sales_amount);
    }
    return {
        title: {
            text: '销售报表',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'产品名称'
        },
        yAxis: {
            name:'采购价格(元)'
        },
        series: [
            {
                name: '销售价格(元)',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}


export const sales_predict_echarts = (data) =>{

    var data_xAxis = [];
    var data_serios_predict_price = [];
    var data_serios_predict_number = [];
    var data_serios_sales_price = [];
    var data_serios_sales_number = [];

    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].name);
        data_serios_predict_price.push(data[i].predict_price);
        data_serios_predict_number.push(data[i].predict_number);

        data_serios_sales_price.push(data[i].sales_price);
        data_serios_sales_number.push(data[i].sales_quantity);
    }
    return {
        title: {
            text: '数据对比',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'产品名称'
        },
        yAxis:{
            name:'预期价格(元)'
        }
        ,
        series: [
            {
                name: '预期价格(元)',
                type: 'bar',
                data: data_serios_predict_price
            },
            {
                name: '已销售价格(元)',
                    type: 'bar',
                data: data_serios_sales_price
            },
            {
                name: '预期销售数量',
                type: 'bar',
                data: data_serios_predict_number
            },
            {
                name: '已销售数量',
                type: 'bar',
                data: data_serios_sales_number
            }
        ]
    }
}




