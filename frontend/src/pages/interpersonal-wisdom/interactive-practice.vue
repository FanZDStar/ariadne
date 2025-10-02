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
          <text class="assistant-desc"
            >专业的人际交往技能训练助手，可以与你进行各种场景的对话练习</text
          >
          <view class="assistant-features">
            <text class="feature-item">💬 真实对话模拟</text>
            <text class="feature-item">📊 实时反馈指导</text>
            <text class="feature-item">🎯 个性化练习</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 练习场景选择 -->
    <view v-if="!scenarioSelected" class="practice-scenarios">
      <text class="section-title">🎭 选择练习场景</text>
      <view class="scenarios-grid">
        <view
          v-for="scenario in practiceScenarios"
          :key="scenario.id"
          class="scenario-card"
          :class="{ active: selectedScenario === scenario.id }"
          @click="selectScenario(scenario)"
        >
          <text class="scenario-icon">{{ scenario.icon }}</text>
          <text class="scenario-name">{{ scenario.name }}</text>
          <text class="scenario-desc">{{ scenario.description }}</text>
        </view>
      </view>
    </view>

    <!-- 对话区域 -->
    <view v-if="scenarioSelected" class="chat-container">
      <view class="chat-messages-wrapper">
        <ChatMessages
          ref="chatMessages"
          :messages="chatHistory"
          theme="interpersonal"
          @ai-typing="handleAiTyping"
        />
      </view>

      <!-- 练习控制面板 -->
      <view class="practice-controls">
        <view
          class="control-item"
          :class="{ disabled: isAiTyping }"
          @click="getPracticeHint"
        >
          <text class="control-icon">💡</text>
          <text class="control-text">获取提示</text>
        </view>
        <view
          class="control-item"
          :class="{ disabled: isAiTyping }"
          @click="analyzePractice"
        >
          <text class="control-icon">📊</text>
          <text class="control-text">分析表现</text>
        </view>
        <view
          class="control-item"
          :class="{ disabled: isAiTyping }"
          @click="switchScenario"
        >
          <text class="control-icon">🔄</text>
          <text class="control-text">切换场景</text>
        </view>
      </view>

      <!-- 底部输入框 -->
      <ChatInput
        class="chat-input"
        placeholder="输入您的回复..."
        theme="interpersonal"
        @send="handleSend"
        :disabled="isAiTyping"
      />
    </view>

    <!-- 悬浮保存按钮 -->
    <SaveButton
      v-if="scenarioSelected"
      :can-save="hasNewMessages && chatHistory.length > 1"
      @save="saveChatHistory"
    />
  </view>
</template>

<script>
import chatMixin from "../../utils/chatMixin.js";
import ChatMessages from "../../components/ChatMessages.vue";
import ChatInput from "../../components/ChatInput.vue";
import SaveButton from "../../components/SaveButton.vue";

export default {
  mixins: [chatMixin],

  components: {
    ChatMessages,
    ChatInput,
    SaveButton,
  },

  data() {
    return {
      scene: "interpersonal-practice",
      welcomeMessage:
        "你好！我是小智，你的人际交往练习助手。我们可以进行各种场景的对话练习，帮你提升沟通技巧。请选择一个练习场景开始吧！",
      selectedScenario: null,
      scenarioSelected: false,
      continueSessionId: null, // 用于继续现有会话
      isContinuingSession: false, // 是否正在继续现有会话
      practiceScenarios: [
        {
          id: "self_introduction",
          icon: "👋",
          name: "自我介绍",
          description: "练习在不同场合介绍自己",
        },
        {
          id: "small_talk",
          icon: "💬",
          name: "闲聊技巧",
          description: "学习如何进行轻松的日常对话",
        },
        {
          id: "conflict_resolution",
          icon: "⚖️",
          name: "冲突解决",
          description: "练习处理分歧和冲突的技巧",
        },
        {
          id: "workplace_communication",
          icon: "💼",
          name: "职场沟通",
          description: "提升职场环境下的沟通能力",
        },
        {
          id: "dating_conversation",
          icon: "💕",
          name: "约会对话",
          description: "学习约会和恋爱中的沟通技巧",
        },
        {
          id: "public_speaking",
          icon: "🎤",
          name: "公众表达",
          description: "提升在群体中的表达能力",
        },
      ],
    };
  },

  onLoad(options) {
    // 检查是否是继续现有会话
    if (options.sessionId && options.continue === "true") {
      this.continueSessionId = options.sessionId;
      this.isContinuingSession = true;
      this.loadExistingSession();
    } else if (options.scenario) {
      // 预选场景
      const scenario = this.practiceScenarios.find(
        (s) => s.id === options.scenario
      );
      if (scenario) {
        this.selectScenario(scenario);
      } else {
        this.initWelcomeMessage();
      }
    } else {
      this.initWelcomeMessage();
    }
  },

  methods: {
    initWelcomeMessage() {
      // 设置欢迎消息
      this.chatHistory = [
        {
          role: "assistant",
          content: this.welcomeMessage,
          timestamp: new Date().toISOString(),
        },
      ];
    },

    async loadExistingSession() {
      try {
        const token = uni.getStorageSync("access_token");
        if (!token) {
          uni.showToast({
            title: "请先登录",
            icon: "none",
          });
          return;
        }

        const response = await uni.request({
          url: `${
            process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
          }/interpersonal-practice/sessions/${this.continueSessionId}`,
          method: "GET",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          const sessionData = response.data;

          // 加载现有对话记录
          this.chatHistory = sessionData.messages || [];

          // 设置场景信息
          this.selectedScenario = sessionData.practice_scenario;
          this.scenarioSelected = true;

          // 添加继续对话的提示消息
          this.chatHistory.push({
            role: "assistant",
            content: "欢迎回来！我们可以继续之前的对话练习。你想继续聊什么呢？",
            timestamp: new Date().toISOString(),
          });

          // 标记有新消息，但不需要立即保存
          this.hasNewMessages = false;

          uni.showToast({
            title: "已加载历史对话",
            icon: "success",
          });
        } else {
          throw new Error("加载会话失败");
        }
      } catch (error) {
        console.error("加载现有会话失败:", error);
        uni.showToast({
          title: "加载会话失败",
          icon: "none",
        });
        // 回退到欢迎消息
        this.initWelcomeMessage();
      }
    },
    selectScenario(scenario) {
      this.selectedScenario = scenario.id;
      this.scenarioSelected = true;

      // 发送场景选择消息给AI
      const scenarioMessage = `我想练习${scenario.name}，${scenario.description}。请为我创建一个练习场景。`;
      this.sendMessage(scenarioMessage);
    },

    getPracticeHint() {
      // 防止在AI回复过程中重复发送
      if (this.isAiTyping) {
        uni.showToast({
          title: "AI正在回复中，请稍等",
          icon: "none",
        });
        return;
      }

      if (!this.selectedScenario) {
        uni.showToast({
          title: "请先选择练习场景",
          icon: "none",
        });
        return;
      }

      const hintMessage = "请给我一些在当前对话中可以改进的建议和提示。";
      this.sendMessage(hintMessage);
    },

    analyzePractice() {
      // 防止在AI回复过程中重复发送
      if (this.isAiTyping) {
        uni.showToast({
          title: "AI正在回复中，请稍等",
          icon: "none",
        });
        return;
      }

      if (this.chatHistory.length < 3) {
        uni.showToast({
          title: "对话内容太少，无法分析",
          icon: "none",
        });
        return;
      }

      const analysisMessage =
        "请分析一下我在这次对话练习中的表现，包括优点和需要改进的地方。";
      this.sendMessage(analysisMessage);
    },

    switchScenario() {
      // 防止在AI回复过程中切换场景
      if (this.isAiTyping) {
        uni.showToast({
          title: "AI正在回复中，请稍等",
          icon: "none",
        });
        return;
      }

      uni.showActionSheet({
        itemList: this.practiceScenarios.map((s) => s.name),
        success: (res) => {
          const selectedScenario = this.practiceScenarios[res.tapIndex];
          this.selectScenario(selectedScenario);
        },
      });
    },

    async saveChatHistory() {
      if (!this.selectedScenario || this.chatHistory.length <= 1) {
        uni.showToast({
          title: "没有可保存的对话内容",
          icon: "none",
        });
        return;
      }

      try {
        const token = uni.getStorageSync("access_token");
        if (!token) {
          uni.showToast({
            title: "请先登录",
            icon: "none",
          });
          return;
        }

        // 计算练习时长（从第一条用户消息开始）
        const startTime = new Date(
          this.chatHistory[1]?.timestamp || Date.now()
        );
        const endTime = new Date();
        const practiceSeconds = Math.floor((endTime - startTime) / 1000);

        // 获取选中的场景信息
        const scenario = this.practiceScenarios.find(
          (s) => s.id === this.selectedScenario
        );

        // 准备保存的数据 - 确保数据格式正确
        const sessionData = {
          session_title: `${
            scenario.name
          }练习 - ${new Date().toLocaleDateString()}`,
          practice_scenario: this.selectedScenario,
          practice_scenario_name: scenario.name,
          scenario_description: scenario.description || "",
          messages: this.chatHistory.map((msg, index) => ({
            role: msg.role,
            content: msg.content,
            timestamp: msg.timestamp || new Date().toISOString(),
          })),
          practice_duration: Math.max(practiceSeconds, 0),
          practice_type: "ai_dialog",
          difficulty_level: "beginner",
          completion_status: "completed",
          skills_practiced: [scenario.name],
          strengths: [],
          improvements: [],
          practice_quality_score: null,
          ai_feedback: null,
          is_completed: 0, // 设置为进行中状态，允许继续对话
        };

        console.log("准备发送的数据:", sessionData);

        let response;
        let isUpdate = false;

        // 如果是继续现有会话，使用PUT更新；否则使用POST创建新会话
        if (this.isContinuingSession && this.continueSessionId) {
          response = await uni.request({
            url: `${
              process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
            }/interpersonal-practice/sessions/${this.continueSessionId}`,
            method: "PUT",
            header: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            data: sessionData,
          });
          isUpdate = true;
        } else {
          response = await uni.request({
            url: `${
              process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"
            }/interpersonal-practice/sessions`,
            method: "POST",
            header: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            data: sessionData,
          });

          // 如果是新创建的会话，设置会话ID以便后续更新
          if (response.statusCode === 200 && response.data.id) {
            this.continueSessionId = response.data.id;
            this.isContinuingSession = true;
          }
        }

        if (response.statusCode === 200) {
          uni.showToast({
            title: isUpdate ? "对话已更新" : "对话已保存",
            icon: "success",
          });

          // 重置保存状态
          this.hasNewMessages = false;
        } else {
          console.error("保存失败详情:", {
            statusCode: response.statusCode,
            data: response.data,
            header: response.header,
          });
          throw new Error(
            `保存失败: ${response.statusCode} - ${JSON.stringify(
              response.data
            )}`
          );
        }
      } catch (error) {
        console.error("保存对话失败:", error);
        console.error("发送的数据:", sessionData);
        uni.showToast({
          title: `保存失败: ${error.message || "请重试"}`,
          icon: "none",
          duration: 3000,
        });
      }
    },
  },
};
</script>

<style scoped>
.dialog-container {
  height: 100vh;
  overflow: hidden;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 40rpx 40rpx;
  color: white;
  text-align: center;
  flex-shrink: 0;
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
  flex-shrink: 0;
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
  flex: 1;
  overflow-y: auto;
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

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 0 40rpx;
  background-color: white;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.chat-messages-wrapper {
  flex: 1;
  overflow: hidden;
}

.chat-input {
  flex-shrink: 0;
  border-top: 1rpx solid #e0e0e0;
}

.practice-controls {
  display: flex;
  justify-content: space-around;
  padding: 16rpx 20rpx;
  background-color: #f8f8f8;
  border-top: 1rpx solid #e0e0e0;
  border-bottom: 1rpx solid #e0e0e0;
  flex-shrink: 0;
}

.control-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8rpx 12rpx;
  border-radius: 12rpx;
  transition: all 0.3s ease;
}

.control-item.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.control-item:active:not(.disabled) {
  background-color: #f0f4ff;
  transform: scale(0.95);
}

.control-icon {
  font-size: 28rpx;
  margin-bottom: 4rpx;
}

.control-text {
  font-size: 20rpx;
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
