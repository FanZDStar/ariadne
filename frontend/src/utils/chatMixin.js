/**
 * 聊天页面通用 mixin
 * 用于减少三个聊天页面的代码重复
 * 统一处理聊天逻辑、AI调用、保存等功能
 */
export default {
    data() {
        return {
            chatHistory: [],
            isAiTyping: false,
            hasNewMessages: false,
            sessionId: null,
            scene: '', // 由具体页面设置
            welcomeMessage: '', // 由具体页面设置
        }
    },

    onLoad(options) {
        // 设置欢迎消息
        if (this.welcomeMessage) {
            this.chatHistory = [{
                role: 'assistant',
                content: this.welcomeMessage
            }]
        }

        // 如果是从历史记录进入，加载历史对话
        if (options.sessionId) {
            this.sessionId = options.sessionId
            this.loadHistorySession(options.sessionId)
        }
    },

    methods: {
        /**
         * 加载历史对话
         */
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

        /**
         * 处理用户发送消息
         */
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

        /**
         * 保存聊天历史
         */
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

        /**
         * 处理AI打字状态变化
         */
        handleAiTyping(typing) {
            this.isAiTyping = typing
        },

        /**
         * 调用AI接口获取响应
         * 使用后端统一的prompt管理，不再在前端维护systemPrompt
         */
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
                        scene: this.scene // 通过scene让后端选择对应的prompt
                    },
                    success: (res) => {
                        console.log('后端AI响应:', res)
                        if (res.statusCode === 200 && res.data && res.data.content) {
                            resolve(res.data.content)
                        } else if (res.statusCode === 401) {
                            // 认证失败，提示用户重新登录
                            uni.showToast({
                                title: '登录已过期，请重新登录',
                                icon: 'none'
                            })
                            // 可以在这里跳转到登录页
                            // uni.reLaunch({ url: '/pages/login/login' })
                            reject(new Error('认证失败'))
                        } else {
                            reject(new Error(`AI响应格式错误: ${JSON.stringify(res.data)}`))
                        }
                    },
                    fail: (err) => {
                        console.error('AI请求失败:', err)
                        // 提供用户友好的错误信息
                        let errorMsg = '网络连接失败，请检查网络后重试'
                        if (err.errMsg && err.errMsg.includes('timeout')) {
                            errorMsg = 'AI服务响应超时，请稍后重试'
                        }
                        reject(new Error(errorMsg))
                    }
                })
            })
        }
    }
}
