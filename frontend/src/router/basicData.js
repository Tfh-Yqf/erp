export default {
  path: '/basicData',
  name: 'basicData',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/basicData/client_classification',
  children: [
    {
      path: 'client',
      meta: { title: '客户', permission: 'client' },
      component: () => import('@/views/basicData/client/index'),
    },
    {
      path: 'supplier',
      meta: { title: '供应商', permission: 'supplier' },
      component: () => import('@/views/basicData/supplier/index'),
    },
    {
      path: 'warehouse',
      meta: { title: '仓库', permission: 'warehouse' },
      component: () => import('@/views/basicData/warehouse/index'),
    },
    {
      path: 'settlement_account',
      meta: { title: '结算账户', permission: 'settlement_account' },
      component: () => import('@/views/basicData/settlementAccount/index'),
    },
    {
      path: 'revenue_expenditure_items',
      meta: { title: ' 收支项目', permission: 'revenue_expenditure_items' },
      component: () => import('@/views/basicData/revenueExpenditureItems/index'),
    },
  ],
}