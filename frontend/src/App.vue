<script>
export default {
  onLaunch: function () {
    console.log('App Launch')
    // 启动时不再自动跳转，交由 index.vue 处理
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
  },
}
</script>

<style>
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