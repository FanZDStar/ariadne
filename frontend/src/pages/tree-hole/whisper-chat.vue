<template>
    <view class="chat-container">
        <view class="whisper-header-note">
            <scroll-view scroll-y="true" class="header-scroll">
                <text class="header-content">{{ originalWhisper.content }}</text>
            </scroll-view>
        </view>

        <scroll-view scroll-y class="chat-messages-scroll" :scroll-top="scrollTop" scroll-with-animation>
            <view class="scroll-content">
                <view v-for="(message, index) in messages" :key="index" class="message-row"
                    :class="message.user_id === selfId ? 'self' : 'other'">
                    <image v-if="message.user_id !== selfId" class="avatar" :src="getAvatar(message.user_id)" />
                    <view class="message-bubble">
                        <text class="message-text">{{ message.content }}</text>
                    </view>
                    <image v-if="message.user_id === selfId" class="avatar" :src="getAvatar(message.user_id)" />
                </view>
            </view>
        </scroll-view>

        <view class="chat-input-area">
            <input class="input-field" v-model="newMessage" placeholder="说点什么吧..." @confirm="sendMessage"
                confirm-type="send" cursor-spacing="20" />
            <button class="send-button" @click="sendMessage" :disabled="!newMessage.trim()">发送</button>
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
    data() {
        return {
            whisper_id: null,
            originalWhisper: {},
            messages: [],
            newMessage: '',
            selfId: null,
            participants: {},
            scrollTop: 0
        };
    },
    onLoad(options) {
        this.whisper_id = options.whisper_id;
        const userInfo = storage.getUserInfo();
        this.selfId = userInfo ? userInfo.user_id : null;
        this.fetchWhisperDetails();
        this.fetchChatHistory();
    },
    methods: {
        getAvatar(userId) {
            if (this.participants[userId]) {
                return this.participants[userId].anonymous_avatar;
            }
            return '/static/avatar.png'; // Fallback avatar
        },
        async fetchWhisperDetails() {
            const token = storage.getToken();
            if (!token) return;
            this.originalWhisper = await api.getWhisperDetails(token, this.whisper_id);
        },
        async fetchChatHistory() {
            const token = storage.getToken();
            if (!token) return;
            this.messages = await api.getWhisperChatHistory(token, this.whisper_id);
            this.scrollToBottom();
        },
        async sendMessage() {
            if (!this.newMessage.trim()) return;
            const token = storage.getToken();
            if (!token) return;

            try {
                await api.sendWhisperChatMessage(token, this.whisper_id, this.newMessage);
                this.newMessage = '';
                this.fetchChatHistory(); // Refresh messages
            } catch (error) {
                console.error("Failed to send message:", error);
                uni.showToast({
                    title: '发送失败',
                    icon: 'none'
                });
            }
        },
        scrollToBottom() {
            this.$nextTick(() => {
                // A large value to scroll to the bottom
                this.scrollTop = 999999;
            });
        }
    }
};
</script>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f4f4f4;
}

.whisper-header-note {
    flex-shrink: 0;
    max-height: 20vh;
    /* Max 1/5 screen height */
    background-color: #fffbe8;
    margin: 20rpx;
    padding: 25rpx;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.08);
    border: 1rpx solid #eee9d5;
}

.header-scroll {
    max-height: calc(20vh - 50rpx);
    /* Adjust based on padding */
}

.header-content {
    font-size: 28rpx;
    color: #6c6c6c;
    line-height: 1.6;
}

.chat-messages-scroll {
    flex: 1;
    width: 100%;
    overflow-y: auto;
}

.scroll-content {
    padding: 20rpx;
    padding-bottom: 40rpx;
    /* Extra space at the bottom */
}

.message-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 30rpx;
    width: 100%;
}

/* My messages on the right */
.message-row.self {
    justify-content: flex-end;
}

/* Other's messages on the left */
.message-row.other {
    justify-content: flex-start;
}

.avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    flex-shrink: 0;
}

.message-bubble {
    max-width: calc(100% - 180rpx);
    padding: 20rpx 25rpx;
    border-radius: 16rpx;
    word-wrap: break-word;
    word-break: break-all;
}

.message-row.self .message-bubble {
    margin-right: 20rpx;
    background-color: #a2d2ff;
    /* Blue bubble for me */
    border-top-right-radius: 0;
}

.message-row.other .message-bubble {
    margin-left: 20rpx;
    background-color: #ffffff;
    /* White bubble for other */
    border: 1rpx solid #e8e8e8;
    border-top-left-radius: 0;
}

.message-text {
    font-size: 30rpx;
    line-height: 1.5;
    color: #333;
}

.chat-input-area {
    display: flex;
    align-items: center;
    padding: 20rpx;
    padding-bottom: calc(20rpx + constant(safe-area-inset-bottom));
    padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
    background-color: #f9f9f9;
    border-top: 1rpx solid #e0e0e0;
    flex-shrink: 0;
}

.input-field {
    flex: 1;
    height: 70rpx;
    background-color: #fff;
    border: 1rpx solid #ddd;
    border-radius: 35rpx;
    padding: 0 30rpx;
    font-size: 28rpx;
}

.send-button {
    background-color: #007aff;
    color: white;
    border-radius: 35rpx;
    font-size: 28rpx;
    margin-left: 20rpx;
    padding: 0 40rpx;
    height: 70rpx;
    line-height: 70rpx;
}

.send-button[disabled] {
    background-color: #a0cfff;
    color: #e0e0e0;
}
</style>