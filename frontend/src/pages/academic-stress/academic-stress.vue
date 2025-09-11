<template>
    <view class="dialog-container">
        <view class="header">
            <view class="header-content">
                <view class="icon-section">
                    <text class="header-icon">📚</text>
                </view>
                <view class="title-section">
                    <text class="page-title">学业压力疏导</text>
                    <text class="page-subtitle">我是您的学业心理咨询师小学</text>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages ref="chatMessages" :messages="chatHistory" @ai-typing="handleAiTyping" />
        </view>

        <!-- 底部输入框 -->
        <ChatInput class="fixed-input" placeholder="告诉我您遇到的学业困扰，比如考试焦虑、学习效率等..." @send="handleSend"
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
            scene: 'academic-stress',
            welcomeMessage: '你好！我是学业压力疏导师小学🎓 很高兴为您提供专业的学业心理支持。\n\n无论您面临考试焦虑、学习效率问题、专业困惑，还是其他学业相关的压力，我都会以专业而温暖的方式陪伴您。让我们一起找到缓解压力、提升学习状态的方法。\n\n请告诉我，您目前最困扰的学业问题是什么？'
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
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