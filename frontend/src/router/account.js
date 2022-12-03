export default {
  path: '/',
  name: 'account',
  component: () => import('@/layouts/BaseLayout'),
  children: [
    {
      path: 'role',
      name: 'role',
      meta: { title: '角色管理', permission: 'role' },
      component: () => import('@/views/role/Role'),
    },
    {
      path: 'account',
      name: 'account', 
      meta: { title: '账号管理', permission: 'account' },
      component: () => import('@/views/account/Account'),
    },
    {
      path: 'config',
      name: 'config', 
      meta: { title: '系统配置', permission: 'config' },
      component: () => import('@/views/config/Config'),
    },
  ],
}