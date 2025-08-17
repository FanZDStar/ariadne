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
                <view v-for="item in historyList" :key="item.id" class="history-item" @click="viewHistoryDetail(item)">
                    <view class="item-header">
                        <text class="item-title">{{ getPreviewText(item.content) }}</text>
                        <text class="item-time">{{ formatTime(item.created_at) }}</text>
                    </view>
                    <text class="item-content">{{ item.content }}</text>
                </view>

                <view v-if="historyList.length === 0" class="empty">
                    暂无对话历史
                </view>
            </scroll-view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            activeTab: 'self-dialog',
            tabs: [
                { type: 'self-dialog', name: '自我对话' },
                { type: 'love-experiment', name: '恋爱尝试' },
                { type: 'love-yourself', name: '爱自己' }
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
            // 这里暂时使用模拟数据，等后端接口完成后替换
            this.historyList = [
                {
                    id: 1,
                    type: this.activeTab,
                    content: "今天和喜欢的人说话时很紧张，不知道该怎么办",
                    created_at: "2023-05-15T10:30:00"
                },
                {
                    id: 2,
                    type: this.activeTab,
                    content: "感觉自己在感情中总是没有安全感",
                    created_at: "2023-05-14T15:45:00"
                }
            ]
        },

        getPreviewText(content) {
            return content.length > 30 ? content.substring(0, 30) + '...' : content
        },

        formatTime(time) {
            // 简单的时间格式化
            return time.substring(0, 16).replace('T', ' ')
        },

        viewHistoryDetail(item) {
            // 跳转到对应的对话页面并传入历史记录
            const pageMap = {
                'self-dialog': '/pages/self-dialog/self-dialog',
                'love-experiment': '/pages/love-experiment/love-experiment',
                'love-yourself': '/pages/love-yourself/love-yourself'
            }

            uni.navigateTo({
                url: `${pageMap[this.activeTab]}?historyId=${item.id}`
            })
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