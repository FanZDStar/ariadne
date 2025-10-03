<template>
    <view class="listen-container">
        <view class="content-wrapper">
            <view v-if="whisper" class="whisper-note" @click="goToWhisperDetail">
                <!-- 第一行：头像和匿名名称 -->
                <view class="whisper-header">
                    <image class="avatar" :src="getAvatarUrl()" mode="aspectFill" />
                    <text class="nickname">{{ getDisplayName() }}</text>
                </view>

                <!-- 第二行：心情和标签 -->
                <view class="whisper-meta">
                    <view class="mood-section" v-if="whisper.mood">
                        <text class="mood-emoji">{{ getMoodEmoji(whisper.mood) }}</text>
                        <text class="mood-text">{{ getMoodText(whisper.mood) }}</text>
                    </view>
                    <view class="tags-section" v-if="whisper.tags && whisper.tags.length > 0">
                        <view class="tag-item" v-for="tag in whisper.tags.slice(0, 3)" :key="tag">
                            <text class="tag-text">#{{ tag }}</text>
                        </view>
                    </view>
                </view>

                <!-- 第三行：正文和图片 -->
                <scroll-view scroll-y="true" class="whisper-scroll-view">
                    <view class="content-section">
                        <text class="whisper-content">{{ getDisplayContent() }}</text>
                        <view class="images-section" v-if="whisper.images && whisper.images.length > 0">
                            <image v-for="(image, index) in whisper.images.slice(0, 2)" :key="index"
                                :src="getImageUrl(image.image_url)" class="whisper-image" mode="aspectFill"
                                @click="previewImage(image.image_url)" />
                        </view>
                    </view>
                </scroll-view>
            </view>

            <view v-else class="empty-state">
                <text class="empty-text">暂时没有新的悄悄话了，\n不如去写下你的心事吧~</text>
            </view>
        </view>

        <view class="footer-actions">
            <view class="action-bubble like-bubble" @click="toggleLike">
                <text class="action-icon">{{ liked ? '❤️' : '🤍' }}</text>
                <text class="action-text">{{ likeCount }}</text>
            </view>
            <view class="action-bubble comment-bubble" @click="goToChat">
                <text class="action-icon">💬</text>
                <text class="action-text">评论</text>
            </view>
            <button class="next-button" @click="fetchRandomWhisper">换一个</button>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            whisper: null,
            liked: false,
            likeCount: 0
        };
    },
    onLoad() {
        this.fetchRandomWhisper();
    },
    methods: {
        async fetchRandomWhisper() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }
            try {
                const whisper = await api.getRandomWhisper(token);
                this.whisper = whisper;
                this.likeCount = whisper.like_count;
                this.liked = whisper.liked;
            } catch (error) {
                this.whisper = null; // 清空旧数据
                console.error('Failed to fetch random whisper:', error);
                uni.showToast({
                    title: '暂时没有悄悄话了',
                    icon: 'none'
                });
            }
        },

        // 获取头像URL
        getAvatarUrl() {
            if (!this.whisper) return '/static/avatar.png';

            // 如果是匿名且有匿名头像，使用匿名头像
            if (this.whisper.is_anonymous && this.whisper.anonymous_avatar) {
                return this.whisper.anonymous_avatar;
            }

            // 否则使用用户头像
            return this.whisper.user?.avatar_url || '/static/avatar.png';
        },

        // 获取显示名称
        getDisplayName() {
            if (!this.whisper) return '匿名用户';

            // 如果是匿名且有匿名名称，使用匿名名称
            if (this.whisper.is_anonymous && this.whisper.anonymous_name) {
                return this.whisper.anonymous_name;
            }

            // 如果是匿名但没有匿名名称，显示默认匿名
            if (this.whisper.is_anonymous) {
                return '匿名用户';
            }

            // 否则使用用户昵称
            return this.whisper.user?.nickname || '匿名用户';
        },

        // 获取心情emoji
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

        // 获取心情文本
        getMoodText(mood) {
            const moodTexts = {
                'very_happy': '超开心',
                'happy': '开心',
                'neutral': '平静',
                'sad': '难过',
                'very_sad': '很难过'
            };
            return moodTexts[mood] || '平静';
        },

        // 获取显示内容（限制50字）
        getDisplayContent() {
            if (!this.whisper || !this.whisper.content) return '';
            const content = this.whisper.content;
            if (content.length > 50) {
                return content.substring(0, 50) + '...';
            }
            return content;
        },

        // 获取图片URL
        getImageUrl(imageUrl) {
            if (imageUrl.startsWith('http')) {
                return imageUrl;
            }

            // 如果是静态资源路径（不包含 /uploads/），使用静态资源处理
            if (!imageUrl.includes('/uploads/')) {
                // 处理静态资源路径
                if (imageUrl.startsWith('/')) {
                    return `/static${imageUrl}`;
                } else {
                    return `/static/${imageUrl}`;
                }
            }

            // 如果是上传的图片，使用API base URL
            const baseUrl = process.env.VUE_APP_API_BASE_URL;
            if (!baseUrl) {
                console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
                return imageUrl;
            }
            if (imageUrl.startsWith('/')) {
                return baseUrl + imageUrl;
            } else {
                return baseUrl + '/' + imageUrl;
            }
        },

        // 预览图片
        previewImage(imageUrl) {
            const fullImageUrl = this.getImageUrl(imageUrl);
            const allImages = this.whisper.images.map(img => this.getImageUrl(img.image_url));

            uni.previewImage({
                current: fullImageUrl,
                urls: allImages
            });
        },
        async toggleLike() {
            if (!this.whisper) return;
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }
            try {
                await api.likeWhisper(token, this.whisper.whisper_id);
                this.liked = !this.liked;
                this.likeCount += this.liked ? 1 : -1;
            } catch (error) {
                console.error('Failed to toggle like:', error);
            }
        },
        goToWhisperDetail() {
            if (!this.whisper) return;
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-detail?whisper_id=${this.whisper.whisper_id}`
            });
        },
        goToChat() {
            if (!this.whisper) return;
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-chat?whisper_id=${this.whisper.whisper_id}`
            });
        }
    }
};
</script>

<style scoped>
.listen-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f4f4f4;
    overflow: hidden;
}

.content-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40rpx;
    padding-bottom: 200rpx;
    /* 为底部按钮留出空间 */
}

.whisper-note {
    display: flex;
    flex-direction: column;
    width: 80%;
    max-width: 600rpx;
    height: 70vh;
    max-height: 1000rpx;
    background-color: #fffbe8;
    /* 淡黄色，像便签纸 */
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.1);
    border: 1rpx solid #eee;
}

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
    border: 2rpx solid #fff;
}

.nickname {
    font-weight: bold;
    font-size: 32rpx;
    color: #555;
}

.whisper-scroll-view {
    flex: 1;
    height: 100%;
    /* 必须设置高度才能在小程序中滚动 */
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
    font-size: 26rpx;
    color: #666;
    background-color: #f0f0f0;
    padding: 5rpx 15rpx;
    border-radius: 20rpx;
}

.tags-section {
    display: flex;
    flex-wrap: wrap;
    gap: 10rpx;
}

.tag-item {
    background-color: #e3f2fd;
    padding: 5rpx 12rpx;
    border-radius: 15rpx;
}

.tag-text {
    font-size: 24rpx;
    color: #1976d2;
}

/* 内容区域 */
.content-section {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.whisper-content {
    font-size: 30rpx;
    color: #333;
    line-height: 1.8;
}

/* 图片区域 */
.images-section {
    display: flex;
    gap: 15rpx;
    flex-wrap: wrap;
}

.whisper-image {
    width: 200rpx;
    height: 200rpx;
    border-radius: 10rpx;
    object-fit: cover;
}

.empty-state {
    text-align: center;
    color: #888;
}

.empty-text {
    font-size: 30rpx;
    line-height: 1.6;
}

.footer-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 30rpx;
    padding-bottom: calc(30rpx + constant(safe-area-inset-bottom));
    padding-bottom: calc(30rpx + env(safe-area-inset-bottom));
    background-color: #f4f4f4;
    border-top: 1rpx solid #e0e0e0;
}

.action-bubble {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15rpx 30rpx;
    border-radius: 40rpx;
    background-color: #fff;
    box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.08);
}

.action-icon {
    font-size: 40rpx;
    margin-right: 15rpx;
}

.action-text {
    font-size: 28rpx;
    color: #333;
}

.next-button {
    background-color: #007aff;
    color: white;
    border-radius: 40rpx;
    font-size: 28rpx;
    padding: 0 40rpx;
    height: 80rpx;
    line-height: 80rpx;
}
</style>