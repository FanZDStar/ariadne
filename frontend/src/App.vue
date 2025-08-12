<script>
export default {
  onLaunch: function () {
    console.log('App Launch')
    // 应用启动时检查是否已登录
    // 这里简化处理，实际应检查登录状态
    uni.redirectTo({
      url: '/pages/login/login'
    })
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
/*每个页面公共css */
</style>