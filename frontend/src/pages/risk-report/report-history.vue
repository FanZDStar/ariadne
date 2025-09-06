<!-- 风险评估报告历史页面 -->
<!-- file: ariadne/frontend/src/pages/risk-report/report-history.vue -->
<template>
    <view class="report-history-page">
        <!-- 页面头部 -->
        <view class="header">
            <text class="title">📈 心理状态历史</text>
            <text class="subtitle">追踪您的心理健康变化</text>
        </view>

        <!-- 统计概览 -->
        <view class="overview-section" v-if="statistics">
            <view class="stats-card">
                <view class="stat-item">
                    <text class="stat-number">{{ statistics.total_reports }}</text>
                    <text class="stat-label">总报告数</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ statistics.avg_risk_score.toFixed(1) }}</text>
                    <text class="stat-label">平均风险分</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ statistics.improvement_trend }}%</text>
                    <text class="stat-label">改善趋势</text>
                </view>
            </view>
        </view>

        <!-- 筛选器 -->
        <view class="filter-section">
            <picker mode="selector" :value="filterIndex" :range="filterOptions" @change="onFilterChange">
                <view class="filter-picker">
                    <text>{{ filterOptions[filterIndex] }}</text>
                    <text class="picker-arrow">▼</text>
                </view>
            </picker>
        </view>

        <!-- 报告列表 -->
        <view class="reports-section">
            <view class="report-card" v-for="(report, index) in filteredReports" :key="report.id"
                @click="viewReport(report)">
                <!-- 报告头部 -->
                <view class="report-header">
                    <view class="risk-badge" :class="'risk-' + report.overall_risk_level">
                        <text class="risk-icon">{{ getRiskIcon(report.overall_risk_level) }}</text>
                        <text class="risk-text">{{ getRiskTitle(report.overall_risk_level) }}</text>
                    </view>
                    <text class="report-date">{{ formatDate(report.report_generated_time) }}</text>
                </view>

                <!-- 报告内容预览 -->
                <view class="report-preview">
                    <text class="preview-text" v-if="report.summary">
                        {{ truncateText(report.summary, 100) }}
                    </text>
                    <text class="preview-text" v-else>
                        风险评分：{{ report.overall_risk_score.toFixed(1) }}/100
                    </text>
                </view>

                <!-- 报告统计 -->
                <view class="report-stats">
                    <view class="stat-chip">
                        <text>💬 {{ report.total_messages }}条消息</text>
                    </view>
                    <view class="stat-chip" v-if="report.risk_messages_count > 0">
                        <text>⚠️ {{ report.risk_messages_count }}条风险</text>
                    </view>
                    <view class="stat-chip">
                        <text>📊 v{{ report.version }}</text>
                    </view>
                </view>

                <!-- 趋势指示器 -->
                <view class="trend-indicator" v-if="index < reports.length - 1">
                    <view class="trend-arrow" :class="getTrendClass(report, reports[index + 1])">
                        <text>{{ getTrendArrow(report, reports[index + 1]) }}</text>
                    </view>
                    <text class="trend-text">
                        {{ getTrendText(report, reports[index + 1]) }}
                    </text>
                </view>
            </view>

            <!-- 空状态 -->
            <view class="empty-state" v-if="filteredReports.length === 0 && !loading">
                <text class="empty-icon">📊</text>
                <text class="empty-title">暂无报告</text>
                <text class="empty-desc">开始聊天后，系统会自动生成心理状态评估报告</text>
                <button class="empty-btn" @click="goToChat">开始聊天</button>
            </view>
        </view>

        <!-- 加载更多 -->
        <view class="load-more" v-if="hasMore && !loading">
            <button class="load-more-btn" @click="loadMore">加载更多</button>
        </view>

        <!-- 加载状态 -->
        <view class="loading" v-if="loading">
            <text>正在加载...</text>
        </view>

        <!-- 浮动操作按钮 -->
        <view class="fab-container">
            <button class="fab" @click="showExportOptions">
                <text class="fab-icon">📤</text>
            </button>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            reports: [],
            statistics: null,
            loading: false,
            hasMore: true,
            page: 1,
            pageSize: 10,
            filterIndex: 0,
            filterOptions: ['全部报告', '最近一周', '最近一月', '最近三月', '高风险报告']
        }
    },

    computed: {
        filteredReports() {
            let filtered = [...this.reports]

            switch (this.filterIndex) {
                case 1: // 最近一周
                    filtered = this.filterByDays(filtered, 7)
                    break
                case 2: // 最近一月
                    filtered = this.filterByDays(filtered, 30)
                    break
                case 3: // 最近三月
                    filtered = this.filterByDays(filtered, 90)
                    break
                case 4: // 高风险报告
                    filtered = filtered.filter(report =>
                        ['critical', 'high'].includes(report.overall_risk_level)
                    )
                    break
            }

            return filtered
        }
    },

    onLoad() {
        this.loadReports()
        this.loadStatistics()
    },

    methods: {
        /**
         * 加载报告列表
         */
        async loadReports(isLoadMore = false) {
            if (this.loading) return

            this.loading = true
            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/risk-assessment/reports-history`,
                    method: 'GET',
                    data: {
                        page: isLoadMore ? this.page : 1,
                        page_size: this.pageSize
                    },
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    // 后端直接返回数组，不是包含在reports字段中
                    const newReports = response.data || []

                    if (isLoadMore) {
                        this.reports = [...this.reports, ...newReports]
                    } else {
                        this.reports = newReports
                    }

                    this.hasMore = newReports.length === this.pageSize
                    this.page = isLoadMore ? this.page + 1 : 2
                } else {
                    throw new Error('加载失败')
                }
            } catch (error) {
                console.error('加载报告列表失败:', error)
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                })
            } finally {
                this.loading = false
            }
        },

        /**
         * 加载统计信息
         */
        async loadStatistics() {
            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/risk-assessment/statistics`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.statistics = response.data
                }
            } catch (error) {
                console.error('加载统计信息失败:', error)
            }
        },

        /**
         * 加载更多
         */
        loadMore() {
            this.loadReports(true)
        },

        /**
         * 筛选器变化
         */
        onFilterChange(e) {
            this.filterIndex = e.detail.value
        },

        /**
         * 按天数筛选
         */
        filterByDays(reports, days) {
            const now = new Date()
            const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000)

            return reports.filter(report => {
                const reportDate = new Date(report.report_generated_time)
                return reportDate > cutoff
            })
        },

        /**
         * 查看报告详情
         */
        viewReport(report) {
            uni.navigateTo({
                url: `/pages/risk-report/report-detail?reportId=${report.report_id}`
            })
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
                'critical': '高危',
                'high': '较高',
                'medium': '中等',
                'low': '较低'
            }
            return titles[level] || '未知'
        },

        /**
         * 格式化日期
         */
        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            const now = new Date()
            const diff = now.getTime() - date.getTime()
            const days = Math.floor(diff / (1000 * 60 * 60 * 24))

            if (days === 0) {
                return '今天'
            } else if (days === 1) {
                return '昨天'
            } else if (days < 7) {
                return `${days}天前`
            } else {
                return date.toLocaleDateString()
            }
        },

        /**
         * 截断文本
         */
        truncateText(text, maxLength) {
            if (!text) return ''
            return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
        },

        /**
         * 获取趋势类别
         */
        getTrendClass(current, previous) {
            if (!previous) return ''

            const currentScore = current.overall_risk_score
            const previousScore = previous.overall_risk_score

            if (currentScore < previousScore) {
                return 'trend-improving'
            } else if (currentScore > previousScore) {
                return 'trend-worsening'
            } else {
                return 'trend-stable'
            }
        },

        /**
         * 获取趋势箭头
         */
        getTrendArrow(current, previous) {
            if (!previous) return ''

            const currentScore = current.overall_risk_score
            const previousScore = previous.overall_risk_score

            if (currentScore < previousScore) {
                return '↓'
            } else if (currentScore > previousScore) {
                return '↑'
            } else {
                return '→'
            }
        },

        /**
         * 获取趋势文本
         */
        getTrendText(current, previous) {
            if (!previous) return ''

            const currentScore = current.overall_risk_score
            const previousScore = previous.overall_risk_score
            const diff = Math.abs(currentScore - previousScore)

            if (currentScore < previousScore) {
                return `改善 ${diff.toFixed(1)}分`
            } else if (currentScore > previousScore) {
                return `上升 ${diff.toFixed(1)}分`
            } else {
                return '保持稳定'
            }
        },

        /**
         * 前往聊天页面
         */
        goToChat() {
            uni.switchTab({
                url: '/pages/index/index'
            })
        },

        /**
         * 显示导出选项
         */
        showExportOptions() {
            uni.showActionSheet({
                itemList: ['导出PDF报告', '导出Excel统计', '生成分享链接'],
                success: (res) => {
                    switch (res.tapIndex) {
                        case 0:
                            this.exportPDF()
                            break
                        case 1:
                            this.exportExcel()
                            break
                        case 2:
                            this.generateShareLink()
                            break
                    }
                }
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
        },

        /**
         * 导出Excel
         */
        exportExcel() {
            uni.showToast({
                title: '功能开发中...',
                icon: 'none'
            })
        },

        /**
         * 生成分享链接
         */
        generateShareLink() {
            uni.showToast({
                title: '功能开发中...',
                icon: 'none'
            })
        }
    }
}
</script>

<style scoped>
.report-history-page {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20rpx;
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

.subtitle {
    display: block;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
}

.overview-section {
    margin-bottom: 30rpx;
}

.stats-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15rpx;
    padding: 30rpx;
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    color: #667eea;
}

.stat-label {
    display: block;
    font-size: 22rpx;
    color: #666;
    margin-top: 10rpx;
}

.filter-section {
    margin-bottom: 30rpx;
}

.filter-picker {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 25rpx;
    padding: 20rpx 30rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.picker-arrow {
    color: #667eea;
}

.reports-section {
    margin-bottom: 100rpx;
}

.report-card {
    background: white;
    border-radius: 15rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    position: relative;
}

.report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
}

.risk-badge {
    display: flex;
    align-items: center;
    padding: 10rpx 20rpx;
    border-radius: 20rpx;
}

.risk-critical {
    background: #ffebee;
    color: #c62828;
}

.risk-high {
    background: #fff3e0;
    color: #ef6c00;
}

.risk-medium {
    background: #e3f2fd;
    color: #1565c0;
}

.risk-low {
    background: #e8f5e8;
    color: #2e7d32;
}

.risk-icon {
    margin-right: 10rpx;
}

.risk-text {
    font-size: 24rpx;
    font-weight: bold;
}

.report-date {
    font-size: 22rpx;
    color: #999;
}

.report-preview {
    margin-bottom: 20rpx;
}

.preview-text {
    font-size: 26rpx;
    line-height: 1.5;
    color: #555;
}

.report-stats {
    display: flex;
    gap: 15rpx;
    margin-bottom: 15rpx;
}

.stat-chip {
    background: #f5f5f5;
    padding: 8rpx 15rpx;
    border-radius: 15rpx;
    font-size: 22rpx;
    color: #666;
}

.trend-indicator {
    display: flex;
    align-items: center;
    margin-top: 20rpx;
    padding-top: 20rpx;
    border-top: 1rpx solid #eee;
}

.trend-arrow {
    width: 40rpx;
    height: 40rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15rpx;
    font-size: 20rpx;
    font-weight: bold;
}

.trend-improving {
    background: #e8f5e8;
    color: #2e7d32;
}

.trend-worsening {
    background: #ffebee;
    color: #c62828;
}

.trend-stable {
    background: #f5f5f5;
    color: #666;
}

.trend-text {
    font-size: 22rpx;
    color: #666;
}

.empty-state {
    text-align: center;
    padding: 100rpx 0;
}

.empty-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 20rpx;
}

.empty-title {
    display: block;
    font-size: 28rpx;
    color: white;
    margin-bottom: 10rpx;
}

.empty-desc {
    display: block;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 30rpx;
}

.empty-btn {
    background: white;
    color: #667eea;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    border: none;
}

.load-more {
    text-align: center;
    margin: 30rpx 0;
}

.load-more-btn {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    border: none;
}

.loading {
    text-align: center;
    padding: 50rpx 0;
    color: white;
}

.fab-container {
    position: fixed;
    bottom: 100rpx;
    right: 30rpx;
    z-index: 999;
}

.fab {
    width: 100rpx;
    height: 100rpx;
    border-radius: 50%;
    background: #667eea;
    border: none;
    box-shadow: 0 8rpx 16rpx rgba(102, 126, 234, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
}

.fab-icon {
    font-size: 40rpx;
    color: white;
}
</style>
