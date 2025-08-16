<!-- src/pages/self-dialog/self-dialog.vue -->
<template>
    <view class="dialog-container">
        <view class="header">
            <image class="header-image" src="../../static/self-dialog.png" mode="widthFix"></image>
        </view>

        <view class="content">
            <ChatMessages 
                ref="chatMessages"
                :messages="chatHistory" 
                @ai-typing="handleAiTyping" 
            />
        </view>
        
        <!-- 底部输入框，类似导航栏效果 -->
        <ChatInput 
            class="fixed-input"
            placeholder="请描述你在感情中遇到的问题或困惑..." 
            @send="handleSend" 
            :disabled="isAiTyping"
        />
    </view>
</template>

<script>
import ChatMessages from '@/components/ChatMessages.vue'
import ChatInput from '@/components/ChatInput.vue'

export default {
    components: {
        ChatMessages,
        ChatInput
    },
    data() {
        return {
            chatHistory: [
                {
                    role: 'ai',
                    content: '你好！我是你的情感助手。请告诉我你在感情中遇到了什么问题或困惑？'
                }
            ],
            isAiTyping: false // 添加AI打字状态
        }
    },
    methods: {
        handleSend(message) {
            // 添加用户消息到聊天记录
            this.chatHistory.push({
                role: 'user',
                content: message
            })

            // 模拟AI响应延迟，提升用户体验
            setTimeout(() => {
                const aiResponse = "感谢你的分享。从你的描述中，我能感受到你的困惑和真诚。让我们一起来分析一下这个问题，帮助你更好地理解自己在感情中的表现。建议你可以：\n\n1. 诚实面对自己的感受\n2. 学会表达而非压抑情感\n3. 给彼此一些时间和空间\n4. 关注自己的成长和需求"; 
                
                this.chatHistory.push({
                    role: 'ai',
                    content: aiResponse
                })
            }, 1000) // 1秒延迟，模拟AI思考
        },
        
        // 处理AI打字状态变化
        handleAiTyping(typing) {
            this.isAiTyping = typing;
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0; /* 为底部输入框留出空间 */
    background-color: #f8f8f8;
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
    flex-shrink: 0;
    text-align: center; /* 居中显示图片 */
}

.header-image {
    width: 100%; /* 或者指定具体宽度 */
    max-width: 600rpx; /* 限制最大宽度 */
    margin: 0 auto; /* 居中对齐 */
}
.title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 15rpx;
}

.subtitle {
    font-size: 26rpx;
    color: #999;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx; /* 增加间距以适应多行输入框 */
}

/* 固定在底部的输入框样式，类似导航栏 */
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