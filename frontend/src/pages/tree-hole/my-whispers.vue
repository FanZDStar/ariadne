<template>
  <view class="my-whispers-container">
    <view class="tabs">
      <view :class="['tab', activeTab === 'posted' ? 'active' : '']" @click="activeTab = 'posted'">我发布的</view>
      <view :class="['tab', activeTab === 'chats' ? 'active' : '']" @click="activeTab = 'chats'">聊天</view>
    </view>
    <scroll-view scroll-y class="content">
      <view v-if="activeTab === 'posted'">
        <view v-for="whisper in myPostedWhispers" :key="whisper.whisper_id" class="whisper-item">
          <text>{{ whisper.content }}</text>
          <view>
            <text>❤️ {{ whisper.like_count }}</text>
            <text>💬 {{ whisper.comment_count }}</text>
          </view>
        </view>
      </view>
      <view v-if="activeTab === 'chats'">
        <view v-for="chat in myChats" :key="chat.whisper_id" class="whisper-item" @click="goToChat(chat.whisper_id)">
          <text>{{ chat.content }}</text>
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
      activeTab: 'posted',
      myPostedWhispers: [],
      myChats: []
    };
  },
  onLoad() {
    this.fetchMyPostedWhispers();
    this.fetchMyChats();
  },
  methods: {
    async fetchMyPostedWhispers() {
      const token = storage.getToken();
      this.myPostedWhispers = await api.getMyPostedWhispers(token);
    },
    async fetchMyChats() {
      const token = storage.getToken();
      this.myChats = await api.getMyChats(token);
    },
    goToChat(whisperId) {
      uni.navigateTo({
        url: `/pages/tree-hole/whisper-chat?whisper_id=${whisperId}`
      });
    }
  }
};
</script>

<style scoped>
.my-whispers-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 15px 0;
  cursor: pointer;
}

.tab.active {
  border-bottom: 2px solid blue;
}

.content {
  flex: 1;
  padding: 10px;
}

.whisper-item {
  background: #fff;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>