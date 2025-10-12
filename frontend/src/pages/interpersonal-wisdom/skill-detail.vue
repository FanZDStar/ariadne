<template>
  <view class="skill-detail-container">
    <view class="content">
      <!-- 技能信息卡片 -->
      <view class="skill-info-card">
        <view class="skill-header">
          <view class="skill-basic-info">
            <text class="skill-title">{{ skillData.name }}</text>
            <view class="skill-meta">
              <view class="meta-item">
                <text class="meta-text">{{ skillData.estimatedTime }}分钟</text>
              </view>
            </view>
          </view>
          <view class="favorite-btn" @click="toggleFavorite">
            <text class="favorite-icon">{{ isFavorited ? '♥' : '♡' }}</text>
          </view>
        </view>

        <text class="skill-description">{{ skillData.description }}</text>

        <view class="skill-tags">
          <text v-for="tag in skillData.tags" :key="tag" class="skill-tag">{{
            tag
          }}</text>
        </view>
      </view>
      <!-- 学习目标 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">学习目标</text>
        </view>
        <view class="objectives-list">
          <view v-for="objective in skillData.objectives" :key="objective" class="objective-item">
            <text class="objective-icon">·</text>
            <text class="objective-text">{{ objective }}</text>
          </view>
        </view>
      </view>

      <!-- 核心要点 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">核心要点</text>
        </view>
        <view class="key-points">
          <view v-for="point in skillData.keyPoints" :key="point.title" class="point-card">
            <view class="point-header">
              <text class="point-title">{{ point.title }}</text>
            </view>
            <text class="point-content">{{ point.content }}</text>
            <view v-if="point.example" class="point-example">
              <text class="example-label">示例：</text>
              <text class="example-text">{{ point.example }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 实践步骤 -->
      <view class="section" v-if="skillData.practiceSteps && skillData.practiceSteps.length > 0">
        <view class="section-header">
          <text class="section-title">实践步骤</text>
        </view>
        <view class="practice-steps">
          <view v-for="(step, index) in skillData.practiceSteps" :key="index" class="step-item">
            <view class="step-number">
              <text class="step-text">{{ index + 1 }}</text>
            </view>
            <view class="step-content">
              <text class="step-title">{{ step.title }}</text>
              <text class="step-description">{{ step.description }}</text>
              <view v-if="step.tips" class="step-tips">
                <text class="tips-label">小贴士：</text>
                <text class="tips-text">{{ step.tips }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 场景应用 -->
      <view class="section" v-if="skillData.scenarios && skillData.scenarios.length > 0">
        <view class="section-header">
          <text class="section-title">场景应用</text>
        </view>
        <view class="scenarios">
          <view v-for="scenario in skillData.scenarios" :key="scenario.id" class="scenario-card"
            @click="practiceScenario(scenario)">
            <view class="scenario-header">
              <text class="scenario-title">{{ scenario.title }}</text>
            </view>
            <text class="scenario-description">{{ scenario.description }}</text>
            <view class="scenario-action">
              <text class="action-text">开始练习</text>
              <text class="action-arrow">→</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 实践场景 (fallback for practiceScenarios) -->
      <view class="section"
        v-if="skillData.practiceScenarios && skillData.practiceScenarios.length > 0 && (!skillData.scenarios || skillData.scenarios.length === 0)">
        <view class="section-header">
          <text class="section-title">实践场景</text>
        </view>
        <view class="scenarios">
          <view v-for="(scenario, index) in skillData.practiceScenarios" :key="index" class="scenario-card"
            @click="practiceScenario(scenario)">
            <view class="scenario-header">
              <text class="scenario-title">{{ scenario.title }}</text>
            </view>
            <text class="scenario-description">{{ scenario.description }}</text>
            <view class="scenario-action">
              <text class="action-text">开始练习</text>
              <text class="action-arrow">→</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 相关技能 -->
      <view class="section" v-if="relatedSkills.length > 0">
        <view class="section-header">
          <text class="section-title">相关技能</text>
        </view>
        <view class="related-skills">
          <view v-for="skill in relatedSkills" :key="skill.id" class="related-skill-card"
            @click="viewRelatedSkill(skill)">
            <text class="related-skill-name">{{ skill.name }}</text>
            <text class="related-skill-desc">{{ skill.brief }}</text>
          </view>
        </view>
      </view>

      <!-- 操作按钮区域 -->
      <view class="action-section">
        <view class="action-btn primary" @click="startScenarioPractice">
          <text class="btn-text">情景演练</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getSkillById, getRelatedSkills } from '@/data/skillsData.js';

export default {
  data() {
    return {
      skillId: "",
      categoryId: "",
      skillData: {},
      relatedSkills: [],
      isFavorited: false, // 收藏状态
    };
  },

  onLoad(options) {
    this.skillId = options.skillId;
    this.categoryId = options.categoryId;
    this.loadSkillDetail();
    this.checkFavoriteStatus();
  },

  onShow() {
    // 页面显示时的处理（已移除星点奖励检查）
  },

  methods: {
    async loadSkillDetail() {
      try {
        uni.showLoading({ title: "加载中..." });

        // 使用统一的数据源
        await this.loadSkillFromDataSource();
      } catch (error) {
        console.error("加载技能详情失败:", error);
        uni.showToast({
          title: "加载失败",
          icon: "none",
        });
      } finally {
        uni.hideLoading();
      }
    },

    async loadSkillFromDataSource() {
      // 从统一数据源获取技能数据
      const skillData = getSkillById(this.skillId);

      if (skillData) {
        this.skillData = skillData;
        // 获取相关技能推荐
        this.relatedSkills = getRelatedSkills(this.skillId, 2);
      } else {
        // 如果统一数据源中没有，使用默认数据
        this.skillData = this.getDefaultSkillData();
        this.relatedSkills = [];
      }
    },

    getDefaultSkillData() {
      return {
        id: this.skillId,
        name: "技能加载中...",
        description: "技能详情正在加载，请稍等。",
        estimatedTime: 20,
        learnerCount: 0,
        tags: ["默认"],
        objectives: ["学习基础技能"],
        keyPoints: [],
        practiceScenarios: []
      };
    },


    startScenarioPractice() {
      // 传递完整的技能信息到练习页面
      const skillParams = {
        skillId: this.skillData.id,
        type: "practice",
        skillTitle: encodeURIComponent(this.skillData.name),
        skillContent: encodeURIComponent(this.skillData.description),
        skillTags: encodeURIComponent(JSON.stringify(this.skillData.tags)),
        skillScenarios: encodeURIComponent(
          JSON.stringify(this.skillData.scenarios || [])
        ),
      };

      const queryString = Object.entries(skillParams)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-practice?${queryString}`,
      });
    },

    startLearning() {
      this.startScenarioPractice();
    },

    continueLearning() {
      this.startScenarioPractice();
    },

    reviewSkill() {
      this.startScenarioPractice();
    },

    async generatePracticeScenario() {
      this.startScenarioPractice();
    },

    practiceScenario(scenario) {
      // 传递完整的技能和场景信息到练习页面
      const practiceParams = {
        skillId: this.skillData.id,
        scenarioId: scenario.id,
        type: "scenario",
        skillTitle: encodeURIComponent(this.skillData.name),
        skillContent: encodeURIComponent(this.skillData.description),
        skillTags: encodeURIComponent(JSON.stringify(this.skillData.tags)),
        scenarioTitle: encodeURIComponent(scenario.title),
        scenarioDescription: encodeURIComponent(scenario.description)
      };

      const queryString = Object.entries(practiceParams)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-practice?${queryString}`,
      });
    },

    viewRelatedSkill(skill) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.id}&categoryId=${this.categoryId}`,
      });
    },

    // 检查收藏状态
    async checkFavoriteStatus() {
      try {
        const token = uni.getStorageSync('access_token');
        if (!token) return;

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/skill-favorites/check`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${token}`
          },
          data: {
            skill_id: this.skillId
          }
        });

        if (response.statusCode === 200) {
          this.isFavorited = response.data.is_favorited;
        }
      } catch (error) {
        console.error('检查收藏状态失败:', error);
      }
    },

    // 切换收藏状态
    async toggleFavorite() {
      try {
        const token = uni.getStorageSync('access_token');
        if (!token) {
          uni.showToast({
            title: '请先登录',
            icon: 'none'
          });
          return;
        }

        uni.showLoading({ title: this.isFavorited ? '取消收藏中...' : '收藏中...' });

        const url = this.isFavorited
          ? `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/skill-favorites/remove`
          : `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/skill-favorites/add`;

        const requestData = {
          skill_id: String(this.skillId), // 确保是字符串类型
          category: this.getCategoryFromSkillId(),
          skill_name: this.skillData.name
        };

        console.log('发送收藏请求:', {
          url: url,
          data: requestData,
          isFavorited: this.isFavorited
        });

        const response = await uni.request({
          url: url,
          method: 'POST',
          header: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          data: requestData
        });

        console.log('收藏请求响应:', response);

        if (response.statusCode === 200) {
          const responseData = response.data;
          const wasAddingFavorite = !this.isFavorited; // 记录操作类型
          this.isFavorited = !this.isFavorited;

          // 处理星点奖励 - 只有添加收藏时才处理奖励
          if (wasAddingFavorite && responseData.star_reward && responseData.star_reward.is_rewarded) {
            // 先显示收藏成功提示
            uni.showToast({
              title: '收藏成功',
              icon: 'success',
              duration: 1500
            });

            // 延迟显示星点奖励提示
            setTimeout(() => {
              uni.showToast({
                title: responseData.star_reward.description,
                icon: 'none',
                duration: 2500
              });
            }, 1800);
          } else {
            uni.showToast({
              title: this.isFavorited ? '收藏成功' : '取消收藏成功',
              icon: 'success'
            });
          }
        } else {
          console.error('API响应状态码不是200:', response.statusCode, response);
          throw new Error(`操作失败，状态码: ${response.statusCode}`);
        }
      } catch (error) {
        console.error('收藏操作失败:', error);
        console.error('完整错误信息:', JSON.stringify(error));
        uni.showToast({
          title: error.message || '操作失败',
          icon: 'none'
        });
      } finally {
        uni.hideLoading();
      }
    },

    // 根据技能ID获取分类
    getCategoryFromSkillId() {
      // 从统一数据源中查找技能所属分类
      const categories = ['communication', 'emotional_expression', 'relationship_building', 'special_scenarios'];

      for (const category of categories) {
        // 这里可以通过skillsData来判断，简化处理直接返回当前categoryId
        if (this.categoryId) {
          return this.categoryId;
        }
      }

      // 默认分类逻辑，可以根据skillId的范围来判断
      const skillNum = parseInt(this.skillId);
      if (skillNum <= 25) return 'communication';
      if (skillNum <= 38) return 'emotional_expression';
      if (skillNum <= 51) return 'relationship_building';
      return 'special_scenarios';
    },


  },
};
</script>

<style scoped>
/* 现代化浅蓝色系设计 */
.skill-detail-container {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #f5f9ff 100%);
  min-height: 100vh;
  position: relative;
}

.skill-detail-container::before {
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

.content {
  padding: 60rpx 40rpx 40rpx;
  position: relative;
  z-index: 1;
}

/* 技能信息卡片 */
.skill-info-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  position: relative;
  overflow: hidden;
}

.skill-info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background: linear-gradient(90deg, #87ceeb 0%, #add8e6 50%, #b0e0e6 100%);
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.skill-basic-info {
  flex: 1;
}

.favorite-btn {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(173, 216, 230, 0.3);
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.15),
    0 2rpx 4rpx rgba(173, 216, 230, 0.1);
}

.favorite-btn:active {
  transform: scale(0.95);
  background: rgba(135, 206, 235, 0.2);
  border-color: #87ceeb;
}

.favorite-icon {
  font-size: 36rpx;
  color: #4682b4;
  font-weight: 600;
}

.skill-title {
  font-size: 42rpx;
  font-weight: 700;
  margin-bottom: 16rpx;
  display: block;
  color: #2c3e50;
}

.skill-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
  background: linear-gradient(135deg, rgba(173, 216, 230, 0.2) 0%, rgba(176, 224, 230, 0.15) 100%);
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  border: 1px solid rgba(70, 130, 180, 0.2);
}

.meta-text {
  font-size: 22rpx;
  color: #4682b4;
  font-weight: 500;
}

.skill-description {
  font-size: 28rpx;
  color: #5a6c7d;
  line-height: 1.7;
  margin-bottom: 20rpx;
  font-weight: 400;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background: linear-gradient(135deg, rgba(173, 216, 230, 0.2) 0%, rgba(176, 224, 230, 0.15) 100%);
  color: #4682b4;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  font-weight: 500;
  border: 1px solid rgba(70, 130, 180, 0.2);
  backdrop-filter: blur(10px);
}

/* 内容区块 */
.section {
  margin-bottom: 32rpx;
}

.section-header {
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3e50;
  position: relative;
  padding-left: 20rpx;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 32rpx;
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  border-radius: 3rpx;
}

/* 学习目标 */
.objectives-list {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
}

.objective-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.objective-item:last-child {
  margin-bottom: 0;
}

.objective-icon {
  color: #87ceeb;
  margin-right: 12rpx;
  font-size: 24rpx;
  line-height: 1.5;
  font-weight: 600;
}

.objective-text {
  flex: 1;
  font-size: 26rpx;
  color: #2c3e50;
  line-height: 1.6;
  font-weight: 400;
}

/* 核心要点 */
.key-points {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.point-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  position: relative;
  overflow: hidden;
}

.point-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3rpx;
  background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
}

.point-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.point-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3e50;
}

.point-content {
  font-size: 26rpx;
  color: #5a6c7d;
  line-height: 1.7;
  margin-bottom: 16rpx;
  font-weight: 400;
}

.point-example {
  background: linear-gradient(135deg, rgba(240, 248, 255, 0.8) 0%, rgba(230, 243, 255, 0.6) 100%);
  padding: 20rpx;
  border-radius: 16rpx;
  border-left: 4px solid #87ceeb;
  backdrop-filter: blur(10px);
}

.example-label {
  font-size: 22rpx;
  color: #4682b4;
  font-weight: 600;
  margin-right: 8rpx;
}

.example-text {
  font-size: 24rpx;
  color: #5a6c7d;
  line-height: 1.6;
  font-weight: 400;
}

/* 实践步骤 */
.practice-steps {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.step-item {
  display: flex;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  position: relative;
  overflow: hidden;
}

.step-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3rpx;
  background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
}

.step-number {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.3),
    0 2rpx 4rpx rgba(173, 216, 230, 0.2);
}

.step-text {
  color: #2c3e50;
  font-size: 24rpx;
  font-weight: 700;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12rpx;
  display: block;
}

.step-description {
  font-size: 26rpx;
  color: #5a6c7d;
  line-height: 1.6;
  margin-bottom: 16rpx;
  font-weight: 400;
}

.step-tips {
  background: linear-gradient(135deg, rgba(240, 248, 255, 0.8) 0%, rgba(230, 243, 255, 0.6) 100%);
  padding: 20rpx;
  border-radius: 16rpx;
  border-left: 4px solid #87ceeb;
  backdrop-filter: blur(10px);
}

.tips-label {
  font-size: 22rpx;
  color: #4682b4;
  font-weight: 600;
  margin-right: 8rpx;
}

.tips-text {
  font-size: 24rpx;
  color: #5a6c7d;
  line-height: 1.6;
  font-weight: 400;
}

/* 场景应用 */
.scenarios {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.scenario-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.scenario-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(135, 206, 235, 0.05) 0%, rgba(173, 216, 230, 0.02) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.scenario-card:active::before {
  opacity: 1;
}

.scenario-card:active {
  transform: translateY(2rpx);
  border-color: #87ceeb;
  box-shadow: 
    0 6rpx 24rpx rgba(135, 206, 235, 0.2),
    0 4rpx 8rpx rgba(173, 216, 230, 0.15);
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.scenario-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3e50;
  position: relative;
  z-index: 1;
}

.scenario-description {
  font-size: 26rpx;
  color: #5a6c7d;
  line-height: 1.6;
  margin-bottom: 20rpx;
  font-weight: 400;
  position: relative;
  z-index: 1;
}

.scenario-action {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8rpx;
  color: #4682b4;
  position: relative;
  z-index: 1;
}

.action-text {
  font-size: 26rpx;
  font-weight: 500;
}

.action-arrow {
  font-size: 24rpx;
  font-weight: 600;
}

/* 相关技能 */
.related-skills {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.related-skill-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.related-skill-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(135, 206, 235, 0.05) 0%, rgba(173, 216, 230, 0.02) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.related-skill-card:active::before {
  opacity: 1;
}

.related-skill-card:active {
  transform: translateY(2rpx);
  border-color: #87ceeb;
  box-shadow: 
    0 6rpx 24rpx rgba(135, 206, 235, 0.2),
    0 4rpx 8rpx rgba(173, 216, 230, 0.15);
}

.related-skill-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8rpx;
  display: block;
  position: relative;
  z-index: 1;
}

.related-skill-desc {
  font-size: 24rpx;
  color: #5a6c7d;
  font-weight: 400;
  position: relative;
  z-index: 1;
}

/* 操作按钮区域 */
.action-section {
  margin-top: 40rpx;
  margin-bottom: 40rpx;
  display: flex;
  justify-content: center;
}

.action-btn {
  width: 60%;
  padding: 28rpx 40rpx;
  border-radius: 20rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 
    0 6rpx 20rpx rgba(135, 206, 235, 0.3),
    0 4rpx 8rpx rgba(173, 216, 230, 0.2);
}

.action-btn:active {
  transform: translateY(2rpx);
  box-shadow: 
    0 4rpx 16rpx rgba(135, 206, 235, 0.25),
    0 2rpx 6rpx rgba(173, 216, 230, 0.15);
}

.action-btn.primary {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  color: #2c3e50;
}

.action-btn.secondary {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.9) 0%, rgba(39, 174, 96, 0.8) 100%);
  color: white;
}

.action-btn.tertiary {
  background: rgba(255, 255, 255, 0.8);
  color: #4682b4;
  border: 2px solid rgba(173, 216, 230, 0.3);
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.15),
    0 2rpx 4rpx rgba(173, 216, 230, 0.1);
}

.btn-text {
  font-size: 28rpx;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .content {
    padding: 50rpx 30rpx 30rpx;
  }
  
  .skill-info-card,
  .point-card,
  .step-item,
  .scenario-card,
  .related-skill-card {
    padding: 24rpx;
  }
  
  .skill-title {
    font-size: 36rpx;
  }
  
  .section-title {
    font-size: 28rpx;
  }
  
  .action-btn {
    width: 70%;
    padding: 24rpx 32rpx;
    font-size: 28rpx;
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
</style>
