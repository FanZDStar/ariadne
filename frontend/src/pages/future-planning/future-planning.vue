<template>
    <view class="dialog-container">
        <view class="header">
            <view class="header-content">
                <view class="icon-section">
                    <text class="header-icon">🔮</text>
                </view>
                <view class="title-section">
                    <text class="page-title">未来规划指导</text>
                    <text class="page-subtitle">我是您的人生规划导师小未</text>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="聊聊您对未来的思考，比如专业选择、职业规划等..." @send="handleSend"
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
            scene: 'future-planning',
            welcomeMessage: '你好！我是未来规划导师小未🌟 很荣幸成为您人生旅程的引路人。\n\n每个人的未来都充满无限可能，无论您在思考专业方向、职业选择、考研升学，还是探索人生价值，我都会以专业的视角和丰富的经验，陪伴您一起规划属于您的精彩未来。\n\n请告诉我，您目前对未来最关心的问题是什么？让我们一起探索您内心的声音。'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
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