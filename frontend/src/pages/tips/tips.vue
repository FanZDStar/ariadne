<template>
    <view class="tips-container">
        <view class="header">
            <text class="title">恋爱小技巧</text>
            <text class="subtitle">每天一点新鲜感，帮助你迈出第一步</text>
        </view>

        <view class="content">
            <view class="tip-card">
                <text class="tip-title">1. 真诚表达</text>
                <text class="tip-content">在合适的时机真诚地表达你的感受，不需要过于华丽的词藻，真实的情感最能打动人心。</text>
            </view>

            <view class="tip-card">
                <text class="tip-title">2. 倾听对方</text>
                <text class="tip-content">学会倾听对方的想法和感受，给予关注和回应，这是建立深度连接的重要方式。</text>
            </view>

            <view class="tip-card">
                <text class="tip-title">3. 创造共同回忆</text>
                <text class="tip-content">一起参与有趣的活动，创造属于你们的独特回忆，这会让关系更加牢固。</text>
            </view>

            <view class="tip-card">
                <text class="tip-title">4. 保持独立</text>
                <text class="tip-content">在恋爱中保持自己的独立性和个人空间，这样可以让关系更加健康和持久。</text>
            </view>

            <view class="tip-card">
                <text class="tip-title">5. 小惊喜</text>
                <text class="tip-content">偶尔给对方一些小惊喜，不一定要昂贵，用心准备的小礼物或安排会让对方感受到你的在意。</text>
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
.tips-container {
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

.tip-card {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.tip-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #007aff;
    display: block;
    margin-bottom: 20rpx;
}

.tip-content {
    font-size: 30rpx;
    color: #666;
    line-height: 1.6;
}
</style>