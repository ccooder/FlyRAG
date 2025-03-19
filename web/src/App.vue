<template>
  <a-config-provider
    :locale="locale"
    :theme="{
      token: {
        // colorPrimary: '#000',
      },
    }"
  >
    <router-view></router-view>
  </a-config-provider>
</template>

<script setup>
import zhCN from 'ant-design-vue/es/locale/zh_CN'
const locale = zhCN
</script>

<style scoped>
</style>
