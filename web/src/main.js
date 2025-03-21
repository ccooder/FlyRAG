/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-17 11:25:51
 * @LastEditTime: 2025-03-17 12:35:33
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\main.js
 * @Copyright 版权声明
 */
import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import './styles/index.scss'
import App from './App.vue'

// 路由
import router from './router/index.js'

createApp(App)
  .use(Antd)
  .use(router)
  .mount('#app')
