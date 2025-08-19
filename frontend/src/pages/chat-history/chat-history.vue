<template>
    <view class="history-container">
        <view class="header">
            <text class="title">对话历史</text>
        </view>

        <view class="tabs">
            <view v-for="tab in tabs" :key="tab.type" :class="['tab', activeTab === tab.type ? 'active' : '']"
                @click="switchTab(tab.type)">
                {{ tab.name }}
            </view>
        </view>

        <view class="content">
            <scroll-view class="history-list" scroll-y="true">
                <view v-for="item in historyList" :key="item.id" class="history-item">
                    <view class="item-content" @click="viewHistoryDetail(item)">
                        <view class="item-header">
                            <text class="item-title">{{ item.title }}</text>
                            <text class="item-time">{{ formatTime(item.created_at) }}</text>
                        </view>
                        <text class="item-preview">{{ getPreviewText(item) }}</text>
                    </view>
                    <view class="item-actions">
                        <button class="delete-btn" @click="deleteSession(item.id)">删除</button>
                    </view>
                </view>

                <view v-if="historyList.length === 0" class="empty">
                    暂无对话历史
                </view>
            </scroll-view>
        </view>
    </view>
</template>

<script>
// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL || 'https://ariadne.nuyoahming.xyz';

export default {
    data() {
        return {
            activeTab: 'self-dialog',
            tabs: [
                { type: 'self-dialog', name: '自我对话' },
                { type: 'love-experiment', name: '恋爱尝试' },
                { type: 'self-love', name: '爱自己' }
            ],
            historyList: []
        }
    },

    mounted() {
        this.loadHistory()
    },

    methods: {
        switchTab(tabType) {
            this.activeTab = tabType
            this.loadHistory()
        },

        async loadHistory() {
            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat/chat-sessions?scene=${this.activeTab}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.historyList = response.data
                } else {
                    console.error('加载历史记录失败:', response)
                    this.historyList = []
                }
            } catch (error) {
                console.error('加载历史记录失败:', error)
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                })
                this.historyList = []
            }
        },

        getPreviewText(session) {
            // 获取第一条用户消息作为预览
            const firstUserMessage = session.messages.find(msg => msg.role === 'user')
            if (firstUserMessage) {
                return firstUserMessage.content.length > 30 ? 
                    firstUserMessage.content.substring(0, 30) + '...' : 
                    firstUserMessage.content
            }
            return session.title || '无内容'
        },

        formatTime(time) {
            // 格式化时间
            const date = new Date(time)
            return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }).replace(/\//g, '-')
        },

        viewHistoryDetail(item) {
            // 跳转到对应的对话页面并传入历史记录
            const pageMap = {
                'self-dialog': '/pages/self-dialog/self-dialog',
                'love-experiment': '/pages/love-experiment/love-experiment',
                'self-love': '/pages/love-yourself/love-yourself'
            }
            
            uni.navigateTo({
                url: `${pageMap[this.activeTab]}?sessionId=${item.id}`
            })
        },

        async deleteSession(sessionId) {
            try {
                const response = await uni.request({
                    url: `${BASE_URL}/chat/chat-sessions/${sessionId}`,
                    method: 'DELETE',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    uni.showToast({
                        title: '删除成功',
                        icon: 'success'
                    })
                    // 重新加载历史记录
                    this.loadHistory()
                } else {
                    uni.showToast({
                        title: '删除失败',
                        icon: 'none'
                    })
                }
            } catch (error) {
                console.error('删除失败:', error)
                uni.showToast({
                    title: '删除失败',
                    icon: 'none'
                })
            }
        }
    }
}
</script>

<style scoped>
.history-container {
    padding: 30rpx;
    background-color: #f8f8f8;
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
}

.title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
}

.tabs {
    display: flex;
    background: #fff;
    border-radius: 10rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.05);
}

.tab {
    flex: 1;
    text-align: center;
    padding: 20rpx 0;
    font-size: 28rpx;
    color: #999;
}

.tab.active {
    color: #007aff;
    border-bottom: 4rpx solid #007aff;
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.history-list {
    flex: 1;
}

.history-item {
    background: #fff;
    border-radius: 10rpx;
    padding: 20rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.05);
}

.item-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10rpx;
}

.item-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
}

.item-time {
    font-size: 24rpx;
    color: #999;
}

.item-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
}

.empty {
    text-align: center;
    color: #999;
    font-size: 28rpx;
    margin-top: 100rpx;
}
</style>