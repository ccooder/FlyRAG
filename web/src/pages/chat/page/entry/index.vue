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
      <div class="chatBody">
        <!-- 对话内容 -->
        <div class="chatBodyWrap">
          <!-- 问 -->
          <div class="ask">
            <div class="askContent">
              你好
            </div>
          </div>
          <!-- 答 -->
          <div class="answer">
            <img src="@/assets/images/chat/chat-icon.png" alt="" class="answerIcon">
            <div class="answerContent">
              你好，我是AI助手
            </div>
          </div>
          <!-- 更多对话... -->
        </div>
      </div>
      <div class="chatFooter">
        <div class="chatFooterWrap">
          <div class="chatFooterInput">
            <a-textarea
              v-model:value="inputText"
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
              <a-button type="primary" :disabled="inputText === ''" @click="onSend">发送</a-button>
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

const inputText = ref('')
// 控制 chatHistory 显示隐藏的状态
const isChatHistoryVisible = ref(true)

// 发送
const onSend = () => {
  if (inputText.value.trim()) { // 检查输入内容是否为空
    console.log(inputText.value)
    inputText.value = '' // 发送后清空输入框
  }
}

// 生命周期
onMounted(() => {
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
      }
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