/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 15:50:15
 * @LastEditTime: 2025-03-24 16:35:24
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 模型相关接口
 * @FilePath: \FlyRAG\web\src\api\mode.js
 * @Copyright 版权声明
 */
import request from '@/utils/request'

/*
 * 获取模型列表
 * type { String } 1: LLM 2: Embedding 3: Reranker
 */
export function getList(params = {}) {
  const data = params
  return request({
    url: '/model/list',
    method: 'post',
    data
  })
}