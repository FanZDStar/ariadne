<template>
    <view class="profile-container">
        <view class="header">
            <image class="avatar" src="/static/avatar.png"></image>
            <text class="username">用户昵称</text>
            <text class="user-desc">情感探索者</text>
        </view>

        <view class="content">
            <view class="menu-item" @click="goToSettings">
                <text class="menu-text">个人设置</text>
                <text class="arrow">></text>
            </view>

            <view class="menu-item" @click="goToHistory">
                <text class="menu-text">对话历史</text>
                <text class="arrow">></text>
            </view>

            <view class="menu-item" @click="goToFavorites">
                <text class="menu-text">我的收藏</text>
                <text class="arrow">></text>
            </view>

            <view class="menu-item" @click="goToFeedback">
                <text class="menu-text">意见反馈</text>
                <text class="arrow">></text>
            </view>

            <view class="menu-item" @click="logout">
                <text class="menu-text logout">退出登录</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    methods: {
        goToSettings() {
            uni.showToast({
                title: '功能开发中',
                icon: 'none'
            })
        },

        goToHistory() {
            uni.showToast({
                title: '功能开发中',
                icon: 'none'
            })
        },

        goToFavorites() {
            uni.showToast({
                title: '功能开发中',
                icon: 'none'
            })
        },

        goToFeedback() {
            uni.showToast({
                title: '功能开发中',
                icon: 'none'
            })
        },

        logout() {
            uni.showModal({
                title: '提示',
                content: '确定要退出登录吗？',
                success: (res) => {
                    if (res.confirm) {
                        uni.redirectTo({
                            url: '/pages/login/login'
                        })
                    }
                }
            })
        }
    }
}
</script>

<style scoped>
.profile-container {
    padding: 40rpx;
    background-color: #f8f8f8;
    min-height: 100vh;
}

.header {
    text-align: center;
    background-color: #fff;
    border-radius: 20rpx;
    padding: 60rpx 40rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.avatar {
    width: 150rpx;
    height: 150rpx;
    border-radius: 50%;
    margin-bottom: 30rpx;
}

.username {
    font-size: 42rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
}

.user-desc {
    font-size: 28rpx;
    color: #999;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
}

.menu-item {
    background-color: #fff;
    padding: 40rpx;
    border-radius: 20rpx;
    position: relative;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.menu-text {
    font-size: 32rpx;
    color: #333;
}

.logout {
    color: #e64340;
}

.arrow {
    position: absolute;
    right: 40rpx;
    top: 50%;
    transform: translateY(-50%);
    color: #ccc;
    font-size: 36rpx;
}
</style>