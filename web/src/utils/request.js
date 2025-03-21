/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-19 16:25:23
 * @LastEditTime: 2025-03-19 17:17:35
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\utils\request.js
 * @Copyright 版权声明
 */
import axios from 'axios'
import { message } from 'ant-design-vue'

// 创建axios实例
const service = axios.create({
  baseURL: 'https://flyrag.loophole.site', // api的base_url
  withCredentials: true,
  timeout: 50000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// respone拦截器
service.interceptors.response.use(
  (response) => {
    /**
     * resType 可结合自己业务进行修改
     */
    const res = response?.data
    if (typeof res.code === 'undefined') {
      return Promise.resolve(response)
    }
    if (res.code === 200) {
      return Promise.resolve(response.data)
    } else {
      if (!response.config.headers['Error-Echo']) {
        message.error(res.msg)
      }
      return Promise.reject(response.data)
    }
  },
  (error) => {
    console.log('err' + error) // for debug
    message.error(error.message)
    return Promise.reject(error)
  }
)

export default service
