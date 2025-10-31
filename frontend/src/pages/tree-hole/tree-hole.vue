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

    <!-- 水滴显示（页面顶部） -->
    <view class="water-drops-display" :key="'water-' + waterDrops">
      <text class="water-drop-icon">💧</text>
      <text class="water-drop-text">{{ waterDrops }}</text>
    </view>

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
      <!-- 水壶图片 - 点击转换所有水滴为能量 -->
      <view class="kettle-container" :key="'kettle-' + waterDrops">
        <image
          class="kettle-image"
          :class="{ 'kettle-disabled': waterDrops === 0 }"
          src="../../static/kettle.png"
          mode="aspectFit"
          @click="convertWaterDrops"
        />
        <!-- 水滴提示 -->
        <view class="kettle-tip" v-if="waterDrops > 0">
          <text class="tip-text">点击转换 {{ waterDrops }} 💧</text>
        </view>
        <view class="kettle-tip disabled" v-else>
          <text class="tip-text">暂无水滴</text>
        </view>
      </view>
    </view>

    <!-- 任务按钮（左下角） -->
    <view class="task-button" @click="showTaskModal = true">
      <text class="task-icon">🎁</text>
      <text class="task-text">任务</text>
    </view>

    <!-- 任务弹窗 -->
    <view
      class="task-modal-overlay"
      v-if="showTaskModal"
      @click="showTaskModal = false"
    >
      <view class="task-modal" @click.stop>
        <view class="modal-header">
          <text class="modal-title">每小时领取水滴</text>
          <view class="close-btn" @click="showTaskModal = false">×</view>
        </view>
        <view class="modal-content">
          <text class="task-description">每1个小时可以领取10个水滴💧</text>

          <!-- 倒计时显示 -->
          <view class="countdown-container" v-if="!canClaim">
            <text class="countdown-label">距离下次领取：</text>
            <text class="countdown-time" :key="claimRemainingSeconds">{{
              claimCountdownDisplay
            }}</text>
            <!-- 调试：显示原始秒数 -->
            <text
              class="countdown-debug"
              style="font-size: 20rpx; color: #999; margin-top: 5rpx"
            >
              ({{ claimRemainingSeconds }}秒)
            </text>
          </view>

          <!-- 领取按钮 -->
          <view class="claim-button-container">
            <button
              class="claim-button"
              :class="{ 'can-claim': canClaim, disabled: !canClaim }"
              :disabled="!canClaim"
              @click="claimWaterDrops"
            >
              {{ canClaim ? "领取 10💧" : "冷却中..." }}
            </button>
          </view>
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
      waterDrops: 0, // 当前水滴数量
      canClaim: true, // 是否可以领取水滴
      claimRemainingSeconds: 0, // 距离下次领取的剩余秒数
      claimCountdownTimer: null, // 领取倒计时定时器
      showTaskModal: false, // 是否显示任务弹窗
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
    // 领取倒计时显示文本（计算属性）
    claimCountdownDisplay() {
      const minutes = Math.floor(this.claimRemainingSeconds / 60);
      const secs = this.claimRemainingSeconds % 60;
      return `${minutes}:${secs.toString().padStart(2, "0")}`;
    },
  },
  watch: {
    level(newLevel, oldLevel) {
      console.log("📊 等级变化:", oldLevel, "→", newLevel);
      this.$forceUpdate(); // 强制更新组件
    },
    theme(newTheme, oldTheme) {
      console.log("🌓 主题切换:", oldTheme, "→", newTheme);
    },
    waterDrops(newVal, oldVal) {
      // 监听水滴数量变化
      console.log("💧 水滴数量变化:", oldVal, "→", newVal);
      this.$forceUpdate(); // 强制更新视图
    },
    claimRemainingSeconds(newVal, oldVal) {
      // 监听倒计时变化，确保视图更新
      console.log("⏱️ 倒计时变化:", oldVal, "→", newVal);
    },
    showTaskModal(newVal) {
      // 监听任务弹窗的打开/关闭
      if (newVal) {
        // 弹窗打开时，刷新水滴状态并启动倒计时
        console.log("🎁 任务弹窗打开，刷新水滴状态");
        this.fetchWaterDropsStatus();
      } else {
        // 弹窗关闭时，不清除倒计时（让它在后台继续运行）
        console.log("🎁 任务弹窗关闭");
      }
    },
  },
  onLoad() {
    this.setInitialTheme();
    this.fetchTreeEnergy();
    this.fetchWaterDropsStatus();
  },
  onShow() {
    // 每次页面显示时都更新导航栏样式，防止从其他页面返回时样式被重置
    this.updateNavBar();
    // 刷新能量数据和水滴数据
    this.fetchTreeEnergy();
    this.fetchWaterDropsStatus();
  },
  onUnload() {
    // 页面卸载时清除定时器
    this.clearClaimCountdown();
  },
  methods: {
    formatTime(seconds) {
      // 格式化倒计时显示
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}:${secs.toString().padStart(2, "0")}`;
    },
    startClaimCountdown() {
      // 启动领取倒计时
      this.clearClaimCountdown();
      console.log(
        "⏰ 启动领取倒计时定时器，初始秒数:",
        this.claimRemainingSeconds
      );

      this.claimCountdownTimer = setInterval(() => {
        if (this.claimRemainingSeconds > 0) {
          // 使用 this.$set 确保响应式更新
          this.claimRemainingSeconds = this.claimRemainingSeconds - 1;
          console.log(
            "⏱️ 领取倒计时更新:",
            this.claimRemainingSeconds,
            "秒",
            "显示:",
            this.claimCountdownDisplay
          );

          // 强制更新视图
          this.$forceUpdate();
        } else {
          console.log("✅ 领取倒计时结束，可以领取了");
          this.canClaim = true;
          this.clearClaimCountdown();
        }
      }, 1000);
    },
    clearClaimCountdown() {
      // 清除领取倒计时
      if (this.claimCountdownTimer) {
        console.log("🛑 清除领取倒计时定时器");
        clearInterval(this.claimCountdownTimer);
        this.claimCountdownTimer = null;
      }
    },
    async fetchWaterDropsStatus() {
      // 获取用户水滴状态
      const token = uni.getStorageSync("access_token");
      if (!token) {
        console.log("❌ 未登录，使用默认水滴状态");
        return;
      }

      try {
        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/water-drops/status`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.waterDrops = parseInt(response.data.water_drops) || 0;
          this.canClaim = response.data.can_claim !== false;
          this.claimRemainingSeconds =
            parseInt(response.data.remaining_seconds) || 0;

          console.log("✅ 水滴状态:", {
            waterDrops: this.waterDrops,
            canClaim: this.canClaim,
            claimRemainingSeconds: this.claimRemainingSeconds,
            rawData: response.data,
          });

          // 清除旧的倒计时
          this.clearClaimCountdown();

          // 如果有剩余时间且不能领取，启动倒计时
          if (this.claimRemainingSeconds > 0 && !this.canClaim) {
            console.log("🔄 启动领取倒计时:", this.claimRemainingSeconds, "秒");
            this.startClaimCountdown();
          } else if (this.canClaim) {
            console.log("✅ 可以领取，无需倒计时");
          }
        }
      } catch (error) {
        console.error("❌ 获取水滴状态异常:", error);
      }
    },
    async claimWaterDrops() {
      // 领取水滴
      if (!this.canClaim) {
        uni.showToast({
          title: `冷却中，还需${this.formatTime(this.claimRemainingSeconds)}`,
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

      try {
        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/water-drops/claim`,
          method: "POST",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          const data = response.data;

          this.waterDrops = parseInt(data.water_drops) || 0;
          this.canClaim = data.can_claim !== false;
          this.claimRemainingSeconds = parseInt(data.remaining_seconds) || 0;

          console.log("💧 领取成功:", {
            waterDrops: this.waterDrops,
            claimedAmount: data.claimed_amount,
            canClaim: this.canClaim,
            claimRemainingSeconds: this.claimRemainingSeconds,
            rawData: data,
          });

          // 强制更新视图
          this.$forceUpdate();

          // 清除旧的倒计时
          this.clearClaimCountdown();

          // 启动新的倒计时
          if (this.claimRemainingSeconds > 0 && !this.canClaim) {
            console.log(
              "🔄 领取后启动倒计时:",
              this.claimRemainingSeconds,
              "秒"
            );
            this.startClaimCountdown();
          }

          // 显示提示信息
          uni.showToast({
            title: data.message,
            icon: "success",
            duration: 2000,
          });

          // 添加震动反馈
          uni.vibrateShort();
        }
      } catch (error) {
        console.error("❌ 领取水滴异常:", error);

        // 处理冷却时间错误
        if (error.statusCode === 400) {
          uni.showToast({
            title: error.data?.detail || "领取冷却中",
            icon: "none",
            duration: 2000,
          });
        } else {
          uni.showToast({
            title: "领取失败，请重试",
            icon: "none",
          });
        }
      }
    },
    async convertWaterDrops() {
      // 转换水滴为能量
      if (this.waterDrops === 0) {
        uni.showToast({
          title: "暂无水滴可转换",
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

      // 确认转换
      uni.showModal({
        title: "确认转换",
        content: `确定要将 ${this.waterDrops} 个水滴转换为能量吗？`,
        success: async (res) => {
          if (res.confirm) {
            try {
              const response = await uni.request({
                url: `${
                  process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
                }/water-drops/convert-to-energy`,
                method: "POST",
                header: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
              });

              if (response.statusCode === 200) {
                const data = response.data;

                this.waterDrops = parseInt(data.water_drops) || 0;
                this.energy = parseInt(data.energy) || 0;
                this.level = parseInt(data.level) || 1;

                console.log("💧➡️⚡ 转换成功:", {
                  convertedDrops: data.converted_drops,
                  waterDrops: this.waterDrops,
                  energy: this.energy,
                  level: this.level,
                  leveledUp: data.leveled_up,
                  rawData: data,
                  background: this.backgroundImage,
                });

                // 强制更新视图
                this.$forceUpdate();

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

                // 刷新能量数据
                this.fetchTreeEnergy();
              }
            } catch (error) {
              console.error("❌ 转换水滴异常:", error);
              uni.showToast({
                title: error.data?.detail || "转换失败，请重试",
                icon: "none",
              });
            }
          }
        },
      });
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
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/tree-energy/status`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.energy = parseInt(response.data.energy) || 0;
          this.level = parseInt(response.data.level) || 1;

          console.log("✅ 能量状态:", {
            energy: this.energy,
            level: this.level,
            rawData: response.data,
            background: this.backgroundImage,
          });
        }
      } catch (error) {
        console.error("❌ 获取能量状态异常:", error);
      }
    },
    async waterTree() {
      // 浇水增加能量 - 已废弃，保留以防需要
      console.warn("⚠️ waterTree 方法已废弃，请使用 convertWaterDrops");
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
  left: 50%;
  top: 0;
  transform: translateX(-50%);
  max-width: 950rpx;
  width: 100%;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  transition: opacity 0.5s ease;
}

/* 水滴显示（页面顶部） */
.water-drops-display {
  position: fixed;
  top: 400rpx;
  left: 20rpx;
  z-index: 999;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 15rpx 30rpx;
  border-radius: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.night-theme .water-drops-display {
  background: rgba(44, 62, 80, 0.95);
}

.water-drop-icon {
  font-size: 40rpx;
  margin-right: 10rpx;
}

.water-drop-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #3498db;
}

.night-theme .water-drop-text {
  color: #5dade2;
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

.kettle-tip {
  margin-top: 10rpx;
  padding: 10rpx 20rpx;
  background: rgba(52, 152, 219, 0.9);
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
}

.kettle-tip.disabled {
  background: rgba(149, 165, 166, 0.7);
}

.tip-text {
  font-size: 24rpx;
  color: #fff;
  font-weight: bold;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

/* 任务按钮（左下角） */
.task-button {
  position: fixed;
  left: 40rpx;
  bottom: 540rpx;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20rpx;
  border-radius: 50%;
  width: 120rpx;
  height: 120rpx;
  justify-content: center;
  box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.4);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.task-button:active {
  transform: scale(0.95);
}

.task-icon {
  font-size: 48rpx;
  margin-bottom: 5rpx;
}

.task-text {
  font-size: 24rpx;
  color: #fff;
  font-weight: bold;
}

/* 任务弹窗 */
.task-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-modal {
  background: #fff;
  border-radius: 30rpx;
  width: 80%;
  max-width: 600rpx;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.night-theme .task-modal {
  background: #34495e;
}

.modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
}

.close-btn {
  font-size: 60rpx;
  color: #fff;
  cursor: pointer;
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  padding: 40rpx;
}

.task-description {
  font-size: 32rpx;
  color: #333;
  text-align: center;
  margin-bottom: 30rpx;
  font-weight: 500;
}

.night-theme .task-description {
  color: #ecf0f1;
}

.countdown-container {
  background: rgba(52, 152, 219, 0.1);
  padding: 20rpx;
  border-radius: 15rpx;
  text-align: center;
  margin-bottom: 30rpx;
}

.countdown-label {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}

.night-theme .countdown-label {
  color: #bdc3c7;
}

.countdown-time {
  font-size: 40rpx;
  font-weight: bold;
  color: #3498db;
}

.night-theme .countdown-time {
  color: #5dade2;
}

.claim-button-container {
  margin-top: 20rpx;
}

.claim-button {
  width: 100%;
  padding: 25rpx;
  border-radius: 20rpx;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.claim-button.can-claim {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  color: #fff;
  box-shadow: 0 6rpx 16rpx rgba(46, 204, 113, 0.4);
}

.claim-button.can-claim:active {
  transform: scale(0.98);
}

.claim-button.disabled {
  background: #bdc3c7;
  color: #7f8c8d;
  cursor: not-allowed;
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
