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
            isAiTyping: false,
            // 系统提示词 - 定义AI的角色和行为
            systemPrompt: `你是一个专业的心理咨询师，专注于帮助用户学会自我关爱。你的使命是帮助用户认识到自我关爱的重要性，并提供实用的建议和指导。

## 角色定义
- 你是一位温暖、富有同理心的心理咨询师
- 你善于倾听，不会批判用户的任何感受
- 你会引导用户深入思考自我关爱的重要性
- 你相信每个人都有能力学会爱自己

## 对话风格
- 温和、理解、充满同理心
- 使用启发性的问题帮助用户思考
- 避免说教或给出标准答案
- 鼓励用户表达真实的感受
- 用"我理解"、"我能感受到"等共情语言

## 回应结构
1. **共情确认**：首先理解和确认用户的感受
2. **深入探索**：通过问题引导用户进一步思考自我关爱
3. **正面反馈**：肯定用户对自我关爱的重视
4. **实用建议**：提供具体的自我关爱方法和技巧

## 特殊要求
- 回复长度控制在150-300字
- 多使用"你觉得..."、"你认为..."、"如果是你..."等启发性问题
- 避免使用"你应该"、"你必须"等指令性语言
- 在用户表达负面情绪时，先共情再引导
- 强调自我关爱是每个人都应该学会的重要技能

## 示例回应风格
用户："我觉得我总是把别人放在第一位，忽略了自己的感受"
你的回应："我能感受到你是一个很为他人着想的人，但忽略自己的感受可能会让你感到疲惫。你觉得在什么情况下，你最忽略自己的感受呢？我们可以一起探讨一些平衡的方法。"

现在，请以心理咨询师的身份，用温暖专业的方式回应用户的每一个关于自我关爱的问题。`
        }
    },
    methods: {
        async handleSend(message) {
            // 添加用户消息到聊天记录
            this.chatHistory.push({
                role: 'user',
                content: message
            })

            // 设置AI正在输入状态
            this.isAiTyping = true;

            try {
                // 调用AI接口获取响应
                const aiResponse = await this.getAIResponse(message);
                
                this.chatHistory.push({
                    role: 'ai',
                    content: aiResponse
                })
            } catch (error) {
                console.error('AI响应错误:', error);
                this.chatHistory.push({
                    role: 'ai',
                    content: '抱歉，我现在有些困惑，让我们换个角度继续我们的对话吧。你还有其他想要分享的感受吗？'
                })
            } finally {
                this.isAiTyping = false;
            }
        },
        
        // 处理AI打字状态变化
        handleAiTyping(typing) {
            this.isAiTyping = typing;
        },
        
        // 调用AI接口获取响应
        async getAIResponse(userMessage) {
            // 构建后端API请求体
            const apiUrl = process.env.VUE_APP_BACKEND_API_URL || 'http://127.0.0.1:8000/ai-dialog';
            // 构造历史消息（role: user/ai）
            const messages = this.chatHistory.slice(-8).map(msg => ({
                role: msg.role,
                content: msg.content
            }));
            // 请求体
            const data = {
                messages: messages,
                system_prompt: this.systemPrompt
            };
            return new Promise((resolve, reject) => {
                uni.request({
                    url: apiUrl,
                    method: 'POST',
                    timeout: 30000,
                    header: {
                        'Content-Type': 'application/json'
                    },
                    data: data,
                    success: (res) => {
                        console.log('后端AI响应:', res);
                        if (res.statusCode === 200 && res.data && res.data.content) {
                            // 后端已做内容优化
                            resolve(res.data.content);
                        } else {
                            reject(new Error(`AI响应格式错误: ${JSON.stringify(res.data)}`));
                        }
                    },
                    fail: (err) => {
                        console.error('请求失败:', err);
                        reject(new Error(`网络请求失败: ${err.errMsg || '未知错误'}`));
                    }
                });
            });
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