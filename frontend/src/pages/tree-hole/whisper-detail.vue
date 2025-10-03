<template>
    <view class="whisper-detail-container">
        <!-- 悄悄话详情卡片 -->
        <view class="whisper-card">
            <!-- 用户信息行 -->
            <view class="user-info">
                <image class="avatar" :src="getAvatarUrl()" mode="aspectFill" />
                <view class="user-details">
                    <text class="username">{{ getDisplayName() }}</text>
                    <text class="timestamp">{{ formatTimestamp(whisper.created_at) }}</text>
                </view>
            </view>

            <!-- 悄悄话内容 -->
            <view class="whisper-content">
                <!-- 标题 -->
                <text v-if="whisper.title" class="whisper-title">{{ whisper.title }}</text>

                <!-- 心情和标签 -->
                <view class="meta-info">
                    <view class="mood-section" v-if="whisper.mood">
                        <text class="mood-emoji">{{ getMoodEmoji(whisper.mood) }}</text>
                        <text class="mood-text">{{ getMoodText(whisper.mood) }}</text>
                    </view>
                    <view class="tags-section" v-if="whisper.tags && whisper.tags.length > 0">
                        <view class="tag-item" v-for="tag in whisper.tags" :key="tag">
                            <text class="tag-text">#{{ tag }}</text>
                        </view>
                    </view>
                </view>

                <!-- 正文内容 -->
                <text class="content-text">{{ whisper.content }}</text>

                <!-- 图片展示 -->
                <view class="images-grid" v-if="whisper.images && whisper.images.length > 0">
                    <image v-for="(image, index) in whisper.images" :key="index" :src="getImageUrl(image.image_url)"
                        class="content-image" mode="aspectFill" @click="previewImage(image.image_url)" />
                </view>
            </view>

            <!-- 互动统计 -->
            <view class="interaction-stats">
                <view class="stat-item">
                    <text class="stat-icon">❤️</text>
                    <text class="stat-text">{{ whisper.like_count || 0 }}</text>
                </view>
                <view class="stat-item">
                    <text class="stat-icon">💬</text>
                    <text class="stat-text">{{ whisper.comment_count || 0 }}</text>
                </view>
            </view>
        </view>

        <!-- 操作按钮 -->
        <view class="action-bar">
            <view class="action-button" :class="{ liked: whisper.liked }" @click="toggleLike">
                <text class="action-icon">{{ whisper.liked ? '❤️' : '🤍' }}</text>
                <text class="action-text">{{ whisper.liked ? '已点赞' : '点赞' }}</text>
            </view>
            <view class="action-button" @click="goToChat">
                <text class="action-icon">💬</text>
                <text class="action-text">评论</text>
            </view>
            <view class="action-button" @click="shareWhisper">
                <text class="action-icon">📤</text>
                <text class="action-text">分享</text>
            </view>
        </view>

        <!-- 评论列表区域 -->
        <view class="comments-section">
            <view class="section-title">
                <text class="title-text">评论 ({{ comments.length }})</text>
            </view>

            <view v-if="comments.length === 0" class="empty-comments">
                <text class="empty-text">还没有评论，快来抢沙发吧~</text>
            </view>

            <view v-for="comment in comments" :key="comment.comment_id" class="comment-item">
                <image class="comment-avatar" :src="getCommentAvatarUrl(comment)" mode="aspectFill" />
                <view class="comment-content">
                    <text class="comment-user">{{ getCommentUserName(comment) }}</text>
                    <text class="comment-text">{{ comment.content }}</text>
                    <text class="comment-time">{{ formatTimestamp(comment.created_at) }}</text>
                </view>
            </view>
        </view>

        <!-- 底部评论输入框 -->
        <view class="comment-input-bar">
            <input class="comment-input" v-model="newComment" placeholder="说些什么吧..." @confirm="submitComment"
                confirm-type="send" />
            <view class="send-button" @click="submitComment" :class="{ active: newComment.trim() }">
                <text class="send-text">发送</text>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            whisper: null,
            comments: [],
            newComment: '',
            whisperId: null
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
        async loadWhisperDetail() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({ title: '请先登录', icon: 'none' });
                return;
            }

            try {
                this.whisper = await api.getWhisperDetail(token, this.whisperId);
            } catch (error) {
                console.error('Failed to load whisper detail:', error);
                uni.showToast({ title: '加载失败', icon: 'none' });
            }
        },

        async loadComments() {
            const token = storage.getToken();
            if (!token) return;

            try {
                this.comments = await api.getWhisperComments(token, this.whisperId);
            } catch (error) {
                console.error('Failed to load comments:', error);
                this.comments = [];
            }
        },

        getAvatarUrl() {
            if (!this.whisper) return '';

            // 如果是匿名悄悄话，使用匿名头像
            if (this.whisper.is_anonymous && this.whisper.anonymous_avatar) {
                return this.whisper.anonymous_avatar;
            }

            // 使用用户头像
            if (this.whisper.user && this.whisper.user.avatar) {
                return api.getImageUrl(this.whisper.user.avatar);
            }

            // 默认头像
            return '/static/avatar/头像.png';
        },

        getDisplayName() {
            if (!this.whisper) return '';

            // 如果是匿名悄悄话，显示匿名名称
            if (this.whisper.is_anonymous) {
                return this.whisper.anonymous_name || 'ariadne_匿名用户';
            }

            // 显示真实用户名
            return this.whisper.user ? this.whisper.user.username : '未知用户';
        },

        getImageUrl(imageUrl) {
            if (!imageUrl) return '';

            // 如果是相对路径，添加static前缀
            if (!imageUrl.startsWith('http') && !imageUrl.startsWith('/static/')) {
                return `/static/${imageUrl}`;
            }

            return imageUrl;
        },

        getMoodEmoji(mood) {
            const moodEmojis = {
                'very_happy': '😄',
                'happy': '😊',
                'neutral': '😐',
                'sad': '😢',
                'very_sad': '😭'
            };
            return moodEmojis[mood] || '😐';
        },

        getMoodText(mood) {
            const moodTexts = {
                'very_happy': '超开心',
                'happy': '开心',
                'neutral': '一般',
                'sad': '难过',
                'very_sad': '很难过'
            };
            return moodTexts[mood] || '一般';
        },

        getCommentAvatarUrl(comment) {
            // 评论头像逻辑，类似悄悄话头像
            if (comment.is_anonymous && comment.anonymous_avatar) {
                return comment.anonymous_avatar;
            }
            if (comment.user && comment.user.avatar) {
                return api.getImageUrl(comment.user.avatar);
            }
            return '/static/avatar/头像.png';
        },

        getCommentUserName(comment) {
            if (comment.is_anonymous) {
                return comment.anonymous_name || 'ariadne_匿名用户';
            }
            return comment.user ? comment.user.username : '未知用户';
        },

        async toggleLike() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({ title: '请先登录', icon: 'none' });
                return;
            }

            try {
                const result = await api.toggleWhisperLike(token, this.whisperId);
                this.whisper.liked = result.liked;

                // 更新点赞数
                if (result.liked) {
                    this.whisper.like_count++;
                } else {
                    this.whisper.like_count--;
                }

                uni.showToast({
                    title: result.liked ? '已点赞' : '已取消点赞',
                    icon: 'success'
                });
            } catch (error) {
                console.error('Failed to toggle like:', error);
                uni.showToast({ title: '操作失败', icon: 'none' });
            }
        },

        async submitComment() {
            if (!this.newComment.trim()) return;

            const token = storage.getToken();
            if (!token) {
                uni.showToast({ title: '请先登录', icon: 'none' });
                return;
            }

            try {
                await api.createWhisperComment(token, this.whisperId, {
                    content: this.newComment.trim(),
                    is_anonymous: true // 默认匿名评论
                });

                this.newComment = '';
                this.loadComments(); // 重新加载评论列表

                // 更新评论数
                this.whisper.comment_count++;

                uni.showToast({ title: '评论成功', icon: 'success' });
            } catch (error) {
                console.error('Failed to submit comment:', error);
                uni.showToast({ title: '评论失败', icon: 'none' });
            }
        },

        previewImage(imageUrl) {
            const fullUrl = this.getImageUrl(imageUrl);
            uni.previewImage({
                urls: [fullUrl],
                current: fullUrl
            });
        },

        goToChat() {
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-chat?whisper_id=${this.whisperId}`
            });
        },

        shareWhisper() {
            uni.showActionSheet({
                itemList: ['复制链接', '保存图片'],
                success: (res) => {
                    if (res.tapIndex === 0) {
                        // 复制链接逻辑
                        uni.setClipboardData({
                            data: `分享一个有趣的悄悄话：${this.whisper.title || this.whisper.content}`,
                            success: () => {
                                uni.showToast({ title: '已复制到剪贴板', icon: 'success' });
                            }
                        });
                    }
                }
            });
        },

        formatTimestamp(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const diff = now.getTime() - date.getTime();

            // 小于1分钟
            if (diff < 60 * 1000) {
                return '刚刚';
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
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');

            return `${month}月${day}日 ${hours}:${minutes}`;
        }
    }
};
</script>

<style scoped>
.whisper-detail-container {
    min-height: 100vh;
    background-color: #f5f5f5;
    padding-bottom: 120rpx;
    /* 为底部输入框留空间 */
}

.whisper-card {
    background: white;
    margin: 20rpx;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.user-info {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    margin-right: 20rpx;
}

.user-details {
    flex: 1;
}

.username {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 8rpx;
}

.timestamp {
    font-size: 24rpx;
    color: #999;
}

.whisper-content {
    margin: 20rpx 0;
}

.whisper-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 15rpx;
    display: block;
}

.meta-info {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 20rpx;
    gap: 15rpx;
}

.mood-section {
    display: flex;
    align-items: center;
    background-color: #f0f9ff;
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
}

.mood-emoji {
    font-size: 28rpx;
    margin-right: 8rpx;
}

.mood-text {
    font-size: 24rpx;
    color: #0ea5e9;
}

.tags-section {
    display: flex;
    flex-wrap: wrap;
    gap: 10rpx;
}

.tag-item {
    background-color: #f3f4f6;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.tag-text {
    font-size: 22rpx;
    color: #6b7280;
}

.content-text {
    font-size: 30rpx;
    color: #374151;
    line-height: 1.6;
    margin: 20rpx 0;
    display: block;
}

.images-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10rpx;
    margin-top: 20rpx;
}

.content-image {
    width: 200rpx;
    height: 200rpx;
    border-radius: 12rpx;
    flex-shrink: 0;
}

.interaction-stats {
    display: flex;
    align-items: center;
    margin-top: 20rpx;
    padding-top: 20rpx;
    border-top: 1rpx solid #f1f5f9;
}

.stat-item {
    display: flex;
    align-items: center;
    margin-right: 30rpx;
}

.stat-icon {
    font-size: 28rpx;
    margin-right: 8rpx;
}

.stat-text {
    font-size: 26rpx;
    color: #64748b;
}

.action-bar {
    display: flex;
    justify-content: space-around;
    background: white;
    margin: 0 20rpx 20rpx;
    border-radius: 20rpx;
    padding: 20rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.action-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15rpx;
    border-radius: 12rpx;
    transition: background-color 0.3s;
}

.action-button.liked {
    background-color: #fef2f2;
}

.action-button:active {
    background-color: #f8fafc;
}

.action-icon {
    font-size: 32rpx;
    margin-bottom: 8rpx;
}

.action-text {
    font-size: 24rpx;
    color: #64748b;
}

.comments-section {
    background: white;
    margin: 0 20rpx 20rpx;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.section-title {
    margin-bottom: 25rpx;
    padding-bottom: 15rpx;
    border-bottom: 1rpx solid #f1f5f9;
}

.title-text {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.empty-comments {
    text-align: center;
    padding: 60rpx 0;
}

.empty-text {
    font-size: 28rpx;
    color: #9ca3af;
}

.comment-item {
    display: flex;
    margin-bottom: 25rpx;
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
}

.comment-content {
    flex: 1;
}

.comment-user {
    font-size: 26rpx;
    color: #6b7280;
    margin-bottom: 8rpx;
    display: block;
}

.comment-text {
    font-size: 28rpx;
    color: #374151;
    line-height: 1.5;
    margin-bottom: 8rpx;
    display: block;
}

.comment-time {
    font-size: 22rpx;
    color: #9ca3af;
}

.comment-input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 20rpx;
    display: flex;
    align-items: center;
    border-top: 1rpx solid #e5e7eb;
    z-index: 1000;
}

.comment-input {
    flex: 1;
    background-color: #f9fafb;
    border: 1rpx solid #e5e7eb;
    border-radius: 25rpx;
    padding: 15rpx 20rpx;
    font-size: 28rpx;
    margin-right: 15rpx;
}

.send-button {
    background-color: #e5e7eb;
    padding: 15rpx 25rpx;
    border-radius: 25rpx;
    transition: background-color 0.3s;
}

.send-button.active {
    background-color: #3b82f6;
}

.send-text {
    font-size: 28rpx;
    color: #6b7280;
}

.send-button.active .send-text {
    color: white;
}
</style>
