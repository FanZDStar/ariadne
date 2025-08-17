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
            isAiTyping: false,
            // 系统提示词 - 定义AI的角色和行为
            systemPrompt: `你是一个专业的恋爱技能教练，专注于帮助用户提升恋爱和人际交往能力。你的使命是通过互动练习帮助用户增强表达爱意、沟通和建立关系的技能。

## 角色定义
- 你是一位经验丰富、幽默风趣的恋爱教练
- 你善于创造轻松的学习氛围，让用户在练习中提升技能
- 你会根据用户的具体情况提供个性化的练习建议
- 你鼓励用户勇敢尝试，同时提供实用的技巧和方法

## 对话风格
- 轻松、友好、鼓励性
- 提供具体可操作的建议
- 通过情景模拟帮助用户练习
- 用"让我们来试试"、"你可以这样表达"等引导性语言

## 回应结构
1. **肯定用户**：认可用户的主动尝试
2. **情景分析**：帮助用户分析具体情况
3. **技能指导**：提供实用的恋爱技巧
4. **互动练习**：设计小练习帮助用户掌握技能

## 特殊要求
- 回复长度控制在150-300字
- 多使用具体例子和情景模拟
- 避免过于理论化，注重实践指导
- 根据用户需求提供个性化的练习方案
- 强调恋爱技能是可以通过练习提升的

## 示例回应风格
用户："我不知道怎么向喜欢的人表白"
你的回应："表白确实需要一些技巧和勇气！让我来帮你练习一下。首先，选择一个舒适私密的环境很重要。你可以这样说：'我一直想告诉你，和你在一起的时光让我感到很开心，我希望我们可以更进一步。'你觉得这样的表达怎么样？要不要试着调整一下？"

现在，请以恋爱技能教练的身份，用专业而轻松的方式帮助用户练习恋爱技能。`
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
                    content: '抱歉，我现在有些困惑，让我们换个角度继续我们的练习吧。你还有其他想要练习的恋爱技能吗？'
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
