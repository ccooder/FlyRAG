/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-04 23:32:23
 * @LastEditTime: 2025-03-17 15:31:30
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 路由
 * @FilePath: \FlyRAG\web\src\router\index.js
 * @Copyright 版权声明
 */
import { createRouter, createWebHashHistory } from 'vue-router'

// Layout
const Layout = () => import('@/layouts/desk/index.vue')

import DeskRoutes from './modules/desk.js'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/datasets',
    name: 'DeskLayout',
    hidden: false,
    meta: {
      top: true
    },
    children: [
      ...DeskRoutes
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export const constantRouterMap = routes

export default router
