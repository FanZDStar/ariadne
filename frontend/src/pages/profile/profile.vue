<!-- <template>
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
</style> -->

<template>
    <view class="profile-container">
        <view class="header">
            <image class="avatar" src="/static/avatar.png"></image>
            <view class="user-info-editable" @click="editNickname">
                <text class="username">{{ userInfo.nickname || '情感小白' }}</text>
                <text class="edit-icon">✏️</text>
            </view>
            <view class="user-desc-editable" @click="editBio">
                <text class="user-desc">{{ userInfo.bio || '情感探索者' }}</text>
                <text class="edit-icon">✏️</text>
            </view>
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
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            userInfo: {
                nickname: '情感小白',
                bio: ''
            }
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
                    // Token可能已过期，清除本地存储并跳转到登录页
                    storage.clearToken();
                    storage.clearUserInfo();
                    uni.redirectTo({
                        url: '/pages/login/login'
                    });
                }
            } else {
                // 没有token，跳转到登录页
                uni.redirectTo({
                    url: '/pages/login/login'
                });
            }
        },

        async editNickname() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }

            uni.showModal({
                title: '修改昵称',
                editable: true,
                placeholderText: '请输入新的昵称（最多6个字符）',
                content: this.userInfo.nickname || '情感小白',
                success: async (res) => {
                    if (res.confirm) {
                        const newNickname = res.content;

                        if (newNickname && newNickname.length > 6) {
                            uni.showToast({
                                title: '昵称最多6个字符',
                                icon: 'none'
                            });
                            return;
                        }

                        try {
                            const updatedUser = await api.updateUserInfo(token, {
                                nickname: newNickname || null
                            });

                            this.userInfo.nickname = updatedUser.nickname;
                            storage.setUserInfo(updatedUser);

                            uni.showToast({
                                title: '昵称修改成功',
                                icon: 'success'
                            });
                        } catch (error) {
                            console.error('修改昵称失败:', error);
                            let errorMsg = '修改失败';
                            if (error.message) {
                                errorMsg = error.message.replace('HTTP 400: ', '');
                            }
                            uni.showToast({
                                title: errorMsg,
                                icon: 'none'
                            });
                        }
                    }
                }
            });
        },

        async editBio() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }

            uni.showModal({
                title: '修改个人简介',
                editable: true,
                placeholderText: '请输入个人简介',
                content: this.userInfo.bio || '',
                success: async (res) => {
                    if (res.confirm) {
                        const newBio = res.content;

                        try {
                            const updatedUser = await api.updateUserInfo(token, {
                                bio: newBio || null
                            });

                            this.userInfo.bio = updatedUser.bio;
                            storage.setUserInfo(updatedUser);

                            uni.showToast({
                                title: '个人简介修改成功',
                                icon: 'success'
                            });
                        } catch (error) {
                            console.error('修改个人简介失败:', error);
                            let errorMsg = '修改失败';
                            if (error.message) {
                                errorMsg = error.message.replace('HTTP 400: ', '');
                            }
                            uni.showToast({
                                title: errorMsg,
                                icon: 'none'
                            });
                        }
                    }
                }
            });
        },

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
                        storage.clearToken();
                        storage.clearUserInfo();
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

.user-info-editable {
    position: relative;
    display: inline-block;
    margin-bottom: 10rpx;
}

.username {
    font-size: 42rpx;
    font-weight: bold;
    color: #333;
    display: block;
}

.user-desc-editable {
    position: relative;
    display: inline-block;
    margin-bottom: 20rpx;
}

.user-desc {
    font-size: 28rpx;
    color: #999;
}

.edit-icon {
    font-size: 24rpx;
    margin-left: 10rpx;
    vertical-align: top;
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