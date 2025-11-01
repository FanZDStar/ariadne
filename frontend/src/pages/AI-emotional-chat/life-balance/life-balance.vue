<template>
    <view class="dialog-container theme-student">
        <!-- 主题化头部 -->
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-emoji">⚖️</text>
                </view>
                <view class="header-info">
                    <text class="header-title">生活平衡教练</text>
                    <text class="header-subtitle">我是您的生活方式顾问小衡</text>
                </view>
                <view class="header-actions">
                    <view class="action-btn" @click="clearChat">
                        <text class="action-icon">🗑️</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="content">
            <ChatMessages 
                ref="chatMessages"
                :messages="chatHistory" 
                theme="student"
                @ai-typing="handleAiTyping" 
            />
        </view>
        
        <!-- 底部输入框，类似导航栏效果 -->
        <ChatInput 
            class="fixed-input"
            placeholder="告诉我您的生活状态，如学习、社交、健康等方面..." 
            theme="student"
            @send="handleSend"
            @send-multimodal="handleMultimodalSend"
            :disabled="isAiTyping"
        />
        
        <!-- 悬浮保存按钮 -->
        <SaveButton 
            :can-save="hasNewMessages && chatHistory.length > 1"
            @save="saveChatHistory"
        />
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
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #f8f8f8;
    box-sizing: border-box;
    transition: all 0.3s ease;
}

/* 大学生专区主题 - 米黄色系背景 */
.theme-student {
    background: linear-gradient(135deg, #fffef8 0%, #faf7f0 100%);
}

/* 头部样式 */
.header {
    flex-shrink: 0;
    padding: 20rpx 30rpx;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10rpx);
    border-bottom: 1rpx solid rgba(0, 0, 0, 0.05);
}

.header-content {
    display: flex;
    align-items: center;
    gap: 20rpx;
}

.header-icon {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
}

.icon-emoji {
    font-size: 36rpx;
}

.header-info {
    flex: 1;
}

.header-title {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
    display: block;
    margin-bottom: 4rpx;
}

.header-subtitle {
    font-size: 24rpx;
    color: #666;
    opacity: 0.8;
}

.header-actions {
    display: flex;
    gap: 15rpx;
}

.action-btn {
    width: 60rpx;
    height: 60rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.action-btn:active {
    transform: scale(0.95);
    background: rgba(0, 0, 0, 0.1);
}

.action-icon {
    font-size: 28rpx;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx;
    padding: 20rpx 30rpx;
}

.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20rpx 30rpx;
    box-shadow: 0 -5rpx 20rpx rgba(0, 0, 0, 0.1);
    z-index: 999;
}

/* 大学生专区主题的输入框样式 */
.theme-student .fixed-input {
    background: linear-gradient(135deg, #fffef8, #faf7f0);
    border-top: 1rpx solid rgba(255, 193, 7, 0.2);
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .header {
        padding: 15rpx 25rpx;
    }
    
    .header-icon {
        width: 60rpx;
        height: 60rpx;
    }
    
    .icon-emoji {
        font-size: 28rpx;
    }
    
    .header-title {
        font-size: 28rpx;
    }
    
    .header-subtitle {
        font-size: 22rpx;
    }
    
    .content {
        padding: 15rpx 25rpx;
    }
}
</style>