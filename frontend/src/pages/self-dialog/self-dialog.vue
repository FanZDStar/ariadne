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
                    content: '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？'
                }
            ],
            isAiTyping: false,
            // 系统提示词 - 定义AI的角色和行为
            systemPrompt: `你是一个专业的情感咨询师，名字叫阿德涅（Ariadne）。你的使命是帮助用户进行自我对话和情感反思。

## 角色定义
- 你是一位温暖、富有同理心的情感咨询师
- 你善于倾听，不会批判用户的任何感受
- 你会引导用户深入思考，而不是直接给出答案
- 你相信每个人都有自己的答案，只需要正确的引导

## 对话风格
- 温和、理解、充满同理心
- 使用启发性的问题帮助用户思考
- 避免说教或给出标准答案
- 鼓励用户表达真实的感受
- 用"我理解"、"我能感受到"等共情语言

## 回应结构
1. **共情确认**：首先理解和确认用户的感受
2. **深入探索**：通过问题引导用户进一步思考
3. **正面反馈**：肯定用户的勇气和成长
4. **温和建议**：如果合适，提供一些温和的建议

## 特殊要求
- 回复长度控制在150-300字
- 多使用"你觉得..."、"你认为..."、"如果是你..."等启发性问题
- 避免使用"你应该"、"你必须"等指令性语言
- 在用户表达负面情绪时，先共情再引导
- 记住你在帮助用户"自己与自己对话"，重点是引导用户自我发现

## 示例回应风格
用户："我总是在恋爱中很没有安全感"
你的回应："我能理解这种不安全感会让你感到很困扰。安全感的缺失往往反映了我们内心深处的一些担忧。你觉得这种不安全感主要来源于什么呢？是对方的某些行为，还是你内心的某些想法？"

现在，请以阿德涅的身份，用温暖专业的方式回应用户的每一个问题。`
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
            const apiUrl = process.env.VUE_APP_AI_API_URL || 'https://api.suanli.cn/v1/chat/completions';
            const apiKey = process.env.VUE_APP_AI_API_KEY || 'sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo';
            const model = process.env.VUE_APP_AI_MODEL || 'free:Qwen3-30B-A3B';
            
            return new Promise((resolve, reject) => {
                // 构建完整的对话上下文
                const messages = this.buildConversationMessages(userMessage);
                
                uni.request({
                    url: apiUrl,
                    method: 'POST',
                    timeout: 30000, // 30秒超时
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    },
                    data: {
                        model: model,
                        messages: messages,
                        temperature: 0.7, // 稍微增加一些创造性
                        max_tokens: 800,  // 限制回复长度
                        top_p: 0.9       // 控制回复质量
                    },
                    success: (res) => {
                        console.log('AI响应:', res);
                        if (res.statusCode === 200 && res.data.choices && res.data.choices.length > 0) {
                            const content = res.data.choices[0].message.content;
                            // 简单的内容过滤和优化
                            const optimizedContent = this.optimizeAIResponse(content);
                            resolve(optimizedContent);
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
        },
        
        // 构建对话上下文
        buildConversationMessages(currentMessage) {
            const messages = [];
            
            // 添加系统提示词
            messages.push({
                role: 'system',
                content: this.systemPrompt
            });
            
            // 添加最近的对话历史（保留最近8轮对话，避免token过多）
            const recentHistory = this.chatHistory.slice(-8);
            recentHistory.forEach(msg => {
                if (msg.role === 'user') {
                    messages.push({
                        role: 'user',
                        content: msg.content
                    });
                } else if (msg.role === 'ai') {
                    messages.push({
                        role: 'assistant',
                        content: msg.content
                    });
                }
            });
            
            // 添加当前用户消息
            messages.push({
                role: 'user',
                content: currentMessage
            });
            
            console.log('发送给AI的完整对话:', messages);
            return messages;
        },
        
        // 优化AI回复内容
        // 优化AI回复内容
optimizeAIResponse(content) {
    // 移除 <think> 标签及其内容
    let optimized = content
        .replace(/<think>[\s\S]*?<\/think>/gi, '') // 移除完整的think标签和内容
        .replace(/<think>[\s\S]*/gi, '')           // 移除未闭合的think标签
        .replace(/我不想展示.*?因为这会影响用户体验/gi, '') // 移除特定的思考内容
        .replace(/^(AI|助手|阿德涅)[:：]\s*/i, '')
        .replace(/^(我是|作为)[^，。]*[，。]\s*/i, '')
        .trim();
    
    // 移除可能的其他AI标识或元信息
    optimized = optimized
        .replace(/\[.*?\]/g, '')              // 移除方括号内容
        .replace(/（.*?思考.*?）/g, '')        // 移除包含"思考"的括号内容
        .replace(/\*.*?思考.*?\*/g, '')        // 移除星号包围的思考内容
        .replace(/【.*?】/g, '')               // 移除中文方括号内容
        .replace(/^\s*[-*•]\s*/gm, '')        // 移除行首的列表符号
        .replace(/\n\s*\n/g, '\n')           // 合并多个空行
        .trim();
    
    // 确保回复不会太短
    if (optimized.length < 20) {
        optimized = "我理解你的感受。能告诉我更多关于这个情况的细节吗？这样我能更好地陪伴你进行这场自我对话。";
    }
    
    // 确保回复不会太长
    if (optimized.length > 500) {
        optimized = optimized.substring(0, 500) + "...";
    }
    
    // 如果过滤后内容为空，提供默认回复
    if (!optimized || optimized.length < 5) {
        optimized = "我正在认真思考你的话。你能再详细说说这个情况吗？我想更好地理解你的感受。";
    }
    
    return optimized;
}
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 30rpx;
    padding-bottom: 0;
    background-color: #f8f8f8;
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
    flex-shrink: 0;
    text-align: center;
}

.header-image {
    width: 100%;
    max-width: 600rpx;
    margin: 0 auto;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 120rpx;
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
</style>