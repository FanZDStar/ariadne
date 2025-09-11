<template>
    <view class="history-container">
        <view class="header">
            <text class="title">💬 对话历史</text>
            <text class="subtitle">{{ getTabDescription(activeTab) }}</text>
        </view>

        <view class="selector-container">
            <picker mode="selector" :range="pickerOptions" :value="pickerIndex" @change="onPickerChange"
                range-key="name">
                <view class="picker-display">
                    <view class="picker-content">
                        <text class="picker-icon">{{ getCurrentIcon() }}</text>
                        <text :class="['picker-text', activeTab ? 'selected' : 'placeholder']">{{ getCurrentText()
                            }}</text>
                    </view>
                    <text class="picker-arrow">▼</text>
                </view>
            </picker>
        </view>

        <view class="content">
            <scroll-view class="history-list" scroll-y="true">
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
                            <text class="stats-item">💬 {{ item.message_count || 0 }}条消息</text>
                            <text class="stats-item" v-if="item.auto_save_enabled">🔄 自动保存</text>
                        </view>
                    </view>
                    <view class="item-actions">
                        <button class="delete-btn" @click.stop="deleteSession(item.id)">删除</button>
                    </view>
                </view>

                <view v-if="historyList.length === 0" class="empty">
                    <text class="empty-icon">📋</text>
                    <text class="empty-text">暂无{{ getSceneName(activeTab) }}对话历史</text>
                    <text class="empty-hint">开始一段新的对话吧</text>
                </view>
            </scroll-view>
        </view>
    </view>
</template>

<script>
// 使用环境变量的API基础地址
const BASE_URL = process.env.VUE_APP_API_BASE_URL;
console.log('当前环境变量 VUE_APP_API_BASE_URL:', process.env.VUE_APP_API_BASE_URL);
console.log('实际使用的 BASE_URL:', BASE_URL);

// 检查环境变量是否正确配置
if (!BASE_URL) {
    console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
    throw new Error('API基础地址未配置，请检查环境变量 VUE_APP_API_BASE_URL');
}

// const BASE_URL = 'http://127.0.0.1:8000';
export default {
    data() {
        return {
            activeTab: '',
            pickerIndex: 0, // 默认选择第一个选项（默认提示）

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
            return [
                { name: '请选择你要查看的对话历史类型', type: '', icon: '📋' },
                ...this.tabs.map(tab => ({
                    name: `${tab.icon} ${tab.name}`,
                    type: tab.type,
                    icon: tab.icon
                }))
            ]
        }
    },
    mounted() {
        // 不自动加载历史记录，等待用户选择
        // this.loadHistory()
    },

    methods: {
        onPickerChange(e) {
            const index = e.detail.value
            this.pickerIndex = index

            if (index === 0) {
                // 选择了默认选项，清空历史列表
                this.activeTab = ''
                this.historyList = []
            } else {
                // 选择了具体的对话类型
                const selectedOption = this.pickerOptions[index]
                this.activeTab = selectedOption.type
                this.loadHistory()
            }
        },

        getCurrentIcon() {
            if (this.pickerIndex <= 0) {
                return '📋'
            }
            const selectedOption = this.pickerOptions[this.pickerIndex]
            return selectedOption.icon || '📋'
        },

        getCurrentText() {
            if (this.pickerIndex === 0 || !this.activeTab) {
                return '请选择你要查看的对话历史类型'
            }
            const selectedOption = this.pickerOptions[this.pickerIndex]
            const tab = this.tabs.find(t => t.type === selectedOption.type)
            return tab ? tab.name : '请选择对话类型'
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
                return '短对话'
            }

            const messageCount = session.messages.length
            if (messageCount < 10) {
                return '短对话'
            } else if (messageCount < 30) {
                return '中等对话'
            } else {
                return '深度对话'
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
    padding: 30rpx;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}

.header {
    margin-bottom: 30rpx;
    text-align: center;
}

.title {
    font-size: 42rpx;
    font-weight: bold;
    color: #fff;
    display: block;
    margin-bottom: 8rpx;
}

.subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
    display: block;
}

/* 下拉框选择器样式 */
.selector-container {
    margin-bottom: 30rpx;
}

.picker-display {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20rpx;
    padding: 25rpx 30rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(10rpx);
    border: 2rpx solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8rpx 25rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.picker-display:active {
    transform: scale(0.98);
    background: rgba(255, 255, 255, 1);
}

.picker-content {
    display: flex;
    align-items: center;
    flex: 1;
}

.picker-icon {
    font-size: 32rpx;
    margin-right: 15rpx;
}

.picker-text {
    font-size: 30rpx;
    color: #333;
    font-weight: 500;
}

.picker-arrow {
    font-size: 24rpx;
    color: #666;
    transform: rotate(0deg);
    transition: transform 0.3s ease;
}

.picker-display:active .picker-arrow {
    transform: rotate(180deg);
}

.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 25rpx;
    padding: 20rpx;
}

.history-list {
    flex: 1;
}

.history-item {
    background: #fff;
    border-radius: 15rpx;
    padding: 25rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 8rpx 25rpx rgba(0, 0, 0, 0.08);
    border: 1rpx solid rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.history-item:active {
    transform: scale(0.98);
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12rpx;
}

.title-container {
    display: flex;
    align-items: center;
    flex: 1;
    margin-right: 20rpx;
}

.scene-badge {
    color: white;
    font-size: 20rpx;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
    margin-right: 10rpx;
    font-weight: 500;
    min-width: 35rpx;
    text-align: center;
}

.item-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #333;
    margin-right: 10rpx;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.ai-badge {
    background: linear-gradient(45deg, #007aff, #5856d6);
    color: white;
    font-size: 18rpx;
    padding: 3rpx 8rpx;
    border-radius: 10rpx;
    font-weight: 500;
}

.item-time {
    font-size: 24rpx;
    color: #999;
    white-space: nowrap;
}

.item-preview {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 12rpx;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
}

.item-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15rpx;
}

.stats-item {
    font-size: 22rpx;
    color: #999;
    margin-right: 15rpx;
}

.item-actions {
    display: flex;
    justify-content: flex-end;
}

.delete-btn {
    background: #ff4757;
    color: white;
    border: none;
    border-radius: 15rpx;
    padding: 8rpx 20rpx;
    font-size: 24rpx;
    transition: all 0.3s ease;
}

.delete-btn:active {
    background: #ff3742;
    transform: scale(0.95);
}

.empty {
    text-align: center;
    margin-top: 100rpx;
    padding: 40rpx;
}

.empty-icon {
    font-size: 80rpx;
    display: block;
    margin-bottom: 20rpx;
    opacity: 0.5;
}

.empty-text {
    color: #666;
    font-size: 32rpx;
    font-weight: 500;
    display: block;
    margin-bottom: 10rpx;
}

.empty-hint {
    color: #999;
    font-size: 26rpx;
    display: block;
}

.picker-text {
    font-size: 30rpx;
    font-weight: 500;
    transition: color 0.3s ease;
}

.picker-text.placeholder {
    color: #999;
    font-style: italic;
}

.picker-text.selected {
    color: #333;
    font-style: normal;
}
</style>