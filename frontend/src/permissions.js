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