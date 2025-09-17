<template>
    <view class="skill-favorites-container">
        <!-- 页面标题 -->
        <view class="page-header">
            <text class="page-title">技能收藏</text>
            <text class="page-subtitle">{{ totalCount }}个已收藏的技能</text>
        </view>

        <!-- 分类筛选 -->
        <view class="category-filter">
            <scroll-view scroll-x="true" class="category-scroll">
                <view class="category-tabs">
                    <view v-for="category in categories" :key="category.id" class="category-tab"
                        :class="{ active: selectedCategory === category.id }" @click="selectCategory(category.id)">
                        <text class="category-icon">{{ category.icon }}</text>
                        <text class="category-name">{{ category.name }}</text>
                        <text class="category-count">({{ getCategoryCount(category.id) }})</text>
                    </view>
                </view>
            </scroll-view>
        </view>

        <!-- 技能列表 -->
        <view class="skills-list" v-if="filteredSkills.length > 0">
            <view v-for="skill in filteredSkills" :key="skill.skill_id" class="skill-card"
                @click="viewSkillDetail(skill)">
                <view class="skill-info">
                    <view class="skill-header">
                        <text class="skill-name">{{ skill.skill_name }}</text>
                        <view class="skill-category">
                            <text class="category-tag">{{ getCategoryName(skill.category) }}</text>
                        </view>
                    </view>
                    <text class="skill-description">{{ getSkillDescription(skill.skill_id) }}</text>
                    <view class="skill-meta">
                        <text class="favorite-time">收藏于 {{ formatTime(skill.created_at) }}</text>
                    </view>
                </view>
                <view class="skill-actions">
                    <view class="action-btn remove" @click.stop="removeFavorite(skill)">
                        <text class="action-icon">🗑️</text>
                    </view>
                    <view class="action-btn practice" @click.stop="startPractice(skill)">
                        <text class="action-text">练习</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-else>
            <text class="empty-icon">💫</text>
            <text class="empty-title">
                {{ selectedCategory === 'all' ? '还没有收藏任何技能' : '该分类下暂无收藏' }}
            </text>
            <text class="empty-subtitle">
                {{ selectedCategory === 'all' ? '去探索感兴趣的技能并收藏吧' : '可以去其他分类看看或添加新收藏' }}
            </text>
            <view class="empty-action">
                <view class="action-btn primary" @click="goToSkillList">
                    <text class="btn-text">去探索技能</text>
                </view>
            </view>
        </view>

        <!-- 加载状态 -->
        <view class="loading-state" v-if="loading">
            <text class="loading-text">加载中...</text>
        </view>
    </view>
</template>

<script>
import { getSkillById } from '@/data/skillsData.js';

export default {
    data() {
        return {
            loading: false,
            selectedCategory: 'all',
            favoriteSkills: [],
            categories: [
                { id: 'all', name: '全部', icon: '📋' },
                { id: 'communication', name: '沟通技巧', icon: '💬' },
                { id: 'emotional_expression', name: '情感表达', icon: '❤️' },
                { id: 'relationship_building', name: '关系建立', icon: '🤝' },
                { id: 'special_scenarios', name: '特殊场景', icon: '🎭' }
            ]
        };
    },

    computed: {
        totalCount() {
            return this.favoriteSkills.length;
        },

        filteredSkills() {
            if (this.selectedCategory === 'all') {
                return this.favoriteSkills;
            }
            return this.favoriteSkills.filter(skill => skill.category === this.selectedCategory);
        }
    },

    onLoad() {
        this.loadFavoriteSkills();
    },

    onShow() {
        // 页面显示时重新加载，以防其他页面有收藏状态变化
        this.loadFavoriteSkills();
    },

    methods: {
        async loadFavoriteSkills() {
            try {
                this.loading = true;
                const token = uni.getStorageSync('access_token');

                if (!token) {
                    uni.showToast({
                        title: '请先登录',
                        icon: 'none'
                    });
                    setTimeout(() => {
                        uni.navigateBack();
                    }, 1500);
                    return;
                }

                const response = await uni.request({
                    url: 'http://localhost:8000/skill-favorites/list',
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.statusCode === 200) {
                    this.favoriteSkills = response.data.favorites || [];
                } else {
                    throw new Error('获取收藏列表失败');
                }
            } catch (error) {
                console.error('加载收藏技能失败:', error);
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                });
            } finally {
                this.loading = false;
            }
        },

        selectCategory(categoryId) {
            this.selectedCategory = categoryId;
        },

        getCategoryCount(categoryId) {
            if (categoryId === 'all') return this.totalCount;
            return this.favoriteSkills.filter(skill => skill.category === categoryId).length;
        },

        getCategoryName(categoryId) {
            const category = this.categories.find(cat => cat.id === categoryId);
            return category ? category.name : categoryId;
        },

        getSkillDescription(skillId) {
            const skillData = getSkillById(skillId);
            return skillData ? skillData.brief || skillData.description : '暂无描述';
        },

        formatTime(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diffTime = now - date;
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 0) {
                return '今天';
            } else if (diffDays === 1) {
                return '昨天';
            } else if (diffDays < 7) {
                return `${diffDays}天前`;
            } else {
                return `${date.getMonth() + 1}/${date.getDate()}`;
            }
        },

        viewSkillDetail(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.skill_id}&categoryId=${skill.category}`
            });
        },

        async removeFavorite(skill) {
            try {
                const result = await new Promise((resolve) => {
                    uni.showModal({
                        title: '确认取消收藏',
                        content: `确定要取消收藏"${skill.skill_name}"吗？`,
                        success: resolve
                    });
                });

                if (!result.confirm) return;

                uni.showLoading({ title: '取消收藏中...' });

                const token = uni.getStorageSync('access_token');
                const response = await uni.request({
                    url: 'http://localhost:8000/skill-favorites/remove',
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        skill_id: skill.skill_id
                    }
                });

                if (response.statusCode === 200) {
                    // 从本地数组中移除
                    const index = this.favoriteSkills.findIndex(s => s.skill_id === skill.skill_id);
                    if (index > -1) {
                        this.favoriteSkills.splice(index, 1);
                    }

                    uni.showToast({
                        title: '取消收藏成功',
                        icon: 'success'
                    });
                } else {
                    throw new Error('取消收藏失败');
                }
            } catch (error) {
                console.error('取消收藏失败:', error);
                uni.showToast({
                    title: '操作失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        startPractice(skill) {
            const skillData = getSkillById(skill.skill_id);
            if (!skillData) {
                uni.showToast({
                    title: '技能数据加载失败',
                    icon: 'none'
                });
                return;
            }

            const skillParams = {
                skillId: skill.skill_id,
                type: "practice",
                skillTitle: encodeURIComponent(skillData.name),
                skillContent: encodeURIComponent(skillData.description),
                skillTags: encodeURIComponent(JSON.stringify(skillData.tags || [])),
                skillScenarios: encodeURIComponent(JSON.stringify(skillData.scenarios || []))
            };

            const queryString = Object.entries(skillParams)
                .map(([key, value]) => `${key}=${value}`)
                .join("&");

            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?${queryString}`
            });
        },

        goToSkillList() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/interpersonal-wisdom'
            });
        }
    }
};
</script>

<style scoped>
.skill-favorites-container {
    background-color: #f5f5f5;
    min-height: 100vh;
    padding-bottom: 40rpx;
}

.page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60rpx 40rpx 40rpx;
    color: white;
}

.page-title {
    font-size: 48rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 16rpx;
}

.page-subtitle {
    font-size: 26rpx;
    opacity: 0.9;
}

.category-filter {
    background-color: white;
    padding: 24rpx 0;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.category-scroll {
    white-space: nowrap;
}

.category-tabs {
    display: flex;
    padding: 0 40rpx;
    gap: 24rpx;
}

.category-tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16rpx 24rpx;
    border-radius: 16rpx;
    background-color: #f8f9ff;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
    white-space: nowrap;
    flex-shrink: 0;
}

.category-tab.active {
    background-color: #667eea;
    color: white;
    border-color: #667eea;
}

.category-icon {
    font-size: 32rpx;
    margin-bottom: 8rpx;
}

.category-name {
    font-size: 24rpx;
    font-weight: 500;
}

.category-count {
    font-size: 20rpx;
    opacity: 0.8;
    margin-top: 4rpx;
}

.skills-list {
    padding: 32rpx 40rpx;
}

.skill-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    transition: transform 0.2s ease;
}

.skill-card:active {
    transform: translateY(2rpx);
}

.skill-info {
    flex: 1;
    margin-right: 24rpx;
}

.skill-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16rpx;
}

.skill-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    flex: 1;
}

.skill-category {
    margin-left: 16rpx;
}

.category-tag {
    background-color: #f0f4ff;
    color: #667eea;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
    border: 1rpx solid #e0e8ff;
}

.skill-description {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 16rpx;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
    overflow: hidden;
}

.skill-meta {
    display: flex;
    align-items: center;
    gap: 16rpx;
}

.favorite-time {
    font-size: 22rpx;
    color: #999;
}

.skill-actions {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
    flex-shrink: 0;
}

.action-btn {
    padding: 12rpx 20rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 24rpx;
    transition: all 0.2s ease;
    min-width: 80rpx;
}

.action-btn:active {
    transform: scale(0.95);
}

.action-btn.remove {
    background-color: #fee;
    color: #f56565;
    border: 1rpx solid #fed7d7;
}

.action-btn.practice {
    background-color: #667eea;
    color: white;
}

.action-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 24rpx 48rpx;
    font-size: 28rpx;
}

.action-icon {
    font-size: 24rpx;
}

.action-text {
    font-size: 24rpx;
}

.btn-text {
    font-size: 28rpx;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 120rpx 40rpx;
    text-align: center;
}

.empty-icon {
    font-size: 120rpx;
    margin-bottom: 32rpx;
    opacity: 0.6;
}

.empty-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
}

.empty-subtitle {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 48rpx;
}

.empty-action {
    margin-top: 24rpx;
}

.loading-state {
    display: flex;
    justify-content: center;
    padding: 80rpx 40rpx;
}

.loading-text {
    font-size: 26rpx;
    color: #666;
}
</style>
