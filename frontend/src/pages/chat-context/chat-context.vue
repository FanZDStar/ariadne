<template>
    <view class="context-container">
        <view class="header">
            <text class="title">选择对话语境</text>
        </view>

        <view class="content">
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
        </view>
    </view>
</template>

<script>
export default {
    methods: {
        goToSelfDialog() {
            uni.navigateTo({
                url: '/pages/self-dialog/self-dialog'
            })
        },

        goToExperience() {
            // 这里可以跳转到具体的恋爱尝试页面
            uni.navigateTo({
                url: '/pages/love-experiment/love-experiment'
            })
        },

        goToLove() {
            // 这里可以跳转到爱自己相关的页面
            uni.navigateTo({
                url: '/pages/love-yourself/love-yourself'
            })
        }
    }
}
</script>

<style scoped>
.context-container {
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
</style>