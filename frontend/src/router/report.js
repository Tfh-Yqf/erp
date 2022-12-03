export default {
  path: '/report',
  name: 'report',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/report/sale_report',
  children: [
    {
      path: 'sale_report',
      meta: { title: '销售报表', permission: 'sale_report' },
      component: () => import('@/views/report/saleReport/index'),
    },
    {
      path: 'purchase_report',
      meta: { title: '采购报表', permission: 'purchase_report' },
      component: () => import('@/views/report/purchaseReport/index'),
    },
    {
      path: 'stock_report',
      meta: { title: '库存报表', permission: 'stock_report' },
      component: () => import('@/views/report/stockReport/index'),
    },
    {
      path: 'income_expense_statistics',
      meta: { title: '收支统计', permission: 'income_expense_statistics' },
      component: () => import('@/views/report/incomeExpenseStatistics/index'),
    },
    {
      path: 'batch_report',
      meta: { title: '批次报表', permission: 'batch_report' },
      component: () => import('@/views/report/batchReport/index'),
    },
  ],
}