<template>
    <view class="dialog-container theme-tree-hole">
        <!-- 主题化头部 -->
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-emoji">💝</text>
                </view>
                <view class="header-info">
                    <text class="header-title">自我关爱助手</text>
                    <text class="header-subtitle">我是您的自我关爱教练小爱</text>
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
                theme="tree-hole"
                @ai-typing="handleAiTyping" 
            />
        </view>
        
        <!-- 底部输入框，类似导航栏效果 -->
        <ChatInput 
            class="fixed-input"
            placeholder="分享您在自我关爱方面的困惑或想法..." 
            theme="tree-hole"
            @send="handleSend" 
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
            scene: 'self-love',
            welcomeMessage: '你好！我是自我关爱助手小爱💝 很高兴成为您的心灵陪伴者。\n\n我理解自我关爱的重要性，无论是情绪管理、自我接纳、内在成长，还是建立健康的生活习惯，我都会以温暖包容的态度陪伴您，一起探索自我关爱的方法。\n\n爱他人之前，先要学会爱自己。这里是安全的心灵港湾，请放心分享您在自我关爱方面的困惑或想法。'
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

/* 心灵树洞主题 - 浅绿色系背景 */
.theme-tree-hole {
    background: linear-gradient(135deg, #f8fff8 0%, #e8f8e8 100%);
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
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.05));
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
    display: block;
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
    background: rgba(76, 175, 80, 0.1);
    transition: all 0.3s ease;
}

.action-btn:active {
    transform: scale(0.95);
    background: rgba(76, 175, 80, 0.2);
}

.action-icon {
    font-size: 24rpx;
}

/* 内容区域 */
.content {
    flex: 1;
    padding: 20rpx;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx;
}

/* 固定底部输入框 */
.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20rpx);
    padding: 20rpx 30rpx;
    box-shadow: 0 -10rpx 30rpx rgba(0, 0, 0, 0.08);
    border-top: 1rpx solid rgba(76, 175, 80, 0.1);
    z-index: 999;
}

/* 确保主题样式优先级 */
.fixed-input :deep(.theme-tree-hole .input:focus),
.fixed-input :deep(.theme-tree-hole .input.typing-active) {
    border-color: #4caf50 !important;
    box-shadow: 0 0 0 4rpx rgba(76, 175, 80, 0.1) !important;
}

.fixed-input :deep(.theme-tree-hole .submit-btn:not(.disabled)) {
    background-color: #4caf50 !important;
}

/* 响应式设计 */
@media screen and (max-width: 750rpx) {
    .header {
        padding: 15rpx 20rpx;
    }
    
    .header-icon {
        width: 70rpx;
        height: 70rpx;
    }
    
    .icon-emoji {
        font-size: 32rpx;
    }
    
    .header-title {
        font-size: 28rpx;
    }
    
    .header-subtitle {
        font-size: 22rpx;
    }
    
    .content {
        padding: 15rpx;
    }
    
    .fixed-input {
        padding: 15rpx 20rpx;
    }
}
</style>