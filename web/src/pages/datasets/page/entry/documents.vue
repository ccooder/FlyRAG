<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 14:21:13
 * @LastEditTime: 2025-03-20 21:27:23
 * @LastEditors: WuFeng <763467339@qq.com>
 * @Description: 
 * @FilePath: \FlyRAG\web\src\pages\datasets\page\entry\documents.vue
 * Copyright 版权声明
-->
<template>
  <div class="pageWrap">
    <ManageLeft></ManageLeft>
    <div class="pageWrap-main">
      <h2 class="title">
        文档
      </h2>
      <p class="desc">
        的所有文件都在这里显示，整个都可以链接到 Dify 引用或通过 Chat 插件进行索引。
      </p>
      <a-spin :tip="spinningConfig.tip" :spinning="spinningConfig.spinning">
        <div class="handleWrap">
          <a-button type="primary" @click="handleCreate">
            <template #icon>
              <PlusOutlined />
            </template>
            添加文件
          </a-button>
        </div>
        <div class="dataTable">
          <a-table :dataSource="listState.data" :columns="listState.columns">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'status'">
                <span>
                  <a-tag
                    v-if="record.status === 3"
                    color="success"
                  >
                    启用
                  </a-tag>
                  <a-tag
                    v-if="record.status === 0"
                    color="error"
                  >
                    禁用
                  </a-tag>
                  <a-tag
                    v-if="record.status === 1"
                    color="warning"
                  >
                    排队中
                  </a-tag>
                  <a-tag
                    v-if="record.status === 2"
                    color="processing"
                  >
                    索引中
                  </a-tag>
                </span>
              </template>
              <template v-if="column.key === 'action'">
                <!-- v-model:checked="state.checked2" -->
                <a-switch size="small" />
                <a-divider type="vertical" />
                <a-button type="link">分段设置</a-button>
                <a-divider type="vertical" />
                <a-button type="link" @click="handleUpdate(record)">重命名</a-button>
                <a-divider type="vertical" />
                <a-popconfirm
                  title="您确定要删除吗？"
                  @confirm="onConfirmDelete(record)"
                >
                  <a-button type="link" danger>删除</a-button>
                </a-popconfirm>
              </template>
            </template>
          </a-table>
        </div>
      </a-spin>
    </div>
    <CreateDrawerKB ref="CreateDrawerRef" @close="loadData"></CreateDrawerKB>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusOutlined
} from '@ant-design/icons-vue'
import ManageLeft from './components/ManageLeft.vue'
import CreateDrawerKB from './components/Documents/CreateDrawer.vue'
import { message } from 'ant-design-vue'

import { getList, saveDelete } from '@/api/documents'

const props = defineProps({
  kbId: {
    type: String,
    required: true
  }
})

const router = useRouter()

// loading 配置
const spinningConfig = reactive({
  spinning: false,
  tip: '处理中...'
})

const CreateDrawerRef = ref(null)

// 列表状态
const listState = reactive(
  {
    columns: [
      {
        title: '名称',
        dataIndex: 'name',
        key: 'name',
      },
      {
        title: '分段模式',
        dataIndex: 'age',
        key: 'age',
        align: 'center',
        width: 140
      },
      {
        title: '字符数',
        dataIndex: 'char_count',
        key: 'char_count',
        align: 'center',
        width: 100
      },
      {
        title: '上传时间',
        dataIndex: 'create_time',
        key: 'create_time',
        align: 'center',
        width: 180
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        align: 'center',
        width: 100
      },
      {
        title: '操作',
        dataIndex: 'action',
        key: 'action',
        width: 350,
        align: 'center',
        // slots: { customRender: 'action' },
      },
    ],
    data: [],
    query: {
      current: 1,
      size: 10
    }
  }
)

// 创建
const handleCreate = () => {
  if (CreateDrawerRef.value) {
    CreateDrawerRef.value.onShow({
      type: 'create',
      row: {
        kbId: props.kbId
      }
    })
  }
}

// 编辑
const handleUpdate = (row) => {
  console.log(`🚀 ~ handleUpdate ~ row:`, row)
  if (CreateDrawerRef.value) {
    CreateDrawerRef.value.onShow({
      type: 'update',
      row: {
        id: row.id,
        name: row.name
      }
    })
  }
}

// 删除
const onConfirmDelete = async (row) => {
  await saveDelete({
    id: row.id
  })
  message.success(`删除成功`)
  loadData()
}

// 加载数据
const loadData = async () => {
  spinningConfig.spinning = true
  try {
    const res = await getList({
      kb_id: props.kbId
    })
    listState.data = res?.data??[]
    spinningConfig.spinning = false
  } catch (error) {
    spinningConfig.spinning = false
  }
}

// 生命周期
onMounted(() => {
  loadData()
})

</script>

<style lang="scss" scoped>
@import url('../../styles/manage.scss');
.handleWrap{
  margin-bottom: 8px;
  display: flex;
  justify-content: flex-end;
}
</style>

