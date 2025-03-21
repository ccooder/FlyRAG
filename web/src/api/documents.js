/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 16:59:36
 * @LastEditTime: 2025-03-20 17:05:29
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\api\documents.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

// 知识库 列表
export function getList(params = {}) {
  const data = params
  return request({
    url: '/document/list',
    method: 'post',
    data
  })
}

// 知识库 详情
export function getDetail(params = {}) {
  return request({
    url: '/document/fetch',
    method: 'get',
    params
  })
}

// 知识库 创建
export function saveCreate(params = {}) {
  const data = params
  return request({
    url: '/document/create',
    method: 'post',
    data
  })
}

// 知识库 修改
export function saveUpdate(params = {}) {
  const data = params
  return request({
    url: '/document/update',
    method: 'post',
    data
  })
}

// 知识库 删除
export function saveDelete(params = {}) {
  const data = params
  return request({
    url: '/document/delete',
    method: 'post',
    data
  })
}