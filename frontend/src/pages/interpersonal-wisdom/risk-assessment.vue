<template>
    <view class="assessment-container">
        <view class="header">
            <text class="title">关系健康评估</text>
            <text class="subtitle">评估你当前关系的健康状况，获得专业建议</text>
        </view>

        <!-- 开始评估页面 -->
        <view v-if="currentStep === 'start'" class="start-section">
            <view class="intro-card">
                <view class="intro-header">
                    <text class="intro-icon">📊</text>
                    <text class="intro-title">为什么需要关系评估？</text>
                </view>
                <text class="intro-text">
                    健康的人际关系对心理健康至关重要。通过科学的评估，你可以：
                </text>
                <view class="benefits-list">
                    <text class="benefit-item">• 了解当前关系的健康状况</text>
                    <text class="benefit-item">• 识别潜在的风险信号</text>
                    <text class="benefit-item">• 获得个性化的改善建议</text>
                    <text class="benefit-item">• 提升情感安全意识</text>
                </view>
            </view>

            <view class="relation-types">
                <text class="section-title">请选择你要评估的关系类型：</text>
                <view class="type-grid">
                    <view v-for="type in relationTypes" :key="type.id" class="type-card"
                        :class="{ selected: selectedRelationType === type.id }" @click="selectRelationType(type.id)">
                        <text class="type-icon">{{ type.icon }}</text>
                        <text class="type-name">{{ type.name }}</text>
                        <text class="type-desc">{{ type.desc }}</text>
                    </view>
                </view>
            </view>

            <view class="start-actions">
                <view class="start-btn" :class="{ disabled: !selectedRelationType }" @click="startAssessment">
                    <text class="btn-text">开始评估</text>
                </view>
            </view>
        </view>

        <!-- 评估问题页面 -->
        <view v-if="currentStep === 'assessment'" class="questions-section">
            <view class="progress-bar">
                <view class="progress-fill" :style="{ width: progressPercentage + '%' }"></view>
            </view>
            <text class="progress-text">{{ currentQuestionIndex + 1 }} / {{ assessmentQuestions.length }}</text>

            <view v-if="currentQuestion" class="question-card">
                <text class="question-text">{{ currentQuestion.question }}</text>
                <view class="options-list">
                    <view v-for="(option, index) in currentQuestion.options" :key="index" class="option-item"
                        :class="{ selected: selectedAnswers[currentQuestion.id] === index }"
                        @click="selectOption(index)">
                        <view class="option-radio">
                            <view class="radio-dot" v-if="selectedAnswers[currentQuestion.id] === index"></view>
                        </view>
                        <text class="option-text">{{ option }}</text>
                    </view>
                </view>
            </view>

            <view class="question-actions">
                <view class="action-btn secondary" v-if="currentQuestionIndex > 0" @click="previousQuestion">
                    <text class="btn-text">上一题</text>
                </view>
                <view class="action-btn primary"
                    :class="{ disabled: selectedAnswers[currentQuestion.id] === undefined }" @click="nextQuestion">
                    <text class="btn-text">{{ isLastQuestion ? '完成评估' : '下一题' }}</text>
                </view>
            </view>
        </view>

        <!-- 评估结果页面 -->
        <view v-if="currentStep === 'result'" class="result-section">
            <view class="result-header">
                <text class="result-icon">{{ getRiskIcon(assessmentResult.risk_level) }}</text>
                <text class="result-title">评估完成</text>
                <text class="result-subtitle">基于你的回答，我们为你生成了专业分析</text>
            </view>

            <view class="result-summary">
                <view class="summary-card">
                    <text class="summary-title">风险等级</text>
                    <view class="risk-level" :class="assessmentResult.risk_level">
                        <text class="level-text">{{ getRiskText(assessmentResult.risk_level) }}</text>
                        <text class="level-score">{{ assessmentResult.risk_percentage.toFixed(1) }}%</text>
                    </view>
                </view>

                <view class="summary-card">
                    <text class="summary-title">关系类型</text>
                    <text class="relation-name">{{ getRelationTypeName(selectedRelationType) }}</text>
                </view>
            </view>

            <view class="ai-analysis">
                <text class="analysis-title">🤖 AI专业分析</text>
                <view class="analysis-content">
                    <text class="analysis-text">{{ assessmentResult.ai_analysis }}</text>
                </view>
            </view>

            <view class="recommendations" v-if="assessmentResult.recommendations">
                <text class="rec-title">💡 个性化建议</text>
                <view v-for="(rec, index) in assessmentResult.recommendations" :key="index" class="rec-item">
                    <view class="rec-header">
                        <text class="rec-type">{{ rec.type }}</text>
                        <view class="rec-priority" :class="rec.priority">
                            <text class="priority-text">{{ getPriorityText(rec.priority) }}</text>
                        </view>
                    </view>
                    <text class="rec-content">{{ rec.content }}</text>
                </view>
            </view>

            <view class="result-actions">
                <view class="action-btn secondary" @click="restartAssessment">
                    <text class="btn-text">重新评估</text>
                </view>
                <view class="action-btn primary" @click="getPersonalizedAdvice">
                    <text class="btn-text">获取更多建议</text>
                </view>
            </view>
        </view>

        <!-- 加载状态 -->
        <view v-if="isAnalyzing" class="loading-overlay">
            <view class="loading-content">
                <text class="loading-icon">🤖</text>
                <text class="loading-text">AI正在分析你的回答...</text>
                <text class="loading-subtext">请稍候，这可能需要几秒钟</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            currentStep: 'start', // start, assessment, result
            selectedRelationType: '',
            assessmentQuestions: [],
            currentQuestionIndex: 0,
            selectedAnswers: {},
            assessmentResult: null,
            isAnalyzing: false,
            relationTypes: [
                {
                    id: 'romantic',
                    name: '恋爱关系',
                    desc: '评估与恋人的关系健康度',
                    icon: '💕'
                },
                {
                    id: 'friendship',
                    name: '友谊关系',
                    desc: '评估与朋友的关系质量',
                    icon: '👫'
                },
                {
                    id: 'family',
                    name: '家庭关系',
                    desc: '评估与家人的相处状况',
                    icon: '👨‍👩‍👧‍👦'
                },
                {
                    id: 'roommate',
                    name: '室友关系',
                    desc: '评估与室友的相处情况',
                    icon: '🏠'
                }
            ]
        }
    },

    computed: {
        currentQuestion() {
            return this.assessmentQuestions[this.currentQuestionIndex];
        },

        progressPercentage() {
            return ((this.currentQuestionIndex + 1) / this.assessmentQuestions.length) * 100;
        },

        isLastQuestion() {
            return this.currentQuestionIndex === this.assessmentQuestions.length - 1;
        }
    },

    methods: {
        selectRelationType(typeId) {
            this.selectedRelationType = typeId;
        },

        async startAssessment() {
            if (!this.selectedRelationType) {
                uni.showToast({
                    title: '请选择关系类型',
                    icon: 'none'
                });
                return;
            }

            try {
                uni.showLoading({ title: '准备评估题目...' });

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/risk-assessment`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    this.assessmentQuestions = response.data.assessment_questions;
                    this.currentStep = 'assessment';
                    this.currentQuestionIndex = 0;
                    this.selectedAnswers = {};
                }
            } catch (error) {
                console.error('获取评估题目失败:', error);
                uni.showToast({
                    title: '获取题目失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        selectOption(optionIndex) {
            this.$set(this.selectedAnswers, this.currentQuestion.id, optionIndex);
        },

        previousQuestion() {
            if (this.currentQuestionIndex > 0) {
                this.currentQuestionIndex--;
            }
        },

        async nextQuestion() {
            if (this.selectedAnswers[this.currentQuestion.id] === undefined) {
                uni.showToast({
                    title: '请选择一个答案',
                    icon: 'none'
                });
                return;
            }

            if (this.isLastQuestion) {
                await this.submitAssessment();
            } else {
                this.currentQuestionIndex++;
            }
        },

        async submitAssessment() {
            try {
                this.isAnalyzing = true;

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/risk-assessment/analyze`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        answers: this.selectedAnswers,
                        relationship_type: this.selectedRelationType
                    }
                });

                if (response.statusCode === 200) {
                    this.assessmentResult = response.data;
                    this.currentStep = 'result';
                }
            } catch (error) {
                console.error('提交评估失败:', error);
                uni.showToast({
                    title: '分析失败，请重试',
                    icon: 'none'
                });
            } finally {
                this.isAnalyzing = false;
            }
        },

        restartAssessment() {
            this.currentStep = 'start';
            this.selectedRelationType = '';
            this.assessmentQuestions = [];
            this.currentQuestionIndex = 0;
            this.selectedAnswers = {};
            this.assessmentResult = null;
        },

        getPersonalizedAdvice() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/personalized-advice?fromAssessment=true'
            });
        },

        getRiskIcon(level) {
            const icons = {
                'low': '✅',
                'medium': '⚠️',
                'high': '🚨',
                'critical': '🆘'
            };
            return icons[level] || '📊';
        },

        getRiskText(level) {
            const texts = {
                'low': '较低风险',
                'medium': '中等风险',
                'high': '较高风险',
                'critical': '高危风险'
            };
            return texts[level] || '未知';
        },

        getRelationTypeName(typeId) {
            const type = this.relationTypes.find(t => t.id === typeId);
            return type ? type.name : '未知';
        },

        getPriorityText(priority) {
            const texts = {
                'urgent': '紧急',
                'high': '重要',
                'medium': '建议',
                'low': '参考'
            };
            return texts[priority] || '建议';
        }
    }
}
</script>

<style scoped>
.assessment-container {
    padding: 0;
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60rpx 40rpx 40rpx;
    color: white;
    text-align: center;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
    margin-bottom: 16rpx;
    display: block;
}

.subtitle {
    font-size: 28rpx;
    opacity: 0.9;
}

.start-section,
.questions-section,
.result-section {
    padding: 40rpx;
}

.intro-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.intro-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.intro-icon {
    font-size: 36rpx;
    margin-right: 16rpx;
}

.intro-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.intro-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 24rpx;
}

.benefits-list {
    display: flex;
    flex-direction: column;
    gap: 12rpx;
}

.benefit-item {
    font-size: 26rpx;
    color: #555;
    line-height: 1.5;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.type-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20rpx;
    margin-bottom: 40rpx;
}

.type-card {
    width: calc(50% - 10rpx);
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.type-card.selected {
    border-color: #667eea;
    background-color: #f8f9ff;
}

.type-icon {
    font-size: 48rpx;
    display: block;
    margin-bottom: 16rpx;
}

.type-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.type-desc {
    font-size: 24rpx;
    color: #999;
}

.start-actions {
    text-align: center;
}

.start-btn {
    background-color: #667eea;
    color: white;
    padding: 32rpx 80rpx;
    border-radius: 50rpx;
    font-size: 32rpx;
    font-weight: bold;
    display: inline-block;
}

.start-btn.disabled {
    background-color: #ccc;
    color: #999;
}

.progress-bar {
    height: 8rpx;
    background-color: #e0e0e0;
    border-radius: 4rpx;
    margin-bottom: 16rpx;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background-color: #667eea;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 24rpx;
    color: #999;
    text-align: center;
    margin-bottom: 40rpx;
    display: block;
}

.question-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 40rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.question-text {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    line-height: 1.5;
    margin-bottom: 32rpx;
    display: block;
}

.options-list {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.option-item {
    display: flex;
    align-items: center;
    padding: 24rpx;
    background-color: #f8f9fa;
    border-radius: 12rpx;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.option-item.selected {
    border-color: #667eea;
    background-color: #f0f4ff;
}

.option-radio {
    width: 32rpx;
    height: 32rpx;
    border: 2rpx solid #ddd;
    border-radius: 50%;
    margin-right: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
}

.option-item.selected .option-radio {
    border-color: #667eea;
}

.radio-dot {
    width: 16rpx;
    height: 16rpx;
    background-color: #667eea;
    border-radius: 50%;
}

.option-text {
    flex: 1;
    font-size: 28rpx;
    color: #333;
    line-height: 1.4;
}

.question-actions {
    display: flex;
    gap: 20rpx;
}

.action-btn {
    flex: 1;
    padding: 28rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 28rpx;
    font-weight: bold;
}

.action-btn.primary {
    background-color: #667eea;
    color: white;
}

.action-btn.secondary {
    background-color: #f0f0f0;
    color: #666;
}

.action-btn.disabled {
    background-color: #ccc;
    color: #999;
}

.result-header {
    text-align: center;
    margin-bottom: 40rpx;
}

.result-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 20rpx;
}

.result-title {
    font-size: 48rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.result-subtitle {
    font-size: 28rpx;
    color: #666;
}

.result-summary {
    display: flex;
    gap: 20rpx;
    margin-bottom: 40rpx;
}

.summary-card {
    flex: 1;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.summary-title {
    font-size: 24rpx;
    color: #999;
    margin-bottom: 16rpx;
    display: block;
}

.risk-level {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.level-text {
    font-size: 32rpx;
    font-weight: bold;
    margin-bottom: 8rpx;
    display: block;
}

.level-score {
    font-size: 24rpx;
    opacity: 0.8;
}

.risk-level.low .level-text {
    color: #4caf50;
}

.risk-level.medium .level-text {
    color: #ff9800;
}

.risk-level.high .level-text {
    color: #f44336;
}

.risk-level.critical .level-text {
    color: #d32f2f;
}

.relation-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.ai-analysis {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.analysis-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.analysis-content {
    background-color: #f8f9fa;
    border-radius: 12rpx;
    padding: 24rpx;
}

.analysis-text {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.recommendations {
    margin-bottom: 40rpx;
}

.rec-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.rec-item {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.rec-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.rec-type {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
}

.rec-priority {
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
    font-size: 20rpx;
}

.rec-priority.urgent {
    background-color: #ffebee;
    color: #f44336;
}

.rec-priority.high {
    background-color: #fff3e0;
    color: #ff9800;
}

.rec-priority.medium {
    background-color: #e8f5e8;
    color: #4caf50;
}

.rec-priority.low {
    background-color: #f0f0f0;
    color: #666;
}

.priority-text {
    font-size: 20rpx;
}

.rec-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
}

.result-actions {
    display: flex;
    gap: 20rpx;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-content {
    background-color: white;
    border-radius: 20rpx;
    padding: 60rpx 40rpx;
    text-align: center;
    margin: 40rpx;
}

.loading-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 20rpx;
    animation: pulse 1.5s ease-in-out infinite;
}

.loading-text {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.loading-subtext {
    font-size: 26rpx;
    color: #666;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }

    100% {
        transform: scale(1);
    }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .type-grid {
        flex-direction: column;
    }

    .type-card {
        width: 100%;
    }

    .result-summary {
        flex-direction: column;
    }

    .question-actions {
        flex-direction: column;
    }

    .result-actions {
        flex-direction: column;
    }
}
</style>