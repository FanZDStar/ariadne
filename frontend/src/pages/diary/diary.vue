<template>
  <view class="diary-container">
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="back-to-journey" v-if="isAtTop" @click="goBackToJourney">
          <text class="back-icon">←</text>
        </view>
        <view class="back-to-top-hint" v-if="showBackToTopHint" @click="scrollToTop">
          <text class="back-icon">↑</text>
          <text class="back-text">回到顶部</text>
        </view>

        <text class="navbar-title" :class="{ 'hidden': showBackToTopHint }">
          碎碎念
        </text>

        <view class="manage-btn" @click="toggleManagementMode">
          <text class="manage-icon">{{ managementMode ? '完成' : '管理' }}</text>
        </view>
      </view>
    </view>

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

    <view class="diary-content">
      <scroll-view class="diary-scroll-view" scroll-y @scroll="onScroll" :scroll-top="scrollTop"
        :enable-back-to-top="true" ref="scrollView" id="scrollView">
        <view class="diary-list">
          <view class="diary-item" v-for="diary in diaryList" :key="diary.diary_id">
            <view class="diary-header">
              <text class="diary-date">{{ formatDiaryDate(diary.created_at) }}</text>
              <text class="diary-time">{{ formatDiaryTime(diary.created_at) }}</text>
            </view>
            <view class="diary-main-content">
              <text class="content-text">{{ diary.content }}</text>
            </view>

            <view class="diary-images" v-if="diary.images && diary.images.length > 0">
              <view class="image-grid"
                :class="{ 'single-image': diary.images.length === 1, 'multi-images': diary.images.length > 1 }">
                <view class="image-wrapper" v-for="image in diary.images.slice(0, 9)" :key="image.image_id">
                  <image :src="getImageUrl(image.image_url)" class="diary-image" mode="aspectFill"
                    @click="previewImage(diary.images, image.image_url)" />
                </view>

                <view class="image-wrapper more-images" v-if="diary.images.length > 9">
                  <text class="more-count">+{{ diary.images.length - 9 }}</text>
                </view>
              </view>
            </view>

            <view class="diary-footer">
              <view class="mood-tag">
                <text>{{ getMoodEmoji(diary.mood) }}</text>
              </view>
              <view v-if="managementMode" class="delete-btn" @click="confirmDelete(diary.diary_id)">
                <text class="delete-icon">🗑️</text>
              </view>
            </view>
          </view>

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
      isAtTop: true, // 是否位于顶部
      managementMode: false, // 是否处于管理模式
    }
  },

  onLoad() {
    this.loadDiaries();
  },

  onShow() {
    // 页面显示时重新加载日记，确保新建或删除后能刷新
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

    toggleManagementMode() {
      this.managementMode = !this.managementMode;
    },

    confirmDelete(diaryId) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这篇碎碎念吗？',
        success: (res) => {
          if (res.confirm) {
            this.deleteDiary(diaryId);
          }
        }
      });
    },

    async deleteDiary(diaryId) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      try {
        // 后端删除成功后，前端直接移除对应项
        await api.deleteDiary(token, diaryId);
        this.diaryList = this.diaryList.filter(diary => diary.diary_id !== diaryId);
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        });
      } catch (error) {
        console.error('删除日记失败:', error);
        uni.showToast({
          title: '删除失败',
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
        url: '/pages/journey/journey'
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

    getImageUrl(imageUrl) {
      if (imageUrl.startsWith('http')) {
        return imageUrl;
      }
      const baseUrl = process.env.VUE_APP_API_BASE_URL || 'https://ariadne.nuyoahming.xyz';
      // const baseUrl = 'http://127.0.0.1:8000';
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

    onScroll(e) {
      const scrollTop = e.detail.scrollTop;
      const scrollRatio = Math.min(scrollTop / 200, 1);
      const newHeight = Math.max(
        this.minBackgroundHeight,
        this.maxBackgroundHeight - (this.maxBackgroundHeight - this.minBackgroundHeight) * scrollRatio
      );

      this.backgroundHeight = newHeight;
      this.showBackToTopHint = scrollTop > this.scrollThreshold;
      this.isAtTop = scrollTop === 0;
    },

    scrollToTop() {
      this.scrollTop = 1;
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

.diary-main-content .content-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 20rpx;
  word-wrap: break-word;
}

/* 图片展示样式 */
.diary-images {
  margin-bottom: 20rpx;
  margin-top: 20rpx;
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

.manage-btn {
  position: absolute;
  right: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.manage-icon {
  font-size: 28rpx;
  color: white;
}

.delete-btn {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete-icon {
  font-size: 30rpx;
}
</style>