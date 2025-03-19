<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 00:08:18
 * @LastEditTime: 2025-03-17 17:12:51
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 知识库管理
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\index.vue
 * Copyright 版权声明
-->
<template>
  <div class="handleWrap">
    <a-button type="primary" @click="handleCreate">
      <template #icon>
        <PlusOutlined />
      </template>
      创建知识库
    </a-button>
  </div>
  <div class="projectList">
    <a-row :gutter="16">
      <a-col class="gutter-row" :span="6" v-for="item in 10" :key="item">
        <a-card hoverable>
          <h2 class="name">知识库名称</h2>
          <div class="desc">
            知识库描述
          </div>
          <p class="info">
            1 文档 . 244 千字符
          </p>
          <!-- <p class="date">
            2024年6月3日
          </p> -->
          <template #actions>
            <!-- <setting-outlined key="setting" title="知识库管理" @click="handleClickSiteManage"/> -->
            <edit-outlined key="edit" title="编辑" @click="handleUpdate(item)"/>
            <a-popconfirm
              title="您确定要删除吗？"
              @confirm="onConfirmDelete"
            >
              <DeleteOutlined key="delete" title="删除" />
            </a-popconfirm>
          </template>
        </a-card>
      </a-col>
    </a-row>
  </div>
  <CreateDrawer ref="CreateDrawerRef"></CreateDrawer>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { PlusOutlined, SettingOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import CreateDrawer from './components/CreateDrawer.vue'

const router = useRouter()

const CreateDrawerRef = ref(null)

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
const onConfirmDelete = (row) => {
}

// 管理站点
const handleClickSiteManage = () => {
  // router.push({
  //   name: 'ProjectSite'
  // })
}

</script>

<style lang="scss" scoped>
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

