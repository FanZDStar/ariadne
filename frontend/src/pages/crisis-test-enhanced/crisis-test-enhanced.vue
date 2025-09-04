<!-- AI增强危机检测测试页面 -->
<template>
    <view class="test-container">
        <view class="header">
            <text class="title">🤖 AI增强危机检测测试</text>
            <text class="subtitle">测试模糊输入、同音字、AI分析等功能</text>
        </view>

        <view class="test-section">
            <text class="section-title">测试输入</text>
            <textarea class="test-input" v-model="testInput" placeholder="输入测试文本，支持模糊输入、同音字等..." auto-height />

            <view class="test-options">
                <view class="option-row">
                    <text class="option-label">聊天场景：</text>
                    <picker mode="selector" :value="sceneIndex" :range="sceneOptions" range-key="name"
                        @change="onSceneChange">
                        <view class="picker-text">{{ sceneOptions[sceneIndex].name }}</view>
                    </picker>
                </view>

                <view class="option-row">
                    <text class="option-label">启用AI分析：</text>
                    <switch :checked="enableAI" @change="onAIToggle" color="#007aff" />
                </view>
            </view>

            <button class="test-btn" :class="{ 'disabled': !testInput.trim() || isAnalyzing }"
                :disabled="!testInput.trim() || isAnalyzing" @click="performTest">
                {{ isAnalyzing ? '分析中...' : '🔍 执行检测' }}
            </button>
        </view>

        <view class="results-section" v-if="testResult">
            <text class="section-title">检测结果</text>

            <!-- 风险等级显示 -->
            <view class="risk-card" :class="testResult.risk_level">
                <view class="risk-header">
                    <text class="risk-icon">{{ getRiskIcon(testResult.risk_level) }}</text>
                    <text class="risk-level">{{ getRiskLevelText(testResult.risk_level) }}</text>
                    <text class="risk-score">{{ testResult.risk_score.toFixed(1) }}分</text>
                </view>
            </view>

            <!-- 检测详情 -->
            <view class="detail-cards">
                <!-- 关键词检测 -->
                <view class="detail-card" v-if="testResult.detected_keywords.length > 0">
                    <text class="card-title">🎯 检测到的关键词</text>
                    <view class="keyword-list">
                        <text v-for="keyword in testResult.detected_keywords" :key="keyword" class="keyword-tag">
                            {{ keyword }}
                        </text>
                    </view>
                </view>

                <!-- 模糊匹配 -->
                <view class="detail-card" v-if="testResult.fuzzy_matches.length > 0">
                    <text class="card-title">🔍 模糊匹配结果</text>
                    <view class="keyword-list">
                        <text v-for="match in testResult.fuzzy_matches" :key="match" class="fuzzy-tag">
                            {{ match }}
                        </text>
                    </view>
                </view>

                <!-- AI分析 -->
                <view class="detail-card" v-if="testResult.ai_analysis">
                    <text class="card-title">🤖 AI分析结果</text>
                    <text class="ai-analysis">{{ testResult.ai_analysis }}</text>
                </view>

                <!-- 测试信息 -->
                <view class="detail-card">
                    <text class="card-title">📊 测试信息</text>
                    <view class="info-list">
                        <view class="info-item">
                            <text class="info-label">场景：</text>
                            <text class="info-value">{{ sceneOptions[sceneIndex].name }}</text>
                        </view>
                        <view class="info-item">
                            <text class="info-label">关键词得分：</text>
                            <text class="info-value">{{ testResult.keyword_score.toFixed(1) }}</text>
                        </view>
                        <view class="info-item">
                            <text class="info-label">AI分析：</text>
                            <text class="info-value">{{ enableAI ? '已启用' : '已禁用' }}</text>
                        </view>
                        <view class="info-item">
                            <text class="info-label">检测时间：</text>
                            <text class="info-value">{{ formatTime(testResult.timestamp) }}</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 预设测试用例 -->
        <view class="preset-section">
            <text class="section-title">📝 预设测试用例</text>
            <scroll-view class="preset-list" scroll-y>
                <view v-for="(preset, index) in presetTests" :key="index" class="preset-item"
                    @click="usePreset(preset)">
                    <view class="preset-header">
                        <text class="preset-title">{{ preset.title }}</text>
                        <text class="preset-level" :class="preset.expectedLevel">
                            {{ getRiskLevelText(preset.expectedLevel) }}
                        </text>
                    </view>
                    <text class="preset-content">{{ preset.content }}</text>
                </view>
            </scroll-view>
        </view>
    </view>
</template>

<script>
import { CrisisAPI, CrisisKeywordDetector, CrisisUtils } from '../../utils/crisisApi.js';

export default {
    data() {
        return {
            testInput: '',
            isAnalyzing: false,
            testResult: null,
            enableAI: true,
            sceneIndex: 0,
            sceneOptions: [
                { value: 'self-dialog', name: '自我对话' },
                { value: 'love-experiment', name: '恋爱练习' },
                { value: 'self-love', name: '爱自己' },
                { value: 'tree-hole', name: '树洞倾诉' },
                { value: 'general', name: '通用场景' }
            ],
            presetTests: [
                {
                    title: '模糊输入测试',
                    content: '我想zi sha，感觉zi己没用',
                    expectedLevel: 'critical'
                },
                {
                    title: '同音字测试',
                    content: '想4了，活着没意思',
                    expectedLevel: 'critical'
                },
                {
                    title: '拆字测试',
                    content: '自 杀算了，受不了了',
                    expectedLevel: 'critical'
                },
                {
                    title: '情绪表达测试',
                    content: '最近情绪不太好，有点焦虑',
                    expectedLevel: 'low'
                },
                {
                    title: '多关键词测试',
                    content: '感觉绝望，很孤独，没人理解我',
                    expectedLevel: 'high'
                },
                {
                    title: '隐晦表达测试',
                    content: '如果有一天我不在了，你们会想我吗',
                    expectedLevel: 'medium'
                },
                {
                    title: '正常对话测试',
                    content: '今天天气不错，心情也还可以',
                    expectedLevel: 'low'
                },
                {
                    title: '英文混合测试',
                    content: '我want to die，真的很pain',
                    expectedLevel: 'high'
                }
            ]
        };
    },

    methods: {
        onSceneChange(e) {
            this.sceneIndex = e.detail.value;
        },

        onAIToggle(e) {
            this.enableAI = e.detail.value;
        },

        usePreset(preset) {
            this.testInput = preset.content;
        },

        async performTest() {
            if (!this.testInput.trim()) return;

            this.isAnalyzing = true;

            try {
                const scene = this.sceneOptions[this.sceneIndex].value;

                // 调用AI增强检测API
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/crisis/assess-risk`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    },
                    data: {
                        content: this.testInput,
                        scene: scene,
                        keyword_score: 0,
                        enable_ai_analysis: this.enableAI
                    }
                });

                if (response.statusCode === 200) {
                    this.testResult = response.data;

                    // 显示检测结果提示
                    this.showResultToast();
                } else {
                    throw new Error(`API错误: ${response.statusCode}`);
                }

            } catch (error) {
                console.error('检测失败:', error);
                uni.showToast({
                    title: '检测失败，请重试',
                    icon: 'none'
                });
            } finally {
                this.isAnalyzing = false;
            }
        },

        showResultToast() {
            const config = CrisisUtils.getWarningConfig(this.testResult.risk_level);
            uni.showToast({
                title: `${config.icon} ${config.title}`,
                icon: 'none',
                duration: 2000
            });
        },

        getRiskIcon(level) {
            const icons = {
                'low': '💙',
                'medium': '⚠️',
                'high': '🚨',
                'critical': '🆘'
            };
            return icons[level] || '💙';
        },

        getRiskLevelText(level) {
            const texts = {
                'low': '低风险',
                'medium': '中等风险',
                'high': '高风险',
                'critical': '极高风险'
            };
            return texts[level] || '未知';
        },

        formatTime(timestamp) {
            return new Date(timestamp).toLocaleString();
        }
    }
};
</script>

<style scoped>
.test-container {
    padding: 20rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-bottom: 30rpx;
}

.title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.subtitle {
    font-size: 24rpx;
    color: #666;
}

.test-section {
    background: white;
    border-radius: 12rpx;
    padding: 20rpx;
    margin-bottom: 20rpx;
}

.section-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 15rpx;
}

.test-input {
    width: 100%;
    min-height: 120rpx;
    border: 1rpx solid #ddd;
    border-radius: 8rpx;
    padding: 12rpx;
    font-size: 24rpx;
    margin-bottom: 15rpx;
    box-sizing: border-box;
}

.test-options {
    margin-bottom: 20rpx;
}

.option-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 15rpx;
}

.option-label {
    font-size: 24rpx;
    color: #333;
}

.picker-text {
    color: #007aff;
    font-size: 24rpx;
}

.test-btn {
    width: 100%;
    background: linear-gradient(45deg, #007aff, #5856d6);
    color: white;
    border-radius: 8rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: 28rpx;
    font-weight: bold;
    border: none;
}

.test-btn.disabled {
    background: #ccc;
    color: #999;
}

.results-section {
    background: white;
    border-radius: 12rpx;
    padding: 20rpx;
    margin-bottom: 20rpx;
}

.risk-card {
    border-radius: 8rpx;
    padding: 15rpx;
    margin-bottom: 15rpx;
}

.risk-card.low {
    background: linear-gradient(45deg, #e6f7ff, #f0f9ff);
    border-left: 4rpx solid #52c41a;
}

.risk-card.medium {
    background: linear-gradient(45deg, #fff7e6, #fffbe6);
    border-left: 4rpx solid #faad14;
}

.risk-card.high {
    background: linear-gradient(45deg, #ffe7e7, #fff2f0);
    border-left: 4rpx solid #ff7875;
}

.risk-card.critical {
    background: linear-gradient(45deg, #ffebee, #ffebee);
    border-left: 4rpx solid #f5222d;
}

.risk-header {
    display: flex;
    align-items: center;
    gap: 10rpx;
}

.risk-icon {
    font-size: 32rpx;
}

.risk-level {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    flex: 1;
}

.risk-score {
    font-size: 24rpx;
    color: #666;
}

.detail-cards {
    display: flex;
    flex-direction: column;
    gap: 15rpx;
}

.detail-card {
    background: #fafafa;
    border-radius: 8rpx;
    padding: 15rpx;
}

.card-title {
    font-size: 24rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.keyword-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8rpx;
}

.keyword-tag {
    background: #ff7875;
    color: white;
    font-size: 20rpx;
    padding: 4rpx 8rpx;
    border-radius: 4rpx;
}

.fuzzy-tag {
    background: #faad14;
    color: white;
    font-size: 20rpx;
    padding: 4rpx 8rpx;
    border-radius: 4rpx;
}

.ai-analysis {
    font-size: 22rpx;
    color: #333;
    line-height: 1.4;
}

.info-list {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
}

.info-item {
    display: flex;
    font-size: 22rpx;
}

.info-label {
    color: #666;
    width: 120rpx;
}

.info-value {
    color: #333;
    flex: 1;
}

.preset-section {
    background: white;
    border-radius: 12rpx;
    padding: 20rpx;
}

.preset-list {
    max-height: 400rpx;
}

.preset-item {
    border: 1rpx solid #eee;
    border-radius: 8rpx;
    padding: 12rpx;
    margin-bottom: 10rpx;
    cursor: pointer;
}

.preset-item:active {
    background: #f0f0f0;
}

.preset-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8rpx;
}

.preset-title {
    font-size: 24rpx;
    font-weight: bold;
    color: #333;
}

.preset-level {
    font-size: 20rpx;
    padding: 2rpx 6rpx;
    border-radius: 4rpx;
    color: white;
}

.preset-level.low {
    background: #52c41a;
}

.preset-level.medium {
    background: #faad14;
}

.preset-level.high {
    background: #ff7875;
}

.preset-level.critical {
    background: #f5222d;
}

.preset-content {
    font-size: 22rpx;
    color: #666;
    line-height: 1.4;
}
</style>
