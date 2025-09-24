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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20rpx;
}

.header {
  text-align: center;
  margin-bottom: 30rpx;
}

.title {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 10rpx;
}

.subtitle {
  display: block;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.overview-section {
  margin-bottom: 30rpx;
}

.stats-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15rpx;
  padding: 30rpx;
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  display: block;
  font-size: 22rpx;
  color: #666;
  margin-top: 10rpx;
}

.filter-section {
  margin-bottom: 30rpx;
}

.filter-picker {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 25rpx;
  padding: 20rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.picker-arrow {
  color: #667eea;
}

.reports-section {
  margin-bottom: 100rpx;
}

.report-card {
  background: white;
  border-radius: 15rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  position: relative;
}

.report-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.title-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
  margin-right: 20rpx;
  line-height: 1.4;
}

.report-date {
  font-size: 22rpx;
  color: #999;
  white-space: nowrap;
}

.report-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 15rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.risk-info {
  display: flex;
  align-items: center;
  gap: 15rpx;
}

.risk-badge {
  display: flex;
  align-items: center;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
}

.risk-critical {
  background: #ffebee;
  color: #c62828;
}

.risk-high {
  background: #fff3e0;
  color: #ef6c00;
}

.risk-medium {
  background: #e3f2fd;
  color: #1565c0;
}

.risk-low {
  background: #e8f5e8;
  color: #2e7d32;
}

.risk-icon {
  margin-right: 8rpx;
  font-size: 20rpx;
}

.risk-text {
  font-size: 22rpx;
  font-weight: bold;
}

.risk-score {
  font-size: 24rpx;
  font-weight: bold;
  color: #667eea;
}

.stats-info {
  display: flex;
  gap: 15rpx;
}

.stat-text {
  font-size: 22rpx;
  color: #666;
  background: #f8f9fa;
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
}

.report-summary {
  margin-bottom: 20rpx;
}

.summary-text {
  font-size: 24rpx;
  line-height: 1.5;
  color: #555;
}

.trend-section {
  padding-top: 15rpx;
  border-top: 1rpx solid #f0f0f0;
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.trend-arrow {
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18rpx;
  font-weight: bold;
}

.trend-improving .trend-arrow {
  background: #e8f5e8;
  color: #2e7d32;
}

.trend-worsening .trend-arrow {
  background: #ffebee;
  color: #c62828;
}

.trend-stable .trend-arrow {
  background: #f5f5f5;
  color: #666;
}

.trend-text {
  font-size: 20rpx;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  display: block;
  margin-bottom: 20rpx;
}

.empty-title {
  display: block;
  font-size: 28rpx;
  color: white;
  margin-bottom: 10rpx;
}

.empty-desc {
  display: block;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 30rpx;
}

.empty-btn {
  background: white;
  color: #667eea;
  padding: 20rpx 40rpx;
  border-radius: 25rpx;
  border: none;
}

.load-more {
  text-align: center;
  margin: 30rpx 0;
}

.load-more-btn {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  padding: 20rpx 40rpx;
  border-radius: 25rpx;
  border: none;
}

.loading {
  text-align: center;
  padding: 50rpx 0;
  color: white;
}
</style>
