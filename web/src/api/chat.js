/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 15:50:15
 * @LastEditTime: 2025-07-30 17:31:24
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
    url: `http://localhost:5173/ragAPI/aichat/gettoken`,
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
  return `/ragAPI/aichat/sendmessage2ai`
  // const data = params
  // return request({
  //   url: `http://localhost:5173/ragAPI/aichat/sendmessage2ai`,
  //   method: 'post',
  //   config: {
  //     responseInterceptor: false
  //   },
  //   data
  // })
}