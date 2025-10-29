<template>
    <view class="category-detail-container">        <view class="content">
            <!-- 推荐技能卡片 -->
            <view v-if="recommendedSkills.length > 0" class="section">
                <view class="section-header">
                    <view class="section-title-wrapper">
                        <text class="section-title">🎯 为你推荐</text>
                        <view class="title-underline"></view>
                    </view>
                </view>
                <view class="recommended-grid">
                    <view v-for="skill in recommendedSkills" :key="skill.id" 
                          class="skill-card recommended glass-card">
                        <view class="card-shimmer"></view>
                        <view class="skill-header">
                            <text class="skill-title">{{ skill.name }}</text>
                            <view class="recommended-badge">
                                <text class="badge-text">推荐</text>
                            </view>
                        </view>
                        <text class="skill-description">{{ skill.description }}</text>
                        <view class="skill-meta">
                            <view class="meta-item">
                                <view class="meta-icon-bg">
                                    <text class="meta-icon">⏱️</text>
                                </view>
                                <text class="meta-text">{{ skill.estimatedTime }}分钟</text>
                            </view>
                        </view>
                        <view class="skill-actions">
                            <view class="action-btn primary modern-btn" @click.stop="viewSkillDetail(skill)">
                                <text class="btn-text">去看看</text>
                                <text class="btn-arrow">→</text>
                                <view class="btn-ripple"></view>
                            </view>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 技能列表部分 -->
            <view class="section">
                <view class="section-header">
                    <view class="section-title-wrapper">
                        <text class="section-title">📚 全部技能</text>
                        <view class="title-underline"></view>
                    </view>
                    <view class="skills-count modern-badge">
                        <text class="count-text">{{ paginationInfo.start }}-{{ paginationInfo.end }} / {{
                            paginationInfo.total }}</text>
                    </view>
                </view>

                <view class="skills-grid">
                    <view v-for="skill in filteredSkills" :key="skill.id" 
                          class="skill-card glass-card" 
                          :class="[
                            { mastered: skill.status === 'mastered', learning: skill.status === 'learning' }
                          ]" 
                          @click="viewSkillDetail(skill)">
                        
                        <view class="skill-content">
                            <text class="skill-name">{{ skill.name }}</text>
                            <text class="skill-brief">{{ skill.brief }}</text>

                            <view class="skill-tags">
                                <text v-for="tag in skill.tags" :key="tag" class="skill-tag modern-tag">{{ tag }}</text>
                            </view>
                        </view>
                    </view>
                </view>

                <!-- 现代化分页器 -->
                <view v-if="totalPages > 1" class="pagination glass-card">
                    <view class="pagination-info">
                        <text class="pagination-text">第 {{ currentPage }} 页，共 {{ totalPages }} 页</text>
                    </view>
                    <view class="pagination-controls">
                        <view class="pagination-btn modern-btn" 
                              :class="{ disabled: currentPage <= 1 }"
                              @click="goToPage(currentPage - 1)">
                            <text class="btn-text">上一页</text>
                            <view class="btn-ripple"></view>
                        </view>

                        <view class="pagination-numbers">
                            <view v-for="page in getVisiblePages()" :key="page" 
                                  class="page-number modern-btn"
                                  :class="{ active: page === currentPage, ellipsis: page === '...' }"
                                  @click="page !== '...' ? goToPage(page) : null">
                                <text class="page-text">{{ page }}</text>
                                <view class="btn-ripple" v-if="page !== '...'"></view>
                            </view>
                        </view>

                        <view class="pagination-btn modern-btn" 
                              :class="{ disabled: currentPage >= totalPages }"
                              @click="goToPage(currentPage + 1)">
                            <text class="btn-text">下一页</text>
                            <view class="btn-ripple"></view>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 学习建议部分 -->
            <view class="section">
                <view class="section-header">
                    <view class="section-title-wrapper">
                        <text class="section-title">💡 学习建议</text>
                        <view class="title-underline"></view>
                    </view>
                    <view class="tip-controls">
                        <view class="refresh-btn modern-btn" @click="refreshTip">
                            <text class="refresh-icon">🔄</text>
                            <view class="btn-ripple"></view>
                        </view>
                    </view>
                </view>
                <view class="suggestion-card glass-card">
                    <view class="suggestion-header">
                        <text class="suggestion-title">{{ learningTip.title }}</text>
                        <view class="suggestion-icon">💡</view>
                    </view>
                    <text class="suggestion-content">{{ learningTip.content }}</text>
                    <view class="suggestion-decoration"></view>
                </view>
            </view>
        </view>

        <BackToTop ref="backToTop" :threshold="50" :bottom="40" :right="40"
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
/* 浅蓝色现代化设计系统 */
.category-detail-container {
    background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #f5f9ff 100%);
    min-height: 100vh;
    position: relative;
}

.category-detail-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(135, 206, 235, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(173, 216, 230, 0.08) 0%, transparent 50%);
    pointer-events: none;
}

/* 玻璃拟态效果 - 浅蓝色主题 */
.glass-card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(173, 216, 230, 0.3);
    border-radius: 24rpx;
    box-shadow: 
        0 8rpx 32rpx rgba(135, 206, 235, 0.15),
        0 2rpx 8rpx rgba(173, 216, 230, 0.1);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3rpx;
    background: linear-gradient(90deg, #87ceeb 0%, #add8e6 50%, #b0e0e6 100%);
    opacity: 0.8;
}

/* 内容区域 */
.content {
    padding: 60rpx 32rpx 120rpx;
    position: relative;
    z-index: 1;
}

.section {
    margin-bottom: 48rpx;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32rpx;
    padding-top: 24rpx;
}

.section-title-wrapper {
    position: relative;
}

.section-title {
    font-size: 36rpx;
    font-weight: 700;
    color: #2c3e50;
    background: linear-gradient(135deg, #4682b4 0%, #87ceeb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.title-underline {
    position: absolute;
    bottom: -8rpx;
    left: 0;
    width: 60rpx;
    height: 4rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 2rpx;
}

/* 现代化徽章 - 浅蓝色主题 */
.modern-badge {
    background: rgba(135, 206, 235, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(173, 216, 230, 0.3);
    border-radius: 20rpx;
    padding: 8rpx 16rpx;
}

.skills-count.modern-badge .count-text {
    font-size: 24rpx;
    color: #4682b4;
    font-weight: 600;
    background: none;
    padding: 0;
}

/* 推荐技能网格 */
.recommended-grid {
    display: grid;
    gap: 24rpx;
}

/* 现代化技能卡片 */
.skill-card {
    padding: 32rpx;
    margin-bottom: 24rpx;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.skill-card:hover {
    transform: translateY(-4rpx);
    box-shadow: 
        0 12rpx 40rpx rgba(135, 206, 235, 0.2),
        0 4rpx 12rpx rgba(173, 216, 230, 0.15);
}

.skill-card:active {
    transform: translateY(-2rpx);
}

/* 推荐技能特殊样式 */
.skill-card.recommended {
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.15) 0%, rgba(255, 255, 255, 0.85) 100%);
    border: 2px solid rgba(173, 216, 230, 0.4);
}

.recommended-badge {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
    font-weight: 600;
    box-shadow: 0 2rpx 8rpx rgba(135, 206, 235, 0.3);
}

.badge-text {
    font-size: 20rpx;
    font-weight: 600;
}

/* 技能状态 - 浅蓝色主题 */
.skill-card {
    border-left: 6rpx solid #87ceeb;
}

.skill-card.mastered {
    border-left: 6rpx solid #4682b4;
    background: linear-gradient(135deg, rgba(70, 130, 180, 0.1) 0%, rgba(255, 255, 255, 0.85) 100%);
}

.skill-card.learning {
    border-left: 6rpx solid #87ceeb;
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(255, 255, 255, 0.85) 100%);
}

/* 技能内容 */
.skill-content {
    position: relative;
    z-index: 2;
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16rpx;
}

.skill-title,
.skill-name {
    font-size: 32rpx;
    font-weight: 700;
    color: #2c3e50;
    line-height: 1.4;
    flex: 1;
    margin-right: 16rpx;
}

.skill-description,
.skill-brief {
    font-size: 26rpx;
    color: #5a6c7d;
    line-height: 1.6;
    margin-bottom: 20rpx;
    font-weight: 400;
}

/* 技能元信息 */
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

.meta-icon-bg {
    width: 32rpx;
    height: 32rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2rpx 8rpx rgba(135, 206, 235, 0.3);
}

.meta-icon {
    font-size: 16rpx;
    color: #2c3e50;
}

.meta-text {
    font-size: 22rpx;
    color: #7f8c8d;
    font-weight: 500;
}

/* 现代化标签 - 浅蓝色主题 */
.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    margin-bottom: 24rpx;
}

.modern-tag {
    background: linear-gradient(135deg, rgba(173, 216, 230, 0.2) 0%, rgba(176, 224, 230, 0.15) 100%);
    border: 1px solid rgba(70, 130, 180, 0.2);
    color: #4682b4;
    padding: 6rpx 12rpx;
    border-radius: 16rpx;
    font-size: 20rpx;
    font-weight: 500;
    backdrop-filter: blur(10px);
}

/* 现代化按钮 */
.modern-btn {
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    border: none;
    cursor: pointer;
}

.btn-ripple {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.3s ease, height 0.3s ease;
}

.modern-btn:active .btn-ripple {
    width: 200rpx;
    height: 200rpx;
}

/* 技能操作按钮 */
.skill-actions {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16rpx;
}

.action-btn {
    padding: 16rpx 32rpx;
    border-radius: 16rpx;
    text-align: center;
    font-size: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8rpx;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.action-btn.primary {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    box-shadow: 0 8rpx 16rpx rgba(135, 206, 235, 0.3);
}

.action-btn.primary:hover {
    box-shadow: 0 12rpx 24rpx rgba(135, 206, 235, 0.4);
    transform: translateY(-2rpx);
}

.btn-text {
    font-size: 26rpx;
    font-weight: 600;
    position: relative;
    z-index: 2;
}

.btn-arrow {
    font-size: 20rpx;
    opacity: 0.8;
    transition: transform 0.3s ease;
    position: relative;
    z-index: 2;
}

.action-btn:active .btn-arrow {
    transform: translateX(4rpx);
}

/* 技能网格 */
.skills-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24rpx;
}

/* 现代化分页器 - 浅蓝色主题 */
.pagination {
    margin-top: 40rpx;
    padding: 32rpx;
    text-align: center;
}

.pagination-info {
    margin-bottom: 24rpx;
}

.pagination-text {
    font-size: 26rpx;
    color: #5a6c7d;
    font-weight: 500;
}

.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16rpx;
}

.pagination-btn {
    padding: 12rpx 24rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    border-radius: 12rpx;
    font-size: 24rpx;
    font-weight: 600;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
}

.pagination-btn.disabled {
    background: rgba(149, 165, 166, 0.3);
    color: #7f8c8d;
    cursor: not-allowed;
    box-shadow: 0 2rpx 8rpx rgba(149, 165, 166, 0.1);
}

.pagination-btn:not(.disabled):hover {
    transform: translateY(-2rpx);
    box-shadow: 0 8rpx 16rpx rgba(135, 206, 235, 0.4);
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
    border-radius: 12rpx;
    font-size: 24rpx;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.page-number:not(.ellipsis) {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(173, 216, 230, 0.3);
    color: #4682b4;
}

.page-number.active {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    font-weight: 700;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
}

.page-number.ellipsis {
    background: transparent;
    color: #7f8c8d;
    cursor: default;
}

.page-number:not(.active):not(.ellipsis):hover {
    background: rgba(135, 206, 235, 0.1);
    transform: translateY(-2rpx);
}

.page-text {
    font-size: 24rpx;
    position: relative;
    z-index: 2;
}

/* 学习建议卡片 - 浅蓝色主题 */
.suggestion-card {
    padding: 32rpx;
    position: relative;
    overflow: hidden;
}

.suggestion-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
}

.suggestion-title {
    font-size: 30rpx;
    font-weight: 700;
    color: #2c3e50;
    flex: 1;
}

.suggestion-icon {
    font-size: 32rpx;
    opacity: 0.7;
    color: #87ceeb;
}

.suggestion-content {
    font-size: 26rpx;
    color: #5a6c7d;
    line-height: 1.7;
    margin-bottom: 20rpx;
    font-weight: 400;
}

.suggestion-decoration {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 120rpx;
    height: 120rpx;
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    transform: translate(50%, 50%);
}

/* 刷新按钮 - 浅蓝色主题 */
.refresh-btn {
    width: 56rpx;
    height: 56rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
}

.refresh-btn:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 8rpx 16rpx rgba(135, 206, 235, 0.4);
}

.refresh-btn:active {
    transform: scale(0.95);
}

.refresh-icon {
    font-size: 24rpx;
    color: #2c3e50;
    position: relative;
    z-index: 2;
    font-weight: 600;
}

/* 响应式设计 */
@media (min-width: 750rpx) {
    .skills-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .recommended-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1200rpx) {
    .skills-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .recommended-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 8rpx;
}

::-webkit-scrollbar-track {
    background: rgba(236, 240, 241, 0.3);
    border-radius: 4rpx;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 4rpx;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #6bb6cd 0%, #98d4e0 100%);
}

/* 文字选择样式 */
::selection {
    background: rgba(135, 206, 235, 0.3);
    color: #2c3e50;
}

/* 焦点样式 */
*:focus {
    outline: none;
}

/* 加载状态 */
.loading {
    opacity: 0.7;
    pointer-events: none;
}

/* 动画增强 */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20rpx);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(10rpx);
}
</style>