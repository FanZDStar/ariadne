<template>
  <view class="breathing-container">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="nav-bar">
        <view class="nav-left" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">深呼吸练习</text>
        <view class="nav-right"></view>
      </view>
    </view>

    <!-- 练习状态 -->
    <view class="practice-status">
      <text class="status-text">{{ statusText }}</text>
      <text class="phase-text">{{ phaseText }}</text>
    </view>

    <!-- 呼吸动画圆圈 -->
    <view class="breathing-circle-wrapper">
      <view
        class="breathing-circle"
        :class="{
          inhale: currentPhase === 'inhale',
          hold: currentPhase === 'hold',
          exhale: currentPhase === 'exhale',
        }"
      >
        <view class="circle-inner">
          <text class="breathing-text">{{ breathingText }}</text>
          <text class="countdown">{{ countdown }}</text>
        </view>
      </view>

      <!-- 呼吸指导圈 -->
      <view class="guide-ring"></view>
    </view>

    <!-- 练习控制 -->
    <view class="practice-controls">
      <view v-if="!isActive" class="start-section">
        <view class="exercise-info">
          <text class="info-title">准备开始</text>
          <text class="info-desc">找一个安静的地方，保持舒适的姿势</text>
        </view>
        <view class="start-btn" @click="startPractice">
          <text class="btn-text">开始练习</text>
        </view>
      </view>

      <view v-else class="active-controls">
        <view class="control-buttons">
          <view class="control-btn pause" @click="pausePractice">
            <text class="btn-icon">{{ isPaused ? "▶️" : "⏸️" }}</text>
            <text class="btn-label">{{ isPaused ? "继续" : "暂停" }}</text>
          </view>
          <view class="control-btn stop" @click="stopPractice">
            <text class="btn-icon">⏹️</text>
            <text class="btn-label">停止</text>
          </view>
        </view>

        <view class="practice-progress">
          <text class="progress-text"
            >第 {{ completedCycles + 1 }} / {{ totalCycles }} 轮</text
          >
          <view class="progress-bar">
            <view
              class="progress-fill"
              :style="{ width: progressPercent + '%' }"
            ></view>
          </view>
        </view>
      </view>
    </view>

    <!-- 练习设置 -->
    <view class="practice-settings">
      <text class="settings-title">练习设置</text>

      <view class="setting-item">
        <text class="setting-label">练习轮数</text>
        <view class="setting-options">
          <view
            v-for="option in cycleOptions"
            :key="option"
            class="option-btn"
            :class="{ active: totalCycles === option }"
            @click="setTotalCycles(option)"
          >
            <text class="option-text">{{ option }}</text>
          </view>
        </view>
      </view>

      <view class="setting-item">
        <text class="setting-label">呼吸节奏</text>
        <view class="rhythm-options">
          <view
            v-for="rhythm in rhythmOptions"
            :key="rhythm.name"
            class="rhythm-btn"
            :class="{ active: currentRhythm.name === rhythm.name }"
            @click="setRhythm(rhythm)"
          >
            <text class="rhythm-name">{{ rhythm.name }}</text>
            <text class="rhythm-pattern">{{ rhythm.pattern }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 练习完成 -->
    <view v-if="isCompleted" class="completion-modal">
      <view class="modal-content">
        <text class="completion-icon">✨</text>
        <text class="completion-title">练习完成！</text>
        <text class="completion-desc"
          >您已完成 {{ totalCycles }} 轮深呼吸练习</text
        >
        <view class="completion-stats">
          <view class="stat-item">
            <text class="stat-value">{{ totalTime }}</text>
            <text class="stat-label">练习时长</text>
          </view>
          <view class="stat-item">
            <text class="stat-value">{{ totalCycles }}</text>
            <text class="stat-label">完成轮数</text>
          </view>
        </view>
        <view class="completion-actions">
          <view class="action-btn secondary" @click="restartPractice">
            <text class="btn-text">再练一次</text>
          </view>
          <view class="action-btn primary" @click="finishPractice">
            <text class="btn-text">完成</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 练习状态
      isActive: false,
      isPaused: false,
      isCompleted: false,

      // 呼吸阶段
      currentPhase: "prepare", // prepare, inhale, hold, exhale
      countdown: 0,

      // 练习进度
      completedCycles: 0,
      totalCycles: 5,

      // 计时器
      timer: null,
      startTime: null,
      totalTime: "",

      // 呼吸节奏设置
      currentRhythm: {
        name: "标准节奏",
        pattern: "4-4-8",
        inhale: 4,
        hold: 4,
        exhale: 8,
      },

      // 设置选项
      cycleOptions: [3, 5, 8, 10],
      rhythmOptions: [
        {
          name: "初学者",
          pattern: "3-3-6",
          inhale: 3,
          hold: 3,
          exhale: 6,
        },
        {
          name: "标准节奏",
          pattern: "4-4-8",
          inhale: 4,
          hold: 4,
          exhale: 8,
        },
        {
          name: "深度放松",
          pattern: "6-6-12",
          inhale: 6,
          hold: 6,
          exhale: 12,
        },
      ],
    };
  },

  computed: {
    statusText() {
      if (!this.isActive) return "准备开始练习";
      if (this.isPaused) return "练习已暂停";
      return "正在练习中...";
    },

    phaseText() {
      const phaseMap = {
        prepare: "准备开始",
        inhale: "缓慢吸气",
        hold: "屏住呼吸",
        exhale: "慢慢呼气",
      };
      return phaseMap[this.currentPhase] || "";
    },

    breathingText() {
      const textMap = {
        prepare: "准备",
        inhale: "吸气",
        hold: "屏气",
        exhale: "呼气",
      };
      return textMap[this.currentPhase] || "";
    },

    progressPercent() {
      if (this.totalCycles === 0) return 0;
      return Math.round((this.completedCycles / this.totalCycles) * 100);
    },
  },

  onLoad() {
    this.initializePractice();
  },

  onUnload() {
    this.clearTimer();
  },

  methods: {
    initializePractice() {
      this.currentPhase = "prepare";
      this.countdown = 0;
      this.completedCycles = 0;
      this.isCompleted = false;
    },

    startPractice() {
      this.isActive = true;
      this.isPaused = false;
      this.startTime = Date.now();
      this.startBreathingCycle();
    },

    pausePractice() {
      this.isPaused = !this.isPaused;

      if (this.isPaused) {
        this.clearTimer();
      } else {
        this.startBreathingCycle();
      }
    },

    stopPractice() {
      uni.showModal({
        title: "确认停止",
        content: "确定要停止当前练习吗？",
        success: (res) => {
          if (res.confirm) {
            this.resetPractice();
          }
        },
      });
    },

    resetPractice() {
      this.isActive = false;
      this.isPaused = false;
      this.clearTimer();
      this.initializePractice();
    },

    startBreathingCycle() {
      if (this.isPaused || !this.isActive) return;

      this.startInhale();
    },

    startInhale() {
      this.currentPhase = "inhale";
      this.countdown = this.currentRhythm.inhale;

      this.timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(this.timer);
          this.startHold();
        }
      }, 1000);
    },

    startHold() {
      this.currentPhase = "hold";
      this.countdown = this.currentRhythm.hold;

      this.timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(this.timer);
          this.startExhale();
        }
      }, 1000);
    },

    startExhale() {
      this.currentPhase = "exhale";
      this.countdown = this.currentRhythm.exhale;

      this.timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(this.timer);
          this.completeCycle();
        }
      }, 1000);
    },

    completeCycle() {
      this.completedCycles++;

      if (this.completedCycles >= this.totalCycles) {
        this.completePractice();
      } else {
        // 短暂休息后继续下一轮
        setTimeout(() => {
          if (this.isActive && !this.isPaused) {
            this.startBreathingCycle();
          }
        }, 1000);
      }
    },

    completePractice() {
      this.isActive = false;
      this.isCompleted = true;
      this.calculateTotalTime();
      this.clearTimer();
    },

    calculateTotalTime() {
      if (this.startTime) {
        const duration = Math.round((Date.now() - this.startTime) / 1000);
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        this.totalTime = `${minutes}分${seconds}秒`;
      }
    },

    setTotalCycles(cycles) {
      if (!this.isActive) {
        this.totalCycles = cycles;
      }
    },

    setRhythm(rhythm) {
      if (!this.isActive) {
        this.currentRhythm = rhythm;
      }
    },

    restartPractice() {
      this.isCompleted = false;
      this.resetPractice();
      this.startPractice();
    },

    finishPractice() {
      this.isCompleted = false;
      this.resetPractice();

      // 可以在这里记录练习数据
      uni.showToast({
        title: "练习记录已保存",
        icon: "success",
      });
    },

    clearTimer() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },

    goBack() {
      if (this.isActive) {
        uni.showModal({
          title: "确认离开",
          content: "练习正在进行中，确定要离开吗？",
          success: (res) => {
            if (res.confirm) {
              this.clearTimer();
              uni.navigateBack();
            }
          },
        });
      } else {
        uni.navigateBack();
      }
    },
  },
};
</script>

<style scoped>
.breathing-container {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: white;
}

/* 顶部导航 */
.header {
  padding-top: env(safe-area-inset-top);
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 40rpx;
  height: 88rpx;
}

.nav-left,
.nav-right {
  width: 80rpx;
  display: flex;
  justify-content: center;
}

.back-icon {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
}

.nav-title {
  font-size: 36rpx;
  font-weight: bold;
  color: white;
  text-align: center;
  flex: 1;
}

/* 练习状态 */
.practice-status {
  text-align: center;
  padding: 40rpx 40rpx 20rpx;
}

.status-text {
  font-size: 24rpx;
  opacity: 0.8;
  margin-bottom: 8rpx;
  display: block;
}

.phase-text {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
}

/* 呼吸动画圆圈 */
.breathing-circle-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;
  position: relative;
}

.breathing-circle {
  width: 400rpx;
  height: 400rpx;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 3s ease-in-out;
}

.breathing-circle.inhale {
  transform: scale(1.2);
  background: radial-gradient(
    circle,
    rgba(102, 126, 234, 0.5) 0%,
    rgba(118, 75, 162, 0.3) 100%
  );
}

.breathing-circle.hold {
  transform: scale(1.2);
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.2) 100%
  );
}

.breathing-circle.exhale {
  transform: scale(0.8);
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
}

.circle-inner {
  text-align: center;
}

.breathing-text {
  font-size: 48rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
}

.countdown {
  font-size: 80rpx;
  font-weight: bold;
  color: white;
}

.guide-ring {
  position: absolute;
  width: 440rpx;
  height: 440rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  pointer-events: none;
}

/* 练习控制 */
.practice-controls {
  padding: 0 40rpx 40rpx;
}

.start-section {
  text-align: center;
}

.exercise-info {
  margin-bottom: 40rpx;
}

.info-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 12rpx;
  display: block;
}

.info-desc {
  font-size: 26rpx;
  opacity: 0.8;
}

.start-btn {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 32rpx 80rpx;
  border-radius: 60rpx;
  margin: 0 auto;
  display: inline-block;
  transition: all 0.3s ease;
}

.start-btn:active {
  transform: scale(0.95);
  background-color: rgba(255, 255, 255, 0.3);
}

.btn-text {
  font-size: 32rpx;
  font-weight: bold;
  color: white;
}

.active-controls {
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 40rpx;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  padding: 24rpx;
  border-radius: 16rpx;
  background-color: rgba(255, 255, 255, 0.2);
  min-width: 120rpx;
  transition: all 0.3s ease;
}

.control-btn:active {
  transform: scale(0.95);
  background-color: rgba(255, 255, 255, 0.3);
}

.btn-icon {
  font-size: 32rpx;
}

.btn-label {
  font-size: 24rpx;
}

.practice-progress {
  text-align: center;
}

.progress-text {
  font-size: 24rpx;
  margin-bottom: 16rpx;
  display: block;
  opacity: 0.8;
}

.progress-bar {
  width: 100%;
  height: 8rpx;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: white;
  border-radius: 4rpx;
  transition: width 0.3s ease;
}

/* 练习设置 */
.practice-settings {
  background-color: rgba(255, 255, 255, 0.1);
  margin: 40rpx;
  border-radius: 24rpx;
  padding: 40rpx;
  backdrop-filter: blur(20rpx);
}

.settings-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 32rpx;
  display: block;
  text-align: center;
}

.setting-item {
  margin-bottom: 40rpx;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  font-size: 26rpx;
  margin-bottom: 20rpx;
  display: block;
  opacity: 0.9;
}

.setting-options {
  display: flex;
  gap: 16rpx;
  justify-content: center;
}

.option-btn {
  padding: 16rpx 24rpx;
  border-radius: 20rpx;
  background-color: rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.option-btn.active {
  background-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
}

.option-text {
  font-size: 24rpx;
  color: white;
}

.rhythm-options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.rhythm-btn {
  padding: 24rpx;
  border-radius: 16rpx;
  background-color: rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.rhythm-btn.active {
  background-color: rgba(255, 255, 255, 0.4);
}

.rhythm-name {
  font-size: 26rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
  display: block;
}

.rhythm-pattern {
  font-size: 22rpx;
  opacity: 0.8;
}

/* 完成模态框 */
.completion-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(20rpx);
}

.modal-content {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(255, 255, 255, 0.8) 100%
  );
  margin: 40rpx;
  border-radius: 24rpx;
  padding: 60rpx 40rpx;
  text-align: center;
  color: #333;
  max-width: 600rpx;
  backdrop-filter: blur(20rpx);
}

.completion-icon {
  font-size: 80rpx;
  margin-bottom: 24rpx;
  display: block;
}

.completion-title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
  color: #333;
}

.completion-desc {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 40rpx;
  display: block;
  line-height: 1.6;
}

.completion-stats {
  display: flex;
  justify-content: center;
  gap: 60rpx;
  margin-bottom: 40rpx;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
  display: block;
}

.stat-label {
  font-size: 22rpx;
  color: #999;
}

.completion-actions {
  display: flex;
  gap: 20rpx;
  justify-content: center;
}

.action-btn {
  padding: 24rpx 40rpx;
  border-radius: 60rpx;
  font-size: 28rpx;
  font-weight: bold;
  transition: all 0.3s ease;
}

.action-btn.secondary {
  background-color: #f0f0f0;
  color: #666;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.action-btn:active {
  transform: scale(0.95);
}

/* 响应式设计 */
@media (max-width: 480rpx) {
  .breathing-circle {
    width: 320rpx;
    height: 320rpx;
  }

  .guide-ring {
    width: 360rpx;
    height: 360rpx;
  }

  .control-buttons {
    gap: 24rpx;
  }

  .completion-stats {
    flex-direction: column;
    gap: 24rpx;
  }

  .completion-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}

/* 动画效果 */
@keyframes breathePulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.breathing-circle.inhale {
  animation: none; /* 使用CSS transition替代 */
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .modal-content {
    background: linear-gradient(
      135deg,
      rgba(50, 50, 50, 0.95) 0%,
      rgba(30, 30, 30, 0.9) 100%
    );
    color: white;
  }

  .completion-title {
    color: white;
  }

  .action-btn.secondary {
    background-color: #333;
    color: #ccc;
  }
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
  .breathing-circle {
    transition-duration: 0.1s !important;
  }

  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.1s !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .breathing-circle {
    border: 4rpx solid white;
  }

  .control-btn,
  .option-btn,
  .rhythm-btn {
    border: 2rpx solid rgba(255, 255, 255, 0.5);
  }
}
</style>
