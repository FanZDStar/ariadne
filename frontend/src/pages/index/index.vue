<template>
  <view>
    <Header />
    <MainContent>
      <text class="welcome">欢迎使用 OurEDA Ariadne！</text>
    </MainContent>
  </view>
</template>

<script>
import Header from '@/components/Header.vue'
import MainContent from '@/components/MainContent.vue'

export default {
  components: {
    Header,
    MainContent
  }
}
</script>

<style scoped>
.welcome {
  font-size: 5vw;
  color: #007aff;
  font-weight: 600;
  margin-top: 4vw;
  letter-spacing: 0.5vw;
  text-align: center;
}
</style>