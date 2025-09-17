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
        <text class="section-title">智能推荐技巧</text>
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
            <view class="difficulty-badge" :class="skill.difficulty">
              <text class="difficulty-text">{{
                getDifficultyText(skill.difficulty)
              }}</text>
            </view>
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
        <view
          v-for="record in practiceHistory"
          :key="record.id"
          class="history-item"
        >
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
          <text class="overview-title">心情晴雨表</text>

          <!-- 7天心情表格 - 移到上面 -->
          <view class="weekly-mood">
            <text class="section-subtitle">最近7天心情记录</text>
            <view class="mood-table-container">
              <!-- 第一行：日期 -->
              <view class="table-row dates-row">
                <view class="table-cell header-cell">日期</view>
                <view
                  v-for="(date, index) in weeklyMoodData.dates"
                  :key="'date-' + index"
                  class="table-cell date-cell"
                >
                  {{ formatShortDate(date) }}
                </view>
              </view>
              <!-- 第二行：心情评分 -->
              <view class="table-row levels-row">
                <view class="table-cell header-cell">心情</view>
                <view
                  v-for="(level, index) in weeklyMoodData.levels"
                  :key="'level-' + index"
                  class="table-cell level-cell"
                  :class="{ 'has-data': level }"
                >
                  {{ level ? getMoodIcon(level) : "--" }}
                </view>
              </view>
            </view>
          </view>

          <!-- 心情打分按钮 - 移到下面 -->
          <view class="mood-rating-section">
            <text class="rating-label">今天的心情如何？给自己打个分吧</text>

            <!-- 未登录提示 -->
            <view v-if="!isLoggedIn" class="login-prompt">
              <text class="prompt-text">请先登录以记录心情</text>
              <view class="login-btn" @click="goToLogin">
                <text class="login-text">去登录</text>
              </view>
            </view>

            <!-- 已登录时的心情选择 -->
            <template v-else>
              <view class="mood-buttons">
                <view
                  v-for="level in [1, 2, 3, 4, 5]"
                  :key="level"
                  class="mood-btn"
                  :class="{ active: selectedMood === level }"
                  @click="selectMood(level)"
                >
                  <text class="mood-icon">{{ getMoodIcon(level) }}</text>
                  <text class="mood-desc">{{ getMoodDesc(level) }}</text>
                </view>
              </view>
              <view v-if="selectedMood" class="save-btn" @click="saveMood">
                <text class="save-text">保存今日心情</text>
              </view>
            </template>
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
        <view
          v-for="suggestion in growthSuggestions"
          :key="suggestion.id"
          class="suggestion-card"
        >
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
import { api } from "../../utils/api.js";

export default {
  data() {
    return {
      activeTab: "skills",
      recommendedSkills: [],
      skillCategories: [],
      practiceHistory: [],
      protectionLevel: "良好",
      protectionLevelDesc: "你具备基本的情感防护意识",
      growthSuggestions: [],

      // 心情晴雨表相关数据
      selectedMood: null,
      weeklyMoodData: {
        dates: [],
        levels: [],
      },
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
          this.loadGrowthData(),
          this.loadWeeklyMood(),
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

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/recommend`,
          method: "GET",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
          },
        });

        if (response.statusCode === 200) {
          this.recommendedSkills = response.data.recommended_skills || [];
        }
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
        )}&skillContent=${encodeURIComponent(skill.content)}&skillDifficulty=${
          skill.difficulty
        }&skillTags=${encodeURIComponent(
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
      // 模拟成长数据
      this.growthSuggestions = [
        {
          id: 1,
          title: "加强情感表达",
          content: '建议多练习"我"开头的表达方式，能更好地传达你的感受',
        },
        {
          id: 2,
          title: "提升边界意识",
          content: "学会在关系中设立清晰的边界，保护自己的情感安全",
        },
      ];
    },

    getDifficultyText(difficulty) {
      const map = {
        basic: "基础",
        intermediate: "进阶",
        advanced: "高级",
      };
      return map[difficulty] || "基础";
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

    // 心情晴雨表相关方法
    // 格式化短日期显示
    formatShortDate(dateStr) {
      if (!dateStr) return "--";
      const date = new Date(dateStr);
      const month = date.getMonth() + 1;
      const day = date.getDate();
      return `${month}/${day}`;
    },

    // 获取心情等级描述
    getMoodDesc(level) {
      const descriptions = {
        1: "很不满意",
        2: "有点失落",
        3: "还过得去",
        4: "挺满意的",
        5: "超级棒",
      };
      return descriptions[level] || "";
    },

    // 获取心情等级图标
    getMoodIcon(level) {
      const icons = {
        1: "😤",
        2: "😕",
        3: "😐",
        4: "😊",
        5: "🤩",
      };
      return icons[level] || "";
    },

    selectMood(level) {
      this.selectedMood = level;
    },

    async saveMood() {
      if (!this.selectedMood) {
        uni.showToast({
          title: "请选择心情档位",
          icon: "none",
        });
        return;
      }

      // 检查是否已登录
      const token = uni.getStorageSync("access_token");
      if (!token) {
        uni.showModal({
          title: "提示",
          content: "请先登录账户",
          success: (res) => {
            if (res.confirm) {
              uni.navigateTo({
                url: "/pages/login/login",
              });
            }
          },
        });
        return;
      }

      try {
        uni.showLoading({ title: "保存中..." });

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/mood-tracker/mood`,
          method: "POST",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          data: {
            mood_level: this.selectedMood,
          },
        });

        if (response.statusCode === 200) {
          uni.showToast({
            title: "心情记录成功",
            icon: "success",
          });

          // 重新加载7天数据
          await this.loadWeeklyMood();

          // 清除选择
          this.selectedMood = null;
        } else if (response.statusCode === 401) {
          uni.showModal({
            title: "登录已过期",
            content: "请重新登录",
            success: (res) => {
              if (res.confirm) {
                uni.removeStorageSync("access_token");
                uni.navigateTo({
                  url: "/pages/login/login",
                });
              }
            },
          });
        } else {
          throw new Error(response.data?.detail || "保存失败");
        }
      } catch (error) {
        console.error("保存心情失败:", error);
        uni.showToast({
          title: error.message || "保存失败",
          icon: "none",
        });
      } finally {
        uni.hideLoading();
      }
    },

    async loadWeeklyMood() {
      const token = uni.getStorageSync("access_token");

      // 如果没有token，显示空数据
      if (!token) {
        this.weeklyMoodData = {
          dates: [],
          levels: [],
        };
        return;
      }

      try {
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/mood-tracker/mood/weekly`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.statusCode === 200) {
          this.weeklyMoodData = response.data;
        } else if (response.statusCode === 401) {
          // Token过期，清除本地存储
          uni.removeStorageSync("access_token");
          this.weeklyMoodData = {
            dates: [],
            levels: [],
          };
        }
      } catch (error) {
        console.error("加载心情数据失败:", error);
        // 出错时显示空数据
        this.weeklyMoodData = {
          dates: [],
          levels: [],
        };
      }
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
  box-shadow: 0 8rpx 32rpx rgba(144, 202, 249, 0.3);
  border-radius: 0 0 60rpx 40rpx;
  margin-bottom: 40rpx;
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
  background: linear-gradient(
    135deg,
    rgba(227, 242, 253, 0.8) 0%,
    rgba(255, 255, 255, 0.9) 100%
  );
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
  background: linear-gradient(
    135deg,
    rgba(227, 242, 253, 0.9) 0%,
    rgba(255, 255, 255, 0.9) 100%
  );
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
  margin-bottom: 8rpx;
}

.category-count {
  font-size: 22rpx;
  color: #999;
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

.growth-overview {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 40rpx;
}

.overview-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
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
  background: linear-gradient(90deg, #42a5f5, #1976d2);
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
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.suggestion-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
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
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  color: white;
  padding: 20rpx;
  border-radius: 12rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.3);
  transition: all 0.3s ease;
}

.suggestion-action:active {
  transform: translateY(1rpx);
  box-shadow: 0 2rpx 8rpx rgba(66, 165, 245, 0.4);
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

  .category-count {
    font-size: 20rpx;
  }
}

@media (max-width: 480rpx) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 16rpx;
  }
}

/* 心情晴雨表样式 */
.mood-rating-section {
  padding: 32rpx 24rpx;
  background: rgba(248, 250, 252, 0.8);
  border-radius: 20rpx;
  border: 1rpx solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.rating-label {
  font-size: 28rpx;
  color: #1e293b;
  margin-bottom: 32rpx;
  display: block;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.5rpx;
}

.mood-buttons {
  display: flex;
  justify-content: space-between;
  gap: 12rpx;
  margin-bottom: 32rpx;
}

.mood-btn {
  flex: 1;
  height: 120rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 2rpx solid #e2e8f0;
  border-radius: 16rpx;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 8rpx;
  position: relative;
  overflow: hidden;
}

.mood-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  transition: left 0.5s;
}

.mood-btn:hover::before {
  left: 100%;
}

.mood-btn.active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-color: #1d4ed8;
  transform: translateY(-2rpx);
  box-shadow: 0 8rpx 25rpx rgba(59, 130, 246, 0.25);
}

.mood-icon {
  font-size: 36rpx;
  line-height: 1;
}

.mood-desc {
  font-size: 22rpx;
  font-weight: 500;
  color: #64748b;
  letter-spacing: 0.3rpx;
}

.mood-btn.active .mood-desc {
  color: #ffffff;
  font-weight: 600;
}

.save-btn {
  background: linear-gradient(135deg, #7dd3fc, #0ea5e9);
  color: white;
  padding: 28rpx 32rpx;
  border-radius: 16rpx;
  text-align: center;
  box-shadow: 0 4rpx 14rpx rgba(14, 165, 233, 0.25);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  position: relative;
  overflow: hidden;
}

.save-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.6s;
}

.save-btn:active::before {
  left: 100%;
}

.save-btn:active {
  transform: translateY(1rpx);
  box-shadow: 0 2rpx 8rpx rgba(14, 165, 233, 0.4);
}

.save-text {
  font-size: 28rpx;
  font-weight: 600;
  letter-spacing: 0.5rpx;
}

.weekly-mood {
  margin-bottom: 32rpx;
  padding: 24rpx;
  background-color: #f8f9fa;
  border-radius: 12rpx;
  border: 1rpx solid #dee2e6;
}

.section-subtitle {
  font-size: 28rpx;
  font-weight: 500;
  color: #495057;
  margin-bottom: 20rpx;
  text-align: center;
}

.mood-table-container {
  background-color: #ffffff;
  border-radius: 8rpx;
  border: 1rpx solid #e9ecef;
  overflow: hidden;
}

.table-row {
  display: flex;
  align-items: stretch;
}

.dates-row {
  background-color: #007aff;
  color: #ffffff;
}

.levels-row {
  background-color: #ffffff;
  border-top: 1rpx solid #e9ecef;
}

.table-cell {
  flex: 1;
  padding: 16rpx 8rpx;
  text-align: center;
  font-size: 24rpx;
  min-height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1rpx solid rgba(0, 0, 0, 0.1);
}

.table-cell:last-child {
  border-right: none;
}

.header-cell {
  font-weight: 500;
  font-size: 26rpx;
  background-color: rgba(0, 0, 0, 0.1);
  color: #ffffff;
  min-width: 80rpx;
}

.levels-row .header-cell {
  background-color: #f8f9fa;
  color: #495057;
  border-right: 1rpx solid #dee2e6;
}

.date-cell {
  font-size: 22rpx;
  font-weight: 400;
  color: #ffffff;
}

.level-cell {
  font-weight: 500;
  color: #6c757d;
  font-size: 28rpx;
}

.level-cell.has-data {
  color: #495057;
  background-color: #e7f3ff;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .mood-buttons {
    gap: 8rpx;
  }

  .mood-btn {
    height: 110rpx;
  }

  .mood-icon {
    font-size: 32rpx;
  }

  .mood-desc {
    font-size: 20rpx;
  }

  .table-cell {
    padding: 12rpx 6rpx;
    font-size: 22rpx;
    min-height: 56rpx;
  }
}

@media (max-width: 480rpx) {
  .mood-rating-section {
    padding: 24rpx 16rpx;
  }

  .weekly-mood {
    padding: 20rpx;
  }

  .mood-buttons {
    gap: 6rpx;
  }

  .mood-btn {
    height: 100rpx;
  }

  .mood-icon {
    font-size: 28rpx;
  }

  .mood-desc {
    font-size: 18rpx;
  }

  .table-cell {
    padding: 10rpx 4rpx;
    font-size: 20rpx;
    min-height: 50rpx;
  }
}

/* 登录提示样式 */
.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24rpx;
  padding: 48rpx 32rpx;
}

.prompt-text {
  font-size: 28rpx;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.3rpx;
}

.login-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 24rpx 48rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  font-weight: 600;
  letter-spacing: 0.5rpx;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4rpx 14rpx rgba(59, 130, 246, 0.25);
  border: none;
}

.login-btn:active {
  transform: translateY(1rpx);
  box-shadow: 0 2rpx 8rpx rgba(59, 130, 246, 0.35);
}

.login-text {
  font-size: 28rpx;
  color: white;
}
</style>
