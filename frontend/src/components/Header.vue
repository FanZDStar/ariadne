<template>
  <view class="header">
    <image class="logo" src="/static/logo.png" alt="logo" />
    <text class="title">OurEDA Ariadne</text>
  </view>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style scoped>
.header {
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 10vw;
  padding-bottom: 4vw;
  background: linear-gradient(135deg, #007aff 0%, #4cd964 100%);
  border-bottom-left-radius: 8vw;
  border-bottom-right-radius: 8vw;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.logo {
  width: 22vw;
  height: 22vw;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
  margin-bottom: 2vw;
}
.title {
  color: #fff;
  font-size: 6vw;
  font-weight: bold;
  letter-spacing: 1vw;
  text-shadow: 0 2px 8px rgba(0,0,0,0.10);
}
</style>
