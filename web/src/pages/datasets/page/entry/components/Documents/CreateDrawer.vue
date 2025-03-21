<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 20:35:12
 * @LastEditTime: 2025-03-20 21:29:20
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\components\Documents\CreateDrawer.vue
 * Copyright 版权声明
-->
<template>
  <a-drawer :title="titleMap[handleType]" :size="`large`" :open="open" @close="onClose" width="30%">
    <template #extra>
      <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
        <a-space>
          <a-button @click="onClose">关闭</a-button>
          <template v-if="handleType === 'create'">
            <a-button type="primary" @click="onSubmitCreate">
              保存
            </a-button>
          </template>
          <template v-if="handleType === 'update'">
            <a-button type="primary" @click="onSubmitUpdate">
              保存
            </a-button>
          </template>
        </a-space>
      </a-spin>
    </template>

    <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
      <a-form
        ref="formRef"
        layout="vertical"
        name="custom-validation"
        :model="formData"
        :rules="rules"
        v-bind="{
          // labelCol: { span: 3 },
          // wrapperCol: { span: 24 }
        }"
      >
        <a-form-item has-feedback label="名称" name="name" v-if="handleType === 'update'">
          <a-input v-model:value="formData.name" placeholder="请输入名称" />
        </a-form-item>
        <template v-if="handleType === 'create'">
          <a-form-item has-feedback label="上传文本文件" name="fileList">
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
    </a-spin>
  </a-drawer>
</template>

<script setup name="CreateDrawer">
import { ref, reactive, defineExpose, defineEmits } from 'vue'
import { message } from 'ant-design-vue'

import { InboxOutlined, FileOutlined, DeleteOutlined } from '@ant-design/icons-vue'

import { uploadDoc } from '@/api/kb'
import { saveCreate, saveUpdate } from '@/api/documents'

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
  'create': '添加文件',
  'update': '文件重命名'
}
// 操作类型
const handleType = ref('create')

const formRef = ref(null)

const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'change' }],
  fileList: [{ required: true, message: '请上传文件', trigger: 'change' }]
}
const formData = ref({
  name: '',
  fileList: [],
  docs: [
    // {
    //   "name": "仲裁须知.pdf",
    //   "original_name": "仲裁须知.pdf",
    //   "size": 133026,
    //   "obj_name": "fly-rag/ae8a84e2-0492-11f0-b5e6-d651885abef6.pdf"
    // }
  ]
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
      console.log(`🚀 ~ customRequest ~ res:`, res)
      const resData = res?.data[0]??{}
      console.log(`🚀 ~ customRequest ~ resData:`, resData)
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
  if (type === 'create') {
    formData.value.kbId = row.kbId
  }
  if (type === 'update') {
    formData.value = Object.assign({}, formData.value, JSON.parse(JSON.stringify(row)))
    formData.value.fileList = []
  }
  open.value = true
  formRef?.value?.resetFields()
}

// 关闭抽屉
const onClose = () => {
  open.value = false
  emit('close')
}

// 添加文件
const onSubmitCreate = () => {
  formRef?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        formData.value.docs = formData.value.fileList.map(item => item.upData)
        await saveCreate({
          kbId: formData.value.kbId,
          docs: formData.value.docs
        })
        spinningConfig.spinning = false
        onClose()
      } catch (error) {
        spinningConfig.spinning = false
      }
    })
    .catch(error => {
      console.log('error', error)
    })
}

// 编辑保存
const onSubmitUpdate = () => {
  formRef?.value
    .validate()
    .then(async () => {
      spinningConfig.spinning = true
      try {
        await saveUpdate({
          id: formData.value.id,
          name: formData.value.name
        })
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

