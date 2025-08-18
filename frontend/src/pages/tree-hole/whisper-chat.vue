<template>
    <view class="chat-container">
        <view class="whisper-header-bar">
            <text>{{ originalWhisper.content }}</text>
        </view>
        <scroll-view scroll-y class="chat-messages">
            <view v-for="(message, index) in messages" :key="index"
                :class="message.is_self ? 'message-self' : 'message-other'">
                <image class="avatar" :src="message.avatar" />
                <view class="message-bubble">
                    <text>{{ message.content }}</text>
                </view>
            </view>
        </scroll-view>
        <view class="chat-input">
            <input v-model="newMessage" placeholder="输入消息..." />
            <button @click="sendMessage">发送</button>
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
            newMessage: ''
        };
    },
    onLoad(options) {
        this.whisper_id = options.whisper_id;
        this.fetchWhisperDetails();
        this.fetchChatHistory();
    },
    methods: {
        async fetchWhisperDetails() {
            const token = storage.getToken();
            this.originalWhisper = await api.getWhisperDetails(token, this.whisper_id);
        },
        async fetchChatHistory() {
            const token = storage.getToken();
            this.messages = await api.getWhisperChatHistory(token, this.whisper_id);
        },
        async sendMessage() {
            if (!this.newMessage.trim()) return;
            const token = storage.getToken();
            await api.sendWhisperChatMessage(token, this.whisper_id, this.newMessage);
            this.newMessage = '';
            this.fetchChatHistory(); // Refresh messages
        }
    }
};
</script>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.whisper-header-bar {
    padding: 10px;
    background-color: #f7f7f7;
    border-bottom: 1px solid #eee;
}

.chat-messages {
    flex: 1;
    padding: 10px;
}

.message-self {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}

.message-other {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.message-bubble {
    max-width: 70%;
    padding: 10px;
    border-radius: 10px;
    margin: 0 10px;
}

.message-self .message-bubble {
    background-color: #dcf8c6;
}

.message-other .message-bubble {
    background-color: #fff;
}

.chat-input {
    display: flex;
    padding: 10px;
    border-top: 1px solid #eee;
}

.chat-input input {
    flex: 1;
    border: 1px solid #ccc;
    border-radius: 20px;
    padding: 5px 10px;
}

.chat-input button {
    margin-left: 10px;
}
</style>