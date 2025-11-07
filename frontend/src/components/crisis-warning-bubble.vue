<template>
  <view
    v-if="showBubble"
    class="crisis-bubble-container"
    :class="{ show: visible }"
  >
    <view class="mascot-avatar">
      <!-- 看板娘头像 -->
      <image :src="mascotAvatar" mode="aspectFit" class="avatar-image" />
    </view>

    <view class="bubble-content" :class="`risk-${riskLevel}`">
      <view class="bubble-header">
        <text class="header-icon">💕</text>
        <text class="header-text">小念的温馨提示</text>
      </view>

      <view class="bubble-message">
        {{ bubbleMessage }}
      </view>

      <!-- AI分析（如果有） -->
      <view v-if="aiAnalysis" class="ai-analysis">
        <text class="analysis-label">💭 </text>
        <text class="analysis-text">{{ aiAnalysis }}</text>
      </view>

      <!-- 建议按钮 -->
      <view class="action-buttons">
        <button class="btn btn-primary" size="mini" @click="handleOk">
          我知道了
        </button>
        <button
          v-if="showResourceBtn"
          class="btn btn-secondary"
          size="mini"
          @click="handleViewResources"
        >
          查看资源
        </button>
      </view>
    </view>

    <!-- 关闭按钮 -->
    <view class="close-btn" @click="handleClose">
      <text class="close-icon">×</text>
    </view>
  </view>
</template>

<script>
export default {
  name: "CrisisWarningBubble",

  props: {
    // 是否显示气泡
    show: {
      type: Boolean,
      default: false,
    },
    // 风险等级：low, medium, high, critical
    riskLevel: {
      type: String,
      default: "low",
      validator: (value) =>
        ["low", "medium", "high", "critical"].includes(value),
    },
    // 气泡消息内容
    message: {
      type: String,
      default: "",
    },
    // AI简短分析
    aiAnalysis: {
      type: String,
      default: "",
    },
    // 看板娘头像URL
    mascotAvatar: {
      type: String,
      default: "/static/images/mascot-default.png",
    },
    // 自动关闭时间（毫秒），0表示不自动关闭
    autoClose: {
      type: Number,
      default: 0,
    },
  },

  data() {
    return {
      visible: false,
      autoCloseTimer: null,
    };
  },

  computed: {
    showBubble() {
      return this.show && this.message;
    },

    bubbleMessage() {
      return this.message || "小念会一直陪伴在你身边哦～💖";
    },

    // 是否显示资源按钮（高风险和严重风险显示）
    showResourceBtn() {
      return ["high", "critical"].includes(this.riskLevel);
    },
  },

  watch: {
    show(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.visible = true;
          this.startAutoClose();
        });
      } else {
        this.visible = false;
        this.clearAutoClose();
      }
    },
  },

  methods: {
    handleOk() {
      this.$emit("ok");
      this.handleClose();
    },

    handleViewResources() {
      this.$emit("view-resources", this.riskLevel);
      // 跳转到资源页面或显示资源列表
      uni.showModal({
        title: "心理健康资源",
        content:
          "全国心理援助热线：400-161-9995\n\n24小时免费提供专业心理咨询服务",
        showCancel: true,
        cancelText: "我知道了",
        confirmText: "拨打热线",
        success: (res) => {
          if (res.confirm) {
            uni.makePhoneCall({
              phoneNumber: "4001619995",
            });
          }
        },
      });
    },

    handleClose() {
      this.visible = false;
      this.clearAutoClose();
      setTimeout(() => {
        this.$emit("close");
      }, 300); // 等待动画结束
    },

    startAutoClose() {
      if (this.autoClose > 0) {
        this.clearAutoClose();
        this.autoCloseTimer = setTimeout(() => {
          this.handleClose();
        }, this.autoClose);
      }
    },

    clearAutoClose() {
      if (this.autoCloseTimer) {
        clearTimeout(this.autoCloseTimer);
        this.autoCloseTimer = null;
      }
    },
  },

  beforeUnmount() {
    this.clearAutoClose();
  },
};
</script>

<style scoped lang="scss">
.crisis-bubble-container {
  position: fixed;
  bottom: 120rpx;
  left: 30rpx;
  right: 30rpx;
  z-index: 9999;
  display: flex;
  align-items: flex-start;
  opacity: 0;
  transform: translateY(100rpx);
  transition: all 0.3s ease;

  &.show {
    opacity: 1;
    transform: translateY(0);
  }
}

.mascot-avatar {
  width: 100rpx;
  height: 100rpx;
  flex-shrink: 0;
  margin-right: 20rpx;

  .avatar-image {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 4rpx solid #fff;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  }
}

.bubble-content {
  flex: 1;
  background: linear-gradient(135deg, #fff5f7 0%, #ffffff 100%);
  border-radius: 24rpx;
  padding: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);
  position: relative;

  // 左侧小三角
  &::before {
    content: "";
    position: absolute;
    left: -16rpx;
    top: 20rpx;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 12rpx 16rpx 12rpx 0;
    border-color: transparent #fff5f7 transparent transparent;
  }

  // 不同风险等级的样式
  &.risk-critical {
    background: linear-gradient(135deg, #ffe5e5 0%, #fff0f0 100%);
    border-left: 6rpx solid #ff4d4f;

    &::before {
      border-color: transparent #ffe5e5 transparent transparent;
    }
  }

  &.risk-high {
    background: linear-gradient(135deg, #fff7e6 0%, #fffbf0 100%);
    border-left: 6rpx solid #ffa940;

    &::before {
      border-color: transparent #fff7e6 transparent transparent;
    }
  }

  &.risk-medium {
    background: linear-gradient(135deg, #e6f7ff 0%, #f0faff 100%);
    border-left: 6rpx solid #40a9ff;

    &::before {
      border-color: transparent #e6f7ff transparent transparent;
    }
  }
}

.bubble-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;

  .header-icon {
    font-size: 32rpx;
    margin-right: 8rpx;
  }

  .header-text {
    font-size: 28rpx;
    font-weight: 600;
    color: #333;
  }
}

.bubble-message {
  font-size: 28rpx;
  line-height: 1.6;
  color: #555;
  margin-bottom: 16rpx;
}

.ai-analysis {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12rpx;
  padding: 16rpx;
  margin-bottom: 16rpx;

  .analysis-label {
    font-size: 24rpx;
    color: #999;
  }

  .analysis-text {
    font-size: 24rpx;
    line-height: 1.5;
    color: #666;
  }
}

.action-buttons {
  display: flex;
  gap: 16rpx;
  margin-top: 16rpx;

  .btn {
    flex: 1;
    font-size: 26rpx;
    border-radius: 12rpx;

    &.btn-primary {
      background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
      color: #fff;
      border: none;
    }

    &.btn-secondary {
      background: #fff;
      color: #ff6b9d;
      border: 2rpx solid #ff6b9d;
    }
  }
}

.close-btn {
  position: absolute;
  top: -12rpx;
  right: -12rpx;
  width: 48rpx;
  height: 48rpx;
  background: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);

  .close-icon {
    font-size: 36rpx;
    color: #999;
    line-height: 1;
  }
}
</style>
