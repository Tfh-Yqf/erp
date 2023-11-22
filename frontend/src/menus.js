export default [

  {
    key: '2', name: '基础档案', icon: 'table', submenus: [
      { key: '/basicData/client', name: '客户管理'},
      { key: '/basicData/supplier', name: '供应商管理'},
      { key: '/basicData/warehouse', name: '仓库管理'},
      { key: '/goods/classification', name: '产品分类' },
      { key: '/goods/information', name: '产品信息' },
      { key: '/basicData/settlement_account', name: '结算账户'},

    ]
  },

  {
    key: '4', name: '采购管理', icon: 'shopping-cart', submenus: [
      { key: '/purchasing/purchase_create', name: '采购订单' },
      { key: '/purchasing/purchase_record', name: '采购记录' },
      { key: '/purchasing/purchase_return_create', name: '采购退货' },
      { key: '/purchasing/return_record', name: '退货记录' },
    ]
  },
  {
    key: '5', name: '销售管理', icon: 'shopping', submenus: [
      // { key: '/sale/sale_predict',name:'销售计划'},
      { key: '/sale/sale_create', name: '销售订单' },
      { key: '/sale/sale_record', name: '销售记录' },
      { key: '/sale/sale_return_create', name: '销售退货' },
      { key: '/sale/sale_return_record', name: '退货记录' },
    ]
  },
  {
    key: '7', name: '库存管理', icon: 'database', submenus: [
      { key: '/warehouse/inStock', name: '入库业务' },
      { key: '/warehouse/outStock', name: '出库业务' },
      { key: '/warehouse/inventory', name: '盘点业务' },
      { key: '/warehouse/allocation', name: '调拨业务' },
      { key: '/warehouse/flow', name: '库存结存' },
    ]
  },



  {
    key: '8', name: '往来管理', icon: 'dollar', submenus: [
      { key: '/finance/arrears_payable', name: '应付账款' },
      { key: '/finance/payment', name: '付款业务' },
      { key: '/finance/arrears_receivable', name: '应收账款' },
      { key: '/finance/collection', name: '收款业务' },
    ]
  },
  {
    key: '1', name: '报表统计', icon: 'line-chart', submenus: [
      { key: '/report/purchase_report', name: '采购报表' },
      { key: '/report/sale_report', name: '销售报表' },
      { key: '/report/stock_report', name: '库存报表' },
      { key: '/report/income_expense_statistics', name: '收支统计' },

    ]
  },
  {
    key: '9', name: '系统管理', icon: 'team', submenus: [
      { key: '/role', name: '角色管理' },
      { key: '/account', name: '用户管理' },

    ]
  },
]