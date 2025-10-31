<template>
    <!-- 简单的好感度奖励浮动提示 -->
    <view class="affection-toast" v-if="visible" :class="{ 'show': showModal, 'level-up': isLevelUp }">
        <view class="toast-content">
            <!-- 普通好感度奖励 -->
            <template v-if="!isLevelUp">
                <view class="reward-icon">💖</view>
                <text class="reward-text">好感度 +{{ points }}</text>
            </template>

            <!-- 升级奖励 -->
            <template v-else>
                <view class="level-up-icon">🎉</view>
                <text class="level-up-text">{{ levelName }} 升级！</text>
            </template>
        </view>
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

        // 显示奖励提示
        showReward() {
            this.visible = true;
            this.$nextTick(() => {
                setTimeout(() => {
                    this.showModal = true;
                }, 50);

                // 3秒后自动消失
                setTimeout(() => {
                    this.closeReward();
                }, 3000);
            });

            // 震动反馈
            uni.vibrateShort();
        },

        // 关闭奖励提示
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
/* 简单的浮动Toast样式 */
.affection-toast {
    position: fixed;
    top: 200rpx;
    left: 50%;
    transform: translateX(-50%) translateY(-100rpx);
    z-index: 9999;
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.affection-toast.show {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
}

.toast-content {
    background: linear-gradient(135deg, #ff69b4, #ff91c7);
    border-radius: 50rpx;
    padding: 20rpx 40rpx;
    display: flex;
    align-items: center;
    gap: 15rpx;
    box-shadow: 0 8rpx 24rpx rgba(255, 105, 180, 0.4);
    border: 2rpx solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10rpx);
}

.affection-toast.level-up .toast-content {
    background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
    box-shadow: 0 8rpx 24rpx rgba(255, 234, 167, 0.4);
    border: 2rpx solid rgba(255, 255, 255, 0.5);
}

/* 普通奖励样式 */
.reward-icon {
    font-size: 40rpx;
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

.reward-text {
    font-size: 30rpx;
    font-weight: bold;
    color: #fff;
    text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

/* 升级奖励样式 */
.level-up-icon {
    font-size: 40rpx;
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

.level-up-text {
    font-size: 30rpx;
    font-weight: bold;
    color: #8b4513;
    text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

/* 响应式调整 */
@media (max-width: 480px) {

    .reward-icon,
    .level-up-icon {
        font-size: 36rpx;
    }

    .reward-text,
    .level-up-text {
        font-size: 26rpx;
    }

    .toast-content {
        padding: 15rpx 30rpx;
        gap: 12rpx;
    }
}
</style>
