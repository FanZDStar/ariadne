<template>
    <view class="login-container">
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
                    <text class="eye-icon" @click="showPassword = !showPassword">{{ showPassword ? '👁️' : '👁️‍🗨️'
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
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            username: '',
            password: '',
            showPassword: false
        }
    },
    methods: {
        async handleLogin() {
            // 简单验证
            if (!this.username || !this.password) {
                uni.showToast({
                    title: '请输入账号和密码',
                    icon: 'none'
                })
                return
            }

            // 调用后端登录接口
            try {
                const res = await api.login({
                    username: this.username,
                    password: this.password
                });

                if (res.access_token) {
                    // 保存token
                    storage.setToken(res.access_token);

                    // 登录成功，跳转到主页
                    uni.showToast({
                        title: '登录成功',
                        icon: 'success'
                    })

                    // 延迟跳转
                    setTimeout(() => {
                        uni.switchTab({
                            url: '/pages/home/home'
                        })
                    }, 1000)
                } else {
                    uni.showToast({
                        title: '登录失败',
                        icon: 'none'
                    })
                }
            } catch (error) {
                console.error('登录错误:', error);

                // 精确区分错误类型
                let errorMsg = '登录失败';

                if (error.message) {
                    // 网络错误
                    if (error.message.includes('网络请求失败')) {
                        errorMsg = '网络连接失败，请检查网络';
                    }
                    // HTTP状态码错误
                    else if (error.message.includes('HTTP 401')) {
                        errorMsg = '账号或密码错误';
                    }
                    else if (error.message.includes('HTTP')) {
                        errorMsg = '服务器错误，请稍后再试';
                    }
                    // 其他错误
                    else {
                        errorMsg = error.message;
                    }
                }

                uni.showToast({
                    title: errorMsg,
                    icon: 'none'
                })
            }
        },

        goToRegister() {
            uni.navigateTo({
                url: '/pages/register/register'
            })
        }
    }
}
</script>

<style scoped>
/* .eye-icon {
    margin-left: 90%;
} */

.login-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

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
    color: #333;
    display: block;
    margin-bottom: 20rpx;
}

.subtitle {
    font-size: 28rpx;
    color: #999;
}

.login-form {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.input-group {
    margin-bottom: 30rpx;
    border-bottom: 1rpx solid #eee;
}

.input {
    height: 80rpx;
    font-size: 32rpx;
}

.login-btn {
    background-color: #007aff;
    color: white;
    border-radius: 10rpx;
    height: 80rpx;
    line-height: 80rpx;
    margin-top: 50rpx;
}

.register-link {
    text-align: center;
    margin-top: 40rpx;
    font-size: 28rpx;
    color: #666;
}

.link {
    color: #007aff;
    margin-left: 10rpx;
}

.input-group {
    margin-bottom: 30rpx;
    border-bottom: 1rpx solid #eee;
}

.password-input-container {
    display: flex;
    align-items: center;
    border-bottom: none;
    /* 移除容器的边框 */
}

.input {
    flex: 1;
    height: 80rpx;
    font-size: 32rpx;
    border: none;
}

.eye-icon {
    margin-left: 10rpx;
}
</style>