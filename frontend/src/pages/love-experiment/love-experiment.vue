<template>
    <view class="dialog-container">
        <view class="header">
            <image class="header-image" src="../../static/love-experiment.png" mode="widthFix"></image>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="请输入你想尝试的交际场景或话题..." @send="handleSend" :disabled="isAiTyping" />

        <!-- 悬浮保存按钮 -->
        <SaveButton :can-save="hasNewMessages && chatHistory.length > 1" @save="saveChatHistory" />
    </view>
</template>

<script>
import ChatMessages from '@/components/ChatMessages.vue'
import ChatInput from '@/components/ChatInput.vue'
import SaveButton from '@/components/SaveButton.vue'
import chatMixin from '@/utils/chatMixin.js'

export default {
    mixins: [chatMixin],
    components: {
        ChatMessages,
        ChatInput,
        SaveButton
    },
    data() {
        return {
            scene: 'love-experiment',
            welcomeMessage: '你好！我是你的人际交流练习伙伴。我们可以一起模拟各种人际交往场景，帮助你练习表达和沟通技巧。你想尝试什么样的场景呢？'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background-color: #f8f8f8;
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
    flex-shrink: 0;
    text-align: center;
}

.header-image {
    width: 80%;
    max-width: 500rpx;
    min-width: 300rpx;
    max-height: 120rpx;
    margin: 0 auto;
    display: block;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx;
    /* 只为输入框留出空间 */
}

.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    padding: 20rpx 30rpx;
    box-shadow: 0 -5rpx 20rpx rgba(0, 0, 0, 0.1);
    z-index: 999;
}
</style>