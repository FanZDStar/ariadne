<template>
    <view class="simulation-container">        <view class="header">
            <text class="title">情景模拟训练</text>
            <text class="subtitle">在真实场景中练习人际交往技能</text>
        </view>

        <!-- 场景选择 -->
        <view v-if="currentStage === 'selection'" class="selection-stage">
            <view class="filter-section">
                <text class="filter-title">🎯 选择练习类型</text>
                <view class="filter-tabs">
                    <view v-for="category in scenarioCategories" :key="category.id" class="filter-tab"
                        :class="{ active: selectedCategory === category.id }" @click="selectCategory(category.id)">
                        <text class="tab-icon">{{ category.icon }}</text>
                        <text class="tab-name">{{ category.name }}</text>
                    </view>
                </view>
            </view>

            <view class="difficulty-section">
                <text class="section-title">📊 难度等级</text>
                <view class="difficulty-slider">
                    <view class="difficulty-labels">
                        <text class="difficulty-label">😊 简单</text>
                        <text class="difficulty-label">😐 中等</text>
                        <text class="difficulty-label">😰 困难</text>
                    </view>
                    <slider v-model="selectedDifficulty" min="1" max="3" step="1" show-value activeColor="#667eea"
                        backgroundColor="#f0f0f0" @change="filterScenarios" />
                </view>
            </view>

            <view class="scenarios-section">
                <text class="section-title">🎭 可用场景</text>
                <view v-for="scenario in filteredScenarios" :key="scenario.id" class="scenario-card"
                    @click="selectScenario(scenario)">
                    <view class="scenario-header">
                        <text class="scenario-icon">{{ scenario.icon }}</text>
                        <view class="scenario-info">
                            <text class="scenario-title">{{ scenario.title }}</text>
                            <text class="scenario-desc">{{ scenario.description }}</text>
                        </view>
                        <view class="scenario-meta">
                            <view class="scenario-difficulty" :class="'level-' + scenario.difficulty">
                                <text class="difficulty-text">{{ getDifficultyText(scenario.difficulty) }}</text>
                            </view>
                            <text class="scenario-duration">{{ scenario.duration }}</text>
                        </view>
                    </view>

                    <view class="scenario-details">
                        <view class="scenario-tags">
                            <text v-for="tag in scenario.tags" :key="tag" class="scenario-tag">
                                {{ tag }}
                            </text>
                        </view>
                        <view class="scenario-skills">
                            <text class="skills-label">练习技能：</text>
                            <text class="skills-list">{{ scenario.skills.join('、') }}</text>
                        </view>
                    </view>

                    <view class="scenario-stats">
                        <view class="stat-item">
                            <text class="stat-icon">👥</text>
                            <text class="stat-text">{{ scenario.participants }}人参与</text>
                        </view>
                        <view class="stat-item">
                            <text class="stat-icon">⭐</text>
                            <text class="stat-text">{{ scenario.rating }}分评价</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 场景简介 -->
        <view v-if="currentStage === 'briefing'" class="briefing-stage">
            <view class="briefing-card">
                <view class="briefing-header">
                    <text class="briefing-icon">{{ currentScenario.icon }}</text>
                    <view class="briefing-info">
                        <text class="briefing-title">{{ currentScenario.title }}</text>
                        <text class="briefing-subtitle">场景简介</text>
                    </view>
                </view>

                <view class="briefing-content">
                    <view class="briefing-section">
                        <text class="section-label">📖 背景设定</text>
                        <text class="section-content">{{ currentScenario.background }}</text>
                    </view>

                    <view class="briefing-section">
                        <text class="section-label">🎯 你的角色</text>
                        <text class="section-content">{{ currentScenario.userRole }}</text>
                    </view>

                    <view class="briefing-section">
                        <text class="section-label">🎪 其他角色</text>
                        <view class="characters-list">
                            <view v-for="character in currentScenario.characters" :key="character.id"
                                class="character-item">
                                <text class="character-icon">{{ character.icon }}</text>
                                <view class="character-info">
                                    <text class="character-name">{{ character.name }}</text>
                                    <text class="character-desc">{{ character.description }}</text>
                                </view>
                            </view>
                        </view>
                    </view>

                    <view class="briefing-section">
                        <text class="section-label">🏆 目标任务</text>
                        <view class="objectives-list">
                            <text v-for="objective in currentScenario.objectives" :key="objective"
                                class="objective-item">
                                • {{ objective }}
                            </text>
                        </view>
                    </view>

                    <view class="briefing-section">
                        <text class="section-label">💡 提示建议</text>
                        <view class="tips-list">
                            <text v-for="tip in currentScenario.tips" :key="tip" class="tip-item">
                                💡 {{ tip }}
                            </text>
                        </view>
                    </view>
                </view>

                <view class="briefing-actions">
                    <view class="action-btn secondary" @click="backToSelection">
                        <text class="btn-text">重新选择</text>
                    </view>
                    <view class="action-btn primary" @click="startSimulation">
                        <text class="btn-text">开始模拟</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 模拟进行中 -->
        <view v-if="currentStage === 'simulation'" class="simulation-stage">
            <view class="simulation-header">
                <view class="simulation-progress">
                    <text class="progress-text">{{ currentStep }}/{{ totalSteps }}</text>
                    <view class="progress-bar">
                        <view class="progress-fill" :style="{ width: (currentStep / totalSteps * 100) + '%' }"></view>
                    </view>
                </view>
                <view class="simulation-timer">
                    <text class="timer-icon">⏱️</text>
                    <text class="timer-text">{{ formatTime(elapsedTime) }}</text>
                </view>
            </view>

            <view class="simulation-scene">
                <view class="scene-image">
                    <text class="scene-emoji">{{ currentScenario.sceneEmoji }}</text>
                </view>

                <view class="scene-description">
                    <text class="scene-text">{{ currentSimulationStep.sceneText }}</text>
                </view>

                <view class="characters-display">
                    <view v-for="character in currentSimulationStep.activeCharacters" :key="character.id"
                        class="character-display" :class="{ speaking: character.isSpeaking }">
                        <text class="character-avatar">{{ character.icon }}</text>
                        <text class="character-name">{{ character.name }}</text>
                        <view v-if="character.dialogue" class="character-dialogue">
                            <text class="dialogue-text">{{ character.dialogue }}</text>
                        </view>
                    </view>
                </view>
            </view>

            <view class="response-section">
                <text class="response-title">你的回应</text>
                <view class="response-options">
                    <view v-for="option in currentSimulationStep.options" :key="option.id" class="response-option"
                        @click="selectResponse(option)">
                        <view class="option-header">
                            <text class="option-icon">{{ option.icon }}</text>
                            <text class="option-text">{{ option.text }}</text>
                        </view>
                        <view class="option-meta">
                            <text class="option-type">{{ option.type }}</text>
                            <view class="option-skills">
                                <text v-for="skill in option.skills" :key="skill" class="skill-badge">
                                    {{ skill }}
                                </text>
                            </view>
                        </view>
                    </view>
                </view>
            </view>

            <view class="simulation-controls">
                <view class="control-btn" @click="pauseSimulation">
                    <text class="control-icon">⏸️</text>
                    <text class="control-text">暂停</text>
                </view>
                <view class="control-btn" @click="getHint">
                    <text class="control-icon">💡</text>
                    <text class="control-text">提示</text>
                </view>
                <view class="control-btn" @click="exitSimulation">
                    <text class="control-icon">🚪</text>
                    <text class="control-text">退出</text>
                </view>
            </view>
        </view>

        <!-- 结果分析 -->
        <view v-if="currentStage === 'analysis'" class="analysis-stage">
            <view class="analysis-header">
                <text class="analysis-icon">📊</text>
                <text class="analysis-title">模拟结果分析</text>
                <text class="analysis-subtitle">{{ currentScenario.title }}</text>
            </view>

            <view class="performance-overview">
                <view class="performance-score">
                    <text class="score-number">{{ simulationResult.overallScore }}</text>
                    <text class="score-label">综合得分</text>
                    <view class="score-stars">
                        <text v-for="n in 5" :key="n" class="score-star"
                            :class="{ active: n <= Math.ceil(simulationResult.overallScore / 20) }">⭐</text>
                    </view>
                </view>

                <view class="performance-stats">
                    <view class="stat-item">
                        <text class="stat-value">{{ simulationResult.completionTime }}</text>
                        <text class="stat-label">完成时间</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-value">{{ simulationResult.correctResponses }}/{{
                            simulationResult.totalResponses }}</text>
                        <text class="stat-label">正确回应</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-value">{{ simulationResult.hintsUsed }}</text>
                        <text class="stat-label">使用提示</text>
                    </view>
                </view>
            </view>

            <view class="skills-analysis">
                <text class="analysis-section-title">🎯 技能表现分析</text>
                <view v-for="skill in simulationResult.skillsAnalysis" :key="skill.name" class="skill-analysis-item">
                    <view class="skill-header">
                        <text class="skill-name">{{ skill.name }}</text>
                        <text class="skill-score">{{ skill.score }}分</text>
                    </view>
                    <view class="skill-progress">
                        <view class="skill-progress-fill" :style="{ width: skill.score + '%' }"></view>
                    </view>
                    <text class="skill-feedback">{{ skill.feedback }}</text>
                </view>
            </view>

            <view class="detailed-feedback">
                <text class="analysis-section-title">💬 详细反馈</text>
                <view v-for="feedback in simulationResult.detailedFeedback" :key="feedback.step" class="feedback-item">
                    <view class="feedback-header">
                        <text class="feedback-step">第{{ feedback.step }}步</text>
                        <view class="feedback-rating" :class="feedback.rating">
                            <text class="rating-text">{{ getRatingText(feedback.rating) }}</text>
                        </view>
                    </view>
                    <text class="feedback-situation">情况：{{ feedback.situation }}</text>
                    <text class="feedback-response">你的回应：{{ feedback.yourResponse }}</text>
                    <text class="feedback-comment">评价：{{ feedback.comment }}</text>
                    <view v-if="feedback.betterResponse" class="feedback-suggestion">
                        <text class="suggestion-label">更好的回应：</text>
                        <text class="suggestion-text">{{ feedback.betterResponse }}</text>
                    </view>
                </view>
            </view>

            <view class="improvement-suggestions">
                <text class="analysis-section-title">📈 改进建议</text>
                <view v-for="suggestion in simulationResult.improvements" :key="suggestion.area"
                    class="improvement-item">
                    <text class="improvement-area">{{ suggestion.area }}</text>
                    <text class="improvement-desc">{{ suggestion.description }}</text>
                    <view class="improvement-actions">
                        <text v-for="action in suggestion.actions" :key="action" class="improvement-action">
                            • {{ action }}
                        </text>
                    </view>
                </view>
            </view>

            <view class="analysis-actions">
                <view class="action-btn secondary" @click="retryScenario">
                    <text class="btn-text">重新练习</text>
                </view>
                <view class="action-btn tertiary" @click="shareResult">
                    <text class="btn-text">分享结果</text>
                </view>
                <view class="action-btn primary" @click="backToSelection">
                    <text class="btn-text">选择新场景</text>
                </view>
            </view>
        </view>

        <!-- 暂停弹窗 -->
        <view v-if="showPauseModal" class="pause-modal">
            <view class="modal-content">
                <text class="modal-title">⏸️ 模拟已暂停</text>
                <text class="modal-desc">你可以选择继续、重新开始或退出模拟</text>
                <view class="modal-actions">
                    <view class="modal-btn secondary" @click="resumeSimulation">
                        <text class="btn-text">继续</text>
                    </view>
                    <view class="modal-btn tertiary" @click="restartSimulation">
                        <text class="btn-text">重新开始</text>
                    </view>
                    <view class="modal-btn primary" @click="confirmExit">
                        <text class="btn-text">退出</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            currentStage: 'selection', // selection, briefing, simulation, analysis
            selectedCategory: 'social',
            selectedDifficulty: 2,
            currentScenario: null,
            currentStep: 0,
            totalSteps: 0,
            elapsedTime: 0,
            timer: null,
            showPauseModal: false,
            simulationResult: {},
            scenarioCategories: [
                { id: 'social', name: '社交聚会', icon: '🎉' },
                { id: 'workplace', name: '职场交往', icon: '💼' },
                { id: 'romantic', name: '恋爱交往', icon: '💕' },
                { id: 'family', name: '家庭关系', icon: '👨‍👩‍👧‍👦' },
                { id: 'conflict', name: '冲突处理', icon: '⚖️' },
                { id: 'daily', name: '日常交流', icon: '💬' }
            ],
            scenarios: [
                {
                    id: 1,
                    category: 'social',
                    title: '初次聚会自我介绍',
                    description: '在朋友聚会上向陌生人介绍自己',
                    icon: '👥',
                    difficulty: 1,
                    duration: '10-15分钟',
                    tags: ['自我介绍', '社交技巧', '第一印象'],
                    skills: ['表达能力', '自信建立', '倾听技巧'],
                    participants: 156,
                    rating: 4.5,
                    sceneEmoji: '🎉',
                    background: '你被朋友邀请参加一个聚会，现场有很多你不认识的人。朋友正在忙，你需要主动与其他人交流。',
                    userRole: '聚会新人，希望融入群体，结识新朋友',
                    characters: [
                        {
                            id: 1,
                            name: '小李',
                            icon: '👨',
                            description: '热情开朗的主人，喜欢介绍朋友认识'
                        },
                        {
                            id: 2,
                            name: '小王',
                            icon: '👩',
                            description: '有点内向，但很友善的参与者'
                        }
                    ],
                    objectives: [
                        '成功向至少2个人介绍自己',
                        '了解其他人的基本信息',
                        '建立良好的第一印象',
                        '自然地融入对话'
                    ],
                    tips: [
                        '保持微笑和眼神接触',
                        '准备一个简短有趣的自我介绍',
                        '主动询问对方的情况',
                        '找到共同话题'
                    ]
                },
                {
                    id: 2,
                    category: 'workplace',
                    title: '与同事处理工作分歧',
                    description: '在团队项目中与同事意见不合',
                    icon: '💼',
                    difficulty: 2,
                    duration: '15-20分钟',
                    tags: ['冲突解决', '团队合作', '沟通技巧'],
                    skills: ['协商能力', '情绪管理', '问题解决'],
                    participants: 89,
                    rating: 4.2,
                    sceneEmoji: '🏢',
                    background: '你和同事小张对项目的实施方案有不同看法，需要在截止日期前达成一致。',
                    userRole: '项目组成员，希望推进自己的方案但也要维护团队和谐',
                    characters: [
                        {
                            id: 1,
                            name: '小张',
                            icon: '👔',
                            description: '经验丰富但有点固执的同事'
                        },
                        {
                            id: 2,
                            name: '经理',
                            icon: '👨‍💼',
                            description: '希望看到团队和谐高效工作的部门经理'
                        }
                    ],
                    objectives: [
                        '清楚地表达自己的观点',
                        '理解同事的立场',
                        '找到双方都能接受的解决方案',
                        '维护良好的工作关系'
                    ],
                    tips: [
                        '先倾听对方的完整观点',
                        '用事实和数据支持自己的立场',
                        '寻找共同目标',
                        '保持专业和尊重的态度'
                    ]
                },
                {
                    id: 3,
                    category: 'romantic',
                    title: '第一次约会交流',
                    description: '与心仪对象的首次约会对话',
                    icon: '💕',
                    difficulty: 2,
                    duration: '20-25分钟',
                    tags: ['约会技巧', '情感表达', '深度交流'],
                    skills: ['情感表达', '倾听技巧', '幽默感'],
                    participants: 234,
                    rating: 4.7,
                    sceneEmoji: '☕',
                    background: '你和在交友软件上认识的对象约在咖啡厅见面，这是你们第一次线下见面。',
                    userRole: '希望给对方留下好印象，了解彼此是否合适',
                    characters: [
                        {
                            id: 1,
                            name: 'Alex',
                            icon: '😊',
                            description: '你的约会对象，有点紧张但很期待这次见面'
                        }
                    ],
                    objectives: [
                        '创造轻松愉快的氛围',
                        '了解对方的兴趣爱好',
                        '分享自己的真实想法',
                        '判断彼此的匹配度'
                    ],
                    tips: [
                        '保持自然不要过度紧张',
                        '问开放性问题了解对方',
                        '分享有趣的个人经历',
                        '注意观察对方的反应'
                    ]
                }
            ],
            currentSimulationStep: {},
            simulationSteps: []
        }
    },

    computed: {
        filteredScenarios() {
            return this.scenarios.filter(scenario =>
                scenario.category === this.selectedCategory &&
                scenario.difficulty === this.selectedDifficulty
            );
        }
    },

    onLoad(options) {
        if (options.category) {
            this.selectedCategory = options.category;
        }
        if (options.difficulty) {
            this.selectedDifficulty = parseInt(options.difficulty);
        }
        this.filterScenarios();
    },

    onUnload() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    },

    methods: {
        selectCategory(categoryId) {
            this.selectedCategory = categoryId;
            this.filterScenarios();
        },

        filterScenarios() {
            // 过滤场景逻辑已在computed中实现
        },

        selectScenario(scenario) {
            this.currentScenario = scenario;
            this.currentStage = 'briefing';
        },

        backToSelection() {
            this.currentStage = 'selection';
            this.currentScenario = null;
        },

        startSimulation() {
            this.currentStage = 'simulation';
            this.currentStep = 1;
            this.totalSteps = 5; // 示例步骤数
            this.elapsedTime = 0;
            this.initializeSimulation();
            this.startTimer();
        },

        initializeSimulation() {
            // 初始化模拟步骤
            this.simulationSteps = this.generateSimulationSteps();
            this.currentSimulationStep = this.simulationSteps[0];
        },

        generateSimulationSteps() {
            // 根据选择的场景生成具体的模拟步骤
            return [
                {
                    id: 1,
                    sceneText: '你走进聚会现场，看到几个人在聊天...',
                    activeCharacters: [
                        {
                            id: 1,
                            name: '小李',
                            icon: '👨',
                            isSpeaking: true,
                            dialogue: '嗨，你好！我是小李，欢迎来到聚会！'
                        }
                    ],
                    options: [
                        {
                            id: 1,
                            icon: '😊',
                            text: '你好小李！我是[你的名字]，很高兴认识你！',
                            type: '友好回应',
                            skills: ['礼貌表达', '自我介绍']
                        },
                        {
                            id: 2,
                            icon: '😅',
                            text: '嗯...你好，我是朋友叫来的...',
                            type: '被动回应',
                            skills: ['基础交流']
                        },
                        {
                            id: 3,
                            icon: '🤝',
                            text: '你好！感谢邀请，这个聚会看起来很棒！',
                            type: '积极回应',
                            skills: ['社交技巧', '赞美表达']
                        }
                    ]
                }
            ];
        },

        selectResponse(option) {
            // 处理用户选择的回应
            this.processResponse(option);
            this.nextStep();
        },

        processResponse(option) {
            // 记录用户的选择和评分
            console.log('用户选择:', option);
        },

        nextStep() {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.currentSimulationStep = this.simulationSteps[this.currentStep - 1] || {};
            } else {
                this.finishSimulation();
            }
        },

        startTimer() {
            this.timer = setInterval(() => {
                this.elapsedTime++;
            }, 1000);
        },

        pauseSimulation() {
            this.showPauseModal = true;
            if (this.timer) {
                clearInterval(this.timer);
            }
        },

        resumeSimulation() {
            this.showPauseModal = false;
            this.startTimer();
        },

        restartSimulation() {
            this.showPauseModal = false;
            this.startSimulation();
        },

        exitSimulation() {
            this.showPauseModal = false;
            this.confirmExit();
        },

        confirmExit() {
            uni.showModal({
                title: '确认退出',
                content: '退出后当前进度将不会保存，确定要退出吗？',
                success: (res) => {
                    if (res.confirm) {
                        this.backToSelection();
                        if (this.timer) {
                            clearInterval(this.timer);
                        }
                    }
                }
            });
        },

        getHint() {
            uni.showModal({
                title: '💡 提示',
                content: '在这种情况下，建议保持微笑，主动倾听对方说话，然后给出真诚的回应。',
                showCancel: false,
                confirmText: '知道了'
            });
        },

        finishSimulation() {
            if (this.timer) {
                clearInterval(this.timer);
            }
            this.generateResult();
            this.currentStage = 'analysis';
        },

        generateResult() {
            // 生成模拟结果
            this.simulationResult = {
                overallScore: 85,
                completionTime: this.formatTime(this.elapsedTime),
                correctResponses: 4,
                totalResponses: 5,
                hintsUsed: 1,
                skillsAnalysis: [
                    {
                        name: '表达能力',
                        score: 90,
                        feedback: '你的表达清晰且有条理，善于传达自己的想法。'
                    },
                    {
                        name: '倾听技巧',
                        score: 80,
                        feedback: '能够认真倾听他人，但可以更多地给予回应和反馈。'
                    }
                ],
                detailedFeedback: [
                    {
                        step: 1,
                        situation: '初次见面打招呼',
                        yourResponse: '你好小李！我是[你的名字]，很高兴认识你！',
                        rating: 'excellent',
                        comment: '回应友好自然，展现了良好的社交礼仪。'
                    }
                ],
                improvements: [
                    {
                        area: '非语言沟通',
                        description: '注意肢体语言和面部表情的配合',
                        actions: ['保持适当的眼神接触', '使用开放性的肢体姿态']
                    }
                ]
            };
        },

        retryScenario() {
            this.startSimulation();
        },

        shareResult() {
            uni.showToast({
                title: '分享功能开发中',
                icon: 'none'
            });
        },

        getDifficultyText(difficulty) {
            const difficultyMap = {
                1: '简单',
                2: '中等',
                3: '困难'
            };
            return difficultyMap[difficulty] || '未知';
        },

        getRatingText(rating) {
            const ratingMap = {
                'excellent': '优秀',
                'good': '良好',
                'average': '一般',
                'poor': '需改进'
            };
            return ratingMap[rating] || '未知';
        },

        formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
        }
    }
}
</script>

<style scoped>
.simulation-container {
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

/* 场景选择阶段 */
.selection-stage {
    padding: 40rpx;
}

.filter-section {
    margin-bottom: 40rpx;
}

.filter-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.filter-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
}

.filter-tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24rpx 20rpx;
    background-color: white;
    border: 2rpx solid #e0e0e0;
    border-radius: 16rpx;
    min-width: 140rpx;
    transition: all 0.3s ease;
}

.filter-tab.active {
    border-color: #667eea;
    background-color: #f0f4ff;
}

.tab-icon {
    font-size: 32rpx;
    margin-bottom: 8rpx;
}

.tab-name {
    font-size: 24rpx;
    color: #333;
    text-align: center;
}

.difficulty-section {
    margin-bottom: 40rpx;
}

.section-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.difficulty-slider {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.difficulty-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20rpx;
}

.difficulty-label {
    font-size: 24rpx;
    color: #666;
}

.scenarios-section {
    margin-bottom: 40rpx;
}

.scenario-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.scenario-card:active {
    transform: translateY(2rpx);
}

.scenario-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20rpx;
}

.scenario-icon {
    font-size: 40rpx;
    margin-right: 20rpx;
}

.scenario-info {
    flex: 1;
}

.scenario-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.scenario-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
}

.scenario-meta {
    text-align: right;
}

.scenario-difficulty {
    margin-bottom: 8rpx;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
}

.scenario-difficulty.level-1 {
    background-color: #f6ffed;
    color: #52c41a;
}

.scenario-difficulty.level-2 {
    background-color: #fff7e6;
    color: #fa8c16;
}

.scenario-difficulty.level-3 {
    background-color: #fff2f0;
    color: #ff4d4f;
}

.scenario-duration {
    font-size: 22rpx;
    color: #999;
}

.scenario-details {
    margin-bottom: 20rpx;
}

.scenario-tags {
    display: flex;
    gap: 8rpx;
    flex-wrap: wrap;
    margin-bottom: 16rpx;
}

.scenario-tag {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
}

.scenario-skills {
    margin-bottom: 16rpx;
}

.skills-label {
    font-size: 24rpx;
    color: #333;
    font-weight: bold;
}

.skills-list {
    font-size: 24rpx;
    color: #666;
}

.scenario-stats {
    display: flex;
    justify-content: space-between;
    padding-top: 16rpx;
    border-top: 1rpx solid #f0f0f0;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
}

.stat-icon {
    font-size: 20rpx;
}

.stat-text {
    font-size: 22rpx;
    color: #666;
}

/* 场景简介阶段 */
.briefing-stage {
    padding: 40rpx;
}

.briefing-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.briefing-header {
    display: flex;
    align-items: center;
    margin-bottom: 32rpx;
    padding-bottom: 20rpx;
    border-bottom: 2rpx solid #f0f0f0;
}

.briefing-icon {
    font-size: 48rpx;
    margin-right: 20rpx;
}

.briefing-info {
    flex: 1;
}

.briefing-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.briefing-subtitle {
    font-size: 24rpx;
    color: #667eea;
}

.briefing-content {
    margin-bottom: 40rpx;
}

.briefing-section {
    margin-bottom: 32rpx;
}

.section-label {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.section-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
}

.characters-list {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}

.character-item {
    display: flex;
    align-items: center;
    padding: 20rpx;
    background-color: #f8f9fa;
    border-radius: 12rpx;
}

.character-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.character-info {
    flex: 1;
}

.character-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 4rpx;
    display: block;
}

.character-desc {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
}

.objectives-list,
.tips-list {
    display: flex;
    flex-direction: column;
    gap: 12rpx;
}

.objective-item,
.tip-item {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
}

.briefing-actions {
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
    transition: all 0.3s ease;
}

.action-btn.primary {
    background-color: #667eea;
    color: white;
}

.action-btn.secondary {
    background-color: #f0f0f0;
    color: #666;
}

.action-btn.tertiary {
    background-color: #fff7e6;
    color: #fa8c16;
}

.action-btn:active {
    transform: scale(0.98);
}

/* 模拟进行阶段 */
.simulation-stage {
    padding: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.simulation-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40rpx;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.simulation-progress {
    flex: 1;
}

.progress-text {
    font-size: 24rpx;
    margin-bottom: 12rpx;
    display: block;
}

.progress-bar {
    height: 8rpx;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4rpx;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background-color: white;
    border-radius: 4rpx;
    transition: width 0.3s ease;
}

.simulation-timer {
    display: flex;
    align-items: center;
    gap: 8rpx;
}

.timer-icon {
    font-size: 24rpx;
}

.timer-text {
    font-size: 24rpx;
    font-weight: bold;
}

.simulation-scene {
    flex: 1;
    padding: 40rpx;
    background-color: white;
}

.scene-image {
    text-align: center;
    margin-bottom: 32rpx;
}

.scene-emoji {
    font-size: 120rpx;
}

.scene-description {
    background-color: #f8f9fa;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
}

.scene-text {
    font-size: 28rpx;
    color: #333;
    line-height: 1.6;
    text-align: center;
}

.characters-display {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
    margin-bottom: 32rpx;
}

.character-display {
    display: flex;
    align-items: flex-start;
    padding: 24rpx;
    background-color: #f0f4ff;
    border-radius: 16rpx;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.character-display.speaking {
    border-color: #667eea;
    box-shadow: 0 4rpx 12rpx rgba(102, 126, 234, 0.2);
}

.character-avatar {
    font-size: 40rpx;
    margin-right: 16rpx;
}

.character-name {
    font-size: 24rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.character-dialogue {
    background-color: white;
    border-radius: 12rpx;
    padding: 16rpx 20rpx;
    margin-top: 8rpx;
    position: relative;
}

.character-dialogue::before {
    content: '';
    position: absolute;
    top: -8rpx;
    left: 20rpx;
    width: 0;
    height: 0;
    border-left: 8rpx solid transparent;
    border-right: 8rpx solid transparent;
    border-bottom: 8rpx solid white;
}

.dialogue-text {
    font-size: 26rpx;
    color: #333;
    line-height: 1.5;
}

.response-section {
    background-color: white;
    border-top: 1rpx solid #f0f0f0;
    padding: 32rpx;
}

.response-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.response-options {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}

.response-option {
    background-color: #f8f9fa;
    border: 2rpx solid #e0e0e0;
    border-radius: 16rpx;
    padding: 24rpx;
    transition: all 0.3s ease;
}

.response-option:active {
    border-color: #667eea;
    background-color: #f0f4ff;
    transform: scale(0.98);
}

.option-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 16rpx;
}

.option-icon {
    font-size: 28rpx;
    margin-right: 12rpx;
}

.option-text {
    flex: 1;
    font-size: 26rpx;
    color: #333;
    line-height: 1.5;
}

.option-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.option-type {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.option-skills {
    display: flex;
    gap: 8rpx;
    flex-wrap: wrap;
}

.skill-badge {
    font-size: 20rpx;
    color: #52c41a;
    background-color: #f6ffed;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
}

.simulation-controls {
    background-color: white;
    border-top: 1rpx solid #f0f0f0;
    padding: 20rpx 40rpx;
    display: flex;
    justify-content: space-around;
}

.control-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16rpx;
    min-width: 120rpx;
    transition: all 0.3s ease;
}

.control-btn:active {
    transform: scale(0.95);
}

.control-icon {
    font-size: 32rpx;
    margin-bottom: 8rpx;
}

.control-text {
    font-size: 22rpx;
    color: #666;
}

/* 结果分析阶段 */
.analysis-stage {
    padding: 40rpx;
}

.analysis-header {
    text-align: center;
    margin-bottom: 40rpx;
}

.analysis-icon {
    font-size: 80rpx;
    margin-bottom: 16rpx;
    display: block;
}

.analysis-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.analysis-subtitle {
    font-size: 26rpx;
    color: #666;
}

.performance-overview {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.performance-score {
    text-align: center;
    margin-bottom: 32rpx;
    padding-bottom: 24rpx;
    border-bottom: 1rpx solid #f0f0f0;
}

.score-number {
    font-size: 80rpx;
    font-weight: bold;
    color: #52c41a;
    display: block;
    margin-bottom: 8rpx;
}

.score-label {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.score-stars {
    display: flex;
    justify-content: center;
    gap: 8rpx;
}

.score-star {
    font-size: 32rpx;
    color: #ddd;
}

.score-star.active {
    color: #ffd700;
}

.performance-stats {
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.stat-label {
    font-size: 24rpx;
    color: #666;
}

.skills-analysis {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.analysis-section-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.skill-analysis-item {
    margin-bottom: 24rpx;
    padding-bottom: 20rpx;
    border-bottom: 1rpx solid #f0f0f0;
}

.skill-analysis-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12rpx;
}

.skill-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
}

.skill-score {
    font-size: 24rpx;
    font-weight: bold;
    color: #667eea;
}

.skill-progress {
    height: 8rpx;
    background-color: #f0f0f0;
    border-radius: 4rpx;
    overflow: hidden;
    margin-bottom: 12rpx;
}

.skill-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 4rpx;
    transition: width 0.3s ease;
}

.skill-feedback {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
}

.detailed-feedback {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.feedback-item {
    margin-bottom: 24rpx;
    padding-bottom: 20rpx;
    border-bottom: 1rpx solid #f0f0f0;
}

.feedback-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.feedback-step {
    font-size: 24rpx;
    font-weight: bold;
    color: #333;
}

.feedback-rating {
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
}

.feedback-rating.excellent {
    background-color: #f6ffed;
    color: #52c41a;
}

.feedback-rating.good {
    background-color: #e6f7ff;
    color: #1890ff;
}

.feedback-rating.average {
    background-color: #fff7e6;
    color: #fa8c16;
}

.feedback-rating.poor {
    background-color: #fff2f0;
    color: #ff4d4f;
}

.feedback-situation,
.feedback-response,
.feedback-comment {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 8rpx;
    display: block;
}

.feedback-suggestion {
    background-color: #f0f4ff;
    border-radius: 12rpx;
    padding: 16rpx;
    margin-top: 12rpx;
}

.suggestion-label {
    font-size: 22rpx;
    font-weight: bold;
    color: #667eea;
    margin-bottom: 8rpx;
    display: block;
}

.suggestion-text {
    font-size: 24rpx;
    color: #333;
    line-height: 1.5;
}

.improvement-suggestions {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.improvement-item {
    margin-bottom: 24rpx;
    padding-bottom: 20rpx;
    border-bottom: 1rpx solid #f0f0f0;
}

.improvement-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.improvement-area {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.improvement-desc {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 12rpx;
}

.improvement-actions {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
}

.improvement-action {
    font-size: 24rpx;
    color: #666;
    line-height: 1.5;
}

.analysis-actions {
    display: flex;
    gap: 16rpx;
}

.analysis-actions .action-btn {
    flex: 1;
}

/* 暂停弹窗 */
.pause-modal {
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

.modal-content {
    background-color: white;
    border-radius: 20rpx;
    padding: 60rpx 40rpx;
    max-width: 600rpx;
    margin: 0 40rpx;
    text-align: center;
}

.modal-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.modal-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 40rpx;
}

.modal-actions {
    display: flex;
    gap: 16rpx;
}

.modal-btn {
    flex: 1;
    padding: 24rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 26rpx;
    font-weight: bold;
}

.btn-text {
    color: inherit;
}

/* 动画效果 */
.scenario-card {
    animation: fadeInUp 0.5s ease-out;
}

.briefing-card {
    animation: slideInDown 0.6s ease-out;
}

.character-display {
    animation: slideInLeft 0.5s ease-out;
}

.response-option {
    animation: slideInRight 0.5s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translateY(-30rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .filter-tabs {
        justify-content: center;
    }

    .filter-tab {
        min-width: 120rpx;
    }

    .briefing-actions,
    .analysis-actions {
        flex-direction: column;
    }

    .performance-stats {
        flex-direction: column;
        gap: 20rpx;
    }

    .modal-actions {
        flex-direction: column;
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
.filter-tab:focus,
.scenario-card:focus,
.action-btn:focus,
.response-option:focus {
    outline: 2rpx solid #667eea;
    outline-offset: 2rpx;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {

    .scenario-card,
    .briefing-card {
        border: 1rpx solid #333;
    }
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* 底部安全间距 */
.simulation-container {
    padding-bottom: env(safe-area-inset-bottom);
}
</style>