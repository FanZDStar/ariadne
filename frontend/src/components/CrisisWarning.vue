// 心理危机预警前端组件
// file: ariadne/frontend/src/components/CrisisWarning.vue
<template>
    <view class="crisis-warning">
        <!-- 风险评估卡片 -->
        <view class="risk-assessment-card" v-if="riskAssessment">
            <view class="card-header" :class="'risk-' + riskAssessment.risk_level">
                <text class="risk-icon">⚠️</text>
                <text class="risk-title">心理健康评估</text>
                <text class="risk-level">{{ getRiskLevelText(riskAssessment.risk_level) }}</text>
            </view>

            <view class="card-content">
                <view class="risk-score">
                    <text class="score-label">风险评分：</text>
                    <text class="score-value">{{ riskAssessment.score.toFixed(1) }}/100</text>
                </view>

                <view class="reasons" v-if="riskAssessment.reasons.length > 0">
                    <text class="section-title">关注点：</text>
                    <view class="reason-item" v-for="(reason, index) in riskAssessment.reasons" :key="index">
                        <text class="reason-text">• {{ reason }}</text>
                    </view>
                </view>

                <view class="recommendations" v-if="riskAssessment.recommendations.length > 0">
                    <text class="section-title">建议：</text>
                    <view class="recommendation-item" v-for="(rec, index) in riskAssessment.recommendations"
                        :key="index">
                        <text class="recommendation-text">• {{ rec }}</text>
                    </view>
                </view>

                <view class="actions">
                    <button class="action-btn" @click="seekHelp" v-if="isHighRisk">
                        寻求专业帮助
                    </button>
                    <button class="action-btn secondary" @click="refreshAssessment">
                        重新评估
                    </button>
                </view>
            </view>
        </view>

        <!-- 预警历史 -->
        <view class="warnings-history" v-if="showHistory">
            <view class="history-header">
                <text class="history-title">预警记录</text>
                <switch @change="onShowUnresolvedChange" :checked="showUnresolvedOnly">
                    <text class="switch-label">仅未解决</text>
                </switch>
            </view>

            <view class="warning-item" v-for="warning in warnings" :key="warning.warning_id"
                :class="'warning-' + warning.risk_level">
                <view class="warning-header">
                    <text class="warning-title">{{ warning.title }}</text>
                    <text class="warning-time">{{ formatTime(warning.created_at) }}</text>
                </view>

                <text class="warning-description">{{ warning.description }}</text>

                <view class="warning-actions" v-if="!warning.is_resolved">
                    <button class="resolve-btn" @click="resolveWarning(warning.warning_id)">
                        标记为已处理
                    </button>
                </view>
            </view>

            <view class="no-warnings" v-if="warnings.length === 0">
                <text>暂无预警记录</text>
            </view>
        </view>

        <!-- 紧急求助弹窗 -->
        <uni-popup ref="helpPopup" type="center">
            <view class="help-popup">
                <view class="popup-header">
                    <text class="popup-title">寻求帮助</text>
                </view>

                <view class="popup-content">
                    <text class="help-text">如果你正在经历心理困扰，请记住你并不孤单。</text>

                    <view class="help-options">
                        <view class="help-option" @click="callHotline">
                            <text class="option-icon">📞</text>
                            <text class="option-text">心理援助热线</text>
                            <text class="option-number">400-161-9995</text>
                        </view>

                        <view class="help-option" @click="emergencyContact">
                            <text class="option-icon">🚨</text>
                            <text class="option-text">紧急联系</text>
                            <text class="option-number">110/120</text>
                        </view>

                        <view class="help-option" @click="findCounselor">
                            <text class="option-icon">👨‍⚕️</text>
                            <text class="option-text">寻找心理咨询师</text>
                        </view>
                    </view>
                </view>

                <view class="popup-actions">
                    <button class="popup-btn secondary" @click="closeHelpPopup">取消</button>
                    <button class="popup-btn primary" @click="markAsSafe">我现在安全</button>
                </view>
            </view>
        </uni-popup>
    </view>
</template>

<script>
export default {
    name: 'CrisisWarning',
    props: {
        showHistory: {
            type: Boolean,
            default: true
        },
        autoAssess: {
            type: Boolean,
            default: false
        }
    },

    data() {
        return {
            riskAssessment: null,
            warnings: [],
            showUnresolvedOnly: false,
            loading: false
        }
    },

    computed: {
        isHighRisk() {
            return this.riskAssessment &&
                ['high', 'critical'].includes(this.riskAssessment.risk_level)
        }
    },

    mounted() {
        if (this.autoAssess) {
            this.performRiskAssessment()
        }
        if (this.showHistory) {
            this.loadWarnings()
        }
    },

    methods: {
        async performRiskAssessment(days = 14) {
            this.loading = true
            try {
                const response = await uni.request({
                    url: `${this.$apiBase}/crisis/assess-risk?days=${days}`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.riskAssessment = response.data

                    // 如果是高风险，自动显示求助选项
                    if (this.isHighRisk) {
                        this.showHelpDialog()
                    }
                }
            } catch (error) {
                console.error('风险评估失败:', error)
                uni.showToast({
                    title: '评估失败，请稍后重试',
                    icon: 'none'
                })
            } finally {
                this.loading = false
            }
        },

        async loadWarnings() {
            try {
                const response = await uni.request({
                    url: `${this.$apiBase}/crisis/warnings`,
                    method: 'GET',
                    data: {
                        unresolved_only: this.showUnresolvedOnly,
                        days: 30
                    },
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    this.warnings = response.data
                }
            } catch (error) {
                console.error('加载预警记录失败:', error)
            }
        },

        async resolveWarning(warningId) {
            try {
                const response = await uni.request({
                    url: `${this.$apiBase}/crisis/warnings/${warningId}/resolve`,
                    method: 'POST',
                    data: {
                        resolver_notes: '用户标记为已处理'
                    },
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`
                    }
                })

                if (response.statusCode === 200) {
                    uni.showToast({
                        title: '已标记为处理',
                        icon: 'success'
                    })
                    this.loadWarnings() // 重新加载
                }
            } catch (error) {
                console.error('解决预警失败:', error)
                uni.showToast({
                    title: '操作失败',
                    icon: 'none'
                })
            }
        },

        refreshAssessment() {
            this.performRiskAssessment()
        },

        onShowUnresolvedChange(e) {
            this.showUnresolvedOnly = e.detail.value
            this.loadWarnings()
        },

        seekHelp() {
            this.$refs.helpPopup.open()
        },

        showHelpDialog() {
            // 高风险情况下自动显示求助对话框
            setTimeout(() => {
                this.$refs.helpPopup.open()
            }, 1000)
        },

        closeHelpPopup() {
            this.$refs.helpPopup.close()
        },

        callHotline() {
            uni.makePhoneCall({
                phoneNumber: '400-161-9995'
            })
        },

        emergencyContact() {
            uni.showModal({
                title: '紧急联系',
                content: '如果遇到生命危险，请立即拨打110或120',
                confirmText: '拨打110',
                cancelText: '拨打120',
                success: (res) => {
                    if (res.confirm) {
                        uni.makePhoneCall({ phoneNumber: '110' })
                    } else if (res.cancel) {
                        uni.makePhoneCall({ phoneNumber: '120' })
                    }
                }
            })
        },

        findCounselor() {
            // 跳转到心理咨询师查找页面或外部链接
            uni.showToast({
                title: '正在为您查找专业咨询师...',
                icon: 'loading',
                duration: 2000
            })

            // 这里可以集成心理咨询师平台的API
            setTimeout(() => {
                uni.navigateTo({
                    url: '/pages/counselor/list'
                })
            }, 2000)
        },

        markAsSafe() {
            this.closeHelpPopup()
            uni.showToast({
                title: '感谢您的反馈，请保重身体',
                icon: 'none',
                duration: 3000
            })
        },

        getRiskLevelText(level) {
            const levelMap = {
                'low': '低风险',
                'medium': '中等风险',
                'high': '高风险',
                'critical': '紧急风险'
            }
            return levelMap[level] || '未知'
        },

        formatTime(dateString) {
            const date = new Date(dateString)
            return date.toLocaleString('zh-CN')
        }
    }
}
</script>

<style scoped>
.crisis-warning {
    padding: 20rpx;
}

.risk-assessment-card {
    background: white;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    margin-bottom: 24rpx;
    overflow: hidden;
}

.card-header {
    padding: 24rpx;
    display: flex;
    align-items: center;
    gap: 12rpx;
}

.risk-low .card-header {
    background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
}

.risk-medium .card-header {
    background: linear-gradient(135deg, #FFF3E0, #FFD54F);
}

.risk-high .card-header {
    background: linear-gradient(135deg, #FFEBEE, #FFAB91);
}

.risk-critical .card-header {
    background: linear-gradient(135deg, #FFEBEE, #E57373);
}

.risk-icon {
    font-size: 32rpx;
}

.risk-title {
    font-size: 32rpx;
    font-weight: bold;
    flex: 1;
}

.risk-level {
    font-size: 24rpx;
    color: #666;
}

.card-content {
    padding: 24rpx;
}

.risk-score {
    display: flex;
    align-items: center;
    margin-bottom: 24rpx;
}

.score-label {
    font-size: 28rpx;
    color: #666;
}

.score-value {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-left: 12rpx;
}

.section-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.reason-item,
.recommendation-item {
    margin-bottom: 8rpx;
}

.reason-text,
.recommendation-text {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
}

.actions {
    margin-top: 24rpx;
    display: flex;
    gap: 12rpx;
}

.action-btn {
    padding: 16rpx 24rpx;
    border-radius: 8rpx;
    font-size: 26rpx;
    border: none;
}

.action-btn:not(.secondary) {
    background: #FF6B6B;
    color: white;
}

.action-btn.secondary {
    background: #F5F5F5;
    color: #666;
}

.warnings-history {
    background: white;
    border-radius: 16rpx;
    padding: 24rpx;
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
}

.history-title {
    font-size: 32rpx;
    font-weight: bold;
}

.warning-item {
    border-left: 4rpx solid #ddd;
    padding: 16rpx;
    margin-bottom: 16rpx;
    background: #fafafa;
    border-radius: 8rpx;
}

.warning-high {
    border-left-color: #FF9800;
}

.warning-critical {
    border-left-color: #F44336;
}

.warning-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8rpx;
}

.warning-title {
    font-weight: bold;
    font-size: 28rpx;
}

.warning-time {
    font-size: 24rpx;
    color: #999;
}

.warning-description {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 12rpx;
}

.resolve-btn {
    padding: 8rpx 16rpx;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4rpx;
    font-size: 24rpx;
}

.help-popup {
    background: white;
    border-radius: 16rpx;
    width: 600rpx;
    padding: 32rpx;
}

.popup-header {
    text-align: center;
    margin-bottom: 24rpx;
}

.popup-title {
    font-size: 36rpx;
    font-weight: bold;
}

.help-text {
    font-size: 28rpx;
    color: #666;
    text-align: center;
    margin-bottom: 32rpx;
    line-height: 1.6;
}

.help-options {
    margin-bottom: 32rpx;
}

.help-option {
    display: flex;
    align-items: center;
    gap: 16rpx;
    padding: 16rpx;
    margin-bottom: 12rpx;
    background: #f8f9fa;
    border-radius: 8rpx;
}

.option-icon {
    font-size: 32rpx;
}

.option-text {
    flex: 1;
    font-size: 28rpx;
    font-weight: 500;
}

.option-number {
    font-size: 24rpx;
    color: #007AFF;
}

.popup-actions {
    display: flex;
    gap: 12rpx;
}

.popup-btn {
    flex: 1;
    padding: 16rpx;
    border-radius: 8rpx;
    font-size: 28rpx;
    border: none;
}

.popup-btn.primary {
    background: #007AFF;
    color: white;
}

.popup-btn.secondary {
    background: #F5F5F5;
    color: #666;
}
</style>
