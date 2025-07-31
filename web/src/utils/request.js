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

// 请求额外配置参数默认值
const CONFIG_DEFAULT = {
  // 入参headers不携带token
  noToken: false,
  // 出参拦截器处理拦截异常但不在页面输出错误信息
  errorEcho: true,
  // 出参返回整个请求体所有参数和数据
  responseAll: false,
  // 拦截器Loading  - 局部控制
  needLoading: false,
  // 出参异常是否拦截
  responseInterceptor: true
}

// 创建axios实例
const service = axios.create({
  baseURL: 'https://flyrag.loophole.site', // api的base_url
  withCredentials: true,
  timeout: 50000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  (config) => {
    config.config = Object.assign({}, CONFIG_DEFAULT, config.config)
    const extConfig = config.config
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
    const extConfig = response.config.config || {}
    /**
     * resType 可结合自己业务进行修改
     */
    const res = response?.data
    // 不做出参异常拦截
    if (extConfig.responseInterceptor === false) {
      return Promise.resolve(extConfig.responseAll === true ? response : res)
    }
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
