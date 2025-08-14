<template>
  <view class="diary-container">
    <!-- 上半屏：背景图片选择区域 -->
    <view class="background-section">
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
    
    <!-- 下半屏：日记列表区域 -->
    <view class="diary-section">
      <scroll-view class="diary-scroll" scroll-y>
        <view class="diary-list">
          <!-- 日记条目 -->
          <view class="diary-item">
            <view class="diary-header">
              <text class="diary-date">2025.8.15</text>
              <text class="diary-time">15:30</text>
            </view>
            <view class="diary-content">
              <text class="content-text">今天去看了小猪佩奇。</text>
            </view>
            <view class="diary-footer">
              <view class="mood-tag">
                <text>😊</text>
              </view>
              <view class="action-buttons">
                <text class="action-btn">❤️ 0</text>
                <text class="action-btn">💬 0</text>
              </view>
            </view>
          </view>
          
          <!-- 可以添加更多日记条目 -->
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      diaryList: [
        {
          id: 1,
          date: '2025.8.15',
          time: '15:30',
          content: '今天去看了小猪佩奇。',
          mood: '😊',
          likes: 0,
          comments: 0
        }
      ]
    }
  },
  
  methods: {
    createNewDiary() {
      uni.showToast({
        title: '创建新日记功能开发中',
        icon: 'none'
      });
    }
  }
}
</script>

<style scoped>
.diary-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 上半屏：背景图片选择区域 */
.background-section {
  height: 40vh;
  position: relative;
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
  text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.3);
}

.new-diary-btn {
  position: absolute;
  bottom: 30rpx;
  right: 30rpx;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20rpx 30rpx;
  border-radius: 50rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.15);
}

.btn-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

/* 下半屏：日记列表区域 */
.diary-section {
  flex: 1;
  background-color: #f5f5f5;
  border-top-left-radius: 40rpx;
  border-top-right-radius: 40rpx;
  margin-top: -20rpx;
  z-index: 10;
  padding: 30rpx;
}

.diary-scroll {
  height: 100%;
}

.diary-list {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.diary-item {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
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

.diary-content {
  margin-bottom: 20rpx;
}

.content-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.6;
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
</style>