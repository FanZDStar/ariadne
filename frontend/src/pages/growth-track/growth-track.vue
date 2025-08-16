
<template>
  <view class="growth-track-container">
    <view class="header">
      <text class="title">成长轨迹</text>
      <text class="subtitle">查看你的情感变化趋势</text>
    </view>
    
    <!-- 时间段选择 -->
    <view class="period-selector">
      <scroll-view class="period-scroll" scroll-x>
        <view class="period-list">
          <view 
            class="period-item" 
            v-for="period in periods" 
            :key="period.value"
            :class="{ active: currentPeriod === period.value }"
            @click="selectPeriod(period.value)"
          >
            <text class="period-text">{{ period.label }}</text>
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 图表区域 -->
    <view class="chart-container">
      <view class="chart-header">
        <text class="chart-title">{{ getCurrentPeriodLabel() }}心情变化趋势</text>
      </view>
      
      <view class="chart-wrapper" v-if="chartData.length > 0">
        <!-- 简单的折线图实现 -->
        <view class="simple-chart">
          <view class="y-axis">
            <text class="y-label">5</text>
            <text class="y-label">4</text>
            <text class="y-label">3</text>
            <text class="y-label">2</text>
            <text class="y-label">1</text>
          </view>
          <view class="chart-content">
            <view class="chart-grid">
              <!-- 网格线 -->
              <view class="grid-line" v-for="i in 5" :key="i"></view>
            </view>
            <!-- 折线 -->
            <canvas 
              class="chart-canvas" 
              canvas-id="moodChart"
              id="moodChart"
              disable-scroll="true"
            ></canvas>
            <!-- 数据点 -->
            <view class="data-points">
              <view 
                class="data-point" 
                v-for="(point, index) in chartData" 
                :key="index"
                :style="{
                  left: `${getPointX(index)}%`,
                  bottom: `${getPointY(point.mood_score)}%`
                }"
              >
                <view class="point-dot"></view>
                <text class="point-value">{{ point.mood_score }}</text>
              </view>
            </view>
            <!-- X轴标签 -->
            <view class="x-axis">
              <text 
                class="x-label" 
                v-for="(point, index) in getVisibleXLabels()" 
                :key="index"
                :style="{ left: `${getPointX(point.index)}%` }"
              >
                {{ point.label }}
              </text>
            </view>
          </view>
        </view>
      </view>
      
      <view class="empty-chart" v-else>
        <text class="empty-text">暂无数据</text>
      </view>
    </view>
    
    <!-- 统计信息 -->
    <view class="stats-container">
      <view class="stats-card">
        <text class="stats-title">统计信息</text>
        <view class="stats-content">
          <view class="stats-item">
            <text class="stats-label">平均心情值</text>
            <text class="stats-value">{{ averageMood }}</text>
          </view>
          <view class="stats-item">
            <text class="stats-label">最高心情值</text>
            <text class="stats-value">{{ maxMood }}</text>
          </view>
          <view class="stats-item">
            <text class="stats-label">最低心情值</text>
            <text class="stats-value">{{ minMood }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      currentPeriod: '30days',
      periods: [
        { value: 'today', label: '今天' },
        { value: '7days', label: '近7天' },
        { value: '30days', label: '近30天' },
        { value: '60days', label: '近60天' },
        { value: '365days', label: '近365天' }
      ],
      chartData: [],
      averageMood: '0.00',
      maxMood: '0.00',
      minMood: '0.00'
    }
  },
  
  onLoad() {
    this.loadMoodData();
  },
  
  methods: {
    selectPeriod(period) {
      this.currentPeriod = period;
      this.loadMoodData();
    },
    
    async loadMoodData() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }
      
      try {
        const response = await api.getMoodStats(token, this.currentPeriod);
        this.chartData = response.data || [];
        this.calculateStats();
      } catch (error) {
        console.error('获取心情数据失败:', error);
        uni.showToast({
          title: '获取数据失败',
          icon: 'none'
        });
      }
    },
    
    calculateStats() {
      if (this.chartData.length === 0) {
        this.averageMood = '0.00';
        this.maxMood = '0.00';
        this.minMood = '0.00';
        return;
      }
      
      const moodScores = this.chartData.map(item => item.mood_score);
      const sum = moodScores.reduce((a, b) => a + b, 0);
      this.averageMood = (sum / moodScores.length).toFixed(2);
      this.maxMood = Math.max(...moodScores).toFixed(2);
      this.minMood = Math.min(...moodScores).toFixed(2);
    },
    
    getCurrentPeriodLabel() {
      const period = this.periods.find(p => p.value === this.currentPeriod);
      return period ? period.label : '';
    },
    
    getPointX(index) {
      if (this.chartData.length <= 1) return 50;
      return (index / (this.chartData.length - 1)) * 100;
    },
    
    getPointY(score) {
      // 将1-5分映射到0-100%
      return ((score - 1) / 4) * 100;
    },
    
    getVisibleXLabels() {
      if (this.chartData.length === 0) return [];
      
      const maxLabels = 5; // 最多显示5个标签
      if (this.chartData.length <= maxLabels) {
        return this.chartData.map((item, index) => ({
          index,
          label: this.formatTimeLabel(item.time)
        }));
      }
      
      // 如果数据点太多，只显示部分标签
      const step = Math.ceil(this.chartData.length / maxLabels);
      const labels = [];
      for (let i = 0; i < this.chartData.length; i += step) {
        labels.push({
          index: i,
          label: this.formatTimeLabel(this.chartData[i].time)
        });
      }
      return labels;
    },
    
    formatTimeLabel(time) {
      if (this.currentPeriod === 'today') {
        return time; // 显示小时，如 "14:00"
      } else {
        // 显示日期，如 "08-15"
        const date = new Date(time);
        return `${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
      }
    }
  }
}
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

/* 时间段选择器 */
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
  white-space: nowrap;
}

.period-item.active {
  background-color: #007aff;
}

.period-text {
  font-size: 28rpx;
  color: #333;
}

.period-item.active .period-text {
  color: white;
}

/* 图表区域 */
.chart-container {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.chart-header {
  margin-bottom: 30rpx;
}

.chart-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

/* 简单图表实现 */
.simple-chart {
  display: flex;
  height: 400rpx;
  position: relative;
}

.y-axis {
  width: 80rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20rpx 0;
}

.y-label {
  font-size: 24rpx;
  color: #999;
  text-align: center;
}

.chart-content {
  flex: 1;
  position: relative;
  padding: 20rpx;
}

.chart-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 40rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.grid-line {
  height: 1rpx;
  background-color: #eee;
}

.chart-canvas {
  position: absolute;
  top: 20rpx;
  left: 20rpx;
  right: 20rpx;
  bottom: 60rpx;
}

.data-points {
  position: absolute;
  top: 20rpx;
  left: 20rpx;
  right: 20rpx;
  bottom: 60rpx;
  pointer-events: none;
}

.data-point {
  position: absolute;
  transform: translate(-50%, 50%);
}

.point-dot {
  width: 20rpx;
  height: 20rpx;
  background-color: #007aff;
  border-radius: 50%;
  margin-left: -10rpx;
  margin-bottom: -10rpx;
}

.point-value {
  font-size: 20rpx;
  color: #007aff;
  position: absolute;
  top: -30rpx;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
}

.x-axis {
  position: absolute;
  left: 20rpx;
  right: 20rpx;
  bottom: 0;
  height: 40rpx;
  display: flex;
  justify-content: space-between;
}

.x-label {
  font-size: 24rpx;
  color: #999;
  position: absolute;
  transform: translateX(-50%);
  white-space: nowrap;
}

.empty-chart {
  height: 400rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-text {
  font-size: 32rpx;
  color: #999;
}

/* 统计信息 */
.stats-container {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.stats-card {
  width: 100%;
}

.stats-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 30rpx;
}

.stats-content {
  display: flex;
  justify-content: space-between;
}

.stats-item {
  text-align: center;
  flex: 1;
}

.stats-label {
  font-size: 28rpx;
  color: #999;
  display: block;
  margin-bottom: 10rpx;
}

.stats-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #007aff;
}
</style>