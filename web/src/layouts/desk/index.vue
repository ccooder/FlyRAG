<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 10:00:12
 * @LastEditTime: 2025-03-20 15:17:29
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\layouts\desk\index.vue
 * Copyright 版权声明
-->
<template>
  <a-layout>
    <a-layout-header :style="{ position: 'fixed', zIndex: 1, width: '100%' }">
      <div class="logo" />
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        @click="handleClickMenu"
      >
        <template v-for="item in DeskRoutes">
          <a-menu-item v-if="item.hidden !== true" :key="item.path">
            {{ item.meta.title || '' }}
          </a-menu-item>
        </template>
      </a-menu>
    </a-layout-header>
    <a-layout-content class="customScrollBar" :style="{ padding: '0 0 0 0', marginTop: '64px', height: 'calc(100vh - 64px)' }">
      <!-- <a-breadcrumb :style="{ margin: '16px 0' }">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>List</a-breadcrumb-item>
        <a-breadcrumb-item>App</a-breadcrumb-item>
      </a-breadcrumb> -->
      <!--, minHeight: 'calc(100vh - 199px)'-->
      <!-- <div :style="{ background: '#fff', padding: '24px', marginTop: '24px' }"> -->
      <div :style="{ marginTop: '0' }">
        <router-view></router-view>
      </div>
    </a-layout-content>
    <!--<a-layout-footer :style="{ textAlign: 'center' }">
      Ant Design ©2018 Created by Ant UED
    </a-layout-footer>-->
  </a-layout>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  import DeskRoutes from '@/router/modules/desk.js'

  const router = useRouter()
  
  const selectedKeys = ref([DeskRoutes[0].path])

  // 点击菜单
  const handleClickMenu = (e) => {
    const { key } = e
    selectedKeys.value = [key]
    router.push({
      path: key
    })
  }
</script>