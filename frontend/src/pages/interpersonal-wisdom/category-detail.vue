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
            <view v-if="recommendedSkills.length > 0" class="section">
                <view class="section-header">
                    <text class="section-title">🎯 为你推荐</text>
                </view>
                <view v-for="skill in recommendedSkills" :key="skill.id" class="skill-card recommended"
                    :class="`skill-color-${skill.id % 12 + 1}`">
                    <view class="skill-header">
                        <text class="skill-title">{{ skill.name }}</text>
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
                    <view class="skills-count">
                        <text class="count-text">{{ paginationInfo.start }}-{{ paginationInfo.end }} / {{
                            paginationInfo.total }}</text>
                    </view>
                </view>

                <view class="skills-grid">
                    <view v-for="skill in filteredSkills" :key="skill.id" class="skill-card" :class="[
                        { mastered: skill.status === 'mastered', learning: skill.status === 'learning' },
                        `skill-color-${skill.id % 12 + 1}`
                    ]" @click="viewSkillDetail(skill)">

                        <text class="skill-name">{{ skill.name }}</text>
                        <text class="skill-brief">{{ skill.brief }}</text>

                        <view class="skill-tags">
                            <text v-for="tag in skill.tags" :key="tag" class="skill-tag">{{ tag }}</text>
                        </view>
                    </view>
                </view>

                <!-- 分页器 -->
                <view v-if="totalPages > 1" class="pagination">
                    <view class="pagination-info">
                        <text class="pagination-text">第 {{ currentPage }} 页，共 {{ totalPages }} 页</text>
                    </view>
                    <view class="pagination-controls">
                        <view class="pagination-btn" :class="{ disabled: currentPage <= 1 }"
                            @click="goToPage(currentPage - 1)">
                            <text class="btn-text">上一页</text>
                        </view>

                        <view class="pagination-numbers">
                            <view v-for="page in getVisiblePages()" :key="page" class="page-number"
                                :class="{ active: page === currentPage, ellipsis: page === '...' }"
                                @click="page !== '...' ? goToPage(page) : null">
                                <text class="page-text">{{ page }}</text>
                            </view>
                        </view>

                        <view class="pagination-btn" :class="{ disabled: currentPage >= totalPages }"
                            @click="goToPage(currentPage + 1)">
                            <text class="btn-text">下一页</text>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 学习建议 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">💡 学习建议</text>
                    <view class="tip-controls">
                        <view class="refresh-btn" @click="refreshTip">
                            <text class="refresh-icon">🔄</text>
                        </view>
                    </view>
                </view>
                <view class="suggestion-card">
                    <text class="suggestion-title">{{ learningTip.title }}</text>
                    <text class="suggestion-content">{{ learningTip.content }}</text>
                </view>
            </view>
        </view>

        <BackToTop ref="backToTop" :threshold="50" :bottom="40" :right="40" icon="🔝"
            @scroll-to-top-success="onScrollToTopSuccess" />
    </view>
</template>

<script>
import BackToTop from '@/components/BackToTop.vue'
import { skillsData, getSkillsByCategory, getSkillById, categories } from '@/data/skillsData.js'
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
            learningTip: {},
            learningTips: [], // 存储所有学习建议
            currentTipIndex: 0, // 当前显示的建议索引
            tipTimer: null, // 定时器
            currentPage: 1, // 当前页码
            pageSize: 5 // 每页显示的技能数量
        }
    },

    computed: {
        progressPercentage() {
            if (this.categoryData.totalSkills === 0) return 0;
            return Math.round((this.categoryData.masteredSkills / this.categoryData.totalSkills) * 100);
        },

        filteredSkills() {
            let skills = [];
            switch (this.filterType) {
                case 'learned':
                    skills = this.allSkills.filter(skill => skill.status === 'mastered');
                    break;
                case 'learning':
                    skills = this.allSkills.filter(skill => skill.status === 'learning');
                    break;
                default:
                    skills = this.allSkills;
            }

            // 计算分页
            const startIndex = (this.currentPage - 1) * this.pageSize;
            const endIndex = startIndex + this.pageSize;
            return skills.slice(startIndex, endIndex);
        },

        // 获取所有过滤后的技能（用于计算总页数）
        allFilteredSkills() {
            switch (this.filterType) {
                case 'learned':
                    return this.allSkills.filter(skill => skill.status === 'mastered');
                case 'learning':
                    return this.allSkills.filter(skill => skill.status === 'learning');
                default:
                    return this.allSkills;
            }
        },

        // 总页数
        totalPages() {
            return Math.ceil(this.allFilteredSkills.length / this.pageSize);
        },

        // 分页信息
        paginationInfo() {
            const total = this.allFilteredSkills.length;
            const start = (this.currentPage - 1) * this.pageSize + 1;
            const end = Math.min(this.currentPage * this.pageSize, total);
            return {
                total,
                start,
                end,
                current: this.currentPage,
                totalPages: this.totalPages
            };
        }
    },

    onLoad(options) {
        this.categoryId = options.categoryId;
        this.categoryName = options.name || '';
        this.loadCategoryData();
    },

    onUnload() {
        // 页面卸载时清除定时器
        this.clearTipTimer();
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
            // 使用统一的技能数据源
            const categoryData = categories[this.categoryId];
            if (!categoryData) {
                console.error('未找到分类数据:', this.categoryId);
                return;
            }

            // 获取该分类下的所有技能
            const skills = getSkillsByCategory(this.categoryId);

            // 为技能添加学习状态（模拟数据）
            const skillsWithStatus = skills.map(skill => ({
                ...skill,
                status: this.getRandomStatus(),
                progress: skill.status === 'learning' ? Math.floor(Math.random() * 100) : (skill.status === 'mastered' ? 100 : 0)
            }));

            this.categoryData = {
                ...categoryData,
                totalSkills: skills.length,
                masteredSkills: skillsWithStatus.filter(s => s.status === 'mastered').length
            };

            this.allSkills = skillsWithStatus;

            // 推荐技能（随机选择3个未掌握的技能）
            const unmastered = skillsWithStatus.filter(s => s.status !== 'mastered');
            this.recommendedSkills = unmastered
                .sort(() => 0.5 - Math.random())
                .slice(0, 3);

            // 学习建议
            this.learningTips = this.getDefaultLearningTips();
            this.learningTip = this.learningTips[0];

            // 定时轮播学习建议
            this.startTipRotation();
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

        // 随机选择一个学习建议
        getRandomTip() {
            if (this.learningTips.length === 0) return {};
            const randomIndex = Math.floor(Math.random() * this.learningTips.length);
            this.currentTipIndex = randomIndex;
            return this.learningTips[randomIndex];
        },

        // 开始定时器
        startTipTimer() {
            this.clearTipTimer(); // 先清除可能存在的定时器
            this.tipTimer = setInterval(() => {
                this.learningTip = this.getRandomTip();
            }, 30000); // 30秒更换一次
        },

        // 清除定时器
        clearTipTimer() {
            if (this.tipTimer) {
                clearInterval(this.tipTimer);
                this.tipTimer = null;
            }
        },

        // 手动刷新建议
        refreshTip() {
            this.learningTip = this.getRandomTip();
            uni.showToast({
                title: '已刷新建议',
                icon: 'success',
                duration: 1000
            });
        },

        // 跳转到指定页码
        goToPage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
        },

        // 获取可见的页码数组
        getVisiblePages() {
            const total = this.totalPages;
            const current = this.currentPage;
            const pages = [];

            if (total <= 7) {
                // 如果总页数小于等于7，显示所有页码
                for (let i = 1; i <= total; i++) {
                    pages.push(i);
                }
            } else {
                // 如果总页数大于7，显示部分页码
                if (current <= 4) {
                    // 当前页在前面
                    for (let i = 1; i <= 5; i++) {
                        pages.push(i);
                    }
                    pages.push('...');
                    pages.push(total);
                } else if (current >= total - 3) {
                    // 当前页在后面
                    pages.push(1);
                    pages.push('...');
                    for (let i = total - 4; i <= total; i++) {
                        pages.push(i);
                    }
                } else {
                    // 当前页在中间
                    pages.push(1);
                    pages.push('...');
                    for (let i = current - 1; i <= current + 1; i++) {
                        pages.push(i);
                    }
                    pages.push('...');
                    pages.push(total);
                }
            }

            return pages;
        },

        getRandomStatus() {
            const statuses = ['new', 'learning', 'mastered'];
            const weights = [0.6, 0.3, 0.1]; // 60%新技能，30%学习中，10%已掌握
            const random = Math.random();
            let sum = 0;
            for (let i = 0; i < statuses.length; i++) {
                sum += weights[i];
                if (random < sum) {
                    return statuses[i];
                }
            }
            return 'new';
        },

        getDefaultLearningTips() {
            return [
                {
                    title: '循序渐进的学习方法',
                    content: '建议从基础技能开始学习，每天练习15-20分钟，结合实际场景应用，效果更佳。'
                },
                {
                    title: '实践应用建议',
                    content: '理论学习后要及时实践，在日常生活中寻找应用机会，加深理解和记忆。'
                },
                {
                    title: '反思总结习惯',
                    content: '每次练习后进行反思总结，记录进步和需要改进的地方，持续优化。'
                },
                {
                    title: '个性化学习路径',
                    content: '根据自己的特点和需求，制定个性化的学习计划和目标。'
                },
                {
                    title: '社群学习支持',
                    content: '加入学习社群，与他人交流经验，获得支持和鼓励。'
                }
            ];
        },

        startTipRotation() {
            this.clearTipTimer();
            this.tipTimer = setInterval(() => {
                this.learningTip = this.getRandomTip();
            }, 30000);
        },

        // 设置过滤器时重置页码
        setFilter(type) {
            this.filterType = type;
            this.currentPage = 1; // 重置到第一页
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

.skills-count {
    display: flex;
    align-items: center;
}

.count-text {
    font-size: 24rpx;
    color: #666;
    background-color: #f0f0f0;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.tip-controls {
    display: flex;
    align-items: center;
    gap: 16rpx;
}

.tip-counter {
    font-size: 22rpx;
    color: #999;
    background-color: #f0f0f0;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.refresh-btn {
    padding: 8rpx;
    background-color: #667eea;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
}

.refresh-btn:active {
    transform: scale(0.95);
}

.refresh-icon {
    font-size: 20rpx;
    color: white;
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
    background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
    border-top: 2rpx solid #667eea;
    border-right: 2rpx solid #667eea;
    border-bottom: 2rpx solid #667eea;
}

.skill-card.mastered {
    border-left: 6rpx solid #4caf50;
}

.skill-card.learning {
    border-left: 6rpx solid #ff9800;
}

/* 技能卡片彩色边框样式 */
.skill-card.skill-color-1 {
    border-left: 6rpx solid #FF6B6B;
    /* 珊瑚红 */
}

.skill-card.skill-color-2 {
    border-left: 6rpx solid #4ECDC4;
    /* 青绿色 */
}

.skill-card.skill-color-3 {
    border-left: 6rpx solid #45B7D1;
    /* 天空蓝 */
}

.skill-card.skill-color-4 {
    border-left: 6rpx solid #96CEB4;
    /* 薄荷绿 */
}

.skill-card.skill-color-5 {
    border-left: 6rpx solid #FECA57;
    /* 阳光黄 */
}

.skill-card.skill-color-6 {
    border-left: 6rpx solid #FF9FF3;
    /* 粉紫色 */
}

.skill-card.skill-color-7 {
    border-left: 6rpx solid #54A0FF;
    /* 蓝紫色 */
}

.skill-card.skill-color-8 {
    border-left: 6rpx solid #5F27CD;
    /* 深紫色 */
}

.skill-card.skill-color-9 {
    border-left: 6rpx solid #00D2D3;
    /* 青蓝色 */
}

.skill-card.skill-color-10 {
    border-left: 6rpx solid #FF9F43;
    /* 橙色 */
}

.skill-card.skill-color-11 {
    border-left: 6rpx solid #10AC84;
    /* 翠绿色 */
}

.skill-card.skill-color-12 {
    border-left: 6rpx solid #EE5A6F;
    /* 玫瑰红 */
}

/* 已掌握技能的边框样式覆盖（保持原色但增加亮度） */
.skill-card.mastered.skill-color-1 {
    border-left: 6rpx solid #FF8A8A;
}

.skill-card.mastered.skill-color-2 {
    border-left: 6rpx solid #6EDED4;
}

.skill-card.mastered.skill-color-3 {
    border-left: 6rpx solid #65C7E1;
}

.skill-card.mastered.skill-color-4 {
    border-left: 6rpx solid #A6DEC4;
}

.skill-card.mastered.skill-color-5 {
    border-left: 6rpx solid #FEDA77;
}

.skill-card.mastered.skill-color-6 {
    border-left: 6rpx solid #FFAFF3;
}

.skill-card.mastered.skill-color-7 {
    border-left: 6rpx solid #74B0FF;
}

.skill-card.mastered.skill-color-8 {
    border-left: 6rpx solid #7F47DD;
}

.skill-card.mastered.skill-color-9 {
    border-left: 6rpx solid #20E2E3;
}

.skill-card.mastered.skill-color-10 {
    border-left: 6rpx solid #FFAF63;
}

.skill-card.mastered.skill-color-11 {
    border-left: 6rpx solid #30BCA4;
}

.skill-card.mastered.skill-color-12 {
    border-left: 6rpx solid #FE7A8F;
}

/* 学习中技能的边框样式（添加渐变效果） */
.skill-card.learning::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 6rpx;
    height: 100%;
    background: linear-gradient(180deg, var(--skill-color) 0%, var(--skill-color) 60%, #FFD700 100%);
    border-radius: 0 0 0 16rpx;
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

/* 分页器样式 */
.pagination {
    margin-top: 40rpx;
    padding: 24rpx;
    background-color: white;
    border-radius: 16rpx;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.pagination-info {
    text-align: center;
    margin-bottom: 20rpx;
}

.pagination-text {
    font-size: 24rpx;
    color: #666;
}

.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16rpx;
}

.pagination-btn {
    padding: 12rpx 20rpx;
    background-color: #667eea;
    color: white;
    border-radius: 8rpx;
    font-size: 24rpx;
    transition: all 0.3s ease;
}

.pagination-btn.disabled {
    background-color: #f0f0f0;
    color: #ccc;
    cursor: not-allowed;
}

.pagination-btn:not(.disabled):active {
    transform: scale(0.95);
    background-color: #5a6fd8;
}

.pagination-numbers {
    display: flex;
    gap: 8rpx;
    align-items: center;
}

.page-number {
    min-width: 64rpx;
    height: 64rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8rpx;
    font-size: 24rpx;
    transition: all 0.3s ease;
    cursor: pointer;
}

.page-number:not(.ellipsis) {
    background-color: #f8f9fa;
    color: #666;
}

.page-number.active {
    background-color: #667eea;
    color: white;
    font-weight: bold;
}

.page-number.ellipsis {
    background-color: transparent;
    color: #999;
    cursor: default;
}

.page-number:not(.active):not(.ellipsis):active {
    transform: scale(0.95);
    background-color: #e9ecef;
}

.page-text {
    font-size: 24rpx;
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

.suggestion-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20rpx;
}

.auto-refresh-hint {
    font-size: 20rpx;
    color: #999;
}

.suggestion-action {
    display: flex;
    align-items: center;
    gap: 8rpx;
    color: #667eea;
    cursor: pointer;
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