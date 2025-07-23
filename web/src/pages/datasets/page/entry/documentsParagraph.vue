<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-07-23 17:30:17
 * @LastEditTime: 2025-07-23 17:44:27
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
        文档 - 段落
      </h2>
      <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
        啊手动阀
        <!-- layout="vertical" -->
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

import { getList as getModeList } from '@/api/mode'
import { getDetail, saveCreate } from '@/api/chunkConfig'

const formRef = ref(null)

const props = defineProps({
  kbId: {
    type: String,
    required: true
  }
})
const formData = ref({
  target_id: props.kbId, // 目标ID，文档或知识库
  type: 1, // 1: 知识库 2: 文档
  embedding_model_id: '', // 向量模型
  mode: 1, // 分段模式 1: 通用 2: 父子 3: 混合
  chunk_size: '', // 分段最大长度
  chunk_overlap: '', // 分段重叠长度
  delimiters: '' // 分段标识符号
})

const router = useRouter()

// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

// 加载数据
const loadData = async () => {
  spinningConfig.spinning = true
  try {
    const res = await getDetail({
      target_id: props.kbId,
      type: 2
    })
    formData.value = Object.assign({}, formData.value, res?.data??{})
    spinningConfig.spinning = false
  } catch (error) {
    spinningConfig.spinning = false
  }
}

// 模型列表数据
const modeList = ref([])

// 获取模型列表
const getModeListData = async () => {
  try {
    const res = await getModeList({
      type: 2
    })
    modeList.value = res?.data?.records??[]

  } catch (error) {
  }
}

// 提交
const onSubmit = () => {
  formRef?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        const subData = JSON.parse(JSON.stringify(formData.value))
        subData.target_id = props.kbId
        subData.type = 1
        await saveCreate(subData)
        spinningConfig.spinning = false
        message.success(`配置文档成功`)
      } catch (error) {
        spinningConfig.spinning = false
      }
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 生命周期
onMounted(() => {
  getModeListData()
  loadData()
})

</script>

<style lang="scss" scoped>
@import url('../../styles/manage.scss');
</style>

