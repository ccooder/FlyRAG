/*
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 13:49:12
 * @LastEditTime: 2025-03-24 17:06:49
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\router\modules\desk.js
 * @Copyright 版权声明
 */
export default [
  // {
  //   path: '/home',
  //   name: 'Home',
  //   component: () => import('@/pages/Home/page/entry/index.vue'),
  //   meta: {
  //     title: '知识库'
  //   }
  // },
  {
    path: '/datasets',
    name: 'Datasets',
    component: () => import('@/pages/datasets/page/entry/index.vue'),
    meta: {
      title: '知识库'
    },
    children: [
    ]
  },
  {
    path: '/datasets/:kbId/settings',
    props: true,
    name: 'DatasetsSettings',
    component: () => import('@/pages/datasets/page/entry/settings.vue'),
    hidden: true,
    meta: {
      title: '知识库 - 知识库 - 设置'
    }
  },
  {
    path: '/datasets/:kbId/documents',
    props: true,
    name: 'DatasetsDocuments',
    component: () => import('@/pages/datasets/page/entry/documents.vue'),
    hidden: true,
    meta: {
      title: '知识库 - 文档管理'
    }
  },
  {
    path: '/datasets/:kbId/documents/:docId/settings',
    props: true,
    name: 'DatasetsDocumentsSettings',
    component: () => import('@/pages/datasets/page/entry/documentsSettings.vue'),
    hidden: true,
    meta: {
      title: '知识库 - 文档管理 - 文档设置'
    }
  }
]