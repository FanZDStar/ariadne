<template>
    <view class="diary-detail-container">
        <!-- 加载状态 -->
        <view v-if="loading" class="loading-container">
            <view class="loading-card">
                <text class="loading-text">加载中...</text>
            </view>
        </view>

        <!-- 错误状态 -->
        <view v-else-if="error" class="error-container">
            <view class="error-card">
                <text class="error-text">{{ error }}</text>
                <button class="retry-btn" @click="loadDiaryDetail">重试</button>
            </view>
        </view>

        <!-- 详情内容 -->
        <view v-else-if="diary" class="diary-content">
            <!-- 主要内容卡片 -->
            <view class="diary-card">
                <!-- 标题 -->
                <view class="title-section">
                    <text class="diary-title">{{ diary.title || '无标题' }}</text>
                    <text class="timestamp">{{ formatTimestamp(diary.created_at) }}</text>
                </view>

                <!-- 碎碎念内容 -->
                <view class="content-section">
                    <!-- 心情和标签 -->
                    <view class="meta-info">
                        <view class="mood-section">
                            <text class="mood-emoji">{{ getMoodEmoji(diary.mood) }}</text>
                            <text class="mood-text">{{ getMoodText(diary.mood) }}</text>
                        </view>
                        <view class="tags-section" v-if="diary.tags && diary.tags.length > 0">
                            <view class="tag-item" v-for="tag in diary.tags" :key="tag">
                                <text class="tag-text">#{{ tag }}</text>
                            </view>
                        </view>
                    </view>

                    <!-- 正文内容 -->
                    <view class="content-container">
                        <text class="content-text" :class="{ 'expanded': showFullContent }">{{ diary.content }}</text>
                        <view v-if="diary.content && diary.content.length > 200 && !showFullContent"
                            class="expand-btn-container">
                            <button class="expand-btn" @click="toggleContent">展开全文</button>
                        </view>
                        <view v-if="showFullContent && diary.content && diary.content.length > 200"
                            class="expand-btn-container">
                            <button class="expand-btn" @click="toggleContent">收起</button>
                        </view>
                    </view>

                    <!-- 图片展示 -->
                    <view v-if="diary.images && diary.images.length > 0" class="images-grid">
                        <image v-for="(image, index) in diary.images" :key="image.image_id" 
                            :src="getImageUrl(image.image_url)" class="content-image" mode="aspectFill"
                            @click="previewImage(index)" @error="onImageError" />
                    </view>

                    <!-- 详细时间信息 -->
                    <view class="detailed-time">
                        <text class="detailed-date">{{ formatDetailDate(diary.created_at) }}</text>
                        <text class="detailed-time-text">{{ formatDetailTime(diary.created_at) }}</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    // 页面加载
    onLoad(option) {
        this.diaryId = option.id;
        if (this.diaryId) {
            this.loadDiaryDetail();
        } else {
            this.error = '缺少日记ID参数';
            this.loading = false;
        }
    },

    data() {
        return {
            diaryId: null,
            diary: null,
            loading: true,
            error: null,
            showFullContent: false,
        };
    },

    methods: {
        async loadDiaryDetail() {
            this.loading = true;
            this.error = null;

            try {
                const token = storage.getToken();
                console.log('详情页面获取到的token:', token);
                console.log('要获取的日记ID:', this.diaryId);

                if (!token) {
                    this.error = '请先登录';
                    return;
                }

                const response = await api.getDiary(this.diaryId, token);
                this.diary = response;

                // 如果内容较短，默认展开全文
                if (this.diary.content && this.diary.content.length <= 200) {
                    this.showFullContent = true;
                }

            } catch (error) {
                console.error('获取日记详情失败:', error);
                this.error = error.message || '获取日记详情失败，请重试';
            } finally {
                this.loading = false;
            }
        },

        goBack() {
            uni.navigateBack({
                delta: 1
            });
        },

        toggleContent() {
            this.showFullContent = !this.showFullContent;
        },

        previewImage(index) {
            if (!this.diary.images || this.diary.images.length === 0) return;

            const urls = this.diary.images.map(img => this.getImageUrl(img.image_url));
            uni.previewImage({
                current: index,
                urls: urls
            });
        },

        getImageUrl(url) {
            if (!url) return '';
            if (url.startsWith('http')) return url;
            return `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}${url}`;
        },

        onImageError(e) {
            console.error('图片加载失败:', e);
        },

        getMoodEmoji(mood) {
            const moodMap = {
                'very_happy': '😄',
                'happy': '😊',
                'neutral': '😐',
                'sad': '😢',
                'very_sad': '😭'
            };
            return moodMap[mood] || '😐';
        },

        getMoodText(mood) {
            const moodMap = {
                'very_happy': '非常开心',
                'happy': '开心',
                'neutral': '平静',
                'sad': '难过',
                'very_sad': '非常难过'
            };
            return moodMap[mood] || '平静';
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
        },

        formatDetailDate(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
            const weekday = weekdays[date.getDay()];
            return `${year}年${month}月${day}日 ${weekday}`;
        },

        formatDetailTime(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${hours}:${minutes}`;
        }
    }
};
</script>

<style scoped>
.diary-detail-container {
    min-height: 100vh;
    background-color: #f5f5f5;
}

/* 加载和错误状态 */
.loading-container,
.error-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.loading-card,
.error-card {
    background: white;
    border-radius: 20rpx;
    padding: 60rpx 40rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
    text-align: center;
}

.loading-text,
.error-text {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 20rpx;
}

.retry-btn {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 20rpx;
    padding: 20rpx 40rpx;
    font-size: 28rpx;
}

/* 主要内容 */
.diary-content {
    padding: 20rpx;
    padding-bottom: 40rpx;
}

.diary-card {
    background: white;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

/* 标题区域 */
.title-section {
    margin-bottom: 20rpx;
    border-bottom: 1rpx solid #f1f5f9;
    padding-bottom: 20rpx;
}

.diary-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    line-height: 1.4;
    margin-bottom: 10rpx;
    display: block;
}

.timestamp {
    font-size: 24rpx;
    color: #999;
}

/* 内容区域 */
.content-section {
    margin-top: 20rpx;
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

.content-container {
    margin: 20rpx 0;
}

.content-text {
    font-size: 30rpx;
    line-height: 1.6;
    color: #374151;
    white-space: pre-wrap;
    word-wrap: break-word;
    display: block;
}

.content-text:not(.expanded) {
    display: -webkit-box;
    -webkit-line-clamp: 6;
    line-clamp: 6;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.expand-btn-container {
    margin-top: 20rpx;
    text-align: center;
}

.expand-btn {
    background-color: #f8fafc;
    color: #3b82f6;
    border: none;
    border-radius: 20rpx;
    padding: 15rpx 30rpx;
    font-size: 24rpx;
}

/* 图片展示 */
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

/* 详细时间信息 */
.detailed-time {
    margin-top: 30rpx;
    padding-top: 20rpx;
    border-top: 1rpx solid #f1f5f9;
    text-align: center;
}

.detailed-date {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 5rpx;
    display: block;
}

.detailed-time-text {
    font-size: 24rpx;
    color: #999;
}
</style>
