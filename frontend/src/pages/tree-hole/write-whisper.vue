<template>
  <view class="write-whisper-container">
    <view class="header">
      <view class="header-left" @click="cancel">
        <text class="cancel-btn">取消</text>
      </view>
      <view class="header-title">
        <text class="title">说悄悄话</text>
      </view>
      <view class="header-right" @click="publish">
        <text class="publish-btn" :class="{ disabled: !canPublish || isPublishing }">
          {{ isPublishing ? '发布中...' : '发布' }}
        </text>
      </view>
    </view>

    <view class="content">
      <textarea 
        class="whisper-content" 
        placeholder="向树洞倾诉你的心声..." 
        v-model="whisperContent"
        maxlength="500"
      />

      <view class="content-info">
        <text class="word-count">{{ whisperContent.length }}/500</text>
      </view>

      <view class="privacy-setting">
        <label class="privacy-label">
          <checkbox 
            :checked="isAnonymous" 
            @click="togglePrivacy" 
            color="#007aff"
          />
          <text>匿名发布</text>
        </label>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      whisperContent: '',
      isAnonymous: true,
      isPublishing: false
    }
  },

  computed: {
    canPublish() {
      return this.whisperContent.trim().length > 0;
    }
  },

  methods: {
    togglePrivacy() {
      this.isAnonymous = !this.isAnonymous;
    },

    cancel() {
      uni.navigateBack();
    },

    async publish() {
      if (!this.canPublish) {
        uni.showToast({
          title: '请输入悄悄话内容',
          icon: 'none'
        });
        return;
      }

      if (this.isPublishing) {
        return; // 防止重复点击
      }

      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      this.isPublishing = true;
      uni.showLoading({
        title: '发布中...'
      });

      try {
        // 创建悄悄话
        const whisperData = {
          content: this.whisperContent,
          is_anonymous: this.isAnonymous
        };

        const result = await api.createWhisper(token, whisperData);

        if (result.whisper_id) {
          uni.hideLoading();
          uni.showToast({
            title: '发布成功',
            icon: 'success'
          });

          // 2秒后跳转到我的悄悄话页面
          setTimeout(() => {
            uni.redirectTo({
              url: '/pages/tree-hole/my-whispers'
            });
          }, 2000);
        }
      } catch (error) {
        this.isPublishing = false;
        uni.hideLoading();
        console.error('发布失败:', error);
        uni.showToast({
          title: '发布失败: ' + (error.message || ''),
          icon: 'none'
        });
      }
    }
  }
}
</script>

<style scoped>
.write-whisper-container {
  height: 100vh;
  background-color: #f8f8f8;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 30rpx;
  background-color: white;
  border-bottom: 1rpx solid #eee;
}

.header-left,
.header-right {
  flex: 1;
}

.header-title {
  flex: 2;
  text-align: center;
}

.cancel-btn,
.publish-btn {
  font-size: 32rpx;
  color: #007aff;
}

.publish-btn.disabled {
  color: #ccc;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.content {
  padding: 30rpx;
}

.whisper-content {
  width: 100%;
  height: 400rpx;
  padding: 20rpx;
  background-color: white;
  border-radius: 20rpx;
  box-sizing: border-box;
  font-size: 30rpx;
  margin-bottom: 20rpx;
}

.content-info {
  text-align: right;
  margin-bottom: 30rpx;
}

.word-count {
  font-size: 24rpx;
  color: #999;
}

.privacy-setting {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
}

.privacy-label {
  display: flex;
  align-items: center;
  font-size: 30rpx;
  color: #333;
}

.privacy-label checkbox {
  margin-right: 20rpx;
}
</style>