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
                    content: '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？'
                }
            ],
            isAiTyping: false,
            hasNewMessages: false, // 标记是否有新消息
            sessionId: null, // 如果是从历史记录进入，记录session id
            scene: 'self-dialog' // 当前场景
        }
    },

    onLoad(options) {
        // 如果是从历史记录进入，加载历史对话
        if (options.sessionId) {
            this.sessionId = options.sessionId
            this.loadHistorySession(options.sessionId)
        }
    },

    // 删除自动保存逻辑
    // onUnload() {
    //     // 页面卸载时询问是否保存
    //     if (this.hasNewMessages && this.chatHistory.length > 1) {
    //         // 同步方式保存，避免页面卸载导致异步请求失败
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
            // 添加用户消息到聊天记录
            this.chatHistory.push({
                role: 'user',
                content: message,
                timestamp: new Date()
            })
            this.hasNewMessages = true
            this.isAiTyping = true

            try {
                const response = await this.getAIResponse(message)
                console.log('AI响应内容:', response)
                this.chatHistory.push({
                    role: 'assistant',
                    content: response,
                    timestamp: new Date()
                })
                console.log('聊天历史更新后:', this.chatHistory)
            } catch (error) {
                console.error('AI响应错误:', error)
                this.chatHistory.push({
                    role: 'assistant',
                    content: '抱歉，我现在有些困惑，让我们换个角度继续我们的对话吧。你还有其他想要分享的感受吗？',
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
                        session_id: this.sessionId // 如果是从历史记录进入，传入session_id
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

        // 处理AI打字状态变化
        handleAiTyping(typing) {
            this.isAiTyping = typing
        },

        // 调用AI接口获取响应
        async getAIResponse(userMessage) {
            const apiUrl = 'http://127.0.0.1:8000/ai-dialog'
            
            // 构造历史消息（最多取最近8条消息）
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
                        console.log('后端AI响应:', res)
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
