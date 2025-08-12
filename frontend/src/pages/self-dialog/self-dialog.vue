<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">自己与自己的对话</text>
            <text class="subtitle">反思感情中的言行举止，获得AI引导和建议</text>
        </view>

        <view class="content">
            <view class="input-section">
                <textarea class="textarea" placeholder="请描述你在感情中遇到的问题或困惑，以及对方的反应..." v-model="userInput" />
                <button class="submit-btn" @click="submitDialog">提交并获取建议</button>
            </view>

            <view class="response-section" v-if="aiResponse">
                <text class="section-title">AI分析与建议</text>
                <view class="response-content">
                    <text>{{ aiResponse }}</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            userInput: '',
            aiResponse: ''
        }
    },
    methods: {
        submitDialog() {
            if (!this.userInput) {
                uni.showToast({
                    title: '请输入内容',
                    icon: 'none'
                })
                return
            }

            // 模拟AI响应（实际应调用后端API）
            this.aiResponse = "感谢你的分享。从你的描述中，我看到了你在感情中的真诚和反思。在面对感情问题时，能够自我反思是非常宝贵的品质。建议你可以：\n\n1. 诚实面对自己的感受\n2. 学会表达而非压抑情感\n3. 给彼此一些时间和空间\n4. 关注自己的成长和需求";

            uni.showToast({
                title: '分析完成',
                icon: 'success'
            })
        }
    }
}
</script>

<style scoped>
.dialog-container {
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

.input-section {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
    margin-bottom: 40rpx;
}

.textarea {
    width: 100%;
    height: 300rpx;
    border: 1rpx solid #eee;
    border-radius: 10rpx;
    padding: 20rpx;
    font-size: 30rpx;
    margin-bottom: 30rpx;
    box-sizing: border-box;
}

.submit-btn {
    background-color: #007aff;
    color: white;
    border-radius: 10rpx;
    height: 80rpx;
    line-height: 80rpx;
}

.response-section {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.section-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 30rpx;
}

.response-content {
    font-size: 30rpx;
    color: #666;
    line-height: 1.6;
}
</style>