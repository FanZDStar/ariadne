<template>
  <view class="reports-container">    <view class="header">
      <text class="title">关系健康测试报告解读</text>
      <text class="subtitle">深度分析你的人际关系健康状况</text>
    </view>

    <!-- 快捷操作区 -->
    <view class="quick-actions">
      <view class="action-card" @click="startNewAssessment">
        <text class="action-icon">📊</text>
        <text class="action-title">开始新评估</text>
        <text class="action-desc">进行全面的关系健康评估</text>
      </view>
    </view>

    <!-- 历史报告列表 -->
    <view class="reports-section">
      <view class="section-header">
        <text class="section-title">📋 历史报告</text>
        <view class="refresh-btn" @click="refreshReports">
          <text class="refresh-icon">🔄</text>
        </view>
      </view>

      <!-- 加载状态 -->
      <view v-if="isLoading" class="loading-section">
        <!-- 骨架屏 -->
        <view class="skeleton-container">
          <view v-for="n in 3" :key="n" class="skeleton-report-item">
            <view class="skeleton-header">
              <view class="skeleton-info">
                <view class="skeleton-title"></view>
                <view class="skeleton-date"></view>
              </view>
              <view class="skeleton-score"></view>
            </view>
            <view class="skeleton-level"></view>
            <view class="skeleton-dimensions">
              <view v-for="m in 4" :key="m" class="skeleton-dimension">
                <view class="skeleton-dimension-name"></view>
                <view class="skeleton-dimension-bar"></view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 报告列表 -->
      <view v-else-if="reports.length > 0" class="reports-list">
        <view 
          class="report-item fade-in"
          v-for="(report, index) in reports" 
          :key="report.id"
          :style="{ animationDelay: (index * 0.1) + 's' }"
          @click="viewReport(report)"
        >
          <view class="report-header">
            <view class="report-info">
              <text class="report-title">{{ getRelationTypeName(report.relationship_type) }}关系评估</text>
              <text class="report-date">{{ formatDate(report.created_at) }}</text>
            </view>
            <view class="report-score" :class="getScoreLevelClass(report.total_score)">
              <text class="score-text">{{ report.total_score.toFixed(1) }}%</text>
            </view>
          </view>
          
          <text class="report-level">{{ report.total_level.level }}</text>
          
          <!-- 维度得分简览 -->
          <view class="dimensions-preview">
            <view 
              v-for="(dimension, name) in report.dimension_scores" 
              :key="name"
              class="dimension-preview"
            >
              <text class="dimension-name">{{ name }}</text>
              <view class="dimension-bar-small">
                <view 
                  class="bar-fill-small" 
                  :style="{ 
                    width: dimension.percentage + '%',
                    backgroundColor: getDimensionColor(dimension.percentage)
                  }"
                ></view>
              </view>
            </view>
          </view>

          <view class="report-arrow">
            <text class="arrow">→</text>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view v-else class="empty-state">
        <view class="empty-content fade-in">
          <text class="empty-icon">📭</text>
          <text class="empty-title">暂无评估报告</text>
          <text class="empty-desc">完成第一次关系健康评估，开始了解你的人际状况</text>
          <view class="empty-action" @click="startNewAssessment">
            <text class="empty-btn-text">立即评估</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 解读指南 -->
    <view class="guide-section">
      <view class="guide-header">
        <text class="guide-title">💡 报告解读指南</text>
      </view>
      
      <view class="guide-items">
        <view class="guide-item">
          <text class="guide-icon">🌟</text>
          <view class="guide-content">
            <text class="guide-item-title">优秀 (85%+)</text>
            <text class="guide-item-desc">关系非常健康，继续保持良好模式</text>
          </view>
        </view>
        
        <view class="guide-item">
          <text class="guide-icon">😊</text>
          <view class="guide-content">
            <text class="guide-item-title">良好 (70-84%)</text>
            <text class="guide-item-desc">关系总体良好，可进一步优化</text>
          </view>
        </view>
        
        <view class="guide-item">
          <text class="guide-icon">😐</text>
          <view class="guide-content">
            <text class="guide-item-title">一般 (55-69%)</text>
            <text class="guide-item-desc">需要关注和改善某些方面</text>
          </view>
        </view>
        
        <view class="guide-item">
          <text class="guide-icon">😔</text>
          <view class="guide-content">
            <text class="guide-item-title">待提升 (40-54%)</text>
            <text class="guide-item-desc">建议重点关注问题维度</text>
          </view>
        </view>
        
        <view class="guide-item">
          <text class="guide-icon">😟</text>
          <view class="guide-content">
            <text class="guide-item-title">需要帮助 (40%以下)</text>
            <text class="guide-item-desc">建议寻求专业指导和帮助</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 温馨提示 -->
    <!-- <view class="notice-card">
      <view class="notice-header">
        <text class="notice-icon">💡</text>
        <text class="notice-title">温馨提示</text>
      </view>
      <text class="notice-text">评估结果仅供参考，持续关注和改善人际关系需要时间和实践</text>
    </view> -->
  </view>
</template>

<script>
export default {
  data() {
    return {
      reports: [],
      isLoading: false,
      relationTypes: {
        'family': '家庭',
        'friendship': '友谊', 
        'romantic': '恋爱',
        'mentor': '师生'
      }
    }
  },

  onLoad() {
    this.loadReports();
  },

  onShow() {
    // 页面显示时刷新报告列表，以防从评估页面返回后有新报告
    this.loadReports();
  },

  methods: {
    // 加载历史报告
    async loadReports() {
      try {
        this.isLoading = true;
        
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/relationship-assessment/reports`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.statusCode === 200) {
          this.reports = response.data.reports || [];
        }
      } catch (error) {
        console.error('加载报告失败:', error);
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        });
      } finally {
        this.isLoading = false;
      }
    },

    // 刷新报告
    refreshReports() {
      uni.showLoading({ title: '刷新中...' });
      this.loadReports().then(() => {
        uni.hideLoading();
        uni.showToast({
          title: '刷新成功',
          icon: 'success'
        });
      });
    },

    // 开始新评估
    startNewAssessment() {
      uni.navigateTo({
        url: '/pages/interpersonal-wisdom/risk-assessment'
      });
    },

    // 查看详细报告
    viewReport(report) {
      // 传递报告ID到详情页面，让详情页面从API获取完整数据
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/report-detail?reportId=${report.id}`
      });
    },

    // 获取关系类型名称
    getRelationTypeName(type) {
      return this.relationTypes[type] || '未知';
    },

    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '未知时间';
      
      const date = new Date(dateString);
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
        return date.toLocaleDateString('zh-CN');
      }
    },

    // 获取得分等级样式类
    getScoreLevelClass(percentage) {
      if (percentage >= 85) return 'excellent';
      if (percentage >= 70) return 'good';
      if (percentage >= 55) return 'average';
      if (percentage >= 40) return 'below-average';
      return 'poor';
    },

    // 获取维度颜色
    getDimensionColor(percentage) {
      if (percentage >= 85) return '#52C41A';
      if (percentage >= 70) return '#1890FF';
      if (percentage >= 55) return '#FAAD14';
      if (percentage >= 40) return '#FF7A45';
      return '#F5222D';
    }
  }
}
</script>

<style scoped>
.reports-container {
  padding: 0;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  padding: 60rpx 40rpx 40rpx;
  color: #1976d2;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8rpx 32rpx rgba(144, 202, 249, 0.3);
  border-radius: 0 0 60rpx 40rpx;
  margin-bottom: 30rpx;
}

.header::before {
  content: '';
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
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 28rpx;
  opacity: 0.9;
  position: relative;
  z-index: 2;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.1);
}

.quick-actions {
  padding: 0 40rpx 30rpx;
}

.action-card {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  text-align: center;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.action-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 64rpx;
  display: block;
  margin-bottom: 20rpx;
}

.action-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 12rpx;
}

.action-desc {
  font-size: 26rpx;
  color: #666;
}

.reports-section {
  padding: 0 40rpx 30rpx;
  min-height: 600rpx; /* 设置最小高度，避免内容加载时页面跳动 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60rpx;
  height: 60rpx;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  backdrop-filter: blur(10rpx);
  transition: all 0.3s ease;
}

.refresh-btn:active {
  transform: scale(0.9);
  background: rgba(255, 255, 255, 0.9);
}

.refresh-icon {
  font-size: 28rpx;
  color: #1976d2;
}

.loading-section {
  padding: 0;
}

/* 骨架屏样式 */
.skeleton-container {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.skeleton-report-item {
  background: white;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.skeleton-info {
  flex: 1;
}

.skeleton-title {
  width: 200rpx;
  height: 30rpx;
  background: #f0f0f0;
  border-radius: 4rpx;
  margin-bottom: 8rpx;
}

.skeleton-date {
  width: 100rpx;
  height: 24rpx;
  background: #f5f5f5;
  border-radius: 4rpx;
}

.skeleton-score {
  width: 120rpx;
  height: 56rpx;
  background: #f0f0f0;
  border-radius: 20rpx;
}

.skeleton-level {
  width: 80rpx;
  height: 26rpx;
  background: #f5f5f5;
  border-radius: 4rpx;
  margin-bottom: 20rpx;
}

.skeleton-dimensions {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.skeleton-dimension {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.skeleton-dimension-name {
  width: 120rpx;
  height: 24rpx;
  background: #f5f5f5;
  border-radius: 4rpx;
  flex-shrink: 0;
}

.skeleton-dimension-bar {
  flex: 1;
  height: 12rpx;
  background: #f0f0f0;
  border-radius: 6rpx;
}

@keyframes skeleton-pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    opacity: 1;
  }
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-out both;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.report-item {
  background: white;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
}

.report-item:active {
  transform: translateY(2rpx);
  box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.15);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.report-info {
  flex: 1;
}

.report-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 8rpx;
}

.report-date {
  font-size: 24rpx;
  color: #999;
}

.report-score {
  padding: 12rpx 20rpx;
  border-radius: 20rpx;
  min-width: 120rpx;
  text-align: center;
}

.report-score.excellent {
  background: #f6ffed;
  border: 2rpx solid #52c41a;
}

.report-score.good {
  background: #e6f7ff;
  border: 2rpx solid #1890ff;
}

.report-score.average {
  background: #fffbe6;
  border: 2rpx solid #faad14;
}

.report-score.below-average {
  background: #fff2e8;
  border: 2rpx solid #ff7a45;
}

.report-score.poor {
  background: #fff1f0;
  border: 2rpx solid #f5222d;
}

.score-text {
  font-size: 28rpx;
  font-weight: bold;
}

.report-score.excellent .score-text { color: #52c41a; }
.report-score.good .score-text { color: #1890ff; }
.report-score.average .score-text { color: #faad14; }
.report-score.below-average .score-text { color: #ff7a45; }
.report-score.poor .score-text { color: #f5222d; }

.report-level {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 20rpx;
  display: block;
}

.dimensions-preview {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.dimension-preview {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.dimension-name {
  font-size: 24rpx;
  color: #666;
  width: 120rpx;
  flex-shrink: 0;
}

.dimension-bar-small {
  flex: 1;
  height: 12rpx;
  background: #f0f0f0;
  border-radius: 6rpx;
  overflow: hidden;
}

.bar-fill-small {
  height: 100%;
  transition: width 0.8s ease-out;
  border-radius: 6rpx;
}

.report-arrow {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
}

.arrow {
  font-size: 32rpx;
  color: #ddd;
}

.empty-state {
  min-height: 500rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  padding: 40rpx;
}

.empty-icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: 30rpx;
  opacity: 0.6;
}

.empty-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 16rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 40rpx;
  display: block;
}

.empty-action {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  color: white;
  padding: 24rpx 60rpx;
  border-radius: 40rpx;
  display: inline-block;
  box-shadow: 0 6rpx 20rpx rgba(66, 165, 245, 0.3);
  transition: all 0.3s ease;
}

.empty-action:active {
  transform: translateY(2rpx);
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.4);
}

.empty-btn-text {
  font-size: 28rpx;
  font-weight: 600;
}

.guide-section {
  padding: 0 40rpx 30rpx;
}

.guide-header {
  margin-bottom: 20rpx;
}

.guide-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.guide-items {
  background: white;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.guide-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.guide-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.guide-icon {
  font-size: 32rpx;
  width: 50rpx;
  text-align: center;
}

.guide-content {
  flex: 1;
}

.guide-item-title {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 6rpx;
}

.guide-item-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

.notice-card {
  margin: 0 40rpx 40rpx;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.notice-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.notice-icon {
  font-size: 32rpx;
  margin-right: 12rpx;
}

.notice-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.notice-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .report-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16rpx;
  }

  .report-score {
    align-self: flex-end;
  }

  .dimension-name {
    width: 100rpx;
    font-size: 22rpx;
  }

  .guide-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12rpx;
  }

  .guide-icon {
    align-self: flex-start;
  }
}
</style>