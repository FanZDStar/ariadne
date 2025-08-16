<!-- src/pages/love-experiment/love-experiment.vue -->
<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">恋爱小尝试</text>
            <text class="subtitle">通过与AI的互动，提升你的恋爱技能</text>
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
            placeholder="请输入你想练习的恋爱话题..." 
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
                    content: '你好！我是你的恋爱技能练习助手。今天我们来练习如何表达爱意吧！你可以告诉我你想对谁表达感情，以及你目前的困扰。'
                }
            ],
            isAiTyping: false
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
            this.isAiTyping = true;
            setTimeout(() => {
                let aiResponse = "";
                
                // 根据用户输入内容给出相关建议
                if (message.includes('表白') || message.includes('表达') || message.includes('爱')) {
                    aiResponse = "表白是一件需要勇气的事情！让我来帮你练习：\n\n1. 选择合适的时机和地点\n2. 真诚地表达你的感受\n3. 给对方回应的空间\n\n你可以试着告诉我，你想对谁表白？";
                } else if (message.includes('聊天') || message.includes('话题') || message.includes('说话')) {
                    aiResponse = "聊天是增进感情的好方法！以下是一些万能话题：\n\n1. 最近看过的电影或书籍\n2. 共同的兴趣爱好\n3. 童年趣事\n4. 对未来的规划\n\n你想练习哪个方面呢？";
                } else if (message.includes('礼物') || message.includes('惊喜')) {
                    aiResponse = "送礼物是表达心意的好方式！记住这几点：\n\n1. 投其所好，了解对方的喜好\n2. 用心准备，不在于价格高低\n3. 选择特殊的日子或创造惊喜时刻\n\n你想为谁准备礼物呢？";
                } else {
                    aiResponse = "这是一个很好的话题！在恋爱中，沟通和理解是最重要的。让我给你一些建议：\n\n1. 保持真诚和开放的态度\n2. 学会倾听对方的想法\n3. 用积极的方式表达自己的需求\n\n你可以和我分享更多细节吗？";
                }
                
                this.chatHistory.push({
                    role: 'ai',
                    content: aiResponse
                })
                
                this.isAiTyping = false;
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