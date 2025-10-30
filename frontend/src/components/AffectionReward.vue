<template>
    <view class="affection-reward-container" v-if="visible">
        <view class="reward-modal" :class="{ 'show': showModal, 'level-up': isLevelUp }">
            <view class="reward-content">
                <!-- 普通好感度奖励 -->
                <template v-if="!isLevelUp">
                    <view class="reward-icon">💖</view>
                    <view class="reward-title">好感度 +{{ points }}</view>
                    <view class="reward-message">{{ message }}</view>
                </template>

                <!-- 升级奖励 -->
                <template v-else>
                    <view class="level-up-icon">🎉</view>
                    <view class="level-up-title">好感度升级！</view>
                    <view class="level-up-content">
                        <view class="level-info">
                            <text class="level-name">{{ levelName }}</text>
                            <text class="level-desc">{{ levelDescription }}</text>
                        </view>
                        <view class="rewards-info" v-if="levelRewards">
                            <view class="reward-item" v-if="levelRewards.star_points">
                                <text class="reward-label">获得星星:</text>
                                <text class="reward-value">+{{ levelRewards.star_points }}</text>
                            </view>
                            <view class="reward-item"
                                v-if="levelRewards.special_items && levelRewards.special_items.length > 0">
                                <text class="reward-label">特殊奖励:</text>
                                <text class="reward-value">{{ levelRewards.special_items.join(', ') }}</text>
                            </view>
                        </view>
                    </view>
                </template>

                <view class="reward-close" @click="closeReward">
                    <text>确定</text>
                </view>
            </view>
        </view>

        <!-- 背景遮罩 -->
        <view class="reward-backdrop" @click="closeReward"></view>
    </view>
</template>

<script>
export default {
    name: 'AffectionReward',
    data() {
        return {
            visible: false,
            showModal: false,
            points: 0,
            message: '',
            isLevelUp: false,
            levelName: '',
            levelDescription: '',
            levelRewards: null
        }
    },

    methods: {
        // 显示普通好感度奖励
        showAffectionReward(points, message) {
            this.points = points;
            this.message = message;
            this.isLevelUp = false;
            this.showReward();
        },

        // 显示升级奖励
        showLevelUpReward(levelInfo, rewards) {
            this.isLevelUp = true;
            this.levelName = levelInfo.name;
            this.levelDescription = levelInfo.description;
            this.levelRewards = rewards;
            this.showReward();
        },

        // 显示奖励弹窗
        showReward() {
            this.visible = true;
            this.$nextTick(() => {
                setTimeout(() => {
                    this.showModal = true;
                }, 50);
            });

            // 震动反馈
            uni.vibrateShort();
        },

        // 关闭奖励弹窗
        closeReward() {
            this.showModal = false;
            setTimeout(() => {
                this.visible = false;
                this.resetData();
            }, 300);
        },

        // 重置数据
        resetData() {
            this.points = 0;
            this.message = '';
            this.isLevelUp = false;
            this.levelName = '';
            this.levelDescription = '';
            this.levelRewards = null;
        }
    }
}
</script>

<style scoped>
.affection-reward-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40rpx;
}

.reward-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5rpx);
}

.reward-modal {
    position: relative;
    background: #fff;
    border-radius: 30rpx;
    max-width: 500rpx;
    width: 100%;
    transform: scale(0.7) translateY(100rpx);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.3);
}

.reward-modal.show {
    transform: scale(1) translateY(0);
    opacity: 1;
}

.reward-modal.level-up {
    background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
    border: 3rpx solid #e17055;
}

.reward-content {
    padding: 60rpx 40rpx 40rpx;
    text-align: center;
}

/* 普通奖励样式 */
.reward-icon {
    font-size: 80rpx;
    margin-bottom: 20rpx;
    animation: heartbeat 1.5s ease-in-out infinite;
}

@keyframes heartbeat {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}

.reward-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #e91e63;
    margin-bottom: 15rpx;
}

.reward-message {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 40rpx;
    line-height: 1.4;
}

/* 升级奖励样式 */
.level-up-icon {
    font-size: 100rpx;
    margin-bottom: 20rpx;
    animation: celebration 2s ease-in-out infinite;
}

@keyframes celebration {

    0%,
    100% {
        transform: rotate(0deg) scale(1);
    }

    25% {
        transform: rotate(-10deg) scale(1.1);
    }

    75% {
        transform: rotate(10deg) scale(1.1);
    }
}

.level-up-title {
    font-size: 42rpx;
    font-weight: bold;
    color: #d63031;
    margin-bottom: 30rpx;
    text-shadow: 2rpx 2rpx 4rpx rgba(214, 48, 49, 0.3);
}

.level-up-content {
    margin-bottom: 40rpx;
}

.level-info {
    margin-bottom: 30rpx;
}

.level-name {
    display: block;
    font-size: 32rpx;
    font-weight: bold;
    color: #2d3436;
    margin-bottom: 10rpx;
}

.level-desc {
    display: block;
    font-size: 26rpx;
    color: #636e72;
    line-height: 1.4;
}

.rewards-info {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 20rpx;
    padding: 20rpx;
    margin-top: 20rpx;
}

.reward-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10rpx;
}

.reward-item:last-child {
    margin-bottom: 0;
}

.reward-label {
    font-size: 26rpx;
    color: #2d3436;
}

.reward-value {
    font-size: 26rpx;
    font-weight: bold;
    color: #00b894;
}

/* 关闭按钮 */
.reward-close {
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    color: #fff;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    font-size: 28rpx;
    font-weight: bold;
    transition: all 0.3s ease;
    display: inline-block;
    box-shadow: 0 8rpx 16rpx rgba(116, 185, 255, 0.3);
}

.reward-close:active {
    transform: translateY(2rpx);
    box-shadow: 0 4rpx 8rpx rgba(116, 185, 255, 0.4);
}

/* 响应式调整 */
@media (max-width: 480px) {
    .reward-modal {
        max-width: 90%;
    }

    .reward-content {
        padding: 50rpx 30rpx 30rpx;
    }

    .reward-icon,
    .level-up-icon {
        font-size: 70rpx;
    }

    .reward-title,
    .level-up-title {
        font-size: 32rpx;
    }

    .level-name {
        font-size: 28rpx;
    }
}
</style>
