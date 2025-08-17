<template>
    <view class="profile-container">
        <view class="header">
            <view class="avatar-container" @click="changeAvatar">
                <image class="avatar" :src="getUserAvatar()" mode="aspectFill"></image>
                <view class="camera-icon">📷</view>
            </view>
            <view class="user-info-container">
                <text class="username" @click="editNickname">{{ userInfo.nickname || '情感小白' }}</text>
            </view>
            <view class="user-desc-container">
                <text class="user-desc" @click="editBio">{{ userInfo.bio || '情感探索者' }}</text>
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

        <!-- 上传头像的加载提示 -->
        <view class="loading-mask" v-if="uploadingAvatar">
            <view class="loading-content">
                <view class="loading-spinner"></view>
                <text class="loading-text">上传中...</text>
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
                bio: '',
                avatar_url: null
            },
            uploadingAvatar: false
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
                    // 只有在确定是认证错误时才清除token并跳转
                    if (error.statusCode === 401) {
                        // Token已过期或无效，清除本地存储并跳转到登录页
                        storage.clearToken();
                        storage.clearUserInfo();
                        uni.showToast({
                            title: '登录已过期，请重新登录',
                            icon: 'none',
                            duration: 2000
                        });
                        setTimeout(() => {
                            uni.redirectTo({
                                url: '/pages/login/login'
                            });
                        }, 2000);
                    } else {
                        // 其他错误（如网络问题）只显示提示，不跳转
                        uni.showToast({
                            title: '获取用户信息失败',
                            icon: 'none'
                        });
                    }
                }
            } else {
                // 没有token，跳转到登录页
                uni.redirectTo({
                    url: '/pages/login/login'
                });
            }
        },

        getUserAvatar() {
            if (this.userInfo.avatar_url) {
                // 如果头像URL是完整URL，直接使用
                if (this.userInfo.avatar_url.startsWith('http')) {
                    return this.userInfo.avatar_url;
                }
                // 如果是相对路径，拼接基础URL
                const baseUrl = 'http://127.0.0.1:8000';
                if (this.userInfo.avatar_url.startsWith('/')) {
                    return baseUrl + this.userInfo.avatar_url;
                } else {
                    return baseUrl + '/' + this.userInfo.avatar_url;
                }
            }
            // 默认头像
            return '/static/avatar.png';
        },

        changeAvatar() {
            uni.chooseImage({
                count: 1,
                sizeType: ['compressed'],
                sourceType: ['album', 'camera'],
                success: async (res) => {
                    const tempFilePath = res.tempFilePaths[0];
                    const token = storage.getToken();

                    if (!token) {
                        uni.showToast({
                            title: '请先登录',
                            icon: 'none'
                        });
                        return;
                    }

                    this.uploadingAvatar = true;

                    try {
                        // 上传图片
                        const uploadResult = await api.uploadImage(tempFilePath, token);

                        // 更新用户信息
                        const updatedUser = await api.updateUserInfo(token, {
                            avatar_url: uploadResult.url
                        });

                        // 更新本地用户信息
                        this.userInfo.avatar_url = updatedUser.avatar_url;
                        storage.setUserInfo(updatedUser);

                        uni.showToast({
                            title: '头像更新成功',
                            icon: 'success'
                        });
                    } catch (error) {
                        console.error('头像上传失败:', error);
                        uni.showToast({
                            title: '头像上传失败',
                            icon: 'none'
                        });
                    } finally {
                        this.uploadingAvatar = false;
                    }
                }
            });
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
            uni.navigateTo({
                url: '/pages/chat-history/chat-history'
            });
        },

        goToFavorites() {
            uni.showToast({
                title: '功能开发中',
                icon: 'none'
            })
        },

        goToFeedback() {
            uni.navigateTo({
                url: '/pages/feedback/feedback'
            });
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
    position: relative;
}

.avatar-container {
    position: relative;
    display: inline-block;
    margin-bottom: 30rpx;
}

.avatar {
    width: 150rpx;
    height: 150rpx;
    border-radius: 50%;
}

.camera-icon {
    position: absolute;
    bottom: 0;
    right: 0;
    background-color: #fff;
    border-radius: 50%;
    width: 50rpx;
    height: 50rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.user-info-container {
    margin-bottom: 10rpx;
}

.username {
    font-size: 42rpx;
    font-weight: bold;
    color: #333;
    display: inline-block;
    padding: 15rpx 20rpx;
    border-radius: 10rpx;
}

.username:active {
    background-color: #f0f0f0;
}

.user-desc-container {
    margin-bottom: 20rpx;
}

.user-desc {
    font-size: 28rpx;
    color: #999;
    display: inline-block;
    padding: 15rpx 20rpx;
    border-radius: 10rpx;
}

.user-desc:active {
    background-color: #f0f0f0;
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

.loading-mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.loading-content {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 40rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.loading-spinner {
    width: 50rpx;
    height: 50rpx;
    border: 5rpx solid #f3f3f3;
    border-top: 5rpx solid #007aff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20rpx;
}

.loading-text {
    font-size: 28rpx;
    color: #333;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>