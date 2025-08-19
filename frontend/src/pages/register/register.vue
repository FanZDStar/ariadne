<template>
    <view class="register-container">
        <view class="register-header">
            <text class="title">注册账号</text>
            <text class="subtitle">创建您的念念有声账号</text>
        </view>

        <view class="register-form">
            <view class="input-group">
                <input class="input" placeholder="请输入用户名" v-model="username" @input="validateUsername" />
                <text v-if="usernameError" class="error-text">{{ usernameError }}</text>
            </view>

            <view class="input-group">
                <input class="input" placeholder="请输入邮箱（可选）" v-model="email" @input="validateEmail" />
                <text v-if="emailError" class="error-text">{{ emailError }}</text>
            </view>

            <view class="input-group">
                <view class="password-input-container">
                    <input class="input" placeholder="请输入密码" :password="!showPassword" v-model="password"
                        @input="validatePassword" />
                    <text class="eye-icon" @click="showPassword = !showPassword">{{ showPassword ? '👁️' : '👁️‍🗨️'
                        }}</text>
                </view>
                <text v-if="passwordError" class="error-text">{{ passwordError }}</text>
            </view>
            <view class="input-group">
                <view class="password-input-container">
                    <input class="input" placeholder="请确认密码" :password="!showConfirmPassword"
                        v-model="confirmPassword" />
                    <text class="eye-icon" @click="showConfirmPassword = !showConfirmPassword">{{ showConfirmPassword ?
                        '👁️' : '👁️‍🗨️' }}</text>
                </view>
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
import { api } from '../../utils/api.js';

export default {
    data() {
        return {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            usernameError: '',
            passwordError: '',
            emailError: '',
            showPassword: false,
            showConfirmPassword: false,
        }
    },
    methods: {
        validateUsername() {
            const regex = /^(?=[a-zA-Z0-9]{2,15}$)(?!^[0-9]+$)(?!^[a-zA-Z]+$)/;
            if (!regex.test(this.username)) {
                this.usernameError = '用户名必须是2-15位的大小写字母和数字的组合';
            } else {
                this.usernameError = '';
            }
        },
        validatePassword() {
            // 更新后的密码正则表达式
            const regex = /^(((?=.*[a-zA-Z])(?=.*[0-9]))|((?=.*[a-zA-Z])(?=.*[!]))|((?=.*[0-9])(?=.*[!])))[a-zA-Z0-9!]{6,15}$/;
            if (!this.password) {
                this.passwordError = '请输入密码';
            } else if (!regex.test(this.password)) {
                this.passwordError = '密码必须是6-15位的大小写字母、数字和英文感叹号的两种或以上组合';
            } else {
                this.passwordError = '';
            }
        },
        validateEmail() {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.email && !regex.test(this.email)) {
                this.emailError = '邮箱格式不正确';
            } else {
                this.emailError = '';
            }
        },
        async handleRegister() {

            this.validateUsername();
            this.validatePassword();
            this.validateEmail();

            if (this.usernameError || this.passwordError || this.emailError) {
                console.log('前端验证失败:', {
                    usernameError: this.usernameError,
                    passwordError: this.passwordError,
                    emailError: this.emailError
                });
                uni.showToast({
                    title: this.usernameError || this.passwordError || this.emailError,
                    icon: 'none'
                });
                return;
            }

            if (!this.username || !this.password) {
                uni.showToast({
                    title: '请输入用户名和密码',
                    icon: 'none'
                })
                return
            }

            if (this.username.length > 15) {
                uni.showToast({
                    title: '用户名最多15个字符',
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

            // 调用后端注册接口
            try {
                const userData = {
                    username: this.username,
                    password: this.password
                };

                // 如果填写了邮箱，则添加到注册数据中
                if (this.email) {
                    userData.email = this.email;
                }

                console.log('发送注册请求:', userData);
                const res = await api.register(userData);
                console.log('注册响应:', res);

                if (res.user_id) {
                    uni.showToast({
                        title: '注册成功',
                        icon: 'success'
                    })

                    // 延迟跳转到登录页
                    setTimeout(() => {
                        uni.navigateBack()
                    }, 1000)
                } else {
                    uni.showToast({
                        title: '注册失败',
                        icon: 'none'
                    })
                }
            } catch (error) {
                console.error('注册错误:', error);
                let errorMsg = '注册失败';

                // 更精确的错误处理
                if (error.message) {
                    errorMsg = error.message;
                    // 如果是HTTP错误，提取关键信息
                    if (errorMsg.includes('already registered')) {
                        if (errorMsg.includes('Username')) {
                            errorMsg = '用户名已存在';
                        } else if (errorMsg.includes('Email')) {
                            errorMsg = '邮箱已被注册';
                        }
                    } else if (errorMsg.includes('HTTP 400')) {
                        errorMsg = '请求参数错误，请检查输入';
                    } else if (errorMsg.includes('网络请求失败')) {
                        errorMsg = '网络连接失败，请检查网络';
                    }
                }

                uni.showToast({
                    title: errorMsg,
                    icon: 'none'
                })
            }
        },

        goToLogin() {
            uni.navigateBack()
        }
    }
}
</script>

<style scoped>

/* .eye-icon {
    margin-left: 90%;
} */
.error-text {
    color: red;
    font-size: 24rpx;
}

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

.input-group {
    margin-bottom: 30rpx;
    border-bottom: 1rpx solid #eee;
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
}

.eye-icon {
    margin-left: 10rpx;
}
</style>