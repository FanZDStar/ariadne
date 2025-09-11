<template>
    <view class="practice-container">
        <view class="header">
            <text class="title">技能练习</text>
            <text class="subtitle">在安全环境中练习交往技巧</text>
        </view>

        <!-- 技能信息展示 -->
        <view v-if="skillInfo" class="skill-info">
            <view class="skill-card">
                <view class="skill-header">
                    <text class="skill-title">{{ skillInfo.title }}</text>
                    <view class="difficulty-badge" :class="skillInfo.difficulty">
                        <text class="difficulty-text">{{ getDifficultyText(skillInfo.difficulty) }}</text>
                    </view>
                </view>
                <text class="skill-content">{{ skillInfo.content }}</text>
                <view class="skill-tags">
                    <text v-for="tag in skillInfo.tags" :key="tag" class="skill-tag">{{ tag }}</text>
                </view>
            </view>
        </view>

        <!-- 场景展示模式 -->
        <view v-if="practiceType === 'scenario' && scenarioData" class="scenario-section">
            <view class="scenario-card">
                <text class="scenario-title">🎬 练习场景</text>
                <view class="scenario-content">
                    <text class="scenario-text">{{ scenarioData.content }}</text>
                </view>
                <view class="scenario-actions">
                    <view class="action-btn primary" @click="startScenarioPractice">
                        <text class="btn-text">开始练习</text>
                    </view>
                    <view class="action-btn secondary" @click="regenerateScenario">
                        <text class="btn-text">重新生成</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 交互练习模式 -->
        <view v-if="practiceType === 'practice' || practiceMode === 'interactive'" class="interactive-section">
            <view class="practice-guide">
                <text class="guide-title">💡 练习指导</text>
                <text class="guide-text">
                    请根据以下情景，练习运用"{{ skillInfo?.title }}"技巧。我会扮演对话中的另一方，为你提供反馈。
                </text>
            </view>

            <!-- 聊天区域 -->
            <view class="chat-area">
                <view v-for="(message, index) in chatMessages" :key="index" class="message-item" :class="message.role">
                    <view class="message-avatar">
                        <text class="avatar-text">{{ message.role === 'user' ? '我' : 'AI' }}</text>
                    </view>
                    <view class="message-content">
                        <text class="message-text">{{ message.content }}</text>
                    </view>
                </view>

                <view v-if="isAiTyping" class="message-item ai typing">
                    <view class="message-avatar">
                        <text class="avatar-text">AI</text>
                    </view>
                    <view class="message-content">
                        <view class="typing-indicator">
                            <view class="typing-dot"></view>
                            <view class="typing-dot"></view>
                            <view class="typing-dot"></view>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 输入区域 -->
            <view class="input-area">
                <view class="input-container">
                    <textarea v-model="userInput" class="input-field" placeholder="输入你的回应..." :disabled="isAiTyping"
                        @input="handleInput"></textarea>
                    <view class="send-btn" :class="{ disabled: !userInput.trim() || isAiTyping }" @click="sendMessage">
                        <text class="send-text">发送</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 练习完成反馈 -->
        <view v-if="practiceCompleted" class="feedback-section">
            <view class="feedback-card">
                <text class="feedback-title">🎉 练习完成</text>
                <view class="feedback-content">
                    <text class="feedback-text">{{ practiceResult.feedback }}</text>
                </view>
                <view class="feedback-actions">
                    <view class="action-btn secondary" @click="restartPractice">
                        <text class="btn-text">再次练习</text>
                    </view>
                    <view class="action-btn primary" @click="nextSkill">
                        <text class="btn-text">学习下一个技巧</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 练习统计 -->
        <view v-if="practiceStats" class="stats-section">
            <text class="stats-title">📊 练习统计</text>
            <view class="stats-grid">
                <view class="stat-item">
                    <text class="stat-number">{{ practiceStats.totalPractices }}</text>
                    <text class="stat-label">总练习次数</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ practiceStats.masteredSkills }}</text>
                    <text class="stat-label">掌握技巧</text>
                </view>
                <view class="stat-item">
                    <text class="stat-number">{{ practiceStats.averageScore }}%</text>
                    <text class="stat-label">平均得分</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            skillId: '',
            practiceType: 'scenario', // scenario, practice
            skillInfo: null,
            scenarioData: null,
            practiceMode: '', // interactive, guided
            chatMessages: [],
            userInput: '',
            isAiTyping: false,
            practiceCompleted: false,
            practiceResult: null,
            practiceStats: null
        }
    },

    onLoad(options) {
        this.skillId = options.skillId || '';
        this.practiceType = options.type || 'scenario';
        this.initializePractice();
    },

    methods: {
        async initializePractice() {
            // 加载技能信息
            await this.loadSkillInfo();

            // 根据练习类型初始化
            if (this.practiceType === 'scenario') {
                await this.loadScenario();
            } else {
                await this.startInteractivePractice();
            }

            // 加载练习统计
            await this.loadPracticeStats();
        },

        async loadSkillInfo() {
            // 从存储中获取技能信息（实际项目中应该调用API）
            const cachedScenario = uni.getStorageSync('currentScenario');
            if (cachedScenario && cachedScenario.skill) {
                this.skillInfo = cachedScenario.skill;
            }
        },

        async loadScenario() {
            const cachedScenario = uni.getStorageSync('currentScenario');
            if (cachedScenario && cachedScenario.scenario) {
                this.scenarioData = cachedScenario.scenario;
            }
        },

        async regenerateScenario() {
            try {
                uni.showLoading({ title: '重新生成中...' });

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/${this.skillId}/generate-scenario`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.statusCode === 200) {
                    this.scenarioData = response.data.scenario;
                }
            } catch (error) {
                console.error('重新生成场景失败:', error);
                uni.showToast({
                    title: '生成失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        startScenarioPractice() {
            this.practiceMode = 'interactive';
            this.initializeChat();
        },

        async startInteractivePractice() {
            this.practiceMode = 'interactive';
            this.initializeChat();
        },

        initializeChat() {
            this.chatMessages = [
                {
                    role: 'ai',
                    content: `欢迎来到"${this.skillInfo?.title}"的练习环节！我会创建一个情景，让你练习这个技巧。准备好了吗？`
                }
            ];
        },

        handleInput() {
            // 可以添加实时输入反馈
        },

        async sendMessage() {
            if (!this.userInput.trim() || this.isAiTyping) return;

            const userMessage = this.userInput.trim();
            this.chatMessages.push({
                role: 'user',
                content: userMessage
            });

            this.userInput = '';
            this.isAiTyping = true;

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/interactive-practice`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        skill_id: this.skillId,
                        user_response: userMessage,
                        scenario_context: this.scenarioData?.content || ''
                    }
                });

                if (response.statusCode === 200) {
                    const result = response.data;

                    this.chatMessages.push({
                        role: 'ai',
                        content: result.ai_feedback
                    });

                    if (result.practice_completed) {
                        this.practiceCompleted = true;
                        this.practiceResult = result;
                    }
                }
            } catch (error) {
                console.error('发送消息失败:', error);
                this.chatMessages.push({
                    role: 'ai',
                    content: '抱歉，系统暂时无法响应，请稍后再试。'
                });
            } finally {
                this.isAiTyping = false;
            }
        },

        async loadPracticeStats() {
            // 模拟练习统计数据
            this.practiceStats = {
                totalPractices: 12,
                masteredSkills: 8,
                averageScore: 85
            };
        },

        restartPractice() {
            this.practiceCompleted = false;
            this.practiceResult = null;
            this.chatMessages = [];
            this.initializeChat();
        },

        nextSkill() {
            uni.showToast({
                title: '即将推荐下一个技巧',
                icon: 'success'
            });

            setTimeout(() => {
                uni.navigateBack();
            }, 1500);
        },

        getDifficultyText(difficulty) {
            const map = {
                'basic': '基础',
                'intermediate': '进阶',
                'advanced': '高级'
            };
            return map[difficulty] || '基础';
        }
    }
}
</script>

<style scoped>
.practice-container {
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

.skill-info {
    padding: 40rpx;
}

.skill-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.skill-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.difficulty-badge {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
}

.difficulty-badge.basic {
    background-color: #e8f5e8;
    color: #4caf50;
}

.difficulty-badge.intermediate {
    background-color: #fff3e0;
    color: #ff9800;
}

.difficulty-badge.advanced {
    background-color: #ffebee;
    color: #f44336;
}

.skill-content {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 20rpx;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
}

.skill-tag {
    background-color: #f0f0f0;
    color: #666;
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
    font-size: 22rpx;
}

.scenario-section {
    padding: 0 40rpx 40rpx;
}

.scenario-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.scenario-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.scenario-content {
    background-color: #f8f9fa;
    border-radius: 12rpx;
    padding: 24rpx;
    margin-bottom: 24rpx;
}

.scenario-text {
    font-size: 28rpx;
    color: #555;
    line-height: 1.7;
}

.scenario-actions {
    display: flex;
    gap: 16rpx;
}

.interactive-section {
    padding: 0 40rpx 40rpx;
}

.practice-guide {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.guide-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.guide-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
}

.chat-area {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;
    min-height: 400rpx;
    max-height: 600rpx;
    overflow-y: auto;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.message-item {
    display: flex;
    margin-bottom: 24rpx;
    align-items: flex-start;
}

.message-item.user {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 60rpx;
    height: 60rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 16rpx;
}

.user .message-avatar {
    background-color: #667eea;
    color: white;
}

.ai .message-avatar {
    background-color: #f0f0f0;
    color: #666;
}

.avatar-text {
    font-size: 20rpx;
    font-weight: bold;
}

.message-content {
    flex: 1;
    max-width: 80%;
}

.message-text {
    background-color: #f8f9fa;
    padding: 20rpx;
    border-radius: 16rpx;
    font-size: 28rpx;
    color: #333;
    line-height: 1.5;
    display: block;
}

.user .message-text {
    background-color: #667eea;
    color: white;
}

.typing-indicator {
    display: flex;
    align-items: center;
    padding: 20rpx;
    background-color: #f8f9fa;
    border-radius: 16rpx;
    gap: 8rpx;
}

.typing-dot {
    width: 12rpx;
    height: 12rpx;
    background-color: #999;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {

    0%,
    80%,
    100% {
        transform: scale(1);
        opacity: 0.5;
    }

    40% {
        transform: scale(1.2);
        opacity: 1;
    }
}

.input-area {
    padding: 0 40rpx 40rpx;
    position: sticky;
    bottom: 0;
    background-color: #f5f5f5;
}

.input-container {
    display: flex;
    background-color: white;
    border-radius: 50rpx;
    padding: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    align-items: flex-end;
}

.input-field {
    flex: 1;
    min-height: 80rpx;
    max-height: 200rpx;
    padding: 20rpx;
    font-size: 28rpx;
    border: none;
    background: transparent;
    resize: none;
}

.send-btn {
    background-color: #667eea;
    color: white;
    padding: 20rpx 32rpx;
    border-radius: 40rpx;
    margin-left: 16rpx;
    font-size: 28rpx;
}

.send-btn.disabled {
    background-color: #ccc;
    color: #999;
}

.action-btn {
    flex: 1;
    padding: 20rpx;
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

.feedback-section {
    padding: 0 40rpx 40rpx;
}

.feedback-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.feedback-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.feedback-content {
    margin-bottom: 32rpx;
}

.feedback-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
}

.feedback-actions {
    display: flex;
    gap: 16rpx;
}

.stats-section {
    padding: 0 40rpx 40rpx;
}

.stats-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.stats-grid {
    display: flex;
    gap: 20rpx;
}

.stat-item {
    flex: 1;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.stat-number {
    font-size: 36rpx;
    font-weight: bold;
    color: #667eea;
    display: block;
    margin-bottom: 8rpx;
}

.stat-label {
    font-size: 24rpx;
    color: #999;
}
</style>