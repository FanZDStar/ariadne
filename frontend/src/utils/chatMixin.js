/**
 * 聊天页面通用 mixin
 * 用于减少三个聊天页面的代码重复
 * 统一处理聊天逻辑、AI调用、保存等功能
 * 增强版：包含自动风险评估和报告功能
 */

// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL;

// 检查环境变量是否正确配置
if (!BASE_URL) {
    console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
    throw new Error('API基础地址未配置，请检查环境变量 VUE_APP_API_BASE_URL');
}

// 引入危机检测相关工具
import { CrisisKeywordDetector } from './crisisKeywordDetector.js';
import { CrisisUtils } from './crisisApi.js';

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
            // 风险评估相关
            conversationStartTime: null,
            hasRiskDetected: false,
            autoSaveEnabled: true,
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
        this.checkAndShowPreviousReport();
    },

    onUnload() {
        // 页面卸载时自动生成风险评估报告
        this.handlePageUnload();
    },

    methods: {
        /**
         * AI 调用方法
         */
        async callAIAPI(messages, scene = 'general') {
            return new Promise((resolve, reject) => {
                uni.request({
                    url: `${BASE_URL}/ai-dialog?t=${Date.now()}`,  // 添加时间戳避免缓存
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        messages: messages,
                        scene: scene
                    },
                    success: (res) => {
                        if (res.statusCode === 200) {
                            resolve(res.data);
                        } else {
                            reject(new Error('AI请求失败'));
                        }
                    },
                    fail: (err) => {
                        let errorMsg = '网络连接失败，请检查网络后重试';
                        if (err.errMsg && err.errMsg.includes('timeout')) {
                            errorMsg = 'AI响应超时，请重试';
                        }
                        reject(new Error(errorMsg));
                    }
                });
            });
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
                    this.markReportAsViewed(report.id);
                }
            });
        },

        /**
         * 查看完整报告
         */
        viewFullReport(report) {
            uni.navigateTo({
                url: `/pages/risk-report/report-detail?reportId=${report.id}`
            });
        },

        /**
         * 标记报告为已查看
         */
        async markReportAsViewed(reportId) {
            try {
                await uni.request({
                    url: `${BASE_URL}/risk-assessment/mark-viewed`,
                    method: 'PUT',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: { report_id: reportId }
                });
            } catch (error) {
                console.log('标记报告已查看失败:', error);
            }
        },

        /**
         * 处理页面卸载事件 - 生成风险评估报告
         */
        async handlePageUnload() {
            if (!this.sessionId || !this.riskDetectedInSession) return;

            try {
                // 生成风险评估报告
                await uni.request({
                    url: `${BASE_URL}/risk-assessment/generate-report`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        session_id: this.sessionId,
                        scene: this.scene,
                        conversation_start_time: this.conversationStartTime,
                        conversation_end_time: new Date()
                    }
                });

                console.log('✅ 风险评估报告已生成');
            } catch (error) {
                console.log('生成风险评估报告失败:', error);
            }
        },

        /**
         * 增强的危机检测方法（包含自动保存）
         */
        async performCrisisDetection(userMessage) {
            if (!this.crisisDetector) return;

            try {
                // 执行危机检测
                const detectionResult = await this.crisisDetector.detectCrisis(userMessage);

                if (detectionResult.isRisk) {
                    console.log('🚨 检测到风险内容:', detectionResult);

                    this.currentRiskLevel = detectionResult.riskLevel;
                    this.showCrisisWarning = true;
                    this.crisisWarningData = detectionResult;
                    this.riskDetectedInSession = true;

                    // 自动保存会话
                    if (this.autoSaveEnabled) {
                        await this.autoSaveSession();
                    }

                    // 显示风险提示
                    this.showRiskDetectionAlert(detectionResult);
                }
            } catch (error) {
                console.error('危机检测失败:', error);
            }
        },

        /**
         * 自动保存会话
         */
        async autoSaveSession() {
            if (!this.sessionId && this.chatHistory.length > 0) {
                try {
                    await this.saveSession();

                    uni.showToast({
                        title: '💾 对话已自动保存',
                        icon: 'success',
                        duration: 2000
                    });
                } catch (error) {
                    console.log('自动保存失败:', error);
                }
            }
        },

        /**
         * 显示风险检测提醒
         */
        showRiskDetectionAlert(detectionResult) {
            const riskMessages = {
                'low': '💙 我注意到您的情绪状态，如需帮助请随时告诉我',
                'medium': '⚠️ 我感受到您可能正在经历一些困扰，建议与朋友或专业人士交流',
                'high': '🚨 您提到的内容让我担心，强烈建议寻求专业心理健康支持',
                'critical': '🆘 请立即寻求专业帮助！如有紧急情况，请拨打心理危机干预热线：400-161-9995'
            };

            uni.showModal({
                title: '💙 关爱提醒',
                content: riskMessages[detectionResult.riskLevel] || riskMessages['medium'],
                showCancel: true,
                cancelText: '我知道了',
                confirmText: '获取帮助',
                success: (res) => {
                    if (res.confirm) {
                        CrisisUtils.showHelpOptions();
                    }
                }
            });
        },

        /**
         * 处理 AI 输入状态（用于 ChatMessages 组件）
         */
        handleAiTyping(typing) {
            this.isAiTyping = typing;
        },

        /**
         * 处理发送消息事件（用于接收 ChatInput 组件的 send 事件）
         */
        handleSend(content) {
            this.sendMessage(content);
        },

        /**
         * 发送消息方法（增强版）
         */
        async sendMessage(content) {
            if (!content.trim()) return;

            // 添加用户消息到聊天历史
            this.chatHistory.push({
                role: 'user',
                content: content
            });

            // 执行危机检测
            await this.performCrisisDetection(content);

            // 显示AI正在输入
            this.isAiTyping = true;

            try {
                // 调用AI API
                const aiResponse = await this.callAIAPI(this.chatHistory, this.scene);

                // 添加AI响应到聊天历史
                this.chatHistory.push({
                    role: 'assistant',
                    content: aiResponse.content  // 修改为正确的字段名
                });

                this.hasNewMessages = true;
            } catch (error) {
                console.error('AI调用失败:', error);
                uni.showToast({
                    title: error.message || 'AI调用失败',
                    icon: 'none',
                    duration: 3000
                });
            } finally {
                this.isAiTyping = false;
            }
        },

        /**
         * 保存聊天历史（用于 SaveButton 组件）
         */
        saveChatHistory() {
            this.saveSession();
        },

        /**
         * 保存会话
         */
        async saveSession() {
            if (this.chatHistory.length === 0) {
                uni.showToast({
                    title: '暂无对话内容可保存',
                    icon: 'none'
                });
                return;
            }

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat/save-chat`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        scene: this.scene,
                        messages: this.chatHistory
                    }
                });

                if (response.statusCode === 200) {
                    this.sessionId = response.data.id;  // 修改为正确的字段名
                    uni.showToast({
                        title: '保存成功',
                        icon: 'success'
                    });
                }
            } catch (error) {
                console.error('保存失败:', error);
                uni.showToast({
                    title: '保存失败',
                    icon: 'none'
                });
            }
        },

        /**
         * 加载历史会话
         */
        async loadHistorySession(sessionId) {
            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat/chat-sessions/${sessionId}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    this.chatHistory = response.data.messages || [];
                }
            } catch (error) {
                console.error('加载历史会话失败:', error);
            }
        },

        /**
         * 清空聊天记录
         */
        clearChat() {
            uni.showModal({
                title: '确认清空',
                content: '确定要清空当前对话吗？此操作不可恢复。',
                success: (res) => {
                    if (res.confirm) {
                        this.chatHistory = this.welcomeMessage ? [{
                            role: 'assistant',
                            content: this.welcomeMessage
                        }] : [];
                        this.sessionId = null;
                        this.hasNewMessages = false;
                        this.riskDetectedInSession = false;
                        this.conversationStartTime = new Date();
                    }
                }
            });
        }
    }
};
