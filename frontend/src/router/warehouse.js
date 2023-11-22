export default {
  path: '/warehouse',
  name: 'warehouse',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/warehouse/inStock',
  children: [
    {
      path: 'inStock',
      meta: { title: '入库任务', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStock/index'),
    },
    {
      path: 'inStock_create',
      meta: { title: '入库创建', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockCreate/index'),
    },
    {
      path: 'inStock_detail',
      meta: { title: '入库通知单详情', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockDetail/index'),
    },
    {
      path: 'inStock_record_detail',
      meta: { title: '入库记录详情', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockRecordDetail/index'),
    },
    {
      path: 'outStock',
      meta: { title: '出库任务', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStock/index'),
    },
    {
      path: 'outStock_create',
      meta: { title: '出库创建', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockCreate/index'),
    },
    {
      path: 'outStock_detail',
      meta: { title: '出库通知单详情', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockDetail/index'),
    },
    {
      path: 'outStock_record_detail',
      meta: { title: '出库记录详情', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockRecordDetail/index'),
    },
    {
      path: 'allocation',
      meta: { title: '调拨', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocation/index'),
    },
    {
      path: 'allocation_create',
      meta: { title: '调拨创建', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocationCreate/index'),
    },
    {
      path: 'allocationDetail_detail',
      meta: { title: '调拨单详情', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocationDetail/index'),
    },
    {
      path: 'inventory',
      meta: { title: '盘点', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventory/index'),
    },
    {
      path: 'inventory_create',
      meta: { title: '盘点创建', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventoryCreate/index'),
    },
    {
      path: 'inventory_detail',
      meta: { title: '盘点详情', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventoryDetail/index'),
    },
    {
      path: 'flow',
      meta: { title: '库存流水', permission: 'inventory_flow' },
      component: () => import('@/views/warehouse/flow/index'),
    },
    {
      path: 'flow_detail',
      meta: { title: '库存流水详情', permission: 'inventory_flow' },
      component: () => import('@/views/warehouse/flowDetail/index'),
    },
  ],
}