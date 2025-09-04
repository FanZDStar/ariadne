/**
 * 聊天页面通用 mixin
 * 用于减少三个聊天页面的代码重复
 * 统一处理聊天逻辑、AI调用、保存等功能
 */

// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL;

// 检查环境变量是否正确配置
if (!BASE_URL) {
    console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
    throw new Error('API基础地址未配置，请检查环境变量 VUE_APP_API_BASE_URL');
}

// 引入危机检测工具
import { CrisisKeywordDetector, CrisisUtils } from './crisisApi.js';

export default {
    data() {
        return {
            chatHistory: [],
            isAiTyping: false,
            hasNewMessages: false,
            sessionId: null,
            scene: '', // 由具体页面设置
            welcomeMessage: '', // 由具体页面设置
            // 危机检测相关
            crisisDetector: null,
            currentRiskLevel: 'low',
            showCrisisWarning: false,
            crisisWarningData: null
        }
    },

    onLoad(options) {
        // 初始化危机检测器
        this.crisisDetector = new CrisisKeywordDetector();

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
                    url: `${BASE_URL}/chat/chat-sessions/${sessionId}`,
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
            // 首先进行危机检测
            await this.performCrisisDetection(message);

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
                    url: `${BASE_URL}/chat/save-chat`,
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
         * 执行危机检测
         */
        async performCrisisDetection(userMessage) {
            try {
                // 前端关键词检测
                const keywordRisk = this.crisisDetector.detectKeywords(userMessage);

                // 调用后端AI分析
                const response = await uni.request({
                    url: `${BASE_URL}/crisis/assess-risk`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        content: userMessage,
                        scene: this.scene,
                        keyword_score: keywordRisk.score,
                        enable_ai_analysis: true  // 启用AI增强分析
                    }
                });

                if (response.statusCode === 200 && response.data) {
                    const riskData = response.data;
                    this.currentRiskLevel = riskData.risk_level;

                    // 根据风险等级显示相应提示
                    if (riskData.risk_level !== 'low') {
                        CrisisUtils.showIntelligentWarning(riskData, keywordRisk);
                        // 记录预警事件
                        this.logCrisisWarning(riskData, keywordRisk);
                    }
                }
            } catch (error) {
                console.error('危机检测失败:', error);
                // 失败时仍然使用前端检测结果
                if (keywordRisk && keywordRisk.level !== 'low') {
                    this.showLocalCrisisWarning(keywordRisk);
                }
            }
        },

        /**
         * 显示本地危机预警
         */
        showLocalCrisisWarning(keywordData) {
            const warningConfig = CrisisUtils.getWarningConfig(keywordData.level);

            uni.showModal({
                title: warningConfig.title,
                content: warningConfig.message + '\n\n检测到可能的风险关键词，建议寻求专业帮助。',
                showCancel: true,
                cancelText: '继续对话',
                confirmText: '获取帮助',
                confirmColor: warningConfig.color,
                success: (res) => {
                    if (res.confirm) {
                        CrisisUtils.showHelpOptions();
                    }
                }
            });
        },

        /**
         * 记录危机预警事件
         */
        async logCrisisWarning(riskData, keywordData) {
            try {
                await uni.request({
                    url: `${BASE_URL}/crisis/warnings`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        content: riskData.content || '',
                        risk_level: riskData.risk_level,
                        risk_score: riskData.risk_score,
                        detected_keywords: keywordData ? keywordData.keywords : [],
                        scene: this.scene,
                        ai_analysis: riskData.ai_analysis || ''
                    }
                });
            } catch (error) {
                console.error('记录危机预警失败:', error);
            }
        },

        /**
         * 调用AI接口获取响应
         * 使用后端统一的prompt管理，不再在前端维护systemPrompt
         */
        async getAIResponse(userMessage) {
            const apiUrl = `${BASE_URL}/ai-dialog`

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
