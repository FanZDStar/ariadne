<!-- src/components/ChatInput.vue -->
<template>
    <view class="input-section">
        <view class="input-container">
            <textarea class="input" :class="{ 'disabled-input': disabled, 'warning-input': inputRiskLevel !== 'low' }"
                :placeholder="placeholder" v-model="userInput" :disabled="disabled" :auto-height="true" maxlength="-1"
                @input="onInputChange" @confirm="sendMessage" />
            <button class="submit-btn"
                :class="{ 'disabled': !userInput.trim() || disabled, 'warning-btn': inputRiskLevel !== 'low' }"
                :disabled="!userInput.trim() || disabled" @click="sendMessage">
                {{ sendButtonText }}
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
            userInput: '',
            // 危机检测相关
            crisisDetector: null,
            inputRiskLevel: 'low',
            showRiskHint: false,
            riskHintText: '',
            debounceTimer: null
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
            // 清除之前的定时器
            if (this.debounceTimer) {
                clearTimeout(this.debounceTimer);
            }

            // 防抖处理，500ms后执行检测
            this.debounceTimer = setTimeout(() => {
                this.performRealTimeDetection();
            }, 500);
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

        sendMessage() {
            // 触发发送事件，让父组件处理
            this.$emit('send', this.userInput)

            // 清空输入框和重置风险状态
            this.userInput = ''
            this.inputRiskLevel = 'low'
            this.showRiskHint = false
        },

        // 提供一个方法用于外部清空输入框
        clearInput() {
            this.userInput = ''
            this.inputRiskLevel = 'low'
            this.showRiskHint = false
        }
    },

    beforeDestroy() {
        // 清理定时器
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
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

.input.warning-input {
    border-color: #ff9500;
    background-color: #fff5e6;
}

.submit-btn {
    background-color: #007aff;
    /* 默认蓝色 */
    color: white;
    border-radius: 22rpx;
    height: 45rpx;
    line-height: 45rpx;
    width: 80rpx;
    font-size: 22rpx;
    flex-shrink: 0;
    border: none;
    margin-bottom: 12rpx;
    /* 与textarea底部对齐 */
}

.submit-btn.disabled {
    background-color: #cccccc;
    /* 禁用时的灰色 */
    color: #999999;
}

.submit-btn.warning-btn {
    background-color: #ff9500;
}

.submit-btn:active:not(.disabled) {
    background-color: #005ccc;
    /* 按下时的深蓝色 */
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
</style>