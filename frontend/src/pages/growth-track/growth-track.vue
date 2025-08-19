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

    <view class="chart-container">
      <view class="chart-header">
        <text class="chart-title">{{ getCurrentPeriodLabel() }}心情变化趋势</text>
      </view>

      <view class="chart-wrapper" v-if="chartData.length > 0">
        <view class="simple-chart">
          <view class="y-axis">
            <text class="y-label">5</text>
            <text class="y-label">4</text>
            <text class="y-label">3</text>
            <text class="y-label">2</text>
            <text class="y-label">1</text>
          </view>
          <view class="chart-content">
            <canvas class="chart-canvas" canvas-id="moodChart" id="moodChart" disable-scroll="true"></canvas>
            <view class="x-axis">
              <text class="x-label" v-for="(point, index) in getVisibleXLabels()" :key="index"
                :style="{ left: `${getPointX(point.index)}%` }">
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
      currentPeriod: '3days',
      periods: [
        { value: '3days', label: '近3天' },
        { value: '7days', label: '近7天' },
        { value: '30days', label: '近30天' },
        { value: '60days', label: '近60天' }
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

  onShow() {
    this.loadMoodData();
  },

  watch: {
    chartData(newVal) {
      if (newVal) {
        this.$nextTick(() => this.drawChart());
      }
    }
  },

  methods: {
    selectPeriod(period) {
      this.currentPeriod = period;
      this.loadMoodData();
    },

    async loadMoodData() {
      const token = storage.getToken();
      if (!token) return;

      try {
        const response = await api.getMoodStats(token, this.currentPeriod);
        this.chartData = response.data || [];
        this.calculateStats();
      } catch (error) {
        console.error('获取心情数据失败:', error);
      }
    },

    drawChart() {
      const query = uni.createSelectorQuery().in(this);
      query.select('#moodChart')
        .boundingClientRect(data => {
          if (!data || !this.chartData) return;

          const ctx = uni.createCanvasContext('moodChart', this);
          const width = data.width;
          const height = data.height;

          const paddingY = height * 0.1;
          const drawableHeight = height - (2 * paddingY);

          ctx.clearRect(0, 0, width, height);

          // 绘制网格线
          ctx.beginPath();
          ctx.setStrokeStyle('#eeeeee');
          ctx.setLineWidth(1);
          for (let i = 1; i <= 5; i++) {
            const y = (height - paddingY) - ((i - 1) / 4) * drawableHeight;
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
          }
          ctx.stroke();

          if (this.chartData.length === 0) {
            ctx.draw();
            return;
          }

          if (this.chartData.length === 1) {
            const point = {
              x: width / 2,
              y: (height - paddingY) - ((this.chartData[0].mood_score - 1) / 4) * drawableHeight
            };
            ctx.beginPath();
            ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
            ctx.setFillStyle('#007aff');
            ctx.fill();
            ctx.draw();
            return;
          }

          const points = this.chartData.map((point, index) => ({
            x: (index / (this.chartData.length - 1)) * width,
            y: (height - paddingY) - ((point.mood_score - 1) / 4) * drawableHeight
          }));

          // Catmull-Rom spline for a smooth curve
          ctx.beginPath();
          ctx.moveTo(points[0].x, points[0].y);
          for (let i = 0; i < points.length - 1; i++) {
            const p0 = i > 0 ? points[i - 1] : points[i];
            const p1 = points[i];
            const p2 = points[i + 1];
            const p3 = i < points.length - 2 ? points[i + 2] : p2;

            const tension = 0.5;
            for (let t = 0; t < 1; t += 0.05) {
              const t2 = t * t;
              const t3 = t2 * t;
              const a = 2 * t3 - 3 * t2 + 1;
              const b = t3 - 2 * t2 + t;
              const c = -2 * t3 + 3 * t2;
              const d = t3 - t2;

              const x = a * p1.x + b * (p2.x - p0.x) * tension + c * p2.x + d * (p3.x - p1.x) * tension;
              const y = a * p1.y + b * (p2.y - p0.y) * tension + c * p2.y + d * (p3.y - p1.y) * tension;
              ctx.lineTo(x, y);
            }
          }
          ctx.setStrokeStyle('#007aff');
          ctx.setLineWidth(2);
          ctx.stroke();

          // Draw data points
          points.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
            ctx.setFillStyle('#007aff');
            ctx.fill();
          });

          ctx.draw();
        }).exec();
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
      return ((score - 1) / 4) * 100;
    },

    getVisibleXLabels() {
      if (!this.chartData || this.chartData.length === 0) return [];

      const data = this.chartData;
      const len = data.length;

      if (len <= 7) {
        return data.map((item, index) => ({
          index,
          label: this.formatTimeLabel(item.time)
        }));
      }

      const maxLabels = 7;
      const labels = [];
      const step = Math.floor((len - 1) / (maxLabels - 1));

      for (let i = 0; i < maxLabels - 1; i++) {
        const index = i * step;
        labels.push({
          index,
          label: this.formatTimeLabel(data[index].time)
        });
      }
      if (labels.findIndex(l => l.index === len - 1) === -1) {
        labels.push({
          index: len - 1,
          label: this.formatTimeLabel(data[len - 1].time)
        });
      }

      return labels;
    },

    formatTimeLabel(time) {
      return time.substring(5); // "MM-DD"
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
  padding: 20rpx 0;
}

.chart-canvas {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.x-axis {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -20rpx;
  height: 40rpx;
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