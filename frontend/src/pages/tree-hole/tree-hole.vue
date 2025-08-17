<template>
  <view class="tree-hole-container">
    <view class="tree-area">
      <view class="tree">
        <!-- 树冠 -->
        <view class="tree-top">
          <view class="leaf-layer layer1"></view>
          <view class="leaf-layer layer2"></view>
          <view class="leaf-layer layer3"></view>
        </view>
        
        <!-- 树干 -->
        <view class="tree-trunk">
          <!-- 树洞 -->
          <view class="tree-hole">
            <text class="hole-text">心灵树洞</text>
          </view>
        </view>
      </view>
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
  methods: {
    goToWhisper() {
      uni.navigateTo({
        url: '/pages/tree-hole/write-whisper'
      });
    },
    
    goToListen() {
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      });
    },
    
    goToMyWhispers() {
      uni.navigateTo({
        url: '/pages/tree-hole/my-whispers'
      });
    }
  }
}
</script>

<style scoped>
.tree-hole-container {
  height: 100vh;
  background: linear-gradient(to bottom, #87CEEB, #E0F6FF);
  display: flex;
  flex-direction: column;
  padding: 40rpx;
  box-sizing: border-box;
}

.tree-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tree {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 树冠 */
.tree-top {
  position: relative;
  margin-bottom: -40rpx;
  z-index: 2;
}

.leaf-layer {
  width: 200rpx;
  height: 120rpx;
  background: linear-gradient(to bottom, #228B22, #006400);
  border-radius: 50%;
  margin-bottom: -30rpx;
  position: relative;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
}

.layer2 {
  width: 240rpx;
  margin-top: -20rpx;
}

.layer3 {
  width: 280rpx;
  margin-top: -20rpx;
}

/* 树干 */
.tree-trunk {
  width: 60rpx;
  height: 200rpx;
  background: #8B4513;
  border-radius: 10rpx;
  position: relative;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.2);
}

/* 树洞 */
.tree-hole {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40rpx;
  height: 60rpx;
  background: #5D4037;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 10rpx rgba(0, 0, 0, 0.5);
}

.hole-text {
  font-size: 16rpx;
  color: #D7CCC8;
  transform: rotate(90deg);
  white-space: nowrap;
}

/* 选项区域 */
.options-container {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 0;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 20rpx;
  margin-top: 40rpx;
}

.option-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30rpx;
  background-color: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
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
</style>