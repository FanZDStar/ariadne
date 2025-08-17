<template>
  <view class="my-whispers-container">
    <view class="header">
      <text class="title">我的悄悄话</text>
      <text class="subtitle">你向树洞倾诉的所有心声</text>
    </view>

    <view class="content">
      <scroll-view class="whispers-scroll" scroll-y>
        <view class="whispers-list">
          <!-- 悄悄话条目 -->
          <view 
            class="whisper-item" 
            v-for="whisper in whisperList" 
            :key="whisper.whisper_id"
            @click="viewWhisperDetail(whisper)"
          >
            <view class="whisper-header">
              <text class="whisper-date">{{ formatWhisperDate(whisper.created_at) }}</text>
              <text class="whisper-time">{{ formatWhisperTime(whisper.created_at) }}</text>
            </view>
            <view class="whisper-content">
              <text class="content-text">{{ getPreviewContent(whisper.content) }}</text>
            </view>
            <view class="whisper-footer">
              <view class="privacy-tag">
                <text>{{ whisper.is_anonymous ? '匿名' : '实名' }}</text>
              </view>
              <view class="action-buttons">
                <text class="action-btn">❤️ {{ whisper.like_count || 0 }}</text>
                <text class="action-btn">💬 {{ whisper.comment_count || 0 }}</text>
              </view>
            </view>
          </view>

          <!-- 没有悄悄话时的提示 -->
          <view v-if="whisperList.length === 0" class="empty-whisper">
            <text class="empty-text">还没有向树洞说过悄悄话，点击下方按钮开始倾诉吧！</text>
          </view>
        </view>
      </scroll-view>
    </view>
    
    <view class="fab" @click="goToWriteWhisper">
      <text class="fab-icon">+</text>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      whisperList: []
    }
  },

  onLoad() {
    this.loadWhispers();
  },

  onPullDownRefresh() {
    this.loadWhispers();
  },

  methods: {
    async loadWhispers() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      try {
        const whispers = await api.getUserWhispers(token);
        this.whisperList = whispers;
        uni.stopPullDownRefresh();
      } catch (error) {
        console.error('获取悄悄话失败:', error);
        uni.showToast({
          title: '获取悄悄话失败',
          icon: 'none'
        });
        uni.stopPullDownRefresh();
      }
    },

    goToWriteWhisper() {
      uni.navigateTo({
        url: '/pages/tree-hole/write-whisper'
      });
    },

    viewWhisperDetail(whisper) {
      // 跳转到悄悄话详情页（待实现）
      uni.showToast({
        title: '详情页开发中',
        icon: 'none'
      });
    },

    formatWhisperDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
    },

    formatWhisperTime(dateString) {
      const date = new Date(dateString);
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    },

    getPreviewContent(content) {
      if (content.length > 50) {
        return content.substring(0, 50) + '...';
      }
      return content;
    }
  }
}
</script>

<style scoped>
.my-whispers-container {
  height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 40rpx;
  background-color: white;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 42rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #999;
}

.content {
  flex: 1;
  padding: 30rpx;
  overflow: hidden;
}

.whispers-scroll {
  height: 100%;
}

.whispers-list {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.whisper-item {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.whisper-item:active {
  background-color: #f9f9f9;
}

.whisper-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.whisper-date {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.whisper-time {
  font-size: 24rpx;
  color: #999;
}

.whisper-content {
  margin-bottom: 20rpx;
}

.content-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.6;
}

.whisper-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.privacy-tag {
  font-size: 24rpx;
  color: #007aff;
  background-color: #e3f2fd;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
}

.action-buttons {
  display: flex;
  gap: 30rpx;
}

.action-btn {
  font-size: 24rpx;
  color: #999;
}

.empty-whisper {
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

.fab {
  position: fixed;
  bottom: 50rpx;
  right: 50rpx;
  width: 100rpx;
  height: 100rpx;
  background-color: #007aff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
  z-index: 100;
}

.fab-icon {
  font-size: 60rpx;
  color: white;
  font-weight: bold;
}
</style>