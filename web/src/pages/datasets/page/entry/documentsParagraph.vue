<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-07-23 17:30:17
 * @LastEditTime: 2025-07-24 14:18:26
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\documentsParagraph.vue
 * Copyright 版权声明
-->
<template>
  <div class="pageWrap">
    <ManageLeft></ManageLeft>
    <div class="pageWrap-main">
      <h2 class="title">
        文档 - 分段
      </h2>
      <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
        <h3 class="totalH">{{ listState?.total }} 分段</h3>
        <a-list 
          item-layout="horizontal" 
          :data-source="listState.data" 
          :pagination="{ 
            current: listState.query.current, 
            pageSize: listState.query.size, 
            total: listState.total,
            onChange: (page, pageSize) => {
              listState.query.current = page
              listState.query.size = pageSize
              loadData()
            }
          }"
        >
          <template #renderItem="{ item }">
            <a-list-item>
              <a-list-item-meta
                :description="item?.chunk"
              >
              </a-list-item-meta>
              <template #actions>
                <a-button type="link" v-if="item.status === 0" @click="onSwitchStatus(item)">启用</a-button>
                <a-button type="link" v-if="item.status === 1" danger @click="onSwitchStatus(item)">禁用</a-button>
              </template>
            </a-list-item>
          </template>
        </a-list>
      </a-spin>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps } from 'vue'
import { useRouter } from 'vue-router'
import {
  SwapLeftOutlined
} from '@ant-design/icons-vue'
import ManageLeft from './components/ManageLeft.vue'
import { message } from 'ant-design-vue'

import { getChunkList, getChunkToggle } from '@/api/documents'

const formRef = ref(null)

const props = defineProps({
  kbId: {
    type: String,
    required: true
  },
  docId: {
    type: String,
    required: true
  }
})

const router = useRouter()

// 切换状态
const onSwitchStatus = async (item) => {
  try {
    await getChunkToggle({
      id: item.id
    })
    message.success('操作成功')
    loadData()
  } catch (error) {
    message.error('操作失败')
  }
}

// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

// 列表状态
const listState = reactive(
  {
    data: [],
    query: {
      current: 1,
      size: 5
    },
    total: 0
  }
)

// 加载数据
const loadData = async () => {
  spinningConfig.spinning = true
  try {
    const res = await getChunkList({
      doc_id: props.docId
    }, listState.query)
    listState.data = res?.data?.records??[]
    listState.total = res?.data?.total??0
    listState.forEach(item => {
      item.statusTemp = item.status
    })
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
@import url('../../styles/manage.scss');
.totalH{
  font-size: 16px;
  font-weight: bold;
  color: #333;
  padding: 8px 24px;
}
</style>

