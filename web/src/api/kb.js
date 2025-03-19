/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-19 16:31:22
 * @LastEditTime: 2025-03-19 16:33:47
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 知识库接口
 * @FilePath: \FlyRAG\web\src\api\kb.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

// 知识库 列表
export function getList(params = {}) {
  const data = params
  return request({
    url: '/kb/list',
    method: 'post',
    data
  })
}