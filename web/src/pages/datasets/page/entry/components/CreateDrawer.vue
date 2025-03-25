<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2024-06-05 23:50:49
 * @LastEditTime: 2025-03-25 14:39:59
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\components\CreateDrawer.vue
 * Copyright 版权声明
-->
<template>
  <a-drawer :title="titleMap[handleType]" :size="`large`" :open="open" @close="onClose" width="100%">
    <template #extra>
      <a-space>
        <a-button @click="onClose">关闭</a-button>
        <!-- <a-button @click="onResetForm">重置</a-button> -->
        <template v-if="handleType === 'create'">
          <a-button type="primary" @click="onSubmitStep1" v-if="currentStep === 0">
            下一步
            <SwapRightOutlined />
          </a-button>
          <template v-if="currentStep === 1">
            <a-button type="primary" @click="currentStep = 0">
              上一步
              <SwapLeftOutlined />
            </a-button>
            <a-button type="primary" @click="onSubmitStep2">
              保存并处理
            </a-button>
          </template>
        </template>
        <template v-if="handleType === 'update'">
          <a-button type="primary" @click="onSubmitUpdate">
            保存
          </a-button>
        </template>
      </a-space>
    </template>

    <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
      <div style="width: 500px; margin: 0 auto 30px;" v-if="handleType === 'create'">
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
              title: '处理并完成',
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
        <a-form-item has-feedback label="知识库描述" name="profile">
          <a-textarea :show-count="true" :auto-size="{ minRows: 3, maxRows: 5 }" placeholder="请输入知识库描述" v-model:value="formData.profile" />
        </a-form-item>
        <template v-if="handleType === 'create'">
          <a-form-item has-feedback label="上传文本文件" name="fileList">
            <!-- accept=".png,.jpg,.jpeg" -->
            <a-upload-dragger
              v-if="formData.fileList.length === 0"
              v-model:fileList="formData.fileList"
              name="file"
              :maxCount="1000"
              :multiple="true"
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
                <InboxOutlined />
              </p>
              <p class="ant-upload-text">拖拽文件至此，或者 <span style="color: #1677ff;">选择文件</span> </p>
              <p class="ant-upload-hint">
                已支持 TXT、 MARKDOWN、 MDX、 PDF、 HTML、 XLSX、 XLS、 DOC、 DOCX、 CSV、 EML、 MSG、 PPTX、 XML、 EPUB、 PPT、 MD、 HTM，每个文件不超过 15MB。
              </p>
            </a-upload-dragger>
            <div class="uped" v-else v-for="(item, index) in formData.fileList" :key="index">
              <div class="iconBox">
                <FileOutlined />
              </div>
              <div class="uped-left">
                <div class="uped-name">{{item?.upData?.name}}</div>
                <div class="uped-size">大小： {{item?.upData?.size}}</div>
              </div>
              <div class="uped-right">
                <DeleteOutlined @click="handleRemoveDoc(item)" />
              </div>
            </div>
          </a-form-item>
        </template>
      </a-form>

      
      <a-form
        v-if="currentStep === 1"
        ref="formRef1"
        :model="formData"
        v-bind="{
          labelCol: { span: 3 },
          wrapperCol: { span: 14 }
        }"
      >
        <a-form-item has-feedback label="向量模型" :name="['chunk_config', 'embedding_model_id']" :rules="[{ required: true, message: '请选择向量模型', trigger: 'change' }]">
          <a-select
            v-model:value="formData.chunk_config.embedding_model_id"
            placeholder="请选择向量模型"
            :options="modeList"
            :field-names="{ label: 'name', value: 'id', options: 'children' }"
          >
          </a-select>
        </a-form-item>
        <a-form-item has-feedback label="分段模式" :name="['chunk_config', 'mode']" :rules="[{ required: true, message: '请选择分段模式', trigger: 'change' }]">
          <a-select
            v-model:value="formData.chunk_config.mode"
            placeholder="请选择分段模式"
          >
            <a-select-option :value="1">通用</a-select-option>
            <a-select-option :value="2" disabled>父子</a-select-option>
            <a-select-option :value="3" disabled>混合</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item has-feedback label="分段标识符号" :name="['chunk_config', 'delimiters']" :rules="[{ required: true, message: '请输入分段标识符', trigger: 'change' }]">
          <a-input v-model:value="formData.chunk_config.delimiters" placeholder="\n\n 用于分段；\n 用于分行" />
        </a-form-item>
        <a-form-item has-feedback label="分段最大长度" :name="['chunk_config', 'chunk_size']" :rules="[{ required: true, message: '请输入分段最大长度', trigger: 'change' }]">
          <a-input v-model:value="formData.chunk_config.chunk_size" placeholder="≤ 4000" />
        </a-form-item>
        <a-form-item has-feedback label="分段重叠长度" :name="['chunk_config', 'chunk_overlap']" :rules="[{ required: true, message: '请输入分段重叠长度', trigger: 'change' }]">
          <a-input v-model:value="formData.chunk_config.chunk_overlap" placeholder="分段重叠长度" />
        </a-form-item>
      </a-form>

    </a-spin>
  </a-drawer>
</template>

<script setup name="CreateDrawer">
import { ref, reactive, defineExpose, toRaw, defineEmits } from 'vue'
import { message } from 'ant-design-vue'

import { SwapRightOutlined, SwapLeftOutlined, InboxOutlined, FileOutlined, DeleteOutlined } from '@ant-design/icons-vue'

import { saveCreate, saveUpdate, uploadDoc } from '@/api/kb'

import { getList as getModeList } from '@/api/mode'

const emit = defineEmits([
  'close'
])

// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

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
const formRef1 = ref(null)

const rules = {
  name: [{ required: true, message: '请输入知识库名称', trigger: 'change' }],
  profile: [{ required: true, message: '请输入知识库描述', trigger: 'change' }],
  fileList: [{ required: true, message: '请上传文件', trigger: 'change' }]
}

const formData = ref({
  name: '',
  profile: '',
  fileList: [],
  docs: [
    // {
    //   "name": "仲裁须知.pdf",
    //   "original_name": "仲裁须知.pdf",
    //   "size": 133026,
    //   "obj_name": "fly-rag/ae8a84e2-0492-11f0-b5e6-d651885abef6.pdf"
    // }
  ],
  chunk_config: {
    type: 1, // 1: 知识库 2: 文档
    embedding_model_id: '', // 向量模型
    mode: 1, // 分段模式 1: 通用 2: 父子 3: 混合
    chunk_size: '500', // 分段最大长度
    chunk_overlap: '200', // 分段重叠长度
    delimiters: '\\n\\n' // 分段标识符号
  }
})

const handleRemove = (file) => {
  return false
}

const handleRemoveDoc = (file) => {
  formData.value.fileList.forEach((item, index) => {
    if (item.uid === file.uid) {
      formData.value.fileList.splice(index, 1)
    }
  })
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
  // return isJpgOrPng && isLt2M;
}

// 自定义上传
const customRequest = async ({ action, file, onSuccess, onError }) => {
  spinningConfig.spinning = true
  try {
    const subData = new FormData()
    subData.append('files', file)
    try {
      const res = await uploadDoc(subData)
      const resData = res?.data[0]??{}
      formData.value.fileList.forEach((item, index) => {
        if (typeof item.upData === 'undefined') {
          item.upData = {}
        }
        if (item.uid === file.uid) {
          item.upData = {...resData, original_name: resData.name}
        }
      })
    } catch (error) {
      formData.value.fileList.forEach((item, index) => {
        if (item.uid === file.uid) {
          formData.value.fileList.splice(index, 1)
        }
      })
    } finally {
      // 关闭loading
      spinningConfig.spinning = false
    }
  } catch (error) {
    // 关闭loading
    message.error(error)
  }
}

// 抽屉显示
const onShow = ({ type = 'create', row = {} }) => {
  handleType.value = type
  currentStep.value = 0
  formData.value = {
    name: '',
    profile: '',
    fileList: [],
    docs: [],
    chunk_config: {
      type: 1, // 1: 知识库 2: 文档
      embedding_model_id: '', // 向量模型
      mode: 1, // 分段模式 1: 通用 2: 父子 3: 混合
      chunk_size: '500', // 分段最大长度
      chunk_overlap: '200', // 分段重叠长度
      delimiters: '\\n\\n' // 分段标识符号
    }
  }
  if (type !== 'create') {
    formData.value = Object.assign({}, formData.value, JSON.parse(JSON.stringify(row)))
  }
  open.value = true
  formRef?.value?.resetFields()
}

// 关闭抽屉
const onClose = () => {
  open.value = false
  emit('close')
}

// 选择数据源
const onSubmitStep1 = () => {
  formRef?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        formData.value.docs = formData.value.fileList.map(item => item.upData)
        await getModeListData()
        spinningConfig.spinning = false
        currentStep.value = 1
      } catch (error) {
        spinningConfig.spinning = false
      }
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 保存并处理
const onSubmitStep2 = () => {
  formRef1?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        await saveCreate(formData.value)
        spinningConfig.spinning = false
        currentStep.value = 2
        onClose()
      } catch (error) {
        spinningConfig.spinning = false
      }
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 模型列表数据
const modeList = ref([])

// 获取模型列表
const getModeListData = async () => {
  try {
    const res = await getModeList({
      type: 2
    })
    modeList.value = res?.data??[]
  } catch (error) {
  }
}

// 编辑保存
const onSubmitUpdate = () => {
  formRef?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        await saveUpdate(formData.value)
        spinningConfig.spinning = false
        message.success(`编辑成功`)
        onClose()
      } catch (error) {
        spinningConfig.spinning = false
      }
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
.uped {
  display: flex;
  border: 1px solid #d9d9d9;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  .iconBox {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    color: #1677ff;
    font-size: 22px;
  }
  &-left {
    flex: 1;
    font-size: 12px;
    .uped-size{
      color: #999;
    }
  }
  &-right {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 10px;
    cursor: pointer;
    font-size: 20px;
  }
}
</style>

