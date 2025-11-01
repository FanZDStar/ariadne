<template>
    <view class="dialog-container theme-tree-hole">
        <!-- 主题化头部 -->
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-emoji">💕</text>
                </view>
                <view class="header-info">
                    <text class="header-title">恋爱社交实验室</text>
                    <text class="header-subtitle">我是您的恋爱交流教练小爱</text>
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
            placeholder="分享您的恋爱困扰或想练习的社交场景..." 
            theme="tree-hole"
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
            scene: 'love-experiment',
            welcomeMessage: '你好！我是恋爱社交教练小爱💕 很高兴成为您的恋爱交流伙伴。\n\n我理解恋爱中的紧张和不确定，无论是初次约会、表白时机、相处技巧，还是情感表达，我都会以温暖理解的态度陪伴您，一起模拟各种恋爱场景，练习沟通技巧。\n\n这里是安全的练习空间，请放心分享您在恋爱中遇到的困惑或想要练习的场景。'
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