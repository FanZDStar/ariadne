<!-- <template>
    <view class="listen-whisper-container">
        <view v-if="whisper" class="whisper-card">
            <view class="whisper-header">
                <image class="avatar" :src="whisper.user.avatar_url || '/static/avatar.png'" />
                <text class="nickname">{{ whisper.user.nickname || '匿名用户' }}</text>
            </view>
            <text class="whisper-content">{{ whisper.content }}</text>
            <view class="whisper-footer">
                <view class="action-bubble" @click="toggleLike">
                    <text>{{ liked ? '❤️' : '🤍' }} {{ likeCount }}</text>
                </view>
                <view class="action-bubble" @click="goToChat">
                    <text>💬 评论</text>
                </view>
            </view>
        </view>
        <view v-else class="empty-state">
            <text>暂时没有新的悄悄话了</text>
        </view>
        <button @click="fetchRandomWhisper">换一个</button>
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
                // ... (handle not logged in)
                return;
            }
            try {
                this.whisper = await api.getRandomWhisper(token);
                this.likeCount = this.whisper.like_count;
                // You'll need an endpoint to check if the current user has liked this whisper
                this.liked = this.whisper.liked;
            } catch (error) {
                console.error('Failed to fetch random whisper:', error);
            }
        },
        async toggleLike() {
            const token = storage.getToken();
            if (!token) {
                // ...
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
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-chat?whisper_id=${this.whisper.whisper_id}`
            });
        }
    }
};
</script>

<style scoped>
.listen-whisper-container {
    padding: 20px;
}

.whisper-card {
    background: #fff;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.whisper-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
}

.nickname {
    font-weight: bold;
}

.whisper-content {
    margin-bottom: 15px;
    display: block;
}

.whisper-footer {
    display: flex;
    justify-content: space-around;
}

.action-bubble {
    background: #f0f0f0;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
}

.empty-state {
    text-align: center;
    margin-top: 50px;
    color: #888;
}
</style> -->

<template>
    <view class="listen-whisper-container">
        <view v-if="whisper" class="whisper-card">
            <view class="whisper-header">
                <image class="avatar" :src="whisper.user.avatar_url || '/static/avatar.png'" />
                <text class="nickname">{{ whisper.user.nickname || '匿名用户' }}</text>
            </view>
            <text class="whisper-content">{{ whisper.content }}</text>
            <view class="whisper-footer">
                <view class="action-bubble" @click="toggleLike">
                    <text>{{ liked ? '❤️' : '🤍' }} {{ likeCount }}</text>
                </view>
                <view class="action-bubble" @click="goToChat">
                    <text>💬 评论</text>
                </view>
            </view>
        </view>
        <view v-else class="empty-state">
            <text>暂时没有新的悄悄话了</text>
        </view>
        <button @click="fetchRandomWhisper">换一个</button>
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
                // ... (handle not logged in)
                return;
            }
            try {
                this.whisper = await api.getRandomWhisper(token);
                this.likeCount = this.whisper.like_count;
                this.liked = this.whisper.liked;
            } catch (error) {
                console.error('Failed to fetch random whisper:', error);
            }
        },
        async toggleLike() {
            const token = storage.getToken();
            if (!token) {
                // ...
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
            uni.navigateTo({
                url: `/pages/tree-hole/whisper-chat?whisper_id=${this.whisper.whisper_id}`
            });
        }
    }
};
</script>

<style scoped>
.listen-whisper-container {
    padding: 20px;
}

.whisper-card {
    background: #fff;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.whisper-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
}

.nickname {
    font-weight: bold;
}

.whisper-content {
    margin-bottom: 15px;
    display: block;
}

.whisper-footer {
    display: flex;
    justify-content: space-around;
}

.action-bubble {
    background: #f0f0f0;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
}

.empty-state {
    text-align: center;
    margin-top: 50px;
    color: #888;
}
</style>