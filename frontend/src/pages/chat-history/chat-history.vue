<template>
    <view class="history-container">
        <!-- 渐变头部区域 -->
        <view class="header">
            <view class="header-content">
                <text class="title">💬 对话历史</text>
                <text class="subtitle">{{ getTabDescription(activeTab) }}</text>
            </view>
            <view class="header-decoration">
                <view class="decoration-circle circle-1"></view>
                <view class="decoration-circle circle-2"></view>
                <view class="decoration-circle circle-3"></view>
            </view>
        </view>

        <!-- 优化的选择器 -->
        <view class="selector-container">
            <picker mode="selector" :range="pickerOptions" :value="pickerIndex" @change="onPickerChange"
                range-key="name">
                <view class="picker-display">
                    <view class="picker-content">
                        <view class="picker-icon-wrapper">
                            <text class="picker-icon">{{ getCurrentIcon() }}</text>
                        </view>
                        <view class="picker-text-wrapper">
                            <text :class="['picker-text', activeTab ? 'selected' : 'placeholder']">{{ getCurrentText() }}</text>
                            <text class="picker-hint" v-if="!activeTab">轻触选择对话类型</text>
                        </view>
                    </view>
                    <view class="picker-arrow-wrapper">
                        <text class="picker-arrow">▼</text>
                    </view>
                </view>
            </picker>
        </view>

        <!-- 内容区域 -->
        <view class="content">
            <scroll-view class="history-list" scroll-y="true" enhanced :show-scrollbar="false">
                <view v-for="item in historyList" :key="item.id" class="history-item">
                    <view class="item-content" @click="viewHistoryDetail(item)">
                        <view class="item-header">
                            <view class="title-container">
                                <text class="scene-badge" :style="{ backgroundColor: getSceneColor(item.scene) }">
                                    {{ getSceneIcon(item.scene) }}
                                </text>
                                <text class="item-title">{{ item.title }}</text>
                                <text class="ai-badge" v-if="item.title && item.title.length <= 15">AI</text>
                            </view>
                            <text class="item-time">{{ formatTime(item.created_at) }}</text>
                        </view>
                        <text class="item-preview">{{ getPreviewText(item) }}</text>
                        <view class="item-stats">
                            <text class="stats-item">💬 {{ getMessageCount(item) }}条消息</text>
                            <text class="stats-item" v-if="item.auto_save_enabled">🔄 自动保存</text>
                        </view>
                    </view>
                    <view class="item-actions">
                        <button class="delete-btn" @click.stop="deleteSession(item.id)">删除</button>
                    </view>
                </view>

                <!-- 空状态优化 -->
                <view v-if="historyList.length === 0" class="empty-state">
                    <view class="empty-illustration">
                        <text class="empty-icon">📋</text>
                        <view class="empty-circles">
                            <view class="empty-circle"></view>
                            <view class="empty-circle"></view>
                            <view class="empty-circle"></view>
                        </view>
                    </view>
                    <text class="empty-title">暂无{{ getSceneName(activeTab) }}对话历史</text>
                    <text class="empty-subtitle">开始一段新的对话，记录美好时光</text>
                    <view class="empty-action" v-if="activeTab">
                        <text class="action-hint">💡 选择其他对话类型或开始新对话</text>
                    </view>
                </view>
            </scroll-view>
        </view>
    </view>
</template>

<script>
// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000';

// const BASE_URL = 'http://127.0.0.1:8000';
export default {
    data() {
        return {
            activeTab: 'self-dialog',
            pickerIndex: 0, // 默认选择第一个对话类型（自我对话，索引0）

            tabs: [
                // 基础场景
                { type: 'self-dialog', name: '自我对话', icon: '🌸', description: '深度自我探索与情感反思' },
                { type: 'emotional-growth', name: '情感成长', icon: '💝', description: '探索情感世界，发展情感智慧' },

                // 大学生专区
                { type: 'academic-stress', name: '学业疏导', icon: '📚', description: '缓解学业压力与考试焦虑' },
                { type: 'social-anxiety', name: '社交陪伴', icon: '👥', description: '克服社交障碍，建立人际关系' },
                { type: 'future-planning', name: '规划指导', icon: '🔮', description: '职业探索与人生方向思考' },
                { type: 'life-balance', name: '生活平衡', icon: '⚖️', description: '多维度生活平衡指导' },

                // 关系成长
                { type: 'love-experiment', name: '心语练习', icon: '🧪', description: '恋爱技能训练与表达练习' },
                { type: 'self-love', name: '爱自己', icon: '🌟', description: '建立健康的自我关系' }
            ],
            historyList: []
        }
    },
    computed: {
        pickerOptions() {
            return this.tabs.map(tab => ({
                name: `${tab.icon} ${tab.name}`,
                type: tab.type,
                icon: tab.icon
            }))
        }
    },
    mounted() {
        // 页面加载时自动加载自我对话历史记录
        this.$nextTick(() => {
            this.loadHistory();
        });
    },

    methods: {
        onPickerChange(e) {
            const index = e.detail.value
            this.pickerIndex = index

            // 直接选择对话类型（已移除"请选择"选项）
            const selectedOption = this.pickerOptions[index]
            if (selectedOption) {
                this.activeTab = selectedOption.type
                this.loadHistory()
            }
        },

        getCurrentIcon() {
            if (this.pickerIndex < 0) {
                return '📋'
            }
            const selectedOption = this.pickerOptions[this.pickerIndex]
            return selectedOption ? selectedOption.icon : '📋'
        },

        getCurrentText() {
            const selectedOption = this.pickerOptions[this.pickerIndex]
            if (selectedOption) {
                const tab = this.tabs.find(t => t.type === selectedOption.type)
                return tab ? tab.name : '对话类型'
            }
            return '对话类型'
        },

        switchTab(tabType) {
            this.activeTab = tabType
            this.loadHistory()

            // 设置动态颜色
            this.setTabColors(tabType)
        },

        setTabColors(tabType) {
            const tab = this.tabs.find(t => t.type === tabType)
            if (tab) {
                // 将颜色值转换为CSS变量
                const colorRgb = this.hexToRgb(tab.color)
                document.documentElement.style.setProperty('--tab-color', tab.color)
                document.documentElement.style.setProperty('--tab-color-rgb', colorRgb)
                document.documentElement.style.setProperty('--scene-color', tab.color)
            }
        },

        hexToRgb(hex) {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
            return result ?
                `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` :
                '0, 122, 255'
        },
        
        getTabDescription(tabType) {
            const tab = this.tabs.find(t => t.type === tabType)
            return tab ? tab.description : ''
        },

        getSceneName(scene) {
            const tab = this.tabs.find(t => t.type === scene)
            return tab ? tab.name : ''
        },

        getSceneIcon(scene) {
            const tab = this.tabs.find(t => t.type === scene)
            return tab ? tab.icon : '💭'
        },

        getSceneColor(scene) {
            const colorMap = {
                'self-dialog': '#667eea',
                'emotional-growth': '#E91E63',
                'academic-stress': '#4CAF50',
                'social-anxiety': '#FF9800',
                'future-planning': '#9C27B0',
                'life-balance': '#607D8B',
                'love-experiment': '#2196F3',
                'self-love': '#FF5722'
            }
            return colorMap[scene] || '#999'
        },
        async loadHistory() {
            if (!this.activeTab) {
                return;
            }
            
            try {
                const token = uni.getStorageSync('access_token');
                if (!token) {
                    return;
                }
                
                const response = await uni.request({
                    url: `${BASE_URL}/chat/chat-sessions?scene=${this.activeTab}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.statusCode === 200) {
                    this.historyList = Array.isArray(response.data) ? response.data : [];
                } else {
                    this.historyList = []
                }
            } catch (error) {
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                })
                this.historyList = []
            }
        },
        getBadgeText(badge) {
            const badgeMap = {
                'basic': '基础',
                'college': '大学生',
                'relationship': '关系'
            }
            return badgeMap[badge] || ''
        },

        getSessionDuration(session) {
            if (!session.messages || session.messages.length < 2) {
                return '简短交流'
            }

            const messageCount = session.messages.length
            if (messageCount < 6) {
                return '简短交流'
            } else if (messageCount < 15) {
                return '轻松聊天'
            } else if (messageCount < 30) {
                return '深入对话'
            } else {
                return '深度交流'
            }
        },
        getPreviewText(session) {
            // 获取第一条用户消息作为预览
            const firstUserMessage = session.messages && session.messages.find(msg => msg.role === 'user')
            if (firstUserMessage) {
                return firstUserMessage.content.length > 30 ?
                    firstUserMessage.content.substring(0, 30) + '...' :
                    firstUserMessage.content
            }
            return session.title || '无内容'
        },

        getMessageCount(session) {
            // 统计对话中的实际消息数量
            if (session.messages && Array.isArray(session.messages)) {
                return session.messages.length
            }
            // 如果没有messages数组，使用message_count字段作为后备
            return session.message_count || 0
        },

        formatTime(time) {
            // 格式化时间
            const date = new Date(time)
            const now = new Date()
            const diff = now - date
            const days = Math.floor(diff / (1000 * 60 * 60 * 24))

            if (days === 0) {
                return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
            } else if (days === 1) {
                return '昨天'
            } else if (days < 7) {
                return `${days}天前`
            } else {
                return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
            }
        },

        viewHistoryDetail(item) {
            // 跳转到对应的对话页面并传入历史记录
            const pageMap = {
                'self-dialog': '/pages/self-dialog/self-dialog',
                'emotional-growth': '/pages/emotional-growth/emotional-growth',
                'academic-stress': '/pages/academic-stress/academic-stress',
                'social-anxiety': '/pages/social-anxiety/social-anxiety',
                'future-planning': '/pages/future-planning/future-planning',
                'life-balance': '/pages/life-balance/life-balance',
                'love-experiment': '/pages/love-experiment/love-experiment',
                'self-love': '/pages/love-yourself/love-yourself'
            }

            const targetPage = pageMap[item.scene] || pageMap[this.activeTab]

            if (targetPage) {
                uni.navigateTo({
                    url: `${targetPage}?sessionId=${item.id}`
                })
            } else {
                uni.showToast({
                    title: '页面不存在',
                    icon: 'none'
                })
            }
        },

        getTabDescription(tabType) {
            if (!tabType) {
                return '选择对话类型以查看相应的历史记录'
            }
            const tab = this.tabs.find(t => t.type === tabType)
            return tab ? tab.description : ''
        },
        async deleteSession(sessionId) {
            uni.showModal({
                title: '确认删除',
                content: '确定要删除这个对话记录吗？此操作不可恢复。',
                success: async (res) => {
                    if (res.confirm) {
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
            })
        }
    }
}
</script>

<style scoped>
.history-container {
    min-height: 100vh;
    background: linear-gradient(180deg, #faf8f3 0%, #ffffff 100%);
    position: relative;
    overflow: hidden;
}

/* 顶部装饰背景 */
.history-container::before {
    content: '';
    position: absolute;
    top: -150rpx;
    left: -100rpx;
    right: -100rpx;
    height: 500rpx;
    background: linear-gradient(135deg, #d4c5a0 0%, #e8dcc0 50%, #f5f0e8 100%);
    border-radius: 0 0 60% 40%;
    opacity: 0.3;
    z-index: 0;
}

/* 头部样式 */
.header {
    position: relative;
    padding: 80rpx 40rpx 40rpx;
    overflow: hidden;
    z-index: 1;
}

.header-content {
    text-align: center;
    position: relative;
    z-index: 2;
}

.title {
    font-size: 56rpx;
    font-weight: 700;
    color: #8b6914;
    text-shadow: 0 2rpx 8rpx rgba(139, 105, 20, 0.1);
    display: block;
    margin-bottom: 18rpx;
    letter-spacing: 3rpx;
}

.subtitle {
    font-size: 28rpx;
    color: #a67c52;
    line-height: 1.6;
    opacity: 0.9;
    font-weight: 400;
}

.header-decoration {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 1;
}

.decoration-circle {
    position: absolute;
    border-radius: 50%;
    background: rgba(139, 105, 20, 0.08);
}

.circle-1 {
    width: 120rpx;
    height: 120rpx;
    top: 20rpx;
    left: 50rpx;
    background: rgba(212, 197, 160, 0.1);
}

.circle-2 {
    width: 80rpx;
    height: 80rpx;
    top: 140rpx;
    right: 80rpx;
    background: rgba(166, 124, 82, 0.08);
}

.circle-3 {
    width: 60rpx;
    height: 60rpx;
    top: 60rpx;
    right: 180rpx;
    background: rgba(245, 241, 232, 0.1);
}

/* 选择器样式 */
.selector-container {
    padding: 0 40rpx 30rpx;
    position: relative;
    z-index: 1;
}

.picker-display {
    background: linear-gradient(135deg, #fff9f0 0%, #fdf6ed 100%);
    border-radius: 28rpx;
    padding: 24rpx 32rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10rpx);
    border: 2rpx solid #f0ead6;
    box-shadow: 
        0 8rpx 32rpx rgba(139, 105, 20, 0.08),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
    transition: all 0.3s ease;
}

.picker-display:active {
    transform: scale(0.98);
    box-shadow: 
        0 4rpx 16rpx rgba(139, 105, 20, 0.12),
        inset 0 1rpx 0 rgba(255, 255, 255, 0.6);
}

.picker-content {
    display: flex;
    align-items: center;
    flex: 1;
}

.picker-icon-wrapper {
    width: 60rpx;
    height: 60rpx;
    border-radius: 16rpx;
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 24rpx;
    box-shadow: 0 4rpx 16rpx rgba(33, 150, 243, 0.2);
    border: 2rpx solid rgba(255, 255, 255, 0.4);
}

.picker-icon {
    font-size: 28rpx;
    color: #1976d2;
}

.picker-text-wrapper {
    flex: 1;
}

.picker-text {
    font-size: 32rpx;
    font-weight: 600;
    color: #8b6914;
    display: block;
    margin-bottom: 4rpx;
    letter-spacing: 1rpx;
}

.picker-text.selected {
    color: #8b6914;
}

.picker-text.placeholder {
    color: #a67c52;
    opacity: 0.7;
}

.picker-hint {
    font-size: 24rpx;
    color: #a67c52;
    opacity: 0.7;
}

.picker-arrow-wrapper {
    display: flex;
    align-items: center;
    margin-left: 20rpx;
}

.picker-arrow {
    font-size: 24rpx;
    color: #d4c5a0;
    transform: rotate(0deg);
    transition: transform 0.3s ease;
}

.picker-display:active .picker-arrow {
    transform: rotate(180deg);
}

/* 内容区域 */
.content {
    flex: 1;
    padding: 0 40rpx 40rpx;
    min-height: 60vh;
    position: relative;
    z-index: 1;
}

.history-list {
    height: 100%;
}

.history-item {
    margin-bottom: 28rpx;
    border-radius: 32rpx;
    overflow: hidden;
    background: linear-gradient(135deg, #fffef8 0%, #faf7f0 50%, #f5f1e8 100%);
    backdrop-filter: blur(10rpx);
    border: 2rpx solid #f0ead6;
    box-shadow: 
        0 12rpx 40rpx rgba(139, 105, 20, 0.12),
        0 4rpx 16rpx rgba(139, 105, 20, 0.08);
    transition: all 0.3s ease;
    position: relative;
}

.history-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg,
            rgba(255, 248, 220, 0.4) 0%,
            rgba(250, 245, 220, 0.2) 50%,
            rgba(245, 241, 232, 0.4) 100%);
    border-radius: 32rpx;
    z-index: 0;
}

.history-item:active {
    transform: translateY(6rpx);
    box-shadow: 
        0 8rpx 25rpx rgba(139, 105, 20, 0.15),
        0 2rpx 8rpx rgba(139, 105, 20, 0.1);
}

.item-content {
    padding: 36rpx;
    position: relative;
    z-index: 1;
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20rpx;
}

.title-container {
    display: flex;
    align-items: center;
    flex: 1;
    margin-right: 20rpx;
}

.scene-badge {
    width: 48rpx;
    height: 48rpx;
    border-radius: 12rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;
    color: white;
    font-weight: bold;
    margin-right: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.item-title {
    font-size: 34rpx;
    font-weight: 600;
    color: #8b6914;
    flex: 1;
    line-height: 1.4;
    margin-right: 16rpx;
    letter-spacing: 1rpx;
}

.ai-badge {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    color: #1976d2;
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 22rpx;
    font-weight: 600;
    box-shadow: 0 4rpx 12rpx rgba(33, 150, 243, 0.2);
    border: 2rpx solid rgba(255, 255, 255, 0.4);
}

.item-time {
    font-size: 24rpx;
    color: #a67c52;
    white-space: nowrap;
    opacity: 0.8;
}

.item-preview {
    font-size: 26rpx;
    color: #a67c52;
    line-height: 1.6;
    margin-bottom: 16rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    opacity: 0.9;
}

.item-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stats-group {
    display: flex;
    align-items: center;
    gap: 32rpx;
}

.stat-item {
    display: flex;
    align-items: center;
    font-size: 24rpx;
    color: #a67c52;
    opacity: 0.8;
}

.stat-icon {
    font-size: 28rpx;
    margin-right: 8rpx;
}

.action-group {
    display: flex;
    gap: 16rpx;
}

.action-btn {
    padding: 10rpx 24rpx;
    border-radius: 20rpx;
    font-size: 24rpx;
    font-weight: 500;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
    backdrop-filter: blur(10rpx);
}

.btn-edit {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    color: #f57c00;
    border: 2rpx solid rgba(245, 124, 0, 0.2);
    box-shadow: 0 4rpx 12rpx rgba(245, 124, 0, 0.15);
}

.btn-edit:active {
    background: linear-gradient(135deg, #ffcc02 0%, #ff9800 100%);
    color: white;
    border-color: rgba(255, 152, 0, 0.3);
}

.btn-delete {
    background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
    color: #e91e63;
    border: 2rpx solid rgba(233, 30, 99, 0.2);
    box-shadow: 0 4rpx 12rpx rgba(233, 30, 99, 0.15);
}

.btn-delete:active {
    background: linear-gradient(135deg, #f06292 0%, #e91e63 100%);
    color: white;
    border-color: rgba(233, 30, 99, 0.3);
}

.stats-item {
    font-size: 22rpx;
    color: #a67c52;
    margin-right: 15rpx;
    opacity: 0.8;
}

/* 操作按钮优化 */
.item-actions {
    position: absolute;
    top: 20rpx;
    right: 20rpx;
    z-index: 2;
}

.delete-btn {
    background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
    color: #e91e63;
    border: 2rpx solid rgba(233, 30, 99, 0.2);
    border-radius: 20rpx;
    padding: 8rpx 20rpx;
    font-size: 22rpx;
    font-weight: 500;
    box-shadow: 0 4rpx 12rpx rgba(233, 30, 99, 0.15);
    transition: all 0.3s ease;
}

.delete-btn:active {
    background: linear-gradient(135deg, #f06292 0%, #e91e63 100%);
    color: white;
    border-color: rgba(233, 30, 99, 0.3);
    transform: scale(0.95);
}

/* 空状态 */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 400rpx;
    text-align: center;
    margin-top: 100rpx;
}

.empty-illustration {
    position: relative;
    margin-bottom: 40rpx;
    display: inline-block;
}

.empty-icon {
    font-size: 120rpx;
    display: block;
    opacity: 0.3;
    color: #d4c5a0;
}

.empty-circles {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.empty-circle {
    position: absolute;
    border: 3rpx solid rgba(212, 197, 160, 0.4);
    border-radius: 50%;
    animation: ripple 2s infinite;
}

.empty-circle:nth-child(1) {
    width: 80rpx;
    height: 80rpx;
    margin: -40rpx;
    animation-delay: 0s;
}

.empty-circle:nth-child(2) {
    width: 120rpx;
    height: 120rpx;
    margin: -60rpx;
    animation-delay: 0.7s;
}

.empty-circle:nth-child(3) {
    width: 160rpx;
    height: 160rpx;
    margin: -80rpx;
    animation-delay: 1.4s;
}

@keyframes ripple {
    0% { transform: scale(0.3); opacity: 0.8; }
    100% { transform: scale(1); opacity: 0; }
}

.empty-title {
    font-size: 36rpx;
    font-weight: 600;
    color: #8b6914;
    margin-bottom: 16rpx;
    letter-spacing: 1rpx;
}

.empty-subtitle {
    font-size: 28rpx;
    color: #a67c52;
    line-height: 1.6;
    margin-bottom: 32rpx;
    opacity: 0.8;
}

.empty-action {
    background: linear-gradient(135deg, rgba(212, 197, 160, 0.1), rgba(245, 241, 232, 0.1));
    border: 2rpx solid rgba(212, 197, 160, 0.3);
    border-radius: 16rpx;
    padding: 20rpx;
    margin-top: 20rpx;
}

.action-hint {
    font-size: 26rpx;
    color: #d4c5a0;
    font-weight: 500;
}

/* 加载状态 */
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200rpx;
}

.loading-spinner {
    width: 60rpx;
    height: 60rpx;
    border: 6rpx solid rgba(139, 105, 20, 0.2);
    border-top: 6rpx solid #8b6914;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

/* 底部装饰 */
.history-container::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 200rpx;
    background: linear-gradient(135deg, rgba(212, 197, 160, 0.1) 0%, rgba(245, 241, 232, 0.1) 100%);
    border-radius: 50% 50% 0 0;
    pointer-events: none;
    z-index: 0;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .header {
        padding: 60rpx 30rpx 30rpx;
    }

    .title {
        font-size: 48rpx;
        letter-spacing: 2rpx;
    }

    .subtitle {
        font-size: 26rpx;
    }

    .content {
        padding: 0 30rpx 30rpx;
    }

    .selector-container {
        padding: 0 30rpx 24rpx;
    }

    .history-item {
        margin-bottom: 24rpx;
    }

    .item-content {
        padding: 32rpx;
    }

    .item-title {
        font-size: 30rpx;
    }

    .item-preview {
        font-size: 24rpx;
    }

    .stats-group {
        gap: 24rpx;
    }
}

/* 大屏幕适配 */
@media (min-width: 1200rpx) {
    .content {
        max-width: 900rpx;
        margin: 0 auto;
    }

    .header {
        max-width: 900rpx;
        margin: 0 auto;
    }

    .selector-container {
        max-width: 900rpx;
        margin: 0 auto;
        padding: 0 40rpx 30rpx;
    }
}
</style>