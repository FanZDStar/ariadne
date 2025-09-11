<template>
    <view class="wisdom-container">
        <view class="header">
            <text class="title">人际智慧</text>
            <text class="subtitle">提升交往技能，保护情感安全</text>
        </view>

        <view class="nav-tabs">
            <view class="tab-item" :class="{ active: activeTab === 'skills' }" @click="activeTab = 'skills'">
                <text class="tab-icon">🤝</text>
                <text class="tab-text">技能学习</text>
            </view>
            <view class="tab-item" :class="{ active: activeTab === 'protection' }" @click="activeTab = 'protection'">
                <text class="tab-icon">🛡️</text>
                <text class="tab-text">防护指南</text>
            </view>
            <view class="tab-item" :class="{ active: activeTab === 'practice' }" @click="activeTab = 'practice'">
                <text class="tab-icon">🎭</text>
                <text class="tab-text">实战练习</text>
            </view>
            <view class="tab-item" :class="{ active: activeTab === 'growth' }" @click="activeTab = 'growth'">
                <text class="tab-icon">📈</text>
                <text class="tab-text">成长档案</text>
            </view>
        </view>

        <!-- 技能学习模块 -->
        <view v-if="activeTab === 'skills'" class="content-section">
            <view class="section-header">
                <text class="section-title">智能推荐技巧</text>
                <view class="refresh-btn" @click="getRecommendedSkills">
                    <text class="refresh-icon">🔄</text>
                    <text class="refresh-text">刷新推荐</text>
                </view>
            </view>

            <view v-if="recommendedSkills.length > 0" class="recommended-skills">
                <view v-for="skill in recommendedSkills" :key="skill.id" class="skill-card recommended"
                    @click="selectSkill(skill)">
                    <view class="skill-header">
                        <text class="skill-title">{{ skill.title }}</text>
                        <view class="difficulty-badge" :class="skill.difficulty">
                            <text class="difficulty-text">{{ getDifficultyText(skill.difficulty) }}</text>
                        </view>
                    </view>
                    <text class="skill-content">{{ skill.content }}</text>
                    <view class="skill-tags">
                        <text v-for="tag in skill.tags" :key="tag" class="skill-tag">{{ tag }}</text>
                    </view>
                    <view class="skill-actions">
                        <view class="action-btn primary" @click.stop="practiceSkill(skill)">
                            <text class="action-text">开始练习</text>
                        </view>
                        <view class="action-btn secondary" @click.stop="generateScenario(skill)">
                            <text class="action-text">生成场景</text>
                        </view>
                    </view>
                </view>
            </view>

            <view class="categories-section">
                <text class="section-title">技能分类</text>
                <view class="categories-grid">
                    <view v-for="category in skillCategories" :key="category.id" class="category-card"
                        @click="viewCategorySkills(category)">
                        <text class="category-icon">{{ getCategoryIcon(category.id) }}</text>
                        <text class="category-name">{{ category.name }}</text>
                        <text class="category-count">{{ category.skill_count }}个技巧</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 防护指南模块 -->
        <view v-if="activeTab === 'protection'" class="content-section">
            <view class="protection-tools">
                <view class="tool-card assessment" @click="startRiskAssessment">
                    <view class="tool-header">
                        <text class="tool-icon">📊</text>
                        <text class="tool-title">关系健康评估</text>
                    </view>
                    <text class="tool-desc">评估你当前关系的健康状况</text>
                    <view class="tool-btn">
                        <text class="btn-text">开始评估</text>
                    </view>
                </view>

                <view class="tool-card simulation" @click="startScenarioSimulation">
                    <view class="tool-header">
                        <text class="tool-icon">🎯</text>
                        <text class="tool-title">情景识别训练</text>
                    </view>
                    <text class="tool-desc">通过模拟场景提升风险识别能力</text>
                    <view class="tool-btn">
                        <text class="btn-text">开始训练</text>
                    </view>
                </view>

                <view class="tool-card advice" @click="getPersonalizedAdvice">
                    <view class="tool-header">
                        <text class="tool-icon">💡</text>
                        <text class="tool-title">个性化建议</text>
                    </view>
                    <text class="tool-desc">获取针对你情况的专属防护建议</text>
                    <view class="tool-btn">
                        <text class="btn-text">获取建议</text>
                    </view>
                </view>

                <view class="tool-card emergency" @click="viewEmergencyResources">
                    <view class="tool-header">
                        <text class="tool-icon">🆘</text>
                        <text class="tool-title">应急资源</text>
                    </view>
                    <text class="tool-desc">查看专业求助渠道和应急联系方式</text>
                    <view class="tool-btn">
                        <text class="btn-text">查看资源</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 实战练习模块 -->
        <view v-if="activeTab === 'practice'" class="content-section">
            <view class="practice-options">
                <view class="practice-card" @click="startInteractivePractice">
                    <view class="practice-header">
                        <text class="practice-icon">💬</text>
                        <text class="practice-title">AI对话练习</text>
                    </view>
                    <text class="practice-desc">与AI进行模拟对话，练习交往技巧</text>
                </view>

                <view class="practice-card" @click="startScenarioPractice">
                    <view class="practice-header">
                        <text class="practice-icon">🎬</text>
                        <text class="practice-title">情景模拟练习</text>
                    </view>
                    <text class="practice-desc">在模拟情景中练习应对各种社交场合</text>
                </view>

                <view class="practice-card" @click="startProtectionDrill">
                    <view class="practice-header">
                        <text class="practice-icon">🛡️</text>
                        <text class="practice-title">防护技能训练</text>
                    </view>
                    <text class="practice-desc">通过练习提升情感风险识别和应对能力</text>
                </view>
            </view>

            <view v-if="practiceHistory.length > 0" class="practice-history">
                <text class="section-title">练习记录</text>
                <view v-for="record in practiceHistory" :key="record.id" class="history-item">
                    <view class="history-header">
                        <text class="history-title">{{ record.title }}</text>
                        <text class="history-date">{{ formatDate(record.date) }}</text>
                    </view>
                    <text class="history-result">{{ record.result }}</text>
                </view>
            </view>
        </view>

        <!-- 成长档案模块 -->
        <view v-if="activeTab === 'growth'" class="content-section">
            <view class="growth-overview">
                <view class="overview-card">
                    <text class="overview-title">学习进度</text>
                    <view class="progress-item">
                        <text class="progress-label">掌握技巧</text>
                        <view class="progress-bar">
                            <view class="progress-fill" :style="{ width: masteredSkillsProgress + '%' }"></view>
                        </view>
                        <text class="progress-text">{{ masteredSkills }}/{{ totalSkills }}</text>
                    </view>
                </view>

                <view class="overview-card">
                    <text class="overview-title">防护能力</text>
                    <view class="protection-level">
                        <text class="level-text">{{ protectionLevel }}</text>
                        <text class="level-desc">{{ protectionLevelDesc }}</text>
                    </view>
                </view>
            </view>

            <view class="growth-suggestions">
                <text class="section-title">成长建议</text>
                <view v-for="suggestion in growthSuggestions" :key="suggestion.id" class="suggestion-card">
                    <text class="suggestion-title">{{ suggestion.title }}</text>
                    <text class="suggestion-content">{{ suggestion.content }}</text>
                    <view class="suggestion-action" @click="applySuggestion(suggestion)">
                        <text class="action-text">立即行动</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api } from '../../utils/api.js';

export default {
    data() {
        return {
            activeTab: 'skills',
            recommendedSkills: [],
            skillCategories: [],
            practiceHistory: [],
            masteredSkills: 5,
            totalSkills: 20,
            protectionLevel: '良好',
            protectionLevelDesc: '你具备基本的情感防护意识',
            growthSuggestions: []
        }
    },

    computed: {
        masteredSkillsProgress() {
            return Math.round((this.masteredSkills / this.totalSkills) * 100);
        }
    },

    onLoad() {
        this.initializeData();
    },

    methods: {
        async initializeData() {
            try {
                await Promise.all([
                    this.getRecommendedSkills(),
                    this.getSkillCategories(),
                    this.loadPracticeHistory(),
                    this.loadGrowthData()
                ]);
            } catch (error) {
                console.error('初始化数据失败:', error);
                uni.showToast({
                    title: '加载数据失败',
                    icon: 'none'
                });
            }
        },

        async getRecommendedSkills() {
            try {
                uni.showLoading({ title: '获取推荐中...' });

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/recommend`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                });

                if (response.statusCode === 200) {
                    this.recommendedSkills = response.data.recommended_skills || [];
                }
            } catch (error) {
                console.error('获取推荐技巧失败:', error);
                uni.showToast({
                    title: '获取推荐失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        async getSkillCategories() {
            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/categories`,
                    method: 'GET'
                });

                if (response.statusCode === 200) {
                    this.skillCategories = response.data.categories || [];
                }
            } catch (error) {
                console.error('获取技能分类失败:', error);
            }
        },

        async generateScenario(skill) {
            try {
                uni.showLoading({ title: 'AI生成场景中...' });

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/${skill.id}/generate-scenario`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {}
                });

                if (response.statusCode === 200) {
                    const scenario = response.data.scenario;
                    this.showScenarioModal(skill, scenario);
                }
            } catch (error) {
                console.error('生成场景失败:', error);
                uni.showToast({
                    title: '生成场景失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        showScenarioModal(skill, scenario) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id}&type=scenario`
            });

            // 暂存场景数据
            uni.setStorageSync('currentScenario', {
                skill: skill,
                scenario: scenario
            });
        },

        async practiceSkill(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id}&type=practice`
            });
        },

        async startRiskAssessment() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/risk-assessment'
            });
        },

        async startScenarioSimulation() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/scenario-simulation'
            });
        },

        async getPersonalizedAdvice() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/personalized-advice'
            });
        },

        async viewEmergencyResources() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/emergency-resources'
            });
        },

        viewCategorySkills(category) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/category-skills?categoryId=${category.id}`
            });
        },

        startInteractivePractice() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/interactive-practice'
            });
        },

        startScenarioPractice() {
            this.startScenarioSimulation();
        },

        startProtectionDrill() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/protection-drill'
            });
        },

        loadPracticeHistory() {
            // 模拟练习历史数据
            this.practiceHistory = [
                {
                    id: 1,
                    title: '主动倾听练习',
                    date: new Date(),
                    result: '表现良好，建议多练习眼神交流'
                },
                {
                    id: 2,
                    title: '风险识别训练',
                    date: new Date(Date.now() - 86400000),
                    result: '识别准确率85%，继续加强'
                }
            ];
        },

        loadGrowthData() {
            // 模拟成长数据
            this.growthSuggestions = [
                {
                    id: 1,
                    title: '加强情感表达',
                    content: '建议多练习"我"开头的表达方式，能更好地传达你的感受'
                },
                {
                    id: 2,
                    title: '提升边界意识',
                    content: '学会在关系中设立清晰的边界，保护自己的情感安全'
                }
            ];
        },

        getDifficultyText(difficulty) {
            const map = {
                'basic': '基础',
                'intermediate': '进阶',
                'advanced': '高级'
            };
            return map[difficulty] || '基础';
        },

        getCategoryIcon(categoryId) {
            const icons = {
                'communication': '💬',
                'emotional_expression': '💝',
                'relationship_building': '🤝',
                'special_scenarios': '🎯'
            };
            return icons[categoryId] || '📚';
        },

        formatDate(date) {
            return new Date(date).toLocaleDateString('zh-CN');
        },

        applySuggestion(suggestion) {
            uni.showToast({
                title: '建议已收藏',
                icon: 'success'
            });
        },

        selectSkill(skill) {
            // 显示技能详情或直接进入练习
            this.practiceSkill(skill);
        }
    }
}
</script>

<style scoped>
.wisdom-container {
    padding: 0;
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60rpx 40rpx 40rpx;
    color: white;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
    margin-bottom: 10rpx;
    display: block;
}

.subtitle {
    font-size: 28rpx;
    opacity: 0.9;
}

.nav-tabs {
    display: flex;
    background-color: white;
    margin: 0;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.tab-item {
    flex: 1;
    padding: 30rpx 20rpx;
    text-align: center;
    border-bottom: 4rpx solid transparent;
    transition: all 0.3s ease;
}

.tab-item.active {
    border-bottom-color: #667eea;
    background-color: #f8f9ff;
}

.tab-icon {
    font-size: 32rpx;
    display: block;
    margin-bottom: 8rpx;
}

.tab-text {
    font-size: 24rpx;
    color: #666;
}

.tab-item.active .tab-text {
    color: #667eea;
    font-weight: bold;
}

.content-section {
    padding: 40rpx;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30rpx;
}

.section-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
}

.refresh-btn {
    display: flex;
    align-items: center;
    padding: 16rpx 24rpx;
    background-color: #667eea;
    border-radius: 40rpx;
    color: white;
}

.refresh-icon {
    font-size: 24rpx;
    margin-right: 8rpx;
}

.refresh-text {
    font-size: 24rpx;
}

.skill-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.skill-card.recommended {
    border: 2rpx solid #667eea;
    background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
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
    margin-bottom: 24rpx;
}

.skill-tag {
    background-color: #f0f0f0;
    color: #666;
    padding: 8rpx 16rpx;
    border-radius: 16rpx;
    font-size: 22rpx;
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
}

.action-btn.primary {
    background-color: #667eea;
    color: white;
}

.action-btn.secondary {
    background-color: #f0f0f0;
    color: #666;
}

.categories-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20rpx;
}

.category-card {
    width: calc(50% - 10rpx);
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.category-icon {
    font-size: 48rpx;
    display: block;
    margin-bottom: 16rpx;
}

.category-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.category-count {
    font-size: 24rpx;
    color: #999;
}

.protection-tools {
    display: flex;
    flex-direction: column;
    gap: 24rpx;
}

.tool-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.tool-header {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
}

.tool-icon {
    font-size: 36rpx;
    margin-right: 16rpx;
}

.tool-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.tool-desc {
    font-size: 28rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 24rpx;
}

.tool-btn {
    background-color: #667eea;
    color: white;
    padding: 20rpx;
    border-radius: 12rpx;
    text-align: center;
}

.practice-options {
    display: flex;
    flex-direction: column;
    gap: 24rpx;
}

.practice-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.practice-header {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
}

.practice-icon {
    font-size: 36rpx;
    margin-right: 16rpx;
}

.practice-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.practice-desc {
    font-size: 28rpx;
    color: #666;
    line-height: 1.5;
}

.growth-overview {
    display: flex;
    flex-direction: column;
    gap: 24rpx;
    margin-bottom: 40rpx;
}

.overview-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.overview-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

.progress-item {
    display: flex;
    align-items: center;
    gap: 16rpx;
}

.progress-label {
    font-size: 28rpx;
    color: #666;
}

.progress-bar {
    flex: 1;
    height: 12rpx;
    background-color: #f0f0f0;
    border-radius: 6rpx;
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
}

.protection-level {
    text-align: center;
}

.level-text {
    font-size: 48rpx;
    font-weight: bold;
    color: #4caf50;
    display: block;
    margin-bottom: 8rpx;
}

.level-desc {
    font-size: 28rpx;
    color: #666;
}

.suggestion-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.suggestion-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.suggestion-content {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 24rpx;
}

.suggestion-action {
    background-color: #667eea;
    color: white;
    padding: 20rpx;
    border-radius: 12rpx;
    text-align: center;
}
</style>