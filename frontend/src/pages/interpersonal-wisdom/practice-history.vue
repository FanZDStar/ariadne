<template>
  <view class="practice-history-container">
    <view class="header">
      <text class="title">对话练习记录</text>
      <text class="subtitle">回顾学习成果，持续提升沟通技能</text>
    </view>

    <!-- 统计信息 -->
    <view class="stats-section">
      <view class="stat-card">
        <text class="stat-number">{{ totalSessions }}</text>
        <text class="stat-label">总练习次数</text>
      </view>
      <view class="stat-card">
        <text class="stat-number">{{ totalTime }}</text>
        <text class="stat-label">总练习时长</text>
      </view>
      <view class="stat-card">
        <text class="stat-number">{{ avgScore }}</text>
        <text class="stat-label">平均得分</text>
      </view>
    </view>

    <!-- 筛选器 -->
    <view class="filter-section">
      <view class="filter-tabs">
        <view
          v-for="filter in filters"
          :key="filter.value"
          class="filter-tab"
          :class="{ active: activeFilter === filter.value }"
          @click="activeFilter = filter.value"
        >
          <text class="filter-text">{{ filter.label }}</text>
        </view>
      </view>
    </view>

    <!-- 会话列表 -->
    <view class="sessions-list">
      <!-- 加载状态 -->
      <view v-if="loading" class="loading-container">
        <view v-for="n in 3" :key="n" class="session-skeleton">
          <view class="skeleton-header">
            <view class="skeleton-title"></view>
            <view class="skeleton-time"></view>
          </view>
          <view class="skeleton-content"></view>
          <view class="skeleton-tags">
            <view class="skeleton-tag"></view>
            <view class="skeleton-tag"></view>
          </view>
        </view>
      </view>

      <!-- 会话项 -->
      <view v-else>
        <view
          v-for="session in filteredSessions"
          :key="session.id"
          class="session-item"
          @click="viewSession(session)"
        >
          <view class="session-header">
            <view class="session-info">
              <text class="session-title">{{ session.session_title }}</text>
              <text class="session-scenario">{{
                session.practice_scenario_name
              }}</text>
            </view>
            <view class="session-meta">
              <text class="session-time">{{
                formatTime(session.created_at)
              }}</text>
              <view v-if="session.practice_quality_score" class="session-score">
                <text class="score-text"
                  >{{ session.practice_quality_score }}分</text
                >
              </view>
            </view>
          </view>

          <view class="session-content">
            <text class="session-description">{{
              session.scenario_description || "人际沟通练习"
            }}</text>
            <view class="session-stats">
              <text class="stat-item">{{ session.total_messages }}条消息</text>
              <text class="stat-separator">·</text>
              <text class="stat-item">{{
                formatDuration(session.practice_duration)
              }}</text>
            </view>
          </view>

          <view class="session-footer">
            <view class="session-tags">
              <text
                v-for="skill in session.skills_practiced"
                :key="skill"
                class="skill-tag"
                >{{ skill }}</text
              >
            </view>
            <view class="session-actions">
              <view class="action-icon" @click.stop="toggleFavorite(session)">
                <text class="icon">{{
                  session.is_favorite ? "❤️" : "🤍"
                }}</text>
              </view>
              <view class="action-icon" @click.stop="shareSession(session)">
                <text class="icon">📤</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 空状态 -->
        <view
          v-if="!loading && filteredSessions.length === 0"
          class="empty-state"
        >
          <text class="empty-icon">💭</text>
          <text class="empty-title">暂无练习记录</text>
          <text class="empty-desc">开始你的第一次AI对话练习吧！</text>
          <view class="empty-action" @click="startPractice">
            <text class="action-text">开始练习</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 悬浮按钮 -->
    <view class="fab" @click="startPractice">
      <text class="fab-icon">💬</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      sessions: [],
      loading: true,
      activeFilter: "all",
      filters: [
        { label: "全部", value: "all" },
        { label: "自我介绍", value: "self_introduction" },
        { label: "日常闲聊", value: "small_talk" },
        { label: "冲突解决", value: "conflict_resolution" },
        { label: "职场沟通", value: "workplace_communication" },
        { label: "情感表达", value: "dating_conversation" },
        { label: "公众演讲", value: "public_speaking" },
      ],
    };
  },

  computed: {
    filteredSessions() {
      if (this.activeFilter === "all") {
        return this.sessions;
      }
      return this.sessions.filter(
        (session) => session.practice_scenario === this.activeFilter
      );
    },

    totalSessions() {
      return this.sessions.length;
    },

    totalTime() {
      const totalSeconds = this.sessions.reduce(
        (sum, session) => sum + (session.practice_duration || 0),
        0
      );
      return this.formatDuration(totalSeconds);
    },

    avgScore() {
      const validScores = this.sessions.filter(
        (session) => session.practice_quality_score
      );
      if (validScores.length === 0) return "0.0";
      const sum = validScores.reduce(
        (sum, session) => sum + session.practice_quality_score,
        0
      );
      return (sum / validScores.length).toFixed(1);
    },
  },

  onLoad() {
    this.loadSessions();
  },

  onPullDownRefresh() {
    this.loadSessions().then(() => {
      uni.stopPullDownRefresh();
    });
  },

  methods: {
    async loadSessions() {
      try {
        this.loading = true;
        const token = uni.getStorageSync("access_token");

        if (!token) {
          uni.showToast({
            title: "请先登录",
            icon: "none",
          });
          return;
        }

        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/interpersonal-practice/sessions`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.sessions = response.data.sessions || [];
        } else {
          uni.showToast({
            title: "加载失败",
            icon: "none",
          });
        }
      } catch (error) {
        console.error("加载练习记录失败:", error);
        uni.showToast({
          title: "网络错误",
          icon: "none",
        });
      } finally {
        this.loading = false;
      }
    },

    viewSession(session) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/practice-detail?sessionId=${session.id}`,
      });
    },

    async toggleFavorite(session) {
      try {
        const token = uni.getStorageSync("access_token");
        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/interpersonal-practice/sessions/${session.id}/favorite`,
          method: "POST",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          data: {
            is_favorite: !session.is_favorite,
          },
        });

        if (response.statusCode === 200) {
          session.is_favorite = !session.is_favorite;
          uni.showToast({
            title: session.is_favorite ? "已收藏" : "已取消收藏",
            icon: "success",
          });
        }
      } catch (error) {
        console.error("切换收藏状态失败:", error);
      }
    },

    shareSession(session) {
      uni.showActionSheet({
        itemList: ["分享到微信", "复制链接", "导出记录"],
        success: (res) => {
          switch (res.tapIndex) {
            case 0:
              // 分享到微信逻辑
              break;
            case 1:
              // 复制链接逻辑
              break;
            case 2:
              // 导出记录逻辑
              break;
          }
        },
      });
    },

    startPractice() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/interactive-practice",
      });
    },

    formatTime(timeString) {
      const date = new Date(timeString);
      const now = new Date();
      const diffTime = now - date;
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) {
        return "今天";
      } else if (diffDays === 1) {
        return "昨天";
      } else if (diffDays < 7) {
        return `${diffDays}天前`;
      } else {
        return date.toLocaleDateString("zh-CN");
      }
    },

    formatDuration(seconds) {
      if (!seconds) return "0分钟";

      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);

      if (hours > 0) {
        return `${hours}小时${minutes}分钟`;
      } else {
        return `${minutes}分钟`;
      }
    },
  },
};
</script>

<style scoped>
.practice-history-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
  padding-bottom: 120rpx;
}

.header {
  padding: 80rpx 40rpx 40rpx;
  text-align: center;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #e8f4fd 100%);
}

.title {
  font-size: 56rpx;
  font-weight: 700;
  color: #1565c0;
  display: block;
  margin-bottom: 16rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #1976d2;
  opacity: 0.8;
}

.stats-section {
  display: flex;
  padding: 40rpx;
  gap: 20rpx;
}

.stat-card {
  flex: 1;
  background: white;
  border-radius: 24rpx;
  padding: 32rpx 20rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.1);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
}

.stat-number {
  font-size: 36rpx;
  font-weight: 700;
  color: #1565c0;
  display: block;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #666;
}

.filter-section {
  padding: 0 40rpx 20rpx;
}

.filter-tabs {
  display: flex;
  background: white;
  border-radius: 28rpx;
  padding: 8rpx;
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.1);
  overflow-x: auto;
}

.filter-tab {
  flex-shrink: 0;
  padding: 16rpx 28rpx;
  border-radius: 20rpx;
  transition: all 0.3s ease;
}

.filter-tab.active {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
}

.filter-text {
  font-size: 24rpx;
  color: #666;
  font-weight: 500;
}

.filter-tab.active .filter-text {
  color: white;
}

.sessions-list {
  padding: 0 40rpx;
}

.session-item {
  background: white;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.08);
  border: 2rpx solid rgba(227, 242, 253, 0.6);
  transition: all 0.3s ease;
}

.session-item:active {
  transform: translateY(2rpx);
  box-shadow: 0 6rpx 20rpx rgba(21, 101, 192, 0.15);
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.session-info {
  flex: 1;
}

.session-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #1565c0;
  display: block;
  margin-bottom: 8rpx;
}

.session-scenario {
  font-size: 24rpx;
  color: #42a5f5;
  background: #e3f2fd;
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  display: inline-block;
}

.session-meta {
  text-align: right;
}

.session-time {
  font-size: 24rpx;
  color: #999;
  display: block;
  margin-bottom: 8rpx;
}

.session-score {
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
}

.score-text {
  font-size: 22rpx;
  color: #4caf50;
  font-weight: 600;
}

.session-content {
  margin-bottom: 20rpx;
}

.session-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12rpx;
  display: block;
}

.session-stats {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.stat-item {
  font-size: 24rpx;
  color: #999;
}

.stat-separator {
  font-size: 24rpx;
  color: #ddd;
}

.session-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.session-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  flex: 1;
}

.skill-tag {
  background: #f0f8ff;
  color: #1976d2;
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  font-size: 20rpx;
  border: 1rpx solid #e3f2fd;
}

.session-actions {
  display: flex;
  gap: 16rpx;
}

.action-icon {
  width: 48rpx;
  height: 48rpx;
  border-radius: 24rpx;
  background: #f8fbff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-icon:active {
  transform: scale(0.9);
  background: #e3f2fd;
}

.icon {
  font-size: 24rpx;
}

.loading-container {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.session-skeleton {
  background: white;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.08);
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.skeleton-title {
  width: 200rpx;
  height: 32rpx;
  background: #f0f0f0;
  border-radius: 4rpx;
}

.skeleton-time {
  width: 80rpx;
  height: 24rpx;
  background: #f5f5f5;
  border-radius: 4rpx;
}

.skeleton-content {
  width: 100%;
  height: 26rpx;
  background: #f0f0f0;
  border-radius: 4rpx;
  margin-bottom: 20rpx;
}

.skeleton-tags {
  display: flex;
  gap: 8rpx;
}

.skeleton-tag {
  width: 60rpx;
  height: 24rpx;
  background: #f5f5f5;
  border-radius: 12rpx;
}

.empty-state {
  text-align: center;
  padding: 80rpx 40rpx;
}

.empty-icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: 30rpx;
  opacity: 0.6;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.empty-desc {
  font-size: 26rpx;
  color: #666;
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
}

.action-text {
  color: white;
  font-weight: 600;
}

.fab {
  position: fixed;
  bottom: 40rpx;
  right: 40rpx;
  width: 112rpx;
  height: 112rpx;
  border-radius: 56rpx;
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  box-shadow: 0 8rpx 24rpx rgba(66, 165, 245, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.fab:active {
  transform: scale(0.9);
}

.fab-icon {
  font-size: 36rpx;
  color: white;
}

/* 动画 */
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

.session-item {
  animation: fadeIn 0.3s ease-out;
}
</style>
