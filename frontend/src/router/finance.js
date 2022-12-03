export default {
  path: '/finance',
  name: 'finance',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/finance/flow',
  children: [
    {
      path: 'payment',
      meta: { title: '付款', permission: 'payment' },
      component: () => import('@/views/finance/payment/index'),
    },
    {
      path: 'payment_create',
      meta: { title: '付款新增', permission: 'payment_create' },
      component: () => import('@/views/finance/paymentCreate/index'),
    },
    {
      path: 'payment_detail',
      meta: { title: '付款详情', permission: 'payment_detail' },
      component: () => import('@/views/finance/paymentDetail/index'),
    },
    {
      path: 'collection',
      meta: { title: '收款', permission: 'collection' },
      component: () => import('@/views/finance/collection/index'),
    },
    {
      path: 'collection_create',
      meta: { title: '收款新增', permission: 'collection_create' },
      component: () => import('@/views/finance/collectionCreate/index'),
    },
    {
      path: 'collection_detail',
      meta: { title: '收款详情', permission: 'collection_detail' },
      component: () => import('@/views/finance/collectionDetail/index'),
    },
    {
      path: 'arrears_payable',
      meta: { title: '应付欠款', permission: 'arrears_payable' },
      component: () => import('@/views/finance/arrearsPayable/index'),
    },
    {
      path: 'arrears_payable_detail',
      meta: { title: '应付欠款详情', permission: 'arrears_payable_detail' },
      component: () => import('@/views/finance/arrearsPayableDetail/index'),
    },
    {
      path: 'arrears_receivable',
      meta: { title: '应收欠款', permission: 'arrears_receivable' },
      component: () => import('@/views/finance/arrearsReceivable/index'),
    },
    {
      path: 'arrears_receivable_detail',
      meta: { title: '应收欠款详情', permission: 'arrears_receivable_detail' },
      component: () => import('@/views/finance/arrearsReceivableDetail/index'),
    },
    {
      path: 'account_transfer',
      meta: { title: '账户转账', permission: 'account_transfer' },
      component: () => import('@/views/finance/accountTransfer/index'),
    },
    {
      path: 'income_and_pay',
      meta: { title: '日常收支', permission: 'income_and_pay' },
      component: () => import('@/views/finance/incomeAndPay/index'),
    },
    {
      path: 'flow',
      meta: { title: '资金流水', permission: 'flow' },
      component: () => import('@/views/finance/flow/index'),
    },
    {
      path: 'flow_detail',
      meta: { title: '资金流水详情', permission: 'flow_detail' },
      component: () => import('@/views/finance/flowDetail/index'),
    },
    // {
    //   path: 'purchase_statement',
    //   meta: { title: '采购对账单', permission: 'purchase_statement' },
    //   component: () => import('@/views/finance/purchaseStatement/index'),
    // },
    // {
    //   path: 'transaction_record',
    //   meta: { title: '往来记录', permission: 'transaction_record' },
    //   component: () => import('@/views/finance/transactionRecord/index'),
    // },
    // {
    //   path: 'sales_statement',
    //   meta: { title: '销售对账单', permission: 'sales_statement' },
    //   component: () => import('@/views/finance/salesStatement/index'),
    // },
  ],
}