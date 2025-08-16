<!-- src/pages/love-yourself/love-yourself.vue -->
<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">爱他人先爱自己</text>
            <text class="subtitle">学会爱自己，才能更好地爱他人</text>
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
            placeholder="分享你在自我关爱方面的困惑或想法..." 
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
                    content: '你好！我是你的自我关爱助手。爱他人之前，先要学会爱自己。请告诉我你在自我关爱方面有什么困惑或想法？'
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
                if (message.includes('价值') || message.includes('自信') || message.includes(' worth')) {
                    aiResponse = "自我价值感是爱自己的基础！以下几个方面可以帮助你提升自我价值感：\n\n1. 认可自己的优点和成就\n2. 接纳自己的不完美\n3. 设定并实现小目标\n4. 培养自己的兴趣爱好\n\n你能分享一下你觉得自己有哪些优点吗？";
                } else if (message.includes('边界') || message.includes('拒绝') || message.includes(' boundaries')) {
                    aiResponse = "学会设立边界是爱自己的重要表现！健康的边界包括：\n\n🛡️ 保护自己：\n- 学会说'不'\n- 不过度迎合他人\n- 保护自己的时间和精力\n\n🤝 平衡关系：\n- 表达自己的需求\n- 尊重他人的边界\n\n你在设立边界方面有什么困难吗？";
                } else if (message.includes('照顾') || message.includes('关爱') || message.includes(' care')) {
                    aiResponse = "自我关爱是爱自己的具体行动！试试这些方法：\n\n💝 日常关爱：\n- 保证充足睡眠\n- 健康饮食\n- 适度运动\n\n🧠 心理关爱：\n- 正面自我对话\n- 给自己独处时间\n- 做让自己开心的事\n\n你平时会怎样关爱自己呢？";
                } else if (message.includes('原谅') || message.includes('宽恕') || message.includes(' forgive')) {
                    aiResponse = "自我宽恕是爱自己的重要一环！学会原谅自己：\n\n🌟 接纳过去：\n- 承认错误但不沉溺其中\n- 从错误中学习成长\n- 给自己改正的机会\n\n🌱 向前看：\n- 专注于当下和未来\n- 用行动证明自己的改变\n\n你是否在某些事情上难以原谅自己？";
                } else {
                    aiResponse = "你提到了一个很重要的话题！爱自己是终身的课题。记住这几个要点：\n\n❤️ 自我接纳：接受完整的自己\n⚖️ 平衡付出：在关爱他人和关爱自己之间找到平衡\n🌱 持续成长：不断学习成为更好的自己\n\n你想深入探讨哪个方面呢？";
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