<template>
  <view class="diary-container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <view class="navbar-content">
        <!-- 返回上一级按钮 -->
        <view class="back-to-journey" v-if="isAtTop" @click="goBackToJourney">
          <text class="back-icon">←</text>
        </view>
        <!-- 返回顶部提示 -->
        <view class="back-to-top-hint" v-if="showBackToTopHint" @click="scrollToTop">
          <text class="back-icon">↑</text>
          <text class="back-text">回到顶部</text>
        </view>

        <!-- 默认标题 -->
        <text class="navbar-title" :class="{ 'hidden': showBackToTopHint }">
          情感日记
        </text>
      </view>
    </view>

    <!-- 上半屏：背景图片选择区域 -->
    <view class="background-section" :style="{ height: backgroundHeight + 'px' }">
      <swiper class="background-swiper" indicator-dots indicator-color="#ffffff80" indicator-active-color="#ffffff">
        <swiper-item>
          <view class="background-item" style="background-color: #ffafcc;">
            <text class="background-label">粉色心情</text>
          </view>
        </swiper-item>
        <swiper-item>
          <view class="background-item" style="background-color: #a2d2ff;">
            <text class="background-label">蓝色忧郁</text>
          </view>
        </swiper-item>
        <swiper-item>
          <view class="background-item" style="background-color: #ffcad4;">
            <text class="background-label">温柔时光</text>
          </view>
        </swiper-item>
        <swiper-item>
          <view class="background-item" style="background-color: #cdb4db;">
            <text class="background-label">紫色梦境</text>
          </view>
        </swiper-item>
      </swiper>

      <view class="new-diary-btn" @click="createNewDiary">
        <text class="btn-text">✍️ 写日记</text>
      </view>
    </view>

    <!-- 日记列表区域 -->
    <view class="diary-content">
      <scroll-view class="diary-scroll-view" scroll-y @scroll="onScroll" :scroll-top="scrollTop"
        :enable-back-to-top="true" ref="scrollView" id="scrollView">
        <view class="diary-list">
          <!-- 日记条目 -->
          <view class="diary-item" v-for="diary in diaryList" :key="diary.diary_id">
            <view class="diary-header">
              <text class="diary-date">{{ formatDiaryDate(diary.created_at) }}</text>
              <text class="diary-time">{{ formatDiaryTime(diary.created_at) }}</text>
            </view>
            <view class="diary-content">
              <text class="content-text">{{ diary.content }}</text>
            </view>

            <view class="diary-images" v-if="diary.images && diary.images.length > 0">
              <view class="image-grid"
                :class="{ 'single-image': diary.images.length === 1, 'multi-images': diary.images.length > 1 }">
                <view class="image-wrapper" v-for="image in diary.images.slice(0, 9)" :key="image.image_id">
                  <image :src="getImageUrl(image.image_url)" class="diary-image" mode="aspectFill"
                    @click="previewImage(diary.images, image.image_url)" />
                </view>

                <!-- 显示更多图片数量 -->
                <view class="image-wrapper more-images" v-if="diary.images.length > 9">
                  <text class="more-count">+{{ diary.images.length - 9 }}</text>
                </view>
              </view>
            </view>

            <view class="diary-footer">
              <view class="mood-tag">
                <text>{{ getMoodEmoji(diary.mood) }}</text>
              </view>
              <view class="action-buttons">
                <text class="action-btn">❤️ 0</text>
                <text class="action-btn">💬 0</text>
              </view>
            </view>
          </view>

          <!-- 没有日记时的提示 -->
          <view v-if="diaryList.length === 0" class="empty-diary">
            <text class="empty-text">还没有写过日记，点击右上角开始记录吧！</text>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      diaryList: [],
      scrollTop: 0,
      backgroundHeight: Math.round(uni.getSystemInfoSync().windowHeight * 0.4), // 初始高度为40%屏幕高度
      maxBackgroundHeight: Math.round(uni.getSystemInfoSync().windowHeight * 0.4), // 最大高度
      minBackgroundHeight: 80, // 最小高度
      showBackToTopHint: false, // 是否显示回到顶部提示
      scrollThreshold: 300, // 滚动多少距离后显示回到顶部提示
      isAtTop: true // 是否位于顶部
    }
  },

  onLoad() {
    this.loadDiaries();
  },

  methods: {
    async loadDiaries() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      try {
        const diaries = await api.getUserDiaries(token);
        this.diaryList = diaries;
      } catch (error) {
        console.error('获取日记失败:', error);
        uni.showToast({
          title: '获取日记失败',
          icon: 'none'
        });
      }
    },

    createNewDiary() {
      uni.navigateTo({
        url: '/pages/diary/write-diary'
      });
    },
    goBackToJourney() {
      uni.switchTab({
        url: '/pages/journey/journey' // 跳转到 Tab 页面
      });
    },
    formatDiaryDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
    },

    formatDiaryTime(dateString) {
      const date = new Date(dateString);
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    },

    getMoodEmoji(mood) {
      const moodMap = {
        'very_happy': '😄',
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'very_sad': '😭'
      };
      return moodMap[mood] || '😊';
    },

    // 修改这个方法，确保正确处理图片URL
    getImageUrl(imageUrl) {
      // 如果已经是完整URL，直接返回
      if (imageUrl.startsWith('http')) {
        return imageUrl;
      }

      // 如果是相对路径，拼接基础URL
      const baseUrl = 'http://127.0.0.1:8000';
      if (imageUrl.startsWith('/')) {
        return baseUrl + imageUrl;
      } else {
        return baseUrl + '/' + imageUrl;
      }
    },

    previewImage(images, currentImage) {
      const urls = images.map(img => this.getImageUrl(img.image_url));
      uni.previewImage({
        urls: urls,
        current: this.getImageUrl(currentImage)
      });
    },

    // 滚动事件处理
    onScroll(e) {
      const scrollTop = e.detail.scrollTop;

      // 根据滚动距离调整背景高度
      // 滚动越多，背景越小
      const scrollRatio = Math.min(scrollTop / 200, 1); // 200px滚动距离内完成变化
      const newHeight = Math.max(
        this.minBackgroundHeight,
        this.maxBackgroundHeight - (this.maxBackgroundHeight - this.minBackgroundHeight) * scrollRatio
      );

      this.backgroundHeight = newHeight;

      // 控制回到顶部提示的显示/隐藏
      this.showBackToTopHint = scrollTop > this.scrollThreshold;
      this.isAtTop = scrollTop === 0; // 判断是否位于顶部
    },

    // 滚动到顶部
    scrollToTop() {
      this.scrollTop = 1;
      // 强制刷新以触发滚动
      this.$nextTick(() => {
        this.scrollTop = 0;
      });
    }
  }
}
</script>

<style scoped>

/* 新增返回上一级按钮样式 */
.back-to-journey {
  position: absolute;
  left: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.back-icon {
  font-size: 32rpx;
  color: white;
  margin-right: 10rpx;
}
.diary-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  position: relative;
  padding-top: var(--status-bar-height);
}

/* 自定义导航栏 */
.custom-navbar {
  position: fixed;
  top: var(--status-bar-height);
  left: 0;
  right: 0;
  height: 44px;
  background-color: #ffafcc;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.navbar-title {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
  transition: opacity 0.3s ease;
}

.navbar-title.hidden {
  opacity: 0;
}

/* 回到顶部提示 */
.back-to-top-hint {
  position: absolute;
  left: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.back-icon {
  font-size: 32rpx;
  color: white;
  margin-right: 10rpx;
}

.back-text {
  font-size: 28rpx;
  color: white;
}

/* 上半屏：背景图片选择区域 */
.background-section {
  position: relative;
  transition: height 0.1s ease-out;
  flex-shrink: 0;
  margin-top: calc(var(--status-bar-height) + 44px);
}

.background-swiper {
  height: 100%;
}

.background-item {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-label {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
}

.new-diary-btn {
  position: absolute;
  bottom: 30rpx;
  right: 30rpx;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20rpx 30rpx;
  border-radius: 50rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
  z-index: 100;
  transition: all 0.1s ease-out;
}

.btn-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

/* 日记内容区域 */
.diary-content {
  flex: 1;
  background-color: #f5f5f5;
  padding: 30rpx;
  padding-top: 0;
  border-top-left-radius: 40rpx;
  border-top-right-radius: 40rpx;
  margin-top: -20rpx;
  overflow: hidden;
}

.diary-scroll-view {
  height: 100%;
}

.diary-list {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
  padding-bottom: 30rpx;
  padding-top: 20rpx;
}

.diary-item {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.diary-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.diary-date {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.diary-time {
  font-size: 24rpx;
  color: #999;
}

.diary-content .content-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 20rpx;
  word-wrap: break-word;
}

/* 图片展示样式 */
.diary-images {
  margin-bottom: 20rpx;
}

.image-grid {
  display: grid;
  gap: 10rpx;
}

.single-image {
  width: 60%;
}

.single-image .image-wrapper {
  width: 100%;
  height: 300rpx;
}

.multi-images {
  grid-template-columns: repeat(3, 1fr);
}

.multi-images .image-wrapper {
  aspect-ratio: 1;
}

.image-wrapper {
  position: relative;
  border-radius: 10rpx;
  overflow: hidden;
}

.diary-image {
  width: 100%;
  height: 100%;
  vertical-align: middle;
}

.more-images {
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.more-count {
  color: white;
  font-size: 28rpx;
  font-weight: bold;
}

.diary-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mood-tag {
  font-size: 36rpx;
}

.action-buttons {
  display: flex;
  gap: 30rpx;
}

.action-btn {
  font-size: 24rpx;
  color: #999;
}

.empty-diary {
  text-align: center;
  padding: 60rpx 0;
  background-color: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style>