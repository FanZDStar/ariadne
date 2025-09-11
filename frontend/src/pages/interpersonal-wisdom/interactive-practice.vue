<template>
    <view class="dialog-container">
        <view class="header">
            <text class="title">AI对话练习</text>
            <text class="subtitle">与AI助手进行人际交往技能练习</text>
        </view>

        <!-- AI助手介绍 -->
        <view class="assistant-intro">
            <view class="intro-card">
                <view class="assistant-avatar">
                    <text class="avatar-emoji">🤖</text>
                    <view class="status-indicator"></view>
                </view>
                <view class="intro-content">
                    <text class="assistant-name">小智导师</text>
                    <text class="assistant-desc">专业的人际交往技能训练助手，可以与你进行各种场景的对话练习</text>
                    <view class="assistant-features">
                        <text class="feature-item">💬 真实对话模拟</text>
                        <text class="feature-item">📊 实时反馈指导</text>
                        <text class="feature-item">🎯 个性化练习</text>
                    </view>
                </view>
            </view>
        </view>

        <!-- 练习场景选择 -->
        <view class="practice-scenarios">
            <text class="section-title">🎭 选择练习场景</text>
            <view class="scenarios-grid">
                <view v-for="scenario in practiceScenarios" :key="scenario.id" class="scenario-card"
                    :class="{ active: selectedScenario === scenario.id }" @click="selectScenario(scenario)">
                    <text class="scenario-icon">{{ scenario.icon }}</text>
                    <text class="scenario-name">{{ scenario.name }}</text>
                    <text class="scenario-desc">{{ scenario.description }}</text>
                </view>
            </view>
        </view>

        <!-- 对话区域 -->
        <view class="chat-section">
            <ChatMessages :messages="chatHistory" :isAiTyping="isAiTyping" @scroll="handleScroll" />

            <ChatInput :disabled="isAiTyping" @send="handleSend" />
        </view>

        <!-- 练习控制面板 -->
        <view class="practice-controls">
            <view class="control-item" @click="getPracticeHint">
                <text class="control-icon">💡</text>
                <text class="control-text">获取提示</text>
            </view>
            <view class="control-item" @click="analyzePractice">
                <text class="control-icon">📊</text>
                <text class="control-text">分析表现</text>
            </view>
            <view class="control-item" @click="switchScenario">
                <text class="control-icon">🔄</text>
                <text class="control-text">切换场景</text>
            </view>
        </view>

        <!-- 保存按钮 -->
        <SaveButton :hasNewMessages="hasNewMessages" @save="saveChatHistory" />
    </view>
</template>

<script>
import chatMixin from '../../utils/chatMixin.js';
import ChatMessages from '../../components/ChatMessages.vue';
import ChatInput from '../../components/ChatInput.vue';
import SaveButton from '../../components/SaveButton.vue';

export default {
    mixins: [chatMixin],

    components: {
        ChatMessages,
        ChatInput,
        SaveButton
    },

    data() {
        return {
            scene: 'interpersonal-practice',
            welcomeMessage: '你好！我是小智，你的人际交往练习助手。我们可以进行各种场景的对话练习，帮你提升沟通技巧。请选择一个练习场景开始吧！',
            selectedScenario: null,
            practiceScenarios: [
                {
                    id: 'self_introduction',
                    icon: '👋',
                    name: '自我介绍',
                    description: '练习在不同场合介绍自己'
                },
                {
                    id: 'small_talk',
                    icon: '💬',
                    name: '闲聊技巧',
                    description: '学习如何进行轻松的日常对话'
                },
                {
                    id: 'conflict_resolution',
                    icon: '⚖️',
                    name: '冲突解决',
                    description: '练习处理分歧和冲突的技巧'
                },
                {
                    id: 'workplace_communication',
                    icon: '💼',
                    name: '职场沟通',
                    description: '提升职场环境下的沟通能力'
                },
                {
                    id: 'dating_conversation',
                    icon: '💕',
                    name: '约会对话',
                    description: '学习约会和恋爱中的沟通技巧'
                },
                {
                    id: 'public_speaking',
                    icon: '🎤',
                    name: '公众表达',
                    description: '提升在群体中的表达能力'
                }
            ]
        }
    },

    onLoad() {
        // 设置欢迎消息
        this.chatHistory = [{
            role: 'assistant',
            content: this.welcomeMessage
        }];
    },

    methods: {
        selectScenario(scenario) {
            this.selectedScenario = scenario.id;

            // 发送场景选择消息给AI
            const scenarioMessage = `我想练习${scenario.name}，${scenario.description}。请为我创建一个练习场景。`;
            this.sendMessage(scenarioMessage);
        },

        getPracticeHint() {
            if (!this.selectedScenario) {
                uni.showToast({
                    title: '请先选择练习场景',
                    icon: 'none'
                });
                return;
            }

            const hintMessage = '请给我一些在当前对话中可以改进的建议和提示。';
            this.sendMessage(hintMessage);
        },

        analyzePractice() {
            if (this.chatHistory.length < 3) {
                uni.showToast({
                    title: '对话内容太少，无法分析',
                    icon: 'none'
                });
                return;
            }

            const analysisMessage = '请分析一下我在这次对话练习中的表现，包括优点和需要改进的地方。';
            this.sendMessage(analysisMessage);
        },

        switchScenario() {
            uni.showActionSheet({
                itemList: this.practiceScenarios.map(s => s.name),
                success: (res) => {
                    const selectedScenario = this.practiceScenarios[res.tapIndex];
                    this.selectScenario(selectedScenario);
                }
            });
        },

        handleScroll(scrollData) {
            // 处理滚动事件
        }
    }
}
</script>

<style scoped>
.dialog-container {
    padding: 0;
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.assistant-intro {
    padding: 40rpx;
}

.intro-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    display: flex;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.assistant-avatar {
    position: relative;
    margin-right: 24rpx;
}

.avatar-emoji {
    font-size: 64rpx;
    display: block;
}

.status-indicator {
    position: absolute;
    bottom: 4rpx;
    right: 4rpx;
    width: 16rpx;
    height: 16rpx;
    background-color: #52c41a;
    border-radius: 50%;
    border: 2rpx solid white;
    animation: pulse 2s infinite;
}

.intro-content {
    flex: 1;
}

.assistant-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 12rpx;
    display: block;
}

.assistant-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 20rpx;
}

.assistant-features {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
}

.feature-item {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.practice-scenarios {
    padding: 0 40rpx 40rpx;
}

.section-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: block;
}

.scenarios-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16rpx;
}

.scenario-card {
    background-color: white;
    border: 2rpx solid #e0e0e0;
    border-radius: 16rpx;
    padding: 24rpx 20rpx;
    text-align: center;
    transition: all 0.3s ease;
}

.scenario-card.active {
    border-color: #667eea;
    background-color: #f0f4ff;
}

.scenario-card:active {
    transform: scale(0.98);
}

.scenario-icon {
    font-size: 40rpx;
    margin-bottom: 12rpx;
    display: block;
}

.scenario-name {
    font-size: 26rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
}

.scenario-desc {
    font-size: 22rpx;
    color: #666;
    line-height: 1.4;
}

.chat-section {
    margin: 0 40rpx;
    background-color: white;
    border-radius: 16rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    min-height: 600rpx;
}

.practice-controls {
    display: flex;
    justify-content: space-around;
    padding: 32rpx 40rpx;
    background-color: white;
    margin: 20rpx 40rpx 0;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.control-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16rpx;
    border-radius: 12rpx;
    transition: all 0.3s ease;
}

.control-item:active {
    background-color: #f0f4ff;
    transform: scale(0.95);
}

.control-icon {
    font-size: 32rpx;
    margin-bottom: 8rpx;
}

.control-text {
    font-size: 22rpx;
    color: #666;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.7;
    }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .scenarios-grid {
        grid-template-columns: 1fr;
    }

    .intro-card {
        flex-direction: column;
        text-align: center;
    }

    .assistant-avatar {
        margin-right: 0;
        margin-bottom: 20rpx;
        align-self: center;
    }
}
</style>