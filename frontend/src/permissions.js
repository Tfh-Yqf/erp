export let permissions = {
  'role': '角色管理',
  'account': '账号管理',
  'warehouse': '仓库管理',
  'stock_location': '库位管理',
  'client': '往来单位',
  'unit': '单位管理',
  'material': '产品管理',
  'material_batch': '产品批次',
  'stock_in': '入库',
  'stock_out': '出库',
  'stock_check': '盘点',
  'stock_transfer': '调拨',
  'config': '功能配置',
  'order_prefix': '单据字头',
  'inventory': '库存信息',
  'flow': '出入库历史',
  'stock_check':'盘点业务'
}

export let permissionsTree = [
  {
    title: '系统管理',
    value: '0',
    key: '0',
    children: [
      {
        title: '角色管理',
        value: 'role',
        key: 'role',
      },
      {
        title: '账号管理',
        value: 'account',
        key: 'account',
      },
      {
        title: '功能配置',
        value: 'config',
        key: 'config',
      },
      {
        title: '单据字头',
        value: 'order_prefix',
        key: 'order_prefix',
      },
    ],
  },
  {
    title: '主数据管理',
    value: '1',
    key: '1',
    children: [
      {
        title: '仓库管理',
        value: 'warehouse',
        key: 'warehouse',
      },
      {
        title: '库位管理',
        value: 'stock_location',
        key: 'stock_location',
      },
      {
        title: '往来单位',
        value: 'client',
        key: 'client',
      },
      {
        title: '单位管理',
        value: 'unit',
        key: 'unit',
      },
      {
        title: '产品管理',
        value: 'material',
        key: 'material',
      },
      {
        title: '产品批次',
        value: 'material_batch',
        key: 'material_batch',
      },
    ],
  },
  {
    title: '出入库作业',
    value: '2',
    key: '2',
    children: [
      {
        title: '出库',
        value: 'stock_out',
        key: 'stock_out',
      },
      {
        title: '入库',
        value: 'stock_in',
        key: 'stock_in',
      },
    ],
  },
  {
    title: '其他作业',
    value: '3',
    key: '3',
    children: [
      {
        title: '盘点',
        value: 'stock_check',
        key: 'stock_check',
      },
      {
        title: '调拨',
        value: 'stock_transfer',
        key: 'stock_transfer',
      },
    ],
  },
  {
    title: '报表',
    value: '4',
    key: '4',
    children: [
      {
        title: '库存信息',
        value: 'inventory',
        key: 'inventory',
      },
      {
        title: '出入库历史',
        value: 'flow',
        key: 'flow',
      },
    ],
  },
]


export let permission_groups = [
  {
      "id": 1,
      "name": "数据看板",
      "permission_items": [
          {
              "id": 1,
              "name": "销售走势",
              "code": "sales_trend"
          },
          {
              "id": 2,
              "name": "销售前十产品",
              "code": "sales_hot_goods"
          },
          {
              "id": 3,
              "name": "订单收款明细",
              "code": "stock_in_reminder"
          }
      ]
  },
  {
      "id": 2,
      "name": "报表统计",
      "permission_items": [
          {
              "id": 6,
              "name": "销售报表",
              "code": "sales_report"
          },
          {
              "id": 7,
              "name": "采购报表",
              "code": "purchase_report"
          },
          {
              "id": 8,
              "name": "库存报表",
              "code": "inventory"
          },

          {
              "id": 10,
              "name": "收支统计",
              "code": "finance_statistic"
          }
      ]
  },
  {
      "id": 3,
      "name": "基础档案",
      "permission_items": [
          {
              "id": 11,
              "name": "客户管理",
              "code": "client"
          },
          {
              "id": 12,
              "name": "供应商管理",
              "code": "supplier"
          },
          {
              "id": 13,
              "name": "仓库管理",
              "code": "warehouse"
          },
          {
              "id": 14,
              "name": "结算账户",
              "code": "account"
          },
          {
              "id": 15,
              "name": "结算账户",
              "code": "charge_item"
          }
      ]
  },
  
  {
      "id": 5,
      "name": "采购管理",
      "permission_items": [
          {
              "id": 19,
              "name": "采购订单",
              "code": "purchase_order"
          },
          {
              "id": 20,
              "name": "采购退货",
              "code": "purchase_return_order"
          }
      ]
  },
  {
      "id": 6,
      "name": "销售管理",
      "permission_items": [
          {
              "id": 21,
              "name": "销售订单",
              "code": "sales_order"
          },
          {
              "id": 22,
              "name": "销售退货",
              "code": "sales_return_order"
          }
      ]
  },

  {
      "id": 8,
      "name": "库存管理",
      "permission_items": [
          {
              "id": 25,
              "name": "入库业务",
              "code": "stock_in"
          },
          {
              "id": 26,
              "name": "出库业务",
              "code": "stock_out"
          },
          {
              "id": 27,
              "name": "盘点业务",
              "code": "stock_check"
          },
          {
              "id": 28,
              "name": "调拨业务",
              "code": "stock_transfer"
          },
          {
            "id": 29,
            "name": "库存结存",
            "code": "inventory_flow"
        },
      ] 
  },
  {
      "id": 9,
      "name": "往来管理",
      "permission_items": [
          {
              "id": 30,
              "name": "应付账款",
              "code": "supplier_arrears"
          },
          {
              "id": 31,
              "name": "付款业务",
              "code": "payment_order"
          },
          {
              "id": 32,
              "name": "应收账款",
              "code": "client_arrears"
          },
          {
              "id": 33,
              "name": "收款业务",
              "code": "collection_order"
          },

          {
              "id": 36,
              "name": "资金流水",
              "code": "finance_flow"
          }
      ]
  }
]