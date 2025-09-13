<template>
    <view class="dialog-container theme-student">
        <!-- 主题化头部 -->
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-emoji">👥</text>
                </view>
                <view class="header-info">
                    <text class="header-title">社交焦虑陪伴</text>
                    <text class="header-subtitle">我是您的社交技能教练小社</text>
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
            placeholder="分享您的社交困扰，比如宿舍关系、课堂发言等..." 
            theme="student"
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
            scene: 'social-anxiety',
            welcomeMessage: '你好！我是社交焦虑陪伴师小社👋 很高兴成为您的社交技能教练。\n\n我理解社交焦虑带来的困扰，无论是宿舍相处、课堂发言、加入社团，还是建立友谊，我都会以温暖包容的态度陪伴您，一起练习社交技巧，建立自信。\n\n这里是安全的练习空间，请放心分享您在社交中遇到的困难或想要改善的地方。'
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