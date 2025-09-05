<!-- 风险评估报告详情页面 -->
<!-- file: ariadne/frontend/src/pages/risk-report/report-detail.vue -->
<template>
    <view class="report-detail-page">
        <!-- 页面头部 -->
        <view class="header">
            <text class="title">💙 心理状态评估报告</text>
            <text class="date" v-if="report">{{ formatDate(report.report_generated_time) }}</text>
        </view>

        <!-- 报告内容 -->
        <view class="report-content" v-if="report">
            <!-- 风险等级概览 -->
            <view class="risk-overview" :class="'risk-' + report.overall_risk_level">
                <view class="risk-header">
                    <text class="risk-icon">{{ getRiskIcon(report.overall_risk_level) }}</text>
                    <text class="risk-title">{{ getRiskTitle(report.overall_risk_level) }}</text>
                </view>
                <view class="risk-score">
                    <text class="score-number">{{ report.overall_risk_score.toFixed(1) }}</text>
                    <text class="score-text">/100</text>
                </view>
            </view>

            <!-- 基本统计 -->
            <view class="stats-section">
                <text class="section-title">📊 对话统计</text>
                <view class="stats-grid">
                    <view class="stat-item">
                        <text class="stat-number">{{ report.total_messages }}</text>
                        <text class="stat-label">总消息数</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ report.risk_messages_count }}</text>
                        <text class="stat-label">风险消息</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ report.version }}</text>
                        <text class="stat-label">报告版本</text>
                    </view>
                </view>
            </view>

            <!-- 摘要 -->
            <view class="summary-section" v-if="report.summary">
                <text class="section-title">📝 报告摘要</text>
                <text class="summary-text">{{ report.summary }}</text>
            </view>

            <!-- AI专业分析 -->
            <view class="ai-analysis-section" v-if="report.ai_analysis">
                <text class="section-title">🤖 AI专业分析</text>
                <text class="analysis-text">{{ report.ai_analysis }}</text>
            </view>

            <!-- 检测到的关键词 -->
            <view class="keywords-section" v-if="report.detected_keywords && report.detected_keywords.length > 0">
                <text class="section-title">🔍 检测关键词</text>
                <view class="keywords-list">
                    <text class="keyword-tag" v-for="(keyword, index) in report.detected_keywords" :key="index">
                        {{ keyword }}
                    </text>
                </view>
            </view>

            <!-- 专业建议 -->
            <view class="recommendations-section" v-if="report.recommendations && report.recommendations.length > 0">
                <text class="section-title">💡 专业建议</text>
                <view class="recommendations-list">
                    <view class="recommendation-item" v-for="(rec, index) in report.recommendations" :key="index">
                        <text class="rec-bullet">•</text>
                        <text class="rec-text">{{ rec }}</text>
                    </view>
                </view>
            </view>

            <!-- 时间信息 -->
            <view class="time-info-section">
                <text class="section-title">⏰ 时间信息</text>
                <view class="time-list">
                    <view class="time-item" v-if="report.conversation_start_time">
                        <text class="time-label">对话开始：</text>
                        <text class="time-value">{{ formatDateTime(report.conversation_start_time) }}</text>
                    </view>
                    <view class="time-item" v-if="report.conversation_end_time">
                        <text class="time-label">对话结束：</text>
                        <text class="time-value">{{ formatDateTime(report.conversation_end_time) }}</text>
                    </view>
                    <view class="time-item">
                        <text class="time-label">报告生成：</text>
                        <text class="time-value">{{ formatDateTime(report.report_generated_time) }}</text>
                    </view>
                </view>
            </view>

            <!-- 操作按钮 -->
            <view class="action-buttons">
                <button class="btn btn-secondary" @click="shareReport">📤 分享报告</button>
                <button class="btn btn-primary" @click="getHelp">💙 获取帮助</button>
            </view>

            <!-- 免责声明 -->
            <view class="disclaimer">
                <text class="disclaimer-text">
                    ⚠️ 此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。
                    如需紧急帮助，请拨打心理危机干预热线：400-161-9995
                </text>
            </view>
        </view>

        <!-- 加载状态 -->
        <view class="loading" v-else-if="loading">
            <text>正在加载报告...</text>
        </view>

        <!-- 错误状态 -->
        <view class="error" v-else>
            <text>无法加载报告</text>
            <button class="retry-btn" @click="loadReport">重试</button>
        </view>
    </view>
</template>

<script>
// 引入危机工具类
import { CrisisUtils } from '../../utils/crisisApi.js'

export default {
    data() {
        return {
            report: null,
            loading: true,
            reportId: null
        }
    },

    onLoad(options) {
        this.reportId = options.reportId
        if (this.reportId) {
            this.loadReport()
        }
    },

    methods: {
        /**
         * 加载报告详情
         */
        async loadReport() {
            this.loading = true
            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/risk-assessment/reports/${this.reportId}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.report = response.data
                } else {
                    throw new Error('加载失败')
                }
            } catch (error) {
                console.error('加载报告失败:', error)
                uni.showToast({
                    title: '加载报告失败',
                    icon: 'none'
                })
            } finally {
                this.loading = false
            }
        },

        /**
         * 获取风险图标
         */
        getRiskIcon(level) {
            const icons = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '⚡',
                'low': '✅'
            }
            return icons[level] || '❓'
        },

        /**
         * 获取风险标题
         */
        getRiskTitle(level) {
            const titles = {
                'critical': '高危风险',
                'high': '较高风险',
                'medium': '中等风险',
                'low': '较低风险'
            }
            return titles[level] || '未知风险'
        },

        /**
         * 格式化日期
         */
        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString()
        },

        /**
         * 格式化日期时间
         */
        formatDateTime(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleString()
        },

        /**
         * 分享报告
         */
        shareReport() {
            uni.showActionSheet({
                itemList: ['保存到相册', '分享给朋友', '导出PDF'],
                success: (res) => {
                    switch (res.tapIndex) {
                        case 0:
                            this.saveToAlbum()
                            break
                        case 1:
                            this.shareToFriend()
                            break
                        case 2:
                            this.exportPDF()
                            break
                    }
                }
            })
        },

        /**
         * 获取帮助
         */
        getHelp() {
            CrisisUtils.showHelpOptions()
        },

        /**
         * 保存到相册
         */
        saveToAlbum() {
            uni.showToast({
                title: '功能开发中...',
                icon: 'none'
            })
        },

        /**
         * 分享给朋友
         */
        shareToFriend() {
            uni.share({
                title: '心理状态评估报告',
                summary: this.report.summary,
                href: `#/pages/risk-report/report-detail?reportId=${this.reportId}`
            })
        },

        /**
         * 导出PDF
         */
        exportPDF() {
            uni.showToast({
                title: '功能开发中...',
                icon: 'none'
            })
        }
    }
}
</script>

<style scoped>
.report-detail-page {
    padding: 20rpx;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-bottom: 30rpx;
}

.title {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    color: white;
    margin-bottom: 10rpx;
}

.date {
    display: block;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
}

.report-content {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
}

.risk-overview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-radius: 15rpx;
    margin-bottom: 30rpx;
}

.risk-critical {
    background: linear-gradient(135deg, #ff6b6b, #ee5a52);
    color: white;
}

.risk-high {
    background: linear-gradient(135deg, #feca57, #ff9ff3);
    color: white;
}

.risk-medium {
    background: linear-gradient(135deg, #48dbfb, #0abde3);
    color: white;
}

.risk-low {
    background: linear-gradient(135deg, #1dd1a1, #10ac84);
    color: white;
}

.risk-header {
    display: flex;
    align-items: center;
}

.risk-icon {
    font-size: 40rpx;
    margin-right: 20rpx;
}

.risk-title {
    font-size: 32rpx;
    font-weight: bold;
}

.risk-score {
    text-align: right;
}

.score-number {
    font-size: 48rpx;
    font-weight: bold;
}

.score-text {
    font-size: 24rpx;
    opacity: 0.8;
}

.section-title {
    display: block;
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
}

.stats-section {
    margin-bottom: 30rpx;
}

.stats-grid {
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 32rpx;
    font-weight: bold;
    color: #667eea;
}

.stat-label {
    display: block;
    font-size: 24rpx;
    color: #666;
    margin-top: 10rpx;
}

.summary-section,
.ai-analysis-section {
    margin-bottom: 30rpx;
}

.summary-text,
.analysis-text {
    display: block;
    font-size: 26rpx;
    line-height: 1.6;
    color: #555;
    background: #f8f9fa;
    padding: 20rpx;
    border-radius: 10rpx;
}

.keywords-section {
    margin-bottom: 30rpx;
}

.keywords-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10rpx;
}

.keyword-tag {
    background: #e3f2fd;
    color: #1976d2;
    padding: 10rpx 20rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
}

.recommendations-section {
    margin-bottom: 30rpx;
}

.recommendations-list {
    background: #f8f9fa;
    padding: 20rpx;
    border-radius: 10rpx;
}

.recommendation-item {
    display: flex;
    margin-bottom: 15rpx;
}

.rec-bullet {
    color: #667eea;
    margin-right: 15rpx;
    font-weight: bold;
}

.rec-text {
    flex: 1;
    font-size: 26rpx;
    line-height: 1.5;
    color: #555;
}

.time-info-section {
    margin-bottom: 30rpx;
}

.time-list {
    background: #f8f9fa;
    padding: 20rpx;
    border-radius: 10rpx;
}

.time-item {
    display: flex;
    margin-bottom: 15rpx;
}

.time-label {
    width: 150rpx;
    font-size: 24rpx;
    color: #666;
}

.time-value {
    flex: 1;
    font-size: 24rpx;
    color: #333;
}

.action-buttons {
    display: flex;
    gap: 20rpx;
    margin-bottom: 30rpx;
}

.btn {
    flex: 1;
    padding: 25rpx;
    border-radius: 10rpx;
    font-size: 26rpx;
    text-align: center;
    border: none;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-secondary {
    background: #f8f9fa;
    color: #667eea;
    border: 2rpx solid #667eea;
}

.disclaimer {
    background: #fff3cd;
    padding: 20rpx;
    border-radius: 10rpx;
    border-left: 4rpx solid #ffc107;
}

.disclaimer-text {
    font-size: 22rpx;
    line-height: 1.5;
    color: #856404;
}

.loading,
.error {
    text-align: center;
    padding: 100rpx 0;
    color: white;
}

.retry-btn {
    margin-top: 20rpx;
    background: white;
    color: #667eea;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    border: none;
}
</style>
