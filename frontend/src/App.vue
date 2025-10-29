<template>
  <view class="app-wrapper">
    <!-- 看板娘由插件全局管理，无需在这里添加 -->
  </view>
</template>

<script>
export default {
  onLaunch: function () {
    console.log('🚀 App Launch')
  },

  onShow: function () {
    console.log('📱 App Show')
  },

  onHide: function () {
    console.log('💤 App Hide')
  }
}
</script>

<style>
/* 应用容器样式 */
.app-wrapper {
  width: 100%;
  height: 100%;
}

/* 每个页面公共css */

/* 限制整体应用容器宽度 */
#app,
uni-app,
body {
  max-width: 750rpx;
  margin: 0 auto !important;
  background-color: #f5f5f5;
}

/* 限制页面主体宽度 */
page {
  max-width: 750rpx;
  margin: 0 auto;
  overflow-x: hidden;
  /* 防止横向滚动 */
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
  max-width: 750rpx !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
}

/* 修复底部 tabBar - 使用正确的选择器 */
.uni-tabbar {
  max-width: 750rpx !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  box-sizing: border-box;
}

/* 修复顶部导航栏 - 使用正确的选择器 */
.uni-page-head {
  max-width: 750rpx !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  box-sizing: border-box;
}

/* 确保自定义导航栏也被限制 */
uni-page-head,
.uni-page-head-hd,
.uni-page-head-bd {
  max-width: 750rpx;
}
</style>