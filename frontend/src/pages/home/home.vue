<!-- <template>
    <view class="home-container">
        <view class="header">
            <text class="title">念念有声</text>
            <text class="subtitle">聚焦人文复兴，关注当代年轻人情感问题</text>
            <view class="user-info" v-if="userInfo">
                <text class="welcome">欢迎，{{ userInfo.nickname || userInfo.username }}</text>
            </view>
        </view>

        <view class="content">
            <view class="card" @click="goToContext">
                <image class="card-icon" src="/static/chat-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">情感对话</text>
                    <text class="card-desc">与AI进行情感对话，获得专业建议</text>
                </view>
            </view>

            <view class="card" @click="goToTips">
                <image class="card-icon" src="/static/tips-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">恋爱小技巧</text>
                    <text class="card-desc">每天一点新鲜感，帮助你迈出第一步</text>
                </view>
            </view>

            <view class="card" @click="goToProtection">
                <image class="card-icon" src="/static/protection-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">感情防护</text>
                    <text class="card-desc">识别恋爱中的不公平，保护自己</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            userInfo: null
        }
    },

    onLoad() {
        this.loadUserInfo();
    },

    methods: {
        async loadUserInfo() {
            const token = storage.getToken();
            if (token) {
                try {
                    const userInfo = await api.getUserInfo(token);
                    this.userInfo = userInfo;
                    storage.setUserInfo(userInfo);
                } catch (error) {
                    console.error('获取用户信息失败:', error);
                    // Token可能已过期，清除本地存储
                    storage.clearToken();
                }
            }
        },

        goToContext() {
            uni.navigateTo({
                url: '/pages/chat-context/chat-context'
            })
        },

        goToTips() {
            uni.navigateTo({
                url: '/pages/tips/tips'
            })
        },

        goToProtection() {
            uni.navigateTo({
                url: '/pages/protection/protection'
            })
        }
    }
}
</script>

<style scoped>
.home-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-top: 60rpx;
    margin-bottom: 80rpx;
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

.user-info {
    margin-top: 20rpx;
}

.welcome {
    font-size: 32rpx;
    color: #007aff;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
}

.card {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.card-icon {
    width: 100rpx;
    height: 100rpx;
    margin-right: 30rpx;
}

.card-text {
    flex: 1;
}

.card-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.card-desc {
    font-size: 28rpx;
    color: #999;
}
</style> -->

<template>
    <view class="home-container">
        <view class="header">
            <text class="title">念念有声</text>
            <text class="subtitle">聚焦人文复兴，关注当代年轻人情感问题</text>
            <view class="user-info" v-if="userInfo">
                <text class="welcome">欢迎，{{ userInfo.nickname || userInfo.username }}</text>
            </view>
        </view>

        <view class="content">
            <view class="card" @click="goToContext">
                <image class="card-icon" src="/static/chat-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">情感对话</text>
                    <text class="card-desc">与AI进行情感对话，获得专业建议</text>
                </view>
            </view>

            <view class="card" @click="goToTips">
                <image class="card-icon" src="/static/tips-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">恋爱小技巧</text>
                    <text class="card-desc">每天一点新鲜感，帮助你迈出第一步</text>
                </view>
            </view>

            <view class="card" @click="goToProtection">
                <image class="card-icon" src="/static/protection-icon.png"></image>
                <view class="card-text">
                    <text class="card-title">感情防护</text>
                    <text class="card-desc">识别恋爱中的不公平，保护自己</text>
                </view>
            </view>

            <view class="card" @click="goToTreeHole">
                <image class="card-icon" src="/static/tree-hole.png"></image>
                <view class="card-text">
                    <text class="card-title">心灵树洞</text>
                    <text class="card-desc">倾诉心声，倾听他人，寻找共鸣</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            userInfo: null
        }
    },

    onLoad() {
        this.loadUserInfo();
    },

    onShow() {
        // 每次页面显示时都检查用户信息
        this.loadUserInfo();
    },

    methods: {
        async loadUserInfo() {
            const token = storage.getToken();
            if (token) {
                try {
                    const userInfo = await api.getUserInfo(token);
                    this.userInfo = userInfo;
                    storage.setUserInfo(userInfo);
                } catch (error) {
                    console.error('获取用户信息失败:', error);
                    // Token可能已过期，清除本地存储
                    storage.clearToken();
                }
            }
        },

        goToContext() {
            uni.navigateTo({
                url: '/pages/chat-context/chat-context'
            })
        },

        goToTips() {
            uni.navigateTo({
                url: '/pages/tips/tips'
            })
        },

        goToProtection() {
            uni.navigateTo({
                url: '/pages/protection/protection'
            })
        },

        goToTreeHole() {
            uni.navigateTo({
                url: '/pages/tree-hole/tree-hole'
            })
        }
    }
}
</script>

<style scoped>
.home-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-top: 60rpx;
    margin-bottom: 80rpx;
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

.user-info {
    margin-top: 20rpx;
}

.welcome {
    font-size: 32rpx;
    color: #007aff;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
}

.card {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.card-icon {
    width: 100rpx;
    height: 100rpx;
    margin-right: 30rpx;
}

.card-text {
    flex: 1;
}

.card-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.card-desc {
    font-size: 28rpx;
    color: #999;
}
</style>