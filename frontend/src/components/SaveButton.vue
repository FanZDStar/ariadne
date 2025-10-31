<!-- src/components/SaveButton.vue -->
<template>
  <view
    class="save-button-floating"
    @click="handleSave"
    :class="{ disabled: !canSave }"
  >
    <image class="save-icon" src="/static/save.png" mode="aspectFit" />
  </view>
</template>

<script>
export default {
  name: "SaveButton",
  props: {
    canSave: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleSave() {
      if (this.canSave) {
        this.$emit("save");
      }
    },
  },
};
</script>

<style scoped>
.save-button-floating {
  position: fixed;
  right: calc(50% - 475rpx + 30rpx);
  bottom: 150rpx;
  width: 100rpx;
  height: 100rpx;
  background-color: #007aff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 122, 255, 0.3);
  z-index: 1000;
  transition: all 0.3s ease;
}

/* 当屏幕宽度小于950rpx时，使用原来的定位 */
@media (max-width: 475px) {
  .save-button-floating {
    right: 30rpx;
  }
}

.save-button-floating.disabled {
  background-color: #cccccc;
  box-shadow: 0 2rpx 6rpx rgba(204, 204, 204, 0.3);
  opacity: 0.6;
}

.save-button-floating:active {
  transform: scale(0.95);
}

.save-icon {
  width: 50rpx;
  height: 50rpx;
}
</style>
