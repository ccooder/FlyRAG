/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 16:59:36
 * @LastEditTime: 2025-07-24 14:22:11
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\api\documents.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

// 文档 列表
export function getList(params = {}, query = {}) {
  const data = params
  return request({
    url: '/document/list',
    method: 'post',
    data,
    params: query
  })
}

// 文档 详情
export function getDetail(params = {}) {
  return request({
    url: '/document/fetch',
    method: 'get',
    params
  })
}

// 文档 创建
export function saveCreate(params = {}) {
  const data = params
  return request({
    url: '/document/create',
    method: 'post',
    data
  })
}

// 文档 修改
export function saveUpdate(params = {}) {
  const data = params
  return request({
    url: '/document/update',
    method: 'post',
    data
  })
}

// 文档 删除
export function saveDelete(params = {}) {
  const data = params
  return request({
    url: '/document/delete',
    method: 'post',
    data
  })
}

// 恢复暂停的文档
export function saveResume(params = {}) {
  return request({
    url: '/document/resume',
    method: 'post',
    params
  })
}

// 暂停索引中的文档
export function savePause(params = {}) {
  return request({
    url: '/document/pause',
    method: 'post',
    params
  })
}

// 段落列表
export function getChunkList(params = {}, query = {}) {
  return request({
    url: '/chunk/list',
    method: 'post',
    data: params,
    params: query
  })
}

// 段落 启用/禁用
export function getChunkToggle(params = {}) {
  return request({
    url: '/chunk/toggle',
    method: 'post',
    params
  })
}