<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 23:50:49
 * @LastEditTime: 2025-03-19 10:30:26
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\components\CreateDrawer.vue
 * Copyright 版权声明
-->
<template>
  <a-drawer :title="titleMap[handleType]" :size="`large`" :open="open" @close="onClose" width="100%">
    <template #extra>
      <a-button style="margin-right: 8px" @click="onClose">关闭</a-button>
      <!-- <a-button style="margin-right: 8px" @click="onResetForm">重置</a-button> -->
      <a-button type="primary" @click="onSubmitStep1" v-if="currentStep === 0">
        下一步
        <SwapRightOutlined />
      </a-button>
      <a-button type="primary" @click="onSubmitStep2" v-if="currentStep === 1">
        保存并处理
      </a-button>
    </template>

    <div style="width: 500px; margin: 0 auto 30px;">
      <a-steps
        v-model:current="currentStep"
        size="small"
        :items="[
          {
            title: '选择数据源',
          },
          {
            title: '文本分段与清洗',
          },
          {
            title: '文本分段与清洗',
          },
        ]"
      ></a-steps>
    </div>

    <a-form
      v-if="currentStep === 0"
      ref="formRef"
      layout="vertical"
      name="custom-validation"
      :model="formData"
      :rules="rules"
      v-bind="{
        labelCol: { span: 3 },
        wrapperCol: { span: 24 }
      }"
    >
    <!-- @finish="handleFinish"
    @validate="handleValidate"
    @finishFailed="handleFinishFailed" -->
    <a-form-item has-feedback label="知识库名称" name="name">
      <a-input v-model:value="formData.name" placeholder="请输入知识库名称" />
    </a-form-item>
    <a-form-item has-feedback label="知识库描述" name="desc">
      <a-textarea :show-count="true" :auto-size="{ minRows: 3, maxRows: 5 }" placeholder="请输入知识库描述" v-model:value="formData.desc" />
    </a-form-item>
    <a-form-item has-feedback label="上传文本文件" name="fileList">
      <a-upload-dragger
        v-show="formData.fileList.length === 0"
        v-model:fileList="formData.fileList"
        accept=".png,.jpg,.jpeg"
        name="file"
        :maxCount="1"
        :multiple="false"
        :showUploadList="false"
        action=""
        :before-upload="beforeUpload"
        :customRequest="customRequest"
        list-type="picture"
        @change="handleChange"
        @drop="handleDrop"
        @remove="handleRemove"
      >
        <p class="ant-upload-drag-icon">
          <inbox-outlined></inbox-outlined>
        </p>
        <p class="ant-upload-text">拖拽文件至此，或者 <span style="color: #1677ff;">选择文件</span> </p>
        <p class="ant-upload-hint">
          已支持 TXT、 MARKDOWN、 MDX、 PDF、 HTML、 XLSX、 XLS、 DOC、 DOCX、 CSV、 EML、 MSG、 PPTX、 XML、 EPUB、 PPT、 MD、 HTM，每个文件不超过 15MB。
        </p>
      </a-upload-dragger>
    </a-form-item>
  </a-form>
  </a-drawer>
</template>

<script setup name="CreateDrawer">
import { ref, defineExpose, toRaw } from 'vue'
import { message } from 'ant-design-vue'

import { SwapRightOutlined } from '@ant-design/icons-vue'

// 打开状态
const open = ref(false)
// 标题
const titleMap = {
  'create': '创建知识库',
  'update': '编辑知识库'
}
// 操作类型
const handleType = ref('create')

// 当前步骤
const currentStep = ref(0)

const formRef = ref(null)

const rules = {
  name: [{ required: true, message: '请输入知识库名称', trigger: 'change' }],
  desc: [{ required: true, message: '请输入知识库描述', trigger: 'change' }],
  fileList: [{ required: true, message: '请上传文件', trigger: 'change' }]
}
const formData = ref({
  name: '',
  desc: '',
  fileList: []
})

const fileList = ref([])



const handleRemove = (file) => {
  return false
}

const handleChange = (info) => {
  const status = info.file.status
  if (status === 'uploading') {
  } else if (status === 'done') {
    message.success(`${info.file.name} 文件上传成功.`)
  } else if (status === 'error') {
    message.error(`${info.file.name} 文件上传错误.`)
  } else if (status === 'removed') {
    message.error(`${info.file.name} 文件删除成功.`)
  }
}
const handleDrop = (e) => {
  console.log(e)
}

const beforeUpload = (file) => {
  return true
  // console.log(`🚀 ~ beforeUpload ~ file:`, file)
  // const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  // if (!isJpgOrPng) {
  //   message.error('请上传png、jpg、jpeg格式的文件!');
  // }
  // const isLt2M = file.size / 1024 / 1024 < 1000;
  // if (!isLt2M) {
  //   message.error('文件必须小于1000MB!');
  // }
  // file.processConfig = {
  //   status: '未识别'
  // }
  // return isJpgOrPng && isLt2M;
}

// 自定义上传
const customRequest = async ({ action, file, onSuccess, onError }) => {
  try {
    formData.value.fileList.find((item, index) => {
      if (item.uid === file.uid) {
        item.status = 'done'
        // 初始化配置项
        item.processConfig = {
          status: '未识别'
        }
      }
      return item.uid === file.uid
    })
  } catch (error) {
    // 关闭loading
    message.error(error)
  }
}

// 抽屉显示
const onShow = ({ type = 'create', row = {} }) => {
  handleType.value = type
  formData.value = Object.assign({}, formData.value, JSON.parse(JSON.stringify(row)))
  open.value = true
  formRef?.value?.resetFields()
}

// 关闭抽屉
const onClose = () => {
  open.value = false
}

// 选择数据源
const onSubmitStep1 = () => {
  formRef?.value
    .validate()
    .then(() => {
      console.log('values', formData, toRaw(formData))
      currentStep.value = 1
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 保存并处理
const onSubmitStep2 = () => {
  formRef?.value
    .validate()
    .then(() => {
      console.log('values', formData, toRaw(formData))
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 重置表单
const onResetForm = () => {
  formRef.value.resetFields()
}

// 暴漏方法
defineExpose({
  onShow
})
</script>

<style lang="scss" scoped>
</style>

