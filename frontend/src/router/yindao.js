export default {
    path: '/yindao',
    name: 'yindao',
    component: () => import('@/layouts/YinDaoYe'),
    children: [
        {
            path: 'login',
            name: 'login',
            meta: { title: '登录' },
            component: () => import('@/views/login/Login'),
        },
        {
            path: 'yindao',
            name: 'yindao',
            meta: { title: '引导页' },
            component: () => import('@/layouts/YinDaoYe'),
        },
        {
            path: 'set_password',
            name: 'setPassword',
            meta: { title: '设置密码' },
            component: () => import('@/views/setPassword/SetPassword'),
        },
    ],
}