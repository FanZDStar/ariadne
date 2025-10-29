<template>
  <view class="report-detail-container">    <!-- 加载状态 -->
    <view v-if="isLoading" class="loading-container">
      <text class="loading-text">正在加载报告详情...</text>
    </view>

    <!-- 报告内容 -->
    <view v-else-if="reportData" class="content">
      <view class="header">
        <text class="title">评估报告详情</text>
        <text class="subtitle">{{ getRelationTypeName(reportData.relationship_type) }}关系 · {{ formatDate(reportData.created_at) }}</text>
      </view>

      <scroll-view scroll-y="true" class="content-scroll">
        <!-- 总体得分卡片 -->
        <view class="score-summary">
          <view class="score-card">
            <text class="score-icon">{{ getScoreIcon(getReportScore()) }}</text>
            <text class="score-title">总体得分</text>
            <view class="score-level" :class="getScoreLevelClass(getReportScore())">
              <text class="level-text">{{ getScoreLevelName(getReportScore()) }}</text>
              <text class="level-score">{{ getReportScore().toFixed(1) }}%</text>
            </view>
            <text class="level-desc">{{ getScoreLevelDescription(getReportScore()) }}</text>
          </view>
        </view>

        <!-- 维度分析 -->
        <view v-if="getDimensionScores()" class="dimension-analysis">
          <text class="analysis-title">📊 各维度表现</text>
          <view v-for="(dimension, name) in getDimensionScores()" :key="name" class="dimension-item">
            <view class="dimension-header">
              <text class="dimension-name">{{ name }}</text>
              <text class="dimension-score">{{ getDimensionPercentage(dimension).toFixed(1) }}%</text>
            </view>
            <view class="dimension-bar">
              <view class="bar-fill" :style="{ 
                width: getDimensionPercentage(dimension) + '%',
                backgroundColor: getDimensionColor(getDimensionPercentage(dimension))
              }"></view>
            </view>
            <text class="dimension-level">{{ getScoreLevelName(getDimensionPercentage(dimension)) }}</text>
          </view>
        </view>

        <!-- AI 分析 -->
        <view v-if="reportData.ai_analysis" class="ai-analysis">
          <text class="analysis-title">🤖 AI专业分析</text>
          <view class="analysis-content">
            <text class="analysis-text">{{ reportData.ai_analysis }}</text>
          </view>
        </view>

        <!-- 个性化建议 -->
        <view v-if="getRecommendations().length > 0" class="recommendations">
          <text class="rec-title">💡 个性化建议</text>
          <view v-for="(rec, index) in getRecommendations()" :key="index" class="rec-item">
            <view class="rec-header">
              <text class="rec-type">{{ rec.title || rec.type }}</text>
              <view class="rec-priority" :class="rec.priority">
                <text class="priority-text">{{ getPriorityText(rec.priority) }}</text>
              </view>
            </view>
            <text class="rec-content">{{ rec.content }}</text>
          </view>
        </view>

        <!-- 操作按钮 -->
        <view class="action-buttons">
          <view class="action-btn secondary" @click="shareReport">
            <text class="btn-text">分享报告</text>
          </view>
          <view class="action-btn primary" @click="startNewAssessment">
            <text class="btn-text">重新评估</text>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      reportData: null,
      isLoading: true,
      reportId: null,
      relationTypes: {
        'family': '家庭',
        'friendship': '友谊',
        'romantic': '恋爱',
        'mentor': '师生'
      }
    }
  },

  onLoad(options) {
    // 优先从reportId获取，兼容旧的data方式
    if (options.reportId) {
      this.reportId = options.reportId;
      this.loadReportFromAPI();
    } else if (options.data) {
      try {
        const data = JSON.parse(decodeURIComponent(options.data));
        this.reportId = data.id;
        this.loadReportFromAPI();
      } catch (error) {
        console.error('解析报告数据失败:', error);
        this.showError('数据解析失败');
      }
    } else {
      this.showError('缺少报告信息');
    }
  },

  methods: {
    // 从API获取完整报告数据
    async loadReportFromAPI() {
      if (!this.reportId) return;
      
      try {
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/relationship-assessment/reports/${this.reportId}`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.statusCode === 200) {
          this.reportData = response.data;
          this.isLoading = false;
        }
      } catch (error) {
        console.error('加载报告失败:', error);
        this.showError('加载失败');
      }
    },

    showError(message) {
      this.isLoading = false;
      uni.showToast({ title: message, icon: 'none' });
      setTimeout(() => uni.navigateBack(), 1500);
    },

    // 获取报告得分（兼容不同数据结构）
    getReportScore() {
      if (!this.reportData) return 0;
      return this.reportData.assessment_result?.total_score || this.reportData.total_score || 0;
    },

    // 获取维度分数（兼容不同数据结构）
    getDimensionScores() {
      if (!this.reportData) return null;
      return this.reportData.assessment_result?.dimension_scores || this.reportData.dimension_scores || null;
    },

    // 获取维度百分比
    getDimensionPercentage(dimension) {
      return dimension.percentage || dimension.score || 0;
    },

    // 获取建议列表（兼容不同数据结构）
    getRecommendations() {
      if (!this.reportData) return [];
      let recommendations = this.reportData.recommendations || [];
      if (typeof recommendations === 'string') {
        try {
          recommendations = JSON.parse(recommendations);
        } catch {
          return [];
        }
      }
      return Array.isArray(recommendations) ? recommendations : [];
    },

    // 获取等级名称
    getScoreLevelName(percentage) {
      if (percentage >= 85) return '优秀';
      if (percentage >= 70) return '良好';
      if (percentage >= 55) return '一般';
      if (percentage >= 40) return '待提升';
      return '需要帮助';
    },

    // 获取等级描述
    getScoreLevelDescription(percentage) {
      if (percentage >= 85) return '表现非常出色，值得继续保持';
      if (percentage >= 70) return '表现良好，有提升空间';
      if (percentage >= 55) return '基本合格，需要一些改进';
      if (percentage >= 40) return '需要重点关注和改进';
      return '建议寻求专业指导';
    },
    // 获取关系类型名称
    getRelationTypeName(type) {
      return this.relationTypes[type] || '未知';
    },

    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '未知时间';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    // 获取得分图标
    getScoreIcon(percentage) {
      if (percentage >= 85) return '🌟';
      if (percentage >= 70) return '😊';
      if (percentage >= 55) return '😐';
      if (percentage >= 40) return '😔';
      return '😟';
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
    },

    // 获取优先级文本
    getPriorityText(priority) {
      const texts = {
        'urgent': '紧急',
        'high': '重要',
        'medium': '建议',
        'low': '参考'
      };
      return texts[priority] || '建议';
    },

    // 分享报告
    shareReport() {
      const shareText = `我刚完成了${this.getRelationTypeName(this.reportData.relationship_type)}关系健康评估，总体得分${this.reportData.total_score.toFixed(1)}%，等级为${this.reportData.total_level.level}。快来一起测试吧！`;
      
      // #ifdef H5
      if (navigator.share) {
        navigator.share({
          title: '关系健康评估报告',
          text: shareText,
        }).catch(err => {
          console.log('分享失败:', err);
          this.copyToClipboard(shareText);
        });
      } else {
        this.copyToClipboard(shareText);
      }
      // #endif

      // #ifdef MP || APP-PLUS
      this.copyToClipboard(shareText);
      // #endif
    },

    // 复制到剪贴板
    copyToClipboard(text) {
      uni.setClipboardData({
        data: text,
        success: () => {
          uni.showToast({
            title: '已复制到剪贴板',
            icon: 'success'
          });
        },
        fail: () => {
          uni.showToast({
            title: '复制失败',
            icon: 'none'
          });
        }
      });
    },

    // 开始新评估
    startNewAssessment() {
      uni.redirectTo({
        url: '/pages/interpersonal-wisdom/risk-assessment'
      });
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 40rpx;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
}

.loading-text {
  font-size: 28rpx;
  color: #666;
  text-align: center;
  margin-top: 20rpx;
}

.loading-text::before {
  content: '📊';
  font-size: 60rpx;
  display: block;
  margin-bottom: 20rpx;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.1); opacity: 1; }
}

.report-detail-container {
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

.content-scroll {
  height: calc(100vh - 160rpx);
  padding: 20rpx;
  box-sizing: border-box;
}

.score-summary {
  margin-bottom: 30rpx;
}

.score-card {
  background: white;
  border-radius: 16rpx;
  padding: 30rpx 20rpx;
  text-align: center;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  max-width: 100%;
}

.score-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 16rpx;
}

.score-title {
  font-size: 26rpx;
  color: #999;
  margin-bottom: 16rpx;
  display: block;
}

.score-level {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16rpx;
}

.level-text {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 6rpx;
  display: block;
}

.level-score {
  font-size: 28rpx;
  opacity: 0.8;
}

.score-level.excellent .level-text { color: #52C41A; }
.score-level.good .level-text { color: #1890FF; }
.score-level.average .level-text { color: #FAAD14; }
.score-level.below-average .level-text { color: #FF7A45; }
.score-level.poor .level-text { color: #F5222D; }

.level-desc {
  font-size: 24rpx;
  color: #666;
  text-align: center;
  line-height: 1.4;
}

.dimension-analysis {
  background: white;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.1);
}

.analysis-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
  display: block;
}

.dimension-item {
  margin-bottom: 24rpx;
}

.dimension-item:last-child {
  margin-bottom: 0;
}

.dimension-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.dimension-name {
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
}

.dimension-score {
  font-size: 24rpx;
  font-weight: 600;
  color: #1890FF;
}

.dimension-bar {
  height: 16rpx;
  background: #f0f0f0;
  border-radius: 8rpx;
  overflow: hidden;
  margin-bottom: 10rpx;
  border: 1rpx solid #e8e8e8;
}

.bar-fill {
  height: 100%;
  transition: width 0.8s ease-out;
  border-radius: 10rpx;
  box-shadow: inset 0 1rpx 2rpx rgba(255, 255, 255, 0.3);
}

.dimension-level {
  font-size: 24rpx;
  color: #666;
}

.ai-analysis {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.analysis-content {
  background: #f8f9fa;
  border-radius: 16rpx;
  padding: 32rpx;
  border-left: 6rpx solid #42a5f5;
}

.analysis-text {
  font-size: 28rpx;
  color: #555;
  line-height: 1.8;
  text-align: justify;
}

.recommendations {
  margin-bottom: 30rpx;
}

.rec-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
  padding: 0 20rpx;
}

.rec-item {
  background: white;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 3rpx 10rpx rgba(0, 0, 0, 0.1);
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.rec-type {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
}

.rec-priority {
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  font-size: 18rpx;
}

.rec-priority.urgent {
  background: #ffebee;
  color: #f44336;
}

.rec-priority.high {
  background: #fff3e0;
  color: #ff9800;
}

.rec-priority.medium {
  background: #e8f5e8;
  color: #4caf50;
}

.rec-priority.low {
  background: #f0f0f0;
  color: #666;
}

.priority-text {
  font-size: 18rpx;
}

.rec-content {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 20rpx;
  margin-top: 20rpx;
}

.action-btn {
  flex: 1;
  padding: 32rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: bold;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  color: white;
  box-shadow: 0 6rpx 20rpx rgba(66, 165, 245, 0.3);
}

.action-btn.secondary {
  background: white;
  color: #666;
  border: 2rpx solid #e0e0e0;
}

.action-btn:active {
  transform: translateY(2rpx);
}

.action-btn.primary:active {
  box-shadow: 0 4rpx 12rpx rgba(66, 165, 245, 0.4);
}

.btn-text {
  font-size: 28rpx;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .rec-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12rpx;
  }

  .action-buttons {
    flex-direction: column;
  }

  .dimension-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8rpx;
  }
}
</style>