<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 15:36:08
 * @LastEditTime: 2025-03-24 17:17:48
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\components\ManageLeft.vue
 * Copyright 版权声明
-->
<template>
  <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
    <div class="pageWrap-left">
      <div class="pageInfo">
        <h2 class="name">
          {{detailData.name}}
        </h2>
        <p class="desc">
          {{detailData.profile}}
        </p>
        <p class="desc">
          更新时间：{{detailData.update_time}}
        </p>
      </div>
      <div class="pageMenu">
        <a-menu
          v-model:openKeys="openKeys"
          v-model:selectedKeys="selectedKeys"
          mode="vertical"
          :items="items"
          @click="handleClick"
        />
      </div>
    </div>
  </a-spin>
</template>

<script setup name="CreateDrawer">
import { h, ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  PlusOutlined,
  SettingOutlined,
  MailOutlined,
  CalendarOutlined,
  AppstoreOutlined
} from '@ant-design/icons-vue'

import { getDetail } from '@/api/kb'

const router = useRouter()
const route = useRoute()

const selectedKeys = ref(['DatasetsDocuments']);
const openKeys = ref([]);
const items = ref([
  {
    key: 'DatasetsDocuments',
    icon: () => h(MailOutlined),
    label: '文档',
    title: '文档',
  },
  // {
  //   key: 'hitTesting',
  //   icon: () => h(CalendarOutlined),
  //   label: '召回测试',
  //   title: '召回测试',
  // },
  {
    key: 'DatasetsSettings',
    icon: () => h(SettingOutlined),
    label: '设置',
    title: '设置',
  }
])
const handleClick = menuInfo => {
  router.push({
    name: menuInfo.key,
    params: {
      kbId: route.params.kbId
    }
  })
}


// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

const detailData = ref({})
const kbId = ref('')

// 加载数据
const loadData = async () => {
  spinningConfig.spinning = true
  try {
    const res = await getDetail({
      id: kbId.value??''
    })
    detailData.value = res?.data??{}
    spinningConfig.spinning = false
  } catch (error) {
    spinningConfig.spinning = false
  }
}

onMounted(() => {
  switch (route.name) {
    case 'DatasetsDocumentsSettings':
      selectedKeys.value = ['DatasetsDocuments']
      break
    default:
      selectedKeys.value = [route.name]
  }
  kbId.value = route.params.kbId??''
  loadData()
})
</script>

<style lang="scss" scoped>
.pageWrap-left{
  width: 220px;
  border-right: 1px solid #1018280a;
  padding: 16px;
  .pageInfo{
    border-bottom: 1px solid #1018280a;
    .name{
      font-size: 14px;
      font-weight: bold;
      margin-bottom: 16px;
    }
    .desc{
      font-size: 12px;
      color: #666;
    }
  }
  .pageMenu{
    padding: 12px 0;
    :where(.css-dev-only-do-not-override-1p3hq3p).ant-menu-light.ant-menu-root.ant-menu-inline, :where(.css-dev-only-do-not-override-1p3hq3p).ant-menu-light.ant-menu-root.ant-menu-vertical{
      border: none;
    }
  }
}
</style>

