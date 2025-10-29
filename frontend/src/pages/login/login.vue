<template>
  <view class="login-container">
    <!-- 背景图片 -->
    <image class="background-image" src="/src/static/loginbg.jpg" mode="aspectFill"></image>

    <!-- 粒子动效层 -->
    <view class="particles-container">
      <view v-for="(particle, index) in particles" :key="index" class="particle" :style="particle.style"></view>
    </view>

    <view class="login-header">
      <image class="logo" src="/static/logo.png"></image>
      <text class="title">念念有声</text>
      <text class="subtitle">聚焦人文复兴，关注当代年轻人情感问题</text>
    </view>

    <view class="login-form">
      <view class="input-group">
        <input class="input" placeholder="请输入账号或邮箱" v-model="username" />
      </view>

      <!-- <view class="input-group">
                <input class="input" placeholder="请输入密码" v-model="password" password />
            </view> -->
      <view class="input-group">
        <view class="password-input-container">
          <input class="input" placeholder="请输入密码" :password="!showPassword" v-model="password" />
          <text class="eye-icon" @click="showPassword = !showPassword">{{
            showPassword ? "👁️" : "👁️‍🗨️"
          }}</text>
        </view>
      </view>
      <button class="login-btn" @click="handleLogin">登录</button>

      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link" @click="goToRegister">立即注册</text>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from "../../utils/api.js";

export default {
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      particles: [], // 粒子数组
      particleConfig: {
        count: 1000, // 粒子数量（可以调整）
        sizeRange: { min: 1, max: 11 }, // 大小范围（px）
        opacityRange: { min: 0.2, max: 0.9 }, // 透明度范围
        speedRange: { min: 6, max: 12 }, // 动画速度范围（秒）
        delayRange: { min: 0, max: 5 }, // 延迟范围（秒）
      },
    };
  },
  mounted() {
    this.initParticles();
  },
  methods: {
    // 初始化粒子系统
    initParticles() {
      this.particles = [];

      // 根据配置创建粒子
      for (let i = 0; i < this.particleConfig.count; i++) {
        this.createParticle(i);
      }
    },

    // 创建单个粒子
    createParticle(index) {
      const config = this.particleConfig;

      // 随机大小
      const size = this.randomInRange(
        config.sizeRange.min,
        config.sizeRange.max
      );

      // 随机透明度
      const opacity = this.randomInRange(
        config.opacityRange.min,
        config.opacityRange.max
      );

      // 随机动画速度
      const duration = this.randomInRange(
        config.speedRange.min,
        config.speedRange.max
      );

      // 随机延迟
      const delay = this.randomInRange(
        config.delayRange.min,
        config.delayRange.max
      );

      // 随机起始位置（从屏幕外开始）
      const startX = this.randomInRange(-200, 100); // vw
      const startY = this.randomInRange(-200, 100); // vh

      // 随机发光强度
      const glowIntensity = this.randomInRange(2, 10);

      const particle = {
        id: index,
        style: {
          width: size + "px",
          height: size + "px",
          left: startX + "vw",
          top: startY + "vh",
          animationDelay: delay + "s",
          animationDuration: duration + "s",
          opacity: opacity,
          boxShadow: `0 0 ${glowIntensity}px rgba(255, 255, 255, ${opacity * 0.8
            })`,
          background: `rgba(255, 255, 255, ${opacity})`,
        },
      };

      this.particles.push(particle);
    },

    // 生成指定范围内的随机数
    randomInRange(min, max) {
      return min + Math.random() * (max - min);
    },
    async handleLogin() {
      // 简单验证
      if (!this.username || !this.password) {
        uni.showToast({
          title: "请输入账号和密码",
          icon: "none",
        });
        return;
      }

      // 调用后端登录接口
      try {
        const res = await api.login({
          username: this.username,
          password: this.password,
        });

        if (res.access_token) {
          // 保存token
          storage.setToken(res.access_token);

          // 保存星星奖励信息到本地存储，供home页面使用
          storage.setStarReward({
            awarded: res.star_awarded || false,
            points: res.star_points || 0,
            message: res.star_message || "欢迎回来~ 💫",
          });

          // 直接跳转到主页，不显示"登录成功"提示
          uni.switchTab({
            url: "/pages/home/home",
          });
        } else {
          uni.showToast({
            title: "登录失败",
            icon: "none",
          });
        }
      } catch (error) {
        console.error("登录错误:", error);

        // 精确区分错误类型
        let errorMsg = "登录失败";

        if (error.message) {
          // 网络错误
          if (error.message.includes("网络请求失败")) {
            errorMsg = "网络连接失败，请检查网络";
          }
          // HTTP状态码错误
          else if (error.message.includes("HTTP 401")) {
            errorMsg = "账号或密码错误";
          } else if (error.message.includes("HTTP")) {
            errorMsg = "服务器错误，请稍后再试";
          }
          // 其他错误
          else {
            errorMsg = error.message;
          }
        }

        uni.showToast({
          title: errorMsg,
          icon: "none",
        });
      }
    },

    goToRegister() {
      uni.navigateTo({
        url: "/pages/register/register",
      });
    },
  },
};
</script>

<style scoped>
.login-container {
  position: relative;
  padding: 40rpx;
  min-height: 100vh;
  overflow: hidden;
}

/* 背景图片样式 */
.background-image {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 750rpx;
  width: 100%;
  height: 100vh;
  z-index: -2;
  object-fit: contain;
  /* 保持比例，不拉伸变形 */
}

/* 粒子容器 */
.particles-container {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  max-width: 750rpx;
  width: 100%;
  height: 100vh;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

/* 粒子样式 */
.particle {
  position: absolute;
  border-radius: 50%;
  animation: float-diagonal infinite linear;
}

/* 添加一些粒子的轻微摆动效果 */
.particle:nth-child(6n) {
  animation: float-diagonal infinite linear, wobble 3s infinite ease-in-out;
}

.particle:nth-child(8n) {
  animation: float-diagonal infinite linear,
    wobble 4s infinite ease-in-out reverse;
}

/* 粒子动画 - 从左上飘到右下 */
@keyframes float-diagonal {
  0% {
    transform: translate(-100px, -100px) rotate(0deg);
    opacity: 0;
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    transform: translate(calc(100vw + 100px), calc(100vh + 100px)) rotate(360deg);
    opacity: 0;
  }
}

@keyframes wobble {

  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-10px);
  }
}

/* uniapp 端样式 - 图片宽度等于屏幕宽，拉伸高度全屏 */
/* #ifdef APP-PLUS || MP-WEIXIN || MP-ALIPAY || MP-BAIDU || MP-TOUTIAO || MP-QQ */
.background-image {
  width: 100vw;
  height: 100vh;
  object-fit: fill;
  /* 拉伸填满整个容器 */
}

/* #endif */

.login-header {
  text-align: center;
  margin-top: 100rpx;
  margin-bottom: 100rpx;
}

.logo {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 30rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  display: block;
  margin-bottom: 20rpx;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* 毛玻璃效果的登录表单 */
.login-form {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 30rpx;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10rpx;
  padding: 0 20rpx;
}

.input {
  height: 80rpx;
  font-size: 32rpx;
  color: #333;
  background: transparent;
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.password-input-container {
  display: flex;
  align-items: center;
  border-bottom: none;
}

.input {
  flex: 1;
  height: 80rpx;
  font-size: 32rpx;
  border: none;
  background: transparent;
  color: #333;
}

.eye-icon {
  margin-left: 10rpx;
  color: rgba(255, 255, 255, 0.8);
}

.login-btn {
  background: linear-gradient(135deg,
      rgba(0, 122, 255, 0.8),
      rgba(0, 122, 255, 1));
  color: white;
  border-radius: 10rpx;
  height: 80rpx;
  line-height: 80rpx;
  margin-top: 50rpx;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.register-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.link {
  color: rgba(0, 122, 255, 1);
  margin-left: 10rpx;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}
</style>
