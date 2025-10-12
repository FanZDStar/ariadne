<template>
  <view
    class="tree-hole-container"
    :class="{ 'day-theme': theme === 'day', 'night-theme': theme === 'night' }"
  >
    <!-- 全屏背景图片 - 添加key强制更新 -->
    <image
      class="background-image"
      :src="backgroundImage"
      :key="'bg-' + theme + '-' + level"
      mode="aspectFill"
    />

    <!-- 能量条 - 添加key强制重新渲染 -->
    <view
      class="energy-bar-container"
      :key="'energy-' + energy + '-level-' + level"
    >
      <view class="energy-bar-bg">
        <view
          class="energy-bar-fill"
          :style="{ width: energyProgress + '%' }"
        ></view>
      </view>
      <text class="energy-bar-text"
        >能量：{{ energyProgress }}/100　等级：Lv.{{ level }}</text
      >
      <text class="energy-tip">每升10级可以让树木成长哦</text>
    </view>

    <!-- 主题切换按钮 -->
    <view class="theme-switch" @click="toggleTheme">
      <text class="theme-icon">{{ theme === "day" ? "🌙" : "☀️" }}</text>
    </view>

    <view class="tree-area">
      <!-- 水壶图片 - 点击浇水 -->
      <view class="kettle-container">
        <image
          class="kettle-image"
          :class="{ 'kettle-disabled': !canWater }"
          src="../../static/kettle.png"
          mode="aspectFit"
          @click="waterTree"
        />
        <!-- 倒计时提示 -->
        <view class="cooldown-timer" v-if="!canWater && remainingSeconds > 0" :key="remainingSeconds">
          <text class="timer-text">{{ cooldownDisplay }}</text>
        </view>
        <view class="cooldown-timer ready" v-else-if="canWater">
          <text class="timer-text">可以浇水</text>
        </view>
      </view>
    </view>

    <view class="options-container">
      <view class="option-card" @click="goToMyWhispers">
        <text class="option-icon">❤️</text>
        <text class="option-text">此情此语</text>
      </view>

      <view class="option-card" @click="goToListen">
        <text class="option-icon">👂</text>
        <text class="option-text">做倾听者</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      theme: "day", // 'day' or 'night'
      energy: 0, // 当前能量
      level: 1, // 当前等级
      isWatering: false, // 是否正在浇水
      canWater: true, // 是否可以浇水
      remainingSeconds: 0, // 剩余冷却秒数
      countdownTimer: null, // 倒计时定时器
    };
  },
  computed: {
    backgroundImage() {
      // 强制依赖 level 和 theme，确保响应式更新
      const currentLevel = Number(this.level);
      const currentTheme = this.theme;

      console.log("🎨 计算背景图片:", {
        level: currentLevel,
        theme: currentTheme,
        "level >= 20": currentLevel >= 20,
        "level >= 10": currentLevel >= 10,
      });

      let imagePath = "";

      if (currentTheme === "day") {
        if (currentLevel >= 20) {
          imagePath = "/static/sun3.png";
          console.log("✅ 白天 - 选择 sun3（>=20级）");
        } else if (currentLevel >= 10) {
          imagePath = "/static/sun2.png";
          console.log("✅ 白天 - 选择 sun2（>=10级）");
        } else {
          imagePath = "/static/sun1.png";
          console.log("✅ 白天 - 选择 sun1（<10级）");
        }
      } else {
        if (currentLevel >= 20) {
          imagePath = "/static/moon3.png";
          console.log("✅ 夜晚 - 选择 moon3（>=20级）");
        } else if (currentLevel >= 10) {
          imagePath = "/static/moon2.png";
          console.log("✅ 夜晚 - 选择 moon2（>=10级）");
        } else {
          imagePath = "/static/moon1.png";
          console.log("✅ 夜晚 - 选择 moon1（<10级）");
        }
      }

      console.log("🖼️ 最终背景路径:", imagePath);
      return imagePath;
    },
    // 计算能量进度（用于能量条显示）
    energyProgress() {
      const progress = this.energy % 100;
      return progress;
    },
    // 倒计时显示文本（计算属性）
    cooldownDisplay() {
      const minutes = Math.floor(this.remainingSeconds / 60);
      const secs = this.remainingSeconds % 60;
      return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
  },
  watch: {
    level(newLevel, oldLevel) {
      console.log("📊 等级变化:", oldLevel, "→", newLevel);
      this.$forceUpdate(); // 强制更新组件
    },
    theme(newTheme, oldTheme) {
      console.log("🌓 主题切换:", oldTheme, "→", newTheme);
    },
  },
  onLoad() {
    this.setInitialTheme();
    this.fetchTreeEnergy();
  },
  onShow() {
    // 每次页面显示时都更新导航栏样式，防止从其他页面返回时样式被重置
    this.updateNavBar();
    // 刷新能量数据
    this.fetchTreeEnergy();
  },
  onUnload() {
    // 页面卸载时清除定时器
    this.clearCountdown();
  },
  methods: {
    formatTime(seconds) {
      // 格式化倒计时显示
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}:${secs.toString().padStart(2, "0")}`;
    },
    startCountdown() {
      // 启动倒计时
      this.clearCountdown();
      console.log("⏰ 启动倒计时定时器，初始秒数:", this.remainingSeconds);
      this.countdownTimer = setInterval(() => {
        if (this.remainingSeconds > 0) {
          this.remainingSeconds--;
          console.log("⏱️ 倒计时更新:", this.remainingSeconds, "秒");
        } else {
          console.log("✅ 倒计时结束，可以浇水了");
          this.canWater = true;
          this.clearCountdown();
        }
      }, 1000);
    },
    clearCountdown() {
      // 清除倒计时
      if (this.countdownTimer) {
        console.log("🛑 清除倒计时定时器");
        clearInterval(this.countdownTimer);
        this.countdownTimer = null;
      }
    },
    async fetchTreeEnergy() {
      // 获取用户能量和等级
      const token = uni.getStorageSync("access_token");
      if (!token) {
        console.log("❌ 未登录，使用默认能量和等级");
        return;
      }

      try {
        const response = await uni.request({
          url: "http://127.0.0.1:8000/tree-energy/status",
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.energy = parseInt(response.data.energy) || 0;
          this.level = parseInt(response.data.level) || 1;
          this.canWater = response.data.can_water !== false; // 默认true，只有明确false才是false
          this.remainingSeconds = parseInt(response.data.remaining_seconds) || 0;

          console.log("✅ 能量状态:", {
            energy: this.energy,
            level: this.level,
            canWater: this.canWater,
            remainingSeconds: this.remainingSeconds,
            rawData: response.data,
            background: this.backgroundImage,
          });

          // 清除旧的倒计时
          this.clearCountdown();
          
          // 如果有剩余时间且不能浇水，启动倒计时
          if (this.remainingSeconds > 0 && !this.canWater) {
            console.log("🔄 启动倒计时:", this.remainingSeconds, "秒");
            this.startCountdown();
          } else if (this.canWater) {
            console.log("✅ 可以浇水，无需倒计时");
          }
        }
      } catch (error) {
        console.error("❌ 获取能量状态异常:", error);
      }
    },
    async waterTree() {
      // 浇水增加能量
      if (this.isWatering) {
        return;
      }

      // 检查是否可以浇水
      if (!this.canWater) {
        uni.showToast({
          title: `冷却中，还需${this.formatTime(this.remainingSeconds)}`,
          icon: "none",
          duration: 2000,
        });
        return;
      }

      const token = uni.getStorageSync("access_token");
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      // 检查是否已达到30级且能量已满
      if (this.level >= 30 && this.energy >= 100) {
        uni.showToast({
          title: "能量已满，无需浇水",
          icon: "none",
          duration: 2000,
        });
        console.log("⚠️ 已达满级且能量已满");
        return;
      }

      this.isWatering = true;

      try {
        const response = await uni.request({
          url: "http://127.0.0.1:8000/tree-energy/water",
          method: "POST",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          const data = response.data;

          this.energy = parseInt(data.energy) || 0;
          this.level = parseInt(data.level) || 1;
          this.canWater = data.can_water !== false;
          this.remainingSeconds = parseInt(data.remaining_seconds) || 0;

          console.log("💧 浇水成功:", {
            energy: this.energy,
            level: this.level,
            leveledUp: data.leveled_up,
            canWater: this.canWater,
            remainingSeconds: this.remainingSeconds,
            rawData: data,
            background: this.backgroundImage,
          });

          // 清除旧的倒计时
          this.clearCountdown();
          
          // 启动新的倒计时
          if (this.remainingSeconds > 0 && !this.canWater) {
            console.log("🔄 浇水后启动倒计时:", this.remainingSeconds, "秒");
            this.startCountdown();
          }

          // 显示提示信息
          uni.showToast({
            title: data.message,
            icon: data.leveled_up ? "success" : "none",
            duration: 2000,
          });

          // 如果升级了，添加震动反馈
          if (data.leveled_up) {
            uni.vibrateShort();
          }
        }
      } catch (error) {
        console.error("❌ 浇水异常:", error);

        // 处理冷却时间错误
        if (error.statusCode === 400) {
          uni.showToast({
            title: error.data?.detail || "浇水冷却中",
            icon: "none",
            duration: 2000,
          });
        } else {
          uni.showToast({
            title: "浇水失败，请重试",
            icon: "none",
          });
        }
      } finally {
        this.isWatering = false;
      }
    },
    setInitialTheme() {
      const hour = new Date().getHours();
      // 晚上6点到早上6点之间为夜晚
      if (hour >= 18 || hour < 6) {
        this.theme = "night";
      } else {
        this.theme = "day";
      }
    },
    toggleTheme() {
      this.theme = this.theme === "day" ? "night" : "day";
      this.updateNavBar();
    },
    updateNavBar() {
      const isDay = this.theme === "day";
      uni.setNavigationBarColor({
        frontColor: isDay ? "#000000" : "#ffffff", // 白天用黑色文字，晚上用白色
        backgroundColor: isDay ? "#87CEEB" : "#2c3e50",
      });
    },
    goToListen() {
      uni.navigateTo({
        url: "/pages/tree-hole/listen-whisper",
      });
    },
    goToMyWhispers() {
      uni.navigateTo({
        url: "/pages/tree-hole/my-whispers",
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
  position: relative;
  overflow: hidden;
}

/* 全屏背景图片 */
.background-image {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  transition: opacity 0.5s ease;
}

/* 能量条容器 */
.energy-bar-container {
  position: fixed;
  top: 120rpx;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  width: 70vw;
  max-width: 600rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  padding: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.night-theme .energy-bar-container {
  background: rgba(44, 62, 80, 0.9);
}

.energy-bar-bg {
  width: 100%;
  height: 30rpx;
  background: rgba(200, 200, 200, 0.3);
  border-radius: 15rpx;
  overflow: hidden;
  margin-bottom: 10rpx;
  border: 2rpx solid rgba(255, 215, 0, 0.5);
}

.energy-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ffd700, #ffed4e);
  border-radius: 15rpx;
  transition: width 0.5s ease;
  box-shadow: 0 0 10rpx rgba(255, 215, 0, 0.5);
}

.energy-bar-text {
  font-size: 24rpx;
  color: #333;
  font-weight: bold;
  text-shadow: 0 1rpx 2rpx rgba(255, 255, 255, 0.8);
}

.night-theme .energy-bar-text {
  color: #ecf0f1;
  text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.5);
}

.energy-tip {
  font-size: 20rpx;
  color: rgba(100, 100, 100, 0.7);
  margin-top: 8rpx;
  text-align: center;
}

.night-theme .energy-tip {
  color: rgba(236, 240, 241, 0.6);
}

.theme-switch {
  position: fixed;
  top: 100rpx;
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
  position: relative;
  z-index: 1;
}

.kettle-container {
  position: fixed;
  right: 20rpx;
  bottom: 550rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
}

.kettle-image {
  width: 200rpx;
  height: 200rpx;
  opacity: 0.95;
  transition: opacity 0.3s, transform 0.3s, filter 0.3s;
  cursor: pointer;
}

.kettle-image:active {
  opacity: 1;
  transform: scale(1.15);
}

.kettle-disabled {
  opacity: 0.5;
  filter: grayscale(50%);
}

.cooldown-timer {
  margin-top: 10rpx;
  padding: 10rpx 20rpx;
  background: rgba(255, 99, 71, 0.9);
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
}

.cooldown-timer.ready {
  background: rgba(76, 175, 80, 0.9);
}

.timer-text {
  font-size: 24rpx;
  color: #fff;
  font-weight: bold;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.options-container {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 0;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 20rpx;
  margin-top: 40rpx;
  margin-bottom: 80rpx;
  transition: background-color 0.5s;
  z-index: 1;
  position: relative;
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
  width: 240rpx;
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
