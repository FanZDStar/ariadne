<template>
    <view class="assessment-container">
        <view class="header">
            <view class="header-content">
                <view class="header-icon">
                    <text class="icon-text">📊</text>
                </view>
                <view class="header-text">
                    <text class="title">关系健康评估</text>
                    <text class="subtitle">评估你当前关系的健康状况，获得专业建议</text>
                </view>
            </view>
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
                        :class="{ selected: selectedRelationType === type.id }" 
                        :style="selectedRelationType === type.id ? `border-color: ${type.color}; background: linear-gradient(135deg, ${type.lightColor} 0%, #ffffff 100%); --selected-color: ${type.color}` : ''"
                        @click="selectRelationType(type.id)">
                        <text class="type-icon">{{ type.icon }}</text>
                        <view class="type-content">
                            <text class="type-name" :style="selectedRelationType === type.id ? `color: ${type.color}` : ''">{{ type.name }}</text>
                            <text class="type-desc">{{ type.desc }}</text>
                        </view>
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

        <!-- AI分析提交中页面 -->
        <view v-if="currentStep === 'analyzing'" class="analyzing-section">
            <view class="analyzing-animation">
                <view class="robot-container">
                    <text class="robot-icon">🤖</text>
                    <view class="thinking-dots">
                        <view class="dot dot1"></view>
                        <view class="dot dot2"></view>
                        <view class="dot dot3"></view>
                    </view>
                </view>
            </view>
            
            <view class="analyzing-content">
                <text class="analyzing-title">AI正在分析您的回答</text>
                <text class="analyzing-subtitle">这可能需要1-2分钟...</text>
                
                <view class="analyzing-steps">
                    <view class="step-item active">
                        <view class="step-icon">✅</view>
                        <text class="step-text">答案已提交</text>
                    </view>
                    <view class="step-item" :class="{ active: analyzingStep >= 2 }">
                        <view class="step-icon">{{ analyzingStep >= 2 ? '✅' : '⏳' }}</view>
                        <text class="step-text">数据分析中</text>
                    </view>
                    <view class="step-item" :class="{ active: analyzingStep >= 3 }">
                        <view class="step-icon">{{ analyzingStep >= 3 ? '✅' : '⏳' }}</view>
                        <text class="step-text">生成报告中</text>
                    </view>
                </view>
            </view>
            
            <view class="notification-card">
                <view class="notification-header">
                    <text class="notification-icon">📋</text>
                    <text class="notification-title">分析完成后的查看方式</text>
                </view>
                <text class="notification-text">AI分析完成后，您可以在以下位置查看详细报告：</text>
                <view class="notification-path">
                    <text class="path-step">人际智慧</text>
                    <text class="path-arrow">→</text>
                    <text class="path-step">成长档案</text>
                    <text class="path-arrow">→</text>
                    <text class="path-step highlight">报告解读</text>
                </view>
                <text class="auto-redirect-text">正在为您跳转回上一页...</text>
            </view>
        </view>

        <!-- 评估结果页面 -->
        <view v-if="currentStep === 'result'" class="result-section">
            <view class="result-header">
                <text class="result-icon">{{ getScoreIcon(assessmentResult.overall_percentage) }}</text>
                <text class="result-title">评估完成</text>
                <text class="result-subtitle">基于你的回答，我们为你生成了专业分析</text>
            </view>

            <view class="result-summary">
                <view class="summary-card">
                    <text class="summary-title">总体得分</text>
                    <view class="score-level" :class="getScoreLevelClass(assessmentResult.overall_percentage)">
                        <text class="level-text">{{ assessmentResult.overall_level.level }}</text>
                        <text class="level-score">{{ assessmentResult.overall_percentage.toFixed(1) }}%</text>
                    </view>
                    <text class="level-desc">{{ assessmentResult.overall_level.description }}</text>
                </view>

                <view class="summary-card">
                    <text class="summary-title">关系类型</text>
                    <text class="relation-name">{{ getRelationTypeName(selectedRelationType) }}</text>
                </view>
            </view>

            <!-- 维度分析 -->
            <view class="dimension-analysis" v-if="assessmentResult.dimension_analysis">
                <text class="analysis-title">📊 各维度表现</text>
                <view v-for="(dimension, name) in assessmentResult.dimension_analysis" :key="name" class="dimension-item">
                    <view class="dimension-header">
                        <text class="dimension-name">{{ name }}</text>
                        <text class="dimension-score">{{ dimension.percentage.toFixed(1) }}%</text>
                    </view>
                    <view class="dimension-bar">
                        <view class="bar-fill" :style="{ 
                            width: dimension.percentage + '%',
                            backgroundColor: getDimensionColor(dimension.percentage)
                        }"></view>
                    </view>
                    <text class="dimension-level">{{ dimension.level.level }}</text>
                </view>
            </view>

            <view class="ai-analysis">
                <text class="analysis-title">🤖 AI专业分析</text>
                <view class="analysis-content">
                    <view class="formatted-text" v-html="formatAnalysisText(assessmentResult.ai_analysis)"></view>
                </view>
            </view>

            <view class="recommendations" v-if="assessmentResult.recommendations && assessmentResult.recommendations.length > 0">
                <text class="rec-title">💡 个性化建议</text>
                <view v-for="(rec, index) in assessmentResult.recommendations" :key="index" class="rec-item">
                    <view class="rec-header">
                        <text class="rec-type">{{ rec.title }}</text>
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
            currentStep: 'start', // start, assessment, analyzing, result
            selectedRelationType: '',
            assessmentQuestions: [],
            currentQuestionIndex: 0,
            selectedAnswers: {},
            assessmentResult: null,
            isAnalyzing: false,
            analyzingStep: 1, // 分析步骤：1-提交完成，2-数据分析中，3-生成报告中
            relationTypes: [
                {
                    id: 'family',
                    name: '家庭关系',
                    desc: '评估与家人的沟通、理解和情感连接',
                    icon: '👨‍👩‍👧‍👦',
                    color: '#4caf50',
                    lightColor: '#e8f5e8'
                },
                {
                    id: 'friendship',
                    name: '友谊关系',
                    desc: '评估与朋友的信任、支持和互动质量',
                    icon: '👫',
                    color: '#2196f3',
                    lightColor: '#e3f2fd'
                },
                {
                    id: 'romantic',
                    name: '恋爱关系',
                    desc: '评估与恋人的情感亲密和关系健康度',
                    icon: '💕',
                    color: '#e91e63',
                    lightColor: '#fce4ec'
                },
                {
                    id: 'mentor',
                    name: '师生关系',
                    desc: '评估与导师或老师的学习互动关系',
                    icon: '👨‍🏫',
                    color: '#ff9800',
                    lightColor: '#fff3e0'
                }
            ],
            sessionToken: '', // 测评会话标识
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
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/relationship-assessment/start`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        relationship_type: this.selectedRelationType
                    }
                });

                if (response.statusCode === 200) {
                    this.assessmentQuestions = response.data.questions;
                    this.sessionToken = response.data.session_token;
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
                console.log('开始提交评估，切换到分析状态');
                // 切换到分析状态
                this.currentStep = 'analyzing';
                this.analyzingStep = 1;
                
                console.log('当前步骤：', this.currentStep);
                
                // 启动分析步骤动画
                setTimeout(() => {
                    console.log('步骤2激活');
                    this.analyzingStep = 2;
                }, 1000);
                
                setTimeout(() => {
                    console.log('步骤3激活');
                    this.analyzingStep = 3;
                }, 2000);

                // 提交评估数据（异步，不等待AI分析结果）
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/relationship-assessment/submit`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        session_token: this.sessionToken,
                        relationship_type: this.selectedRelationType,
                        answers: this.selectedAnswers,
                        async_mode: true // 告诉后端这是异步模式
                    }
                });

                console.log('API响应:', response);

                if (response.statusCode === 200) {
                    // 3秒后显示完成提示并跳转回人际智慧主页
                    setTimeout(() => {
                        console.log('显示成功提示');
                        uni.showToast({
                            title: '评估提交成功！请稍后在成长档案中查看报告解读',
                            icon: 'success',
                            duration: 2000
                        });
                        
                        // Toast显示完后跳转回人际智慧主页
                        setTimeout(() => {
                            console.log('准备跳转回上一页');
                            uni.navigateBack();
                        }, 2000);
                    }, 3000);
                } else {
                    throw new Error('提交失败');
                }

            } catch (error) {
                console.error('提交评估失败:', error);
                uni.showToast({
                    title: '提交失败，请重试',
                    icon: 'none'
                });
                // 回到评估页面
                this.currentStep = 'assessment';
            }
        },

        restartAssessment() {
            this.currentStep = 'start';
            this.selectedRelationType = '';
            this.assessmentQuestions = [];
            this.currentQuestionIndex = 0;
            this.selectedAnswers = {};
            this.assessmentResult = null;
            this.sessionToken = '';
            this.analyzingStep = 1;
        },

        getPersonalizedAdvice() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/personalized-advice?fromAssessment=true'
            });
        },

        getScoreIcon(percentage) {
            if (percentage >= 85) return '🌟';
            if (percentage >= 70) return '😊';
            if (percentage >= 55) return '😐';
            if (percentage >= 40) return '😔';
            return '😟';
        },

        getScoreLevelClass(percentage) {
            if (percentage >= 85) return 'excellent';
            if (percentage >= 70) return 'good';
            if (percentage >= 55) return 'average';
            if (percentage >= 40) return 'below-average';
            return 'poor';
        },

        getDimensionColor(percentage) {
            if (percentage >= 85) return '#52C41A';
            if (percentage >= 70) return '#1890FF';
            if (percentage >= 55) return '#FAAD14';
            if (percentage >= 40) return '#FF7A45';
            return '#F5222D';
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
        },

        formatAnalysisText(text) {
            if (!text) return '';
            
            return text
                // 处理加粗文本 **text** 或 __text__
                .replace(/\*\*(.*?)\*\*/g, '<strong class="bold-text">$1</strong>')
                .replace(/__(.*?)__/g, '<strong class="bold-text">$1</strong>')
                // 处理斜体文本 *text* 或 _text_
                .replace(/\*(.*?)\*/g, '<em class="italic-text">$1</em>')
                .replace(/_(.*?)_/g, '<em class="italic-text">$1</em>')
                // 处理标题 ## text
                .replace(/^## (.*?)$/gm, '<h3 class="heading-text">$1</h3>')
                .replace(/^### (.*?)$/gm, '<h4 class="subheading-text">$1</h4>')
                // 处理列表项 - text 或 * text
                .replace(/^[-*] (.*?)$/gm, '<div class="list-item">• $1</div>')
                // 处理数字列表 1. text
                .replace(/^\d+\. (.*?)$/gm, '<div class="numbered-item">$1</div>')
                // 处理段落（双换行转为段落分隔）
                .replace(/\n\s*\n/g, '</p><p class="paragraph">')
                // 处理单换行（转为行内换行）
                .replace(/\n/g, '<br class="line-break"/>')
                // 包装整体内容为段落
                .replace(/^/, '<p class="paragraph">')
                .replace(/$/, '</p>');
        }
    }
}
</script>

<style scoped>
.assessment-container {
    padding: 0;
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
    padding: 60rpx 40rpx 60rpx;
    color: #1976d2;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8rpx 32rpx rgba(144, 202, 249, 0.3);
    border-radius: 0 0 60rpx 40rpx;
    margin-bottom: 40rpx;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(227, 242, 253, 0.1);
    backdrop-filter: blur(10rpx);
}

.header-content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
}

.header-icon {
    width: 120rpx;
    height: 120rpx;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 32rpx;
    backdrop-filter: blur(10rpx);
    border: 2rpx solid rgba(255, 255, 255, 0.3);
}

.icon-text {
    font-size: 56rpx;
    filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.2));
}

.header-text {
    flex: 1;
}
.title {
    font-size: 48rpx;
    font-weight: bold;
    margin-bottom: 16rpx;
    display: block;
    text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.subtitle {
    font-size: 28rpx;
    opacity: 0.9;
    line-height: 1.4;
    text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.start-section,
.questions-section,
.result-section {
    padding: 30rpx 40rpx 50rpx;
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

.relation-types {
    margin-bottom: 50rpx;
}

.section-title {
    font-size: 34rpx;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 32rpx;
    display: block;
    text-align: center;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -12rpx;
    left: 50%;
    transform: translateX(-50%);
    width: 60rpx;
    height: 4rpx;
    background: linear-gradient(90deg, #42a5f5, #1976d2);
    border-radius: 2rpx;
}

.type-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24rpx;
    margin-bottom: 40rpx;
}

.type-card {
    background-color: white;
    border-radius: 20rpx;
    padding: 32rpx 24rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 6rpx 24rpx rgba(0, 0, 0, 0.08);
    border: 3rpx solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.type-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4rpx;
    background: #e0e0e0;
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.type-card.selected {
    transform: translateY(-4rpx);
    box-shadow: 0 12rpx 32rpx rgba(0, 0, 0, 0.15);
}

.type-card.selected::before {
    transform: scaleX(1);
    background: var(--selected-color, #42a5f5);
}

.type-icon {
    font-size: 56rpx;
    margin-right: 24rpx;
    flex-shrink: 0;
    filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.1));
}

.type-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.type-name {
    font-size: 30rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 6rpx;
    line-height: 1.3;
}

.type-desc {
    font-size: 24rpx;
    color: #666;
    line-height: 1.4;
    opacity: 0.9;
}

.start-actions {
    text-align: center;
    margin-top: 20rpx;
}

.start-btn {
    background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
    color: white;
    padding: 36rpx 100rpx;
    border-radius: 60rpx;
    font-size: 32rpx;
    font-weight: 600;
    display: inline-block;
    box-shadow: 0 8rpx 24rpx rgba(66, 165, 245, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.start-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.start-btn:active::before {
    left: 100%;
}

.start-btn:active {
    transform: translateY(2rpx);
    box-shadow: 0 6rpx 16rpx rgba(102, 126, 234, 0.25);
}

.start-btn.disabled {
    background: #e0e0e0;
    color: #9e9e9e;
    box-shadow: none;
    cursor: not-allowed;
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
    background-color: #42a5f5;
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
    border-color: #42a5f5;
    background-color: #e3f2fd;
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
    border-color: #42a5f5;
}

.radio-dot {
    width: 16rpx;
    height: 16rpx;
    background-color: #42a5f5;
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
    background-color: #42a5f5;
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

/* 新的评分样式 */
.score-level {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.score-level.excellent .level-text {
    color: #52C41A;
}

.score-level.good .level-text {
    color: #1890FF;
}

.score-level.average .level-text {
    color: #FAAD14;
}

.score-level.below-average .level-text {
    color: #FF7A45;
}

.score-level.poor .level-text {
    color: #F5222D;
}

.level-desc {
    font-size: 24rpx;
    color: #666;
    text-align: center;
    margin-top: 8rpx;
}

/* 维度分析样式 */
.dimension-analysis {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.dimension-item {
    margin-bottom: 32rpx;
}

.dimension-item:last-child {
    margin-bottom: 0;
}

.dimension-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12rpx;
}

.dimension-name {
    font-size: 28rpx;
    font-weight: 600;
    color: #333;
}

.dimension-score {
    font-size: 26rpx;
    font-weight: 600;
    color: #1890FF;
}

.dimension-bar {
    height: 20rpx;
    background-color: #f0f0f0;
    border-radius: 10rpx;
    overflow: hidden;
    margin-bottom: 12rpx;
    border: 1rpx solid #e8e8e8;
}

.bar-fill {
    height: 100%;
    transition: width 0.8s ease-out;
    border-radius: 10rpx;
    box-shadow: inset 0 1rpx 2rpx rgba(255, 255, 255, 0.3);
}

.dimension-level {
    font-size: 24rpx;
    color: #666;
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
    padding: 32rpx 28rpx;
    border-left: 6rpx solid #42a5f5;
}

.analysis-text {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.formatted-text {
    font-size: 28rpx;
    color: #555;
    line-height: 1.8;
}

.formatted-text .paragraph {
    margin: 0 0 16rpx 0;
    text-align: justify;
}

.formatted-text .paragraph:last-child {
    margin-bottom: 0;
}

.formatted-text .line-break {
    margin: 4rpx 0;
}

.formatted-text .bold-text {
    font-weight: bold;
    color: #333;
}

.formatted-text .italic-text {
    font-style: italic;
    color: #666;
}

.formatted-text .heading-text {
    font-size: 32rpx;
    font-weight: bold;
    color: #42a5f5;
    margin: 24rpx 0 12rpx 0;
    display: block;
}

.formatted-text .subheading-text {
    font-size: 30rpx;
    font-weight: 600;
    color: #555;
    margin: 20rpx 0 8rpx 0;
    display: block;
}

.formatted-text .list-item {
    margin: 6rpx 0;
    padding-left: 16rpx;
    color: #555;
    line-height: 1.6;
}

.formatted-text .numbered-item {
    margin: 6rpx 0;
    padding-left: 20rpx;
    color: #555;
    position: relative;
    counter-increment: item;
    line-height: 1.6;
}

.formatted-text .numbered-item::before {
    content: counter(item) ". ";
    position: absolute;
    left: 0;
    color: #42a5f5;
    font-weight: bold;
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
        grid-template-columns: 1fr;
        gap: 20rpx;
    }

    .type-card {
        padding: 28rpx 20rpx;
    }

    .type-icon {
        font-size: 48rpx;
        margin-right: 20rpx;
    }

    .type-name {
        font-size: 28rpx;
    }

    .type-desc {
        font-size: 22rpx;
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
    
    .analyzing-steps {
        max-width: 100%;
    }
    
    .notification-path {
        flex-direction: column;
        gap: 8rpx;
    }
    
    .path-arrow {
        transform: rotate(90deg);
    }
    
    .analyzing-actions {
        flex-direction: column;
    }
}

/* 分析页面样式 */
.analyzing-section {
    padding: 60rpx 40rpx;
    text-align: center;
    min-height: calc(100vh - 120rpx);
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
}

.analyzing-animation {
    margin-bottom: 60rpx;
}

.robot-container {
    position: relative;
    display: inline-block;
}

.robot-icon {
    font-size: 120rpx;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-20rpx);
    }
    60% {
        transform: translateY(-10rpx);
    }
}

.thinking-dots {
    display: flex;
    justify-content: center;
    margin-top: 20rpx;
    gap: 8rpx;
}

.dot {
    width: 12rpx;
    height: 12rpx;
    background-color: #42a5f5;
    border-radius: 50%;
    animation: thinking 1.4s infinite ease-in-out;
}

.dot1 { animation-delay: -0.32s; }
.dot2 { animation-delay: -0.16s; }
.dot3 { animation-delay: 0; }

@keyframes thinking {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1.2);
        opacity: 1;
    }
}

.analyzing-content {
    margin-bottom: 60rpx;
}

.analyzing-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #1976d2;
    margin-bottom: 16rpx;
    display: block;
}

.analyzing-subtitle {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 50rpx;
    display: block;
}

.analyzing-steps {
    display: flex;
    flex-direction: column;
    gap: 24rpx;
    max-width: 400rpx;
    margin: 0 auto;
}

.step-item {
    display: flex;
    align-items: center;
    padding: 20rpx;
    background: white;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.step-item.active {
    background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);
    border-left: 6rpx solid #4caf50;
}

.step-icon {
    font-size: 32rpx;
    margin-right: 20rpx;
    width: 40rpx;
}

.step-text {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
}

.notification-card {
    background: white;
    border-radius: 20rpx;
    padding: 40rpx;
    margin-bottom: 50rpx;
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
    text-align: left;
}

.notification-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.notification-icon {
    font-size: 32rpx;
    margin-right: 12rpx;
}

.notification-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
}

.notification-text {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 24rpx;
    display: block;
}

.notification-path {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12rpx;
    padding: 24rpx;
    background: #f8f9fa;
    border-radius: 16rpx;
}

.path-step {
    font-size: 26rpx;
    padding: 12rpx 20rpx;
    background: #e9ecef;
    border-radius: 20rpx;
    color: #495057;
    font-weight: 500;
}

.path-step.highlight {
    background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
    color: white;
    box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.3);
}

.path-arrow {
    font-size: 24rpx;
    color: #6c757d;
    font-weight: bold;
}

.auto-redirect-text {
    font-size: 24rpx;
    color: #42a5f5;
    text-align: center;
    margin-top: 20rpx;
    display: block;
    opacity: 0.8;
    animation: pulse 1.5s ease-in-out infinite;
}

.analyzing-actions {
    display: flex;
    gap: 20rpx;
}
</style>