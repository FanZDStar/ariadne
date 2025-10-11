<!-- 风险评估报告详情页面 -->
<!-- file: ariadne/frontend/src/pages/risk-report/report-detail.vue -->
<template>
  <view class="report-detail-page">
    <!-- 页面头部 -->
    <view class="header">
      <text class="title">心理状态评估报告</text>
      <text class="date" v-if="report">{{
        formatDate(report.report_generated_time)
      }}</text>
    </view>

    <!-- 报告内容 -->
    <view class="report-content" v-if="report">
      <!-- 会话信息 -->
      <view class="session-section">
        <text class="section-title">相关会话</text>
        <view class="session-info">
          <text class="session-title">{{
            report.session_title || "未知会话"
          }}</text>
          <text class="session-meta">ID: {{ report.session_id }}</text>
        </view>
      </view>

      <!-- 风险等级概览 -->
      <view class="risk-overview" :class="'risk-' + report.overall_risk_level">
        <view class="risk-header">
          <text class="risk-icon">{{
            getRiskIcon(report.overall_risk_level)
          }}</text>
          <text class="risk-title">{{
            getRiskTitle(report.overall_risk_level)
          }}</text>
        </view>
        <view class="risk-score">
          <text class="score-number">{{
            report.overall_risk_score.toFixed(1)
          }}</text>
          <text class="score-text">/100</text>
        </view>
      </view>

      <!-- 基本统计 -->
      <view class="stats-section">
        <text class="section-title">对话统计</text>
        <view class="stats-grid">
          <view class="stat-item">
            <text class="stat-number">{{ report.total_messages }}</text>
            <text class="stat-label">总消息数</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ report.risk_messages_count }}</text>
            <text class="stat-label">风险消息</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ report.version }}</text>
            <text class="stat-label">报告版本</text>
          </view>
        </view>
      </view>

      <!-- 摘要 -->
      <view class="summary-section" v-if="report.summary">
        <text class="section-title">报告摘要</text>
        <text class="summary-text">{{ report.summary }}</text>
      </view>

      <!-- AI专业分析 -->
      <view class="ai-analysis-section" v-if="report.ai_analysis">
        <text class="section-title">AI专业分析</text>
        <view class="analysis-container">
          <MarkdownRenderer :content="report.ai_analysis" />
        </view>
      </view>

      <!-- 检测到的关键词 -->
      <view class="keywords-section" v-if="report.detected_keywords && report.detected_keywords.length > 0">
        <text class="section-title">检测关键词</text>
        <view class="keywords-list">
          <text class="keyword-tag" v-for="(keyword, index) in report.detected_keywords" :key="index">
            {{ keyword }}
          </text>
        </view>
      </view>

      <!-- 专业建议 -->
      <view class="recommendations-section" v-if="report.recommendations && report.recommendations.length > 0">
        <text class="section-title">专业建议</text>
        <view class="recommendations-list">
          <view class="recommendation-item" v-for="(rec, index) in report.recommendations" :key="index">
            <text class="rec-bullet">•</text>
            <text class="rec-text">{{ rec }}</text>
          </view>
        </view>
      </view>

      <!-- 时间信息 -->
      <view class="time-info-section">
        <text class="section-title">时间信息</text>
        <view class="time-list">
          <view class="time-item" v-if="report.conversation_start_time">
            <text class="time-label">对话开始：</text>
            <text class="time-value">{{
              formatDateTime(report.conversation_start_time)
            }}</text>
          </view>
          <view class="time-item" v-if="report.conversation_end_time">
            <text class="time-label">对话结束：</text>
            <text class="time-value">{{
              formatDateTime(report.conversation_end_time)
            }}</text>
          </view>
          <view class="time-item">
            <text class="time-label">报告生成：</text>
            <text class="time-value">{{
              formatDateTime(report.report_generated_time)
            }}</text>
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-buttons">
        <button class="btn btn-primary" @click="getHelp">获取帮助</button>
      </view>

      <!-- 免责声明 -->
      <view class="disclaimer">
        <text class="disclaimer-text">
          此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。
          如需紧急帮助，请拨打心理危机干预热线：400-161-9995
        </text>
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading" v-else-if="loading">
      <text>正在加载报告...</text>
    </view>

    <!-- 错误状态 -->
    <view class="error" v-else>
      <text>无法加载报告</text>
      <button class="retry-btn" @click="loadReport">重试</button>
    </view>

    <!-- 回到顶部组件 -->
    <BackToTop ref="backToTop" :bottom="150" @start-scroll-listener="startScrollListener"
      @remove-scroll-listener="removeScrollListener" />
  </view>
</template>

<script>
// 引入危机工具类
import { CrisisUtils } from "../../utils/crisisApi.js";
import BackToTop from "../../components/BackToTop.vue";
import MarkdownRenderer from "../../components/MarkdownRenderer.vue";

export default {
  components: {
    BackToTop,
    MarkdownRenderer,
  },
  data() {
    return {
      report: null,
      loading: true,
      reportId: null,
    };
  },

  onLoad(options) {
    this.reportId = options.reportId;
    if (this.reportId) {
      this.loadReport();
    }
  },

  methods: {
    /**
     * 加载报告详情
     */
    async loadReport() {
      this.loading = true;
      try {
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
            }/risk-assessment/reports/${this.reportId}`,
          method: "GET",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
          },
        });

        if (response.statusCode === 200) {
          this.report = response.data;
        } else {
          throw new Error("加载失败");
        }
      } catch (error) {
        console.error("加载报告失败:", error);
        uni.showToast({
          title: "加载报告失败",
          icon: "none",
        });
      } finally {
        this.loading = false;
      }
    },

    /**
     * 获取风险图标
     */
    getRiskIcon(level) {
      const icons = {
        critical: "",
        high: "",
        medium: "",
        low: "",
      };
      return icons[level] || "";
    },

    /**
     * 获取风险标题
     */
    getRiskTitle(level) {
      const titles = {
        critical: "高危风险",
        high: "较高风险",
        medium: "中等风险",
        low: "较低风险",
      };
      return titles[level] || "未知风险";
    },

    /**
     * 格式化日期
     */
    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },

    /**
     * 格式化日期时间
     */
    formatDateTime(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleString();
    },

    /**
     * 获取帮助
     */
    getHelp() {
      uni.showActionSheet({
        itemList: [
          "防护技能训练",
          "技能学习",
          "情感对话",
          "心理援助热线",
        ],
        success: (res) => {
          switch (res.tapIndex) {
            case 0:
              this.goToProtectionSkills();
              break;
            case 1:
              this.goToSkillLearning();
              break;
            case 2:
              this.goToEmotionalChat();
              break;
            case 3:
              this.showHelpHotline();
              break;
          }
        },
      });
    },

    /**
     * 跳转到防护技能训练
     */
    goToProtectionSkills() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/protection-drill",
      });
    },

    /**
     * 跳转到技能学习
     */
    goToSkillLearning() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/interpersonal-wisdom",
      });
    },

    /**
     * 跳转到情感对话
     */
    goToEmotionalChat() {
      uni.navigateTo({
        url: "/pages/AI-emotional-chat/chat-context/chat-context",
      });
    },

    /**
     * 显示心理援助热线
     */
    showHelpHotline() {
      uni.showModal({
        title: "心理援助热线",
        content:
          "如需紧急帮助，请拨打：\n\n• 全国心理援助热线：400-161-9995\n• 北京危机干预热线：400-161-9995\n• 上海心理援助热线：021-34289888\n• 深圳心理援助热线：0755-25629459",
        showCancel: true,
        cancelText: "取消",
        confirmText: "拨打热线",
        success: (res) => {
          if (res.confirm) {
            uni.makePhoneCall({
              phoneNumber: "400-161-9995",
            });
          }
        },
      });
    },

    // 滚动监听相关方法
    startScrollListener() {
      // H5环境使用window.addEventListener
      if (typeof window !== "undefined") {
        this.handleScroll = () => {
          const scrollTop =
            window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
          if (this.$refs.backToTop) {
            this.$refs.backToTop.updateVisibility(scrollTop);
          }
        };
        window.addEventListener("scroll", this.handleScroll);
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
      if (typeof window !== "undefined" && this.handleScroll) {
        window.removeEventListener("scroll", this.handleScroll);
      } else if (typeof uni !== "undefined" && uni.offPageScroll) {
        uni.offPageScroll();
      }
    },
  },
};
</script>

<style scoped>
.report-detail-page {
  padding: 24rpx;
  background: #f8fafe;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 32rpx;
  background: white;
  border-radius: 20rpx;
  padding: 40rpx 32rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
}

.title {
  display: block;
  font-size: 40rpx;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12rpx;
  letter-spacing: 1rpx;
}

.date {
  display: block;
  font-size: 26rpx;
  color: #64748b;
  background: #f1f5f9;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  display: inline-block;
  font-weight: 500;
}

.report-content {
  background: white;
  border-radius: 20rpx;
  padding: 36rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
}

.risk-overview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-radius: 16rpx;
  margin-bottom: 32rpx;
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

.risk-header {
  display: flex;
  align-items: center;
}

.risk-icon {
  font-size: 0rpx;
  margin-right: 0rpx;
  width: 0rpx;
}

.risk-title {
  font-size: 32rpx;
  font-weight: 700;
}

.risk-score {
  text-align: right;
}

.score-number {
  font-size: 48rpx;
  font-weight: 700;
}

.score-text {
  font-size: 24rpx;
  opacity: 0.7;
  font-weight: 500;
}

.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 24rpx;
  position: relative;
  padding-left: 16rpx;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4rpx;
  height: 24rpx;
  background: #3b82f6;
  border-radius: 2rpx;
}

.session-section {
  margin-bottom: 32rpx;
}

.session-info {
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 16rpx;
  border-left: 4rpx solid #3b82f6;
  border: 1rpx solid #e2e8f0;
}

.session-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8rpx;
}

.session-meta {
  font-size: 24rpx;
  color: #64748b;
  font-weight: 500;
}

.stats-section {
  margin-bottom: 32rpx;
}

.stats-grid {
  display: flex;
  justify-content: space-around;
  background: #f8fafc;
  padding: 32rpx 24rpx;
  border-radius: 16rpx;
  border: 1rpx solid #e2e8f0;
}

.stat-item {
  text-align: center;
  position: relative;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -40rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 1rpx;
  height: 60rpx;
  background: #e2e8f0;
}

.stat-number {
  display: block;
  font-size: 36rpx;
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

.summary-section,
.ai-analysis-section {
  margin-bottom: 32rpx;
}

.summary-text {
  display: block;
  font-size: 28rpx;
  line-height: 1.6;
  color: #374151;
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e2e8f0;
  font-weight: 400;
}

.analysis-container {
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e2e8f0;
}

.analysis-text {
  display: block;
  font-size: 28rpx;
  line-height: 1.6;
  color: #374151;
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 12rpx;
  font-weight: 400;
}

.keywords-section {
  margin-bottom: 32rpx;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.keyword-tag {
  background: #eff6ff;
  color: #2563eb;
  padding: 12rpx 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  font-weight: 500;
  border: 1rpx solid #bfdbfe;
}

.recommendations-section {
  margin-bottom: 32rpx;
}

.recommendations-list {
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e2e8f0;
}

.recommendation-item {
  display: flex;
  margin-bottom: 16rpx;
}

.recommendation-item:last-child {
  margin-bottom: 0;
}

.rec-bullet {
  color: #3b82f6;
  margin-right: 16rpx;
  font-weight: 700;
  font-size: 28rpx;
}

.rec-text {
  flex: 1;
  font-size: 28rpx;
  line-height: 1.6;
  color: #374151;
  font-weight: 400;
}

.time-info-section {
  margin-bottom: 32rpx;
}

.time-list {
  background: #f8fafc;
  padding: 24rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e2e8f0;
}

.time-item {
  display: flex;
  margin-bottom: 16rpx;
  align-items: center;
}

.time-item:last-child {
  margin-bottom: 0;
}

.time-label {
  width: 160rpx;
  font-size: 26rpx;
  color: #64748b;
  font-weight: 500;
}

.time-value {
  flex: 1;
  font-size: 26rpx;
  color: #1e293b;
  font-weight: 400;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 32rpx;
}

.btn {
  padding: 28rpx 48rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  text-align: center;
  border: none;
  width: 100%;
  max-width: 400rpx;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  box-shadow: 0 4rpx 20rpx rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2rpx);
  box-shadow: 0 6rpx 25rpx rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: white;
  color: #3b82f6;
  border: 2rpx solid #3b82f6;
}

.disclaimer {
  background: #fef3c7;
  padding: 24rpx;
  border-radius: 12rpx;
  border-left: 4rpx solid #f59e0b;
  border: 1rpx solid #fed7aa;
}

.disclaimer-text {
  font-size: 24rpx;
  line-height: 1.6;
  color: #92400e;
  font-weight: 400;
}

.loading,
.error {
  text-align: center;
  padding: 120rpx 32rpx;
  background: white;
  border-radius: 20rpx;
  box-shadow: 0 2rpx 20rpx rgba(59, 130, 246, 0.08);
  border: 1rpx solid #e2e8f0;
  margin: 24rpx;
}

.loading text,
.error text {
  color: #64748b;
  font-size: 28rpx;
  font-weight: 500;
}

.retry-btn {
  margin-top: 24rpx;
  background: #3b82f6;
  color: white;
  padding: 24rpx 48rpx;
  border-radius: 16rpx;
  border: none;
  font-size: 28rpx;
  font-weight: 600;
  box-shadow: 0 4rpx 20rpx rgba(59, 130, 246, 0.3);
}
</style>
