<template>
  <view class="reports-container">
    <!-- 快捷操作区 -->
    <view class="quick-actions">
      <view class="action-card" @click="startNewDrill">
        <text class="action-title">开始新训练</text>
        <text class="action-desc">进行防护技能训练</text>
      </view>
    </view>

    <!-- 统计概览 -->
    <view class="statistics-section">
      <view class="stats-card">
        <view class="stat-item">
          <text class="stat-number">{{ statistics.total_reports || 0 }}</text>
          <text class="stat-label">训练次数</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ getFormattedAverageScore() }}%</text>
          <text class="stat-label">平均得分</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ getDrillTypeCount() }}</text>
          <text class="stat-label">训练类型</text>
        </view>
      </view>
    </view>

    <!-- 历史报告列表 -->
    <view class="reports-section">
      <view class="section-header">
        <text class="section-title">训练记录</text>
        <view class="refresh-btn" @click="refreshReports">
          <text class="refresh-icon">刷新</text>
        </view>
      </view>

      <!-- 加载状态 -->
      <view v-if="isLoading" class="loading-section">
        <view class="skeleton-container">
          <view v-for="n in 3" :key="n" class="skeleton-report-item">
            <view class="skeleton-header">
              <view class="skeleton-info">
                <view class="skeleton-title"></view>
                <view class="skeleton-date"></view>
              </view>
              <view class="skeleton-score"></view>
            </view>
            <view class="skeleton-content"></view>
          </view>
        </view>
      </view>

      <!-- 报告列表 -->
      <view v-else-if="reports.length > 0" class="reports-list">
        <view
          class="report-item fade-in"
          v-for="(report, index) in reports"
          :key="report.id"
          :style="{ animationDelay: index * 0.1 + 's' }"
          @click="viewReport(report)"
        >
          <view class="report-header">
            <view class="report-info">
              <text class="report-title">{{ report.drill_type }}训练</text>
              <text class="report-subtitle" v-if="report.scenario_name">{{
                report.scenario_name
              }}</text>
              <text class="report-date">{{
                formatDate(report.created_at)
              }}</text>
            </view>
            <view
              class="report-score"
              :class="getScoreLevelClass(report.score)"
            >
              <text class="score-text">{{ report.score }}%</text>
            </view>
          </view>

          <view class="report-summary">
            <view class="summary-item">
              <text class="summary-label">题数</text>
              <text class="summary-value">{{ report.total_questions }}</text>
            </view>
            <view class="summary-item">
              <text class="summary-label">正确</text>
              <text class="summary-value">{{ report.correct_answers }}</text>
            </view>
            <view class="summary-item" v-if="report.completion_time">
              <text class="summary-label">用时</text>
              <text class="summary-value">{{
                formatTime(report.completion_time)
              }}</text>
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
          <text class="empty-title">暂无训练记录</text>
          <text class="empty-desc"
            >开始第一次防护技能训练，提升自我保护能力</text
          >
          <view class="start-btn" @click="startNewDrill">
            <text class="btn-text">开始训练</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      isLoading: true,
      reports: [],
      statistics: {
        total_reports: 0,
        average_score: 0,
        drill_type_distribution: {},
      },
      currentPage: 0,
      pageSize: 20,
      hasMore: true,
    };
  },
  onLoad() {
    this.loadReports();
    this.loadStatistics();
  },
  onPullDownRefresh() {
    this.refreshReports();
  },
  onReachBottom() {
    if (this.hasMore && !this.isLoading) {
      this.loadMoreReports();
    }
  },
  methods: {
    async loadReports() {
      try {
        this.isLoading = true;
        const token = uni.getStorageSync("access_token");

        // 添加调试信息
        console.log(
          "Current token:",
          token ? "Token exists" : "No token found"
        );

        if (!token) {
          uni.showToast({
            title: "请先登录",
            icon: "none",
          });
          setTimeout(() => {
            uni.redirectTo({
              url: "/pages/login/login",
            });
          }, 1500);
          return;
        }

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/protection-drill/reports`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          data: {
            skip: 0,
            limit: this.pageSize,
          },
        });

        if (response.statusCode === 200) {
          this.reports = response.data.reports;
          this.hasMore = this.reports.length >= this.pageSize;
          this.currentPage = 0;
        } else {
          throw new Error(response.data?.detail || "加载失败");
        }
      } catch (error) {
        console.error("加载报告失败:", error);
        uni.showToast({
          title: "加载失败",
          icon: "error",
        });
      } finally {
        this.isLoading = false;
        uni.stopPullDownRefresh();
      }
    },

    async loadMoreReports() {
      try {
        this.isLoading = true;
        const token = uni.getStorageSync("access_token");
        const skip = (this.currentPage + 1) * this.pageSize;

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/protection-drill/reports`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          data: {
            skip: skip,
            limit: this.pageSize,
          },
        });

        if (response.statusCode === 200) {
          const newReports = response.data.reports;
          this.reports = [...this.reports, ...newReports];
          this.hasMore = newReports.length >= this.pageSize;
          this.currentPage++;
        }
      } catch (error) {
        console.error("加载更多报告失败:", error);
      } finally {
        this.isLoading = false;
      }
    },

    async loadStatistics() {
      try {
        const token = uni.getStorageSync("access_token");

        if (!token) {
          console.log("No token for statistics");
          // 设置默认统计数据
          this.statistics = {
            total_reports: 0,
            average_score: 0,
            drill_type_distribution: {},
          };
          return;
        }

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/protection-drill/statistics`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          // 验证并设置默认值
          this.statistics = {
            total_reports: response.data.total_reports || 0,
            average_score:
              typeof response.data.average_score === "number"
                ? response.data.average_score
                : 0,
            drill_type_distribution:
              response.data.drill_type_distribution || {},
          };
        } else {
          // 设置默认统计数据
          this.statistics = {
            total_reports: 0,
            average_score: 0,
            drill_type_distribution: {},
          };
        }
      } catch (error) {
        console.error("加载统计信息失败:", error);
        // 设置默认统计数据
        this.statistics = {
          total_reports: 0,
          average_score: 0,
          drill_type_distribution: {},
        };
      }
    },

    refreshReports() {
      this.loadReports();
      this.loadStatistics();
    },

    viewReport(report) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/protection-drill-report-detail?id=${report.id}`,
      });
    },

    startNewDrill() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/protection-drill",
      });
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;

      if (diff < 60000) {
        // 1分钟内
        return "刚刚";
      } else if (diff < 3600000) {
        // 1小时内
        return Math.floor(diff / 60000) + "分钟前";
      } else if (diff < 86400000) {
        // 1天内
        return Math.floor(diff / 3600000) + "小时前";
      } else if (diff < 604800000) {
        // 1周内
        return Math.floor(diff / 86400000) + "天前";
      } else {
        return date.toLocaleDateString("zh-CN", {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
      }
    },

    formatTime(seconds) {
      if (seconds < 60) {
        return `${seconds}秒`;
      } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return remainingSeconds > 0
          ? `${minutes}分${remainingSeconds}秒`
          : `${minutes}分钟`;
      } else {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}小时${minutes}分钟`;
      }
    },

    getScoreLevelClass(score) {
      if (score >= 90) return "score-excellent";
      if (score >= 80) return "score-good";
      if (score >= 70) return "score-average";
      if (score >= 60) return "score-poor";
      return "score-critical";
    },

    getFormattedAverageScore() {
      if (
        !this.statistics ||
        this.statistics.average_score === null ||
        this.statistics.average_score === undefined ||
        typeof this.statistics.average_score !== "number"
      ) {
        return "0.0";
      }
      return this.statistics.average_score.toFixed(1);
    },

    getDrillTypeCount() {
      if (
        !this.statistics ||
        !this.statistics.drill_type_distribution ||
        typeof this.statistics.drill_type_distribution !== "object"
      ) {
        return 0;
      }
      return Object.keys(this.statistics.drill_type_distribution).length;
    },
  },
};
</script>

<style scoped>
.reports-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fdf4 50%, #ffffff 100%);
  padding: 40rpx 20rpx 20rpx;
}

.quick-actions {
  margin-bottom: 40rpx;
}

.action-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(34, 197, 94, 0.15);
  border: 1rpx solid rgba(34, 197, 94, 0.1);
  transition: all 0.3s ease;
}

.action-card:active {
  transform: translateY(2rpx) scale(0.98);
  box-shadow: 0 4rpx 16rpx rgba(34, 197, 94, 0.25);
}

.action-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #059669;
  display: block;
  margin-bottom: 8rpx;
}

.action-desc {
  font-size: 26rpx;
  color: #666;
  display: block;
}

.statistics-section {
  margin-bottom: 40rpx;
}

.stats-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  padding: 40rpx;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 8rpx 32rpx rgba(34, 197, 94, 0.15);
  border: 1rpx solid rgba(34, 197, 94, 0.1);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #059669;
  display: block;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #666;
  display: block;
}

.reports-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx 24rpx 0 0;
  min-height: 60vh;
  border: 1rpx solid rgba(34, 197, 94, 0.1);
  box-shadow: 0 8rpx 32rpx rgba(34, 197, 94, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40rpx 40rpx 20rpx;
  border-bottom: 1rpx solid rgba(34, 197, 94, 0.1);
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #059669;
}

.refresh-btn {
  padding: 16rpx 20rpx;
  border-radius: 16rpx;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(34, 197, 94, 0.3);
  transition: all 0.3s ease;
}

.refresh-btn:active {
  transform: scale(0.95);
}

.refresh-icon {
  font-size: 24rpx;
  color: white;
  font-weight: bold;
}

.loading-section {
  padding: 40rpx;
}

.skeleton-container {
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.skeleton-report-item {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  border: 1rpx solid rgba(34, 197, 94, 0.1);
  animation: skeleton-shimmer 1.5s infinite;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.skeleton-info {
  flex: 1;
}

.skeleton-title {
  height: 32rpx;
  background: linear-gradient(90deg, #e8f5e8 0%, #d1fae5 50%, #e8f5e8 100%);
  border-radius: 4rpx;
  margin-bottom: 16rpx;
  width: 60%;
}

.skeleton-date {
  height: 24rpx;
  background: linear-gradient(90deg, #e8f5e8 0%, #d1fae5 50%, #e8f5e8 100%);
  border-radius: 4rpx;
  width: 40%;
}

.skeleton-score {
  width: 80rpx;
  height: 60rpx;
  background: linear-gradient(90deg, #e8f5e8 0%, #d1fae5 50%, #e8f5e8 100%);
  border-radius: 8rpx;
}

.skeleton-content {
  height: 60rpx;
  background: linear-gradient(90deg, #e8f5e8 0%, #d1fae5 50%, #e8f5e8 100%);
  border-radius: 4rpx;
  width: 100%;
}

@keyframes skeleton-shimmer {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

.reports-list {
  padding: 20rpx 40rpx 40rpx;
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.report-item {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(34, 197, 94, 0.1);
  border: 1rpx solid rgba(34, 197, 94, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.report-item:active {
  transform: translateY(-2rpx) scale(0.98);
  box-shadow: 0 12rpx 40rpx rgba(34, 197, 94, 0.2);
}

.fade-in {
  animation: fadeIn 0.6s ease forwards;
  opacity: 0;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.report-info {
  flex: 1;
}

.report-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #059669;
  display: block;
  margin-bottom: 8rpx;
}

.report-subtitle {
  font-size: 26rpx;
  color: #666;
  display: block;
  margin-bottom: 8rpx;
}

.report-date {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.report-score {
  background: #f0f0f0;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
  text-align: center;
  min-width: 80rpx;
}

.score-text {
  font-size: 28rpx;
  font-weight: bold;
}

.score-excellent {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(5, 150, 105, 0.3);
}

.score-good {
  background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(34, 197, 94, 0.3);
}

.score-average {
  background: linear-gradient(135deg, #65a30d 0%, #84cc16 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(132, 204, 22, 0.3);
}

.score-poor {
  background: linear-gradient(135deg, #ca8a04 0%, #eab308 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(234, 179, 8, 0.3);
}

.score-critical {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(239, 68, 68, 0.3);
}

.report-summary {
  display: flex;
  gap: 40rpx;
  margin-bottom: 16rpx;
}

.summary-item {
  text-align: center;
}

.summary-label {
  font-size: 24rpx;
  color: #999;
  display: block;
  margin-bottom: 8rpx;
}

.summary-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #059669;
  display: block;
}

.report-arrow {
  position: absolute;
  right: 32rpx;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.3;
}

.arrow {
  font-size: 32rpx;
  color: #666;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400rpx;
  padding: 40rpx;
}

.empty-content {
  text-align: center;
}

.empty-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #059669;
  display: block;
  margin-bottom: 16rpx;
}

.empty-desc {
  font-size: 28rpx;
  color: #666;
  display: block;
  margin-bottom: 40rpx;
  line-height: 1.6;
}

.start-btn {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
  padding: 24rpx 48rpx;
  border-radius: 48rpx;
  display: inline-block;
  font-size: 28rpx;
  font-weight: bold;
  box-shadow: 0 8rpx 24rpx rgba(5, 150, 105, 0.3);
  transition: all 0.3s ease;
}

.start-btn:active {
  transform: translateY(2rpx) scale(0.98);
  box-shadow: 0 4rpx 12rpx rgba(5, 150, 105, 0.4);
}

.btn-text {
  color: white;
}
</style>
