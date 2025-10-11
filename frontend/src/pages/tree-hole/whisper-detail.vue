<template>
  <view class="whisper-detail-container">
    <!-- 悄悄话详情卡片 -->
    <view class="whisper-card">
      <!-- 用户信息行 -->
      <view class="user-info">
        <image class="avatar" :src="getAvatarUrl()" mode="aspectFill" />
        <view class="user-details">
          <text class="username">{{ getDisplayName() }}</text>
          <text class="timestamp">{{
            formatTimestamp(whisper.created_at)
          }}</text>
        </view>
        <!-- 右上角分享按钮 -->
        <view class="share-button" @click="shareWhisper">
          <text class="share-icon">📤</text>
        </view>
      </view>

      <!-- 悄悄话内容 -->
      <view class="whisper-content">
        <!-- 标题 -->
        <text v-if="whisper.title" class="whisper-title">{{
          whisper.title
        }}</text>

        <!-- 心情和标签 -->
        <view class="meta-info">
          <view class="mood-section" v-if="whisper.mood">
            <text class="mood-emoji">{{ getMoodEmoji(whisper.mood) }}</text>
            <text class="mood-text">{{ getMoodText(whisper.mood) }}</text>
          </view>
          <view
            class="tags-section"
            v-if="whisper.tags && whisper.tags.length > 0"
          >
            <view class="tag-item" v-for="tag in whisper.tags" :key="tag">
              <text class="tag-text">#{{ tag }}</text>
            </view>
          </view>
        </view>

        <!-- 正文内容 -->
        <text class="content-text">{{ whisper.content }}</text>

        <!-- 图片展示 -->
        <view
          class="images-grid"
          v-if="whisper.images && whisper.images.length > 0"
        >
          <image
            v-for="(image, index) in whisper.images"
            :key="index"
            :src="getImageUrl(image.image_url)"
            class="content-image"
            mode="aspectFill"
            @click="previewImage(image.image_url)"
          />
        </view>
      </view>

      <!-- 互动统计 - 可交互 -->
      <view class="interaction-stats">
        <view 
          class="stat-item stat-clickable" 
          :class="{ 'stat-liked': whisper.liked }"
          @click="toggleLike"
        >
          <text class="stat-icon">{{ whisper.liked ? "❤️" : "🤍" }}</text>
          <text class="stat-text">{{ whisper.like_count || 0 }}</text>
        </view>
        <view 
          class="stat-item"
        >
          <text class="stat-icon">💬</text>
          <text class="stat-text">{{ whisper.comment_count || 0 }}</text>
        </view>
      </view>
    </view>

    <!-- 评论列表区域 -->
    <view class="comments-section">
      <view class="section-title">
        <text class="title-text">评论 ({{ whisper.comment_count || 0 }})</text>
      </view>

      <view v-if="comments.length === 0" class="empty-comments">
        <text class="empty-text">还没有评论，快来抢沙发吧~</text>
      </view>

      <view
        v-for="comment in comments"
        :key="comment.comment_id"
        class="comment-item"
      >
        <image
          class="comment-avatar"
          :src="getCommentAvatarUrl(comment)"
          mode="aspectFill"
        />
        <view class="comment-content">
          <text class="comment-user">{{ getCommentUserName(comment) }}</text>
          <text class="comment-text">{{ comment.content }}</text>
          <view class="comment-actions">
            <text class="comment-time">{{
              formatTimestamp(comment.created_at)
            }}</text>
            <text class="reply-btn" @click="replyToComment(comment)">回复</text>
          </view>

          <!-- 回复列表 -->
          <view
            v-if="comment.replies && comment.replies.length > 0"
            class="replies-section"
          >
            <view
              v-for="reply in comment.replies"
              :key="reply.reply_id"
              class="reply-item"
            >
              <image
                class="reply-avatar"
                :src="getCommentAvatarUrl(reply)"
                mode="aspectFill"
              />
              <view class="reply-content">
                <text class="reply-user">{{ getCommentUserName(reply) }}</text>
                <text v-if="reply.reply_to_user" class="reply-mention">
                  回复 @{{ getCommentUserName(reply.reply_to) }}：
                </text>
                <text class="reply-text">{{ reply.content }}</text>
                <view class="reply-actions">
                  <text class="reply-time">{{
                    formatTimestamp(reply.created_at)
                  }}</text>
                  <text class="reply-btn" @click="replyToReply(comment, reply)"
                    >回复</text
                  >
                </view>
              </view>
            </view>

            <!-- 查看更多回复 -->
            <view
              v-if="comment.reply_count > comment.replies.length"
              class="load-more-replies"
              @click="loadMoreReplies(comment)"
            >
              <text class="load-more-text">
                查看更多回复 ({{
                  comment.reply_count - comment.replies.length
                }}条)
              </text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部评论输入框 -->
    <view class="comment-input-bar">
      <!-- 回复提示 -->
      <view v-if="replyingTo" class="reply-hint">
        <text class="reply-hint-text">
          回复 @{{ replyingTo.userName }}：{{ replyingTo.content }}
        </text>
        <text class="cancel-reply" @click="cancelReply">✕</text>
      </view>

      <view class="input-row">
        <input
          class="comment-input"
          v-model="newComment"
          :placeholder="replyingTo ? '回复评论...' : '说些什么吧...'"
          @confirm="submitComment"
          confirm-type="send"
        />
        <view
          class="send-button"
          @click="submitComment"
          :class="{ active: newComment.trim() }"
        >
          <text class="send-text">发送</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from "../../utils/api.js";

export default {
  data() {
    return {
      whisper: null,
      comments: [],
      newComment: "",
      whisperId: null,
      replyingTo: null, // 当前回复的对象 { type: 'comment'|'reply', id: xxx, userName: xxx, content: xxx }
    };
  },
  onLoad(option) {
    this.whisperId = option.whisper_id;
    if (this.whisperId) {
      this.loadWhisperDetail();
      this.loadComments();
    }
  },
  methods: {
    async loadWhisperDetail(retryCount = 0) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({ title: "请先登录", icon: "none" });
        return;
      }

      const maxRetries = 2; // 最多重试2次

      try {
        this.whisper = await api.getWhisperDetails(token, this.whisperId);
      } catch (error) {
        console.error(`Failed to load whisper detail (attempt ${retryCount + 1}):`, error);
        
        // 如果是网络错误或服务器错误，且还有重试次数，自动重试
        if (retryCount < maxRetries) {
          console.log(`⏳ 自动重试中... (${retryCount + 1}/${maxRetries})`);
          
          // 延迟后重试，延迟时间随重试次数增加
          await new Promise(resolve => setTimeout(resolve, 1000 * (retryCount + 1)));
          
          return this.loadWhisperDetail(retryCount + 1);
        }
        
                // 重试失败后显示简单的错误提示
        uni.showToast({
          title: '加载失败',
          icon: 'none',
          duration: 2000
        });
      }
    },

    async loadComments() {
      const token = storage.getToken();
      if (!token) return;

      try {
        this.comments = await api.getWhisperComments(token, this.whisperId);
      } catch (error) {
        console.error("Failed to load comments:", error);
        this.comments = [];
      }
    },

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

    getImageUrl(imageUrl) {
      if (!imageUrl) return "";

      if (imageUrl.startsWith("http")) {
        return imageUrl;
      }

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

    getMoodText(mood) {
      const moodTexts = {
        very_happy: "超开心",
        happy: "开心",
        neutral: "一般",
        sad: "难过",
        very_sad: "很难过",
      };
      return moodTexts[mood] || "一般";
    },

    getCommentAvatarUrl(comment) {
      // 评论头像逻辑，类似悄悄话头像
      if (comment.is_anonymous && comment.anonymous_avatar) {
        return this.getImageUrl(comment.anonymous_avatar);
      }
      if (comment.user && comment.user.avatar_url) {
        return this.getImageUrl(comment.user.avatar_url);
      }
      return "/static/avatar.png";
    },

    getCommentUserName(comment) {
      if (comment.is_anonymous) {
        return comment.anonymous_name || "匿名用户";
      }
      return comment.user
        ? comment.user.nickname || comment.user.username
        : "未知用户";
    },

    async toggleLike() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({ title: "请先登录", icon: "none" });
        return;
      }

      try {
        // 乐观更新UI
        const originalLiked = this.whisper.liked;
        const originalCount = this.whisper.like_count || 0;

        this.whisper.liked = !this.whisper.liked;
        this.whisper.like_count = this.whisper.liked
          ? originalCount + 1
          : originalCount - 1;

        // 调用API
        await api.likeWhisper(token, this.whisperId);

        uni.showToast({
          title: this.whisper.liked ? "已点赞" : "已取消点赞",
          icon: "success",
        });
      } catch (error) {
        // 如果请求失败，回滚UI状态
        this.whisper.liked = originalLiked;
        this.whisper.like_count = originalCount;

        console.error("Failed to toggle like:", error);
        uni.showToast({ title: "操作失败，请稍后重试", icon: "none" });
      }
    },

    async submitComment() {
      if (!this.newComment.trim()) return;

      const token = storage.getToken();
      if (!token) {
        uni.showToast({ title: "请先登录", icon: "none" });
        return;
      }

      try {
        const commentData = {
          content: this.newComment.trim(),
          is_anonymous: true, // 默认匿名评论
        };

        // 如果是回复评论或回复
        if (this.replyingTo) {
          if (this.replyingTo.type === "comment") {
            // 回复评论
            try {
              await api.createCommentReply(
                token,
                this.replyingTo.id,
                commentData
              );
              // 回复成功，评论数不增加（回复不算独立评论）
            } catch (error) {
              // 如果回复接口不存在，fallback到普通评论
              console.log("回复接口暂未实现，使用普通评论模式");
              commentData.content = `回复 @${this.replyingTo.userName}：${commentData.content}`;
              await api.createWhisperComment(
                token,
                this.whisperId,
                commentData
              );
              this.whisper.comment_count++;
            }
          } else if (this.replyingTo.type === "reply") {
            // 回复回复
            try {
              commentData.reply_to_user_id = this.replyingTo.userId;
              await api.createCommentReply(
                token,
                this.replyingTo.commentId,
                commentData
              );
              // 回复成功，评论数不增加（回复不算独立评论）
            } catch (error) {
              // 如果回复接口不存在，fallback到普通评论
              console.log("回复接口暂未实现，使用普通评论模式");
              commentData.content = `回复 @${this.replyingTo.userName}：${commentData.content}`;
              await api.createWhisperComment(
                token,
                this.whisperId,
                commentData
              );
              this.whisper.comment_count++;
            }
          }
        } else {
          // 普通评论
          await api.createWhisperComment(token, this.whisperId, commentData);
          // 更新评论数
          this.whisper.comment_count++;
        }

        this.newComment = "";
        this.replyingTo = null;
        this.loadComments(); // 重新加载评论列表

        uni.showToast({ title: "发送成功", icon: "success" });
      } catch (error) {
        console.error("Failed to submit comment:", error);
        uni.showToast({ title: "发送失败", icon: "none" });
      }
    },

    // 回复评论
    replyToComment(comment) {
      this.replyingTo = {
        type: "comment",
        id: comment.comment_id,
        userName: this.getCommentUserName(comment),
        content:
          comment.content.length > 20
            ? comment.content.substring(0, 20) + "..."
            : comment.content,
      };
      // 聚焦输入框
      this.focusInput();
    },

    // 回复回复
    replyToReply(comment, reply) {
      this.replyingTo = {
        type: "reply",
        id: reply.reply_id,
        commentId: comment.comment_id,
        userId: reply.user_id,
        userName: this.getCommentUserName(reply),
        content:
          reply.content.length > 20
            ? reply.content.substring(0, 20) + "..."
            : reply.content,
      };
      // 聚焦输入框
      this.focusInput();
    },

    // 取消回复
    cancelReply() {
      this.replyingTo = null;
      this.newComment = "";
    },

    // 聚焦输入框
    focusInput() {
      this.$nextTick(() => {
        // 在小程序中模拟聚焦效果
        uni.pageScrollTo({
          scrollTop: 999999,
          duration: 300,
        });
      });
    },

    // 加载更多回复
    async loadMoreReplies(comment) {
      const token = storage.getToken();
      if (!token) return;

      try {
        const replies = await api.getCommentReplies(
          token,
          comment.comment_id,
          comment.replies.length
        );
        comment.replies = [...comment.replies, ...replies];
      } catch (error) {
        console.error("Failed to load more replies:", error);
        // 如果后端接口不存在，隐藏"查看更多"按钮
        comment.reply_count = comment.replies.length;
        uni.showToast({ title: "暂不支持加载更多回复", icon: "none" });
      }
    },

    // 获取悄悄话的所有图片URL数组
    getWhisperImages(whisper) {
      if (!whisper || !whisper.images || whisper.images.length === 0) {
        return [];
      }
      return whisper.images.map((image) => this.getImageUrl(image.image_url));
    },

    previewImage(imageUrl) {
      const allImages = this.getWhisperImages(this.whisper);
      const fullUrl = this.getImageUrl(imageUrl);

      uni.previewImage({
        urls: allImages,
        current: fullUrl,
      });
    },

    // 聊天功能已隐藏，评论统计现在只显示不可点击
    // goToChat() {
    //   // 聚焦到评论输入框
    //   const query = uni.createSelectorQuery().in(this);
    //   query.select('.comment-input').boundingClientRect();
    //   query.exec((res) => {
    //     if (res[0]) {
    //       uni.pageScrollTo({
    //         scrollTop: res[0].top - 100,
    //         duration: 300
    //       });
    //     }
    //   });
    //   
    //   // 提示用户可以评论
    //   uni.showToast({
    //     title: "请在底部输入评论",
    //     icon: "none",
    //     duration: 1500
    //   });
    // },

    shareWhisper() {
      uni.showActionSheet({
        itemList: ["复制链接", "保存图片"],
        success: (res) => {
          if (res.tapIndex === 0) {
            // 复制链接逻辑
            uni.setClipboardData({
              data: `分享一个有趣的悄悄话：${
                this.whisper.title || this.whisper.content
              }`,
              success: () => {
                uni.showToast({ title: "已复制到剪贴板", icon: "success" });
              },
            });
          }
        },
      });
    },

    formatTimestamp(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now.getTime() - date.getTime();

      // 小于1分钟
      if (diff < 60 * 1000) {
        return "刚刚";
      }

      // 小于1小时
      if (diff < 60 * 60 * 1000) {
        const minutes = Math.floor(diff / (60 * 1000));
        return `${minutes}分钟前`;
      }

      // 小于1天
      if (diff < 24 * 60 * 60 * 1000) {
        const hours = Math.floor(diff / (60 * 60 * 1000));
        return `${hours}小时前`;
      }

      // 超过1天，显示具体日期
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");

      return `${month}月${day}日 ${hours}:${minutes}`;
    },
  },
};
</script>

<style scoped>
.whisper-detail-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-top: 60rpx;
  padding-bottom: 140rpx;
  /* 为底部输入框留空间 */
}

.whisper-card {
  background: #fffbf0;
  margin: 30rpx 20rpx 20rpx 20rpx;
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.15);
  border: 2rpx solid #f0e6d2;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 25rpx;
  position: relative;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  border: 3rpx solid #fff;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.user-details {
  flex: 1;
}

/* 右上角分享按钮 */
.share-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70rpx;
  height: 70rpx;
  background: linear-gradient(135deg, #f8f4e6, #f0e6d2);
  border-radius: 50%;
  border: 2rpx solid #e8dcc6;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.share-button:active {
  transform: scale(0.9);
  background: linear-gradient(135deg, #f0e6d2, #e8dcc6);
}

.share-icon {
  font-size: 32rpx;
}

.username {
  font-size: 30rpx;
  font-weight: bold;
  color: #2c3e50;
  display: block;
  margin-bottom: 8rpx;
}

.timestamp {
  font-size: 22rpx;
  color: #7f8c8d;
}

.whisper-content {
  margin: 25rpx 0;
}

.whisper-title {
  font-size: 34rpx;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20rpx;
  display: block;
  line-height: 1.4;
}

.meta-info {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 25rpx;
  gap: 15rpx;
}

.mood-section {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f8f4e6, #f0e6d2);
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  border: 1rpx solid #e8dcc6;
}

.mood-emoji {
  font-size: 28rpx;
  margin-right: 8rpx;
}

.mood-text {
  font-size: 24rpx;
  color: #8d7b5f;
  font-weight: 500;
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
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

.content-text {
  font-size: 28rpx;
  color: #2c3e50;
  line-height: 1.7;
  margin: 25rpx 0;
  display: block;
  letter-spacing: 0.5rpx;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15rpx;
  margin-top: 25rpx;
}

.content-image {
  width: 100%;
  height: 200rpx;
  border-radius: 12rpx;
  object-fit: cover;
  border: 2rpx solid #f0e6d2;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

/* 互动统计区域 - 可交互 */
.interaction-stats {
  display: flex;
  align-items: center;
  gap: 30rpx;
  margin-top: 25rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #e8dcc6;
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
  padding: 10rpx 24rpx;
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

.stat-text {
  font-size: 24rpx;
  color: #666;
  font-weight: 500;
}

.comments-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  margin: 0 20rpx 20rpx;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.section-title {
  margin-bottom: 25rpx;
  padding-bottom: 15rpx;
  border-bottom: 2rpx solid #f1f5f9;
}

.title-text {
  font-size: 30rpx;
  font-weight: bold;
  color: #2c3e50;
}

.empty-comments {
  text-align: center;
  padding: 60rpx 0;
}

.empty-text {
  font-size: 26rpx;
  color: #9ca3af;
}

.comment-item {
  display: flex;
  margin-bottom: 30rpx;
  padding-bottom: 25rpx;
  border-bottom: 1rpx solid #f8fafc;
}

.comment-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.comment-avatar {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  margin-right: 15rpx;
  flex-shrink: 0;
  border: 2rpx solid #fff;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.1);
}

.comment-content {
  flex: 1;
}

.comment-user {
  font-size: 24rpx;
  color: #6b7280;
  margin-bottom: 8rpx;
  display: block;
  font-weight: 500;
}

.comment-text {
  font-size: 26rpx;
  color: #374151;
  line-height: 1.6;
  margin-bottom: 8rpx;
  display: block;
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.comment-time {
  font-size: 20rpx;
  color: #9ca3af;
}

.reply-btn {
  font-size: 22rpx;
  color: #667eea;
  padding: 4rpx 8rpx;
  cursor: pointer;
}

.reply-btn:active {
  background-color: rgba(102, 126, 234, 0.1);
  border-radius: 4rpx;
}

/* 回复区域样式 */
.replies-section {
  margin-top: 15rpx;
  margin-left: 20rpx;
  padding-left: 20rpx;
  border-left: 2rpx solid #f1f5f9;
}

.reply-item {
  display: flex;
  margin-bottom: 20rpx;
  padding-bottom: 15rpx;
  border-bottom: 1rpx solid #f8fafc;
}

.reply-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.reply-avatar {
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  margin-right: 12rpx;
  flex-shrink: 0;
  border: 2rpx solid #fff;
  box-shadow: 0 1rpx 4rpx rgba(0, 0, 0, 0.1);
}

.reply-content {
  flex: 1;
}

.reply-user {
  font-size: 22rpx;
  color: #6b7280;
  margin-bottom: 4rpx;
  display: block;
  font-weight: 500;
}

.reply-mention {
  font-size: 22rpx;
  color: #667eea;
  margin-bottom: 4rpx;
  display: block;
}

.reply-text {
  font-size: 24rpx;
  color: #374151;
  line-height: 1.5;
  margin-bottom: 6rpx;
  display: block;
}

.reply-actions {
  display: flex;
  align-items: center;
  gap: 15rpx;
}

.reply-time {
  font-size: 18rpx;
  color: #9ca3af;
}

.load-more-replies {
  text-align: center;
  padding: 15rpx;
  margin-top: 10rpx;
}

.load-more-text {
  font-size: 22rpx;
  color: #667eea;
  cursor: pointer;
}

.comment-input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20rpx);
  padding: 20rpx;
  border-top: 1rpx solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  z-index: 1000;
  /* 安全区域适配 */
  padding-bottom: calc(20rpx + constant(safe-area-inset-bottom));
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
}

.reply-hint {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f4e6;
  padding: 12rpx 16rpx;
  border-radius: 12rpx;
  margin-bottom: 15rpx;
  border: 1rpx solid #e8dcc6;
}

.reply-hint-text {
  font-size: 22rpx;
  color: #8d7b5f;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cancel-reply {
  font-size: 24rpx;
  color: #999;
  padding: 4rpx 8rpx;
  cursor: pointer;
}

.input-row {
  display: flex;
  align-items: center;
}

.comment-input {
  flex: 1;
  background-color: #f9fafb;
  border: 1rpx solid #e5e7eb;
  border-radius: 25rpx;
  padding: 15rpx 20rpx;
  font-size: 26rpx;
  margin-right: 15rpx;
  transition: all 0.3s ease;
}

.comment-input:focus {
  border-color: #667eea;
  background-color: #fff;
}

.send-button {
  background: linear-gradient(135deg, #e5e7eb, #d1d5db);
  padding: 15rpx 25rpx;
  border-radius: 25rpx;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.send-button.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.3);
}

.send-text {
  font-size: 26rpx;
  color: #6b7280;
  font-weight: 500;
}

.send-button.active .send-text {
  color: white;
}
</style>
