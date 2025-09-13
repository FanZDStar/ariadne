<template>
    <view class="input-section" :class="themeClass">
        <!-- 输入状态提示 -->
        <view v-if="showTypingIndicator" class="typing-indicator">
            <view class="typing-dots">
                <view class="dot"></view>
                <view class="dot"></view>
                <view class="dot"></view>
            </view>
            <text class="typing-text">正在输入...</text>
        </view>

        <view class="input-container">
            <textarea 
                class="input" 
                :class="{ 
                    'disabled-input': disabled, 
                    'warning-input': inputRiskLevel !== 'low',
                    'typing-active': isTyping
                }"
                :placeholder="placeholder" 
                v-model="userInput" 
                :disabled="disabled" 
                :auto-height="true" 
                maxlength="-1"
                @input="onInputChange" 
                @confirm="sendMessage"
                @focus="handleFocus"
                @blur="handleBlur"
            />
            <button 
                class="submit-btn"
                :class="{ 
                    'disabled': !userInput.trim() || disabled, 
                    'warning-btn': inputRiskLevel !== 'low',
                    'sending': isSending
                }"
                :disabled="!userInput.trim() || disabled" 
                @click="sendMessage"
            >
                <text v-if="!isSending" class="btn-text">{{ sendButtonText }}</text>
                <view v-else class="loading-spinner"></view>
            </button>
        </view>

        <!-- 实时风险提示 -->
        <view v-if="inputRiskLevel !== 'low' && showRiskHint" class="risk-hint" :class="inputRiskLevel">
            <text class="risk-icon">⚠️</text>
            <text class="risk-text">{{ riskHintText }}</text>
            <text class="risk-close" @click="hideRiskHint">×</text>
        </view>
    </view>
</template>

<script>
// 引入危机检测工具
import { CrisisKeywordDetector, CrisisUtils } from '../utils/crisisApi.js';

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
            default: '发'
        },
        // 是否禁用输入框
        disabled: {
            type: Boolean,
            default: false
        },
        // 主题配色
        theme: {
            type: String,
            default: 'default', // default, emotion, interpersonal, tree-hole
            validator: value => ['default', 'emotion', 'interpersonal', 'tree-hole'].includes(value)
        },
        // 是否显示输入状态提示
        showTypingIndicator: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            userInput: '',
            // 危机检测相关
            crisisDetector: null,
            inputRiskLevel: 'low',
            showRiskHint: false,
            riskHintText: '',
            debounceTimer: null,
            // 输入状态相关
            isTyping: false,
            typingTimer: null,
            isSending: false
        }
    },
    computed: {
        // 根据主题返回样式类
        themeClass() {
            return `theme-${this.theme}`
        }
    },
    mounted() {
        // 初始化危机检测器
        this.crisisDetector = new CrisisKeywordDetector();
    },
    methods: {
        /**
         * 输入内容变化处理
         */
        onInputChange() {
            // 输入状态管理
            this.isTyping = true;
            this.$emit('typing-start');
            
            // 清除之前的输入状态定时器
            if (this.typingTimer) {
                clearTimeout(this.typingTimer);
            }
            
            // 2秒后隐藏输入状态
            this.typingTimer = setTimeout(() => {
                this.isTyping = false;
                this.$emit('typing-end');
            }, 2000);

            // 清除之前的危机检测定时器
            if (this.debounceTimer) {
                clearTimeout(this.debounceTimer);
            }

            // 防抖处理，500ms后执行检测
            this.debounceTimer = setTimeout(() => {
                this.performRealTimeDetection();
            }, 500);
        },

        /**
         * 输入框获得焦点
         */
        handleFocus() {
            this.$emit('input-focus');
        },

        /**
         * 输入框失去焦点
         */
        handleBlur() {
            this.isTyping = false;
            this.$emit('input-blur');
            this.$emit('typing-end');
        },

        /**
         * 执行实时检测
         */
        performRealTimeDetection() {
            if (!this.userInput.trim()) {
                this.inputRiskLevel = 'low';
                this.showRiskHint = false;
                return;
            }

            const riskResult = this.crisisDetector.detectKeywords(this.userInput);
            this.inputRiskLevel = riskResult.level;

            if (riskResult.level !== 'low') {
                this.showRiskHint = true;
                this.riskHintText = this.getRiskHintText(riskResult);
            } else {
                this.showRiskHint = false;
            }
        },

        /**
         * 获取风险提示文本
         */
        getRiskHintText(riskResult) {
            const config = CrisisUtils.getWarningConfig(riskResult.level);
            const keywords = riskResult.keywords.slice(0, 2).join('、');
            return `检测到风险关键词：${keywords}。${config.hint || '建议谨慎表达或寻求帮助。'}`;
        },

        /**
         * 隐藏风险提示
         */
        hideRiskHint() {
            this.showRiskHint = false;
        },

        async sendMessage() {
            if (!this.userInput.trim() || this.disabled || this.isSending) return;

            this.isSending = true;
            this.isTyping = false;
            
            try {
                // 触发发送事件，让父组件处理
                this.$emit('send', this.userInput);

                // 清空输入框和重置状态
                this.userInput = '';
                this.inputRiskLevel = 'low';
                this.showRiskHint = false;
                this.$emit('typing-end');
            } finally {
                // 延迟重置发送状态，给用户反馈
                setTimeout(() => {
                    this.isSending = false;
                }, 500);
            }
        },

        // 提供一个方法用于外部清空输入框
        clearInput() {
            this.userInput = '';
            this.inputRiskLevel = 'low';
            this.showRiskHint = false;
            this.isTyping = false;
            this.isSending = false;
        }
    },

    beforeDestroy() {
        // 清理定时器
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        if (this.typingTimer) {
            clearTimeout(this.typingTimer);
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
    transition: all 0.3s ease;
}

/* 输入状态指示器 */
.typing-indicator {
    display: flex;
    align-items: center;
    padding: 8rpx 16rpx;
    margin-bottom: 8rpx;
    background: rgba(0, 122, 255, 0.1);
    border-radius: 16rpx;
    animation: fadeInUp 0.3s ease;
}

.typing-dots {
    display: flex;
    gap: 4rpx;
    margin-right: 8rpx;
}

.typing-dots .dot {
    width: 6rpx;
    height: 6rpx;
    background-color: #007aff;
    border-radius: 50%;
    animation: typingDots 1.4s infinite;
}

.typing-dots .dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots .dot:nth-child(3) {
    animation-delay: 0.4s;
}

.typing-text {
    font-size: 20rpx;
    color: #007aff;
}

/* 主题样式 */
.theme-emotion .typing-indicator {
    background: rgba(41, 182, 246, 0.1);
}

.theme-emotion .typing-dots .dot,
.theme-emotion .typing-text {
    color: #29b6f6;
}

.theme-interpersonal .typing-indicator {
    background: rgba(156, 39, 176, 0.1);
}

.theme-interpersonal .typing-dots .dot,
.theme-interpersonal .typing-text {
    color: #9c27b0;
}

.theme-tree-hole .typing-indicator {
    background: rgba(76, 175, 80, 0.1);
}

.theme-tree-hole .typing-dots .dot,
.theme-tree-hole .typing-text {
    color: #4caf50;
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
    border: 2rpx solid #e0e0e0;
    border-radius: 22rpx;
    padding: 12rpx 18rpx;
    font-size: 24rpx;
    background-color: #f9f9f9;
    box-sizing: border-box;
    width: 100%;
    line-height: 1.4;
    overflow-y: auto;
    transition: all 0.3s ease;
}

.input:focus,
.input.typing-active {
    border-color: #007aff;
    background-color: #fff;
    box-shadow: 0 0 0 4rpx rgba(0, 122, 255, 0.1);
}

.input.disabled-input {
    background-color: #f0f0f0;
    color: #999;
    border-color: #d0d0d0;
}

.input.warning-input {
    border-color: #ff9500;
    background-color: #fff5e6;
}

.submit-btn {
    /* 默认灰色状态 - 没有输入时 */
    background-color: #cccccc;
    color: #999999;
    border-radius: 22rpx;
    height: 45rpx;
    line-height: 45rpx;
    width: 80rpx;
    font-size: 22rpx;
    flex-shrink: 0;
    border: none;
    margin-bottom: 12rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

/* 有输入内容且不是禁用状态时显示蓝色 */
.submit-btn:not(.disabled) {
    background-color: #007aff;
    color: white;
}

.submit-btn.disabled {
    background-color: #cccccc;
    color: #999999;
}

.submit-btn.warning-btn {
    background-color: #ff9500;
}

.submit-btn.sending {
    background-color: #5ac8fa;
    transform: scale(0.95);
}

.submit-btn:active:not(.disabled) {
    transform: scale(0.98);
}

/* 主题按钮样式 - 只在非禁用状态下应用主题色 */
.theme-emotion .submit-btn:not(.disabled) {
    background-color: #29b6f6;
}

.theme-emotion .input:focus,
.theme-emotion .input.typing-active {
    border-color: #29b6f6;
    box-shadow: 0 0 0 4rpx rgba(41, 182, 246, 0.1);
}

.theme-interpersonal .submit-btn:not(.disabled) {
    background-color: #9c27b0;
}

.theme-interpersonal .input:focus,
.theme-interpersonal .input.typing-active {
    border-color: #9c27b0;
    box-shadow: 0 0 0 4rpx rgba(156, 39, 176, 0.1);
}

.theme-tree-hole .submit-btn:not(.disabled) {
    background-color: #4caf50;
}

.theme-tree-hole .input:focus,
.theme-tree-hole .input.typing-active {
    border-color: #4caf50;
    box-shadow: 0 0 0 4rpx rgba(76, 175, 80, 0.1);
}

.btn-text {
    font-size: 22rpx;
}

/* 加载动画 */
.loading-spinner {
    width: 20rpx;
    height: 20rpx;
    border: 2rpx solid rgba(255, 255, 255, 0.3);
    border-top: 2rpx solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* 风险提示样式 */
.risk-hint {
    display: flex;
    align-items: center;
    margin-top: 8rpx;
    padding: 8rpx 12rpx;
    border-radius: 8rpx;
    font-size: 20rpx;
    animation: fadeIn 0.3s ease-in;
}

.risk-hint.medium {
    background-color: #fff5e6;
    border: 1rpx solid #ff9500;
    color: #ff6600;
}

.risk-hint.high {
    background-color: #ffe6e6;
    border: 1rpx solid #ff3333;
    color: #cc0000;
}

.risk-hint.critical {
    background-color: #ffebee;
    border: 1rpx solid #d32f2f;
    color: #d32f2f;
}

.risk-icon {
    margin-right: 6rpx;
    font-size: 18rpx;
}

.risk-text {
    flex: 1;
    line-height: 1.3;
}

.risk-close {
    margin-left: 8rpx;
    font-size: 24rpx;
    cursor: pointer;
    padding: 0 4rpx;
}

/* 动画定义 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10rpx);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10rpx);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes typingDots {
    0%, 60%, 100% {
        transform: scale(1);
        opacity: 0.5;
    }
    30% {
        transform: scale(1.2);
        opacity: 1;
    }
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>