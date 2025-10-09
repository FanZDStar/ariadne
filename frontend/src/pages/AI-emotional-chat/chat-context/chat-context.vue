<template>
    <view class="context-container">
        <view class="header">
            <text class="title">选择对话语境</text>
            <text class="subtitle">为大学生量身定制的心理成长陪伴</text>
        </view>

        <view class="content">
            <!-- 基础场景 -->
            <view class="section">
                <text class="section-title">💖 情感探索</text>
                <view class="grid-container">
                    <view class="context-card" @click="navigateToScene('self-dialog')">
                        <view class="card-icon">🌸</view>
                        <text class="card-title">与自己对话</text>
                        <text class="card-desc">反思内心世界，获得AI引导</text>
                    </view>

                    <view class="context-card" @click="navigateToScene('emotional-growth')">
                        <view class="card-icon">💝</view>
                        <text class="card-title">情感成长</text>
                        <text class="card-desc">探索情感世界，发展智慧</text>
                    </view>
                </view>
            </view>

            <!-- 大学生专属场景 -->
            <view class="section">
                <text class="section-title">🎓 大学生专区</text>
                <view class="grid-container">
                    <view class="context-card" @click="navigateToScene('academic-stress')">
                        <view class="card-icon">📚</view>
                        <text class="card-title">学业压力疏导</text>
                        <text class="card-desc">考试焦虑、学习困扰解答</text>
                    </view>

                    <view class="context-card" @click="navigateToScene('social-anxiety')">
                        <view class="card-icon">👥</view>
                        <text class="card-title">社交焦虑陪伴</text>
                        <text class="card-desc">克服社交障碍，建立关系</text>
                    </view>

                    <view class="context-card" @click="navigateToScene('future-planning')">
                        <view class="card-icon">🔮</view>
                        <text class="card-title">未来规划指导</text>
                        <text class="card-desc">职业探索、人生方向思考</text>
                    </view>

                    <view class="context-card" @click="navigateToScene('life-balance')">
                        <view class="card-icon">⚖️</view>
                        <text class="card-title">生活平衡教练</text>
                        <text class="card-desc">学习、社交、健康平衡</text>
                    </view>
                </view>
            </view>

            <!-- 关系成长 -->
            <view class="section">
                <text class="section-title">💕 关系成长</text>
                <view class="grid-container">
                    <view class="context-card" @click="navigateToScene('love-experiment')">
                        <view class="card-icon">🧪</view>
                        <text class="card-title">心语练习</text>
                        <text class="card-desc">恋爱技能训练，表达练习</text>
                    </view>

                    <view class="context-card" @click="navigateToScene('self-love')">
                        <view class="card-icon">🌟</view>
                        <text class="card-title">爱自己</text>
                        <text class="card-desc">建立健康的自我关系</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    methods: {
        navigateToScene(scene) {
            // 通用的场景导航方法
            const sceneConfig = {
                'self-dialog': {
                    url: '/pages/AI-emotional-chat/self-dialog/self-dialog',
                    scene: 'self-dialog'
                },
                'love-experiment': {
                    url: '/pages/AI-emotional-chat/love-experiment/love-experiment',
                    scene: 'love-experiment'
                },
                'self-love': {
                    url: '/pages/AI-emotional-chat/love-yourself/love-yourself',
                    scene: 'self-love'
                },
                'emotional-growth': {
                    url: '/pages/AI-emotional-chat/emotional-growth/emotional-growth',
                    scene: 'emotional-growth'
                },
                'academic-stress': {
                    url: '/pages/AI-emotional-chat/academic-stress/academic-stress',
                    scene: 'academic-stress'
                },
                'social-anxiety': {
                    url: '/pages/AI-emotional-chat/social-anxiety/social-anxiety',
                    scene: 'social-anxiety'
                },
                'future-planning': {
                    url: '/pages/AI-emotional-chat/future-planning/future-planning',
                    scene: 'future-planning'
                },
                'life-balance': {
                    url: '/pages/AI-emotional-chat/life-balance/life-balance',
                    scene: 'life-balance'
                }
            };
            const config = sceneConfig[scene];
            if (config) {
                uni.navigateTo({
                    url: `${config.url}?scene=${config.scene}`
                });
            }
        },

        goToSelfDialog() {
            this.navigateToScene('self-dialog');
        },

        goToExperience() {
            this.navigateToScene('love-experiment');
        },

        goToLove() {
            this.navigateToScene('self-love');
        },
        goToGrowth() {
            this.navigateToScene('emotional-growth');
        },
        goToStress() {
            this.navigateToScene('academic-stress');
        },
        goToAnxiety() {
            this.navigateToScene('social-anxiety');
        },
        goToPlanning() {
            this.navigateToScene('future-planning');
        },
        goToBalance() {
            this.navigateToScene('life-balance');
        }
    }
}
</script>

<style scoped>
.context-container {
    padding: 30rpx 25rpx;
    background-color: #ffffff;
    min-height: 100vh;
}

.header {
    margin-bottom: 40rpx;
    text-align: center;
}

.title {
    font-size: 38rpx;
    font-weight: bold;
    color: #2c3e50;
    display: block;
    margin-bottom: 12rpx;
}

.subtitle {
    font-size: 26rpx;
    color: #7f8c8d;
    line-height: 1.4;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 35rpx;
}

.section {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
    border-radius: 24rpx;
    padding: 30rpx;
    border: 3rpx solid;
    box-shadow:
        0 2rpx 8rpx rgba(0, 0, 0, 0.06),
        0 8rpx 24rpx rgba(0, 0, 0, 0.04),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
    position: relative;
}

/* 第一个模块 - 很淡的蓝色 */
.section:nth-child(1) {
    background-color: #f8fbff;
    border-color: #e6f2ff;
    box-shadow:
        0 2rpx 8rpx rgba(135, 206, 250, 0.08),
        0 8rpx 24rpx rgba(135, 206, 250, 0.06),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
}

.section:nth-child(1)::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 24rpx;
    background: linear-gradient(135deg,
            rgba(173, 216, 230, 0.3) 0%,
            rgba(176, 224, 230, 0.15) 50%,
            rgba(230, 242, 255, 0.3) 100%);
    pointer-events: none;
}

.section:nth-child(1) .section-title {
    color: #1e5799;
}

/* 第二个模块 - 很淡的米黄色 */
.section:nth-child(2) {
    background-color: #fffef8;
    border-color: #f5f3e7;
    box-shadow:
        0 2rpx 8rpx rgba(218, 165, 32, 0.08),
        0 8rpx 24rpx rgba(218, 165, 32, 0.06),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
}

.section:nth-child(2)::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 24rpx;
    background: linear-gradient(135deg,
            rgba(255, 248, 220, 0.4) 0%,
            rgba(250, 245, 220, 0.2) 50%,
            rgba(245, 243, 231, 0.4) 100%);
    pointer-events: none;
}

.section:nth-child(2) .section-title {
    color: #8b6914;
}

/* 第三个模块 - 很淡的浅绿色 */
.section:nth-child(3) {
    background-color: #f8fff8;
    border-color: #e7f5e7;
    box-shadow:
        0 2rpx 8rpx rgba(144, 238, 144, 0.08),
        0 8rpx 24rpx rgba(144, 238, 144, 0.06),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
}

.section:nth-child(3)::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 24rpx;
    background: linear-gradient(135deg,
            rgba(240, 255, 240, 0.4) 0%,
            rgba(220, 245, 220, 0.2) 50%,
            rgba(231, 245, 231, 0.4) 100%);
    pointer-events: none;
}

.section:nth-child(3) .section-title {
    color: #2d5a2d;
}

.section-title {
    font-size: 30rpx;
    font-weight: bold;
    margin-bottom: 8rpx;
    padding-left: 10rpx;
    position: relative;
    z-index: 1;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18rpx;
    position: relative;
    z-index: 1;
}

.context-card {
    background-color: #ffffff;
    border-radius: 20rpx;
    padding: 25rpx 20rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 2rpx solid #f0f0f0;
    box-shadow:
        0 4rpx 12rpx rgba(0, 0, 0, 0.08),
        0 2rpx 6rpx rgba(0, 0, 0, 0.06),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease;
    position: relative;
    min-height: 140rpx;
}

.context-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 20rpx;
    background: linear-gradient(135deg,
            rgba(248, 249, 250, 0.3) 0%,
            rgba(245, 246, 247, 0.2) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.context-card:hover {
    transform: translateY(-4rpx);
    box-shadow:
        0 8rpx 24rpx rgba(0, 0, 0, 0.12),
        0 4rpx 12rpx rgba(0, 0, 0, 0.10),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.9);
    border-color: #d0d0d0;
}

.context-card:hover::before {
    opacity: 1;
}

.context-card:active {
    transform: translateY(-2rpx);
    box-shadow:
        0 6rpx 18rpx rgba(0, 0, 0, 0.15),
        0 3rpx 9rpx rgba(0, 0, 0, 0.12);
}

.card-icon {
    font-size: 45rpx;
    margin-bottom: 12rpx;
    height: 55rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 1;
}

.card-title {
    font-size: 26rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 8rpx;
    line-height: 1.2;
    position: relative;
    z-index: 1;
}

.card-desc {
    font-size: 20rpx;
    color: #7f8c8d;
    line-height: 1.3;
    position: relative;
    z-index: 1;
}

/* 响应式适配 */
@media (max-width: 750rpx) {
    .grid-container {
        grid-template-columns: 1fr;
        gap: 15rpx;
    }

    .section {
        padding: 25rpx;
    }

    .context-card {
        padding: 20rpx 15rpx;
        min-height: 120rpx;
    }

    .card-icon {
        font-size: 40rpx;
        height: 50rpx;
    }

    .card-title {
        font-size: 24rpx;
    }

    .card-desc {
        font-size: 18rpx;
    }
}

/* 大屏幕适配 */
@media (min-width: 1200rpx) {
    .grid-container {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>