<!-- src/components/ChatMessages.vue -->
<template>
    <view class="chat-section">
        <scroll-view class="chat-history" scroll-y="true" :scroll-top="scrollTop" scroll-with-animation="true">
            <view v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                <text class="message-text">{{ message.content }}</text>
            </view>
        </scroll-view>
    </view>
</template>

<script>
export default {
    name: 'ChatMessages',
    props: {
        // 聊天消息列表
        messages: {
            type: Array,
            default: () => []
        }
    },
    data() {
        return {
            scrollTop: 0
        }
    },
    watch: {
        // 监听消息变化，自动滚动到底部
        messages: {
            handler() {
                this.scrollToBottom()
            },
            deep: true
        }
    },
    methods: {
        scrollToBottom() {
            this.$nextTick(() => {
                this.scrollTop = this.messages.length * 200
            })
        }
    }
}
</script>

<style scoped>
.chat-section {
    flex: 1;
    margin-bottom: 20rpx;
    background-color: #fff;
    border-radius: 15rpx;
    padding: 15rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.chat-history {
    flex: 1;
    height: 100%;
}

.message {
    padding: 15rpx;
    margin-bottom: 15rpx;
    border-radius: 8rpx;
    max-width: 80%;
}

.message.user {
    background-color: #007aff;
    color: white;
    margin-left: auto;
}

.message.ai {
    background-color: #f0f0f0;
    color: #333;
    margin-right: auto;
}

.message-text {
    font-size: 26rpx;
    line-height: 1.4;
    white-space: pre-wrap;
}
</style>