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
            autoSaveEnabled: false,  // 默认不启用自动保存，只有检测到风险或从数据库加载时才启用
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
         * 检查会话是否有心理评估报告
         */
        async checkSessionReport() {
            if (!this.sessionId) return false;

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/risk-assessment/session/${this.sessionId}/has-report`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    return response.data.has_report;
                }
            } catch (error) {
                console.log('检查会话报告失败:', error);
            }
            return false;
        },

        /**
         * 获取会话的心理评估报告
         */
        async getSessionReport() {
            if (!this.sessionId) return null;

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/risk-assessment/session/${this.sessionId}/report`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    return response.data;
                } else if (response.statusCode === 404) {
                    return null; // 没有报告
                }
            } catch (error) {
                console.log('获取会话报告失败:', error);
                if (error.statusCode === 404) {
                    return null;
                }
            }
            return null;
        },

        /**
         * 显示心理评估报告
         */
        async showPsychologicalReport() {
            const report = await this.getSessionReport();
            if (!report) return;

            const riskLevelText = {
                'critical': '🚨 高危',
                'high': '⚠️ 较高',
                'medium': '⚡ 中等',
                'low': '✅ 较低'
            };

            const content = `基于您的对话内容，系统为您生成了心理状态评估报告：

风险等级：${riskLevelText[report.overall_risk_level] || report.overall_risk_level}
风险分数：${report.overall_risk_score.toFixed(1)}/100
对话消息：${report.total_messages}条

📋 报告摘要：
${report.summary}

是否查看完整的AI分析报告？`;

            uni.showModal({
                title: '🧠 心理状态评估报告',
                content: content,
                showCancel: true,
                cancelText: '稍后查看',
                confirmText: '查看详情',
                success: (res) => {
                    if (res.confirm) {
                        this.viewDetailedReport(report);
                    }
                }
            });
        },

        /**
         * 查看详细报告
         */
        viewDetailedReport(report) {
            // 跳转到报告详情页面
            uni.navigateTo({
                url: `/pages/risk-report/report-detail?reportId=${report.report_id}`,
                success: () => {
                    console.log('跳转到报告详情页面成功');
                },
                fail: (err) => {
                    console.error('跳转到报告详情页面失败:', err);
                    // 如果跳转失败，显示简单的模态框作为备选方案
                    uni.showModal({
                        title: '🧠 AI心理分析',
                        content: report.ai_analysis.substring(0, 300) + (report.ai_analysis.length > 300 ? '...\n\n请稍后重试查看完整分析' : ''),
                        showCancel: false,
                        confirmText: '我知道了'
                    });
                }
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
         * 检查会话的自动保存状态
         */
        async checkAutoSaveStatus() {
            if (!this.sessionId) return false;

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat-history/chat-sessions/${this.sessionId}/auto-save-status`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    this.autoSaveEnabled = response.data.auto_save_enabled;
                    console.log(`✅ 会话 ${this.sessionId} 自动保存状态: ${this.autoSaveEnabled}`);
                    return this.autoSaveEnabled;
                }
            } catch (error) {
                console.log('检查自动保存状态失败:', error);
            }
            return false;
        },

        /**
         * 为会话启用自动保存（用于手动保存的会话）
         */
        async enableSessionAutoSave() {
            if (!this.sessionId) return;

            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat-history/chat-sessions/${this.sessionId}/enable-auto-save`,
                    method: 'PUT',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    console.log(`✅ 会话 ${this.sessionId} 已启用自动保存`);
                    return true;
                }
            } catch (error) {
                console.log('启用自动保存失败:', error);
            }
            return false;
        },        /**
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
         * 增强的危机检测方法（标记风险但不立即保存）
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

                    // 不在这里立即保存，等AI回复后再保存
                    console.log('🔍 标记会话需要自动保存');

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
         * 自动保存对话以获取星点奖励
         */
        async autoSaveForStarReward() {
            // 检查token是否存在
            const token = uni.getStorageSync('access_token');
            if (!token) {
                console.error('❌ 没有access_token，无法保存');
                return;
            }

            try {
                console.log('💾 自动保存对话以获取星点奖励...');
                await this.saveSession();
            } catch (error) {
                console.error('❌ 自动保存失败:', error);
                // 静默失败，不影响用户对话体验
            }
        },

        /**
         * 处理风险相关逻辑（不包括常规保存）
         */
        async handleRiskLogic() {
            if (this.sessionId && this.riskDetectedInSession) {
                // 如果是因为检测到风险而触发，检查是否生成了心理评估报告
                setTimeout(async () => {
                    try {
                        const hasReport = await this.checkSessionReport();
                        if (hasReport) {
                            console.log('✅ 检测到新的心理评估报告');
                            // 显示温和的提示，不打断用户的对话流程
                            uni.showToast({
                                title: '已生成心理评估报告',
                                icon: 'none',
                                duration: 2000
                            });

                            // 延迟显示报告详情
                            setTimeout(() => {
                                this.showPsychologicalReport();
                            }, 3000);
                        }
                    } catch (error) {
                        console.log('检查心理评估报告失败:', error);
                    }
                }, 5000); // 5秒后检查，给AI生成报告足够时间
            }
        },

        /**
         * 处理风险会话的自动保存逻辑（保留原有逻辑用于兼容）
         */
        async handleRiskSessionSave() {
            // 如果检测到风险或者会话已启用自动保存，则进行保存
            if (!this.riskDetectedInSession && !this.autoSaveEnabled) {
                console.log('❌ 不满足自动保存条件');
                console.log('riskDetectedInSession:', this.riskDetectedInSession);
                console.log('autoSaveEnabled:', this.autoSaveEnabled);
                return;
            }

            // 检查token是否存在
            const token = uni.getStorageSync('access_token');
            if (!token) {
                console.error('❌ 没有access_token，无法保存');
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }

            try {
                console.log('💾 风险对话自动保存中...');
                console.log('当前会话ID:', this.sessionId);
                console.log('当前聊天历史长度:', this.chatHistory.length);
                console.log('聊天历史内容:', JSON.stringify(this.chatHistory, null, 2));

                await this.saveSession();

                // 保存成功后检查会话的自动保存状态
                if (this.sessionId) {
                    await this.checkAutoSaveStatus();

                    // 如果是因为检测到风险而触发的自动保存，检查是否生成了心理评估报告
                    if (this.riskDetectedInSession) {
                        setTimeout(async () => {
                            try {
                                const hasReport = await this.checkSessionReport();
                                if (hasReport) {
                                    console.log('✅ 自动保存后检测到新的心理评估报告');
                                    // 显示温和的提示，不打断用户的对话流程
                                    uni.showToast({
                                        title: '已生成心理评估报告',
                                        icon: 'none',
                                        duration: 2000
                                    });

                                    // 延迟显示报告详情
                                    setTimeout(() => {
                                        this.showPsychologicalReport();
                                    }, 3000);
                                }
                            } catch (error) {
                                console.log('检查心理评估报告失败:', error);
                            }
                        }, 5000); // 5秒后检查，给AI生成报告足够时间
                    }
                }
            } catch (error) {
                console.log('风险会话保存失败:', error);
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

            // 检查当前会话的自动保存状态
            if (this.sessionId) {
                await this.checkAutoSaveStatus();
            }

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

                // 每次对话后自动保存以触发星点奖励
                console.log('� 自动保存对话以获取星点奖励...');
                await this.autoSaveForStarReward();

                // 如果检测到风险或会话已启用自动保存，处理风险相关逻辑
                if (this.riskDetectedInSession || this.autoSaveEnabled) {
                    console.log('🚨 触发风险处理逻辑...');
                    await this.handleRiskLogic();
                }

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
                const requestData = {
                    scene: this.scene,
                    messages: this.chatHistory,
                    session_id: this.sessionId // 如果有sessionId，则更新现有会话
                };

                console.log('保存请求数据:', JSON.stringify(requestData, null, 2));

                const response = await uni.request({
                    url: `${BASE_URL}/chat/save-chat`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: requestData
                });

                console.log('保存响应:', response);

                if (response.statusCode === 200) {
                    if (!this.sessionId) {
                        this.sessionId = response.data.id;  // 首次保存时设置sessionId
                        console.log('设置新会话ID:', this.sessionId);
                    }

                    // 处理星点奖励
                    if (response.data.star_reward && response.data.star_reward.is_rewarded) {
                        this.handleStarReward(response.data.star_reward);
                    }

                    // 重置新消息标志
                    this.hasNewMessages = false;

                    // 手动保存的会话应该启用自动保存，便于日后继续会话时自动保存
                    this.autoSaveEnabled = true;

                    // 检查并更新数据库中的自动保存状态
                    if (this.sessionId) {
                        await this.enableSessionAutoSave();
                    }

                    // 处理星点奖励
                    if (response.data.star_reward && response.data.star_reward.is_rewarded && response.data.star_reward.show_toast) {
                        const reward = response.data.star_reward;
                        uni.showToast({
                            title: `${reward.description}！`,
                            icon: 'success',
                            duration: 2000
                        });
                    } else {
                        uni.showToast({
                            title: '保存成功',
                            icon: 'success'
                        });
                    }

                    // 保存成功后，延迟检查是否生成了心理评估报告
                    setTimeout(async () => {
                        try {
                            const hasReport = await this.checkSessionReport();
                            if (hasReport) {
                                console.log('✅ 检测到新的心理评估报告');
                                // 延迟显示报告，让用户先看到保存成功的提示
                                setTimeout(() => {
                                    this.showPsychologicalReport();
                                }, 2000);
                            }
                        } catch (error) {
                            console.log('检查心理评估报告失败:', error);
                        }
                    }, 3000); // 3秒后检查，给后台任务足够时间生成报告
                }
            } catch (error) {
                console.error('保存失败:', error);
                console.error('保存响应详情:', error.response || error);

                if (error.statusCode === 401) {
                    console.error('❌ 认证失败，token可能过期');
                    uni.showToast({
                        title: '登录已过期，请重新登录',
                        icon: 'none'
                    });
                } else {
                    uni.showToast({
                        title: '保存失败',
                        icon: 'none'
                    });
                }
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

                    // 检查该会话的自动保存状态
                    await this.checkAutoSaveStatus();

                    console.log(`✅ 加载历史会话 ${sessionId}，自动保存状态: ${this.autoSaveEnabled}`);

                    // 检查该会话是否有心理评估报告，如果有且未查看过，则提示用户
                    setTimeout(async () => {
                        try {
                            const hasReport = await this.checkSessionReport();
                            if (hasReport) {
                                const report = await this.getSessionReport();
                                if (report && !report.is_viewed) {
                                    console.log('📊 发现未查看的心理评估报告');
                                    uni.showToast({
                                        title: '发现心理评估报告',
                                        icon: 'none',
                                        duration: 2000
                                    });

                                    // 延迟显示报告
                                    setTimeout(() => {
                                        this.showPsychologicalReport();
                                    }, 2000);
                                }
                            }
                        } catch (error) {
                            console.log('检查历史会话报告失败:', error);
                        }
                    }, 1000);
                }
            } catch (error) {
                console.error('加载历史会话失败:', error);
            }
        },

        /**
         * 自动保存对话以获取星点奖励
         */
        async autoSaveForStarReward() {
            try {
                console.log('💫 开始自动保存以获取星点奖励...');
                const requestData = {
                    scene: this.scene,
                    messages: this.chatHistory,
                    session_id: this.sessionId
                };

                const response = await uni.request({
                    url: `${BASE_URL}/chat/save-chat`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: requestData
                });

                if (response.statusCode === 200) {
                    if (!this.sessionId) {
                        this.sessionId = response.data.id;
                        console.log('设置新会话ID:', this.sessionId);
                    }

                    // 处理星点奖励
                    if (response.data.star_reward && response.data.star_reward.is_rewarded) {
                        this.handleStarReward(response.data.star_reward);
                    }

                    console.log('✅ 自动保存成功');
                } else {
                    console.error('❌ 自动保存失败:', response);
                }
            } catch (error) {
                console.error('❌ 自动保存异常:', error);
            }
        },

        /**
         * 处理星点奖励
         */
        handleStarReward(rewardInfo) {
            console.log('⭐ 收到星点奖励:', rewardInfo);

            // 只在前5条消息时显示toast提示
            if (rewardInfo.show_toast) {
                uni.showToast({
                    title: `+${rewardInfo.earned_points}⭐`,
                    icon: 'none',
                    duration: 2000
                });

                console.log(`⭐ 显示奖励提示: +${rewardInfo.earned_points}星点`);
            } else {
                console.log(`⭐ 获得奖励但不显示提示: +${rewardInfo.earned_points}星点`);
            }
        },

        /**
         * 处理风险相关逻辑（从原来的自动保存逻辑中分离）
         */
        async handleRiskLogic() {
            try {
                // 这里可以添加风险相关的特殊处理逻辑
                // 比如额外的风险评估、报告生成等
                console.log('🚨 处理风险相关逻辑...');
            } catch (error) {
                console.error('❌ 风险逻辑处理失败:', error);
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
                        this.autoSaveEnabled = false;  // 重置自动保存状态
                        this.conversationStartTime = new Date();
                    }
                }
            });
        }
    }
};
