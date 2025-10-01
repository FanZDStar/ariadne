<template>
  <view class="wisdom-container">
    <view class="header">
      <text class="title">人际智慧</text>
      <text class="subtitle">提升交往技能，保护情感安全</text>
    </view>

    <view class="nav-tabs">
      <view
        class="tab-item"
        :class="{ active: activeTab === 'skills' }"
        @click="activeTab = 'skills'"
      >
        <text class="tab-icon">🤝</text>
        <text class="tab-text">技能学习</text>
      </view>
      <view
        class="tab-item"
        :class="{ active: activeTab === 'protection' }"
        @click="activeTab = 'protection'"
      >
        <text class="tab-icon">🛡️</text>
        <text class="tab-text">防护指南</text>
      </view>
      <view
        class="tab-item"
        :class="{ active: activeTab === 'practice' }"
        @click="activeTab = 'practice'"
      >
        <text class="tab-icon">🎭</text>
        <text class="tab-text">实战练习</text>
      </view>
      <view
        class="tab-item"
        :class="{ active: activeTab === 'growth' }"
        @click="activeTab = 'growth'"
      >
        <text class="tab-icon">📈</text>
        <text class="tab-text">成长档案</text>
      </view>
    </view>

    <!-- 技能学习模块 -->
    <view v-if="activeTab === 'skills'" class="content-section">
      <view class="section-header">
        <view class="refresh-btn" @click="getRecommendedSkills">
          <text class="refresh-icon">🔄</text>
          <text class="refresh-text">刷新推荐</text>
        </view>
      </view>

      <view v-if="recommendedSkills.length > 0" class="recommended-skills">
        <view
          v-for="skill in recommendedSkills"
          :key="skill.id"
          class="skill-card recommended"
          @click="selectSkill(skill)"
        >
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
          <view
            v-for="category in skillCategories"
            :key="category.id"
            class="category-card"
            @click="viewCategorySkills(category)"
          >
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
      <view class="recommended-protection">
        <view class="skill-card recommended" @click="startRiskAssessment">
          <view class="skill-header">
            <text class="skill-title">关系健康评估</text>
          </view>
          <text class="skill-content"
            >评估你当前关系的健康状况，识别潜在风险</text
          >
          <view class="skill-tags">
            <text class="skill-tag">评估</text>
            <text class="skill-tag">健康</text>
            <text class="skill-tag">风险识别</text>
          </view>
          <view class="skill-actions">
            <view class="action-btn primary" @click.stop="startRiskAssessment">
              <text class="action-text">开始评估</text>
            </view>
          </view>
        </view>

        <view class="skill-card recommended" @click="getPersonalizedAdvice">
          <view class="skill-header">
            <text class="skill-title">个性化建议</text>
          </view>
          <text class="skill-content"
            >获取针对你情况的专属防护建议，提升安全意识</text
          >
          <view class="skill-tags">
            <text class="skill-tag">建议</text>
            <text class="skill-tag">个性化</text>
            <text class="skill-tag">防护</text>
          </view>
          <view class="skill-actions">
            <view
              class="action-btn primary"
              @click.stop="getPersonalizedAdvice"
            >
              <text class="action-text">获取建议</text>
            </view>
          </view>
        </view>

        <view class="skill-card recommended" @click="viewEmergencyResources">
          <view class="skill-header">
            <text class="skill-title">应急资源</text>
          </view>
          <text class="skill-content"
            >查看专业求助渠道和应急联系方式，关键时刻获得帮助</text
          >
          <view class="skill-tags">
            <text class="skill-tag">应急</text>
            <text class="skill-tag">求助</text>
            <text class="skill-tag">资源</text>
          </view>
          <view class="skill-actions">
            <view
              class="action-btn primary"
              @click.stop="viewEmergencyResources"
            >
              <text class="action-text">查看资源</text>
            </view>
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
            <text class="practice-title">AI情景模拟训练</text>
          </view>
          <text class="practice-desc">与AI进行模拟对话，练习交往技巧</text>
        </view>

        <!-- <view class="practice-card" @click="startScenarioPractice">
          <view class="practice-header">
            <text class="practice-icon">🎬</text>
            <text class="practice-title">情景模拟练习</text>
          </view>
          <text class="practice-desc">在模拟情景中练习应对各种社交场合</text>
        </view> -->

        <view class="practice-card" @click="startProtectionDrill">
          <view class="practice-header">
            <text class="practice-icon">🛡️</text>
            <text class="practice-title">防护技能训练</text>
          </view>
          <text class="practice-desc">通过练习提升情感风险识别和应对能力</text>
        </view>
      </view>

      <!-- <view v-if="practiceHistory.length > 0" class="practice-history">
        <text class="section-title">练习记录</text>
        <view v-for="record in practiceHistory" :key="record.id" class="history-item">
          <view class="history-header">
            <text class="history-title">{{ record.title }}</text>
            <text class="history-date">{{ formatDate(record.date) }}</text>
          </view>
          <text class="history-result">{{ record.result }}</text>
        </view>
      </view> -->
    </view>

    <!-- 成长档案模块 -->
    <view v-if="activeTab === 'growth'" class="content-section">
      <view class="recommended-growth">
        <view class="skill-card recommended" @click="goToSkillFavorites">
          <view class="skill-header">
            <text class="skill-title">技能收藏</text>
          </view>
          <text class="skill-content"
            >查看和管理你收藏的所有技能，随时回顾学习进度</text
          >
          <view class="skill-tags">
            <text class="skill-tag">收藏</text>
            <text class="skill-tag">管理</text>
            <text class="skill-tag">回顾</text>
          </view>
          <view class="skill-actions">
            <view class="action-btn primary" @click.stop="goToSkillFavorites">
              <text class="action-text">进入收藏夹</text>
            </view>
          </view>
        </view>

        <view class="skill-card recommended" @click="goToAssessmentReports">
          <view class="skill-header">
            <text class="skill-title">测试报告解读</text>
          </view>
          <text class="skill-content"
            >查看历史评估报告和AI分析建议，了解关系健康状况</text
          >
          <view class="skill-tags">
            <text class="skill-tag">报告</text>
            <text class="skill-tag">分析</text>
            <text class="skill-tag">建议</text>
          </view>
          <view class="skill-actions">
            <view
              class="action-btn primary"
              @click.stop="goToAssessmentReports"
            >
              <text class="action-text">查看报告</text>
            </view>
          </view>
        </view>

        <view class="skill-card recommended" @click="testClick">
          <view class="skill-header">
            <text class="skill-title">历史对话记录</text>
          </view>
          <text class="skill-content"
            >查看所有AI对话练习记录，回顾学习成果和改进建议</text
          >
          <view class="skill-tags">
            <text class="skill-tag">对话</text>
            <text class="skill-tag">练习</text>
            <text class="skill-tag">历史</text>
          </view>
          <view class="skill-actions">
            <view class="action-btn primary" @click.stop="goToPracticeHistory">
              <text class="action-text">查看记录</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 回到顶部按钮 -->
    <BackToTop
      ref="backToTop"
      :threshold="100"
      :bottom="100"
      :right="30"
      @start-scroll-listener="onStartScrollListener"
      @remove-scroll-listener="onRemoveScrollListener"
      @scroll-to-top-success="onScrollToTopSuccess"
    />
  </view>
</template>

<script>
import { api } from "../../utils/api.js";
import BackToTop from "@/components/BackToTop.vue";

export default {
  components: {
    BackToTop,
  },
  data() {
    return {
      activeTab: "skills",
      recommendedSkills: [],
      skillCategories: [],
      practiceHistory: [],

      // 登录状态
      isLoggedIn: false,
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
    // 将滚动事件传递给BackToTop组件
    if (this.$refs.backToTop) {
      this.$refs.backToTop.updateVisibility(e.scrollTop);
    }
  },

  onUnload() {
    // 页面卸载时的清理工作
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
            tags: ["沟通", "倾听", "理解"],
          },
          {
            id: "topic_transition",
            title: "非暴力沟通",
            content: "用非批判性的方式表达需求和感受，减少冲突",
            tags: ["沟通", "和谐", "表达"],
          },
          {
            id: "emotion_sharing",
            title: "共情能力培养",
            content: "理解和感受他人情感，增进人际关系的深度",
            tags: ["理解", "情感", "连接"],
          },
          {
            id: "express_clearly",
            title: "建设性反馈",
            content: "以支持性的方式提供反馈，促进他人成长",
            tags: ["反馈", "成长", "支持"],
          },
          {
            id: "conflict_resolution",
            title: "冲突解决策略",
            content: "有效处理分歧和冲突，寻找双赢解决方案",
            tags: ["冲突", "解决", "合作"],
          },
          {
            id: "romantic_expression",
            title: "情感智力提升",
            content: "识别、理解和管理自己及他人的情感",
            tags: ["情感", "智力", "管理"],
          },
          {
            id: "boundary_setting",
            title: "边界设定技巧",
            content: "在关系中建立健康的边界，保护自己的情感安全",
            tags: ["边界", "保护", "安全"],
          },
          {
            id: "sincere_gratitude",
            title: "有效道歉方式",
            content: "真诚地承认错误并修复关系裂痕",
            tags: ["道歉", "修复", "真诚"],
          },
          {
            id: "ice_breaking",
            title: "赞美与认可",
            content: "恰当地表达欣赏和认可，增强他人的自信",
            tags: ["赞美", "认可", "鼓励"],
          },
          {
            id: "trust_building",
            title: "情感表达艺术",
            content: "以恰当的方式表达情感，增进理解",
            tags: ["表达", "情感", "艺术"],
          },
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
        url: `/pages/interpersonal-wisdom/skill-practice?skillId=${
          skill.id
        }&type=practice&skillTitle=${encodeURIComponent(
          skill.title
        )}&skillContent=${encodeURIComponent(
          skill.content
        )}&skillTags=${encodeURIComponent(
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

    refreshProtectionTools() {
      uni.showToast({
        title: "防护工具已刷新",
        icon: "success",
      });
    },

    refreshGrowthTools() {
      uni.showToast({
        title: "成长工具已刷新",
        icon: "success",
      });
    },

    // viewCategorySkills(category) {
    //     uni.navigateTo({
    //         url: `/pages/interpersonal-wisdom/category-skills?categoryId=${category.id}`
    //     });
    // },

    viewCategorySkills(category) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/category-detail?categoryId=${
          category.id
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
        url: "/pages/interpersonal-wisdom/skill-favorites",
      });
    },

    // 跳转到关系健康测试报告页面
    goToAssessmentReports() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/assessment-reports",
      });
    },

    // 测试点击事件
    testClick() {
      console.log("测试点击事件触发");
      uni.showToast({
        title: "点击成功!",
        icon: "success",
      });

      // 调用跳转方法
      this.goToPracticeHistory();
    },

    // 跳转到历史对话记录页面
    goToPracticeHistory() {
      console.log("点击了历史对话记录");

      // 先显示提示，确认方法被调用
      uni.showToast({
        title: "正在跳转...",
        icon: "loading",
        duration: 1000,
      });

      setTimeout(() => {
        uni.navigateTo({
          url: "/pages/interpersonal-wisdom/practice-history",
          fail: (err) => {
            console.error("跳转失败:", err);
            uni.showToast({
              title: "页面跳转失败",
              icon: "none",
            });
          },
          success: () => {
            console.log("跳转成功");
          },
        });
      }, 500);
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

    // 组件事件处理方法
    onStartScrollListener() {
      // 组件已挂载，准备接收滚动事件
    },

    onRemoveScrollListener() {
      // 组件将要销毁
    },

    onScrollToTopSuccess() {
      console.log("回到顶部成功");
    },
  },
};
</script>

<style scoped>
.wisdom-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* 顶部装饰背景 */
.wisdom-container::before {
  content: "";
  position: absolute;
  top: -150rpx;
  left: -100rpx;
  right: -100rpx;
  height: 500rpx;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #e8f4fd 100%);
  border-radius: 0 0 60% 40%;
  opacity: 0.4;
  z-index: 0;
}

/* 头部区域 */
.header {
  position: relative;
  padding: 80rpx 40rpx 40rpx;
  text-align: center;
  overflow: hidden;
  z-index: 1;
}

.title {
  font-size: 56rpx;
  font-weight: 700;
  color: #1565c0;
  text-shadow: 0 2rpx 8rpx rgba(21, 101, 192, 0.1);
  display: block;
  margin-bottom: 18rpx;
  letter-spacing: 3rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #1976d2;
  line-height: 1.6;
  opacity: 0.8;
  font-weight: 400;
}

/* 导航标签 */
.nav-tabs {
  display: flex;
  background: linear-gradient(135deg, #fff 0%, #f8fbff 100%);
  backdrop-filter: blur(20rpx);
  margin: 0 40rpx 20rpx;
  border-radius: 28rpx;
  box-shadow: 0 8rpx 32rpx rgba(21, 101, 192, 0.08),
    inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 1;
  border: 2rpx solid rgba(227, 242, 253, 0.6);
}

.tab-item {
  flex: 1;
  padding: 28rpx 16rpx;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  border-radius: 28rpx;
}

.tab-item::before {
  content: "";
  position: absolute;
  bottom: 8rpx;
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
  background: linear-gradient(135deg, #e3f2fd 0%, #f8fbff 100%);
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.15);
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
  color: #1565c0;
  font-weight: 600;
}

/* 内容区域 */
.content-section {
  padding: 30rpx 40rpx 40rpx;
  position: relative;
  z-index: 1;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #1565c0;
  letter-spacing: 1rpx;
}

.refresh-btn {
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 28rpx;
  color: #1565c0;
  box-shadow: 0 4rpx 12rpx rgba(21, 101, 192, 0.2);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  transition: all 0.3s ease;
}

.refresh-btn:active {
  transform: scale(0.95);
  box-shadow: 0 2rpx 8rpx rgba(21, 101, 192, 0.3);
}

.refresh-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.refresh-text {
  font-size: 24rpx;
  font-weight: 500;
}

/* 技能卡片 */
.recommended-skills {
  margin-bottom: 40rpx;
}

.recommended-protection {
  margin-bottom: 40rpx;
}

.recommended-growth {
  margin-bottom: 40rpx;
}

.skill-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 50%, #f3f8ff 100%);
  backdrop-filter: blur(10rpx);
  border-radius: 32rpx;
  padding: 36rpx;
  margin-bottom: 28rpx;
  box-shadow: 0 12rpx 40rpx rgba(21, 101, 192, 0.12),
    0 4rpx 16rpx rgba(21, 101, 192, 0.08);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.skill-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(248, 251, 255, 0.4) 0%,
    rgba(227, 242, 253, 0.2) 50%,
    rgba(243, 248, 255, 0.4) 100%
  );
  border-radius: 32rpx;
  z-index: 0;
}

.skill-card:active {
  transform: translateY(6rpx);
  box-shadow: 0 8rpx 25rpx rgba(21, 101, 192, 0.15),
    0 2rpx 8rpx rgba(21, 101, 192, 0.1);
}

.skill-card.recommended {
  border: 2rpx solid rgba(66, 165, 245, 0.4);
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 50%, #e8f4fd 100%);
}

.skill-card.recommended::before {
  background: linear-gradient(
    135deg,
    rgba(232, 244, 253, 0.5) 0%,
    rgba(227, 242, 253, 0.3) 50%,
    rgba(248, 251, 255, 0.5) 100%
  );
}

.skill-header,
.tool-header,
.practice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  position: relative;
  z-index: 1;
}

.skill-title,
.tool-title,
.practice-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #1565c0;
  letter-spacing: 1rpx;
}

.skill-content,
.tool-desc,
.practice-desc {
  font-size: 26rpx;
  color: #1976d2;
  line-height: 1.6;
  margin-bottom: 20rpx;
  opacity: 0.8;
  position: relative;
  z-index: 1;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 24rpx;
  position: relative;
  z-index: 1;
}

.skill-tag {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  font-weight: 500;
  border: 1rpx solid rgba(227, 242, 253, 0.8);
  box-shadow: 0 2rpx 8rpx rgba(21, 101, 192, 0.1);
}

.skill-actions {
  display: flex;
  gap: 16rpx;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.action-btn {
  padding: 20rpx 40rpx;
  border-radius: 28rpx;
  text-align: center;
  min-width: 200rpx;
  transition: all 0.3s ease;
  backdrop-filter: blur(10rpx);
  border: 2rpx solid transparent;
}

.action-btn.primary {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(66, 165, 245, 0.3);
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.action-btn.primary:active {
  transform: scale(0.95);
  box-shadow: 0 2rpx 8rpx rgba(66, 165, 245, 0.4);
}

.action-btn.secondary {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  box-shadow: 0 4rpx 12rpx rgba(21, 101, 192, 0.15);
}

.action-text,
.btn-text {
  font-size: 28rpx;
  font-weight: 500;
}

/* 分类区域 */
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
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
  backdrop-filter: blur(10rpx);
  border-radius: 28rpx;
  padding: 32rpx;
  text-align: center;
  box-shadow: 0 8rpx 24rpx rgba(21, 101, 192, 0.08),
    0 4rpx 12rpx rgba(21, 101, 192, 0.05);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.category-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(248, 251, 255, 0.4) 0%,
    rgba(227, 242, 253, 0.2) 100%
  );
  border-radius: 28rpx;
  z-index: 0;
}

.category-card:active {
  transform: translateY(4rpx) scale(0.98);
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.12),
    0 2rpx 8rpx rgba(21, 101, 192, 0.08);
}

.category-icon,
.tool-icon,
.practice-icon {
  font-size: 40rpx;
  display: block;
  margin-bottom: 12rpx;
  position: relative;
  z-index: 1;
}

.category-name {
  font-size: 26rpx;
  font-weight: 600;
  color: #1565c0;
  display: block;
  position: relative;
  z-index: 1;
  letter-spacing: 1rpx;
}

/* 练习选项 */
.practice-options {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.practice-card,
.tool-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 50%, #f3f8ff 100%);
  backdrop-filter: blur(10rpx);
  border-radius: 32rpx;
  padding: 36rpx;
  box-shadow: 0 12rpx 40rpx rgba(21, 101, 192, 0.12),
    0 4rpx 16rpx rgba(21, 101, 192, 0.08);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.practice-card::before,
.tool-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(248, 251, 255, 0.4) 0%,
    rgba(227, 242, 253, 0.2) 50%,
    rgba(243, 248, 255, 0.4) 100%
  );
  border-radius: 32rpx;
  z-index: 0;
}

.practice-card:active,
.tool-card:active {
  transform: translateY(6rpx);
  box-shadow: 0 8rpx 25rpx rgba(21, 101, 192, 0.15),
    0 2rpx 8rpx rgba(21, 101, 192, 0.1);
}

.tool-btn {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  color: white;
  padding: 24rpx;
  border-radius: 28rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(66, 165, 245, 0.3);
  transition: all 0.3s ease;
  border: 2rpx solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10rpx);
}

.tool-btn:active {
  transform: scale(0.95);
  box-shadow: 0 2rpx 8rpx rgba(66, 165, 245, 0.4);
}

/* 底部装饰 */
.wisdom-container::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 200rpx;
  background: linear-gradient(
    135deg,
    rgba(227, 242, 253, 0.1) 0%,
    rgba(248, 251, 255, 0.1) 100%
  );
  border-radius: 50% 50% 0 0;
  pointer-events: none;
  z-index: 0;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .header {
    padding: 60rpx 30rpx 30rpx;
  }

  .title {
    font-size: 48rpx;
    letter-spacing: 2rpx;
  }

  .subtitle {
    font-size: 26rpx;
  }

  .content-section {
    padding: 20rpx 30rpx 30rpx;
  }

  .nav-tabs {
    margin: 0 30rpx 20rpx;
  }

  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
  }

  .category-card {
    padding: 24rpx;
  }

  .category-icon {
    font-size: 36rpx;
  }

  .category-name {
    font-size: 24rpx;
  }

  .skill-card,
  .practice-card,
  .tool-card {
    padding: 32rpx;
    margin-bottom: 24rpx;
  }

  .skill-title,
  .tool-title,
  .practice-title {
    font-size: 30rpx;
  }

  .skill-content,
  .tool-desc,
  .practice-desc {
    font-size: 24rpx;
  }

  .action-btn {
    padding: 18rpx 32rpx;
    min-width: 160rpx;
  }

  .action-text,
  .btn-text {
    font-size: 26rpx;
  }
}

@media (max-width: 480rpx) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 16rpx;
  }

  .nav-tabs {
    margin: 0 20rpx 20rpx;
  }

  .tab-item {
    padding: 24rpx 12rpx;
  }

  .tab-icon {
    font-size: 28rpx;
  }

  .tab-text {
    font-size: 22rpx;
  }
}

/* 大屏幕适配 */
@media (min-width: 1200rpx) {
  .content-section {
    max-width: 1000rpx;
    margin: 0 auto;
    padding: 30rpx 40rpx 40rpx;
  }

  .header {
    max-width: 1000rpx;
    margin: 0 auto;
  }

  .nav-tabs {
    max-width: 1000rpx;
    margin: 0 auto 20rpx;
  }

  .categories-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24rpx;
  }
}
</style>
