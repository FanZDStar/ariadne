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
                    <text v-if="diaryCount !== null">已记录 {{ diaryCount }} 篇日记</text>
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
            randomBroadcast: ''
        }
    },

    onLoad() {
        this.loadDiaryCount();
        this.loadGrowthScore();
        this.setRandomBroadcast();
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
</style>