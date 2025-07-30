/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 15:50:15
 * @LastEditTime: 2025-07-29 09:13:26
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: AI助手相关接口
 * @FilePath: \FlyRAG\web\src\api\chat.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

/**
 * @description 获取token
 */
export function gettoken(params) {
  const data = params
  return request({
    url: `http://192.168.28.245:7788/aichat/gettoken`,
    method: 'post',
    config: {
      responseInterceptor: false
    },
    data
  })
}

/**
 * @description AI助手 对话
 */
export function aiChat(params) {
  const data = params
  return request({
    url: `http://192.168.28.245:7788/aichat/sendmessage2ai`,
    method: 'post',
    config: {
      responseInterceptor: false
    },
    data
  })
}