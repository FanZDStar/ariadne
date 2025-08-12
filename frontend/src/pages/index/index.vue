
<template>
  <view>
    <text>欢迎</text>
  </view>
</template>

<script>
export default {
  mounted() {
    setTimeout(() => {
      uni.redirectTo({
        url: '/pages/login/login'
      })
    }, 1000) // 1秒后跳转
  }
}
</script>

<style scoped>
</style>