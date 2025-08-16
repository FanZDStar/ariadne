<!-- src/components/ChatInput.vue -->
<template>
    <view class="input-section">
        <view class="input-container">
            <textarea 
                class="input" 
                :placeholder="placeholder" 
                v-model="userInput" 
                :disabled="disabled"
                :class="{ 'disabled-input': disabled }"
                :auto-height="true"
                maxlength="-1"
                @confirm="sendMessage"
            />
            <button 
                class="submit-btn" 
                :class="{ 'disabled': !userInput.trim() || disabled }"
                :disabled="!userInput.trim() || disabled"
                @click="sendMessage"
            >
                {{ sendButtonText }}
            </button>
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
        },
        // 是否禁用输入框
        disabled: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            userInput: ''
        }
    },
    methods: {
        sendMessage() {
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
    box-shadow: none;
    flex-shrink: 0;
}

.input-container {
    display: flex;
    align-items: flex-end;
    gap: 12rpx;
}

.input {
    flex: 1;
    min-height: 45rpx;
    max-height: 200rpx;
    border: 1rpx solid #ddd;
    border-radius: 22rpx;
    padding: 12rpx 18rpx;
    font-size: 24rpx;
    background-color: #f9f9f9;
    box-sizing: border-box;
    width: 100%;
    line-height: 1.4;
    overflow-y: auto;
}

.input.disabled-input {
    background-color: #f0f0f0;
    color: #999;
}

.submit-btn {
    background-color: #007aff; /* 默认蓝色 */
    color: white;
    border-radius: 22rpx;
    height: 45rpx;
    line-height: 45rpx;
    width: 80rpx;
    font-size: 22rpx;
    flex-shrink: 0;
    border: none;
    margin-bottom: 12rpx; /* 与textarea底部对齐 */
}

.submit-btn.disabled {
    background-color: #cccccc; /* 禁用时的灰色 */
    color: #999999;
}

.submit-btn:active:not(.disabled) {
    background-color: #005ccc; /* 按下时的深蓝色 */
}
</style>