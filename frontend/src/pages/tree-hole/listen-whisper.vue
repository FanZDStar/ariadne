<template>
  <view class="listen-container">
    <!-- 卡片翻动容器 -->
    <view class="content-wrapper">
      <view class="whisper-card-stack">
        <!-- 主卡片 -->
        <view
          v-if="whisper"
          class="whisper-note main-card"
          :class="{ flipping: isFlipping }"
          @click="goToWhisperDetail"
        >
          <!-- 悄悄话标题 -->
          <view class="whisper-title-section" v-if="whisper.title">
            <text class="whisper-title">{{ whisper.title }}</text>
          </view>

          <!-- 第一行：头像和匿名名称 -->
          <view class="whisper-header">
            <image class="avatar" :src="getAvatarUrl()" mode="aspectFill" />
            <view class="user-info">
              <text class="nickname">{{ getDisplayName() }}</text>
              <text class="post-time">{{
                formatTime(whisper.created_at)
              }}</text>
            </view>
          </view>

          <!-- 第二行：心情和标签 -->
          <view class="whisper-meta">
            <view class="mood-section" v-if="whisper.mood">
              <text class="mood-emoji">{{ getMoodEmoji(whisper.mood) }}</text>
              <text class="mood-text">{{ getMoodText(whisper.mood) }}</text>
            </view>
            <view
              class="tags-section"
              v-if="whisper.tags && whisper.tags.length > 0"
            >
              <view
                class="tag-item"
                v-for="tag in whisper.tags.slice(0, 3)"
                :key="tag"
              >
                <text class="tag-text">#{{ tag }}</text>
              </view>
              <text v-if="whisper.tags.length > 3" class="more-tags">...</text>
            </view>
          </view>

          <!-- 第三行：正文和图片 -->
          <scroll-view scroll-y="true" class="whisper-scroll-view">
            <view class="content-section">
              <text class="whisper-content">{{ getDisplayContent() }}</text>
              <view
                class="images-section"
                v-if="whisper.images && whisper.images.length > 0"
              >
                <image
                  v-for="(image, index) in whisper.images.slice(0, 2)"
                  :key="index"
                  :src="getImageUrl(image.image_url)"
                  class="whisper-image"
                  mode="aspectFill"
                  @click.stop="previewImage(image.image_url)"
                />
                <view v-if="whisper.images.length > 2" class="more-images">
                  <text class="more-images-text"
                    >还有{{ whisper.images.length - 2 }}张图片</text
                  >
                </view>
              </view>
            </view>
          </scroll-view>

          <!-- 卡片底部统计信息 - 可交互 -->
          <view class="whisper-stats">
            <view
              class="stat-item stat-clickable"
              :class="{ 'stat-liked': liked }"
              @click.stop="toggleLike"
            >
              <text class="stat-icon">{{ liked ? "❤️" : "🤍" }}</text>
              <text class="stat-count">{{ likeCount }}</text>
            </view>
            <view
              class="stat-item stat-clickable"
              @click.stop="goToWhisperDetail"
            >
              <text class="stat-icon">💬</text>
              <text class="stat-count">{{ whisper.comment_count || 0 }}</text>
            </view>
          </view>
        </view>

        <!-- 背景卡片（营造堆叠效果） -->
        <view class="whisper-note shadow-card shadow-card-1"></view>
        <view class="whisper-note shadow-card shadow-card-2"></view>

        <!-- 空状态 -->
        <view v-if="!whisper && !loading" class="empty-state">
          <text class="empty-text"
            >暂时没有新的悄悄话了，\n不如去写下你的心事吧~</text
          >
        </view>

        <!-- 加载状态 -->
        <view v-if="loading" class="loading-state">
          <text class="loading-text">正在为你寻找新的悄悄话...</text>
        </view>
      </view>
    </view>

    <!-- 底部操作区 - 只保留换一个按钮 -->
    <view class="footer-actions">
      <button
        class="next-button"
        :disabled="loading"
        @click="fetchRandomWhisper"
      >
        {{ loading ? "加载中..." : "抽一条" }}
      </button>
    </view>
  </view>
</template>

<script>
import { api, storage } from "../../utils/api.js";

export default {
  data() {
    return {
      whisper: null,
      liked: false,
      likeCount: 0,
      loading: false,
      isFlipping: false,
    };
  },
  onLoad() {
    this.fetchRandomWhisper();
  },
  onShow() {
    // 从详情页返回时刷新当前悄悄话数据
    if (this.whisper && this.whisper.whisper_id) {
      this.refreshCurrentWhisper();
    }
  },
  methods: {
    // 刷新当前悄悄话的点赞和评论数
    async refreshCurrentWhisper() {
      const token = storage.getToken();
      if (!token || !this.whisper) return;

      try {
        const updatedWhisper = await api.getWhisperDetails(
          token,
          this.whisper.whisper_id
        );
        // 更新点赞和评论数
        this.whisper.like_count = updatedWhisper.like_count;
        this.whisper.comment_count = updatedWhisper.comment_count;
        this.whisper.liked = updatedWhisper.liked;

        // 同步到本地变量
        this.likeCount = updatedWhisper.like_count || 0;
        this.liked = updatedWhisper.liked || false;
      } catch (error) {
        console.error("Failed to refresh whisper:", error);
        // 刷新失败不影响用户体验，静默处理
      }
    },
    async fetchRandomWhisper() {
      // 触发翻页动画
      this.isFlipping = true;
      this.loading = true;

      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        this.loading = false;
        this.isFlipping = false;
        return;
      }

      try {
        // 延迟一下让动画效果更明显
        await new Promise((resolve) => setTimeout(resolve, 300));

        const whisper = await api.getRandomWhisper(token);
        this.whisper = whisper;
        this.likeCount = whisper.like_count || 0;
        this.liked = whisper.liked || false;

        // 动画结束
        setTimeout(() => {
          this.isFlipping = false;
        }, 400);
      } catch (error) {
        this.whisper = null;
        console.error("Failed to fetch random whisper:", error);
        uni.showToast({
          title: "暂时没有悄悄话了",
          icon: "none",
        });
        this.isFlipping = false;
      } finally {
        this.loading = false;
      }
    },

    // 格式化时间显示
    formatTime(dateString) {
      if (!dateString) return "";

      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;

      // 计算时间差
      const minutes = Math.floor(diff / (1000 * 60));
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));

      if (minutes < 1) {
        return "刚刚";
      } else if (minutes < 60) {
        return `${minutes}分钟前`;
      } else if (hours < 24) {
        return `${hours}小时前`;
      } else if (days < 7) {
        return `${days}天前`;
      } else {
        return date.toLocaleDateString();
      }
    },

    // 获取头像URL
    getAvatarUrl() {
      if (!this.whisper) return "/static/avatar.png";

      // 如果是匿名且有匿名头像，使用匿名头像
      if (this.whisper.is_anonymous && this.whisper.anonymous_avatar) {
        return this.getImageUrl(this.whisper.anonymous_avatar);
      }

      // 否则使用用户头像
      const avatarUrl = this.whisper.user?.avatar_url;
      if (!avatarUrl) return "/static/avatar.png";

      return this.getImageUrl(avatarUrl);
    },

    // 获取显示名称
    getDisplayName() {
      if (!this.whisper) return "匿名用户";

      // 如果是匿名且有匿名名称，使用匿名名称
      if (this.whisper.is_anonymous && this.whisper.anonymous_name) {
        return this.whisper.anonymous_name;
      }

      // 如果是匿名但没有匿名名称，显示默认匿名
      if (this.whisper.is_anonymous) {
        return "匿名用户";
      }

      // 否则使用用户昵称
      return this.whisper.user?.nickname || "匿名用户";
    },

    // 获取心情emoji
    getMoodEmoji(mood) {
      const moodEmojis = {
        very_happy: "😄",
        happy: "😊",
        neutral: "😐",
        sad: "😢",
        very_sad: "😭",
      };
      return moodEmojis[mood] || "😐";
    },

    // 获取心情文本
    getMoodText(mood) {
      const moodTexts = {
        very_happy: "超开心",
        happy: "开心",
        neutral: "平静",
        sad: "难过",
        very_sad: "很难过",
      };
      return moodTexts[mood] || "平静";
    },

    // 获取显示内容（限制80字）
    getDisplayContent() {
      if (!this.whisper || !this.whisper.content) return "";
      const content = this.whisper.content;
      if (content.length > 80) {
        return content.substring(0, 80) + "...";
      }
      return content;
    },

    // 获取图片URL
    getImageUrl(imageUrl) {
      if (imageUrl.startsWith("http")) {
        return imageUrl;
      }

      // 如果是静态资源路径（不包含 /uploads/），使用静态资源处理
      if (!imageUrl.includes("/uploads/")) {
        // 处理静态资源路径
        if (imageUrl.startsWith("/")) {
          return `/static${imageUrl}`;
        } else {
          return `/static/${imageUrl}`;
        }
      }

      // 如果是上传的图片，使用API base URL
      const baseUrl = process.env.VUE_APP_API_BASE_URL;
      if (!baseUrl) {
        console.error("❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!");
        return imageUrl;
      }
      if (imageUrl.startsWith("/")) {
        return baseUrl + imageUrl;
      } else {
        return baseUrl + "/" + imageUrl;
      }
    },

    // 预览图片
    previewImage(imageUrl) {
      const fullImageUrl = this.getImageUrl(imageUrl);
      const allImages = this.whisper.images.map((img) =>
        this.getImageUrl(img.image_url)
      );

      uni.previewImage({
        current: fullImageUrl,
        urls: allImages,
      });
    },

    // 点赞功能
    async toggleLike() {
      if (!this.whisper) return;

      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      try {
        // 乐观更新UI
        const originalLiked = this.liked;
        const originalCount = this.likeCount;

        this.liked = !this.liked;
        this.likeCount += this.liked ? 1 : -1;

        // 显示点赞反馈
        if (this.liked) {
          uni.showToast({
            title: "点赞成功",
            icon: "success",
            duration: 1000,
          });
        }

        await api.likeWhisper(token, this.whisper.whisper_id);
      } catch (error) {
        // 如果请求失败，回滚UI状态
        this.liked = originalLiked;
        this.likeCount = originalCount;

        console.error("Failed to toggle like:", error);
        uni.showToast({
          title: "操作失败，请稍后重试",
          icon: "none",
        });
      }
    },

    // 跳转到悄悄话详情页
    goToWhisperDetail() {
      if (!this.whisper) return;
      uni.navigateTo({
        url: `/pages/tree-hole/whisper-detail?whisper_id=${this.whisper.whisper_id}`,
      });
    },

    // 跳转到聊天页面（已弃用，现在直接跳详情页）
    goToChat() {
      this.goToWhisperDetail();
    },
  },
};
</script>

<style scoped>
.listen-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%);
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 950rpx;
  width: 100%;
  bottom: 0;
}

.content-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 60rpx 40rpx 40rpx 40rpx;
  padding-top: 100rpx;
  padding-right: 100rpx;
  padding-bottom: 200rpx;
  overflow: hidden;
  /* 禁止滚动 */
}

/* 卡片堆叠容器 */
.whisper-card-stack {
  position: relative;
  width: 85%;
  max-width: 850rpx;
  height: 75vh;
  max-height: 1100rpx;
}

/* 主卡片 */
.whisper-note {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-color: #fffbf0;
  /* 更温暖的米白色 */
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.15);
  border: 2rpx solid #f0e6d2;
  /* 淡淡的边框 */
  transition: all 0.3s ease;
}

/* 主卡片样式 */
.main-card {
  z-index: 3;
  transform: translateY(0);
}

/* 翻页动画 */
.main-card.flipping {
  animation: flipCard 0.6s ease-in-out;
}

@keyframes flipCard {
  0% {
    transform: rotateY(0deg) scale(1);
  }
  50% {
    transform: rotateY(90deg) scale(0.8);
  }
  100% {
    transform: rotateY(0deg) scale(1);
  }
}

/* 背景卡片（制造层叠效果） */
.shadow-card {
  background-color: #f5f1e8;
  border: 1rpx solid #e8dcc6;
  z-index: 1;
}

.shadow-card-1 {
  transform: translateY(8rpx) translateX(4rpx) rotate(1deg);
  z-index: 2;
}

.shadow-card-2 {
  transform: translateY(16rpx) translateX(8rpx) rotate(2deg);
  z-index: 1;
}

/* 悄悄话标题 */
.whisper-title-section {
  margin-bottom: 25rpx;
  flex-shrink: 0;
}

.whisper-title {
  font-size: 34rpx;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1.4;
  display: block;
}

/* 用户信息头部 */
.whisper-header {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
  flex-shrink: 0;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  border: 3rpx solid #fff;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 5rpx;
}

.nickname {
  font-weight: bold;
  font-size: 30rpx;
  color: #2c3e50;
}

.post-time {
  font-size: 22rpx;
  color: #7f8c8d;
}

/* 心情和标签区域 */
.whisper-meta {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
  margin-bottom: 25rpx;
  flex-shrink: 0;
}

.mood-section {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.mood-emoji {
  font-size: 36rpx;
}

.mood-text {
  font-size: 24rpx;
  color: #666;
  background-color: #f8f4e6;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  border: 1rpx solid #e8dcc6;
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  align-items: center;
}

.tag-item {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  padding: 6rpx 14rpx;
  border-radius: 16rpx;
  border: 1rpx solid #90caf9;
}

.tag-text {
  font-size: 22rpx;
  color: #1565c0;
  font-weight: 500;
}

.more-tags {
  font-size: 24rpx;
  color: #7f8c8d;
  margin-left: 5rpx;
}

/* 内容滚动区域 */
.whisper-scroll-view {
  flex: 1;
  height: 100%;
}

.content-section {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.whisper-content {
  font-size: 28rpx;
  color: #2c3e50;
  line-height: 1.7;
  letter-spacing: 0.5rpx;
}

/* 图片区域 */
.images-section {
  display: flex;
  gap: 15rpx;
  flex-wrap: wrap;
  align-items: center;
}

.whisper-image {
  width: 180rpx;
  height: 180rpx;
  border-radius: 12rpx;
  object-fit: cover;
  border: 2rpx solid #f0e6d2;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.more-images {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 180rpx;
  height: 180rpx;
  background: linear-gradient(135deg, #f8f4e6, #f0e6d2);
  border-radius: 12rpx;
  border: 2rpx dashed #d0c4a8;
}

.more-images-text {
  font-size: 22rpx;
  color: #8d7b5f;
  text-align: center;
}

/* 卡片底部统计 */
.whisper-stats {
  display: flex;
  justify-content: flex-start;
  gap: 40rpx;
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #e8dcc6;
  flex-shrink: 0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  transition: transform 0.2s ease;
}

/* 可点击的统计项 */
.stat-clickable {
  cursor: pointer;
  padding: 8rpx 20rpx;
  border-radius: 30rpx;
  background-color: #f8f4e6;
  border: 1rpx solid #e8dcc6;
}

.stat-clickable:active {
  transform: scale(0.95);
  background-color: #f0e6d2;
}

/* 已点赞状态 */
.stat-liked {
  background: linear-gradient(135deg, #ffe5e5, #ffd1d1);
  border-color: #ffb3b3;
}

.stat-icon {
  font-size: 28rpx;
}

.stat-count {
  font-size: 24rpx;
  color: #666;
  font-weight: 500;
}

/* 空状态和加载状态 */
.empty-state,
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.empty-text,
.loading-text {
  font-size: 30rpx;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

/* 底部操作区 */
.footer-actions {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 950rpx;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30rpx;
  padding-bottom: calc(30rpx + constant(safe-area-inset-bottom));
  padding-bottom: calc(30rpx + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-top: 1rpx solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.next-button {
  background: linear-gradient(135deg, #99a8eb, #b99ed4);
  color: white;
  border-radius: 50rpx;
  font-size: 32rpx;
  font-weight: 600;
  padding: 0 80rpx;
  height: 90rpx;
  line-height: 90rpx;
  box-shadow: 0 8rpx 24rpx rgba(105, 111, 138, 0.4);
  transition: all 0.3s ease;
  min-width: 280rpx;
}

.next-button:active {
  transform: scale(0.95);
  box-shadow: 0 4rpx 16rpx rgba(50, 58, 97, 0.3);
}

.next-button[disabled] {
  background: #a0a0a0;
  box-shadow: none;
  opacity: 0.6;
}
</style>
