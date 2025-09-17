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
          </view>
          <text class="skill-content">{{ skill.content }}</text>
          <view class="skill-tags">
            <text v-for="tag in skill.tags" :key="tag" class="skill-tag">{{
              tag
            }}</text>
          </view>
          <view class="skill-actions">
            <view class="action-btn primary" @click.stop="practiceSkill(skill)">
              <text class="action-text">综合练习</text>
            </view>
          </view>
        </view>
      </view>

      <view class="categories-section">
        <text class="section-title">技能分类</text>
        <view class="categories-grid">
          <view v-for="category in skillCategories" :key="category.id" class="category-card"
            @click="viewCategorySkills(category)">
            <text class="category-icon">{{
              getCategoryIcon(category.id)
            }}</text>
            <text class="category-name">{{ category.name }}</text>
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
      <view class="favorites-section">
        <view class="favorites-card" @click="goToSkillFavorites">
          <view class="favorites-header">
            <text class="favorites-icon">💖</text>
            <text class="favorites-title">技能收藏</text>
            <text class="favorites-icon">💖</text>
          </view>
          <text class="favorites-desc">查看和管理你收藏的所有技能</text>
          <view class="favorites-btn">
            <text class="btn-text">进入收藏夹</text>
            <text class="arrow">→</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 回到顶部按钮 -->
    <view v-if="showBackToTop" class="back-to-top" @click="backToTop">
      <text class="back-to-top-icon">↑</text>
    </view>
  </view>
</template>

<script>
import { api } from "../../utils/api.js";

export default {
  components: {
    // 移除MoodTracker组件
  },
  data() {
    return {
      activeTab: "skills",
      recommendedSkills: [],
      skillCategories: [],
      practiceHistory: [],

      // 登录状态
      isLoggedIn: false,

      // 回到顶部相关
      showBackToTop: false,
      scrollTop: 0,
    };
  },

  computed: {
    // 移除了masteredSkillsProgress计算属性
  },

  onLoad() {
    this.checkLoginStatus();
    this.initializeData();
  },

  onPageScroll(e) {
    this.scrollTop = e.scrollTop;
    // 当滚动距离超过300px时显示回到顶部按钮
    this.showBackToTop = e.scrollTop > 30;
  },

  onUnload() {
    // 页面卸载时清理
    this.showBackToTop = false;
  },

  methods: {
    // 检查登录状态
    checkLoginStatus() {
      const token = uni.getStorageSync("access_token");
      this.isLoggedIn = !!token;
    },

    // 跳转到登录页
    goToLogin() {
      uni.navigateTo({
        url: "/pages/login/login",
      });
    },

    async initializeData() {
      try {
        await Promise.all([
          this.getRecommendedSkills(),
          this.getSkillCategories(),
          this.loadPracticeHistory(),
        ]);
      } catch (error) {
        console.error("初始化数据失败:", error);
        uni.showToast({
          title: "加载数据失败",
          icon: "none",
        });
      }
    },

    async getRecommendedSkills() {
      try {
        uni.showLoading({ title: "获取推荐中..." });

        // 使用本地技能数据随机推荐
        const allSkills = [
          {
            id: "listen_actively",
            title: "积极倾听技巧",
            content: "学习如何专注、理解并回应他人的话语，建立更深层的连接",
            tags: ["沟通", "倾听", "理解"]
          },
          {
            id: "topic_transition",
            title: "非暴力沟通",
            content: "用非批判性的方式表达需求和感受，减少冲突",
            tags: ["沟通", "和谐", "表达"]
          },
          {
            id: "emotion_sharing",
            title: "共情能力培养",
            content: "理解和感受他人情感，增进人际关系的深度",
            tags: ["理解", "情感", "连接"]
          },
          {
            id: "express_clearly",
            title: "建设性反馈",
            content: "以支持性的方式提供反馈，促进他人成长",
            tags: ["反馈", "成长", "支持"]
          },
          {
            id: "conflict_resolution",
            title: "冲突解决策略",
            content: "有效处理分歧和冲突，寻找双赢解决方案",
            tags: ["冲突", "解决", "合作"]
          },
          {
            id: "romantic_expression",
            title: "情感智力提升",
            content: "识别、理解和管理自己及他人的情感",
            tags: ["情感", "智力", "管理"]
          },
          {
            id: "boundary_setting",
            title: "边界设定技巧",
            content: "在关系中建立健康的边界，保护自己的情感安全",
            tags: ["边界", "保护", "安全"]
          },
          {
            id: "sincere_gratitude",
            title: "有效道歉方式",
            content: "真诚地承认错误并修复关系裂痕",
            tags: ["道歉", "修复", "真诚"]
          },
          {
            id: "ice_breaking",
            title: "赞美与认可",
            content: "恰当地表达欣赏和认可，增强他人的自信",
            tags: ["赞美", "认可", "鼓励"]
          },
          {
            id: "trust_building",
            title: "情感表达艺术",
            content: "以恰当的方式表达情感，增进理解",
            tags: ["表达", "情感", "艺术"]
          }
        ];

        // 随机选择3个技能进行推荐
        const shuffled = allSkills.sort(() => 0.5 - Math.random());
        this.recommendedSkills = shuffled.slice(0, 3);

      } catch (error) {
        console.error("获取推荐技巧失败:", error);
        uni.showToast({
          title: "获取推荐失败",
          icon: "none",
        });
      } finally {
        uni.hideLoading();
      }
    },

    async getSkillCategories() {
      try {
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/categories`,
          method: "GET",
        });

        if (response.statusCode === 200) {
          this.skillCategories = response.data.categories || [];
        }
      } catch (error) {
        console.error("获取技能分类失败:", error);
      }
    },

    async practiceSkill(skill) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id
          }&type=practice&skillTitle=${encodeURIComponent(
            skill.title
          )}&skillContent=${encodeURIComponent(skill.content)}&skillTags=${encodeURIComponent(
            JSON.stringify(skill.tags)
          )}&skillScenarios=${encodeURIComponent(
            JSON.stringify(skill.scenarios || [])
          )}`,
      });
    },

    async startRiskAssessment() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/risk-assessment",
      });
    },

    async startScenarioSimulation() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/scenario-simulation",
      });
    },

    async getPersonalizedAdvice() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/personalized-advice",
      });
    },

    async viewEmergencyResources() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/emergency-resources",
      });
    },

    // viewCategorySkills(category) {
    //     uni.navigateTo({
    //         url: `/pages/interpersonal-wisdom/category-skills?categoryId=${category.id}`
    //     });
    // },

    viewCategorySkills(category) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/category-detail?categoryId=${category.id
          }&name=${encodeURIComponent(category.name)}`,
      });
    },

    startInteractivePractice() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/interactive-practice",
      });
    },

    startScenarioPractice() {
      this.startScenarioSimulation();
    },

    startProtectionDrill() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/protection-drill",
      });
    },

    loadPracticeHistory() {
      // 模拟练习历史数据
      this.practiceHistory = [
        {
          id: 1,
          title: "主动倾听练习",
          date: new Date(),
          result: "表现良好，建议多练习眼神交流",
        },
        {
          id: 2,
          title: "风险识别训练",
          date: new Date(Date.now() - 86400000),
          result: "识别准确率85%，继续加强",
        },
      ];
    },

    loadGrowthData() {
      // 移除原有的成长数据加载逻辑
    },

    // 跳转到技能收藏页面
    goToSkillFavorites() {
      uni.navigateTo({
        url: '/pages/interpersonal-wisdom/skill-favorites'
      });
    },

    getCategoryIcon(categoryId) {
      const icons = {
        communication: "💬",
        emotional_expression: "💝",
        relationship_building: "🤝",
        special_scenarios: "🎯",
      };
      return icons[categoryId] || "📚";
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString("zh-CN");
    },

    applySuggestion(suggestion) {
      uni.showToast({
        title: "建议已收藏",
        icon: "success",
      });
    },

    selectSkill(skill) {
      // 显示技能详情或直接进入练习
      this.practiceSkill(skill);
    },

    // 组件事件处理方法（已移除）

    // 回到顶部方法
    backToTop() {
      uni.pageScrollTo({
        scrollTop: 0,
        duration: 300
      });
    },
  },
};
</script>

<style scoped>
.wisdom-container {
  padding: 0;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.header {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  padding: 60rpx 40rpx 60rpx;
  color: #1976d2;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.4);
}

.favorites-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400rpx;
}

.favorites-card {
  background: linear-gradient(135deg,
      rgba(255, 182, 193, 0.9) 0%,
      rgba(255, 105, 180, 0.9) 50%,
      rgba(238, 130, 238, 0.9) 100%);
  backdrop-filter: blur(10rpx);
  border-radius: 24rpx;
  padding: 48rpx 40rpx;
  text-align: center;
  box-shadow: 0 12rpx 32rpx rgba(255, 105, 180, 0.25);
  border: 3rpx solid rgba(255, 255, 255, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-width: 600rpx;
  width: 100%;
}

.favorites-card:active {
  transform: translateY(4rpx) scale(0.98);
  box-shadow: 0 8rpx 24rpx rgba(255, 105, 180, 0.35);
}

.favorites-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24rpx;
  gap: 16rpx;
}

.favorites-icon {
  font-size: 40rpx;
  animation: heartbeat 2s ease-in-out infinite;
}

.favorites-title {
  font-size: 40rpx;
  font-weight: bold;
  color: white;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.favorites-desc {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.6;
  margin-bottom: 32rpx;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.favorites-btn {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10rpx);
  color: white;
  padding: 24rpx 40rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  box-shadow: 0 4rpx 16rpx rgba(255, 255, 255, 0.2);
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.favorites-btn:active {
  transform: scale(0.95);
  background: rgba(255, 255, 255, 0.35);
}

.favorites-btn .btn-text {
  font-size: 30rpx;
  font-weight: 600;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.favorites-btn .arrow {
  font-size: 28rpx;
  font-weight: bold;
}

@keyframes heartbeat {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

.header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(227, 242, 253, 0.1);
  backdrop-filter: blur(10rpx);
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
  position: relative;
  z-index: 2;
}

.subtitle {
  font-size: 28rpx;
  opacity: 0.8;
  position: relative;
  z-index: 2;
}

.nav-tabs {
  display: flex;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10rpx);
  margin: 0 20rpx;
  border-radius: 20rpx 20rpx 0 0;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

.tab-item {
  flex: 1;
  padding: 32rpx 20rpx;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.tab-item::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 60%;
  height: 4rpx;
  background: linear-gradient(90deg, #42a5f5, #1976d2);
  border-radius: 2rpx;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-item.active::before {
  transform: translateX(-50%) scaleX(1);
}

.tab-item.active {
  background: linear-gradient(135deg,
      rgba(227, 242, 253, 0.8) 0%,
      rgba(255, 255, 255, 0.9) 100%);
}

.tab-icon {
  font-size: 32rpx;
  display: block;
  margin-bottom: 8rpx;
  transition: transform 0.3s ease;
}

.tab-item.active .tab-icon {
  transform: scale(1.1);
}

.tab-text {
  font-size: 24rpx;
  color: #666;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tab-item.active .tab-text {
  color: #1976d2;
  font-weight: 600;
}

.content-section {
  padding: 20rpx 40rpx 40rpx;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20rpx);
  margin: 0 20rpx 40rpx;
  border-radius: 0 0 32rpx 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
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
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  border-radius: 40rpx;
  color: white;
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.3);
}

.refresh-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.refresh-text {
  font-size: 24rpx;
}

.skill-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.skill-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
}

.skill-card.recommended {
  border: 2rpx solid rgba(66, 165, 245, 0.3);
  background: linear-gradient(135deg,
      rgba(227, 242, 253, 0.9) 0%,
      rgba(255, 255, 255, 0.9) 100%);
  position: relative;
}

.skill-card.recommended::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background: linear-gradient(90deg, #42a5f5, #1976d2);
  border-radius: 20rpx 20rpx 0 0;
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
  justify-content: center;
}

.action-btn {
  padding: 20rpx 40rpx;
  border-radius: 12rpx;
  text-align: center;
  min-width: 200rpx;
}

.action-btn.primary {
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  color: white;
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.3);
}

.action-btn.secondary {
  background-color: #f0f0f0;
  color: #666;
}

.categories-section {
  margin-top: 40rpx;
  position: relative;
}

.categories-section::before {
  content: "";
  position: absolute;
  top: -20rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 100rpx;
  height: 4rpx;
  background: linear-gradient(90deg, #42a5f5, #1976d2);
  border-radius: 2rpx;
  opacity: 0.3;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.category-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 28rpx;
  text-align: center;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-card:active {
  transform: translateY(2rpx) scale(0.98);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
}

.category-icon {
  font-size: 40rpx;
  display: block;
  margin-bottom: 12rpx;
}

.category-name {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  display: block;
}

.protection-tools {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.tool-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tool-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
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
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  color: white;
  padding: 20rpx;
  border-radius: 12rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.3);
  transition: all 0.3s ease;
}

.tool-btn:active {
  transform: translateY(1rpx);
  box-shadow: 0 2rpx 8rpx rgba(66, 165, 245, 0.4);
}

.btn-text {
  font-size: 28rpx;
  font-weight: 500;
}

.practice-options {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.practice-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.practice-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
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

.favorites-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400rpx;
}

.favorites-card {
  background: linear-gradient(135deg,
      rgba(255, 182, 193, 0.9) 0%,
      rgba(255, 105, 180, 0.9) 50%,
      rgba(238, 130, 238, 0.9) 100%);
  backdrop-filter: blur(10rpx);
  border-radius: 24rpx;
  padding: 48rpx 40rpx;
  text-align: center;
  box-shadow: 0 12rpx 32rpx rgba(255, 105, 180, 0.25);
  border: 3rpx solid rgba(255, 255, 255, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-width: 600rpx;
  width: 100%;
}

.favorites-card:active {
  transform: translateY(4rpx) scale(0.98);
  box-shadow: 0 8rpx 24rpx rgba(255, 105, 180, 0.35);
}

.favorites-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24rpx;
  gap: 16rpx;
}

.favorites-icon {
  font-size: 40rpx;
  animation: heartbeat 2s ease-in-out infinite;
}

.favorites-title {
  font-size: 40rpx;
  font-weight: bold;
  color: white;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.favorites-desc {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.6;
  margin-bottom: 32rpx;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.favorites-btn {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10rpx);
  color: white;
  padding: 24rpx 40rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  box-shadow: 0 4rpx 16rpx rgba(255, 255, 255, 0.2);
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.favorites-btn:active {
  transform: scale(0.95);
  background: rgba(255, 255, 255, 0.35);
}

.favorites-btn .btn-text {
  font-size: 30rpx;
  font-weight: 600;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.favorites-btn .arrow {
  font-size: 28rpx;
  font-weight: bold;
}

@keyframes heartbeat {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

@media (max-width: 750rpx) {
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12rpx;
  }

  .category-card {
    padding: 20rpx;
  }

  .category-icon {
    font-size: 36rpx;
  }

  .category-name {
    font-size: 24rpx;
  }
}

@media (max-width: 480rpx) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 16rpx;
  }
}

/* 回到顶部按钮样式 */
.back-to-top {
  position: fixed;
  right: 30rpx;
  bottom: 100rpx;
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(66, 165, 245, 0.4);
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.3);
}

.back-to-top:active {
  transform: scale(0.9);
  box-shadow: 0 4rpx 16rpx rgba(66, 165, 245, 0.6);
}

.back-to-top-icon {
  font-size: 32rpx;
  color: white;
  font-weight: bold;
  line-height: 1;
}

/* 添加动画效果 */
.back-to-top {
  animation: fadeInUp 0.3s ease-out;
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
</style>
