<template>
    <view class="chat-container">
        <view class="chat-section">
            <scroll-view class="chat-history" scroll-y="true" :scroll-top="scrollTop" scroll-with-animation="true">
                <view v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                    <text class="message-text">{{ message.content }}</text>
                </view>
            </scroll-view>
        </view>

        <view class="input-section">
            <view class="input-container">
                <input 
                    class="input" 
                    :placeholder="placeholder" 
                    v-model="userInput" 
                    @confirm="sendMessage"
                />
                <button class="submit-btn" @click="sendMessage">发</button>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'ChatBox',
    props: {
        // 聊天消息列表
        messages: {
            type: Array,
            default: () => []
        },
        // 输入框占位符
        placeholder: {
            type: String,
            default: '请输入内容...'
        }
    },
    data() {
        return {
            userInput: '',
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
        sendMessage() {
            if (!this.userInput.trim()) {
                uni.showToast({
                    title: '请输入内容',
                    icon: 'none'
                })
                return
            }

            // 触发发送事件，让父组件处理
            this.$emit('send', this.userInput)
            
            // 清空输入框
            this.userInput = ''
        },
        
        scrollToBottom() {
            this.$nextTick(() => {
                this.scrollTop = this.messages.length * 200
            })
        }
    }
}
</script>

<style scoped>
.chat-container {
    height: 100%;
    display: flex;
    flex-direction: column;
}

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

.input-section {
    background-color: #fff;
    border-radius: 12rpx;
    padding: 12rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
    flex-shrink: 0;
}

.input-container {
    display: flex;
    align-items: center;
    gap: 12rpx;
}

.input {
    flex: 1;
    height: 45rpx;
    border: 1rpx solid #ddd;
    border-radius: 22rpx;
    padding: 0 18rpx;
    font-size: 24rpx;
    background-color: #f9f9f9;
    box-sizing: border-box;
}

.submit-btn {
    background-color: #007aff;
    color: white;
    border-radius: 22rpx;
    height: 45rpx;
    line-height: 45rpx;
    width: 80rpx;
    font-size: 22rpx;
    flex-shrink: 0;
}
</style>