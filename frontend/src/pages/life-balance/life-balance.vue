<template>
    <view class="dialog-container">
        <view class="header">
            <view class="header-content">
                <view class="icon-section">
                    <text class="header-icon">⚖️</text>
                </view>
                <view class="title-section">
                    <text class="page-title">生活平衡教练</text>
                    <text class="page-subtitle">我是您的生活方式顾问小衡</text>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="告诉我您的生活状态，比如学习、社交、健康等方面..." @send="handleSend"
            :disabled="isAiTyping" />

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
            scene: 'life-balance',
            welcomeMessage: '你好！我是生活平衡教练小衡🌟 很高兴成为您的生活方式顾问。\n\n大学生活丰富多彩，但如何在学习、社交、健康、兴趣等各个方面找到平衡，是一门重要的生活艺术。我会以务实而有条理的方式，帮助您分析现状、设定优先级、制定可持续的生活方案。\n\n请告诉我您目前的生活状态，或者您希望改善的生活领域，让我们一起创造更平衡、更充实的大学生活。'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background: linear-gradient(135deg, #607D8B 0%, #90A4AE 100%);
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
    flex-shrink: 0;
}

.header-content {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20rpx;
    padding: 30rpx;
    display: flex;
    align-items: center;
    backdrop-filter: blur(10rpx);
}

.icon-section {
    margin-right: 25rpx;
}

.header-icon {
    font-size: 60rpx;
    display: block;
}

.title-section {
    flex: 1;
}

.page-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
    display: block;
    margin-bottom: 8rpx;
}

.page-subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
    display: block;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20rpx 20rpx 0 0;
    padding: 20rpx;
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