<template>
  <view class="app-wrapper">
    <!-- 看板娘由插件全局管理，无需在这里添加 -->
  </view>
</template>

<script>
export default {
  onLaunch: function () {
    console.log("🚀 App Launch");
  },

  onShow: function () {
    console.log("📱 App Show");
  },

  onHide: function () {
    console.log("💤 App Hide");
  },
};
</script>

<style>
/* 引入全局样式文件 */
@import "@/static/css/global.css";

/* 应用容器样式 */
.app-wrapper {
  width: 100%;
  height: 100%;
}

/* 全局限制所有图片宽度 */
image,
img {
  max-width: 100% !important;
  height: auto;
  display: block;
}

/* 限制所有使用100vw的元素 */
.mascot-container,
.tree-hole-container,
.dress-modal {
  max-width: 950rpx !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
}
</style>
