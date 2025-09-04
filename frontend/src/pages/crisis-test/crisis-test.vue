<!-- 心理健康评估测试页面 -->
<!-- file: ariadne/frontend/src/pages/crisis-test/crisis-test.vue -->
<template>
    <view class="crisis-test-page">
        <view class="header">
            <text class="title">心理健康评估测试</text>
            <text class="subtitle">测试心理危机预警系统功能</text>
        </view>

        <!-- 文本检测测试 -->
        <view class="test-section">
            <text class="section-title">🔍 实时关键词检测</text>
            <view class="input-area">
                <textarea v-model="testInput" placeholder="请输入一些文字来测试关键词检测..." class="test-input"
                    @input="onInputChange" />

                <view class="detection-result" v-if="detectionResult">
                    <view class="result-header" :class="'risk-' + detectionResult.riskLevel">
                        <text class="risk-icon">{{ getRiskIcon(detectionResult.riskLevel) }}</text>
                        <text class="risk-text">{{ getRiskText(detectionResult.riskLevel) }}</text>
                    </view>

                    <view class="detected-keywords" v-if="detectionResult.detectedKeywords.length > 0">
                        <text class="keywords-label">检测到的关键词：</text>
                        <text class="keywords-list">{{ detectionResult.detectedKeywords.join(', ') }}</text>
                    </view>

                    <view class="recommendations" v-if="recommendations.length > 0">
                        <text class="rec-label">建议：</text>
                        <view class="rec-item" v-for="(rec, index) in recommendations" :key="index">
                            <text>• {{ rec }}</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 风险评估测试 -->
        <view class="test-section">
            <text class="section-title">📊 风险评估测试</text>

            <view class="assessment-controls">
                <button class="test-btn" @click="performAssessment" :disabled="assessmentLoading">
                    {{ assessmentLoading ? '评估中...' : '执行风险评估' }}
                </button>

                <picker mode="selector" :range="dayOptions" @change="onDayChange">
                    <view class="picker-text">分析周期: {{ selectedDays }}天</view>
                </picker>
            </view>

            <view class="assessment-result" v-if="assessmentResult">
                <view class="result-card" :class="'risk-' + assessmentResult.risk_level">
                    <view class="card-header">
                        <text class="assessment-title">风险评估结果</text>
                        <text class="risk-level">{{ getRiskText(assessmentResult.risk_level) }}</text>
                    </view>

                    <view class="card-content">
                        <view class="score-display">
                            <text class="score-label">风险评分：</text>
                            <text class="score-value">{{ assessmentResult.score.toFixed(1) }}/100</text>
                        </view>

                        <view class="reasons" v-if="assessmentResult.reasons.length > 0">
                            <text class="reasons-title">风险因素：</text>
                            <view class="reason-item" v-for="(reason, index) in assessmentResult.reasons" :key="index">
                                <text>• {{ reason }}</text>
                            </view>
                        </view>

                        <view class="recommendations" v-if="assessmentResult.recommendations.length > 0">
                            <text class="rec-title">专业建议：</text>
                            <view class="rec-item" v-for="(rec, index) in assessmentResult.recommendations"
                                :key="index">
                                <text>• {{ rec }}</text>
                            </view>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 预警记录测试 -->
        <view class="test-section">
            <text class="section-title">⚠️ 预警记录</text>

            <view class="warnings-controls">
                <button class="test-btn secondary" @click="loadWarnings">
                    {{ warningsLoading ? '加载中...' : '获取预警记录' }}
                </button>

                <switch @change="onUnresolvedChange" :checked="showUnresolvedOnly">
                    <text class="switch-label">仅未解决</text>
                </switch>
            </view>

            <view class="warnings-list" v-if="warnings.length > 0">
                <view class="warning-item" v-for="warning in warnings" :key="warning.warning_id"
                    :class="'warning-' + warning.risk_level">
                    <view class="warning-header">
                        <text class="warning-title">{{ warning.title }}</text>
                        <text class="warning-time">{{ formatTime(warning.created_at) }}</text>
                    </view>

                    <text class="warning-desc">{{ warning.description }}</text>

                    <view class="warning-meta">
                        <text class="warning-type">类型: {{ getWarningType(warning.warning_type) }}</text>
                        <text class="warning-score">评分: {{ warning.score.toFixed(1) }}</text>
                    </view>

                    <view class="warning-actions" v-if="!warning.is_resolved">
                        <button class="resolve-btn" @click="resolveWarning(warning.warning_id)">
                            标记为已解决
                        </button>
                    </view>
                </view>
            </view>

            <view class="no-warnings" v-else-if="!warningsLoading && warningsLoaded">
                <text>暂无预警记录</text>
            </view>
        </view>

        <!-- 系统信息 -->
        <view class="system-info">
            <text class="info-title">🔧 系统信息</text>
            <text class="info-item">API地址: {{ apiBase }}</text>
            <text class="info-item">当前用户: {{ currentUser || '未登录' }}</text>
            <text class="info-item">系统状态: {{ systemStatus }}</text>
        </view>
    </view>
</template>

<script>
import { CrisisAPI, CrisisKeywordDetector, CrisisUtils } from '@/utils/crisisApi.js'

export default {
    name: 'CrisisTest',

    data() {
        return {
            // 文本检测
            testInput: '',
            detectionResult: null,
            recommendations: [],

            // 风险评估
            assessmentResult: null,
            assessmentLoading: false,
            selectedDays: 14,
            dayOptions: ['7天', '14天', '30天'],

            // 预警记录
            warnings: [],
            warningsLoading: false,
            warningsLoaded: false,
            showUnresolvedOnly: false,

            // 系统信息
            apiBase: 'http://localhost:8000/api',
            currentUser: null,
            systemStatus: '检查中...'
        }
    },

    onLoad() {
        this.checkSystemStatus()
        this.getCurrentUser()
    },

    methods: {
        // 实时检测输入内容
        onInputChange() {
            if (!this.testInput.trim()) {
                this.detectionResult = null
                this.recommendations = []
                return
            }

            // 使用本地关键词检测
            this.detectionResult = CrisisKeywordDetector.quickDetect(this.testInput)

            // 获取建议
            this.recommendations = CrisisUtils.getRecommendations(
                this.detectionResult.riskLevel,
                this.detectionResult.categories
            )

            // 如果检测到高风险，可以显示特殊提醒
            if (['high', 'critical'].includes(this.detectionResult.riskLevel)) {
                this.showRiskAlert()
            }
        },

        // 执行风险评估
        async performAssessment() {
            this.assessmentLoading = true
            try {
                this.assessmentResult = await CrisisAPI.assessRisk(this.selectedDays)

                uni.showToast({
                    title: '评估完成',
                    icon: 'success'
                })

                // 如果是高风险，显示额外提醒
                if (['high', 'critical'].includes(this.assessmentResult.risk_level)) {
                    this.showHighRiskAlert()
                }

            } catch (error) {
                console.error('风险评估失败:', error)
                uni.showToast({
                    title: '评估失败: ' + error.message,
                    icon: 'none',
                    duration: 3000
                })
            } finally {
                this.assessmentLoading = false
            }
        },

        // 加载预警记录
        async loadWarnings() {
            this.warningsLoading = true
            try {
                this.warnings = await CrisisAPI.getWarnings({
                    days: 30,
                    unresolvedOnly: this.showUnresolvedOnly
                })
                this.warningsLoaded = true

                uni.showToast({
                    title: `加载了 ${this.warnings.length} 条记录`,
                    icon: 'success'
                })

            } catch (error) {
                console.error('加载预警记录失败:', error)
                uni.showToast({
                    title: '加载失败: ' + error.message,
                    icon: 'none',
                    duration: 3000
                })
            } finally {
                this.warningsLoading = false
            }
        },

        // 解决预警
        async resolveWarning(warningId) {
            try {
                await CrisisAPI.resolveWarning(warningId, '测试页面标记为已解决')

                uni.showToast({
                    title: '已标记为解决',
                    icon: 'success'
                })

                // 重新加载预警记录
                this.loadWarnings()

            } catch (error) {
                console.error('解决预警失败:', error)
                uni.showToast({
                    title: '操作失败',
                    icon: 'none'
                })
            }
        },

        // 检查系统状态
        async checkSystemStatus() {
            try {
                const response = await uni.request({
                    url: `${this.apiBase.replace('/api', '')}/health`,
                    method: 'GET'
                })

                if (response.statusCode === 200) {
                    this.systemStatus = '正常运行'
                } else {
                    this.systemStatus = '服务异常'
                }
            } catch (error) {
                this.systemStatus = '连接失败'
                console.error('系统状态检查失败:', error)
            }
        },

        // 获取当前用户信息
        getCurrentUser() {
            const token = uni.getStorageSync('access_token')
            if (token) {
                // 这里可以解析token获取用户信息，简化处理
                this.currentUser = '已登录用户'
            } else {
                this.currentUser = '未登录'
            }
        },

        // 事件处理
        onDayChange(e) {
            const dayValues = [7, 14, 30]
            this.selectedDays = dayValues[e.detail.value]
        },

        onUnresolvedChange(e) {
            this.showUnresolvedOnly = e.detail.value
        },

        // 显示风险提醒
        showRiskAlert() {
            if (this.detectionResult.riskLevel === 'critical') {
                uni.showModal({
                    title: '⚠️ 检测到紧急风险',
                    content: '如果你正在经历困难，请记住你并不孤单。是否需要查看帮助资源？',
                    confirmText: '查看帮助',
                    cancelText: '我知道了',
                    success: (res) => {
                        if (res.confirm) {
                            this.showEmergencyHelp()
                        }
                    }
                })
            }
        },

        showHighRiskAlert() {
            uni.showModal({
                title: '关怀提醒',
                content: '检测到你可能需要一些关怀和支持。如需帮助，请不要犹豫寻求专业支持。',
                confirmText: '了解更多',
                cancelText: '谢谢关心'
            })
        },

        showEmergencyHelp() {
            uni.showActionSheet({
                itemList: [
                    '心理援助热线 400-161-9995',
                    '紧急求助 110',
                    '医疗急救 120'
                ],
                success: (res) => {
                    const phones = ['400-161-9995', '110', '120']
                    if (phones[res.tapIndex]) {
                        uni.makePhoneCall({
                            phoneNumber: phones[res.tapIndex]
                        })
                    }
                }
            })
        },

        // 工具函数
        getRiskIcon(level) {
            const icons = {
                'low': '✅',
                'medium': '⚠️',
                'high': '🚨',
                'critical': '🆘'
            }
            return icons[level] || '❓'
        },

        getRiskText(level) {
            const texts = {
                'low': '低风险',
                'medium': '中等风险',
                'high': '高风险',
                'critical': '紧急风险'
            }
            return texts[level] || '未知'
        },

        getWarningType(type) {
            const types = {
                'mood_trend': '心情趋势',
                'keyword_alert': '关键词预警',
                'ai_analysis': 'AI分析',
                'behavior_pattern': '行为模式'
            }
            return types[type] || '未知类型'
        },

        formatTime(timeString) {
            const date = new Date(timeString)
            return date.toLocaleString('zh-CN')
        }
    }
}
</script>

<style scoped>
.crisis-test-page {
    padding: 20rpx;
    background: #f5f5f5;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-bottom: 40rpx;
}

.title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.subtitle {
    font-size: 26rpx;
    color: #666;
}

.test-section {
    background: white;
    border-radius: 16rpx;
    padding: 24rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.test-input {
    width: 100%;
    min-height: 200rpx;
    border: 2rpx solid #eee;
    border-radius: 8rpx;
    padding: 16rpx;
    font-size: 28rpx;
    margin-bottom: 16rpx;
}

.detection-result {
    border: 2rpx solid #eee;
    border-radius: 8rpx;
    padding: 16rpx;
    background: #fafafa;
}

.result-header {
    display: flex;
    align-items: center;
    gap: 8rpx;
    margin-bottom: 12rpx;
    padding: 8rpx 12rpx;
    border-radius: 6rpx;
}

.risk-low {
    background: #e8f5e8;
}

.risk-medium {
    background: #fff3e0;
}

.risk-high {
    background: #ffebee;
}

.risk-critical {
    background: #ffebee;
}

.risk-icon {
    font-size: 24rpx;
}

.risk-text {
    font-weight: bold;
    font-size: 26rpx;
}

.detected-keywords {
    margin-bottom: 12rpx;
}

.keywords-label,
.rec-label {
    font-size: 24rpx;
    color: #666;
    font-weight: bold;
}

.keywords-list {
    font-size: 24rpx;
    color: #333;
    margin-left: 8rpx;
}

.assessment-controls,
.warnings-controls {
    display: flex;
    gap: 16rpx;
    align-items: center;
    margin-bottom: 20rpx;
}

.test-btn {
    padding: 16rpx 24rpx;
    background: #007AFF;
    color: white;
    border: none;
    border-radius: 8rpx;
    font-size: 26rpx;
}

.test-btn.secondary {
    background: #34C759;
}

.test-btn:disabled {
    background: #ccc;
}

.picker-text {
    padding: 16rpx;
    background: #f8f9fa;
    border-radius: 8rpx;
    font-size: 26rpx;
}

.result-card {
    border: 2rpx solid #eee;
    border-radius: 12rpx;
    overflow: hidden;
}

.card-header {
    padding: 20rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.assessment-title {
    font-size: 28rpx;
    font-weight: bold;
}

.card-content {
    padding: 20rpx;
    background: white;
}

.score-display {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.score-label {
    font-size: 26rpx;
    color: #666;
}

.score-value {
    font-size: 32rpx;
    font-weight: bold;
    margin-left: 12rpx;
    color: #007AFF;
}

.reasons,
.recommendations {
    margin-bottom: 16rpx;
}

.reasons-title,
.rec-title {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.reason-item,
.rec-item {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 4rpx;
}

.warning-item {
    border: 2rpx solid #eee;
    border-radius: 8rpx;
    padding: 16rpx;
    margin-bottom: 12rpx;
    background: white;
}

.warning-high {
    border-left: 6rpx solid #FF9800;
}

.warning-critical {
    border-left: 6rpx solid #F44336;
}

.warning-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8rpx;
}

.warning-title {
    font-weight: bold;
    font-size: 26rpx;
}

.warning-time {
    font-size: 22rpx;
    color: #999;
}

.warning-desc {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 8rpx;
    line-height: 1.4;
}

.warning-meta {
    display: flex;
    gap: 20rpx;
    margin-bottom: 8rpx;
}

.warning-type,
.warning-score {
    font-size: 22rpx;
    color: #999;
}

.resolve-btn {
    padding: 8rpx 16rpx;
    background: #34C759;
    color: white;
    border: none;
    border-radius: 4rpx;
    font-size: 22rpx;
}

.system-info {
    background: white;
    border-radius: 16rpx;
    padding: 24rpx;
    margin-top: 20rpx;
}

.info-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.info-item {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 8rpx;
    display: block;
}

.no-warnings {
    text-align: center;
    padding: 40rpx;
    color: #999;
    font-size: 26rpx;
}

.switch-label {
    font-size: 24rpx;
    color: #666;
    margin-left: 8rpx;
}
</style>
