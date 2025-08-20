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
            <view class="menu-item" @click="openSettingsModal">
                <text class="menu-text">信息修改</text>
                <text class="arrow">></text>
            </view>
            <view class="menu-item" @click="goToHistory">
                <text class="menu-text">对话历史</text>
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

        <view class="settings-modal-backdrop" v-if="showSettingsModal" @click.self="closeSettingsModal">
            <view class="modal-content">
                <view v-if="modalView === 'main'">
                    <view class="modal-header">
                        <text class="back-btn" @click="closeSettingsModal">←</text>
                        <text class="modal-title">信息修改</text>
                    </view>
                    <view class="modal-options">
                        <view class="option-item" @click="modalView = 'email'">
                            <text>变更邮箱</text>
                            <text class="arrow">></text>
                        </view>
                        <view class="option-item" @click="modalView = 'password'">
                            <text>修改密码</text>
                            <text class="arrow">></text>
                        </view>
                    </view>
                </view>

                <view v-if="modalView === 'email'">
                    <view class="modal-header">
                        <text class="back-btn" @click="returnToMainModal">←</text>
                        <text class="modal-title">变更邮箱</text>
                    </view>
                    <view class="modal-body">
                        <view class="info-row">
                            <text class="info-label">当前邮箱:</text>
                            <text class="info-value">{{ userInfo.email || '未设置' }}</text>
                        </view>
                        <input class="input" placeholder="请输入新邮箱" v-model="newEmail" @input="validateEmail" />
                        <text v-if="emailError" class="error-text">{{ emailError }}</text>
                        <text v-if="emailSuccessMessage" class="success-text">{{ emailSuccessMessage }}</text>
                        <button class="submit-btn" @click="handleChangeEmail">确定</button>
                    </view>
                </view>

                <view v-if="modalView === 'password'">
                    <view class="modal-header">
                        <text class="back-btn" @click="returnToMainModal">←</text>
                        <text class="modal-title">修改密码</text>
                    </view>
                    <view class="modal-body">
                        <view class="password-input-container">
                            <input class="input" placeholder="请输入旧密码" :password="!showOldPassword"
                                v-model="oldPassword" />
                            <text class="eye-icon" @click="showOldPassword = !showOldPassword">{{ showOldPassword ?
                                '👁️' : '👁️‍🗨️' }}</text>
                        </view>
                        <view class="password-input-container">
                            <input class="input" placeholder="请输入新密码" :password="!showNewPassword" v-model="newPassword"
                                @input="validatePassword" />
                            <text class="eye-icon" @click="showNewPassword = !showNewPassword">{{ showNewPassword ?
                                '👁️' : '👁️‍🗨️' }}</text>
                        </view>
                        <view class="password-input-container">
                            <input class="input" placeholder="请确认新密码" :password="!showConfirmNewPassword"
                                v-model="confirmNewPassword" />
                            <text class="eye-icon" @click="showConfirmNewPassword = !showConfirmNewPassword">{{
                                showConfirmNewPassword ? '👁️' : '👁️‍🗨️' }}</text>
                        </view>
                        <text v-if="passwordError" class="error-text">{{ passwordError }}</text>
                        <text v-if="passwordSuccessMessage" class="success-text">{{ passwordSuccessMessage }}</text>
                        <button class="submit-btn" @click="handleChangePassword">提交</button>
                    </view>
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
            userInfo: {
                nickname: '情感小白',
                bio: '',
                avatar_url: null
            },
            uploadingAvatar: false,
            showSettingsModal: false,
            modalView: 'main', // 'main', 'email', 'password'
            newEmail: '',
            emailError: '',
            emailSuccessMessage: '',
            oldPassword: '',
            newPassword: '',
            confirmNewPassword: '',
            passwordError: '',
            passwordSuccessMessage: '',
            showOldPassword: false,
            showNewPassword: false,
            showConfirmNewPassword: false,
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
                    if (error.statusCode === 401) {
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
                        uni.showToast({
                            title: '获取用户信息失败',
                            icon: 'none'
                        });
                    }
                }
            } else {
                uni.redirectTo({
                    url: '/pages/login/login'
                });
            }
        },

        getUserAvatar() {
            if (this.userInfo.avatar_url) {
                if (this.userInfo.avatar_url.startsWith('http')) {
                    return this.userInfo.avatar_url;
                }
                // const baseUrl = 'http://127.0.0.1:8000';
                const baseUrl = process.env.VUE_APP_API_BASE_URL;
                if (!baseUrl) {
                    console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
                    return '/static/avatar.png'; // 返回默认头像
                }
                if (this.userInfo.avatar_url.startsWith('/')) {
                    return baseUrl + this.userInfo.avatar_url;
                } else {
                    return baseUrl + '/' + this.userInfo.avatar_url;
                }
            }
            return '/static/avatar.png';
        },

        openSettingsModal() {
            this.modalView = 'main';
            this.showSettingsModal = true;
        },

        closeSettingsModal() {
            this.showSettingsModal = false;
            this.clearModalState();
        },

        returnToMainModal() {
            this.modalView = 'main';
            this.clearModalState();
        },

        clearModalState() {
            this.newEmail = '';
            this.emailError = '';
            this.emailSuccessMessage = '';
            this.oldPassword = '';
            this.newPassword = '';
            this.confirmNewPassword = '';
            this.passwordError = '';
            this.passwordSuccessMessage = '';
        },
        validateEmail() {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.newEmail && !regex.test(this.newEmail)) {
                this.emailError = '邮箱格式不正确';
            } else {
                this.emailError = '';
            }
        },

        validatePassword() {
            const regex = /^(((?=.*[a-zA-Z])(?=.*[0-9]))|((?=.*[a-zA-Z])(?=.*[!]))|((?=.*[0-9])(?=.*[!])))[a-zA-Z0-9!]{6,15}$/;
            if (this.newPassword && !regex.test(this.newPassword)) {
                this.passwordError = '新密码必须是6-15位的大小写字母、数字和英文感叹号的两种或以上组合';
            } else {
                this.passwordError = '';
            }
        },

        // async handleChangeEmail() {
        //     this.validateEmail();
        //     if (this.emailError) return;

        //     if (!this.newEmail) {
        //         this.emailError = '请输入新邮箱';
        //         return;
        //     }

        //     const token = storage.getToken();
        //     try {
        //         const updatedUser = await api.updateUserEmail(token, { email: this.newEmail });
        //         this.userInfo.email = updatedUser.email;
        //         storage.setUserInfo(updatedUser);

        //         this.emailSuccessMessage = '邮箱更新成功';

        //         setTimeout(() => {
        //             this.closeSettingsModal();
        //         }, 3000);

        //     } catch (error) {
        //         console.error('更新邮箱失败:', error);
        //         if (error.responseData && error.responseData.detail) {
        //             this.emailError = error.responseData.detail === 'Email already registered' ? '该邮箱已被注册' : error.responseData.detail;
        //         } else {
        //             this.emailError = '更新失败，请稍后重试';
        //         }
        //     }
        // },

        async handleChangeEmail() {
            this.emailError = '';
            this.emailSuccessMessage = '';

            this.validateEmail();
            if (this.emailError) return;

            if (!this.newEmail) {
                this.emailError = '请输入新邮箱';
                return;
            }

            if (this.newEmail === this.userInfo.email) {
                this.emailError = '新邮箱不能与当前邮箱相同';
                return;
            }

            const token = storage.getToken();
            try {
                const updatedUser = await api.updateUserEmail(token, { email: this.newEmail });
                this.userInfo.email = updatedUser.email;
                storage.setUserInfo(updatedUser);
                this.emailSuccessMessage = '邮箱更新成功';
                setTimeout(() => {
                    this.closeSettingsModal();
                }, 3000);
            } catch (error) {
                console.error('更新邮箱失败:', error);
                if (error.responseData && error.responseData.detail) {
                    this.emailError = error.responseData.detail === 'Email already registered' ? '该邮箱已被注册' : error.responseData.detail;
                } else {
                    this.emailError = '更新失败，请稍后重试';
                }
            }
        },

        async handleChangePassword() {
            this.passwordError = '';

            this.validatePassword();
            if (this.passwordError) {
                return;
            }

            if (this.newPassword !== this.confirmNewPassword) {
                this.passwordError = '两次输入的新密码不一致';
                return;
            }

            if (!this.oldPassword || !this.newPassword) {
                this.passwordError = '请输入所有密码字段';
                return;
            }

            const token = storage.getToken();
            try {
                await api.updateUserPassword(token, {
                    old_password: this.oldPassword,
                    new_password: this.newPassword
                });

                this.passwordSuccessMessage = '密码修改成功';

                setTimeout(() => {
                    this.closeSettingsModal();
                }, 3000);

            } catch (error) {
                console.error('修改密码失败:', error);
                if (error.responseData && error.responseData.detail) {
                    this.passwordError = error.responseData.detail;
                } else {
                    this.passwordError = '修改失败，请稍后重试';
                }
            }
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
                        const uploadResult = await api.uploadImage(tempFilePath, token);
                        const updatedUser = await api.updateUserInfo(token, {
                            avatar_url: uploadResult.url
                        });

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

        goToHistory() {
            uni.navigateTo({
                url: '/pages/chat-history/chat-history'
            });
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

.settings-modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background-color: #f8f8f8;
    border-radius: 20rpx;
    width: 85%;
    padding: 40rpx;
    box-sizing: border-box;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 50rpx;
}

.modal-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
}

.back-btn {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    font-size: 40rpx;
    color: #999;
}

.modal-options .option-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx 10rpx;
    border-bottom: 1rpx solid #eee;
}

.modal-body {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
}

.password-input-container {
    display: flex;
    align-items: center;
    background-color: #fff;
    border: 1rpx solid #ddd;
    border-radius: 10rpx;
    padding: 0 20rpx;
}

.input {
    flex: 1;
    height: 80rpx;
    font-size: 28rpx;
    border: none;
    /* Removed individual input border */
    background-color: transparent;
}

.eye-icon {
    padding-left: 10rpx;
}

.submit-btn {
    background-color: #007aff;
    color: white;
    border-radius: 10rpx;
    height: 80rpx;
    line-height: 80rpx;
    margin-top: 20rpx;
}

.error-text {
    color: red;
    font-size: 24rpx;
    margin-top: -15rpx;
    margin-bottom: 5rpx;
}

.success-text {
    color: green;
    font-size: 24rpx;
    margin-top: -15rpx;
    margin-bottom: 5rpx;
}
</style>