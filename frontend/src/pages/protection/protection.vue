<template>
    <view class="protection-container">
        <view class="header">
            <text class="title">感情防护</text>
            <text class="subtitle">识别恋爱中的不公平，保护自己</text>
        </view>

        <view class="content">
            <view class="protection-card">
                <text class="card-title">识别渣男渣女的特征</text>
                <view class="card-content">
                    <text class="point">1. 只在需要时联系你，平时对你漠不关心</text>
                    <text class="point">2. 经常撒谎或隐瞒重要信息</text>
                    <text class="point">3. 情绪不稳定，经常对你发脾气</text>
                    <text class="point">4. 不愿意为关系付出，总是索取</text>
                    <text class="point">5. 同时与多人保持暧昧关系</text>
                </view>
            </view>

            <view class="protection-card">
                <text class="card-title">保护自己的方法</text>
                <view class="card-content">
                    <text class="point">1. 建立清晰的底线和原则</text>
                    <text class="point">2. 学会说"不"，不要一味妥协</text>
                    <text class="point">3. 保持与朋友和家人的联系</text>
                    <text class="point">4. 相信自己的直觉，如果感觉不对就及时抽身</text>
                    <text class="point">5. 不要为了维持关系而改变自己的核心价值观</text>
                </view>
            </view>

            <view class="protection-card">
                <text class="card-title">遇到问题怎么办</text>
                <view class="card-content">
                    <text class="point">1. 冷静分析问题的本质</text>
                    <text class="point">2. 寻求信任的朋友或专业人士的建议</text>
                    <text class="point">3. 必要时果断结束不健康的关系</text>
                    <text class="point">4. 从经历中学习，提升识别能力</text>
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
.protection-container {
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

.protection-card {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.card-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #e64340;
    display: block;
    margin-bottom: 30rpx;
}

.card-content {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.point {
    font-size: 30rpx;
    color: #666;
    line-height: 1.6;
    position: relative;
    padding-left: 30rpx;
}

.point::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #007aff;
}
</style>