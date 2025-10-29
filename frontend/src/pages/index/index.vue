<template>
  <view class="splash-container">
    <image class="splash-image" src="/src/static/beforelogin.png" mode="aspectFill"></image>
  </view>
</template>

<script>
export default {
  mounted() {
    setTimeout(() => {
      uni.redirectTo({
        url: "/pages/login/login",
      });
    }, 3000); // 3秒后跳转到登录页面
  },
};
</script>

<style scoped>
.splash-container {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 750rpx;
  width: 100%;
  height: 100vh;
  z-index: 9999;
  background: #ffffff;
}

.splash-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* uniapp 端样式 - 图片宽度等于屏幕宽，拉升全屏 */
/* #ifdef APP-PLUS || MP-WEIXIN || MP-ALIPAY || MP-BAIDU || MP-TOUTIAO || MP-QQ */
.splash-image {
  width: 100%;
  height: 100vh;
  object-fit: fill;
  /* 拉升填满整个容器 */
}

/* #endif */

/* web 端样式 - 高度是网页高度，不全屏拉伸 */
/* #ifdef H5 */
.splash-container {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 750rpx;
  width: 100%;
  height: 100vh;
}

.splash-image {
  width: 100%;
  height: 100vh;
  /* 高度等于视口高度 */
  object-fit: contain;
  /* 保持比例，不拉伸变形 */
}

/* #endif */
</style>
