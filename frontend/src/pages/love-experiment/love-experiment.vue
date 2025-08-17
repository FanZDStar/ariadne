<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">恋爱尝试</text>
            <text class="subtitle">模拟恋爱场景，练习表达和沟通技巧</text>
        </view>

        <view class="content">
            <ChatMessages 
                ref="chatMessages"
                :messages="chatHistory" 
                @ai-typing="handleAiTyping" 
            />
        </view>
        
        <!-- 底部输入框 -->
        <ChatInput 
            class="fixed-input"
            placeholder="请输入你想尝试的恋爱场景或话题..." 
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

export default {
    components: {
        ChatMessages,
        ChatInput,
        SaveButton
    },
    data() {
        return {
            chatHistory: [
                {
                    role: 'assistant',
                    content: '你好！我是你的恋爱练习伙伴。我们可以一起模拟各种恋爱场景，帮助你练习表达和沟通技巧。你想尝试什么样的场景呢？'
                }
            ],
            isAiTyping: false,
            hasNewMessages: false,
            sessionId: null,
            scene: 'love-experiment'
        }
    },

    onLoad(options) {
        if (options.sessionId) {
            this.sessionId = options.sessionId
            this.loadHistorySession(options.sessionId)
        }
    },

    // 删除自动保存逻辑
    // onUnload() {
    //     if (this.hasNewMessages && this.chatHistory.length > 1) {
    //         this.saveChatHistorySync()
    //     }
    // },

    methods: {
        async loadHistorySession(sessionId) {
            try {
                const response = await uni.request({
                    url: `http://127.0.0.1:8000/chat/chat-sessions/${sessionId}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.chatHistory = response.data.messages.map(msg => ({
                        role: msg.role,
                        content: msg.content,
                        timestamp: new Date(msg.created_at)
                    }))
                }
            } catch (error) {
                console.error('加载历史对话失败:', error)
                uni.showToast({
                    title: '加载历史对话失败',
                    icon: 'none'
                })
            }
        },

        async handleSend(message) {
            this.chatHistory.push({
                role: 'user',
                content: message,
                timestamp: new Date()
            })
            this.hasNewMessages = true
            this.isAiTyping = true

            try {
                const response = await this.getAIResponse(message)
                this.chatHistory.push({
                    role: 'assistant',
                    content: response,
                    timestamp: new Date()
                })
            } catch (error) {
                console.error('AI响应错误:', error)
                this.chatHistory.push({
                    role: 'assistant',
                    content: '抱歉，我没能理解你的意思。你能换个方式表达吗？',
                    timestamp: new Date()
                })
            } finally {
                this.isAiTyping = false
            }
        },

        async saveChatHistory() {
            try {
                const messages = this.chatHistory.filter(msg => msg.role === 'user' || msg.role === 'assistant').map(msg => ({
                    role: msg.role,
                    content: msg.content
                }))

                await uni.request({
                    url: 'http://127.0.0.1:8000/chat/save-chat',
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        scene: this.scene,
                        messages: messages,
                        session_id: this.sessionId
                    }
                })

                uni.showToast({
                    title: '对话已保存',
                    icon: 'success'
                })
                this.hasNewMessages = false
            } catch (error) {
                console.error('保存对话失败:', error)
                uni.showToast({
                    title: '保存失败',
                    icon: 'none'
                })
            }
        },

        handleAiTyping(typing) {
            this.isAiTyping = typing
        },

        async getAIResponse(userMessage) {
            const apiUrl = 'http://127.0.0.1:8000/ai-dialog'
            
            const messages = this.chatHistory.slice(-8).map(msg => ({
                role: msg.role,
                content: msg.content
            }))

            return new Promise((resolve, reject) => {
                uni.request({
                    url: apiUrl,
                    method: 'POST',
                    timeout: 30000,
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        messages: messages,
                        scene: this.scene
                    },
                    success: (res) => {
                        if (res.statusCode === 200 && res.data && res.data.content) {
                            resolve(res.data.content)
                        } else {
                            reject(new Error(`AI响应格式错误: ${JSON.stringify(res.data)}`))
                        }
                    },
                    fail: (err) => {
                        reject(err)
                    }
                })
            })
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
    margin-bottom: 120rpx; /* 只为输入框留出空间 */
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