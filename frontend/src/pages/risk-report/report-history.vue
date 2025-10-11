<!-- 风险评估报告历史页面 -->
<!-- file: ariadne/frontend/src/pages/risk-report/report-history.vue -->
<template>
  <view class="report-history-page">
    <!-- 页面头部 -->
    <view class="header">
      <text class="title">📈 心理状态历史</text>
      <text class="subtitle">追踪您的心理健康变化</text>
    </view>

    <!-- 统计概览 -->
    <view class="overview-section" v-if="statistics">
      <view class="stats-card">
        <view class="stat-item">
          <text class="stat-number">{{ statistics.total_reports }}</text>
          <text class="stat-label">总报告数</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{
            statistics.avg_risk_score.toFixed(1)
          }}</text>
          <text class="stat-label">平均风险分</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ statistics.improvement_trend }}%</text>
          <text class="stat-label">改善趋势</text>
        </view>
      </view>
    </view>

    <!-- 筛选器 -->
    <view class="filter-section">
      <picker
        mode="selector"
        :value="filterIndex"
        :range="filterOptions"
        @change="onFilterChange"
      >
        <view class="filter-picker">
          <text>{{ filterOptions[filterIndex] }}</text>
          <text class="picker-arrow">▼</text>
        </view>
      </picker>
    </view>

    <!-- 报告列表 -->
    <view class="reports-section">
      <view
        class="report-card"
        v-for="(report, index) in filteredReports"
        :key="report.id"
        @click="viewReport(report)"
      >
        <!-- 报告标题 -->
        <view class="report-title">
          <text class="title-text">{{
            report.session_title || "心理状态评估报告"
          }}</text>
          <text class="report-date">{{
            formatDate(report.report_generated_time)
          }}</text>
        </view>

        <!-- 危机程度和统计信息 -->
        <view class="report-meta">
          <view class="risk-info">
            <view
              class="risk-badge"
              :class="'risk-' + report.overall_risk_level"
            >
              <text class="risk-icon">{{
                getRiskIcon(report.overall_risk_level)
              }}</text>
              <text class="risk-text">{{
                getRiskTitle(report.overall_risk_level)
              }}</text>
            </view>
            <text class="risk-score"
              >Lv{{ report.overall_risk_score.toFixed(1) }}</text
            >
          </view>
          <view class="stats-info">
            <text class="stat-text">{{ report.total_messages }}条消息</text>
            <text class="stat-text" v-if="report.risk_messages_count > 0"
              >{{ report.risk_messages_count }}条风险</text
            >
          </view>
        </view>

        <!-- 报告概要 -->
        <view class="report-summary">
          <text class="summary-text" v-if="report.summary">
            {{ truncateText(report.summary, 120) }}
          </text>
          <text class="summary-text" v-else>
            该报告基于对话分析生成，风险评分为
            {{ report.overall_risk_score.toFixed(1) }} 分。
          </text>
        </view>

        <!-- 趋势指示器 -->
        <view class="trend-section" v-if="index < reports.length - 1">
          <view
            class="trend-indicator"
            :class="getTrendClass(report, reports[index + 1])"
          >
            <text class="trend-arrow">{{
              getTrendArrow(report, reports[index + 1])
            }}</text>
            <text class="trend-text">{{
              getTrendText(report, reports[index + 1])
            }}</text>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view class="empty-state" v-if="filteredReports.length === 0 && !loading">
        <text class="empty-icon">📊</text>
        <text class="empty-title">暂无报告</text>
        <text class="empty-desc"
          >开始聊天后，系统会自动生成心理状态评估报告</text
        >
        <button class="empty-btn" @click="goToChat">开始聊天</button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more" v-if="hasMore && !loading">
      <button class="load-more-btn" @click="loadMore">加载更多</button>
    </view>

    <!-- 加载状态 -->
    <view class="loading" v-if="loading">
      <text>正在加载...</text>
    </view>

   <BackToTop 
      ref="backToTop"
      :bottom="150"
      @start-scroll-listener="startScrollListener"
      @remove-scroll-listener="removeScrollListener"
    />
  </view>
</template>

<script>
import BackToTop from "../../components/BackToTop.vue";

export default {
  components: {
    BackToTop,
  },
  data() {
    return {
      reports: [],
      statistics: null,
      loading: false,
      hasMore: true,
      page: 1,
      pageSize: 10,
      filterIndex: 0,
      filterOptions: [
        "全部报告",
        "最近一周",
        "最近一月",
        "最近三月",
        "高风险报告",
      ],
    };
  },

  computed: {
    filteredReports() {
      let filtered = [...this.reports];

      switch (this.filterIndex) {
        case 1: // 最近一周
          filtered = this.filterByDays(filtered, 7);
          break;
        case 2: // 最近一月
          filtered = this.filterByDays(filtered, 30);
          break;
        case 3: // 最近三月
          filtered = this.filterByDays(filtered, 90);
          break;
        case 4: // 高风险报告
          filtered = filtered.filter((report) =>
            ["critical", "high"].includes(report.overall_risk_level)
          );
          break;
      }

      return filtered;
    },
  },

  onLoad() {
    this.loadReports();
    this.loadStatistics();
  },

  methods: {
    /**
     * 加载报告列表
     */
    async loadReports(isLoadMore = false) {
      if (this.loading) return;

      this.loading = true;
      try {
        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/risk-assessment/reports-history`,
          method: "GET",
          data: {
            page: isLoadMore ? this.page : 1,
            page_size: this.pageSize,
          },
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
          },
        });

        if (response.statusCode === 200) {
          // 后端直接返回数组，不是包含在reports字段中
          const newReports = response.data || [];

          if (isLoadMore) {
            this.reports = [...this.reports, ...newReports];
          } else {
            this.reports = newReports;
          }

          this.hasMore = newReports.length === this.pageSize;
          this.page = isLoadMore ? this.page + 1 : 2;
        } else {
          throw new Error("加载失败");
        }
      } catch (error) {
        console.error("加载报告列表失败:", error);
        uni.showToast({
          title: "加载失败",
          icon: "none",
        });
      } finally {
        this.loading = false;
      }
    },

    /**
     * 加载统计信息
     */
    async loadStatistics() {
      try {
        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/risk-assessment/statistics`,
          method: "GET",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
          },
        });

        if (response.statusCode === 200) {
          this.statistics = response.data;
        }
      } catch (error) {
        console.error("加载统计信息失败:", error);
      }
    },

    /**
     * 加载更多
     */
    loadMore() {
      this.loadReports(true);
    },

    /**
     * 筛选器变化
     */
    onFilterChange(e) {
      this.filterIndex = e.detail.value;
    },

    /**
     * 按天数筛选
     */
    filterByDays(reports, days) {
      const now = new Date();
      const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

      return reports.filter((report) => {
        const reportDate = new Date(report.report_generated_time);
        return reportDate > cutoff;
      });
    },

    /**
     * 查看报告详情
     */
    viewReport(report) {
      uni.navigateTo({
        url: `/pages/risk-report/report-detail?reportId=${report.report_id}`,
      });
    },

    /**
     * 获取风险图标
     */
    getRiskIcon(level) {
      const icons = {
        critical: "🚨",
        high: "⚠️",
        medium: "⚡",
        low: "✅",
      };
      return icons[level] || "❓";
    },

    /**
     * 获取风险标题
     */
    getRiskTitle(level) {
      const titles = {
        critical: "高危",
        high: "较高",
        medium: "中等",
        low: "较低",
      };
      return titles[level] || "未知";
    },

    /**
     * 格式化日期
     */
    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      const now = new Date();
      const diff = now.getTime() - date.getTime();
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));

      if (days === 0) {
        return "今天";
      } else if (days === 1) {
        return "昨天";
      } else if (days < 7) {
        return `${days}天前`;
      } else {
        return date.toLocaleDateString();
      }
    },

    /**
     * 截断文本
     */
    truncateText(text, maxLength) {
      if (!text) return "";
      return text.length > maxLength
        ? text.substring(0, maxLength) + "..."
        : text;
    },

    /**
     * 获取趋势类别
     */
    getTrendClass(current, previous) {
      if (!previous) return "";

      const currentScore = current.overall_risk_score;
      const previousScore = previous.overall_risk_score;

      if (currentScore < previousScore) {
        return "trend-improving";
      } else if (currentScore > previousScore) {
        return "trend-worsening";
      } else {
        return "trend-stable";
      }
    },

    /**
     * 获取趋势箭头
     */
    getTrendArrow(current, previous) {
      if (!previous) return "";

      const currentScore = current.overall_risk_score;
      const previousScore = previous.overall_risk_score;

      if (currentScore < previousScore) {
        return "↓";
      } else if (currentScore > previousScore) {
        return "↑";
      } else {
        return "→";
      }
    },

    /**
     * 获取趋势文本
     */
    getTrendText(current, previous) {
      if (!previous) return "";

      const currentScore = current.overall_risk_score;
      const previousScore = previous.overall_risk_score;
      const diff = Math.abs(currentScore - previousScore);

      if (currentScore < previousScore) {
        return `改善 ${diff.toFixed(1)}分`;
      } else if (currentScore > previousScore) {
        return `上升 ${diff.toFixed(1)}分`;
      } else {
        return "保持稳定";
      }
    },

    /**
     * 前往聊天页面
     */
    goToChat() {
      uni.switchTab({
        url: "/pages/index/index",
      });
    },

    // 滚动监听相关方法
    startScrollListener() {
      // H5环境使用window.addEventListener
      if (typeof window !== 'undefined') {
        this.handleScroll = () => {
          const scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
          if (this.$refs.backToTop) {
            this.$refs.backToTop.updateVisibility(scrollTop);
          }
        };
        window.addEventListener('scroll', this.handleScroll);
      } else {
        // 小程序环境使用uni.onPageScroll
        uni.onPageScroll((res) => {
          if (this.$refs.backToTop) {
            this.$refs.backToTop.updateVisibility(res.scrollTop);
          }
        });
      }
    },

    removeScrollListener() {
      if (typeof window !== 'undefined' && this.handleScroll) {
        window.removeEventListener('scroll', this.handleScroll);
      } else if (typeof uni !== 'undefined' && uni.offPageScroll) {
        uni.offPageScroll();
      }
    },

    /**
     * 回到顶部成功回调
     */
    onScrollToTopSuccess() {
      console.log("已回到顶部");
    },
  },
};
</script>

<style scoped>
.report-history-page {
  background: #f8fafe;
  min-height: 100vh;
  padding: 24rpx;
}

.header {
  text-align: center;
  margin-bottom: 40rpx;
  padding: 40rpx 0;
  background: white;
  border-radius: 20rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  margin: 24rpx 0 40rpx 0;
}

.title {
  display: block;
  font-size: 40rpx;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12rpx;
  letter-spacing: 1rpx;
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: #64748b;
  font-weight: 400;
}

.overview-section {
  margin-bottom: 32rpx;
}

.stats-card {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx 32rpx;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
}

.stat-item {
  text-align: center;
  position: relative;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -50rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 1rpx;
  height: 60rpx;
  background: #e2e8f0;
}

.stat-number {
  display: block;
  font-size: 44rpx;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 8rpx;
}

.stat-label {
  display: block;
  font-size: 24rpx;
  color: #64748b;
  font-weight: 500;
}

.filter-section {
  margin-bottom: 32rpx;
}

.filter-picker {
  background: white;
  border-radius: 16rpx;
  padding: 24rpx 32rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2rpx 16rpx rgba(59, 130, 246, 0.06);
  border: 1rpx solid #e2e8f0;
  font-size: 28rpx;
  color: #374151;
  font-weight: 500;
}

.picker-arrow {
  color: #3b82f6;
  font-size: 24rpx;
  font-weight: 600;
}

.reports-section {
  margin-bottom: 120rpx;
}

.report-card {
  background: white;
  border-radius: 20rpx;
  padding: 36rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
  position: relative;
  transition: all 0.3s ease;
}

.report-card:hover {
  transform: translateY(-2rpx);
  box-shadow: 0 6rpx 30rpx rgba(59, 130, 246, 0.12);
}

.report-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.title-text {
  font-size: 30rpx;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
  margin-right: 24rpx;
  line-height: 1.5;
}

.report-date {
  font-size: 24rpx;
  color: #64748b;
  white-space: nowrap;
  background: #f1f5f9;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  font-weight: 500;
}

.report-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f1f5f9;
}

.risk-info {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.risk-badge {
  display: flex;
  align-items: center;
  padding: 12rpx 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  font-weight: 600;
  border: 1rpx solid transparent;
}

.risk-critical {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.risk-high {
  background: #fef3c7;
  color: #d97706;
  border-color: #fed7aa;
}

.risk-medium {
  background: #dbeafe;
  color: #2563eb;
  border-color: #bfdbfe;
}

.risk-low {
  background: #dcfce7;
  color: #16a34a;
  border-color: #bbf7d0;
}

.risk-icon {
  margin-right: 8rpx;
  font-size: 22rpx;
}

.risk-text {
  font-size: 24rpx;
  font-weight: 600;
}

.risk-score {
  font-size: 26rpx;
  font-weight: 700;
  color: #3b82f6;
  background: #eff6ff;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  border: 1rpx solid #dbeafe;
}

.stats-info {
  display: flex;
  gap: 16rpx;
}

.stat-text {
  font-size: 24rpx;
  color: #4b5563;
  background: #f8fafc;
  padding: 10rpx 16rpx;
  border-radius: 12rpx;
  font-weight: 500;
  border: 1rpx solid #e2e8f0;
}

.report-summary {
  margin-bottom: 24rpx;
}

.summary-text {
  font-size: 26rpx;
  line-height: 1.6;
  color: #374151;
  font-weight: 400;
}

.trend-section {
  padding-top: 20rpx;
  border-top: 1rpx solid #f1f5f9;
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.trend-arrow {
  width: 36rpx;
  height: 36rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  font-weight: 700;
}

.trend-improving .trend-arrow {
  background: #dcfce7;
  color: #16a34a;
}

.trend-worsening .trend-arrow {
  background: #fef2f2;
  color: #dc2626;
}

.trend-stable .trend-arrow {
  background: #f1f5f9;
  color: #64748b;
}

.trend-text {
  font-size: 24rpx;
  color: #4b5563;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 120rpx 32rpx;
  background: white;
  border-radius: 20rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
}

.empty-icon {
  font-size: 100rpx;
  display: block;
  margin-bottom: 24rpx;
  opacity: 0.8;
}

.empty-title {
  display: block;
  font-size: 32rpx;
  color: #1e293b;
  margin-bottom: 12rpx;
  font-weight: 600;
}

.empty-desc {
  display: block;
  font-size: 26rpx;
  color: #64748b;
  margin-bottom: 40rpx;
  line-height: 1.5;
}

.empty-btn {
  background: #3b82f6;
  color: white;
  padding: 24rpx 48rpx;
  border-radius: 16rpx;
  border: none;
  font-size: 28rpx;
  font-weight: 600;
  box-shadow: 0 4rpx 20rpx rgba(59, 130, 246, 0.3);
}

.load-more {
  text-align: center;
  margin: 40rpx 0;
}

.load-more-btn {
  background: white;
  color: #3b82f6;
  padding: 24rpx 48rpx;
  border-radius: 16rpx;
  border: 2rpx solid #3b82f6;
  font-size: 28rpx;
  font-weight: 600;
  box-shadow: 0 2rpx 16rpx rgba(59, 130, 246, 0.1);
}

.loading {
  text-align: center;
  padding: 60rpx 0;
  color: #64748b;
  font-size: 28rpx;
  font-weight: 500;
}
</style>
