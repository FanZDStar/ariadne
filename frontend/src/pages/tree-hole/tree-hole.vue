<template>
  <view class="tree-hole-container" :class="{ 'day-theme': theme === 'day', 'night-theme': theme === 'night' }">
    <view class="theme-switch" @click="toggleTheme">
      <text class="theme-icon">{{ theme === 'day' ? '🌙' : '☀️' }}</text>
    </view>

    <view class="tree-area">
      <image class="tree-image" :src="treeImage" mode="aspectFit" />
    </view>

    <view class="options-container">
      <view class="option-card" @click="goToWhisper">
        <text class="option-icon">💬</text>
        <text class="option-text">说悄悄话</text>
      </view>

      <view class="option-card" @click="goToListen">
        <text class="option-icon">👂</text>
        <text class="option-text">做倾听者</text>
      </view>

      <view class="option-card" @click="goToMyWhispers">
        <text class="option-icon">📝</text>
        <text class="option-text">我的悄悄话</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      theme: 'day', // 'day' or 'night'
    };
  },
  computed: {
    treeImage() {
      // 确保你的 static 目录下有 tree-day.png 和 tree-night.png
      if (this.theme === 'day') {
        return '/static/tree-day.png';
      } else {
        return '/static/tree-night.png';
      }
    },
  },
  onLoad() {
    this.setInitialTheme();
  },
  onShow() {
    // 每次页面显示时都更新导航栏样式，防止从其他页面返回时样式被重置
    this.updateNavBar();
  },
  methods: {
    setInitialTheme() {
      const hour = new Date().getHours();
      // 晚上6点到早上6点之间为夜晚
      if (hour >= 18 || hour < 6) {
        this.theme = 'night';
      } else {
        this.theme = 'day';
      }
    },
    toggleTheme() {
      this.theme = this.theme === 'day' ? 'night' : 'day';
      this.updateNavBar();
    },
    updateNavBar() {
      const isDay = this.theme === 'day';
      uni.setNavigationBarColor({
        frontColor: isDay ? '#000000' : '#ffffff', // 白天用黑色文字，晚上用白色
        backgroundColor: isDay ? '#87CEEB' : '#2c3e50',
      });
    },
    goToWhisper() {
      uni.navigateTo({
        url: '/pages/tree-hole/write-whisper',
      });
    },
    goToListen() {
      uni.navigateTo({
        url: '/pages/tree-hole/listen-whisper'
      });
    },
    goToMyWhispers() {
      uni.navigateTo({
        url: '/pages/tree-hole/my-whispers',
      });
    },
  },
};
</script>

<style scoped>
.tree-hole-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 40rpx;
  box-sizing: border-box;
  transition: background-color 0.5s;
}

.day-theme {
  background: linear-gradient(to bottom, #87ceeb, #e0f6ff);
}

.night-theme {
  background: linear-gradient(to bottom, #2c3e50, #34495e);
}

.theme-switch {
  position: fixed;
  top: 100rpx;
  /* 调整位置以避开导航栏 */
  right: 40rpx;
  z-index: 999;
  width: 80rpx;
  height: 80rpx;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.night-theme .theme-switch {
  background-color: rgba(0, 0, 0, 0.3);
}

.theme-icon {
  font-size: 48rpx;
}

.tree-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tree-image {
  width: 100%;
  height: 100%;
  max-width: 600rpx;
  max-height: 600rpx;
}

.options-container {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 0;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 20rpx;
  margin-top: 40rpx;
  transition: background-color 0.5s;
}

.night-theme .options-container {
  background-color: rgba(0, 0, 0, 0.3);
}

.option-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: background-color 0.5s;
  width: 180rpx;
}

.night-theme .option-card {
  background-color: rgba(44, 62, 80, 0.7);
}

.option-icon {
  font-size: 60rpx;
  margin-bottom: 20rpx;
}

.option-text {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
}

.night-theme .option-text {
  color: #ecf0f1;
}
</style>