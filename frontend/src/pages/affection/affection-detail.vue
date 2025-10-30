<template>
    <view class="affection-detail-container">
        <!-- 自定义导航栏 -->
        <view class="custom-navbar">
            <view class="navbar-left" @click="goBack">
                <text class="back-icon">←</text>
            </view>
            <view class="navbar-title">好感度详情</view>
            <view class="navbar-right"></view>
        </view>

        <!-- 当前好感度状态 -->
        <view class="affection-status-section">
            <view class="current-level">
                <view class="level-icon">💖</view>
                <view class="level-info">
                    <text class="level-name">{{ currentLevel.name }}</text>
                    <text class="level-description">{{ currentLevel.description }}</text>
                </view>
            </view>

            <view class="affection-progress">
                <view class="progress-header">
                    <text class="current-points">当前好感度: {{ currentAffection }}</text>
                    <text class="next-level" v-if="nextLevelPoints > 0">
                        距离下级还需: {{ nextLevelPoints - currentAffection }} 点
                    </text>
                    <text class="max-level" v-else>已达到最高等级</text>
                </view>

                <view class="progress-bar">
                    <view class="progress-fill" :style="{ width: progressPercentage + '%' }"></view>
                </view>

                <view class="progress-labels">
                    <text class="progress-start">{{ currentLevelMinPoints }}</text>
                    <text class="progress-end" v-if="nextLevelPoints > 0">{{ nextLevelPoints }}</text>
                    <text class="progress-end" v-else>MAX</text>
                </view>
            </view>
        </view>

        <!-- 等级解锁内容 -->
        <view class="unlocked-content-section">
            <view class="section-title">已解锁内容</view>
            <view class="unlocked-items">
                <view class="unlocked-item" v-for="action in unlockedActions" :key="action">
                    <view class="item-icon">✨</view>
                    <text class="item-text">{{ action }}</text>
                </view>
            </view>
        </view>

        <!-- 好感度记录 -->
        <view class="affection-logs-section">
            <view class="section-title">好感度记录</view>
            <view class="logs-list" v-if="affectionLogs.length > 0">
                <view class="log-item" v-for="log in affectionLogs" :key="log.id">
                    <view class="log-icon">{{ getActionIcon(log.action_type) }}</view>
                    <view class="log-content">
                        <text class="log-action">{{ getActionName(log.action_type) }}</text>
                        <text class="log-time">{{ formatTime(log.created_at) }}</text>
                    </view>
                    <view class="log-points" :class="{ 'positive': log.points_change > 0 }">
                        +{{ log.points_change }}
                    </view>
                </view>
            </view>
            <view class="empty-logs" v-else>
                <text>暂无好感度记录</text>
            </view>
        </view>

        <!-- 加载更多 -->
        <view class="load-more" v-if="hasMoreLogs" @click="loadMoreLogs">
            <text>加载更多</text>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            currentAffection: 0,
            currentLevel: {
                name: '陌生',
                description: '刚刚认识的关系',
            },
            currentLevelMinPoints: 0,
            nextLevelPoints: 100,
            unlockedActions: [],
            affectionLogs: [],
            hasMoreLogs: true,
            loadingLogs: false,
            logsOffset: 0,
            logsLimit: 20,
        };
    },

    computed: {
        progressPercentage() {
            if (this.nextLevelPoints <= 0) return 100;
            const range = this.nextLevelPoints - this.currentLevelMinPoints;
            const current = this.currentAffection - this.currentLevelMinPoints;
            return Math.min(Math.max((current / range) * 100, 0), 100);
        },
    },

    onLoad() {
        this.loadAffectionSummary();
        this.loadAffectionLogs();
    },

    methods: {
        goBack() {
            uni.navigateBack();
        },

        // 加载好感度概览
        async loadAffectionSummary() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none',
                });
                return;
            }

            try {
                const data = await api.getMascotAffectionSummary(token);
                this.currentAffection = data.current_affection || 0;
                this.currentLevel = {
                    name: data.level_name || '陌生',
                    description: data.level_description || '刚刚认识的关系',
                };
                this.currentLevelMinPoints = data.current_level_min_points || 0;
                this.nextLevelPoints = data.next_level_points || 100;
                this.unlockedActions = data.unlocked_actions || [];
            } catch (error) {
                console.error('获取好感度概览失败:', error);
                uni.showToast({
                    title: '获取好感度信息失败',
                    icon: 'none',
                });
            }
        },

        // 加载好感度记录
        async loadAffectionLogs(isLoadMore = false) {
            if (this.loadingLogs) return;

            const token = storage.getToken();
            if (!token) return;

            this.loadingLogs = true;

            try {
                const offset = isLoadMore ? this.affectionLogs.length : 0;
                const data = await api.getMascotAffectionLogs(token, this.logsLimit);

                if (isLoadMore) {
                    this.affectionLogs = this.affectionLogs.concat(data.logs || []);
                } else {
                    this.affectionLogs = data.logs || [];
                }

                this.hasMoreLogs = (data.logs || []).length >= this.logsLimit;
            } catch (error) {
                console.error('获取好感度记录失败:', error);
                if (!isLoadMore) {
                    uni.showToast({
                        title: '获取记录失败',
                        icon: 'none',
                    });
                }
            } finally {
                this.loadingLogs = false;
            }
        },

        // 加载更多记录
        loadMoreLogs() {
            this.loadAffectionLogs(true);
        },

        // 获取行为图标
        getActionIcon(actionType) {
            const icons = {
                'daily_login': '🎯',
                'outfit_purchase': '👗',
                'emotion_chat': '💬',
                'diary_complete': '📔',
                'mood_tracking': '😊',
                'manual_award': '🎁',
            };
            return icons[actionType] || '⭐';
        },

        // 获取行为名称
        getActionName(actionType) {
            const names = {
                'daily_login': '每日登录',
                'outfit_purchase': '购买服装',
                'emotion_chat': '情感对话',
                'diary_complete': '完成日记',
                'mood_tracking': '心情记录',
                'manual_award': '手动奖励',
            };
            return names[actionType] || '未知行为';
        },

        // 格式化时间
        formatTime(timeStr) {
            const date = new Date(timeStr);
            const now = new Date();
            const diff = now - date;

            if (diff < 60 * 1000) {
                return '刚刚';
            } else if (diff < 60 * 60 * 1000) {
                return Math.floor(diff / (60 * 1000)) + '分钟前';
            } else if (diff < 24 * 60 * 60 * 1000) {
                return Math.floor(diff / (60 * 60 * 1000)) + '小时前';
            } else if (diff < 7 * 24 * 60 * 60 * 1000) {
                return Math.floor(diff / (24 * 60 * 60 * 1000)) + '天前';
            } else {
                return date.toLocaleDateString();
            }
        },
    },
};
</script>

<style scoped>
.affection-detail-container {
    width: 100%;
    min-height: 100vh;
    background: #faf8f3;
}

/* 自定义导航栏 */
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 88rpx;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    padding: 0 32rpx;
    z-index: 1000;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.navbar-left {
    flex: 0 0 80rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 30rpx;
    background: rgba(255, 105, 180, 0.1);
    transition: all 0.3s ease;
}

.navbar-left:active {
    background: rgba(255, 105, 180, 0.2);
    transform: scale(0.95);
}

.back-icon {
    font-size: 32rpx;
    color: #ff69b4;
    font-weight: bold;
}

.navbar-title {
    flex: 1;
    text-align: center;
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.navbar-right {
    flex: 0 0 80rpx;
}

/* 好感度状态区域 */
.affection-status-section {
    margin-top: 88rpx;
    padding: 40rpx 30rpx;
    background: #fff;
    border-radius: 0 0 40rpx 40rpx;
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.current-level {
    display: flex;
    align-items: center;
    margin-bottom: 40rpx;
}

.level-icon {
    font-size: 60rpx;
    margin-right: 20rpx;
}

.level-info {
    flex: 1;
}

.level-name {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    color: #e91e63;
    margin-bottom: 8rpx;
}

.level-description {
    display: block;
    font-size: 28rpx;
    color: #666;
    line-height: 1.4;
}

.affection-progress {
    padding: 0;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
}

.current-points {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
}

.next-level,
.max-level {
    font-size: 24rpx;
    color: #999;
}

.progress-bar {
    height: 12rpx;
    background: #f0f0f0;
    border-radius: 6rpx;
    overflow: hidden;
    margin-bottom: 10rpx;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff69b4, #ff91c7);
    border-radius: 6rpx;
    transition: width 0.3s ease;
}

.progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 22rpx;
    color: #999;
}

/* 解锁内容区域 */
.unlocked-content-section {
    margin: 30rpx;
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
}

.unlocked-items {
    display: flex;
    flex-wrap: wrap;
    gap: 15rpx;
}

.unlocked-item {
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
    border-radius: 15rpx;
    padding: 10rpx 15rpx;
    margin-bottom: 10rpx;
}

.item-icon {
    font-size: 24rpx;
    margin-right: 8rpx;
}

.item-text {
    font-size: 24rpx;
    color: #2d3436;
}

/* 好感度记录区域 */
.affection-logs-section {
    margin: 0 30rpx 30rpx;
    background: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.logs-list {
    margin-top: 20rpx;
}

.log-item {
    display: flex;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #f0f0f0;
}

.log-item:last-child {
    border-bottom: none;
}

.log-icon {
    font-size: 32rpx;
    margin-right: 15rpx;
    width: 50rpx;
    text-align: center;
}

.log-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.log-action {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 5rpx;
}

.log-time {
    font-size: 22rpx;
    color: #999;
}

.log-points {
    font-size: 28rpx;
    font-weight: bold;
    color: #999;
}

.log-points.positive {
    color: #00b894;
}

.empty-logs {
    text-align: center;
    padding: 60rpx 0;
    color: #999;
    font-size: 28rpx;
}

/* 加载更多 */
.load-more {
    text-align: center;
    padding: 30rpx;
    margin: 0 30rpx 30rpx;
    background: #fff;
    border-radius: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
    color: #007aff;
    font-size: 28rpx;
    transition: all 0.3s ease;
}

.load-more:active {
    background: #f8f8f8;
    transform: scale(0.98);
}

/* 响应式调整 */
@media (max-width: 480px) {
    .affection-status-section {
        padding: 30rpx 20rpx;
    }

    .current-level {
        margin-bottom: 30rpx;
    }

    .level-icon {
        font-size: 50rpx;
    }

    .level-name {
        font-size: 32rpx;
    }

    .unlocked-content-section,
    .affection-logs-section {
        margin: 20rpx;
        padding: 20rpx;
    }
}
</style>
