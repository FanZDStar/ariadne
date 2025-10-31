<template>
  <view
    v-if="visible"
    class="back-to-top"
    :style="buttonStyle"
    @click="scrollToTop"
  >
    <image src="../static/backToTop.png" class="back-to-top-icon"></image>
  </view>
</template>

<script>
export default {
  name: "BackToTop",
  props: {
    threshold: {
      type: Number,
      default: 300,
    },
    bottom: {
      type: Number,
      default: 80,
    },
    right: {
      type: Number,
      default: 30,
    },
    duration: {
      type: Number,
      default: 50,
    },
  },
  data() {
    return {
      visible: false,
    };
  },
  computed: {
    buttonStyle() {
      return {
        bottom: this.bottom + "rpx",
        right: this.right + "rpx",
      };
    },
  },
  mounted() {
    this.$emit("start-scroll-listener");
  },
  beforeDestroy() {
    this.$emit("remove-scroll-listener");
  },
  methods: {
    updateVisibility(scrollTop) {
      this.visible = scrollTop > this.threshold;
    },
    scrollToTop() {
      // 尝试触发父组件的滚动到顶部方法
      this.$emit("scroll-to-top");

      // 备用的页面滚动方法
      uni.pageScrollTo({
        scrollTop: 0,
        duration: this.duration,
        success: () => {
          this.$emit("scroll-to-top-success");
        },
      });
    },
  },
};
</script>

<style scoped>
.back-to-top {
  position: absolute; /* 从 fixed 改为 absolute，相对于父容器定位 */
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #ffafcc, #ffc8dd);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  transition: all 0.3s ease;
  box-shadow: 0 4rpx 16rpx rgba(255, 175, 204, 0.4);
}

.back-to-top:active {
  transform: scale(0.9);
}

.back-to-top-icon {
  width: 60rpx;
  height: 60rpx;
  filter: brightness(0) invert(1);
}
</style>
