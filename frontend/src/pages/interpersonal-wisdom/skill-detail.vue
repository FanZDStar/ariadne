<template>
  <view class="skill-detail-container">
    <view class="header">
      <view class="skill-header">
        <view class="skill-basic-info">
          <text class="skill-title">{{ skillData.name }}</text>
          <view class="skill-meta">
            <view class="meta-item">
              <text class="meta-icon">⏱️</text>
              <text class="meta-text">{{ skillData.estimatedTime }}分钟</text>
            </view>
          </view>
        </view>
        <view class="favorite-btn" @click="toggleFavorite">
          <text class="favorite-icon">{{ isFavorited ? '❤️' : '🤍' }}</text>
        </view>
      </view>

      <text class="skill-description">{{ skillData.description }}</text>

      <view class="skill-tags">
        <text v-for="tag in skillData.tags" :key="tag" class="skill-tag">{{
          tag
        }}</text>
      </view>
    </view>

    <view class="content">
      <!-- 学习目标 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">🎯 学习目标</text>
        </view>
        <view class="objectives-list">
          <view v-for="objective in skillData.objectives" :key="objective" class="objective-item">
            <text class="objective-icon">•</text>
            <text class="objective-text">{{ objective }}</text>
          </view>
        </view>
      </view>

      <!-- 核心要点 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">💡 核心要点</text>
        </view>
        <view class="key-points">
          <view v-for="point in skillData.keyPoints" :key="point.title" class="point-card">
            <view class="point-header">
              <text class="point-icon">{{ point.icon }}</text>
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
          <text class="section-title">📋 实践步骤</text>
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
                <text class="tips-label">💡 小贴士：</text>
                <text class="tips-text">{{ step.tips }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 场景应用 -->
      <view class="section" v-if="skillData.scenarios && skillData.scenarios.length > 0">
        <view class="section-header">
          <text class="section-title">🎭 场景应用</text>
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
          <text class="section-title">🎭 实践场景</text>
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
          <text class="section-title">🔗 相关技能</text>
        </view>
        <view class="related-skills">
          <view v-for="skill in relatedSkills" :key="skill.id" class="related-skill-card"
            @click="viewRelatedSkill(skill)">
            <text class="related-skill-name">{{ skill.name }}</text>
            <text class="related-skill-desc">{{ skill.brief }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部操作区域 -->
    <view class="bottom-actions">
      <view class="action-btn primary" @click="startScenarioPractice">
        <text class="btn-text">情景演练</text>
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
          url: 'http://localhost:8000/skill-favorites/check',
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
          ? 'http://localhost:8000/skill-favorites/remove'
          : 'http://localhost:8000/skill-favorites/add';

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
.skill-detail-container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx;
  color: white;
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
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.favorite-btn:active {
  transform: scale(0.95);
  background-color: rgba(255, 255, 255, 0.3);
}

.favorite-icon {
  font-size: 36rpx;
}

.skill-title {
  font-size: 42rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
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
}

.meta-icon {
  font-size: 18rpx;
}

.meta-text {
  font-size: 22rpx;
  opacity: 0.9;
}

.skill-description {
  font-size: 26rpx;
  line-height: 1.6;
  opacity: 0.95;
  margin-bottom: 20rpx;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.3);
}

.content {
  padding: 0 40rpx;
}

.section {
  margin-bottom: 48rpx;
}

.section-header {
  margin-bottom: 24rpx;
  padding-top: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.objectives-list {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
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
  color: #667eea;
  margin-right: 12rpx;
  font-size: 24rpx;
  line-height: 1.5;
}

.objective-text {
  flex: 1;
  font-size: 26rpx;
  color: #333;
  line-height: 1.5;
}

.key-points {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.point-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.point-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.point-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.point-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.point-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.point-example {
  background-color: #f8f9ff;
  padding: 16rpx;
  border-radius: 12rpx;
  border-left: 4rpx solid #667eea;
}

.example-label {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  margin-right: 8rpx;
}

.example-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.practice-steps {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.step-item {
  display: flex;
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.step-number {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
}

.step-text {
  color: white;
  font-size: 24rpx;
  font-weight: bold;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.step-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16rpx;
}

.step-tips {
  background-color: #f0f4ff;
  padding: 16rpx;
  border-radius: 12rpx;
  border-left: 4rpx solid #667eea;
}

.tips-label {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  margin-right: 8rpx;
}

.tips-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.scenarios {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.scenario-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.scenario-card:active {
  transform: translateY(2rpx);
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.scenario-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.scenario-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 20rpx;
}

.scenario-action {
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

.related-skills {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.related-skill-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s ease;
}

.related-skill-card:active {
  transform: translateY(2rpx);
}

.related-skill-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.related-skill-desc {
  font-size: 24rpx;
  color: #666;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 24rpx 40rpx;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
}

.action-btn {
  width: 60%;
  padding: 28rpx 40rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: bold;
  transition: all 0.2s ease;
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.3);
}

.action-btn:active {
  transform: translateY(2rpx);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background-color: #4caf50;
  color: white;
}

.action-btn.tertiary {
  background-color: #f0f0f0;
  color: #666;
  border: 2rpx solid #e0e0e0;
}

.btn-text {
  font-size: 28rpx;
}
</style>
