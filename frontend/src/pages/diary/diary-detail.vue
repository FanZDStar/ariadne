<template>
  <view class="diary-detail-container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
          <text class="back-text">返回</text>
        </view>
        <text class="navbar-title">碎碎念详情</text>
        <view class="placeholder"></view>
      </view>
    </view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-container">
      <text class="error-text">{{ error }}</text>
      <button class="retry-btn" @click="loadDiaryDetail">重试</button>
    </view>

    <!-- 详情内容 -->
    <scroll-view v-else-if="diary" class="detail-scroll-view" scroll-y>
      <view class="diary-detail-content">
        
        <!-- 标题 -->
        <view class="title-section">
          <text class="diary-title">{{ diary.title || '无标题' }}</text>
        </view>

        <!-- 标签和心情 -->
        <view class="meta-section">
          <view class="tags-container" v-if="diary.tags && diary.tags.length > 0">
            <text class="section-label">标签</text>
            <view class="tags-list">
              <text class="tag-item" v-for="tag in diary.tags" :key="tag">
                #{{ tag }}
              </text>
            </view>
          </view>
          
          <view class="mood-container">
            <text class="section-label">心情</text>
            <view class="mood-display">
              <text class="mood-emoji">{{ getMoodEmoji(diary.mood) }}</text>
              <text class="mood-text">{{ getMoodText(diary.mood) }}</text>
            </view>
          </view>
        </view>

        <!-- 正文内容 -->
        <view class="content-section">
          <text class="section-label">正文</text>
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
        </view>

        <!-- 图片展示 -->
        <view v-if="diary.images && diary.images.length > 0" class="images-section">
          <text class="section-label">图片 ({{ diary.images.length }})</text>
          <view class="images-grid">
            <view 
              v-for="(image, index) in diary.images" 
              :key="image.image_id" 
              class="image-item"
              :class="{ 'single-image': diary.images.length === 1 }"
            >
              <image 
                :src="getImageUrl(image.image_url)" 
                class="diary-image"
                mode="aspectFill"
                @click="previewImage(index)"
                @error="onImageError"
              />
            </view>
          </view>
        </view>

        <!-- 发布时间 -->
        <view class="time-section">
          <text class="section-label">发布时间</text>
          <view class="time-container">
            <text class="publish-date">{{ formatDetailDate(diary.created_at) }}</text>
            <text class="publish-time">{{ formatDetailTime(diary.created_at) }}</text>
          </view>
        </view>

      </view>
    </scroll-view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      diaryId: null,
      diary: null,
      loading: true,
      error: null,
      showFullContent: false,
    };
  },

  onLoad(option) {
    this.diaryId = option.id;
    if (this.diaryId) {
      this.loadDiaryDetail();
    } else {
      this.error = '缺少日记ID参数';
      this.loading = false;
    }
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
      return `http://127.0.0.1:8000${url}`;
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
  background-color: #f8f9fa;
}

/* 导航栏样式 */
.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-top: var(--status-bar-height);
}

.navbar-content {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30rpx;
}

.back-btn {
  display: flex;
  align-items: center;
  padding: 10rpx;
}

.back-icon {
  font-size: 36rpx;
  color: white;
  margin-right: 10rpx;
}

.back-text {
  font-size: 28rpx;
  color: white;
}

.navbar-title {
  font-size: 32rpx;
  font-weight: bold;
  color: white;
}

.placeholder {
  width: 120rpx;
}

/* 内容区域 */
.detail-scroll-view {
  margin-top: calc(88rpx + var(--status-bar-height));
  height: calc(100vh - 88rpx - var(--status-bar-height));
}

.diary-detail-content {
  padding: 40rpx 30rpx;
}

/* 加载和错误状态 */
.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400rpx;
}

.loading-text,
.error-text {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.retry-btn {
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 20rpx;
  padding: 20rpx 40rpx;
  font-size: 28rpx;
}

/* 标题区域 */
.title-section {
  margin-bottom: 40rpx;
}

.diary-title {
  font-size: 42rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.4;
}

/* 元信息区域 */
.meta-section {
  margin-bottom: 40rpx;
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.tags-container {
  margin-bottom: 30rpx;
}

.mood-container {
  margin-top: 10rpx;
}

.section-label {
  font-size: 24rpx;
  color: #888;
  margin-bottom: 15rpx;
  display: block;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.tag-item {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
}

.mood-display {
  display: flex;
  align-items: center;
  gap: 15rpx;
}

.mood-emoji {
  font-size: 40rpx;
}

.mood-text {
  font-size: 28rpx;
  color: #333;
}

/* 内容区域 */
.content-section {
  margin-bottom: 40rpx;
}

.content-container {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.content-text {
  font-size: 32rpx;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
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
  background-color: #f0f0f0;
  color: #007aff;
  border: none;
  border-radius: 20rpx;
  padding: 15rpx 30rpx;
  font-size: 24rpx;
}

/* 图片区域 */
.images-section {
  margin-bottom: 40rpx;
}

.images-grid {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.image-item.single-image .diary-image {
  grid-column: 1 / -1;
  max-width: 400rpx;
  margin: 0 auto;
}

.diary-image {
  width: 100%;
  height: 200rpx;
  border-radius: 15rpx;
  object-fit: cover;
}

/* 时间区域 */
.time-section {
  margin-bottom: 40rpx;
}

.time-container {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.publish-date {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 10rpx;
  display: block;
}

.publish-time {
  font-size: 28rpx;
  color: #666;
}
</style>
