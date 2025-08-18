<template>
    <view class="listen-container">
        <view class="content-wrapper">
            <view v-if="whisper" class="whisper-note">
                <view class="whisper-header">
                    <image class="avatar" :src="whisper.user.avatar_url || '/static/avatar.png'" mode="aspectFill" />
                    <text class="nickname">{{ whisper.user.nickname || '匿名用户' }}</text>
                </view>

                <scroll-view scroll-y="true" class="whisper-scroll-view">
                    <text class="whisper-content">{{ whisper.content }}</text>
                </scroll-view>
            </view>

            <view v-else class="empty-state">
                <text class="empty-text">暂时没有新的悄悄话了，\n不如去写下你的心事吧~</text>
            </view>
        </view>

        <view class="footer-actions">
            <view class="action-bubble like-bubble" @click="toggleLike">
                <text class="action-icon">{{ liked ? '❤️' : '🤍' }}</text>
                <text class="action-text">{{ likeCount }}</text>
            </view>
            <view class="action-bubble comment-bubble" @click="goToChat">
                <text class="action-icon">💬</text>
                <text class="action-text">评论</text>
            </view>
            <button class="next-button" @click="fetchRandomWhisper">换一个</button>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            whisper: null,
            liked: false,
            likeCount: 0
        };
    },
    onLoad() {
        this.fetchRandomWhisper();
    },
    methods: {
        async fetchRandomWhisper() {
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }
            try {
                const whisper = await api.getRandomWhisper(token);
                this.whisper = whisper;
                this.likeCount = whisper.like_count;
                this.liked = whisper.liked;
            } catch (error) {
                this.whisper = null; // 清空旧数据
                console.error('Failed to fetch random whisper:', error);
                uni.showToast({
                    title: '暂时没有悄悄话了',
                    icon: 'none'
                });
            }
        },
        async toggleLike() {
            if (!this.whisper) return;
            const token = storage.getToken();
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }
            try {
                await api.likeWhisper(token, this.whisper.whisper_id);
                this.liked = !this.liked;
                this.likeCount += this.liked ? 1 : -1;
            } catch (error) {
                console.error('Failed to toggle like:', error);
            }
        },
        goToChat() {
            if (!this.whisper) return;
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-chat?whisper_id=${this.whisper.whisper_id}`
            });
        }
    }
};
</script>

<style scoped>
.listen-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f4f4f4;
    overflow: hidden;
}

.content-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40rpx;
    padding-bottom: 200rpx;
    /* 为底部按钮留出空间 */
}

.whisper-note {
    display: flex;
    flex-direction: column;
    width: 80%;
    max-width: 600rpx;
    height: 70vh;
    max-height: 1000rpx;
    background-color: #fffbe8;
    /* 淡黄色，像便签纸 */
    border-radius: 20rpx;
    padding: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.1);
    border: 1rpx solid #eee;
}

.whisper-header {
    display: flex;
    align-items: center;
    margin-bottom: 30rpx;
    flex-shrink: 0;
}

.avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    margin-right: 20rpx;
    border: 2rpx solid #fff;
}

.nickname {
    font-weight: bold;
    font-size: 32rpx;
    color: #555;
}

.whisper-scroll-view {
    flex: 1;
    height: 100%;
    /* 必须设置高度才能在小程序中滚动 */
}

.whisper-content {
    font-size: 30rpx;
    color: #333;
    line-height: 1.8;
}

.empty-state {
    text-align: center;
    color: #888;
}

.empty-text {
    font-size: 30rpx;
    line-height: 1.6;
}

.footer-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 30rpx;
    padding-bottom: calc(30rpx + constant(safe-area-inset-bottom));
    padding-bottom: calc(30rpx + env(safe-area-inset-bottom));
    background-color: #f4f4f4;
    border-top: 1rpx solid #e0e0e0;
}

.action-bubble {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15rpx 30rpx;
    border-radius: 40rpx;
    background-color: #fff;
    box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.08);
}

.action-icon {
    font-size: 40rpx;
    margin-right: 15rpx;
}

.action-text {
    font-size: 28rpx;
    color: #333;
}

.next-button {
    background-color: #007aff;
    color: white;
    border-radius: 40rpx;
    font-size: 28rpx;
    padding: 0 40rpx;
    height: 80rpx;
    line-height: 80rpx;
}
</style>