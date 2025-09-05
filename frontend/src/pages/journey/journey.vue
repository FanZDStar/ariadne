<template>
    <view class="journey-container">
        <view class="header">
            <text class="title">心之旅程</text>
            <text class="subtitle">记录你的情感成长历程</text>
        </view>

        <view class="broadcast-banner">
            <text class="broadcast-icon">📣</text>
            <text class="broadcast-text">{{ randomBroadcast }}</text>
        </view>

        <view class="content">
            <view class="journey-card" @click="goToDiary">
                <text class="card-title">碎碎念</text>
                <text class="card-desc">记录每天的情感变化和感悟</text>
                <view class="status">
                    <text v-if="diaryCount !== null">已记录 {{ diaryCount }} 篇碎碎念</text>
                    <text v-else class="loading-text">数据加载中...</text>
                </view>
            </view>

            <view class="journey-card" @click="goToGrowthTrack">
                <text class="card-title">见心录</text>
                <text class="card-desc">查看你在情感方面的成长变化</text>
                <view class="status">
                    <text v-if="growthScore !== '计算中...'">情感指数：{{ growthScore }}</text>
                    <text v-else class="loading-text">数据加载中...</text>
                </view>
            </view>

            <view class="journey-card risk-assessment-card" @click="goToRiskReports">
                <text class="card-title">💙 心理状态评估</text>
                <text class="card-desc">AI分析你的心理健康状态和风险评估</text>
                <view class="status">
                    <text v-if="riskReportCount !== null">已生成 {{ riskReportCount }} 份评估报告</text>
                    <text v-else class="loading-text">数据加载中...</text>
                </view>
                <view class="risk-status" v-if="latestRiskLevel">
                    <text class="risk-indicator" :class="'risk-' + latestRiskLevel">
                        {{ getRiskLevelText(latestRiskLevel) }}
                    </text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';
import { broadcasts } from '../../utils/broadcasts.js';

export default {
    data() {
        return {
            diaryCount: null,
            growthScore: '计算中...',
            randomBroadcast: '',
            // 风险评估相关数据
            riskReportCount: null,
            latestRiskLevel: null
        }
    },

    onLoad() {
        this.loadDiaryCount();
        this.loadGrowthScore();
        this.loadRiskReportData();
        this.setRandomBroadcast();
    },

    onShow() {
        // 每次显示页面时重新加载数据
        this.loadDiaryCount();
        this.loadGrowthScore();
        this.loadRiskReportData();
    },

    methods: {
        setRandomBroadcast() {
            const randomIndex = Math.floor(Math.random() * broadcasts.length);
            this.randomBroadcast = broadcasts[randomIndex];
        },
        async loadDiaryCount() {
            const token = storage.getToken();
            if (!token) {
                return;
            }

            try {
                const response = await api.getUserDiaries(token);
                // 确保响应数据是数组
                const diaries = Array.isArray(response) ? response : (response.data || []);
                this.diaryCount = diaries.length;
            } catch (error) {
                console.error('获取日记数量失败:', error);
                this.diaryCount = 0; // 出错时设置默认值
            }
        },

        async loadGrowthScore() {
            const token = storage.getToken();
            if (!token) {
                this.growthScore = '请先登录';
                return;
            }

            try {
                // 获取近3天的心情数据
                const response = await api.getMoodStats(token, '3days');
                const moodData = response.data || [];

                if (moodData.length === 0) {
                    this.growthScore = '暂无数据';
                    return;
                }

                // 计算平均心情值
                const totalScore = moodData.reduce((sum, item) => sum + item.mood_score, 0);
                const averageScore = totalScore / moodData.length;

                // 格式化显示
                this.growthScore = averageScore.toFixed(1) + '/5.0';
            } catch (error) {
                console.error('获取成长指数失败:', error);
                this.growthScore = '获取失败';
            }
        },

        goToDiary() {
            uni.navigateTo({
                url: '/pages/diary/diary'
            });
        },

        goToGrowthTrack() {
            uni.navigateTo({
                url: '/pages/growth-track/growth-track'
            });
        },

        goToRiskReports() {
            uni.navigateTo({
                url: '/pages/risk-report/report-history'
            });
        },

        async loadRiskReportData() {
            const token = uni.getStorageSync('access_token');
            if (!token) {
                this.riskReportCount = 0;
                return;
            }

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/risk-assessment/reports-history`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`
                    },
                    data: {
                        page: 1,
                        page_size: 100 // 获取所有报告来统计数量
                    }
                });

                if (response.statusCode === 200) {
                    const reports = response.data.reports || [];
                    this.riskReportCount = reports.length;

                    // 获取最新的风险等级
                    if (reports.length > 0) {
                        this.latestRiskLevel = reports[0].overall_risk_level;
                    }
                } else {
                    this.riskReportCount = 0;
                }
            } catch (error) {
                console.error('获取风险评估报告数据失败:', error);
                this.riskReportCount = 0;
            }
        },

        getRiskLevelText(level) {
            const levelTexts = {
                'low': '✅ 状态良好',
                'medium': '⚡ 需要关注',
                'high': '⚠️ 较高风险',
                'critical': '🚨 高度风险'
            };
            return levelTexts[level] || '未知状态';
        }
    }
}
</script>

<style scoped>
.journey-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.header {
    margin-bottom: 40rpx;
}

.title {
    font-size: 42rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 20rpx;
}

.subtitle {
    font-size: 28rpx;
    color: #999;
}

.broadcast-banner {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    border-radius: 20rpx;
    padding: 25rpx 30rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 8rpx 25rpx rgba(0, 0, 0, 0.06);
}

.broadcast-icon {
    font-size: 36rpx;
    margin-right: 20rpx;
}

.broadcast-text {
    font-size: 26rpx;
    color: #666;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
}

.journey-card {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.journey-card:active {
    background-color: #f0f0f0;
}

.card-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.card-desc {
    font-size: 28rpx;
    color: #999;
    display: block;
    margin-bottom: 30rpx;
}

.status {
    font-size: 28rpx;
    color: #007aff;
}

.loading-text {
    color: #999;
    font-style: italic;
}

/* 风险评估卡片特殊样式 */
.risk-assessment-card {
    border-left: 8rpx solid #667eea;
    position: relative;
}

.risk-status {
    margin-top: 20rpx;
}

.risk-indicator {
    display: inline-block;
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
    font-weight: bold;
}

.risk-low {
    background-color: #e8f5e8;
    color: #2e7d32;
}

.risk-medium {
    background-color: #e3f2fd;
    color: #1565c0;
}

.risk-high {
    background-color: #fff3e0;
    color: #ef6c00;
}

.risk-critical {
    background-color: #ffebee;
    color: #c62828;
}
</style>