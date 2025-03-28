/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-19 16:31:22
 * @LastEditTime: 2025-03-20 17:00:31
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

// 知识库 详情
export function getDetail(params = {}) {
  return request({
    url: '/kb/fetch',
    method: 'get',
    params
  })
}

// 知识库 创建
export function saveCreate(params = {}) {
  const data = params
  return request({
    url: '/kb/create',
    method: 'post',
    data
  })
}

// 知识库 修改
export function saveUpdate(params = {}) {
  const data = params
  return request({
    url: '/kb/update',
    method: 'post',
    data
  })
}

// 知识库 删除
export function saveDelete(params = {}) {
  const data = params
  return request({
    url: '/kb/delete',
    method: 'post',
    data
  })
}

// 上传文件
export function uploadDoc(params = {}) {
  const data = params
  return request({
    url: '/file/upload',
    method: 'post',
    // responseType: 'blob',
    data
  })
}