<!--
 * @Author: WuFeng <763467339@qq.com>
 * @Date: 2025-03-20 14:21:13
 * @LastEditTime: 2025-07-23 17:27:55
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
          <a-table 
            :dataSource="listState.data" 
            :columns="listState.columns"
            :pagination="{ current: listState.query.current, pageSize: listState.query.size, total: listState.total }"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'name'">
                <span>
                  <router-link :to="{ path: `/datasets/${props.kbId}/documents/${record.id}` }">
                    {{ record.name }}
                  </router-link>
                </span>
              </template>
              <template v-if="column.key === 'chunk_mode'">
                <span>
                  <a-tag
                    v-if="record.chunk_mode === 1"
                  >
                    通用
                  </a-tag>
                  <a-tag
                    v-if="record.chunk_mode === 2"
                  >
                    父子
                  </a-tag>
                  <a-tag
                    v-if="record.chunk_mode === 3"
                  >
                    混合
                  </a-tag>
                </span>
              </template>
              <template v-if="column.key === 'status'">
                <span>
                  <a-tag
                    v-if="record.status === 3"
                    color="success"
                  >
                    可用
                  </a-tag>
                  <a-tag
                    v-else-if="record.status === 0"
                    color="error"
                  >
                    禁用
                  </a-tag>
                  <a-tag
                    v-else-if="record.status === 1 && record.pause === 0"
                    color="warning"
                  >
                    排队中
                  </a-tag>
                  <a-tag
                    v-else-if="record.status === 2 && record.pause === 0"
                    color="processing"
                  >
                    索引中
                  </a-tag>

                  <a-tag 
                    v-if="record.pause === 1"
                    color="error"
                  >
                    已暂停
                  </a-tag>
                  
                  <a-popconfirm
                    v-if="(record.status === 1 || record.status === 2) && record.pause === 0"
                    title="您确定要暂停吗？"
                    @confirm="confirmPause(record)"
                  >
                    <a-divider type="vertical" />
                    <StopOutlined title="暂停" style="color: #ff4d4f;font-size: 16px;cursor: pointer;" />
                  </a-popconfirm>
                  
                  <a-popconfirm
                    v-if="(record.status === 1 || record.status === 2) && record.pause === 1"
                    title="您确定要恢复吗？"
                    @confirm="confirmResume(record)"
                  >
                    <a-divider type="vertical" />
                    <PlayCircleOutlined title="恢复" style="color: #389e0d;font-size: 16px;cursor: pointer;" />
                  </a-popconfirm>
                </span>
              </template>
              <template v-if="column.key === 'action'">
                <a-tooltip>
                  <template #title v-if="record.status !== 0 && record.status !== 3">排队中、索引中的文档无法禁用</template>
                  <a-switch 
                    :disabled="record.status !== 0 && record.status !== 3"
                    v-model:checked="record.statusTemp" 
                    size="small" 
                    :checkedValue="3" 
                    :unCheckedValue="0"
                    @change="(val) => onSwitchChange(val, record)"
                  />
                </a-tooltip>
                <a-divider type="vertical" />
                <a-button type="link" @click="handleSettings(record)">分段设置</a-button>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusOutlined,
  PlayCircleOutlined,
  StopOutlined
} from '@ant-design/icons-vue'
import ManageLeft from './components/ManageLeft.vue'
import CreateDrawerKB from './components/Documents/CreateDrawer.vue'
import { message } from 'ant-design-vue'

import { getList, saveDelete, saveUpdate, saveResume, savePause } from '@/api/documents'

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
        minWidth: 200
      },
      {
        title: '分段模式',
        dataIndex: 'chunk_mode',
        key: 'chunk_mode',
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
        width: 180
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
      size: 3
    },
    total: 0
  }
)

// 暂停
const confirmPause = async (row) => {
  try {
    await savePause({
      id: row.id
    })
    message.success(`暂停成功`)
    loadData()
  } catch (error) {
    // message.error(`暂停失败`)
  }
}

// 恢复
const confirmResume = async (row) => {
  try {
    await saveResume({
      id: row?.id??''
    })
    message.success(`恢复成功`)
    loadData()
  } catch (error) {
    // message.error(`恢复失败`)
  }
}

// 切换状态
const onSwitchChange = async (val, row) => {
  console.log(`🚀 ~ onSwitchChange ~ row:`, row)
  console.log(`🚀 ~ onSwitchChange ~ val:`, val)
  try {
    await saveUpdate({
      id: row.id,
      status: val
    })
    message.success(`状态修改成功`)
    loadData()
  } catch (error) {
    row.statusTemp = row.status
  }
}

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

// 分段设置
const handleSettings = (row) => {
  router.push({
    name: 'DatasetsDocumentsSettings',
    params: {
      kbId: props.kbId,
      docId: row.id
    }
  })
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
    }, listState.query)
    listState.data = res?.data?.records??[]
    listState.total = res?.data?.total??0
    listState.forEach(item => {
      item.statusTemp = item.status
    })
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

