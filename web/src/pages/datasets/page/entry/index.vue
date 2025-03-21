<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 00:08:18
 * @LastEditTime: 2025-03-20 17:16:11
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 知识库管理
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\index.vue
 * Copyright 版权声明
-->
<template>
  <div class="pageWrap">
    <div class="handleWrap">
      <a-button type="primary" @click="handleCreate">
        <template #icon>
          <PlusOutlined />
        </template>
        创建知识库
      </a-button>
    </div>
    <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
      <div class="projectList" v-if="listState.data.length > 0">
        <a-row :gutter="16">
          <a-col class="gutter-row" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 12}" :lg="{span: 12}" :xl="{span: 8}" :xxl="{span: 6}" v-for="(item, index) in listState.data" :key="index">
            <a-card hoverable>
              <h2 class="name">
                <span class="icon" style="border: 1px solid rgb(224 234 255);border-radius:5px;margin-right: 5px;background-color: rgb(245 248 255); display: inline-block;width: 32px;height: 32px;line-height:32px;text-align: center;">
                  <FolderOutlined style="color: rgb(68 76 231);" />
                </span>
                {{item.name}}
              </h2>
              <div class="desc">
                {{item.profile}}
              </div>
              <p class="info">
                <a-tag color="#87d068" v-if="item.status === 1">启用</a-tag>
                <a-tag color="#f50" v-if="item.status === 0">禁用</a-tag>
                <!-- 1 文档 . 244 千字符 -->
              </p>
              <!-- <p class="date">
                2024年6月3日
              </p> -->
              <template #actions>
                <setting-outlined key="setting" title="知识库管理" @click="handleClickManage(item)"/>
                <edit-outlined key="edit" title="编辑" @click="handleUpdate(item)"/>
                <a-popconfirm
                  title="您确定要删除吗？"
                  @confirm="onConfirmDelete(item)"
                >
                  <DeleteOutlined key="delete" title="删除" />
                </a-popconfirm>
              </template>
            </a-card>
          </a-col>
        </a-row>
      </div>
      <div v-else style="padding: 30px 0;background-color: #fff;">
        <a-empty />
      </div>
    </a-spin>
  </div>
  <CreateDrawer ref="CreateDrawerRef" @close="loadData"></CreateDrawer>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusOutlined, SettingOutlined, EditOutlined, DeleteOutlined, FolderOutlined } from '@ant-design/icons-vue'
import CreateDrawer from './components/CreateDrawer.vue'
import { message } from 'ant-design-vue'

import { getList, saveDelete } from '@/api/kb'

const router = useRouter()

// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

const CreateDrawerRef = ref(null)

// 列表状态
const listState = reactive(
  {
    data: [],
    query: {
      current: 1,
      size: 10
    }
  }
)

// 创建知识库
const handleCreate = () => {
  if (CreateDrawerRef.value) {
    CreateDrawerRef.value.onShow({
      type: 'create'
    })
  }
}

// 编辑知识库
const handleUpdate = (row) => {
  if (CreateDrawerRef.value) {
    CreateDrawerRef.value.onShow({
      type: 'update',
      row
    })
  }
}

// 删除知识库
const onConfirmDelete = async (row) => {
  await saveDelete({
    id: row.id
  })
  message.success(`删除成功`)
  loadData()
}

// 管理知识库
const handleClickManage = (item) => {
  router.push({
    // path: `/datasets/${item.id}/documents`
    name: 'DatasetsDocuments',
    params: {
      kbId: item.id
    }
  })
}

// 加载数据
const loadData = async () => {
  spinningConfig.spinning = true
  try {
    const res = await getList()
    listState.data = res?.data??[]
    spinningConfig.spinning = false
  } catch (error) {
    spinningConfig.spinning = false
  }
}

// 生命周期
onMounted(() => {
  loadData()
})

</script>

<style lang="scss" scoped>
.pageWrap{
  padding: 24px;
}
.handleWrap{
  margin-bottom: 8px;
  display: flex;
  justify-content: flex-end;
}
.projectList{
  .gutter-row{
    margin: 8px 0;
    :deep(.ant-card-body){
      padding: 16px;
      .name{
        font-size: 16px;
        font-weight: bold;
      }
      .desc{
        font-size: 14px;
        color: #999;
        height: 46px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      p{
        // margin-bottom: 8px;
        margin-bottom: 0;
      }
      .date{
        color: #999;
      }
    }
  }
}
</style>

