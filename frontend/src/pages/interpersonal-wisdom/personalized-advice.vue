<template>
    <view class="advice-container">
        <view class="header">
            <text class="title">个性化建议</text>
            <text class="subtitle">基于你的情况，为你量身定制专业建议</text>
        </view>

        <!-- 用户情况收集 -->
        <view v-if="currentStep === 'input'" class="input-section">
            <view class="form-card">
                <text class="form-title">🤔 请描述你的情况</text>
                <text class="form-subtitle">为了给出更精准的建议，请简单描述一下你目前遇到的问题</text>

                <view class="form-item">
                    <text class="form-label">当前情况描述</text>
                    <textarea v-model="formData.situation" class="form-textarea"
                        placeholder="例如：最近和朋友相处时总是感觉很尴尬，不知道该聊什么..." maxlength="500"></textarea>
                    <text class="char-count">{{ formData.situation.length }}/500</text>
                </view>

                <view class="form-item">
                    <text class="form-label">关系类型</text>
                    <view class="relation-types">
                        <view v-for="type in relationTypes" :key="type.id" class="type-chip"
                            :class="{ active: formData.relationType === type.id }" @click="selectRelationType(type.id)">
                            <text class="type-icon">{{ type.icon }}</text>
                            <text class="type-name">{{ type.name }}</text>
                        </view>
                    </view>
                </view>

                <view class="form-item">
                    <text class="form-label">情感状态</text>
                    <view class="emotion-slider">
                        <view class="emotion-labels">
                            <text class="emotion-label">😰 焦虑</text>
                            <text class="emotion-label">😐 平静</text>
                            <text class="emotion-label">😊 开心</text>
                        </view>
                        <slider v-model="formData.emotionLevel" min="1" max="5" step="1" show-value
                            activeColor="#667eea" backgroundColor="#f0f0f0" @change="handleEmotionChange" />
                    </view>
                </view>

                <view class="form-item">
                    <text class="form-label">具体担忧</text>
                    <textarea v-model="formData.concerns" class="form-textarea small"
                        placeholder="你最担心的是什么？例如：害怕被拒绝、不知道如何开口..." maxlength="200"></textarea>
                    <text class="char-count">{{ formData.concerns.length }}/200</text>
                </view>

                <view class="form-item">
                    <text class="form-label">紧急程度</text>
                    <view class="urgency-options">
                        <view v-for="urgency in urgencyLevels" :key="urgency.id" class="urgency-item"
                            :class="{ selected: formData.urgency === urgency.id }" @click="selectUrgency(urgency.id)">
                            <text class="urgency-icon">{{ urgency.icon }}</text>
                            <text class="urgency-name">{{ urgency.name }}</text>
                            <text class="urgency-desc">{{ urgency.desc }}</text>
                        </view>
                    </view>
                </view>
            </view>

            <view class="input-actions">
                <view class="submit-btn" :class="{ disabled: !canSubmit }" @click="submitAdviceRequest">
                    <text class="btn-text">获取个性化建议</text>
                </view>
            </view>
        </view>

        <!-- 建议展示 -->
        <view v-if="currentStep === 'advice'" class="advice-section">
            <view class="advice-header">
                <text class="advice-title">💡 为你定制的建议</text>
                <text class="advice-subtitle">基于你的情况，我们为你准备了以下建议</text>
            </view>

            <!-- 核心建议卡片 -->
            <view v-if="adviceResult.core_advice" class="core-advice">
                <view class="advice-card primary">
                    <view class="card-header">
                        <text class="card-icon">🎯</text>
                        <text class="card-title">核心建议</text>
                    </view>
                    <text class="card-content">{{ adviceResult.core_advice }}</text>
                </view>
            </view>

            <!-- 具体行动建议 -->
            <view v-if="adviceResult.action_steps" class="action-steps">
                <text class="section-title">📋 具体行动步骤</text>
                <view v-for="(step, index) in adviceResult.action_steps" :key="index" class="step-item">
                    <view class="step-number">{{ index + 1 }}</view>
                    <view class="step-content">
                        <text class="step-title">{{ step.title }}</text>
                        <text class="step-desc">{{ step.description }}</text>
                        <view v-if="step.tips" class="step-tips">
                            <text v-for="tip in step.tips" :key="tip" class="tip-item">• {{ tip }}</text>
                        </view>
                    </view>
                </view>
            </view>

            <!-- AI深度分析 -->
            <view v-if="adviceResult.ai_analysis" class="ai-analysis">
                <view class="analysis-card">
                    <view class="analysis-header">
                        <text class="analysis-icon">🤖</text>
                        <text class="analysis-title">AI深度分析</text>
                    </view>
                    <text class="analysis-content">{{ adviceResult.ai_analysis }}</text>
                </view>
            </view>

            <!-- 推荐技巧 -->
            <view v-if="adviceResult.recommended_skills" class="recommended-skills">
                <text class="section-title">🚀 推荐学习技巧</text>
                <view v-for="skill in adviceResult.recommended_skills" :key="skill.id" class="skill-recommendation"
                    @click="practiceSkill(skill)">
                    <view class="skill-info">
                        <text class="skill-name">{{ skill.title }}</text>
                        <text class="skill-reason">{{ skill.reason }}</text>
                    </view>
                    <view class="skill-action">
                        <text class="action-text">立即练习</text>
                        <text class="action-arrow">→</text>
                    </view>
                </view>
            </view>

            <!-- 情感支持 -->
            <view v-if="adviceResult.emotional_support" class="emotional-support">
                <view class="support-card">
                    <view class="support-header">
                        <text class="support-icon">💝</text>
                        <text class="support-title">情感支持</text>
                    </view>
                    <text class="support-content">{{ adviceResult.emotional_support }}</text>
                </view>
            </view>

            <!-- 行动按钮 -->
            <view class="advice-actions">
                <view class="action-btn secondary" @click="restartAdviceInput">
                    <text class="btn-text">重新咨询</text>
                </view>
                <view class="action-btn primary" @click="saveAdvice">
                    <text class="btn-text">保存建议</text>
                </view>
            </view>
        </view>

        <!-- 历史建议 -->
        <view v-if="currentStep === 'history'" class="history-section">
            <text class="history-title">📚 历史建议记录</text>
            <view v-for="record in adviceHistory" :key="record.id" class="history-item"
                @click="viewHistoryAdvice(record)">
                <view class="history-header">
                    <text class="history-date">{{ formatDate(record.date) }}</text>
                    <view class="history-status" :class="record.status">
                        <text class="status-text">{{ getStatusText(record.status) }}</text>
                    </view>
                </view>
                <text class="history-situation">{{ record.situation.substring(0, 50) }}...</text>
                <text class="history-type">{{ getRelationTypeName(record.relationType) }}</text>
            </view>
        </view>

        <!-- 加载状态 -->
        <view v-if="isGenerating" class="loading-overlay">
            <view class="loading-content">
                <text class="loading-icon">🤖</text>
                <text class="loading-text">AI正在为你生成个性化建议...</text>
                <text class="loading-subtext">分析你的情况并匹配最适合的解决方案</text>
                <view class="loading-progress">
                    <view class="progress-bar">
                        <view class="progress-fill" :style="{ width: loadingProgress + '%' }"></view>
                    </view>
                    <text class="progress-text">{{ loadingProgress }}%</text>
                </view>
            </view>
        </view>

        <!-- 底部导航 -->
        <view class="bottom-nav">
            <view class="nav-item" :class="{ active: currentStep === 'input' }" @click="currentStep = 'input'">
                <text class="nav-icon">📝</text>
                <text class="nav-text">咨询建议</text>
            </view>
            <view class="nav-item" :class="{ active: currentStep === 'history' }" @click="viewHistory">
                <text class="nav-icon">📚</text>
                <text class="nav-text">历史记录</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            currentStep: 'input', // input, advice, history
            isGenerating: false,
            loadingProgress: 0,
            formData: {
                situation: '',
                relationType: '',
                emotionLevel: 3,
                concerns: '',
                urgency: 'normal'
            },
            adviceResult: null,
            adviceHistory: [],
            relationTypes: [
                { id: 'romantic', name: '恋爱关系', icon: '💕' },
                { id: 'friendship', name: '友谊关系', icon: '👫' },
                { id: 'family', name: '家庭关系', icon: '👨‍👩‍👧‍👦' },
                { id: 'colleague', name: '同事关系', icon: '👔' },
                { id: 'roommate', name: '室友关系', icon: '🏠' }
            ],
            urgencyLevels: [
                {
                    id: 'low',
                    name: '一般咨询',
                    desc: '想了解一些建议',
                    icon: '🤔'
                },
                {
                    id: 'normal',
                    name: '需要帮助',
                    desc: '遇到了一些困难',
                    icon: '😕'
                },
                {
                    id: 'urgent',
                    name: '比较紧急',
                    desc: '情况让我很困扰',
                    icon: '😰'
                }
            ]
        }
    },

    computed: {
        canSubmit() {
            return this.formData.situation.trim().length > 10 &&
                this.formData.relationType &&
                this.formData.urgency;
        }
    },

    onLoad(options) {
        // 如果从评估页面跳转过来，预填充一些信息
        if (options.fromAssessment === 'true') {
            this.formData.situation = '刚完成了关系健康评估，希望获得更具体的改善建议';
            this.formData.urgency = 'normal';
        }

        this.loadAdviceHistory();
    },

    methods: {
        selectRelationType(typeId) {
            this.formData.relationType = typeId;
        },

        selectUrgency(urgencyId) {
            this.formData.urgency = urgencyId;
        },

        handleEmotionChange(e) {
            this.formData.emotionLevel = e.detail.value;
        },

        async submitAdviceRequest() {
            if (!this.canSubmit) {
                uni.showToast({
                    title: '请完善必要信息',
                    icon: 'none'
                });
                return;
            }

            this.isGenerating = true;
            this.loadingProgress = 0;

            // 模拟进度加载
            const progressInterval = setInterval(() => {
                this.loadingProgress += 10;
                if (this.loadingProgress >= 90) {
                    clearInterval(progressInterval);
                }
            }, 200);

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/personalized-advice`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        situation: this.formData.situation,
                        relationship_type: this.formData.relationType,
                        concerns: this.formData.concerns,
                        urgency: this.formData.urgency
                    }
                });

                this.loadingProgress = 100;

                if (response.statusCode === 200) {
                    this.adviceResult = this.parseAdviceResult(response.data.personalized_advice);
                    this.currentStep = 'advice';

                    // 保存到历史记录
                    this.saveToHistory();
                }
            } catch (error) {
                console.error('获取建议失败:', error);
                uni.showToast({
                    title: '获取建议失败，请重试',
                    icon: 'none'
                });
            } finally {
                this.isGenerating = false;
                clearInterval(progressInterval);
            }
        },

        parseAdviceResult(adviceText) {
            // 这里应该解析AI返回的文本，提取结构化信息
            // 简化示例，实际项目中可能需要更复杂的解析逻辑
            return {
                core_advice: "基于你的情况，建议你先从建立基本的沟通信心开始。",
                action_steps: [
                    {
                        title: "练习基础对话技巧",
                        description: "从简单的日常问候开始，逐步增加对话深度",
                        tips: ["保持眼神接触", "主动倾听对方", "适时提问"]
                    },
                    {
                        title: "创造合适的交流机会",
                        description: "选择舒适的环境和合适的时机进行交流",
                        tips: ["选择轻松的环境", "避免压力过大的场合"]
                    }
                ],
                ai_analysis: adviceText,
                recommended_skills: [
                    {
                        id: "listen_actively",
                        title: "主动倾听",
                        reason: "帮助你更好地理解对方的感受"
                    }
                ],
                emotional_support: "记住，每个人在人际交往中都会遇到困难，这是成长的一部分。你已经迈出了寻求帮助的第一步，这很棒！"
            };
        },

        saveToHistory() {
            const record = {
                id: Date.now(),
                date: new Date(),
                situation: this.formData.situation,
                relationType: this.formData.relationType,
                urgency: this.formData.urgency,
                advice: this.adviceResult,
                status: 'new'
            };

            this.adviceHistory.unshift(record);
            uni.setStorageSync('adviceHistory', this.adviceHistory);
        },

        loadAdviceHistory() {
            const history = uni.getStorageSync('adviceHistory') || [];
            this.adviceHistory = history;
        },

        restartAdviceInput() {
            this.currentStep = 'input';
            this.formData = {
                situation: '',
                relationType: '',
                emotionLevel: 3,
                concerns: '',
                urgency: 'normal'
            };
            this.adviceResult = null;
        },

        async saveAdvice() {
            uni.showToast({
                title: '建议已保存',
                icon: 'success'
            });

            // 更新历史记录状态
            if (this.adviceHistory.length > 0) {
                this.adviceHistory[0].status = 'saved';
                uni.setStorageSync('adviceHistory', this.adviceHistory);
            }
        },

        practiceSkill(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id}&type=practice`
            });
        },

        viewHistory() {
            this.currentStep = 'history';
            this.loadAdviceHistory();
        },

        viewHistoryAdvice(record) {
            this.adviceResult = record.advice;
            this.currentStep = 'advice';
        },

        formatDate(date) {
            return new Date(date).toLocaleDateString('zh-CN', {
                month: 'numeric',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        getStatusText(status) {
            const statusMap = {
                'new': '新建议',
                'saved': '已保存',
                'applied': '已应用'
            };
            return statusMap[status] || '未知';
        },

        getRelationTypeName(typeId) {
            const type = this.relationTypes.find(t => t.id === typeId);
            return type ? type.name : '未知';
        }
    }
}
</script>

<style scoped>
.advice-container {
    padding: 0;
    background-color: #f5f5f5;
    min-height: 100vh;
    padding-bottom: 140rpx;
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

.input-section {
    padding: 40rpx;
}

.form-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.form-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.form-subtitle {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 32rpx;
}

.form-item {
    margin-bottom: 32rpx;
}

.form-label {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.form-textarea {
    width: 100%;
    min-height: 120rpx;
    padding: 20rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 12rpx;
    font-size: 28rpx;
    color: #333;
    background-color: #fafafa;
    box-sizing: border-box;
}

.form-textarea.small {
    min-height: 80rpx;
}

.char-count {
    font-size: 22rpx;
    color: #999;
    text-align: right;
    margin-top: 8rpx;
    display: block;
}

.relation-types {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
}

.type-chip {
    display: flex;
    align-items: center;
    padding: 16rpx 24rpx;
    background-color: #f8f9fa;
    border: 2rpx solid #e0e0e0;
    border-radius: 40rpx;
    transition: all 0.3s ease;
}

.type-chip.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

.type-icon {
    font-size: 24rpx;
    margin-right: 8rpx;
}

.type-name {
    font-size: 24rpx;
}

.emotion-slider {
    margin-top: 16rpx;
}

.emotion-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16rpx;
}

.emotion-label {
    font-size: 24rpx;
    color: #666;
}

.urgency-options {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}

.urgency-item {
    display: flex;
    align-items: center;
    padding: 24rpx;
    background-color: #f8f9fa;
    border: 2rpx solid #e0e0e0;
    border-radius: 12rpx;
    transition: all 0.3s ease;
}

.urgency-item.selected {
    background-color: #f0f4ff;
    border-color: #667eea;
}

.urgency-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.urgency-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-right: 16rpx;
}

.urgency-desc {
    font-size: 24rpx;
    color: #666;
    flex: 1;
}

.input-actions {
    text-align: center;
}

.submit-btn {
    background-color: #667eea;
    color: white;
    padding: 32rpx 80rpx;
    border-radius: 50rpx;
    font-size: 32rpx;
    font-weight: bold;
    display: inline-block;
}

.submit-btn.disabled {
    background-color: #ccc;
    color: #999;
}

.advice-section {
    padding: 40rpx;
}

.advice-header {
    text-align: center;
    margin-bottom: 40rpx;
}

.advice-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.advice-subtitle {
    font-size: 26rpx;
    color: #666;
}

.advice-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.advice-card.primary {
    background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
    border: 2rpx solid #667eea;
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.card-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.card-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.card-content {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.step-item {
    display: flex;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.step-number {
    width: 60rpx;
    height: 60rpx;
    background-color: #667eea;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;
    font-weight: bold;
    margin-right: 24rpx;
    flex-shrink: 0;
}

.step-content {
    flex: 1;
}

.step-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.step-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 16rpx;
}

.step-tips {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
}

.tip-item {
    font-size: 24rpx;
    color: #888;
    padding-left: 16rpx;
}

.analysis-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.analysis-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.analysis-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.analysis-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.analysis-content {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.skill-recommendation {
    display: flex;
    align-items: center;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.skill-recommendation:active {
    transform: translateY(2rpx);
}

.skill-info {
    flex: 1;
}

.skill-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.skill-reason {
    font-size: 26rpx;
    color: #666;
}

.skill-action {
    display: flex;
    align-items: center;
    color: #667eea;
}

.action-text {
    font-size: 26rpx;
    margin-right: 8rpx;
}

.action-arrow {
    font-size: 24rpx;
}

.support-card {
    background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    border: 2rpx solid #ff9999;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
}

.support-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.support-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.support-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.support-content {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.advice-actions {
    display: flex;
    gap: 20rpx;
    margin-top: 40rpx;
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

.history-section {
    padding: 40rpx;
}

.history-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 32rpx;
    display: block;
}

.history-item {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.history-item:active {
    transform: translateY(2rpx);
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.history-date {
    font-size: 24rpx;
    color: #999;
}

.history-status {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
}

.history-status.new {
    background-color: #e6f7ff;
    color: #1890ff;
}

.history-status.saved {
    background-color: #f6ffed;
    color: #52c41a;
}

.history-status.applied {
    background-color: #fff2e8;
    color: #fa8c16;
}

.status-text {
    font-size: 20rpx;
}

.history-situation {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
    line-height: 1.5;
}

.history-type {
    font-size: 24rpx;
    color: #667eea;
    padding: 6rpx 12rpx;
    background-color: #f0f4ff;
    border-radius: 12rpx;
    display: inline-block;
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
    max-width: 600rpx;
    margin: 0 40rpx;
}

.loading-icon {
    font-size: 80rpx;
    margin-bottom: 20rpx;
    display: block;
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
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
    margin-bottom: 40rpx;
    display: block;
}

.loading-progress {
    margin-top: 40rpx;
}

.progress-bar {
    width: 100%;
    height: 8rpx;
    background-color: #f0f0f0;
    border-radius: 4rpx;
    overflow: hidden;
    margin-bottom: 16rpx;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 4rpx;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 24rpx;
    color: #667eea;
    font-weight: bold;
}

.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    border-top: 1rpx solid #e0e0e0;
    padding: 20rpx 0;
    display: flex;
    z-index: 100;
}

.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16rpx;
    transition: all 0.3s ease;
}

.nav-item.active {
    color: #667eea;
}

.nav-item.active .nav-icon {
    transform: scale(1.1);
}

.nav-icon {
    font-size: 40rpx;
    margin-bottom: 8rpx;
    transition: transform 0.3s ease;
}

.nav-text {
    font-size: 22rpx;
    color: #666;
}

.nav-item.active .nav-text {
    color: #667eea;
    font-weight: bold;
}

.btn-text {
    font-size: inherit;
    color: inherit;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .advice-actions {
        flex-direction: column;
    }

    .relation-types {
        justify-content: center;
    }

    .type-chip {
        min-width: 140rpx;
        justify-content: center;
    }
}

/* 动画效果 */
.advice-card {
    animation: fadeInUp 0.5s ease-out;
}

.step-item {
    animation: fadeInLeft 0.5s ease-out;
}

.skill-recommendation {
    animation: fadeInRight 0.5s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-20rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInRight {
    from {
        opacity: 0;
        transform: translateX(20rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6rpx;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb:hover {
    background: #5a67d8;
}

/* 焦点状态 */
.form-textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3rpx rgba(102, 126, 234, 0.1);
    outline: none;
}

/* 禁用状态 */
.submit-btn.disabled:active {
    transform: none;
}

/* 触摸反馈 */
.type-chip:active,
.urgency-item:active,
.submit-btn:active,
.action-btn:active {
    transform: scale(0.98);
}

/* 长文本处理 */
.history-situation {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 安全区域适配 */
.bottom-nav {
    padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
}

.advice-container {
    padding-bottom: calc(140rpx + env(safe-area-inset-bottom));
}
</style>