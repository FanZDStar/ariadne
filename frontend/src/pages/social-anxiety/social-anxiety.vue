<template>
    <view class="dialog-container">
        <view class="header">
            <view class="header-content">
                <view class="icon-section">
                    <text class="header-icon">👥</text>
                </view>
                <view class="title-section">
                    <text class="page-title">社交焦虑陪伴</text>
                    <text class="page-subtitle">我是您的社交技能教练小社</text>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="分享您的社交困扰，比如宿舍关系、课堂发言等..." @send="handleSend"
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
            scene: 'social-anxiety',
            welcomeMessage: '你好！我是社交焦虑陪伴师小社👋 很高兴成为您的社交技能教练。\n\n我理解社交焦虑带来的困扰，无论是宿舍相处、课堂发言、加入社团，还是建立友谊，我都会以温暖包容的态度陪伴您，一起练习社交技巧，建立自信。\n\n这里是安全的练习空间，请放心分享您在社交中遇到的困难或想要改善的地方。'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
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