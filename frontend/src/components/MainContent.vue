<template>
  <view class="main-content">
    <slot />
  </view>
</template>

<script>
export default {
  name: 'MainContent',
}
</script>

<style scoped>
.main-content {
  width: 90vw;
  margin: 0 auto;
  margin-top: 6vw;
  background: #fff;
  border-radius: 4vw;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 6vw 4vw;
  min-height: 40vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
