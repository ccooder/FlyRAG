
<template>
  <div class="chatWrap">
    <div class="chatHeader">
      <div class="chatHeaderTitle">
        <img src="@/assets/images/chat/title-icon.png" alt="">
        AI助手
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 生命周期
onMounted(() => {
})

</script>

<style lang="scss" scoped>
.chatWrap{
  width: 100%;
  height: 100vh;
  background: #fff;
  .chatHeader{
    height: 64px;
    line-height: 64px;
    padding: 0 24px;
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
}
</style>

