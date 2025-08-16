<!-- <template>
    <view class="journey-container">
        <view class="header">
            <text class="title">心之旅程</text>
            <text class="subtitle">记录你的情感成长历程</text>
        </view>

        <view class="content">
            <view class="journey-card">
                <text class="card-title">情感日记</text>
                <text class="card-desc">记录每天的情感变化和感悟</text>
                <view class="status">
                    <text>已记录 0 篇日记</text>
                </view>
            </view>

            <view class="journey-card">
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
export default {
    data() {
        return {}
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
                    <text>已记录 0 篇日记</text>
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
export default {
    data() {
        return {}
    },
    methods: {
        goToDiary() {
            console.log('尝试跳转到情感日记页面');
            uni.navigateTo({
                url: '/pages/diary/diary',
                success: () => {
                    console.log('跳转成功');
                },
                fail: (err) => {
                    console.error('跳转失败:', err);
                    uni.showToast({
                        title: '跳转失败',
                        icon: 'none'
                    });
                }
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