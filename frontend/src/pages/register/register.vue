<template>
    <view class="register-container">
        <view class="register-header">
            <text class="title">注册账号</text>
            <text class="subtitle">创建您的恋恋有声账号</text>
        </view>

        <view class="register-form">
            <view class="input-group">
                <input class="input" placeholder="请输入用户名" v-model="username" />
            </view>

            <view class="input-group">
                <input class="input" placeholder="请输入密码" v-model="password" password />
            </view>

            <view class="input-group">
                <input class="input" placeholder="请确认密码" v-model="confirmPassword" password />
            </view>

            <button class="register-btn" @click="handleRegister">注册</button>

            <view class="login-link">
                <text>已有账号？</text>
                <text class="link" @click="goToLogin">立即登录</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            confirmPassword: ''
        }
    },
    methods: {
        handleRegister() {
            if (!this.username || !this.password) {
                uni.showToast({
                    title: '请输入用户名和密码',
                    icon: 'none'
                })
                return
            }

            if (this.password !== this.confirmPassword) {
                uni.showToast({
                    title: '两次输入的密码不一致',
                    icon: 'none'
                })
                return
            }

            // 注册逻辑（这里简化处理，实际应调用后端接口）
            uni.showToast({
                title: '注册成功',
                icon: 'success'
            })

            // 延迟跳转到登录页
            setTimeout(() => {
                uni.navigateBack()
            }, 1000)
        },

        goToLogin() {
            uni.navigateBack()
        }
    }
}
</script>

<style scoped>
.register-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.register-header {
    text-align: center;
    margin-top: 100rpx;
    margin-bottom: 100rpx;
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

.register-form {
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

.register-btn {
    background-color: #007aff;
    color: white;
    border-radius: 10rpx;
    height: 80rpx;
    line-height: 80rpx;
    margin-top: 50rpx;
}

.login-link {
    text-align: center;
    margin-top: 40rpx;
    font-size: 28rpx;
    color: #666;
}

.link {
    color: #007aff;
    margin-left: 10rpx;
}
</style>