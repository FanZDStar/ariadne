<template>
    <view class="dialog-container">
        <view class="header">
            <view class="header-content">
                <view class="icon-section">
                    <text class="header-icon">💝</text>
                </view>
                <view class="title-section">
                    <text class="page-title">情感成长陪伴</text>
                    <text class="page-subtitle">我是您的情感成长引导者小心</text>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="分享您的情感困惑，比如情绪管理、关系处理等..." @send="handleSend"
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
            scene: 'emotional-growth',
            welcomeMessage: '你好！我是情感成长陪伴师小心💕 很高兴能陪伴您探索内心的情感世界。\n\n情感成长是人生中最珍贵的旅程之一。无论您想要学习情绪管理、改善人际关系、处理心理创伤，还是建立更健康的情感模式，我都会以细腻的共情和专业的洞察，温暖地陪伴您。\n\n请放心分享您内心的感受和困惑，这里是安全的情感港湾。'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background: linear-gradient(135deg, #E91E63 0%, #F06292 100%);
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