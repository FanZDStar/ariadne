<template>
  <view class="my-whispers-container">
    <view class="header">
      <text class="title">我的悄悄话</text>
      <text class="subtitle">你向树洞倾诉的所有心声</text>
    </view>

    <view class="tabs">
      <view :class="['tab-item', { active: activeTab === 'posted' }]" @click="activeTab = 'posted'">
        我发布的
      </view>
      <view :class="['tab-item', { active: activeTab === 'chats' }]" @click="activeTab = 'chats'">
        聊天
      </view>
    </view>

    <scroll-view class="content-scroll-view" scroll-y>
      <view v-if="activeTab === 'posted'" class="whisper-list">
        <view v-if="myPostedWhispers.length === 0" class="empty-state">
          <text class="empty-text">你还没有发布过悄悄话...</text>
        </view>
        <view class="whisper-item" v-for="whisper in myPostedWhispers" :key="whisper.whisper_id">
          <view class="whisper-timestamp">{{ formatTimestamp(whisper.created_at) }}</view>
          <view class="whisper-content">{{ whisper.content }}</view>
          <view class="whisper-stats">
            <text class="stat-item">❤️ {{ whisper.like_count || 0 }}</text>
            <text class="stat-item">💬 {{ whisper.comment_count || 0 }}</text>
          </view>
        </view>
      </view>

      <view v-if="activeTab === 'chats'" class="whisper-list">
        <view v-if="myChats.length === 0" class="empty-state">
          <text class="empty-text">你还没有参与过任何聊天...</text>
        </view>
        <view class="whisper-item" v-for="chat in myChats" :key="chat.whisper_id" @click="goToChat(chat.whisper_id)">
          <view class="whisper-timestamp">{{ formatTimestamp(chat.created_at) }}</view>
          <view class="whisper-content">{{ chat.content }}</view>
          <view class="whisper-stats">
            <text class="stat-item">❤️ {{ chat.like_count || 0 }}</text>
            <text class="stat-item">💬 {{ chat.comment_count || 0 }}</text>
          </view>
        </view>
      </view>
    </scroll-view>

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
      activeTab: 'posted',
      myPostedWhispers: [],
      myChats: []
    };
  },
  onLoad() {
    this.loadData();
  },
  onPullDownRefresh() {
    this.loadData().then(() => uni.stopPullDownRefresh());
  },
  methods: {
    async loadData() {
      await this.fetchMyPostedWhispers();
      await this.fetchMyChats();
    },
    async fetchMyPostedWhispers() {
      const token = storage.getToken();
      if (!token) return;
      try {
        this.myPostedWhispers = await api.getMyPostedWhispers(token);
      } catch (error) {
        console.error('Failed to fetch posted whispers:', error);
      }
    },
    async fetchMyChats() {
      const token = storage.getToken();
      if (!token) return;
      try {
        this.myChats = await api.getMyChats(token);
      } catch (error) {
        console.error('Failed to fetch chats:', error);
      }
    },
    goToChat(whisperId) {
      uni.navigateTo({
        url: `/pages/tree-hole/whisper-chat?whisper_id=${whisperId}`
      });
    },
    goToWriteWhisper() {
      uni.navigateTo({
        url: '/pages/tree-hole/write-whisper'
      });
    },
    formatTimestamp(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${year}.${month}.${day} ${hours}:${minutes}`;
    }
  }
};
</script>

<style scoped>
.my-whispers-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9fa;
}

.header {
  padding: 40rpx;
  background-color: white;
  text-align: center;
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

.tabs {
  display: flex;
  background-color: white;
  border-bottom: 1rpx solid #eee;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 25rpx 0;
  font-size: 30rpx;
  color: #666;
  position: relative;
  cursor: pointer;
  transition: color 0.3s;
}

.tab-item.active {
  color: #007aff;
  font-weight: bold;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 6rpx;
  background-color: #007aff;
  border-radius: 3rpx;
}

.content-scroll-view {
  flex: 1;
  height: 100%;
}

.whisper-list {
  padding: 30rpx;
}

.whisper-item {
  background: #fff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.whisper-timestamp {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.whisper-content {
  font-size: 30rpx;
  color: #555;
  line-height: 1.6;
  margin-bottom: 25rpx;
  /* For text truncation */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.whisper-stats {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 26rpx;
  color: #999;
}

.stat-item {
  margin-left: 30rpx;
}

.empty-state {
  text-align: center;
  padding-top: 200rpx;
  color: #aaa;
}

.empty-text {
  font-size: 28rpx;
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