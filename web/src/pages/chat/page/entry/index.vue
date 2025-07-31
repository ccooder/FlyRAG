<template>
  <div class="chatWrap">
    <!-- 使用 v-model 绑定显示隐藏状态 -->
    <div class="chatHistory" :class="{'chatHistoryHide': !isChatHistoryVisible}">
      <div class="chatHistorySwitch">
        <a-button type="primary" ghost>
          <template #icon>
            <PlusOutlined />
          </template>
          新建对话
        </a-button>
        <a-tooltip placement="right" v-if="isChatHistoryVisible">
          <template #title>
            <span>收起边栏</span>
          </template>
          <LeftCircleOutlined class="chatHistorySwitchIcon" @click="isChatHistoryVisible = false" />
        </a-tooltip>
        <a-tooltip placement="right" v-else>
          <template #title>
            <span>打开边栏</span>
          </template>
          <RightCircleOutlined class="chatHistorySwitchIcon" @click="isChatHistoryVisible = true" />
        </a-tooltip>
      </div>
      <div class="chatHistoryWrap">
        <div class="chatHistoryItem active">
          <div class="con">
            测试测试哟
          </div>
          <a-dropdown>
            <div class="icon">
              <EllipsisOutlined />
            </div>
            <template #overlay>
              <a-menu>
                <a-menu-item>
                  <EditOutlined />
                  <a-button type="link">重命名</a-button>
                </a-menu-item>
                <a-menu-item>
                  <DeleteOutlined />
                  <a-button type="link" danger>删除</a-button>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
        <div class="chatHistoryTitle">
          七天内
        </div>
        <div class="chatHistoryItem" v-for="(item, index) in 100" :key="index">
          <div class="con">
            测试测试哟 {{ item }}
          </div>
          <a-dropdown>
            <div class="icon">
              <EllipsisOutlined />
            </div>
            <template #overlay>
              <a-menu>
                <a-menu-item>
                  <EditOutlined />
                  <a-button type="link">重命名</a-button>
                </a-menu-item>
                <a-menu-item>
                  <DeleteOutlined />
                  <a-button type="link" danger>删除</a-button>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>
    </div>
    <div class="chatWrapMain" :style="{ flex: isChatHistoryVisible ? '1' : '1 1 100%' }">
      <div class="chatHeader">
        <div class="chatHeaderTitle">
          <img src="@/assets/images/chat/title-icon.png" alt="">
          AI助手
        </div>
      </div>
      <div class="chatBody" ref="contentBodyRef">
        <!-- 对话内容 -->
        <div class="chatBodyWrap" v-if="rag.messageList.length > 0">
          <template v-for="(item, index) in rag.messageList" :key="index">
            <!-- 问 -->
            <div class="ask" v-if="item.type === 'ask'">
              <div class="askContent">
                {{ item.content }}
              </div>
            </div>
            <!-- 答 -->
            <div class="answer" v-if="item.type === 'answer'">
              <img src="@/assets/images/chat/chat-icon.png" alt="" class="answerIcon">
              <div class="answerContent">
                {{ item.content }}
              </div>
            </div>
            <!-- 更多对话... -->
          </template>
        </div>
        <div class="emptyMessage" v-else>
          <h3>
            我是 AI 助手，很高兴见到你！
          </h3>
          <p>
            我是一个 AI 助手，你可以向我咨询任何问题。
          </p>
        </div>
      </div>
      <div class="chatFooter">
        <div class="chatFooterWrap">
          <div class="chatFooterInput">
            <a-textarea
              v-model:value="rag.inputText"
              placeholder="直接输入对文件内容的要求，或文件的用途。"
              :auto-size="{ minRows: 1, maxRows: 10 }"
              @keydown.enter.prevent="onSend"
            />
          </div>
          <div class="chatFooterBtn">
            <div class="handleBtn">
              <span class="btn">
                <span class="myFont myIcon-lianwangsousuo"></span>
                深度思考
              </span>
              <span class="btn">
                <span class="myFont myIcon-shendusikao"></span>
                联网搜索
              </span>
            </div>
            <div class="sendBtn">
              <a-button :loading="rag.isSending" type="primary" :disabled="rag.inputText === ''" @click="onSend">发送</a-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusOutlined, LeftCircleOutlined, RightCircleOutlined, EllipsisOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue'

import { gettoken, aiChat } from '@/api/chat.js'


// 控制 chatHistory 显示隐藏的状态
const isChatHistoryVisible = ref(true)

// 内容容器引用
const contentBodyRef = ref(null)

// ai 助手
const rag = reactive({
  // 会话 token
  token: '',
  // 输入框内容
  inputText: '',
  // 是否为发送中
  isSending: false,
  // 对话 list
  messageList: []
})

// 发送
const onSend = () => {
  // 检查输入内容是否为空
  if (rag.inputText.trim()) {
    console.log(rag.inputText)
  }
  if (!rag.token) {
    gettoken().then(res => {
      rag.token = res.data
      onSendMessage()
    })
    return
  }

  // 发送状态
  rag.isSending = true

  const url = aiChat()
  const params = {
    appId: 'string',
    appToken: rag.token,
    // appToken: rag.token + 'a',
    message: rag.inputText,
    userId: `${new Date().getTime()}`
  }

  // 使用 fetch 发起 POST 请求
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    if (!response.body) {
      throw new Error('No response body')
    }
    
    // 问题内容
    rag.messageList.push({
      type: 'ask',
      content: rag.inputText
    })
    // 回答内容
    rag.messageList.push({
      type: 'answer',
      content: ''
    })

    // 发送后清空输入框
    rag.inputText = ''

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    const readChunk = async () => {
      const aaa = await reader.read()
      // console.log('--------------------', aaa)
      const { done, value } = await reader.read()
      if (done === true) {
        // 加载结束
        rag.isSending = false
        return
      }
      buffer += decoder.decode(value, { stream: true })
      const events = buffer.split(/\n\n/)
      buffer = events.pop() || ''

      events.forEach(event => {
        if (event.startsWith('data:')) {
          const data = event.slice(5).trim()
          // console.log('--', data)
          try {
            const parsedData = JSON.parse(data)
            // 假设解析后的数据中有一个名为 'content' 的字段存储回答内容
            const content = parsedData?.answer ?? ''
            if (content) {
              // 回答内容
              rag.messageList[rag.messageList.length - 1].content += content
              // console.log(`🚀 ~ readChunk ~ rag.messageList:`, rag.messageList)
              // 自动滚动到最新内容位置
              if (contentBodyRef.value) {
                contentBodyRef.value.scrollTop = contentBodyRef.value.scrollHeight
              }
            }
          } catch (error) {
            // console.error('解析 SSE 数据出错:', error)
            // rag.isSending = false
          }
        }
      })

      return readChunk()
    }

    return readChunk()
  })
  .catch(error => {
    console.error('SSE 请求出错:', error)
    // 加载出错，结束加载状态
    rag.isSending = false
  })
}

// 生命周期
onMounted(() => {
  gettoken({
    appId: 'string'
  }).then(res => {
    rag.token = res?.data?.appToken ?? ''
  })
})
</script>

<style lang="scss" scoped>
.chatWrap{
  width: 100%;
  height: 100vh;
  background: #fff;
  display: flex; // 使用 Flex 布局
  .chatHistory{
    transition: width 0.3s ease; // 添加宽度变化的过渡效果
    overflow: hidden; // 隐藏超出部分
    border-right: 1px solid #F0F0F0; // 添加分隔线
    position: relative;
    background-color: #F7F8FA; // 设置背景色
    width: 275px;
    .chatHistorySwitch {
      height: 60px;
      display: flex; // 使用 Flexbox 布局
      justify-content: space-between; // 让子元素两端对齐
      align-items: center; // 垂直居中对齐
      padding: 0 16px;

      .chatHistorySwitchIcon{
        font-size: 22px;
        cursor: pointer;
      }
    }

    .chatHistoryWrap {
      padding: 16px;
      height: calc(100% - 60px);
      overflow-y: auto;

      .chatHistoryTitle {
        font-size: 14px;
        font-weight: 600;
        color: #262626;
        margin: 12px 0;
        padding-left: 12px;
        border-left: 2px solid #1890ff;
      }

      .chatHistoryItem {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;

        .con {
          flex: 1;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          color: #595959;
        }

        .icon {
          color: #333;
          transition: color 0.3s ease;
          display: none;

          &:hover {
            color: #000;
          }
        }

        &:hover,
        &.active {
          background-color: #D8E5FF;
          .icon{
            display: block;
          }
        }
      }
    }
    &.chatHistoryHide{
      width: 60px;
      .chatHistorySwitch{
        .ant-btn{
          display: none;
        }
      }
      .chatHistoryWrap{
        display: none;
      }
    }
  }
  .chatWrapMain{
    flex: 1;
    display: flex;
    flex-direction: column;
    .chatHeader{
      height: 60px;
      line-height: 60px;
      padding: 0 20px;
      border-bottom: 1px  solid #F0F0F0;
      &Title{
        font-size: 20px;
        font-weight: bold;
        img{
          vertical-align: middle;
          margin-right: 5px;
          margin-top: -3px;
        }
      }
    }
    .chatBody{
      padding: 20px;
      flex: 1; // 让聊天内容区域自动填充剩余空间
      overflow-y: auto; // 内容超出时显示滚动条
      .chatBodyWrap {
        display: flex;
        flex-direction: column;
        gap: 12px; // 对话之间的间距
        .ask {
          display: flex;
          justify-content: flex-end; // 提问内容在右侧
          .askContent {
            background-color: #F7FAFF; // 提问背景色
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 70%;
          }
        }
        .answer {
          display: flex;
          align-items: flex-start;
          .answerIcon {
            width: 49px;
            margin-right: 5px;
          }
          .answerContent {
            background-color: #F7FAFF; // 回答背景色
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 70%;
          }
        }
      }
      .emptyMessage{
        display: flex; // 使用 Flexbox 布局
        flex-direction: column; // 子元素垂直排列
        justify-content: center; // 垂直居中
        align-items: center; // 水平居中
        height: 100%; // 确保容器高度占满父元素
        text-align: center; // 文本水平居中
        h3{
          font-size: 22px;
          font-weight: bold;
        }
        p{
          margin-top: 5px;
        }
      }
    }
    .chatFooter{
      padding: 20px;
      .chatFooterWrap{
        background: #FFFFFF;
        box-shadow: 4px 2px 20px 0px rgba(33,109,255,0); /* 默认阴影透明度为 0 */
        border-radius: 30px;
        border: 1px solid #216DFF;
        overflow: hidden;
        padding: 15px;
        transition: box-shadow 0.3s ease; /* 添加过渡效果 */
  
        &:hover,
        &:focus-within {
          box-shadow: 4px 2px 20px 0px rgba(33,109,255,0.2); /* 输入框获取焦点时显示阴影 */
        }
        .chatFooterInput{
          .ant-input{
            border: none;
            box-shadow: none;
            &::placeholder{
              color: #999999;
            }
          }
        }
        .chatFooterBtn{
          display: flex; // 使用 Flexbox 布局
          justify-content: space-between; // 让子元素两端对齐
          align-items: center; // 垂直居中对齐
          padding-top: 15px;
  
          .handleBtn{
            display: flex; // 让按钮水平排列
            gap: 10px; // 按钮之间的间距
  
            .btn{
              padding: 8px 16px;
              border: 1px solid #E2E2E2;
              border-radius: 20px;
              color: #4C4C4C;
              cursor: pointer;
              transition: all 0.3s ease;
  
              &:hover,
              &.active{
                border-color: #C0D9FE;
                background-color: #DBE9FE;
                color: #4D6BFE;
              }
            }
          }
  
          .sendBtn{
            .ant-btn{
              border-radius: 20px; // 让按钮有圆角
            }
          }
        }
      }
    }
  }
}
</style>