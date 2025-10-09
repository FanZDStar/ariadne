<template>
    <view class="dialog-container theme-emotion">
        <!-- 主题化头部 -->
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-emoji">💝</text>
                </view>
                <view class="header-info">
                    <text class="header-title">情感成长陪伴</text>
                    <text class="header-subtitle">我是您的情感成长引导者小心</text>
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
                theme="emotion"
                @ai-typing="handleAiTyping" 
            />
        </view>
        
        <!-- 底部输入框，类似导航栏效果 -->
        <ChatInput 
            class="fixed-input"
            placeholder="分享您的情感困惑，比如情绪管理、关系处理等..." 
            theme="emotion"
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
            scene: 'emotional-growth',
            welcomeMessage: '你好！我是情感成长陪伴师小心💕 很高兴能陪伴您探索内心的情感世界。\n\n情感成长是人生中最珍贵的旅程之一。无论您想要学习情绪管理、改善人际关系、处理心理创伤，还是建立更健康的情感模式，我都会以细腻的共情和专业的洞察，温暖地陪伴您。\n\n请放心分享您内心的感受和困惑，这里是安全的情感港湾。'
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

/* 情感对话主题 - 蓝色系背景 */
.theme-emotion {
    background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
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
    background: linear-gradient(135deg, rgba(41, 182, 246, 0.1), rgba(41, 182, 246, 0.05));
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
    background-color: #fff;
    padding: 20rpx 30rpx;
    box-shadow: 0 -5rpx 20rpx rgba(0, 0, 0, 0.1);
    z-index: 999;
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