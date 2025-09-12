<!-- <template>
    <view class="categories-container">
        <view class="header">
            <text class="title">技能分类</text>
            <text class="subtitle">系统化学习人际交往技能</text>
        </view>

        <view class="progress-overview">
            <view class="progress-card">
                <view class="progress-header">
                    <text class="progress-title">📈 学习进度</text>
                    <text class="progress-percentage">{{ overallProgress }}%</text>
                </view>
                <view class="progress-bar">
                    <view class="progress-fill" :style="{ width: overallProgress + '%' }"></view>
                </view>
                <view class="progress-stats">
                    <view class="stat-item">
                        <text class="stat-number">{{ completedSkills }}</text>
                        <text class="stat-label">已掌握</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ totalSkills }}</text>
                        <text class="stat-label">总技能</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ studyDays }}</text>
                        <text class="stat-label">学习天数</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="recommended-section">
            <text class="section-title">🎯 为你推荐</text>
            <view class="recommended-skill" @click="startRecommendedSkill">
                <view class="recommended-content">
                    <text class="recommended-icon">⭐</text>
                    <view class="recommended-info">
                        <text class="recommended-name">{{ recommendedSkill.name }}</text>
                        <text class="recommended-reason">{{ recommendedSkill.reason }}</text>
                        <view class="recommended-tags">
                            <text v-for="tag in recommendedSkill.tags" :key="tag" class="skill-tag">
                                {{ tag }}
                            </text>
                        </view>
                    </view>
                </view>
                <view class="recommended-action">
                    <text class="action-text">开始学习</text>
                    <text class="action-arrow">→</text>
                </view>
            </view>
        </view>

        <view class="categories-section">
            <text class="section-title">📚 技能分类</text>
            <view v-for="category in skillCategories" :key="category.id" class="category-card"
                @click="enterCategory(category)">
                <view class="category-header">
                    <text class="category-icon">{{ category.icon }}</text>
                    <view class="category-info">
                        <text class="category-name">{{ category.name }}</text>
                        <text class="category-desc">{{ category.description }}</text>
                    </view>
                    <view class="category-stats">
                        <text class="category-progress">{{ category.progress }}%</text>
                        <text class="category-count">{{ category.completedCount }}/{{ category.totalCount }}</text>
                    </view>
                </view>
                
                <view class="category-progress-bar">
                    <view class="category-progress-fill" 
                        :style="{ width: category.progress + '%' }"></view>
                </view>
                
                <view class="category-skills">
                    <text class="skills-preview">
                        技能预览：{{ category.skills.slice(0, 3).join('、') }}
                        <text v-if="category.skills.length > 3">等{{ category.skills.length }}项</text>
                    </text>
                </view>
                
                <view class="category-difficulty">
                    <text class="difficulty-label">难度：</text>
                    <view class="difficulty-stars">
                        <text v-for="n in 5" :key="n" class="star"
                            :class="{ active: n <= category.difficulty }">⭐</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="path-section">
            <text class="section-title">🛤️ 推荐学习路径</text>
            <view v-for="path in learningPaths" :key="path.id" class="path-card"
                @click="followLearningPath(path)">
                <view class="path-header">
                    <text class="path-icon">{{ path.icon }}</text>
                    <view class="path-info">
                        <text class="path-name">{{ path.name }}</text>
                        <text class="path-desc">{{ path.description }}</text>
                    </view>
                    <view class="path-status" :class="path.status">
                        <text class="status-text">{{ getPathStatusText(path.status) }}</text>
                    </view>
                </view>
                
                <view class="path-timeline">
                    <view v-for="(step, index) in path.steps" :key="index" class="timeline-step"
                        :class="{ completed: step.completed, current: step.current }">
                        <view class="step-dot"></view>
                        <text class="step-title">{{ step.title }}</text>
                        <text class="step-duration">{{ step.duration }}</text>
                    </view>
                </view>
                
                <view class="path-footer">
                    <text class="path-duration">预计 {{ path.totalDuration }}</text>
                    <text class="path-level">{{ path.level }}</text>
                </view>
            </view>
        </view>

        <view class="quick-practice">
            <text class="section-title">⚡ 快速练习</text>
            <view class="practice-grid">
                <view v-for="practice in quickPractices" :key="practice.id" class="practice-item"
                    @click="startQuickPractice(practice)">
                    <text class="practice-icon">{{ practice.icon }}</text>
                    <text class="practice-name">{{ practice.name }}</text>
                    <text class="practice-time">{{ practice.duration }}</text>
                </view>
            </view>
        </view>

        <view class="achievements-section">
            <view class="achievements-header">
                <text class="section-title">🏆 学习成就</text>
                <text class="view-all" @click="viewAllAchievements">查看全部</text>
            </view>
            <scroll-view class="achievements-scroll" scroll-x="true" show-scrollbar="false">
                <view class="achievements-list">
                    <view v-for="achievement in recentAchievements" :key="achievement.id" class="achievement-item"
                        :class="{ unlocked: achievement.unlocked }">
                        <text class="achievement-icon">{{ achievement.icon }}</text>
                        <text class="achievement-name">{{ achievement.name }}</text>
                        <text class="achievement-desc">{{ achievement.description }}</text>
                        <view v-if="!achievement.unlocked" class="achievement-progress">
                            <text class="progress-text">{{ achievement.current }}/{{ achievement.target }}</text>
                        </view>
                    </view>
                </view>
            </scroll-view>
        </view>

        <view class="floating-actions">
            <view class="fab-item" @click="openLearningAssistant">
                <text class="fab-icon">🤖</text>
                <text class="fab-label">学习助手</text>
            </view>
        </view>
    </view>
</template> -->

<template>
    <view class="categories-container">
        <view class="header">
            <text class="title">技能分类</text>
            <text class="subtitle">系统化学习人际交往技能</text>
        </view>

        <!-- 学习进度概览 -->
        <view class="progress-overview">
            <view class="progress-card">
                <view class="progress-header">
                    <text class="progress-title">📈 学习进度</text>
                    <text class="progress-percentage">{{ overallProgress }}%</text>
                </view>
                <view class="progress-bar">
                    <view class="progress-fill" :style="{ width: overallProgress + '%' }"></view>
                </view>
                <view class="progress-stats">
                    <view class="stat-item">
                        <text class="stat-number">{{ completedSkills }}</text>
                        <text class="stat-label">已掌握</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ totalSkills }}</text>
                        <text class="stat-label">总技能</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-number">{{ studyDays }}</text>
                        <text class="stat-label">学习天数</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 推荐学习 -->
        <view class="recommended-section">
            <text class="section-title">🎯 为你推荐</text>
            <view class="recommended-skill" @click="startRecommendedSkill">
                <view class="recommended-content">
                    <text class="recommended-icon">⭐</text>
                    <view class="recommended-info">
                        <text class="recommended-name">{{ recommendedSkill.name }}</text>
                        <text class="recommended-reason">{{ recommendedSkill.reason }}</text>
                        <view class="recommended-tags">
                            <text v-for="tag in recommendedSkill.tags" :key="tag" class="skill-tag">
                                {{ tag }}
                            </text>
                        </view>
                    </view>
                </view>
                <view class="recommended-action">
                    <text class="action-text">开始学习</text>
                    <text class="action-arrow">→</text>
                </view>
            </view>
        </view>

        <!-- 技能分类 -->
        <view class="categories-section">
            <text class="section-title">📚 技能分类</text>
            <view class="categories-grid">
                <view v-for="category in skillCategories" :key="category.id" class="category-card"
                    @click="enterCategory(category)">
                    <view class="category-header">
                        <text class="category-icon">{{ category.icon }}</text>
                        <view class="category-info">
                            <text class="category-name">{{ category.name }}</text>
                            <text class="category-desc">{{ category.description }}</text>
                        </view>
                    </view>

                    <view class="category-stats">
                        <text class="category-progress">{{ category.progress }}%</text>
                        <text class="category-count">{{ category.completedCount }}/{{ category.totalCount }}</text>
                    </view>

                    <view class="category-progress-bar">
                        <view class="category-progress-fill" :style="{ width: category.progress + '%' }"></view>
                    </view>

                    <view class="category-skills">
                        <text class="skills-preview">
                            {{ category.skills.slice(0, 2).join('、') }}
                            <text v-if="category.skills.length > 2">等{{ category.skills.length }}项</text>
                        </text>
                    </view>

                    <view class="category-difficulty">
                        <text class="difficulty-label">难度：</text>
                        <view class="difficulty-stars">
                            <text v-for="n in 5" :key="n" class="star"
                                :class="{ active: n <= category.difficulty }">⭐</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 学习路径 -->
        <view class="path-section">
            <text class="section-title">🛤️ 推荐学习路径</text>
            <view v-for="path in learningPaths" :key="path.id" class="path-card" @click="followLearningPath(path)">
                <view class="path-header">
                    <text class="path-icon">{{ path.icon }}</text>
                    <view class="path-info">
                        <text class="path-name">{{ path.name }}</text>
                        <text class="path-desc">{{ path.description }}</text>
                    </view>
                    <view class="path-status" :class="path.status">
                        <text class="status-text">{{ getPathStatusText(path.status) }}</text>
                    </view>
                </view>

                <view class="path-timeline">
                    <view v-for="(step, index) in path.steps" :key="index" class="timeline-step"
                        :class="{ completed: step.completed, current: step.current }">
                        <view class="step-dot"></view>
                        <text class="step-title">{{ step.title }}</text>
                        <text class="step-duration">{{ step.duration }}</text>
                    </view>
                </view>

                <view class="path-footer">
                    <text class="path-duration">预计 {{ path.totalDuration }}</text>
                    <text class="path-level">{{ path.level }}</text>
                </view>
            </view>
        </view>

        <!-- 快速练习 -->
        <view class="quick-practice">
            <text class="section-title">⚡ 快速练习</text>
            <view class="practice-grid">
                <view v-for="practice in quickPractices" :key="practice.id" class="practice-item"
                    @click="startQuickPractice(practice)">
                    <text class="practice-icon">{{ practice.icon }}</text>
                    <text class="practice-name">{{ practice.name }}</text>
                    <text class="practice-time">{{ practice.duration }}</text>
                </view>
            </view>
        </view>

        <!-- 学习成就 -->
        <view class="achievements-section">
            <view class="achievements-header">
                <text class="section-title">🏆 学习成就</text>
                <text class="view-all" @click="viewAllAchievements">查看全部</text>
            </view>
            <scroll-view class="achievements-scroll" scroll-x="true" show-scrollbar="false">
                <view class="achievements-list">
                    <view v-for="achievement in recentAchievements" :key="achievement.id" class="achievement-item"
                        :class="{ unlocked: achievement.unlocked }">
                        <text class="achievement-icon">{{ achievement.icon }}</text>
                        <text class="achievement-name">{{ achievement.name }}</text>
                        <text class="achievement-desc">{{ achievement.description }}</text>
                        <view v-if="!achievement.unlocked" class="achievement-progress">
                            <text class="progress-text">{{ achievement.current }}/{{ achievement.target }}</text>
                        </view>
                    </view>
                </view>
            </scroll-view>
        </view>

        <!-- 浮动按钮 -->
        <view class="floating-actions">
            <view class="fab-item" @click="openLearningAssistant">
                <text class="fab-icon">🤖</text>
                <text class="fab-label">学习助手</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            overallProgress: 42,
            completedSkills: 15,
            totalSkills: 36,
            studyDays: 12,
            recommendedSkill: {
                name: '主动倾听技巧',
                reason: '基于你的学习记录，建议重点提升倾听能力',
                tags: ['基础技能', '实用性强', '适合初学者']
            },
            skillCategories: [
                {
                    id: 1,
                    name: '沟通基础',
                    icon: '💬',
                    description: '学习有效沟通的基本原则和技巧',
                    progress: 65,
                    completedCount: 8,
                    totalCount: 12,
                    difficulty: 2,
                    skills: ['主动倾听', '表达技巧', '非言语沟通', '反馈技巧', '询问技巧']
                },
                {
                    id: 2,
                    name: '情感表达',
                    icon: '❤️',
                    description: '学会准确表达和理解情感',
                    progress: 30,
                    completedCount: 3,
                    totalCount: 10,
                    difficulty: 3,
                    skills: ['情感识别', '情绪调节', '共情能力', '情感表达', '情感支持']
                },
                {
                    id: 3,
                    name: '冲突处理',
                    icon: '⚖️',
                    description: '掌握化解矛盾和处理冲突的方法',
                    progress: 15,
                    completedCount: 2,
                    totalCount: 8,
                    difficulty: 4,
                    skills: ['冲突识别', '协商技巧', '妥协艺术', '和解方法']
                },
                {
                    id: 4,
                    name: '社交礼仪',
                    icon: '🤝',
                    description: '了解和掌握各种社交场合的礼仪规范',
                    progress: 80,
                    completedCount: 4,
                    totalCount: 5,
                    difficulty: 1,
                    skills: ['见面礼仪', '餐桌礼仪', '职场礼仪', '网络礼仪', '约会礼仪']
                },
                {
                    id: 5,
                    name: '建立关系',
                    icon: '🌟',
                    description: '学习如何建立和维护良好的人际关系',
                    progress: 45,
                    completedCount: 5,
                    totalCount: 11,
                    difficulty: 3,
                    skills: ['初次见面', '维持友谊', '深化关系', '信任建立', '界限设定']
                },
                {
                    id: 6,
                    name: '自我保护',
                    icon: '🛡️',
                    description: '识别和防范人际关系中的风险',
                    progress: 0,
                    completedCount: 0,
                    totalCount: 7,
                    difficulty: 4,
                    skills: ['识别操控', '拒绝技巧', '边界维护', '危险信号', '求助方法']
                }
            ],
            learningPaths: [
                {
                    id: 1,
                    name: '人际交往新手路径',
                    icon: '🌱',
                    description: '适合刚开始学习人际技能的用户',
                    status: 'current',
                    totalDuration: '4周',
                    level: '初级',
                    steps: [
                        { title: '基础沟通', duration: '3天', completed: true, current: false },
                        { title: '倾听技巧', duration: '4天', completed: true, current: false },
                        { title: '表达练习', duration: '5天', completed: false, current: true },
                        { title: '社交礼仪', duration: '3天', completed: false, current: false }
                    ]
                },
                {
                    id: 2,
                    name: '情感表达专精路径',
                    icon: '💝',
                    description: '深入学习情感识别和表达技巧',
                    status: 'locked',
                    totalDuration: '6周',
                    level: '中级',
                    steps: [
                        { title: '情感认知', duration: '1周', completed: false, current: false },
                        { title: '表达训练', duration: '2周', completed: false, current: false },
                        { title: '共情练习', duration: '2周', completed: false, current: false },
                        { title: '综合应用', duration: '1周', completed: false, current: false }
                    ]
                },
                {
                    id: 3,
                    name: '冲突解决大师路径',
                    icon: '⚡',
                    description: '成为化解矛盾的高手',
                    status: 'locked',
                    totalDuration: '8周',
                    level: '高级',
                    steps: [
                        { title: '冲突分析', duration: '2周', completed: false, current: false },
                        { title: '协商技巧', duration: '3周', completed: false, current: false },
                        { title: '调解方法', duration: '2周', completed: false, current: false },
                        { title: '实战演练', duration: '1周', completed: false, current: false }
                    ]
                }
            ],
            quickPractices: [
                { id: 1, name: '1分钟自我介绍', icon: '👋', duration: '5分钟' },
                { id: 2, name: '倾听练习', icon: '👂', duration: '10分钟' },
                { id: 3, name: '情绪识别', icon: '😊', duration: '3分钟' },
                { id: 4, name: '拒绝练习', icon: '🙅', duration: '8分钟' }
            ],
            recentAchievements: [
                {
                    id: 1,
                    name: '沟通新手',
                    icon: '🥉',
                    description: '完成第一个沟通技能',
                    unlocked: true
                },
                {
                    id: 2,
                    name: '倾听达人',
                    icon: '🎧',
                    description: '掌握所有倾听技巧',
                    unlocked: true
                },
                {
                    id: 3,
                    name: '学习之星',
                    icon: '⭐',
                    description: '连续学习7天',
                    unlocked: false,
                    current: 5,
                    target: 7
                },
                {
                    id: 4,
                    name: '技能收集者',
                    icon: '📚',
                    description: '掌握20个技能',
                    unlocked: false,
                    current: 15,
                    target: 20
                }
            ]
        }
    },

    onLoad() {
        this.loadUserProgress();
    },

    methods: {
        // startRecommendedSkill() {
        //     uni.navigateTo({
        //         url: '/pages/interpersonal-wisdom/skill-detail?id=recommended&type=listening'
        //     });
        // },

        startRecommendedSkill() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/skill-detail?skillId=recommended&type=listening'
            });
        },

        enterCategory(category) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/category-detail?categoryId=${category.id}&name=${category.name}`
            });
        },

        followLearningPath(path) {
            if (path.status === 'locked') {
                uni.showToast({
                    title: '请先完成前置学习路径',
                    icon: 'none'
                });
                return;
            }

            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/learning-path?pathId=${path.id}`
            });
        },

        getPathStatusText(status) {
            const statusMap = {
                'current': '进行中',
                'completed': '已完成',
                'locked': '未解锁'
            };
            return statusMap[status] || '未知';
        },

        startQuickPractice(practice) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/quick-practice?practiceId=${practice.id}`
            });
        },

        viewAllAchievements() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/achievements'
            });
        },

        openLearningAssistant() {
            uni.showModal({
                title: '🤖 学习助手',
                content: '我是你的专属学习助手！\n\n可以帮你：\n• 制定学习计划\n• 推荐合适技能\n• 解答学习疑问\n• 提供练习建议',
                confirmText: '开始对话',
                cancelText: '稍后再说',
                success: (res) => {
                    if (res.confirm) {
                        uni.navigateTo({
                            url: '/pages/interpersonal-wisdom/learning-assistant'
                        });
                    }
                }
            });
        },

        loadUserProgress() {
            // 从本地存储或服务器加载用户学习进度
            const progress = uni.getStorageSync('skillProgress') || {};
            // 更新进度数据
            this.updateProgressData(progress);
        },

        updateProgressData(progress) {
            // 根据用户进度更新显示数据
            // 这里可以添加具体的进度计算逻辑
        }
    }
}
</script>

<!-- <style scoped>
.categories-container {
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

.progress-overview {
    padding: 40rpx;
}

.progress-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border-radius: 20rpx;
    padding: 32rpx;
    box-shadow: 0 8rpx 32rpx rgba(102, 126, 234, 0.15);
    border: 2rpx solid #667eea;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
}

.progress-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.progress-percentage {
    font-size: 48rpx;
    font-weight: bold;
    color: #667eea;
}

.progress-bar {
    height: 12rpx;
    background-color: #f0f0f0;
    border-radius: 6rpx;
    overflow: hidden;
    margin-bottom: 24rpx;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 6rpx;
    transition: width 0.3s ease;
}

.progress-stats {
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.stat-label {
    font-size: 24rpx;
    color: #666;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    padding: 0 40rpx;
    display: block;
}

.recommended-section {
    margin-bottom: 40rpx;
}

.recommended-skill {
    background-color: white;
    margin: 0 40rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    border: 2rpx solid #ffd700;
}

.recommended-content {
    display: flex;
    align-items: center;
    flex: 1;
}

.recommended-icon {
    font-size: 48rpx;
    margin-right: 20rpx;
}

.recommended-info {
    flex: 1;
}

.recommended-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.recommended-reason {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 12rpx;
    display: block;
    line-height: 1.5;
}

.recommended-tags {
    display: flex;
    gap: 8rpx;
    flex-wrap: wrap;
}

.skill-tag {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
}

.recommended-action {
    display: flex;
    align-items: center;
    color: #ffd700;
}

.action-text {
    font-size: 26rpx;
    font-weight: bold;
    margin-right: 8rpx;
}

.action-arrow {
    font-size: 24rpx;
}

.categories-section {
    margin-bottom: 40rpx;
}

.category-card {
    background-color: white;
    margin: 0 40rpx 20rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.category-card:active {
    transform: translateY(2rpx);
}

.category-header {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20rpx;
}

.category-icon {
    font-size: 40rpx;
    margin-right: 20rpx;
}

.category-info {
    flex: 1;
}

.category-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.category-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
}

.category-stats {
    text-align: right;
}

.category-progress {
    font-size: 32rpx;
    font-weight: bold;
    color: #667eea;
    display: block;
    margin-bottom: 4rpx;
}

.category-count {
    font-size: 22rpx;
    color: #999;
}

.category-progress-bar {
    height: 8rpx;
    background-color: #f0f0f0;
    border-radius: 4rpx;
    overflow: hidden;
    margin-bottom: 16rpx;
}

.category-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 4rpx;
    transition: width 0.3s ease;
}

.category-skills {
    margin-bottom: 16rpx;
}

.skills-preview {
    font-size: 24rpx;
    color: #888;
    line-height: 1.6;
}

.category-difficulty {
    display: flex;
    align-items: center;
}

.difficulty-label {
    font-size: 24rpx;
    color: #666;
    margin-right: 8rpx;
}

.difficulty-stars {
    display: flex;
    gap: 2rpx;
}

.star {
    font-size: 20rpx;
    color: #ddd;
}

.star.active {
    color: #ffd700;
}

.path-section {
    margin-bottom: 40rpx;
}

.path-card {
    background-color: white;
    margin: 0 40rpx 20rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.path-header {
    display: flex;
    align-items: center;
    margin-bottom: 24rpx;
}

.path-icon {
    font-size: 40rpx;
    margin-right: 20rpx;
}

.path-info {
    flex: 1;
}

.path-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.path-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
}

.path-status {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
    font-size: 22rpx;
}

.path-status.current {
    background-color: #e6f7ff;
    color: #1890ff;
}

.path-status.completed {
    background-color: #f6ffed;
    color: #52c41a;
}

.path-status.locked {
    background-color: #f5f5f5;
    color: #999;
}

.path-timeline {
    margin-bottom: 20rpx;
}

.timeline-step {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
    position: relative;
}

.timeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    left: 12rpx;
    top: 32rpx;
    width: 2rpx;
    height: 20rpx;
    background-color: #e0e0e0;
}

.timeline-step.completed::after {
    background-color: #52c41a;
}

.step-dot {
    width: 24rpx;
    height: 24rpx;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 16rpx;
    flex-shrink: 0;
}

.timeline-step.completed .step-dot {
    background-color: #52c41a;
}

.timeline-step.current .step-dot {
    background-color: #1890ff;
    animation: pulse 2s infinite;
}

.step-title {
    font-size: 26rpx;
    color: #333;
    margin-right: 16rpx;
}

.step-duration {
    font-size: 22rpx;
    color: #999;
}

.path-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16rpx;
    border-top: 1rpx solid #f0f0f0;
}

.path-duration {
    font-size: 24rpx;
    color: #666;
}

.path-level {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.quick-practice {
    margin-bottom: 40rpx;
}

.practice-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
    padding: 0 40rpx;
}

.practice-item {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx 20rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.practice-item:active {
    transform: scale(0.98);
}

.practice-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.practice-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.practice-time {
    font-size: 22rpx;
    color: #667eea;
}

.achievements-section {
    margin-bottom: 40rpx;
}

.achievements-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40rpx;
    margin-bottom: 24rpx;
}

.view-all {
    font-size: 26rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
}

.achievements-scroll {
    padding: 0 40rpx;
}

.achievements-list {
    display: flex;
    gap: 20rpx;
    padding-bottom: 20rpx;
}

.achievement-item {
    min-width: 280rpx;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx 24rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.achievement-item.unlocked {
    border-color: #52c41a;
    background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
}

.achievement-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.achievement-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.achievement-desc {
    font-size: 22rpx;
    color: #666;
    margin-bottom: 12rpx;
    line-height: 1.4;
}

.achievement-progress {
    margin-top: 12rpx;
}

.progress-text {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.floating-actions {
    position: fixed;
    bottom: 120rpx;
    right: 40rpx;
    z-index: 100;
}

.fab-item {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50rpx;
    padding: 20rpx 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
    animation: float 3s ease-in-out infinite;
}

.fab-icon {
    font-size: 32rpx;
    margin-right: 8rpx;
}

.fab-label {
    font-size: 24rpx;
    font-weight: bold;
}

/* 动画效果 */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10rpx);
    }
}

.progress-card {
    animation: slideInDown 0.6s ease-out;
}

.recommended-skill {
    animation: slideInLeft 0.6s ease-out 0.2s both;
}

.category-card {
    animation: fadeInUp 0.5s ease-out;
}

.category-card:nth-child(2) {
    animation-delay: 0.1s;
}

.category-card:nth-child(3) {
    animation-delay: 0.2s;
}

.category-card:nth-child(4) {
    animation-delay: 0.3s;
}

.path-card {
    animation: slideInRight 0.6s ease-out;
}

.practice-item {
    animation: zoomIn 0.4s ease-out;
}

.practice-item:nth-child(2) {
    animation-delay: 0.1s;
}

.practice-item:nth-child(3) {
    animation-delay: 0.2s;
}

.practice-item:nth-child(4) {
    animation-delay: 0.3s;
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translateY(-50rpx);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50rpx);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50rpx);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
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

@keyframes zoomIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .practice-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12rpx;
    }
    
    .practice-item {
        padding: 24rpx 16rpx;
    }
    
    .practice-icon {
        font-size: 40rpx;
    }
    
    .floating-actions {
        bottom: 100rpx;
        right: 30rpx;
    }
    
    .fab-item {
        padding: 16rpx 24rpx;
    }
    
    .fab-icon {
        font-size: 28rpx;
    }
    
    .fab-label {
        font-size: 22rpx;
    }
}

@media (max-width: 480rpx) {
    .category-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 16rpx;
    }
    
    .category-stats {
        text-align: left;
        display: flex;
        align-items: center;
        gap: 20rpx;
    }
    
    .recommended-skill {
        flex-direction: column;
        text-align: center;
        gap: 20rpx;
    }
    
    .recommended-content {
        flex-direction: column;
        text-align: center;
    }
    
    .path-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 16rpx;
    }
    
    .achievements-scroll {
        padding: 0 20rpx;
    }
    
    .achievement-item {
        min-width: 240rpx;
    }
}

/* 交互增强 */
.category-card:hover {
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.2);
    transform: translateY(-4rpx);
}

.practice-item:hover {
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.15);
}

.recommended-skill:active {
    transform: scale(0.98);
}

.fab-item:active {
    transform: scale(0.95) translateY(-10rpx);
}

/* 状态指示器增强 */
.path-status.current::before {
    content: '';
    position: absolute;
    left: -8rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 6rpx;
    height: 6rpx;
    border-radius: 50%;
    background-color: #1890ff;
    animation: pulse 2s infinite;
}

.path-status {
    position: relative;
}

/* 进度条动画 */
.progress-fill,
.category-progress-fill {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
    background-size: 200% 100%;
    animation: progressGlow 3s ease-in-out infinite;
}

@keyframes progressGlow {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

/* 成就徽章效果 */
.achievement-item.unlocked {
    position: relative;
    overflow: hidden;
}

.achievement-item.unlocked::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(82, 196, 26, 0.3), transparent);
    animation: shine 2s infinite;
}

@keyframes shine {
    0% {
        left: -100%;
    }
    100% {
        left: 100%;
    }
}

/* 技能标签悬停效果 */
.skill-tag {
    transition: all 0.3s ease;
}

.recommended-skill:hover .skill-tag {
    background-color: #667eea;
    color: white;
    transform: scale(1.05);
}

/* 难度星级动画 */
.star.active {
    animation: starTwinkle 2s ease-in-out infinite;
    animation-delay: calc(var(--star-index, 0) * 0.2s);
}

@keyframes starTwinkle {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.7;
        transform: scale(1.1);
    }
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6rpx;
    height: 6rpx;
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
.category-card:focus,
.practice-item:focus,
.fab-item:focus {
    outline: 2rpx solid #667eea;
    outline-offset: 2rpx;
}

/* 加载状态 */
.categories-container[data-loading="true"] {
    pointer-events: none;
    opacity: 0.8;
}

/* 错误状态 */
.category-card[data-error="true"] {
    background-color: #fff2f0;
    border: 1rpx solid #ffccc7;
}

/* 成功状态 */
.category-card[data-success="true"] {
    background-color: #f6ffed;
    border: 1rpx solid #d9f7be;
}

/* 底部安全间距 */
.categories-container {
    padding-bottom: calc(140rpx + env(safe-area-inset-bottom));
}

.floating-actions {
    bottom: calc(120rpx + env(safe-area-inset-bottom));
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
    .category-card,
    .practice-item,
    .path-card {
        border: 1rpx solid #333;
    }
    
    .fab-item {
        border: 2rpx solid #000;
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

/* 文字选择样式 */
::selection {
    background-color: rgba(102, 126, 234, 0.3);
    color: #333;
}

/* 长按效果 */
.category-card:active {
    transform: translateY(2rpx) scale(0.98);
}

.practice-item:active {
    transform: scale(0.95);
}

/* 网格布局优化 */
.practice-grid {
    gap: 16rpx;
}

@supports (display: grid) {
    .practice-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300rpx, 1fr));
    }
}

@supports not (display: grid) {
    .practice-grid {
        display: flex;
        flex-wrap: wrap;
    }
    
    .practice-item {
        flex: 1;
        min-width: 300rpx;
        margin: 8rpx;
    }
}
</style> -->

<style scoped>
.categories-container {
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

.progress-overview {
    padding: 40rpx;
}

.progress-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border-radius: 20rpx;
    padding: 32rpx;
    box-shadow: 0 8rpx 32rpx rgba(102, 126, 234, 0.15);
    border: 2rpx solid #667eea;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
}

.progress-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.progress-percentage {
    font-size: 48rpx;
    font-weight: bold;
    color: #667eea;
}

.progress-bar {
    height: 12rpx;
    background-color: #f0f0f0;
    border-radius: 6rpx;
    overflow: hidden;
    margin-bottom: 24rpx;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 6rpx;
    transition: width 0.3s ease;
}

.progress-stats {
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.stat-label {
    font-size: 24rpx;
    color: #666;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    padding: 0 40rpx;
    display: block;
}

.recommended-section {
    margin-bottom: 40rpx;
}

.recommended-skill {
    background-color: white;
    margin: 0 40rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    border: 2rpx solid #ffd700;
}

.recommended-content {
    display: flex;
    align-items: center;
    flex: 1;
}

.recommended-icon {
    font-size: 48rpx;
    margin-right: 20rpx;
}

.recommended-info {
    flex: 1;
}

.recommended-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.recommended-reason {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 12rpx;
    display: block;
    line-height: 1.5;
}

.recommended-tags {
    display: flex;
    gap: 8rpx;
    flex-wrap: wrap;
}

.skill-tag {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
}

.recommended-action {
    display: flex;
    align-items: center;
    color: #ffd700;
}

.action-text {
    font-size: 26rpx;
    font-weight: bold;
    margin-right: 8rpx;
}

.action-arrow {
    font-size: 24rpx;
}

/* 技能分类网格布局 */
.categories-section {
    margin-bottom: 40rpx;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
    padding: 0 40rpx;
}

.category-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 24rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.category-card:active {
    transform: translateY(2rpx);
}

.category-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 16rpx;
    text-align: center;
}

.category-icon {
    font-size: 48rpx;
    margin-bottom: 12rpx;
}

.category-info {
    width: 100%;
    text-align: center;
}

.category-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.category-desc {
    font-size: 22rpx;
    color: #666;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.category-stats {
    text-align: center;
    margin-bottom: 12rpx;
}

.category-progress {
    font-size: 28rpx;
    font-weight: bold;
    color: #667eea;
    display: block;
    margin-bottom: 4rpx;
}

.category-count {
    font-size: 20rpx;
    color: #999;
}

.category-progress-bar {
    height: 6rpx;
    background-color: #f0f0f0;
    border-radius: 3rpx;
    overflow: hidden;
    margin-bottom: 12rpx;
}

.category-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 3rpx;
    transition: width 0.3s ease;
}

.category-skills {
    margin-bottom: 12rpx;
}

.skills-preview {
    font-size: 20rpx;
    color: #888;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.category-difficulty {
    display: flex;
    align-items: center;
    justify-content: center;
}

.difficulty-label {
    font-size: 20rpx;
    color: #666;
    margin-right: 6rpx;
}

.difficulty-stars {
    display: flex;
    gap: 2rpx;
}

.star {
    font-size: 16rpx;
    color: #ddd;
}

.star.active {
    color: #ffd700;
}

.path-section {
    margin-bottom: 40rpx;
}

.path-card {
    background-color: white;
    margin: 0 40rpx 20rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.path-header {
    display: flex;
    align-items: center;
    margin-bottom: 24rpx;
}

.path-icon {
    font-size: 40rpx;
    margin-right: 20rpx;
}

.path-info {
    flex: 1;
}

.path-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.path-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
}

.path-status {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
    font-size: 22rpx;
}

.path-status.current {
    background-color: #e6f7ff;
    color: #1890ff;
}

.path-status.completed {
    background-color: #f6ffed;
    color: #52c41a;
}

.path-status.locked {
    background-color: #f5f5f5;
    color: #999;
}

.path-timeline {
    margin-bottom: 20rpx;
}

.timeline-step {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
    position: relative;
}

.timeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    left: 12rpx;
    top: 32rpx;
    width: 2rpx;
    height: 20rpx;
    background-color: #e0e0e0;
}

.timeline-step.completed::after {
    background-color: #52c41a;
}

.step-dot {
    width: 24rpx;
    height: 24rpx;
    border-radius: 50%;
    background-color: #e0e0e0;
    margin-right: 16rpx;
    flex-shrink: 0;
}

.timeline-step.completed .step-dot {
    background-color: #52c41a;
}

.timeline-step.current .step-dot {
    background-color: #1890ff;
    animation: pulse 2s infinite;
}

.step-title {
    font-size: 26rpx;
    color: #333;
    margin-right: 16rpx;
}

.step-duration {
    font-size: 22rpx;
    color: #999;
}

.path-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16rpx;
    border-top: 1rpx solid #f0f0f0;
}

.path-duration {
    font-size: 24rpx;
    color: #666;
}

.path-level {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.quick-practice {
    margin-bottom: 40rpx;
}

.practice-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
    padding: 0 40rpx;
}

.practice-item {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx 20rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.practice-item:active {
    transform: scale(0.98);
}

.practice-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.practice-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.practice-time {
    font-size: 22rpx;
    color: #667eea;
}

.achievements-section {
    margin-bottom: 40rpx;
}

.achievements-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40rpx;
    margin-bottom: 24rpx;
}

.view-all {
    font-size: 26rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
}

.achievements-scroll {
    padding: 0 40rpx;
}

.achievements-list {
    display: flex;
    gap: 20rpx;
    padding-bottom: 20rpx;
}

.achievement-item {
    min-width: 280rpx;
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx 24rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.achievement-item.unlocked {
    border-color: #52c41a;
    background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
}

.achievement-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.achievement-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.achievement-desc {
    font-size: 22rpx;
    color: #666;
    margin-bottom: 12rpx;
    line-height: 1.4;
}

.achievement-progress {
    margin-top: 12rpx;
}

.progress-text {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.floating-actions {
    position: fixed;
    bottom: 120rpx;
    right: 40rpx;
    z-index: 100;
}

.fab-item {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50rpx;
    padding: 20rpx 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
    animation: float 3s ease-in-out infinite;
}

.fab-icon {
    font-size: 32rpx;
    margin-right: 8rpx;
}

.fab-label {
    font-size: 24rpx;
    font-weight: bold;
}

/* 动画效果 */
@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10rpx);
    }
}

.progress-card {
    animation: slideInDown 0.6s ease-out;
}

.recommended-skill {
    animation: slideInLeft 0.6s ease-out 0.2s both;
}

.category-card {
    animation: fadeInUp 0.5s ease-out;
}

.category-card:nth-child(2) {
    animation-delay: 0.1s;
}

.category-card:nth-child(3) {
    animation-delay: 0.2s;
}

.category-card:nth-child(4) {
    animation-delay: 0.3s;
}

.path-card {
    animation: slideInRight 0.6s ease-out;
}

.practice-item {
    animation: zoomIn 0.4s ease-out;
}

.practice-item:nth-child(2) {
    animation-delay: 0.1s;
}

.practice-item:nth-child(3) {
    animation-delay: 0.2s;
}

.practice-item:nth-child(4) {
    animation-delay: 0.3s;
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translateY(-50rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
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

@keyframes zoomIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .categories-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12rpx;
        padding: 0 30rpx;
    }

    .category-card {
        padding: 20rpx;
    }

    .category-icon {
        font-size: 40rpx;
    }

    .category-name {
        font-size: 26rpx;
    }

    .category-desc {
        font-size: 20rpx;
    }

    .practice-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12rpx;
    }

    .practice-item {
        padding: 24rpx 16rpx;
    }

    .practice-icon {
        font-size: 40rpx;
    }

    .floating-actions {
        bottom: 100rpx;
        right: 30rpx;
    }

    .fab-item {
        padding: 16rpx 24rpx;
    }

    .fab-icon {
        font-size: 28rpx;
    }

    .fab-label {
        font-size: 22rpx;
    }
}

@media (max-width: 480rpx) {
    .categories-grid {
        grid-template-columns: 1fr;
        gap: 16rpx;
    }

    .category-header {
        flex-direction: row;
        align-items: center;
        text-align: left;
    }

    .category-icon {
        margin-right: 16rpx;
        margin-bottom: 0;
    }

    .category-info {
        text-align: left;
        flex: 1;
    }

    .category-stats {
        text-align: left;
        display: flex;
        align-items: center;
        gap: 20rpx;
    }

    .recommended-skill {
        flex-direction: column;
        text-align: center;
        gap: 20rpx;
    }

    .recommended-content {
        flex-direction: column;
        text-align: center;
    }

    .path-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 16rpx;
    }

    .achievements-scroll {
        padding: 0 20rpx;
    }

    .achievement-item {
        min-width: 240rpx;
    }
}

/* 交互增强 */
.category-card:hover {
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.2);
    transform: translateY(-4rpx);
}

.practice-item:hover {
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.15);
}

.recommended-skill:active {
    transform: scale(0.98);
}

.fab-item:active {
    transform: scale(0.95) translateY(-10rpx);
}

/* 状态指示器增强 */
.path-status.current::before {
    content: '';
    position: absolute;
    left: -8rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 6rpx;
    height: 6rpx;
    border-radius: 50%;
    background-color: #1890ff;
    animation: pulse 2s infinite;
}

.path-status {
    position: relative;
}

/* 进度条动画 */
.progress-fill,
.category-progress-fill {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
    background-size: 200% 100%;
    animation: progressGlow 3s ease-in-out infinite;
}

@keyframes progressGlow {

    0%,
    100% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }
}

/* 成就徽章效果 */
.achievement-item.unlocked {
    position: relative;
    overflow: hidden;
}

.achievement-item.unlocked::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(82, 196, 26, 0.3), transparent);
    animation: shine 2s infinite;
}

@keyframes shine {
    0% {
        left: -100%;
    }

    100% {
        left: 100%;
    }
}

/* 技能标签悬停效果 */
.skill-tag {
    transition: all 0.3s ease;
}

.recommended-skill:hover .skill-tag {
    background-color: #667eea;
    color: white;
    transform: scale(1.05);
}

/* 难度星级动画 */
.star.active {
    animation: starTwinkle 2s ease-in-out infinite;
    animation-delay: calc(var(--star-index, 0) * 0.2s);
}

@keyframes starTwinkle {

    0%,
    100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: 0.7;
        transform: scale(1.1);
    }
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6rpx;
    height: 6rpx;
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
.category-card:focus,
.practice-item:focus,
.fab-item:focus {
    outline: 2rpx solid #667eea;
    outline-offset: 2rpx;
}

/* 加载状态 */
.categories-container[data-loading="true"] {
    pointer-events: none;
    opacity: 0.8;
}

/* 错误状态 */
.category-card[data-error="true"] {
    background-color: #fff2f0;
    border: 1rpx solid #ffccc7;
}

/* 成功状态 */
.category-card[data-success="true"] {
    background-color: #f6ffed;
    border: 1rpx solid #d9f7be;
}

/* 底部安全间距 */
.categories-container {
    padding-bottom: calc(140rpx + env(safe-area-inset-bottom));
}

.floating-actions {
    bottom: calc(120rpx + env(safe-area-inset-bottom));
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {

    .category-card,
    .practice-item,
    .path-card {
        border: 1rpx solid #333;
    }

    .fab-item {
        border: 2rpx solid #000;
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

/* 文字选择样式 */
::selection {
    background-color: rgba(102, 126, 234, 0.3);
    color: #333;
}

/* 长按效果 */
.category-card:active {
    transform: translateY(2rpx) scale(0.98);
}

.practice-item:active {
    transform: scale(0.95);
}

/* 网格布局优化 */
.practice-grid {
    gap: 16rpx;
}

@supports (display: grid) {
    .practice-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300rpx, 1fr));
    }
}

@supports not (display: grid) {
    .practice-grid {
        display: flex;
        flex-wrap: wrap;
    }

    .practice-item {
        flex: 1;
        min-width: 300rpx;
        margin: 8rpx;
    }
}
</style>