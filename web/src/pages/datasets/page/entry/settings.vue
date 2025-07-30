<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-24 16:59:22
 * @LastEditTime: 2025-07-23 15:35:04
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
      <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
        
        <!-- layout="vertical" -->
        <a-form
          ref="formRef"
          name="custom-validation"
          :model="formData"
          :rules="rules"
          v-bind="{
            labelCol: { span: 3 },
            wrapperCol: { span: 14 }
          }"
        >
          <a-form-item has-feedback label="向量模型" name="embedding_model_id">
            <a-select
              v-model:value="formData.embedding_model_id"
              placeholder="请选择向量模型"
              :options="modeList"
              :field-names="{ label: 'name', value: 'id', options: 'children' }"
            >
            </a-select>
          </a-form-item>
          <a-form-item has-feedback label="分段模式" name="mode">
            <a-select
              v-model:value="formData.mode"
              placeholder="请选择分段模式"
            >
              <a-select-option :value="1">通用</a-select-option>
              <a-select-option :value="2" disabled>父子</a-select-option>
              <a-select-option :value="3" disabled>混合</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item has-feedback label="分段标识符号" name="delimiters">
            <a-input v-model:value="formData.delimiters" placeholder="\n\n 用于分段；\n 用于分行" />
          </a-form-item>
          <a-form-item has-feedback label="分段最大长度" name="chunk_size">
            <a-input v-model:value="formData.chunk_size" placeholder="≤ 4000" />
          </a-form-item>
          <a-form-item has-feedback label="分段重叠长度" name="chunk_overlap">
            <a-input v-model:value="formData.chunk_overlap" placeholder="分段重叠长度" />
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
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

const rules = {
  embedding_model_id: [{ required: true, message: '请选择向量模型', trigger: 'change' }],
  mode: [{ required: true, message: '请选择分段模式', trigger: 'change' }],
  delimiters: [{ required: true, message: '请输入分段标识符', trigger: 'change' }],
  chunk_size: [{ required: true, message: '请输入分段最大长度', trigger: 'change' }],
  chunk_overlap: [{ required: true, message: '请输入分段重叠长度', trigger: 'change' }]
}
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

