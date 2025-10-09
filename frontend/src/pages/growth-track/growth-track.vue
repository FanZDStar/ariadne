<template>
  <view class="growth-track-container">
    <view class="header">
      <text class="title">见心录</text>
      <text class="subtitle">查看你的情感变化趋势</text>
    </view>

    <view class="period-selector">
      <scroll-view class="period-scroll" scroll-x>
        <view class="period-list">
          <view class="period-item" v-for="period in periods" :key="period.value"
            :class="{ active: currentPeriod === period.value }" @click="selectPeriod(period.value)">
            <text class="period-text">{{ period.label }}</text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 情感趋势图表组件 -->
    <EmotionalTrendChart :currentPeriod="currentPeriod" :periods="periods" :isLoggedIn="isLoggedIn" ref="trendChart" />

    <!-- 心情晴雨表组件 -->
    <view class="mood-tracker-section">
      <MoodTracker :isLoggedIn="isLoggedIn" ref="moodTracker" @mood-saved="handleMoodSaved" />
    </view>

    <!-- 心理测评栏目 -->
    <view class="psychological-assessment-section">
      <view class="assessment-card" @click="goToPsychologicalAssessment">
        <view class="assessment-header">
          <text class="assessment-icon">🧠</text>
          <text class="assessment-title">心理测评</text>
        </view>
        <text class="assessment-desc">多维度了解自己的心理状态</text>
        <view class="assessment-arrow">
          <text class="arrow-text">→</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { storage } from "../../utils/api.js";
import MoodTracker from "../../components/MoodTracker.vue";
import EmotionalTrendChart from "../../components/EmotionalTrendChart.vue";

export default {
  components: {
    MoodTracker,
    EmotionalTrendChart,
  },

  data() {
    return {
      currentPeriod: "7days",
      periods: [
        { value: "3days", label: "近3天" },
        { value: "7days", label: "近7天" },
        { value: "30days", label: "近30天" },
        { value: "60days", label: "近60天" },
      ],
      isLoggedIn: false,
    };
  },

  onLoad() {
    this.checkLoginStatus();
  },

  onShow() {
    this.checkLoginStatus();
  },

  methods: {
    selectPeriod(period) {
      this.currentPeriod = period;
      // 通知图表组件重新加载数据
      if (this.$refs.trendChart) {
        this.$refs.trendChart.loadAllData();
      }
    },

    checkLoginStatus() {
      const token = storage.getToken();
      this.isLoggedIn = !!token;
    },

    goToPsychologicalAssessment() {
      uni.navigateTo({
        url: "/pages/psychological-assessment/assessment-list",
      });
    },

    handleMoodSaved(eventData) {
// 心情保存成功后的处理
      console.log('心情保存成功:', eventData);
      
      // 如果获得了星星奖励，可以在这里做额外处理
      if (eventData.star_awarded) {
        console.log(`获得了 ${eventData.star_points} 个星星!`);
        // 可以触发一些动画效果或其他奖励展示
      }
    },
  },
};
</script>

<style scoped>
.growth-track-container {
  padding: 40rpx;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.header {
  margin-bottom: 40rpx;
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

.period-selector {
  background-color: white;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.period-scroll {
  width: 100%;
  white-space: nowrap;
}

.period-list {
  display: inline-flex;
  padding: 10rpx 0;
}

.period-item {
  padding: 20rpx 30rpx;
  margin-right: 20rpx;
  background-color: #f5f5f5;
  border-radius: 50rpx;
}

.period-item.active {
  background-color: #007aff;
}

.period-text {
  font-size: 28rpx;
  color: #333;
  /* 修改处：确保文字不换行 */
  white-space: nowrap;
}

.period-item.active .period-text {
  color: white;
}

/* 心情晴雨表区域样式 */
.mood-tracker-section {
  margin-bottom: 40rpx;
}

/* 心理测评栏目样式 */
.psychological-assessment-section {
  margin-bottom: 40rpx;
}

.assessment-card {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 20rpx;
  padding: 40rpx;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10rpx 30rpx rgba(102, 126, 234, 0.3);
}

.assessment-card:active {
  transform: translateY(2rpx);
  box-shadow: 0 8rpx 25rpx rgba(102, 126, 234, 0.4);
}

.assessment-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.assessment-icon {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.assessment-title {
  font-size: 36rpx;
  font-weight: bold;
  color: white;
}

.assessment-desc {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20rpx;
}

.assessment-arrow {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
}

.arrow-text {
  font-size: 32rpx;
  color: white;
  font-weight: bold;
}
</style>
