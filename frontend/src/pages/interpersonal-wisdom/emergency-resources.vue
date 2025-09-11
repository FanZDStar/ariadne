<template>
    <view class="emergency-container">
        <view class="header">
            <text class="title">应急资源</text>
            <text class="subtitle">紧急情况下的专业支持与求助渠道</text>
        </view>

        <!-- 紧急状态评估 -->
        <view class="emergency-assessment">
            <view class="assessment-card urgent">
                <view class="assessment-header">
                    <text class="assessment-icon">🆘</text>
                    <text class="assessment-title">紧急情况评估</text>
                </view>
                <text class="assessment-desc">如果你正在经历紧急心理危机，请立即寻求专业帮助</text>
                <view class="assessment-actions">
                    <view class="action-btn emergency" @click="callEmergencyHotline">
                        <text class="btn-text">🚨 紧急求助</text>
                    </view>
                    <view class="action-btn assessment" @click="startCrisisAssessment">
                        <text class="btn-text">📊 危机评估</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 专业热线 -->
        <view class="hotline-section">
            <text class="section-title">📞 专业求助热线</text>
            <view v-for="hotline in hotlines" :key="hotline.id" class="hotline-card" @click="callHotline(hotline)">
                <view class="hotline-info">
                    <text class="hotline-name">{{ hotline.name }}</text>
                    <text class="hotline-desc">{{ hotline.description }}</text>
                    <view class="hotline-details">
                        <text class="hotline-time">⏰ {{ hotline.time }}</text>
                        <text class="hotline-type">{{ hotline.type }}</text>
                    </view>
                </view>
                <view class="hotline-action">
                    <text class="hotline-number">{{ hotline.number }}</text>
                    <text class="call-icon">📞</text>
                </view>
            </view>
        </view>

        <!-- 在线咨询 -->
        <view class="online-section">
            <text class="section-title">💻 在线专业咨询</text>
            <view v-for="service in onlineServices" :key="service.id" class="service-card"
                @click="accessOnlineService(service)">
                <view class="service-header">
                    <text class="service-icon">{{ service.icon }}</text>
                    <view class="service-info">
                        <text class="service-name">{{ service.name }}</text>
                        <text class="service-status" :class="service.status">{{ getStatusText(service.status) }}</text>
                    </view>
                </view>
                <text class="service-desc">{{ service.description }}</text>
                <view class="service-features">
                    <text v-for="feature in service.features" :key="feature" class="feature-tag">
                        {{ feature }}
                    </text>
                </view>
            </view>
        </view>

        <!-- 自助工具 -->
        <view class="tools-section">
            <text class="section-title">🛠️ 心理自助工具</text>
            <view class="tools-grid">
                <view v-for="tool in selfHelpTools" :key="tool.id" class="tool-card" @click="useTool(tool)">
                    <text class="tool-icon">{{ tool.icon }}</text>
                    <text class="tool-name">{{ tool.name }}</text>
                    <text class="tool-desc">{{ tool.description }}</text>
                </view>
            </view>
        </view>

        <!-- 紧急联系人 -->
        <view class="contacts-section">
            <view class="contacts-header">
                <text class="section-title">👥 紧急联系人</text>
                <text class="add-contact" @click="addEmergencyContact">+ 添加</text>
            </view>
            <view v-if="emergencyContacts.length === 0" class="no-contacts">
                <text class="no-contacts-icon">📱</text>
                <text class="no-contacts-text">暂无紧急联系人</text>
                <text class="no-contacts-desc">添加信任的朋友或家人作为紧急联系人</text>
            </view>
            <view v-else class="contacts-list">
                <view v-for="contact in emergencyContacts" :key="contact.id" class="contact-card">
                    <view class="contact-info">
                        <text class="contact-name">{{ contact.name }}</text>
                        <text class="contact-relation">{{ contact.relation }}</text>
                    </view>
                    <view class="contact-actions">
                        <view class="contact-btn call" @click="callContact(contact)">
                            <text class="btn-icon">📞</text>
                        </view>
                        <view class="contact-btn message" @click="messageContact(contact)">
                            <text class="btn-icon">💬</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 安全计划 -->
        <view class="safety-plan">
            <view class="plan-header">
                <text class="section-title">📋 个人安全计划</text>
                <text class="plan-status" :class="{ 'has-plan': hasSafetyPlan }">
                    {{ hasSafetyPlan ? '已制定' : '未制定' }}
                </text>
            </view>
            <view class="plan-card" @click="manageSafetyPlan">
                <text class="plan-icon">🛡️</text>
                <view class="plan-content">
                    <text class="plan-title">{{ hasSafetyPlan ? '查看/编辑安全计划' : '制定个人安全计划' }}</text>
                    <text class="plan-desc">
                        {{ hasSafetyPlan ? '包含个人预警信号、应对策略和求助方式' : '制定个性化的危机应对策略和求助计划' }}
                    </text>
                </view>
                <text class="plan-arrow">→</text>
            </view>
        </view>

        <!-- 资源库 -->
        <view class="resources-section">
            <text class="section-title">📚 心理健康资源</text>
            <view class="resources-tabs">
                <view v-for="tab in resourceTabs" :key="tab.id" class="tab-item"
                    :class="{ active: currentResourceTab === tab.id }" @click="switchResourceTab(tab.id)">
                    <text class="tab-text">{{ tab.name }}</text>
                </view>
            </view>
            <view class="resources-content">
                <view v-for="resource in currentResources" :key="resource.id" class="resource-item"
                    @click="viewResource(resource)">
                    <text class="resource-title">{{ resource.title }}</text>
                    <text class="resource-desc">{{ resource.description }}</text>
                    <view class="resource-meta">
                        <text class="resource-type">{{ resource.type }}</text>
                        <text class="resource-time">{{ resource.readTime }}</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            hotlines: [
                {
                    id: 1,
                    name: '国家心理危机干预热线',
                    number: '400-161-9995',
                    description: '24小时免费心理危机干预服务',
                    time: '24小时',
                    type: '免费'
                },
                {
                    id: 2,
                    name: '北京心理危机研究与干预热线',
                    number: '400-658-9995',
                    description: '专业心理危机干预和情感支持',
                    time: '24小时',
                    type: '免费'
                },
                {
                    id: 3,
                    name: '上海心理援助热线',
                    number: '021-64387250',
                    description: '心理咨询和危机干预服务',
                    time: '9:00-23:00',
                    type: '免费'
                },
                {
                    id: 4,
                    name: '青少年心理健康热线',
                    number: '12355',
                    description: '专门为青少年提供心理支持',
                    time: '9:00-17:00',
                    type: '免费'
                }
            ],
            onlineServices: [
                {
                    id: 1,
                    name: '在线心理咨询',
                    icon: '💭',
                    description: '与专业心理咨询师一对一在线交流',
                    status: 'online',
                    features: ['实时对话', '隐私保护', '专业认证']
                },
                {
                    id: 2,
                    name: '情绪支持聊天室',
                    icon: '🤝',
                    description: '与其他用户分享经历，互相支持',
                    status: 'online',
                    features: ['匿名交流', '同伴支持', '监管安全']
                },
                {
                    id: 3,
                    name: '视频心理咨询',
                    icon: '📹',
                    description: '通过视频与心理专家面对面交流',
                    status: 'busy',
                    features: ['面对面交流', '专业诊断', '预约制']
                }
            ],
            selfHelpTools: [
                {
                    id: 1,
                    name: '呼吸练习',
                    icon: '🫁',
                    description: '缓解焦虑的呼吸技巧'
                },
                {
                    id: 2,
                    name: '情绪记录',
                    icon: '📝',
                    description: '追踪和分析情绪变化'
                },
                {
                    id: 3,
                    name: '冥想指导',
                    icon: '🧘',
                    description: '正念冥想练习'
                },
                {
                    id: 4,
                    name: '积极思维',
                    icon: '💭',
                    description: '培养积极心态的练习'
                },
                {
                    id: 5,
                    name: '睡眠助手',
                    icon: '😴',
                    description: '改善睡眠质量的工具'
                },
                {
                    id: 6,
                    name: '压力测试',
                    icon: '📊',
                    description: '评估当前压力水平'
                }
            ],
            emergencyContacts: [],
            hasSafetyPlan: false,
            currentResourceTab: 'articles',
            resourceTabs: [
                { id: 'articles', name: '文章' },
                { id: 'videos', name: '视频' },
                { id: 'books', name: '书籍' },
                { id: 'apps', name: '应用' }
            ],
            resources: {
                articles: [
                    {
                        id: 1,
                        title: '如何识别抑郁症的早期信号',
                        description: '了解抑郁症的常见症状和求助方式',
                        type: '科普文章',
                        readTime: '5分钟'
                    },
                    {
                        id: 2,
                        title: '应对焦虑的实用方法',
                        description: '学习有效缓解焦虑情绪的技巧',
                        type: '实用指南',
                        readTime: '8分钟'
                    }
                ],
                videos: [
                    {
                        id: 1,
                        title: '正念冥想入门教程',
                        description: '跟随专家学习基础的冥想技巧',
                        type: '教学视频',
                        readTime: '15分钟'
                    }
                ],
                books: [
                    {
                        id: 1,
                        title: '《感受的治愈力》',
                        description: '了解情绪的本质和调节方法',
                        type: '心理学著作',
                        readTime: '推荐阅读'
                    }
                ],
                apps: [
                    {
                        id: 1,
                        title: 'Headspace',
                        description: '专业的冥想和正念练习应用',
                        type: '冥想应用',
                        readTime: '免费试用'
                    }
                ]
            }
        }
    },

    computed: {
        currentResources() {
            return this.resources[this.currentResourceTab] || [];
        }
    },

    onLoad() {
        this.loadEmergencyContacts();
        this.checkSafetyPlan();
    },

    methods: {
        callEmergencyHotline() {
            uni.showModal({
                title: '紧急求助',
                content: '将拨打国家心理危机干预热线：400-161-9995\n\n24小时免费服务，请放心拨打。',
                confirmText: '立即拨打',
                cancelText: '取消',
                success: (res) => {
                    if (res.confirm) {
                        uni.makePhoneCall({
                            phoneNumber: '400-161-9995'
                        });
                    }
                }
            });
        },

        startCrisisAssessment() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/crisis-assessment'
            });
        },

        callHotline(hotline) {
            uni.showActionSheet({
                itemList: ['拨打电话', '查看详情', '收藏热线'],
                success: (res) => {
                    switch (res.tapIndex) {
                        case 0:
                            uni.makePhoneCall({
                                phoneNumber: hotline.number
                            });
                            break;
                        case 1:
                            this.showHotlineDetails(hotline);
                            break;
                        case 2:
                            this.favoriteHotline(hotline);
                            break;
                    }
                }
            });
        },

        showHotlineDetails(hotline) {
            uni.showModal({
                title: hotline.name,
                content: `电话：${hotline.number}\n服务时间：${hotline.time}\n费用：${hotline.type}\n\n${hotline.description}`,
                showCancel: false,
                confirmText: '知道了'
            });
        },

        favoriteHotline(hotline) {
            uni.showToast({
                title: '已收藏热线',
                icon: 'success'
            });
        },

        accessOnlineService(service) {
            if (service.status === 'offline') {
                uni.showToast({
                    title: '服务暂时不可用',
                    icon: 'none'
                });
                return;
            }

            uni.showModal({
                title: service.name,
                content: service.description + '\n\n是否现在开始使用？',
                success: (res) => {
                    if (res.confirm) {
                        // 这里可以跳转到相应的在线服务页面
                        uni.showToast({
                            title: '正在连接服务...',
                            icon: 'loading'
                        });
                    }
                }
            });
        },

        getStatusText(status) {
            const statusMap = {
                'online': '在线',
                'busy': '繁忙',
                'offline': '离线'
            };
            return statusMap[status] || '未知';
        },

        useTool(tool) {
            // 根据工具类型跳转到不同页面
            const toolRoutes = {
                1: '/pages/tools/breathing-exercise',
                2: '/pages/tools/emotion-diary',
                3: '/pages/tools/meditation',
                4: '/pages/tools/positive-thinking',
                5: '/pages/tools/sleep-helper',
                6: '/pages/tools/stress-test'
            };

            const route = toolRoutes[tool.id];
            if (route) {
                uni.navigateTo({
                    url: route
                });
            } else {
                uni.showToast({
                    title: '功能开发中',
                    icon: 'none'
                });
            }
        },

        addEmergencyContact() {
            uni.navigateTo({
                url: '/pages/emergency/add-contact'
            });
        },

        loadEmergencyContacts() {
            const contacts = uni.getStorageSync('emergencyContacts') || [];
            this.emergencyContacts = contacts;
        },

        callContact(contact) {
            uni.makePhoneCall({
                phoneNumber: contact.phone
            });
        },

        messageContact(contact) {
            uni.showModal({
                title: '发送消息',
                content: `向 ${contact.name} 发送求助消息？\n\n"我现在需要帮助，能联系我吗？"`,
                success: (res) => {
                    if (res.confirm) {
                        // 这里可以集成短信API或其他消息服务
                        uni.showToast({
                            title: '消息已发送',
                            icon: 'success'
                        });
                    }
                }
            });
        },

        checkSafetyPlan() {
            const plan = uni.getStorageSync('safetyPlan');
            this.hasSafetyPlan = !!plan;
        },

        manageSafetyPlan() {
            uni.navigateTo({
                url: '/pages/emergency/safety-plan'
            });
        },

        switchResourceTab(tabId) {
            this.currentResourceTab = tabId;
        },

        viewResource(resource) {
            uni.navigateTo({
                url: `/pages/resources/resource-detail?id=${resource.id}&type=${this.currentResourceTab}`
            });
        }
    }
}
</script>

<style scoped>
.emergency-container {
    padding: 0;
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    padding: 60rpx 40rpx 40rpx;
    color: white;
    text-align: center;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
    margin-bottom: 16rpx;
    display: block;
}

.subtitle {
    font-size: 28rpx;
    opacity: 0.9;
}

.emergency-assessment {
    padding: 40rpx;
}

.assessment-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.assessment-card.urgent {
    border: 2rpx solid #ff6b6b;
    background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
}

.assessment-header {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
}

.assessment-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.assessment-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.assessment-desc {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 32rpx;
    line-height: 1.6;
}

.assessment-actions {
    display: flex;
    gap: 20rpx;
}

.action-btn {
    flex: 1;
    padding: 24rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 26rpx;
    font-weight: bold;
}

.action-btn.emergency {
    background-color: #ff6b6b;
    color: white;
}

.action-btn.assessment {
    background-color: #f0f0f0;
    color: #666;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    padding: 0 40rpx;
    display: block;
}

.hotline-section {
    margin-bottom: 40rpx;
}

.hotline-card {
    background-color: white;
    margin: 0 40rpx 16rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.hotline-card:active {
    transform: translateY(2rpx);
}

.hotline-info {
    flex: 1;
}

.hotline-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.hotline-desc {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 12rpx;
    display: block;
}

.hotline-details {
    display: flex;
    gap: 20rpx;
}

.hotline-time {
    font-size: 22rpx;
    color: #999;
}

.hotline-type {
    font-size: 22rpx;
    color: #52c41a;
    background-color: #f6ffed;
    padding: 4rpx 8rpx;
    border-radius: 8rpx;
}

.hotline-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;
}

.hotline-number {
    font-size: 24rpx;
    font-weight: bold;
    color: #ff6b6b;
}

.call-icon {
    font-size: 32rpx;
}

.online-section {
    margin-bottom: 40rpx;
}

.service-card {
    background-color: white;
    margin: 0 40rpx 16rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.service-header {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
}

.service-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.service-info {
    flex: 1;
}

.service-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 4rpx;
    display: block;
}

.service-status {
    font-size: 22rpx;
    padding: 4rpx 12rpx;
    border-radius: 12rpx;
}

.service-status.online {
    background-color: #f6ffed;
    color: #52c41a;
}

.service-status.busy {
    background-color: #fff7e6;
    color: #fa8c16;
}

.service-status.offline {
    background-color: #f5f5f5;
    color: #999;
}

.service-desc {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 16rpx;
    line-height: 1.6;
}

.service-features {
    display: flex;
    gap: 12rpx;
    flex-wrap: wrap;
}

.feature-tag {
    font-size: 20rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.tools-section {
    margin-bottom: 40rpx;
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
    padding: 0 40rpx;
}

.tool-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx 24rpx;
    text-align: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.tool-card:active {
    transform: scale(0.98);
}

.tool-icon {
    font-size: 48rpx;
    margin-bottom: 16rpx;
    display: block;
}

.tool-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.tool-desc {
    font-size: 22rpx;
    color: #666;
    line-height: 1.4;
}

.contacts-section {
    margin-bottom: 40rpx;
}

.contacts-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40rpx;
    margin-bottom: 24rpx;
}

.add-contact {
    font-size: 26rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 12rpx 20rpx;
    border-radius: 20rpx;
}

.no-contacts {
    background-color: white;
    margin: 0 40rpx;
    border-radius: 16rpx;
    padding: 60rpx 32rpx;
    text-align: center;
}

.no-contacts-icon {
    font-size: 80rpx;
    margin-bottom: 20rpx;
    display: block;
    opacity: 0.5;
}

.no-contacts-text {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.no-contacts-desc {
    font-size: 24rpx;
    color: #666;
}

.contact-card {
    background-color: white;
    margin: 0 40rpx 16rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.contact-info {
    flex: 1;
}

.contact-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.contact-relation {
    font-size: 24rpx;
    color: #666;
}

.contact-actions {
    display: flex;
    gap: 12rpx;
}

.contact-btn {
    width: 64rpx;
    height: 64rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
}

.contact-btn.call {
    background-color: #52c41a;
    color: white;
}

.contact-btn.message {
    background-color: #1890ff;
    color: white;
}

.safety-plan {
    margin-bottom: 40rpx;
}

.plan-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40rpx;
    margin-bottom: 24rpx;
}

.plan-status {
    font-size: 22rpx;
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
    background-color: #f5f5f5;
    color: #999;
}

.plan-status.has-plan {
    background-color: #f6ffed;
    color: #52c41a;
}

.plan-card {
    background-color: white;
    margin: 0 40rpx;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    align-items: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.plan-icon {
    font-size: 48rpx;
    margin-right: 24rpx;
}

.plan-content {
    flex: 1;
}

.plan-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.plan-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
}

.plan-arrow {
    font-size: 32rpx;
    color: #ccc;
}

.resources-section {
    margin-bottom: 40rpx;
}

.resources-tabs {
    display: flex;
    padding: 0 40rpx;
    margin-bottom: 24rpx;
    gap: 8rpx;
}


.tab-item {
    flex: 1;
    padding: 16rpx;
    text-align: center;
    background-color: #f8f9fa;
    border-radius: 12rpx;
    transition: all 0.3s ease;
}

.tab-item.active {
    background-color: #667eea;
    color: white;
}

.tab-text {
    font-size: 26rpx;
    color: #666;
}

.tab-item.active .tab-text {
    color: white;
    font-weight: bold;
}

.resources-content {
    padding: 0 40rpx;
}

.resource-item {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.resource-item:active {
    transform: translateY(2rpx);
}

.resource-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
    line-height: 1.4;
}

.resource-desc {
    font-size: 26rpx;
    color: #666;
    margin-bottom: 16rpx;
    line-height: 1.6;
}

.resource-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.resource-type {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.resource-time {
    font-size: 22rpx;
    color: #999;
}

.btn-text {
    font-size: inherit;
    color: inherit;
}

.btn-icon {
    font-size: inherit;
    color: inherit;
}

/* 动画效果 */
.assessment-card {
    animation: bounceIn 0.6s ease-out;
}

.hotline-card,
.service-card {
    animation: fadeInUp 0.5s ease-out;
}

.tool-card {
    animation: zoomIn 0.4s ease-out;
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.8) translateY(-20rpx);
    }

    50% {
        transform: scale(1.05) translateY(0);
    }

    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes zoomIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* 紧急状态高亮效果 */
.action-btn.emergency {
    position: relative;
    overflow: hidden;
}

.action-btn.emergency::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.5s;
}

.action-btn.emergency:active::before {
    left: 100%;
}

/* 热线卡片悬停效果 */
.hotline-card {
    border-left: 4rpx solid transparent;
    transition: all 0.3s ease;
}

.hotline-card:hover {
    border-left-color: #ff6b6b;
    box-shadow: 0 8rpx 24rpx rgba(255, 107, 107, 0.2);
}

/* 服务状态指示器 */
.service-status {
    position: relative;
}

.service-status.online::before {
    content: '';
    position: absolute;
    left: -16rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 8rpx;
    height: 8rpx;
    border-radius: 50%;
    background-color: #52c41a;
    animation: pulse 2s infinite;
}

.service-status.busy::before {
    content: '';
    position: absolute;
    left: -16rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 8rpx;
    height: 8rpx;
    border-radius: 50%;
    background-color: #fa8c16;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(82, 196, 26, 0.7);
    }

    70% {
        box-shadow: 0 0 0 10rpx rgba(82, 196, 26, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(82, 196, 26, 0);
    }
}

/* 工具网格布局优化 */
@media (max-width: 750rpx) {
    .tools-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12rpx;
    }

    .tool-card {
        padding: 24rpx 16rpx;
    }

    .tool-icon {
        font-size: 40rpx;
    }
}

@media (max-width: 480rpx) {
    .assessment-actions {
        flex-direction: column;
        gap: 16rpx;
    }

    .action-btn {
        width: 100%;
    }

    .hotline-card {
        flex-direction: column;
        text-align: center;
        gap: 20rpx;
    }

    .hotline-info {
        text-align: center;
    }

    .resources-tabs {
        flex-wrap: wrap;
        gap: 8rpx;
    }

    .tab-item {
        min-width: 120rpx;
    }
}

/* 紧急联系人按钮样式增强 */
.contact-btn {
    transition: all 0.3s ease;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.contact-btn:active {
    transform: scale(0.95);
    box-shadow: 0 1rpx 4rpx rgba(0, 0, 0, 0.2);
}

.contact-btn.call:active {
    background-color: #389e0d;
}

.contact-btn.message:active {
    background-color: #096dd9;
}

/* 安全计划卡片增强 */
.plan-card {
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
}

.plan-card:active {
    border-color: #667eea;
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.2);
    transform: translateY(-2rpx);
}

/* 资源标签样式优化 */
.feature-tag {
    transition: all 0.3s ease;
}

.service-card:active .feature-tag {
    background-color: #667eea;
    color: white;
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6rpx;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb {
    background: #ff6b6b;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb:hover {
    background: #ee5a6f;
}

/* 焦点状态 */
.action-btn:focus,
.tab-item:focus {
    outline: 2rpx solid #667eea;
    outline-offset: 2rpx;
}

/* 无障碍访问增强 */
.hotline-card[aria-pressed="true"] {
    background-color: #f0f4ff;
    border-color: #667eea;
}

/* 文字选择样式 */
::selection {
    background-color: rgba(255, 107, 107, 0.3);
    color: #333;
}

/* 长按效果 */
.hotline-card:active {
    transform: translateY(2rpx) scale(0.98);
}

.service-card:active {
    transform: translateY(2rpx) scale(0.98);
}

/* 加载状态 */
.emergency-container[data-loading="true"] {
    pointer-events: none;
    opacity: 0.8;
}

/* 错误状态 */
.service-card[data-error="true"] {
    background-color: #fff2f0;
    border: 1rpx solid #ffccc7;
}

.service-card[data-error="true"] .service-name {
    color: #cf1322;
}

/* 成功状态 */
.contact-card[data-success="true"] {
    background-color: #f6ffed;
    border: 1rpx solid #d9f7be;
}

/* 危险状态高亮 */
.assessment-card.urgent {
    animation: urgentPulse 2s infinite;
}

@keyframes urgentPulse {

    0%,
    100% {
        box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    }

    50% {
        box-shadow: 0 8rpx 24rpx rgba(255, 107, 107, 0.3);
    }
}

/* 底部安全间距 */
.emergency-container {
    padding-bottom: env(safe-area-inset-bottom);
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
    .action-btn.emergency {
        border: 2rpx solid #000;
    }

    .hotline-card,
    .service-card,
    .tool-card {
        border: 1rpx solid #333;
    }
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>