<template>
    <view class="home-container">        <!-- 顶部装饰背景 -->
        <view class="top-decoration"></view>

        <!-- 头部区域 -->
        <view class="header">
            <view class="brand-section">
                <text class="brand-title">念念有声</text>
                <text class="brand-subtitle">聚焦人文复兴，关注当代年轻人情感问题</text>
            </view>

            <view class="user-welcome" v-if="userInfo">
                <view class="welcome-card">
                    <text class="welcome-text">你好，{{ userInfo.nickname || userInfo.username }}</text>
                    <text class="welcome-desc">今天也要好好照顾自己哦 💫</text>
                </view>
            </view>
        </view>

        <!-- 功能卡片区域 -->
        <view class="feature-grid">
            <!-- 情感对话卡片 -->
            <view class="feature-card" @click="goToContext">
                <view class="card-background beige-bg"></view>
                <view class="card-content">
                    <view class="card-icon-wrapper blue-icon">
                        <text class="card-emoji">💭</text>
                    </view>
                    <view class="card-info">
                        <text class="card-title">情感对话</text>
                        <text class="card-description">与AI进行深度情感交流，获得专业的心理支持与建议</text>
                    </view>
                    <view class="card-arrow">›</view>
                </view>
            </view>

            <!-- 人际智慧卡片 -->
            <view class="feature-card" @click="goToWisdom">
                <view class="card-background beige-bg"></view>
                <view class="card-content">
                    <view class="card-icon-wrapper purple-icon">
                        <text class="card-emoji">🧠</text>
                    </view>
                    <view class="card-info">
                        <text class="card-title">人际智慧</text>
                        <text class="card-description">提升交往技能，防护情感风险，成为关系达人</text>
                    </view>
                    <view class="new-badge">新功能</view>
                    <view class="card-arrow">›</view>
                </view>
            </view>

            <!-- 心灵树洞卡片 -->
            <view class="feature-card" @click="goToTreeHole">
                <view class="card-background beige-bg"></view>
                <view class="card-content">
                    <view class="card-icon-wrapper green-icon">
                        <text class="card-emoji">🌳</text>
                    </view>
                    <view class="card-info">
                        <text class="card-title">心灵树洞</text>
                        <text class="card-description">倾诉心声，倾听他人，在匿名空间寻找共鸣</text>
                    </view>
                    <view class="card-arrow">›</view>
                </view>
            </view>
        </view>

        <!-- 底部装饰 -->
        <view class="bottom-decoration">
            <view class="decoration-wave"></view>
            <view class="decoration-dots">
                <view class="dot dot-1"></view>
                <view class="dot dot-2"></view>
                <view class="dot dot-3"></view>
                <view class="dot dot-4"></view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            userInfo: null,
        }
    },

    onLoad() {
        this.loadUserInfo();
        this.checkStarReward();
    },

    onShow() {
        // 每次页面显示时都检查用户信息
        this.loadUserInfo();
        this.checkStarReward();
    },

    methods: {
        async loadUserInfo() {
            const token = storage.getToken();
            if (token) {
                try {
                    const userInfo = await api.getUserInfo(token);
                    this.userInfo = userInfo;
                    storage.setUserInfo(userInfo);
                } catch (error) {
                    console.error('获取用户信息失败:', error);
                    // Token可能已过期，清除本地存储
                    storage.clearToken();
                }
            }
        },

        goToContext() {
            uni.navigateTo({
                url: '/pages/AI-emotional-chat/chat-context/chat-context'
            })
        },

        goToWisdom() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/interpersonal-wisdom'
            })
        },

        goToTreeHole() {
            uni.navigateTo({
                url: '/pages/tree-hole/tree-hole'
            })
        },

        checkStarReward() {
            // 检查是否有星星奖励信息
            const starReward = storage.getStarReward();
            if (starReward && starReward.message) {
                // 显示星星奖励提示
                uni.showToast({
                    title: starReward.message,
                    icon: 'none',
                    duration: 2500
                });

                // 清除奖励信息，避免重复显示
                storage.clearStarReward();
            }
        }
    }
}
</script>

<style scoped>
.home-container {
    min-height: 100vh;
    background: linear-gradient(180deg, #faf8f3 0%, #ffffff 100%);
    position: relative;
    overflow: hidden;
}

/* 顶部装饰背景 */
.top-decoration {
    position: absolute;
    top: -150rpx;
    left: -100rpx;
    right: -100rpx;
    height: 500rpx;
    background: linear-gradient(135deg, #d4c5a0 0%, #e8dcc0 50%, #f5f0e8 100%);
    border-radius: 0 0 60% 40%;
    opacity: 0.3;
    z-index: 0;
}

/* 头部区域 */
.header {
    padding: 80rpx 40rpx 40rpx;
    position: relative;
    z-index: 1;
}

.brand-section {
    text-align: center;
    margin-bottom: 40rpx;
}

.brand-title {
    font-size: 56rpx;
    font-weight: 700;
    color: #8b6914;
    display: block;
    margin-bottom: 18rpx;
    letter-spacing: 3rpx;
    text-shadow: 0 2rpx 8rpx rgba(139, 105, 20, 0.1);
}

.brand-subtitle {
    font-size: 28rpx;
    color: #a67c52;
    line-height: 1.6;
    opacity: 0.9;
    font-weight: 400;
}

.user-welcome {
    margin-top: 40rpx;
}

.welcome-card {
    background: linear-gradient(135deg, #fff9f0 0%, #fdf6ed 100%);
    border-radius: 28rpx;
    padding: 32rpx;
    text-align: center;
    backdrop-filter: blur(10rpx);
    border: 2rpx solid #f0ead6;
    box-shadow:
        0 8rpx 32rpx rgba(139, 105, 20, 0.08),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
}

.welcome-text {
    font-size: 34rpx;
    font-weight: 600;
    color: #8b6914;
    display: block;
    margin-bottom: 10rpx;
}

.welcome-desc {
    font-size: 26rpx;
    color: #a67c52;
    opacity: 0.8;
}

/* 功能卡片网格 */
.feature-grid {
    padding: 20rpx 40rpx 60rpx;
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 28rpx;
}

.feature-card {
    border-radius: 32rpx;
    overflow: hidden;
    position: relative;
    box-shadow:
        0 12rpx 40rpx rgba(139, 105, 20, 0.12),
        0 4rpx 16rpx rgba(139, 105, 20, 0.08);
    transition: all 0.3s ease;
    border: 2rpx solid #f0ead6;
}

.feature-card:active {
    transform: translateY(6rpx);
    box-shadow:
        0 8rpx 25rpx rgba(139, 105, 20, 0.15),
        0 2rpx 8rpx rgba(139, 105, 20, 0.1);
}

.card-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 32rpx;
}

.beige-bg {
    background: linear-gradient(135deg, #fffef8 0%, #faf7f0 50%, #f5f1e8 100%);
}

.beige-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg,
            rgba(255, 248, 220, 0.4) 0%,
            rgba(250, 245, 220, 0.2) 50%,
            rgba(245, 241, 232, 0.4) 100%);
    border-radius: 32rpx;
}

.card-content {
    position: relative;
    padding: 36rpx;
    display: flex;
    align-items: center;
    gap: 28rpx;
}

.card-icon-wrapper {
    width: 88rpx;
    height: 88rpx;
    border-radius: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10rpx);
    border: 2rpx solid rgba(255, 255, 255, 0.4);
}

.blue-icon {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    box-shadow: 0 4rpx 16rpx rgba(33, 150, 243, 0.2);
}

.purple-icon {
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    box-shadow: 0 4rpx 16rpx rgba(156, 39, 176, 0.2);
}

.green-icon {
    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
    box-shadow: 0 4rpx 16rpx rgba(76, 175, 80, 0.2);
}

.card-emoji {
    font-size: 44rpx;
}

.card-info {
    flex: 1;
}

.card-title {
    font-size: 34rpx;
    font-weight: 600;
    color: #8b6914;
    display: block;
    margin-bottom: 10rpx;
    letter-spacing: 1rpx;
}

.card-description {
    font-size: 26rpx;
    color: #a67c52;
    line-height: 1.5;
    opacity: 0.9;
}

.card-arrow {
    font-size: 44rpx;
    color: #d4c5a0;
    font-weight: 300;
    transform: translateX(0);
    transition: transform 0.3s ease;
}

.feature-card:hover .card-arrow {
    transform: translateX(6rpx);
}

.new-badge {
    position: absolute;
    top: 18rpx;
    right: 18rpx;
    background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
    color: white;
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
    font-size: 22rpx;
    font-weight: 600;
    box-shadow: 0 4rpx 12rpx rgba(255, 107, 107, 0.3);
}

/* 底部装饰 */
.bottom-decoration {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 200rpx;
    pointer-events: none;
    z-index: 0;
}

.decoration-wave {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 80rpx;
    background: linear-gradient(135deg, rgba(212, 197, 160, 0.1) 0%, rgba(245, 241, 232, 0.1) 100%);
    border-radius: 50% 50% 0 0;
}

.decoration-dots {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 200rpx;
}

.dot {
    position: absolute;
    border-radius: 50%;
    background: rgba(139, 105, 20, 0.08);
}

.dot-1 {
    width: 20rpx;
    height: 20rpx;
    bottom: 120rpx;
    left: 15%;
}

.dot-2 {
    width: 16rpx;
    height: 16rpx;
    bottom: 80rpx;
    right: 20%;
    background: rgba(166, 124, 82, 0.08);
}

.dot-3 {
    width: 24rpx;
    height: 24rpx;
    bottom: 140rpx;
    right: 15%;
    background: rgba(212, 197, 160, 0.1);
}

.dot-4 {
    width: 12rpx;
    height: 12rpx;
    bottom: 100rpx;
    left: 70%;
    background: rgba(245, 241, 232, 0.1);
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .header {
        padding: 60rpx 30rpx 30rpx;
    }

    .brand-title {
        font-size: 48rpx;
        letter-spacing: 2rpx;
    }

    .brand-subtitle {
        font-size: 26rpx;
    }

    .feature-grid {
        padding: 20rpx 30rpx 50rpx;
        gap: 24rpx;
    }

    .card-content {
        padding: 32rpx;
        gap: 24rpx;
    }

    .card-icon-wrapper {
        width: 76rpx;
        height: 76rpx;
        border-radius: 20rpx;
    }

    .card-emoji {
        font-size: 38rpx;
    }

    .card-title {
        font-size: 30rpx;
    }

    .card-description {
        font-size: 24rpx;
    }

    .welcome-card {
        padding: 28rpx;
    }

    .welcome-text {
        font-size: 30rpx;
    }

    .welcome-desc {
        font-size: 24rpx;
    }
}

/* 大屏幕适配 */
@media (min-width: 1200rpx) {
    .feature-grid {
        max-width: 900rpx;
        margin: 0 auto;
    }

    .header {
        max-width: 900rpx;
        margin: 0 auto;
    }
}
</style>