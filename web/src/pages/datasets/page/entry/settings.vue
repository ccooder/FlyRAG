<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 16:59:22
 * @LastEditTime: 2025-07-30 15:00:14
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\settings.vue
 * Copyright 版权声明
-->
<template>
  <div class="pageWrap">
    <ManageLeft></ManageLeft>
    <div class="pageWrap-main">
      <h2 class="title">
        知识库设置
      </h2>
      
      <a-tabs v-model:activeKey="activeKey">
        <a-tab-pane key="1" tab="切片配置">
          <ChunkConfig :kbId="kbId"></ChunkConfig>
        </a-tab-pane>
        <a-tab-pane key="2" tab="检索配置" force-render>
          <RetrivalConfig :kbId="kbId"></RetrivalConfig>
        </a-tab-pane>
      </a-tabs>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ManageLeft from './components/ManageLeft.vue'
import ChunkConfig from './components/Settings/ChunkConfig.vue'
import RetrivalConfig from './components/Settings/RetrivalConfig.vue'

const activeKey = ref('1')

const props = defineProps({
  kbId: {
    type: String,
    required: true
  }
})
// 生命周期
onMounted(() => {
})

</script>

<style lang="scss" scoped>
@import url('../../styles/manage.scss');
</style>

