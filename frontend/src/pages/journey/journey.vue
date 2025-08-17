<!-- <template>
    <view class="journey-container">
        <view class="header">
            <text class="title">心之旅程</text>
            <text class="subtitle">记录你的情感成长历程</text>
        </view>

        <view class="content">
            <view class="journey-card" @click="goToDiary">
                <text class="card-title">情感日记</text>
                <text class="card-desc">记录每天的情感变化和感悟</text>
                <view class="status">
                    <text>已记录 {{ diaryCount }} 篇日记</text>
                </view>
            </view>

            <view class="journey-card" @click="goToGrowthTrack">
                <text class="card-title">成长轨迹</text>
                <text class="card-desc">查看你在情感方面的成长变化</text>
                <view class="status">
                    <text>情感指数：★★★★☆</text>
                </view>
            </view>

            <view class="journey-card">
                <text class="card-title">收获与反思</text>
                <text class="card-desc">总结从每段感情中获得的经验</text>
                <view class="status">
                    <text>已总结 0 条经验</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            diaryCount: 0
        }
    },

    onLoad() {
        this.loadDiaryCount();
    },

    methods: {
        async loadDiaryCount() {
            const token = storage.getToken();
            if (!token) {
                return;
            }

            try {
                const diaries = await api.getUserDiaries(token);
                this.diaryCount = diaries.length;
            } catch (error) {
                console.error('获取日记数量失败:', error);
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
    margin-bottom: 60rpx;
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
</style> -->

<template>
    <view class="journey-container">
        <view class="header">
            <text class="title">心之旅程</text>
            <text class="subtitle">记录你的情感成长历程</text>
        </view>

        <view class="content">
            <view class="journey-card" @click="goToDiary">
                <text class="card-title">情感日记</text>
                <text class="card-desc">记录每天的情感变化和感悟</text>
                <view class="status">
                    <text>已记录 {{ diaryCount }} 篇日记</text>
                </view>
            </view>

            <view class="journey-card" @click="goToGrowthTrack">
                <text class="card-title">成长轨迹</text>
                <text class="card-desc">查看你在情感方面的成长变化</text>
                <view class="status">
                    <text>情感指数：{{ growthScore }}</text>
                </view>
            </view>

            <view class="journey-card">
                <text class="card-title">收获与反思</text>
                <text class="card-desc">总结从每段感情中获得的经验</text>
                <view class="status">
                    <text>已总结 0 条经验</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            diaryCount: 0,
            growthScore: '计算中...'
        }
    },

    onLoad() {
        this.loadDiaryCount();
        this.loadGrowthScore();
    },

    methods: {
        async loadDiaryCount() {
            const token = storage.getToken();
            if (!token) {
                return;
            }

            try {
                const diaries = await api.getUserDiaries(token);
                this.diaryCount = diaries.length;
            } catch (error) {
                console.error('获取日记数量失败:', error);
            }
        },

        async loadGrowthScore() {
            const token = storage.getToken();
            if (!token) {
                this.growthScore = '请先登录';
                return;
            }

        //     try {
        //         // 获取近3天的心情数据
        //         const response = await api.getMoodStats(token, '3days');
        //         const moodData = response.data || [];

        //         if (moodData.length === 0) {
        //             this.growthScore = '暂无数据';
        //             return;
        //         }

        //         // 计算平均心情值
        //         const totalScore = moodData.reduce((sum, item) => sum + item.mood_score, 0);
        //         const averageScore = totalScore / moodData.length;

        //         // 格式化显示
        //         this.growthScore = averageScore.toFixed(1) + '/5.0';
        //     } catch (error) {
        //         console.error('获取成长指数失败:', error);
        //         this.growthScore = '获取失败';
        //     }
            // },

            try {
                // 获取近3天的成长指数
                const response = await api.getGrowthScore(token);
                this.growthScore = response.formatted_score;
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
    margin-bottom: 60rpx;
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
</style>