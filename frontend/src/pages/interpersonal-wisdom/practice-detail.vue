<template>
  <view class="practice-detail-container">
    <!-- 顶部导航 -->
    <view class="custom-navbar">
      <view class="nav-left" @click="goBack">
        <text class="nav-icon">←</text>
      </view>
      <view class="nav-center">
        <text class="nav-title">练习详情</text>
      </view>
      <view class="nav-right" @click="showActions">
        <text class="nav-icon">⋯</text>
      </view>
    </view>

    <!-- 会话信息头部 -->
    <view class="session-header" v-if="sessionData">
      <view class="session-info">
        <text class="session-title">{{ sessionData.session_title }}</text>
        <text class="session-scenario">{{
          sessionData.practice_scenario_name
        }}</text>
        <text class="session-time">{{
          formatFullTime(sessionData.created_at)
        }}</text>
      </view>

      <view class="session-stats">
        <view class="stat-item">
          <text class="stat-label">消息数</text>
          <text class="stat-value">{{ sessionData.total_messages }}</text>
        </view>
        <view class="stat-item" v-if="sessionData.practice_quality_score">
          <text class="stat-label">评分</text>
          <text class="stat-value"
            >{{ sessionData.practice_quality_score }}分</text
          >
        </view>
      </view>

      <!-- 练习技能标签 -->
      <view
        class="skills-section"
        v-if="
          sessionData.skills_practiced &&
          sessionData.skills_practiced.length > 0
        "
      >
        <text class="skills-title">练习技能</text>
        <view class="skills-tags">
          <text
            v-for="skill in sessionData.skills_practiced"
            :key="skill"
            class="skill-tag"
            >{{ skill }}</text
          >
        </view>
      </view>
    </view>

    <!-- 对话内容 -->
    <view class="messages-container">
      <!-- 加载状态 -->
      <view v-if="loading" class="loading-messages">
        <view v-for="n in 3" :key="n" class="message-skeleton">
          <view class="skeleton-avatar"></view>
          <view class="skeleton-content">
            <view class="skeleton-text-line"></view>
            <view class="skeleton-text-line short"></view>
          </view>
        </view>
      </view>

      <!-- 消息列表 -->
      <view v-else class="messages-list">
        <view
          v-for="(message, index) in messages"
          :key="index"
          class="message-item"
          :class="{
            'user-message': message.role === 'user',
            'ai-message': message.role === 'assistant',
          }"
        >
          <view class="message-avatar">
            <text class="avatar-text">{{
              message.role === "user" ? "我" : "AI"
            }}</text>
          </view>

          <view class="message-content">
            <view class="message-bubble">
              <text class="message-text">{{ message.content }}</text>
            </view>
            <text class="message-time">{{
              formatMessageTime(message.timestamp)
            }}</text>
          </view>
        </view>

        <!-- 空状态 -->
        <view v-if="!loading && messages.length === 0" class="empty-messages">
          <text class="empty-icon">💭</text>
          <text class="empty-text">暂无对话记录</text>
        </view>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-actions" v-if="sessionData">
      <view class="action-button" @click="exportSession">
        <text class="action-icon">📄</text>
        <text class="action-text">导出</text>
      </view>
      <view class="action-button" @click="continueSession">
        <text class="action-icon">▶️</text>
        <text class="action-text">继续练习</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      sessionId: "",
      sessionData: null,
      messages: [],
      loading: true,
    };
  },

  onLoad(options) {
    this.sessionId = options.sessionId;
    if (this.sessionId) {
      this.loadSessionDetail();
    }
  },

  onShareAppMessage() {
    return {
      title: `AI对话练习记录：${
        this.sessionData?.session_title || "人际沟通练习"
      }`,
      path: `/pages/interpersonal-wisdom/practice-detail?sessionId=${this.sessionId}`,
    };
  },

  methods: {
    async loadSessionDetail() {
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
          }/interpersonal-practice/sessions/${this.sessionId}`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.sessionData = response.data;
          // messages 字段已经是解析过的数组，不需要再次JSON.parse
          this.messages = response.data.messages || [];
        } else if (response.statusCode === 404) {
          uni.showToast({
            title: "记录不存在",
            icon: "none",
          });
          this.goBack();
        } else {
          uni.showToast({
            title: "加载失败",
            icon: "none",
          });
        }
      } catch (error) {
        console.error("加载练习详情失败:", error);
        uni.showToast({
          title: "网络错误",
          icon: "none",
        });
      } finally {
        this.loading = false;
      }
    },

    exportSession() {
      // 导出对话记录
      let exportText = `AI对话练习记录\n`;
      exportText += `标题: ${this.sessionData.session_title}\n`;
      exportText += `场景: ${this.sessionData.practice_scenario_name}\n`;
      exportText += `时间: ${this.formatFullTime(
        this.sessionData.created_at
      )}\n\n`;
      exportText += `对话内容:\n`;

      this.messages.forEach((message, index) => {
        exportText += `${index + 1}. ${
          message.role === "user" ? "我" : "AI"
        }: ${message.content}\n`;
      });

      uni.setClipboardData({
        data: exportText,
        success: () => {
          uni.showToast({
            title: "记录已复制到剪贴板",
            icon: "success",
          });
        },
      });
    },

    continueSession() {
      // 继续当前会话的对话
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/interactive-practice?sessionId=${this.sessionId}&scenario=${this.sessionData.practice_scenario}&continue=true`,
      });
    },

    showActions() {
      uni.showActionSheet({
        itemList: ["重新练习", "删除记录", "举报内容"],
        success: (res) => {
          switch (res.tapIndex) {
            case 0:
              this.continueSession();
              break;
            case 1:
              this.deleteSession();
              break;
            case 2:
              // 举报功能
              uni.showToast({
                title: "举报功能开发中",
                icon: "none",
              });
              break;
          }
        },
      });
    },

    deleteSession() {
      uni.showModal({
        title: "确认删除",
        content: "删除后将无法恢复，确定要删除这条练习记录吗？",
        confirmColor: "#ff6b6b",
        success: async (res) => {
          if (res.confirm) {
            try {
              const token = uni.getStorageSync("access_token");
              const response = await uni.request({
                url: `${
                  process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
                }/interpersonal-practice/sessions/${this.sessionId}`,
                method: "DELETE",
                header: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
              });

              if (response.statusCode === 200) {
                uni.showToast({
                  title: "删除成功",
                  icon: "success",
                });
                setTimeout(() => {
                  this.goBack();
                }, 1000);
              } else {
                uni.showToast({
                  title: "删除失败",
                  icon: "none",
                });
              }
            } catch (error) {
              console.error("删除记录失败:", error);
              uni.showToast({
                title: "网络错误",
                icon: "none",
              });
            }
          }
        },
      });
    },

    goBack() {
      uni.navigateBack({
        delta: 1,
      });
    },

    formatFullTime(timeString) {
      const date = new Date(timeString);
      return date.toLocaleString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    formatMessageTime(timestamp) {
      if (!timestamp) return "";
      const date = new Date(timestamp);
      return date.toLocaleTimeString("zh-CN", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
.practice-detail-container {
  min-height: 100vh;
  background: #f8fbff;
  padding-bottom: 120rpx;
}

.custom-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 40rpx;
  background: white;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  max-width: 950rpx;
  margin: 0 auto;
  left: 0;
  right: 0;
}

.nav-left,
.nav-right {
  width: 80rpx;
  display: flex;
  justify-content: center;
}

.nav-center {
  flex: 1;
  text-align: center;
}

.nav-icon {
  font-size: 36rpx;
  color: #1565c0;
  font-weight: 600;
}

.nav-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.session-header {
  background: white;
  padding: 40rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(21, 101, 192, 0.08);
}

.session-info {
  margin-bottom: 32rpx;
  text-align: center;
}

.session-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #1565c0;
  display: block;
  margin-bottom: 12rpx;
}

.session-scenario {
  font-size: 26rpx;
  color: #42a5f5;
  background: #e3f2fd;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  display: inline-block;
  margin-bottom: 12rpx;
}

.session-time {
  font-size: 24rpx;
  color: #999;
  display: block;
}

.session-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 32rpx;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 8rpx;
}

.stat-value {
  font-size: 32rpx;
  font-weight: 600;
  color: #1565c0;
  display: block;
}

.skills-section {
  border-top: 2rpx solid #f5f5f5;
  padding-top: 32rpx;
}

.skills-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background: #f0f8ff;
  color: #1976d2;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  border: 1rpx solid #e3f2fd;
}

.messages-container {
  flex: 1;
  padding: 0 40rpx;
}

.loading-messages {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.message-skeleton {
  display: flex;
  gap: 20rpx;
  padding: 20rpx 0;
}

.skeleton-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 40rpx;
  background: #f0f0f0;
}

.skeleton-content {
  flex: 1;
}

.skeleton-text-line {
  height: 24rpx;
  background: #f0f0f0;
  border-radius: 4rpx;
  margin-bottom: 12rpx;
}

.skeleton-text-line.short {
  width: 60%;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.message-item {
  display: flex;
  gap: 20rpx;
  animation: messageSlideIn 0.3s ease-out;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
}

.ai-message .message-avatar {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
}

.avatar-text {
  color: white;
  font-size: 24rpx;
  font-weight: 600;
}

.ai-message .avatar-text {
  color: #666;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message-bubble {
  padding: 24rpx;
  border-radius: 24rpx;
  margin-bottom: 8rpx;
  position: relative;
}

.user-message .message-bubble {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  border-bottom-right-radius: 8rpx;
}

.ai-message .message-bubble {
  background: white;
  border-bottom-left-radius: 8rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.message-text {
  font-size: 28rpx;
  line-height: 1.6;
  color: white;
  word-break: break-word;
}

.ai-message .message-text {
  color: #333;
}

.message-time {
  font-size: 20rpx;
  color: #999;
  padding: 0 8rpx;
}

.user-message .message-time {
  text-align: right;
}

.empty-messages {
  text-align: center;
  padding: 120rpx 40rpx;
}

.empty-icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: 30rpx;
  opacity: 0.6;
}

.empty-text {
  font-size: 28rpx;
  color: #666;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 24rpx 40rpx;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx;
  border-radius: 16rpx;
  transition: all 0.3s ease;
}

.action-button:active {
  transform: scale(0.95);
  background: #f5f5f5;
}

.action-icon {
  font-size: 32rpx;
}

.action-text {
  font-size: 20rpx;
  color: #666;
}

/* 动画 */
@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 滚动条优化 */
::-webkit-scrollbar {
  display: none;
}
</style>
