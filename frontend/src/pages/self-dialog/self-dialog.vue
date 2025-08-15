<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">自己与自己的对话</text>
            <text class="subtitle">反思感情中的言行举止，获得AI引导和建议</text>
        </view>

        <view class="content">
            <ChatBox 
                :messages="chatHistory" 
                placeholder="请描述你在感情中遇到的问题或困惑..." 
                @send="handleSend" 
            />
        </view>
    </view>
</template>

<script>
import ChatBox from '@/components/ChatBox.vue';

export default {
    components: {
        ChatBox
    },
    data() {
        return {
            chatHistory: [
                {
                    role: 'ai',
                    content: '你好！我是你的情感助手。请告诉我你在感情中遇到了什么问题或困惑？'
                }
            ]
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
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
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
}
</style>