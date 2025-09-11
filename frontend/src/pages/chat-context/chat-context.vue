<template>
    <view class="context-container">
        <view class="header">
            <text class="title">选择对话语境</text>
            <text class="subtitle">为大学生量身定制的心理成长陪伴</text>
        </view>

        <!-- <view class="content">
            <view class="context-item" @click="goToSelfDialog">
                <text class="item-title">自己与自己的对话</text>
                <text class="item-desc">反思感情中的言行举止，获得AI引导和建议</text>
                <text class="arrow">></text>
            </view>

            <view class="context-item" @click="goToExperience">
                <text class="item-title">心语练习 </text>
                <text class="item-desc">帮助胆小没有经验的人迈出第一步</text>
                <text class="arrow">></text>
            </view>

            <view class="context-item" @click="goToLove">
                <text class="item-title">爱他人先爱自己</text>
                <text class="item-desc">探讨如何在爱他人之前先学会爱自己</text>
                <text class="arrow">></text>
            </view>
        </view> -->

        <view class="content">
            <!-- 基础场景 -->
            <view class="section">
                <text class="section-title">💖 情感探索</text>
                <view class="context-item" @click="navigateToScene('self-dialog')">
                    <view class="item-icon">🌸</view>
                    <view class="item-content">
                        <text class="item-title">与自己对话</text>
                        <text class="item-desc">反思内心世界，获得AI引导和建议</text>
                    </view>
                    <text class="arrow">></text>
                </view>

                <view class="context-item" @click="navigateToScene('emotional-growth')">
                    <view class="item-icon">💝</view>
                    <view class="item-content">
                        <text class="item-title">情感成长</text>
                        <text class="item-desc">探索情感世界，发展情感智慧</text>
                    </view>
                    <text class="arrow">></text>
                </view>
            </view>

            <!-- 大学生专属场景 -->
            <view class="section">
                <text class="section-title">🎓 大学生专区</text>
                <view class="context-item" @click="navigateToScene('academic-stress')">
                    <view class="item-icon">📚</view>
                    <view class="item-content">
                        <text class="item-title">学业压力疏导</text>
                        <text class="item-desc">考试焦虑、学习困扰、专业迷茫解答</text>
                    </view>
                    <text class="arrow">></text>
                </view>

                <view class="context-item" @click="navigateToScene('social-anxiety')">
                    <view class="item-icon">👥</view>
                    <view class="item-content">
                        <text class="item-title">社交焦虑陪伴</text>
                        <text class="item-desc">克服社交障碍，建立健康人际关系</text>
                    </view>
                    <text class="arrow">></text>
                </view>

                <view class="context-item" @click="navigateToScene('future-planning')">
                    <view class="item-icon">🔮</view>
                    <view class="item-content">
                        <text class="item-title">未来规划指导</text>
                        <text class="item-desc">职业探索、升学决策、人生方向思考</text>
                    </view>
                    <text class="arrow">></text>
                </view>

                <view class="context-item" @click="navigateToScene('life-balance')">
                    <view class="item-icon">⚖️</view>
                    <view class="item-content">
                        <text class="item-title">生活平衡教练</text>
                        <text class="item-desc">学习、社交、健康的多维度平衡</text>
                    </view>
                    <text class="arrow">></text>
                </view>
            </view>

            <!-- 关系成长 -->
            <view class="section">
                <text class="section-title">💕 关系成长</text>
                <view class="context-item" @click="navigateToScene('love-experiment')">
                    <view class="item-icon">🧪</view>
                    <view class="item-content">
                        <text class="item-title">心语练习</text>
                        <text class="item-desc">恋爱技能训练，表达沟通练习</text>
                    </view>
                    <text class="arrow">></text>
                </view>

                <view class="context-item" @click="navigateToScene('self-love')">
                    <view class="item-icon">🌟</view>
                    <view class="item-content">
                        <text class="item-title">爱自己</text>
                        <text class="item-desc">建立健康的自我关系，学会自我关爱</text>
                    </view>
                    <text class="arrow">></text>
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
                    url: '/pages/self-dialog/self-dialog',
                    scene: 'self-dialog'
                },
                'love-experiment': {
                    url: '/pages/love-experiment/love-experiment',
                    scene: 'love-experiment'
                },
                'self-love': {
                    url: '/pages/love-yourself/love-yourself',
                    scene: 'self-love'
                },
                'emotional-growth': {
                    url: '/pages/emotional-growth/emotional-growth',
                    scene: 'emotional-growth'
                },
                'academic-stress': {
                    url: '/pages/academic-stress/academic-stress',
                    scene: 'academic-stress'
                },
                'social-anxiety': {
                    url: '/pages/social-anxiety/social-anxiety',
                    scene: 'social-anxiety'
                },
                'future-planning': {
                    url: '/pages/future-planning/future-planning',
                    scene: 'future-planning'
                },
                'life-balance': {
                    url: '/pages/life-balance/life-balance',
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
        // goToSelfDialog() {
        //     uni.navigateTo({
        //         url: '/pages/self-dialog/self-dialog'
        //     })
        // },

        // goToExperience() {
        //     // 这里可以跳转到具体的恋爱尝试页面
        //     uni.navigateTo({
        //         url: '/pages/love-experiment/love-experiment'
        //     })
        // },

        // goToLove() {
        //     // 这里可以跳转到爱自己相关的页面
        //     uni.navigateTo({
        //         url: '/pages/love-yourself/love-yourself'
        //     })
        // },
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
    padding: 40rpx;
    /* background-color: #f8f8f8; */
    /* test */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.header {
    margin-bottom: 60rpx;
    /* test */
    text-align: center;
}

.title {
    font-size: 42rpx;
    font-weight: bold;
    /* color: #333; */
    /* test */
    color: #fff;
    display: block;
    margin-bottom: 16rpx;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
}

.context-item {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
    position: relative;
}

.item-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.item-desc {
    font-size: 28rpx;
    color: #999;
}

.arrow {
    position: absolute;
    right: 40rpx;
    top: 50%;
    transform: translateY(-50%);
    color: #ccc;
    font-size: 36rpx;
}
/*test*/
.section {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #fff;
    margin-bottom: 10rpx;
    padding-left: 20rpx;
}
</style>