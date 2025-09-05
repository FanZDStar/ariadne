/**
 * 聊天页面通用 mixin
 * 用于减少三个聊天页面的代码重复
 * 统一处理聊天逻辑、AI调用、保存等功能
 */

// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000';

// 引入危机检测
import { CrisisKeywordDetector, CrisisUtils } from './crisisApi.js'

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
            crisisWarningData: null,
            // 新增：会话管理和风险评估
            conversationStartTime: null,
            hasRiskDetected: false,
            autoSaveEnabled: false,
            riskDetectedInSession: false
        }
    },

    onLoad(options) {
        // 初始化危机检测器
        this.crisisDetector = new CrisisKeywordDetector();

        // 记录对话开始时间
        this.conversationStartTime = new Date();

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

        // 检查并显示上次的风险评估报告
        this.checkAndShowPreviousReport()
    },

    onUnload() {
        // 页面卸载时，如果有新对话且检测到风险，生成评估报告
        this.handlePageUnload()
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
                // 调用 AI 接口获取回复
                const aiResponse = await this.callAI()

                // 添加 AI 回复到聊天记录
                this.chatHistory.push({
                    role: 'assistant',
                    content: aiResponse,
                    timestamp: new Date()
                })
            } catch (error) {
                console.error('AI 调用失败:', error)
                this.chatHistory.push({
                    role: 'assistant',
                    content: '抱歉，我暂时无法回复。请稍后再试。',
                    timestamp: new Date()
                })
            } finally {
                this.isAiTyping = false
            }
        },

        /**
         * 保存聊天记录
         */
        async saveChatHistory() {
            if (!this.sessionId) {
                // 生成新的会话ID
                this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
            }

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat/save-session`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        session_id: this.sessionId,
                        scene: this.scene,
                        messages: this.chatHistory.map(msg => ({
                            role: msg.role,
                            content: msg.content
                        }))
                    }
                })

                if (response.statusCode === 200) {
                    this.hasNewMessages = false
                    uni.showToast({
                        title: '保存成功',
                        icon: 'success'
                    })
                } else {
                    throw new Error('保存失败')
                }
            } catch (error) {
                console.error('保存聊天记录失败:', error)
                uni.showToast({
                    title: '保存失败',
                    icon: 'none'
                })
            }
        },

        /**
         * 处理AI打字状态
         */
        handleAiTyping(typing) {
            this.isAiTyping = typing
        },

        /**
         * 危机检测
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
                        this.riskDetectedInSession = true; // 标记本次会话检测到风险

                        CrisisUtils.showIntelligentWarning(riskData, keywordRisk);
                        // 记录预警事件
                        this.logCrisisWarning(riskData, keywordRisk);

                        // 自动保存会话
                        await this.autoSaveSession();
                    }
                }
            } catch (error) {
                console.error('危机检测失败:', error);
                // 失败时仍然使用前端检测结果
                if (keywordRisk && keywordRisk.level !== 'low') {
                    this.riskDetectedInSession = true;
                    this.showLocalCrisisWarning(keywordRisk);
                    // 即使后端失败也要自动保存
                    await this.autoSaveSession();
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
         * 调用AI接口
         */
        async callAI() {
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
                            reject(new Error('认证失败'))
                        } else {
                            reject(new Error(`AI响应格式错误: ${JSON.stringify(res.data)}`))
                        }
                    },
                    fail: (err) => {
                        console.error('AI请求失败:', err)
                        let errorMsg = '网络连接失败，请检查网络后重试'
                        if (err.errMsg && err.errMsg.includes('timeout')) {
                            errorMsg = 'AI响应超时，请重试'
                        }
                        reject(new Error(errorMsg))
                    }
                })
            })
        },

        /**
         * 检查并显示上次的风险评估报告
         */
        async checkAndShowPreviousReport() {
            if (!this.sessionId) return;

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/risk-assessment/latest-report/${this.sessionId}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200 && response.data && !response.data.is_viewed) {
                    // 显示风险评估报告
                    this.showRiskAssessmentReport(response.data);
                }
            } catch (error) {
                console.log('获取风险评估报告失败:', error);
            }
        },

        /**
         * 显示风险评估报告弹窗
         */
        showRiskAssessmentReport(report) {
            const riskLevelText = {
                'critical': '🚨 高危',
                'high': '⚠️ 较高',
                'medium': '⚡ 中等',
                'low': '✅ 较低'
            };

            const content = `上次对话风险评估结果：

风险等级：${riskLevelText[report.overall_risk_level] || report.overall_risk_level}
风险分数：${report.overall_risk_score.toFixed(1)}/100
对话消息：${report.total_messages}条（${report.risk_messages_count}条检测到风险）

${report.summary}

AI专业分析：
${report.ai_analysis.substring(0, 100)}...

是否查看完整报告？`;

            uni.showModal({
                title: '💙 心理状态评估报告',
                content: content,
                showCancel: true,
                cancelText: '稍后查看',
                confirmText: '查看详情',
                success: (res) => {
                    if (res.confirm) {
                        this.viewFullReport(report);
                    }
                    // 标记为已查看
                    this.markReportAsViewed(report.report_id);
                }
            });
        },

        /**
         * 查看完整报告
         */
        viewFullReport(report) {
            // 跳转到报告详情页面或显示详细信息
            uni.navigateTo({
                url: `/pages/risk-report/report-detail?reportId=${report.report_id}`
            });
        },

        /**
         * 标记报告为已查看
         */
        async markReportAsViewed(reportId) {
            try {
                await uni.request({
                    url: `${BASE_URL}/risk-assessment/mark-viewed`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        report_id: reportId
                    }
                });
            } catch (error) {
                console.log('标记报告已查看失败:', error);
            }
        },

        /**
         * 页面卸载时处理
         */
        async handlePageUnload() {
            // 如果有新对话且检测到风险，生成评估报告
            if (this.hasNewMessages && this.riskDetectedInSession && this.sessionId) {
                try {
                    await uni.request({
                        url: `${BASE_URL}/risk-assessment/generate-report`,
                        method: 'POST',
                        header: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                        },
                        data: {
                            session_id: this.sessionId,
                            scene: this.scene,
                            conversation_start_time: this.conversationStartTime?.toISOString()
                        }
                    });
                    console.log('风险评估报告已生成');
                } catch (error) {
                    console.log('生成风险评估报告失败:', error);
                }
            }
        },

        /**
         * 自动保存会话（当检测到风险时触发）
         */
        async autoSaveSession() {
            if (!this.sessionId) {
                // 生成新的会话ID
                this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            }

            try {
                await this.saveChatHistory();
                this.autoSaveEnabled = true;
                console.log('会话已自动保存');

                uni.showToast({
                    title: '💾 对话已自动保存',
                    icon: 'success',
                    duration: 2000
                });
            } catch (error) {
                console.log('自动保存失败:', error);
            }
        }
    }
}
