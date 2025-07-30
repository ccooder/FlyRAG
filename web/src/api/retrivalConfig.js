/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 15:31:08
 * @LastEditTime: 2025-07-29 11:08:11
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 检索配置
 * @FilePath: \FlyRAG\web\src\api\retrivalConfig.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

// 保存配置
export function saveCreate(params = {}) {
  const data = params
  return request({
    url: '/retrival_config/submit',
    method: 'post',
    data
  })
}

// 获取配置
export function getDetail(params = {}) {
  return request({
    url: '/retrival_config/fetch',
    method: 'get',
    params
  })
}