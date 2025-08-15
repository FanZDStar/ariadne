<!-- src/components/ChatInput.vue -->
<template>
    <view class="input-section">
        <view class="input-container">
            <input 
                class="input" 
                :placeholder="placeholder" 
                v-model="userInput" 
                @confirm="sendMessage"
            />
            <button class="submit-btn" @click="sendMessage">{{ sendButtonText }}</button>
        </view>
    </view>
</template>

<script>
export default {
    name: 'ChatInput',
    props: {
        // 输入框占位符
        placeholder: {
            type: String,
            default: '请输入内容...'
        },
        // 发送按钮文字
        sendButtonText: {
            type: String,
            default: '发送'
        }
    },
    data() {
        return {
            userInput: ''
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
        
        // 提供一个方法用于外部清空输入框
        clearInput() {
            this.userInput = ''
        }
    }
}
</script>

<style scoped>
.input-section {
    background-color: #fff;
    border-radius: 12rpx;
    padding: 12rpx;
    box-shadow: none; /* 移除原来的阴影 */
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