<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 16:59:22
 * @LastEditTime: 2025-07-30 15:53:49
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\components\Settings\RetrivalConfig.vue
 * Copyright 版权声明
-->
<template>

  <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
    
    <!-- layout="vertical" -->
    <a-form
      ref="formRef"
      name="custom-validation"
      :model="formData"
      :rules="rules"
      v-bind="{
        labelCol: { span: 3 },
        wrapperCol: { span: 10 }
      }"
    >
      <a-form-item has-feedback label="检索模式" name="mode">
        <a-select
          v-model:value="formData.mode"
          placeholder="请选择检索模式"
        >
          <a-select-option :value="2">混合模式</a-select-option>
          <a-select-option :value="1">打分调序</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item has-feedback label="重排序模型" name="reranker_model_id">
        <a-select
          v-model:value="formData.reranker_model_id"
          placeholder="请选择重排序模型"
          :options="modeList"
          :field-names="{ label: 'name', value: 'id', options: 'children' }"
        >
        </a-select>
      </a-form-item>
      <a-form-item has-feedback label="检索取前K个" name="top_k">
        <a-input v-model:value="formData.top_k" placeholder="取值范围 1-10" />
      </a-form-item>
      <a-form-item has-feedback label="重排序后取前N个" name="top_n">
        <a-input v-model:value="formData.top_n" placeholder="取值范围 1-5" />
      </a-form-item>
      <a-form-item has-feedback label="Score阈值" name="score">
        <a-input v-model:value="formData.score" placeholder="0 表示无阈值，取值范围 0-1" />
      </a-form-item>
      <a-form-item label=" " :colon="false">
        <a-space>
          <!-- <a-button type="default" @click="router.back()">
            <SwapLeftOutlined />
            上一步
          </a-button> -->
          <a-button type="primary" @click="onSubmit">
            保存
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </a-spin>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  SwapLeftOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

import { getList as getModeList } from '@/api/mode'
import { getDetail, saveCreate } from '@/api/retrivalConfig'

const formRef = ref(null)

const props = defineProps({
  kbId: {
    type: String,
    required: true
  }
})

const rules = {
  reranker_model_id: [{ required: true, message: '请选择重排序模型', trigger: 'change' }],
  mode: [{ required: true, message: '请选择检索模式', trigger: 'change' }],
  top_k: [{ required: true, message: '请输入检索取前K个', trigger: 'change' }],
  top_n: [{ required: true, message: '请输入重排序后取前N个', trigger: 'change' }],
  score: [{ required: true, message: '请输入Score阈值', trigger: 'change' }]
}
const formData = ref({
  kb_id: props.kbId, // 目标ID，文档或知识库
  reranker_model_id: '', // 重排序模型
  mode: 2, // 检索模式 1: RAGFusion 2: Mixed
  top_n: '', // 重排序后取前N个
  score: '', // Score阈值 - 0 表示无阈值 取值范围 0-1
  top_k: '' // 检索取前K个
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
      kb_id: props.kbId
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
        subData.kb_id = props.kbId
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
</style>

