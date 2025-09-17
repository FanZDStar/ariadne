<template>
    <view class="category-detail-container">
        <view class="header">
            <view class="category-info">
                <text class="category-icon">{{ categoryData.icon }}</text>
                <view class="category-text">
                    <text class="category-name">{{ categoryData.name }}</text>
                    <text class="category-desc">{{ categoryData.description }}</text>
                </view>
            </view>
        </view>

        <view class="content">
            <!-- 推荐技能 -->
            <view v-if="recommendedSkills.length > 0" class="section">
                <view class="section-header">
                    <text class="section-title">🎯 为你推荐</text>
                </view>
                <!-- <view v-for="skill in recommendedSkills" :key="skill.id" class="skill-card recommended"
                    @click="viewSkillDetail(skill)"> -->
                <view v-for="skill in recommendedSkills" :key="skill.id" class="skill-card recommended">
                    <view class="skill-header">
                        <text class="skill-title">{{ skill.name }}</text>
                        <view class="difficulty-badge" :class="skill.difficulty">
                            <text class="difficulty-text">{{ getDifficultyText(skill.difficulty) }}</text>
                        </view>
                    </view>
                    <text class="skill-description">{{ skill.description }}</text>
                    <view class="skill-meta">
                        <view class="meta-item">
                            <text class="meta-icon">⏱️</text>
                            <text class="meta-text">{{ skill.estimatedTime }}分钟</text>
                        </view>
                    </view>
                    <view class="skill-actions">
                        <view class="action-btn primary" @click.stop="viewSkillDetail(skill)">
                            <text class="btn-text">开始学习</text>
                        </view>
                        <view class="action-btn secondary" @click.stop="addToFavorites(skill)">
                            <text class="btn-text">收藏</text>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 技能列表 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">📚 全部技能</text>
                </view>

                <view class="skills-grid">
                    <view v-for="skill in filteredSkills" :key="skill.id" class="skill-card"
                        :class="{ mastered: skill.status === 'mastered', learning: skill.status === 'learning' }"
                        @click="viewSkillDetail(skill)">
                        <!-- <view class="skill-status-indicator" v-if="skill.status === 'mastered'">
                            <text class="status-icon">✅</text>
                        </view>
                        <view class="skill-status-indicator" v-else-if="skill.status === 'learning'">
                            <text class="status-icon">📖</text>
                        </view> -->

                        <text class="skill-name">{{ skill.name }}</text>
                        <text class="skill-brief">{{ skill.brief }}</text>

                        <view class="skill-tags">
                            <text v-for="tag in skill.tags" :key="tag" class="skill-tag">{{ tag }}</text>
                        </view>

                        <view class="skill-footer">
                            <view class="difficulty-indicator" :class="skill.difficulty">
                                <text class="difficulty-dot">●</text>
                                <text class="difficulty-label">{{ getDifficultyText(skill.difficulty) }}</text>
                            </view>
                            <!-- <view v-if="skill.status === 'learning'" class="learning-progress">
                                <text class="progress-text">{{ skill.progress }}%</text>
                            </view> -->
                        </view>
                    </view>
                </view>
            </view>

            <!-- 学习建议 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">💡 学习建议</text>
                </view>
                <view class="suggestion-card">
                    <text class="suggestion-title">{{ learningTip.title }}</text>
                    <text class="suggestion-content">{{ learningTip.content }}</text>
                    <view class="suggestion-action" @click="followSuggestion">
                    </view>
                </view>
            </view>
        </view>

        <BackToTop ref="backToTop" :threshold="50" :bottom="40" :right="40" icon="🔝"
            @scroll-to-top-success="onScrollToTopSuccess" />
    </view>
</template>

<script>
import BackToTop from '@/components/BackToTop.vue'
export default {
    components: {
        BackToTop
    },
    data() {
        return {
            categoryId: '',
            categoryName: '',
            categoryData: {},
            allSkills: [],
            recommendedSkills: [],
            filterType: 'all',
            learningTip: {}
        }
    },

    computed: {
        progressPercentage() {
            if (this.categoryData.totalSkills === 0) return 0;
            return Math.round((this.categoryData.masteredSkills / this.categoryData.totalSkills) * 100);
        },

        filteredSkills() {
            switch (this.filterType) {
                case 'learned':
                    return this.allSkills.filter(skill => skill.status === 'mastered');
                case 'learning':
                    return this.allSkills.filter(skill => skill.status === 'learning');
                default:
                    return this.allSkills;
            }
        }
    },

    onLoad(options) {
        this.categoryId = options.categoryId;
        this.categoryName = options.name || '';
        this.loadCategoryData();
    },
    // 监听页面滚动
    onPageScroll(e) {
        // 更新返回顶部按钮的显示状态
        if (this.$refs.backToTop) {
            this.$refs.backToTop.updateShowState(e.scrollTop);
        }
    },
    methods: {
        // 返回顶部成功回调
        onScrollToTopSuccess() {
            uni.showToast({
                title: '已回到顶部',
                icon: 'success',
                duration: 1000
            });
        },
        async loadCategoryData() {
            try {
                uni.showLoading({ title: '加载中...' });

                // 模拟API调用
                await this.mockLoadCategoryData();

            } catch (error) {
                console.error('加载分类数据失败:', error);
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        async mockLoadCategoryData() {
            // 根据不同的 categoryId 返回不同的分类数据
            const categoryDataMap = {
                'communication': {
                    id: this.categoryId,
                    name: '沟通表达',
                    description: '学会清晰、准确、有效的表达自己的想法和感受',
                    icon: '💬',
                    totalSkills: 12,
                    masteredSkills: 5,
                    skills: [
                        {
                            id: 1,
                            name: '主动倾听',
                            brief: '学会用心倾听对方的话语和情感',
                            description: '主动倾听是建立良好人际关系的基础技能，包括关注对方的言语和非言语信息。',
                            difficulty: 'basic',
                            estimatedTime: 15,
                            learnerCount: 1234,
                            status: 'mastered',
                            tags: ['倾听', '沟通基础'],
                            progress: 100
                        },
                        {
                            id: 2,
                            name: '情感表达',
                            brief: '准确表达自己的情感和需求',
                            description: '学会用"我"的句式表达情感，避免指责和批评。',
                            difficulty: 'intermediate',
                            estimatedTime: 20,
                            learnerCount: 956,
                            status: 'learning',
                            tags: ['情感', '表达'],
                            progress: 65
                        },
                        {
                            id: 3,
                            name: '非暴力沟通',
                            brief: '以善意和理解进行沟通',
                            description: '学习非暴力沟通的四个步骤：观察、感受、需要、请求。',
                            difficulty: 'advanced',
                            estimatedTime: 30,
                            learnerCount: 567,
                            status: 'new',
                            tags: ['沟通技巧', '冲突处理']
                        }
                    ],
                    learningTip: {
                        title: '循序渐进的学习方法',
                        content: '建议从基础技能开始学习，每天练习15-20分钟，结合实际场景应用，效果更佳。'
                    }
                },
                'emotional_expression': {
                    id: this.categoryId,
                    name: '情感理解',
                    description: '理解自己和他人的情感，提升情感智慧',
                    icon: '💝',
                    totalSkills: 10,
                    masteredSkills: 3,
                    skills: [
                        {
                            id: 4,
                            name: '情绪识别',
                            brief: '准确识别自己和他人的情绪状态',
                            description: '通过观察面部表情、语调、肢体语言等识别情绪。',
                            difficulty: 'basic',
                            estimatedTime: 12,
                            learnerCount: 890,
                            status: 'mastered',
                            tags: ['情绪识别', '观察力'],
                            progress: 100
                        },
                        {
                            id: 5,
                            name: '情感共鸣',
                            brief: '与他人产生情感共鸣和理解',
                            description: '学会站在对方角度思考，理解对方的感受。',
                            difficulty: 'intermediate',
                            estimatedTime: 25,
                            learnerCount: 675,
                            status: 'learning',
                            tags: ['共情', '理解'],
                            progress: 40
                        },
                        {
                            id: 6,
                            name: '情绪调节',
                            brief: '有效管理和调节自己的情绪',
                            description: '掌握深呼吸、认知重构等情绪调节技巧。',
                            difficulty: 'advanced',
                            estimatedTime: 35,
                            learnerCount: 445,
                            status: 'new',
                            tags: ['情绪管理', '自我调节']
                        }
                    ],
                    learningTip: {
                        title: '情感智慧提升要点',
                        content: '多观察自己的情绪变化，练习表达感受而非情绪，培养换位思考的习惯。'
                    }
                },
                'relationship_building': {
                    id: this.categoryId,
                    name: '关系建立',
                    description: '建立和维护健康、积极的人际关系',
                    icon: '🤝',
                    totalSkills: 8,
                    masteredSkills: 2,
                    skills: [
                        {
                            id: 7,
                            name: '破冰技巧',
                            brief: '在新环境中快速与他人建立联系',
                            description: '掌握开场白、话题引导等社交技巧。',
                            difficulty: 'basic',
                            estimatedTime: 18,
                            learnerCount: 1123,
                            status: 'mastered',
                            tags: ['破冰', '社交'],
                            progress: 100
                        },
                        {
                            id: 8,
                            name: '信任建立',
                            brief: '在关系中建立互相信任的基础',
                            description: '通过真诚、一致性、可靠性建立信任关系。',
                            difficulty: 'intermediate',
                            estimatedTime: 28,
                            learnerCount: 789,
                            status: 'learning',
                            tags: ['信任', '关系维护'],
                            progress: 55
                        },
                        {
                            id: 9,
                            name: '冲突解决',
                            brief: '有效处理人际冲突和分歧',
                            description: '学会协商、妥协、寻找双赢解决方案。',
                            difficulty: 'advanced',
                            estimatedTime: 40,
                            learnerCount: 234,
                            status: 'new',
                            tags: ['冲突处理', '协商']
                        }
                    ],
                    learningTip: {
                        title: '关系建立核心原则',
                        content: '真诚是最好的社交技巧，保持一致性和可靠性，学会给予和接受。'
                    }
                },
                'special_scenarios': {
                    id: this.categoryId,
                    name: '特殊情境',
                    description: '应对特殊场合和复杂人际情境',
                    icon: '🎯',
                    totalSkills: 15,
                    masteredSkills: 1,
                    skills: [
                        {
                            id: 10,
                            name: '职场沟通',
                            brief: '在职场环境中有效沟通',
                            description: '掌握正式场合的沟通技巧和职场礼仪。',
                            difficulty: 'intermediate',
                            estimatedTime: 22,
                            learnerCount: 1567,
                            status: 'mastered',
                            tags: ['职场', '正式沟通'],
                            progress: 100
                        },
                        {
                            id: 11,
                            name: '异地恋维护',
                            brief: '维护异地恋关系的特殊技巧',
                            description: '学会通过技术手段保持亲密度和信任。',
                            difficulty: 'advanced',
                            estimatedTime: 45,
                            learnerCount: 456,
                            status: 'learning',
                            tags: ['异地恋', '关系维护'],
                            progress: 30
                        },
                        {
                            id: 12,
                            name: '危机干预',
                            brief: '在他人遇到情感危机时提供支持',
                            description: '学会识别危机信号，提供适当的支持和帮助。',
                            difficulty: 'advanced',
                            estimatedTime: 50,
                            learnerCount: 123,
                            status: 'new',
                            tags: ['危机干预', '支持技巧']
                        }
                    ],
                    learningTip: {
                        title: '特殊情境应对策略',
                        content: '每种情境都有其特殊性，重要的是保持灵活性和适应性，必要时寻求专业帮助。'
                    }
                }
            };

            // 根据 categoryId 获取对应数据，如果没有匹配则使用默认数据
            const categoryData = categoryDataMap[this.categoryId] || categoryDataMap['communication'];

            this.categoryData = {
                id: categoryData.id,
                name: categoryData.name,
                description: categoryData.description,
                icon: categoryData.icon,
                totalSkills: categoryData.totalSkills,
                masteredSkills: categoryData.masteredSkills
            };

            this.allSkills = categoryData.skills;
            this.recommendedSkills = this.allSkills.filter(skill => skill.status === 'new').slice(0, 2);
            this.learningTip = categoryData.learningTip;
        },

        setFilter(type) {
            this.filterType = type;
        },

        viewSkillDetail(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.id}&categoryId=${this.categoryId}`
            });
        },

        startLearning(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id}&type=learning`
            });
        },

        addToFavorites(skill) {
            uni.showToast({
                title: '已添加到收藏',
                icon: 'success'
            });
        },

        followSuggestion() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/learning-assistant'
            });
        },

        showLearningPlan() {
            uni.showModal({
                title: '制定学习计划',
                content: `为"${this.categoryData.name}"制定个性化学习计划？\n\n系统将根据你的水平和目标推荐最适合的学习路径。`,
                confirmText: '开始制定',
                success: (res) => {
                    if (res.confirm) {
                        uni.navigateTo({
                            url: `/pages/interpersonal-wisdom/learning-path?categoryId=${this.categoryId}&action=create`
                        });
                    }
                }
            });
        },

        getDifficultyText(difficulty) {
            const map = {
                'basic': '基础',
                'intermediate': '进阶',
                'advanced': '高级'
            };
            return map[difficulty] || '未知';
        }
    }
}
</script>

<style scoped>
.category-detail-container {
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40rpx;
    color: white;
}

.category-info {
    display: flex;
    align-items: center;
    margin-bottom: 32rpx;
}

.category-icon {
    font-size: 64rpx;
    margin-right: 24rpx;
}

.category-text {
    flex: 1;
}

.category-name {
    font-size: 42rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 8rpx;
}

.category-desc {
    font-size: 26rpx;
    opacity: 0.9;
    line-height: 1.4;
}


.content {
    padding: 0 40rpx 120rpx;
}

.section {
    margin-bottom: 48rpx;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
    padding-top: 24rpx;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.section-subtitle {
    font-size: 24rpx;
    color: #666;
    margin-top: 4rpx;
}

.filter-controls {
    display: flex;
    gap: 12rpx;
}

.filter-btn {
    padding: 12rpx 20rpx;
    background-color: #f0f0f0;
    border-radius: 20rpx;
    font-size: 24rpx;
    color: #666;
    transition: all 0.3s ease;
}

.filter-btn.active {
    background-color: #667eea;
    color: white;
}

.skill-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    position: relative;
    transition: transform 0.2s ease;
}

.skill-card:active {
    transform: translateY(2rpx);
}

.skill-card.recommended {
    border: 2rpx solid #667eea;
    background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
}

.skill-card.mastered {
    border-left: 6rpx solid #4caf50;
}

.skill-card.learning {
    border-left: 6rpx solid #ff9800;
}

.skill-status-indicator {
    position: absolute;
    top: 16rpx;
    right: 16rpx;
}

.status-icon {
    font-size: 24rpx;
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.skill-title,
.skill-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
}

.skill-description,
.skill-brief {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 20rpx;
}

.difficulty-badge {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
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

.skill-meta {
    display: flex;
    gap: 24rpx;
    margin-bottom: 24rpx;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
}

.meta-icon {
    font-size: 20rpx;
}

.meta-text {
    font-size: 22rpx;
    color: #999;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    margin-bottom: 24rpx;
}

.skill-tag {
    background-color: #f0f0f0;
    color: #666;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
}

.skill-actions {
    display: flex;
    gap: 16rpx;
}

.action-btn {
    flex: 1;
    padding: 20rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 26rpx;
}

.action-btn.primary {
    background-color: #667eea;
    color: white;
}

.action-btn.secondary {
    background-color: #f0f0f0;
    color: #666;
}

.skill-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.difficulty-indicator {
    display: flex;
    align-items: center;
    gap: 8rpx;
    font-size: 22rpx;
}

.difficulty-indicator.basic {
    color: #4caf50;
}

.difficulty-indicator.intermediate {
    color: #ff9800;
}

.difficulty-indicator.advanced {
    color: #f44336;
}

.difficulty-dot {
    font-size: 16rpx;
}

.learning-progress {
    font-size: 22rpx;
    color: #667eea;
    font-weight: bold;
}

.skills-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20rpx;
}

.suggestion-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.suggestion-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.suggestion-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 24rpx;
}

.suggestion-action {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8rpx;
    color: #667eea;
}

.action-text {
    font-size: 26rpx;
}

.action-arrow {
    font-size: 24rpx;
}


@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-8rpx);
    }
}

/* 响应式设计 */
@media (min-width: 750rpx) {
    .skills-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>