<template>
  <view class="protection-container">
    <view class="header">
      <text class="title">防护技能训练</text>
      <text class="subtitle">识别风险信号，学会自我保护</text>
    </view>

    <!-- 训练模式选择 -->
    <view v-if="currentStage === 'selection'" class="mode-selection">
      <view class="risk-alert">
        <text class="alert-icon">⚠️</text>
        <text class="alert-text">学习识别和应对人际关系中的潜在风险</text>
      </view>

      <view class="training-modes">
        <text class="section-title">🛡️ 选择训练模式</text>
        <view
          v-for="mode in trainingModes"
          :key="mode.id"
          class="mode-card"
          @click="selectMode(mode)"
        >
          <view class="mode-header">
            <text class="mode-icon">{{ mode.icon }}</text>
            <view class="mode-info">
              <text class="mode-title">{{ mode.title }}</text>
              <text class="mode-desc">{{ mode.description }}</text>
            </view>
            <view class="mode-level" :class="'level-' + mode.level">
              <text class="level-text">{{ getLevelText(mode.level) }}</text>
            </view>
          </view>

          <view class="mode-details">
            <view class="mode-stats">
              <view class="stat-item">
                <text class="stat-icon">🎯</text>
                <text class="stat-text">{{ mode.scenarios }}个场景</text>
              </view>
              <view class="stat-item">
                <text class="stat-icon">⏱️</text>
                <text class="stat-text">{{ mode.duration }}</text>
              </view>
            </view>

            <view class="mode-skills">
              <text class="skills-title">训练技能：</text>
              <view class="skills-tags">
                <text
                  v-for="skill in mode.skills"
                  :key="skill"
                  class="skill-tag"
                >
                  {{ skill }}
                </text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 训练简介 -->
    <view v-if="currentStage === 'briefing'" class="briefing-stage">
      <view class="briefing-card">
        <view class="briefing-header">
          <text class="briefing-icon">{{ selectedMode.icon }}</text>
          <view class="briefing-title-area">
            <text class="briefing-title">{{ selectedMode.title }}</text>
            <text class="briefing-subtitle">训练说明</text>
          </view>
        </view>

        <view class="briefing-content">
          <view class="warning-section">
            <text class="warning-icon">🚨</text>
            <text class="warning-title">重要提醒</text>
            <text class="warning-text"
              >这是模拟训练，帮助你在安全环境中学习识别和应对风险。真实情况下如遇到危险，请立即寻求帮助。</text
            >
          </view>

          <view class="training-objectives">
            <text class="section-label">🎯 训练目标</text>
            <view class="objectives-list">
              <text
                v-for="objective in selectedMode.objectives"
                :key="objective"
                class="objective-item"
              >
                • {{ objective }}
              </text>
            </view>
          </view>

          <view class="risk-signals">
            <text class="section-label">⚠️ 重点识别信号</text>
            <view class="signals-list">
              <view
                v-for="signal in selectedMode.riskSignals"
                :key="signal.type"
                class="signal-item"
              >
                <view class="signal-header">
                  <text class="signal-icon">{{ signal.icon }}</text>
                  <text class="signal-type">{{ signal.type }}</text>
                </view>
                <text class="signal-desc">{{ signal.description }}</text>
              </view>
            </view>
          </view>

          <view class="protection-strategies">
            <text class="section-label">🛡️ 保护策略</text>
            <view class="strategies-list">
              <text
                v-for="strategy in selectedMode.strategies"
                :key="strategy"
                class="strategy-item"
              >
                ✓ {{ strategy }}
              </text>
            </view>
          </view>
        </view>

        <view class="briefing-actions">
          <view class="action-btn secondary" @click="backToSelection">
            <text class="btn-text">重新选择</text>
          </view>
          <view class="action-btn primary" @click="startTraining">
            <text class="btn-text">开始训练</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 训练进行中 -->
    <view v-if="currentStage === 'training'" class="training-stage">
      <view class="training-header">
        <view class="progress-info">
          <text class="progress-text"
            >场景 {{ currentScenario }}/{{ totalScenarios }}</text
          >
          <view class="progress-bar">
            <view
              class="progress-fill"
              :style="{ width: (currentScenario / totalScenarios) * 100 + '%' }"
            >
            </view>
          </view>
        </view>
        <view class="training-score">
          <text class="score-icon">🏆</text>
          <text class="score-text">{{ currentScore }}分</text>
        </view>
      </view>

      <view class="scenario-content">
        <view class="scenario-background">
          <text class="scenario-title">{{ currentTrainingStep.title }}</text>
          <text class="scenario-description">{{
            currentTrainingStep.description
          }}</text>
        </view>

        <view class="scenario-dialogue">
          <view
            v-for="message in currentTrainingStep.dialogue"
            :key="message.id"
            class="dialogue-item"
            :class="{
              'risk-message': message.isRisk,
              'normal-message': !message.isRisk,
            }"
          >
            <view class="speaker-info">
              <text class="speaker-name">{{ message.speaker }}</text>
              <text v-if="message.isRisk" class="risk-indicator">⚠️</text>
            </view>
            <text class="dialogue-text">{{ message.text }}</text>
          </view>
        </view>

        <view class="question-section">
          <text class="question-title">{{
            currentTrainingStep.question.title
          }}</text>
          <text class="question-text">{{
            currentTrainingStep.question.text
          }}</text>

          <view class="answer-options">
            <view
              v-for="option in currentTrainingStep.question.options"
              :key="option.id"
              class="option-item"
              @click="selectAnswer(option)"
            >
              <view class="option-header">
                <text class="option-letter">{{
                  String.fromCharCode(65 + option.id - 1)
                }}</text>
                <text class="option-text">{{ option.text }}</text>
              </view>
              <text class="option-desc">{{ option.description }}</text>
            </view>
          </view>
        </view>
      </view>

      <view class="training-controls">
        <view class="control-btn" @click="getHint">
          <text class="control-icon">💡</text>
          <text class="control-text">提示</text>
        </view>
        <view class="control-btn" @click="skipScenario">
          <text class="control-icon">⏭️</text>
          <text class="control-text">跳过</text>
        </view>
        <view class="control-btn" @click="pauseTraining">
          <text class="control-icon">⏸️</text>
          <text class="control-text">暂停</text>
        </view>
      </view>
    </view>

    <!-- 答案反馈 -->
    <view v-if="currentStage === 'feedback'" class="feedback-stage">
      <view class="feedback-card">
        <view class="feedback-header">
          <text class="feedback-icon">{{
            feedbackResult.isCorrect ? "✅" : "❌"
          }}</text>
          <text class="feedback-title">{{
            feedbackResult.isCorrect ? "回答正确！" : "需要改进"
          }}</text>
          <view class="feedback-score">
            <text class="score-gained"
              >+{{ feedbackResult.scoreGained }}分</text
            >
          </view>
        </view>

        <view class="feedback-content">
          <view class="correct-analysis">
            <text class="analysis-title">正确分析：</text>
            <text class="analysis-text">{{
              feedbackResult.correctAnalysis
            }}</text>
          </view>

          <view class="risk-explanation">
            <text class="explanation-title">风险解释：</text>
            <text class="explanation-text">{{
              feedbackResult.riskExplanation
            }}</text>
          </view>

          <view class="protection-advice">
            <text class="advice-title">防护建议：</text>
            <view class="advice-list">
              <text
                v-for="advice in feedbackResult.protectionAdvice"
                :key="advice"
                class="advice-item"
              >
                • {{ advice }}
              </text>
            </view>
          </view>

          <view v-if="!feedbackResult.isCorrect" class="better-choice">
            <text class="better-title">更好的选择：</text>
            <text class="better-text">{{ feedbackResult.betterChoice }}</text>
          </view>
        </view>

        <view class="feedback-actions">
          <view class="feedback-btn primary" @click="nextScenario">
            <text class="btn-text">{{
              currentScenario < totalScenarios ? "下一个场景" : "查看结果"
            }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 训练结果 -->
    <view v-if="currentStage === 'result'" class="result-stage">
      <view class="result-header">
        <text class="result-icon">🏆</text>
        <text class="result-title">训练完成！</text>
        <text class="result-subtitle">{{ selectedMode.title }}</text>
      </view>

      <view class="result-overview">
        <view class="final-score">
          <text class="score-number">{{ finalResult.totalScore }}</text>
          <text class="score-label">总分</text>
          <view
            class="score-level"
            :class="getScoreLevel(finalResult.totalScore)"
          >
            <text class="level-text">{{
              getScoreLevelText(finalResult.totalScore)
            }}</text>
          </view>
        </view>

        <view class="result-stats">
          <view class="stat-item">
            <text class="stat-number">{{ finalResult.correctAnswers }}</text>
            <text class="stat-label">正确识别</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ finalResult.totalQuestions }}</text>
            <text class="stat-label">总题目</text>
          </view>
          <view class="stat-item">
            <text class="stat-number"
              >{{ Math.round(finalResult.accuracy) }}%</text
            >
            <text class="stat-label">准确率</text>
          </view>
        </view>
      </view>

      <view class="skills-mastery">
        <text class="mastery-title">🎯 技能掌握度</text>
        <view
          v-for="skill in finalResult.skillsMastery"
          :key="skill.name"
          class="skill-mastery-item"
        >
          <view class="skill-header">
            <text class="skill-name">{{ skill.name }}</text>
            <text class="skill-score">{{ skill.score }}%</text>
          </view>
          <view class="skill-progress">
            <view
              class="skill-progress-fill"
              :style="{ width: skill.score + '%' }"
            ></view>
          </view>
          <text class="skill-feedback">{{ skill.feedback }}</text>
        </view>
      </view>

      <view class="improvement-suggestions">
        <text class="improvement-title">📈 提升建议</text>
        <view
          v-for="suggestion in finalResult.improvements"
          :key="suggestion.area"
          class="improvement-item"
        >
          <text class="improvement-area">{{ suggestion.area }}</text>
          <text class="improvement-desc">{{ suggestion.description }}</text>
          <view class="improvement-actions">
            <text
              v-for="action in suggestion.actions"
              :key="action"
              class="improvement-action"
            >
              • {{ action }}
            </text>
          </view>
        </view>
      </view>

      <view class="result-actions">
        <view class="action-btn secondary" @click="retryTraining">
          <text class="btn-text">重新训练</text>
        </view>
        <view class="action-btn tertiary" @click="shareResult">
          <text class="btn-text">分享成果</text>
        </view>
        <view class="action-btn primary" @click="backToSelection">
          <text class="btn-text">选择新训练</text>
        </view>
      </view>
    </view>

    <!-- 紧急求助按钮 -->
    <view class="emergency-help">
      <view class="help-btn" @click="showEmergencyHelp">
        <text class="help-icon">🆘</text>
        <text class="help-text">紧急求助</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentStage: "selection", // selection, briefing, training, feedback, result
      selectedMode: null,
      currentScenario: 0,
      totalScenarios: 0,
      currentScore: 0,
      currentTrainingStep: {},
      feedbackResult: {},
      finalResult: {},
      trainingModes: [],
      trainingQuestions: [],
      currentSessionId: null,
      currentQuestionIndex: 0,
    };
  },

  onLoad() {
    this.loadTrainingTypes();
  },

  methods: {
    // 加载训练类型
    async loadTrainingTypes() {
      try {
        const response = await uni.request({
          url: "http://localhost:8000/api/protection-drill/training-types",
          method: "GET",
        });

        if (response.data.code === 200) {
          this.trainingModes = response.data.data.map((item) => ({
            id: item.id,
            title: item.title,
            icon: item.icon,
            description: item.description,
            level: item.level,
            scenarios: 8, // 默认8个场景
            duration: item.duration,
            skills: item.skills,
            objectives: item.objectives,
            riskSignals: item.risk_signals,
            strategies: item.strategies,
          }));
        } else {
          throw new Error(response.data.message || "获取训练类型失败");
        }
      } catch (error) {
        console.error("加载训练类型失败:", error);
        uni.showToast({
          title: "加载失败，请重试",
          icon: "none",
        });
        // 使用原有的硬编码数据作为备选
        this.loadFallbackData();
      }
    },

    // 备选数据
    loadFallbackData() {
      this.trainingModes = [
        {
          id: 1,
          title: "操控识别训练",
          icon: "�",
          description: "学会识别和应对情感操控、PUA等行为",
          level: 2,
          scenarios: 8,
          duration: "20-30分钟",
          skills: ["操控识别", "边界设定", "自我保护"],
          objectives: [
            "识别常见的情感操控手段",
            "学会设定和维护个人边界",
            "掌握应对操控的有效策略",
            "提升自我保护意识",
          ],
          riskSignals: [
            {
              type: "情感操控",
              icon: "🎪",
              description: "通过情感绑架、威胁等方式控制你的行为和想法",
            },
            {
              type: "孤立策略",
              icon: "🏝️",
              description: "试图让你远离朋友、家人，增加对其依赖",
            },
            {
              type: "贬低打击",
              icon: "⬇️",
              description: "不断贬低你的价值，降低你的自信心",
            },
          ],
          strategies: [
            "保持客观理性的判断",
            "维护与朋友家人的联系",
            "明确表达自己的边界",
            "及时寻求外部支持",
          ],
        },
        // 其他训练模式...
      ];
    },

    selectMode(mode) {
      this.selectedMode = mode;
      this.currentStage = "briefing";
    },

    backToSelection() {
      this.currentStage = "selection";
      this.selectedMode = null;
      this.currentSessionId = null;
      this.trainingQuestions = [];
    },

    async startTraining() {
      try {
        // 创建训练会话
        const sessionResponse = await uni.request({
          url: "http://localhost:8000/api/protection-drill/session/start",
          method: "POST",
          data: {
            training_type_id: this.selectedMode.id,
          },
          header: {
            Authorization: "Bearer " + uni.getStorageSync("token"),
          },
        });

        if (sessionResponse.data.code !== 200) {
          throw new Error(sessionResponse.data.message || "创建会话失败");
        }

        this.currentSessionId = sessionResponse.data.data.session_id;

        // 获取训练题目
        const questionsResponse = await uni.request({
          url: `http://localhost:8000/api/protection-drill/questions/${this.selectedMode.id}`,
          method: "GET",
          data: { count: 8 },
        });

        if (questionsResponse.data.code !== 200) {
          throw new Error(questionsResponse.data.message || "获取题目失败");
        }

        this.trainingQuestions = questionsResponse.data.data;
        this.currentStage = "training";
        this.currentScenario = 1;
        this.totalScenarios = this.trainingQuestions.length;
        this.currentScore = 0;
        this.currentQuestionIndex = 0;
        this.loadCurrentQuestion();
      } catch (error) {
        console.error("开始训练失败:", error);
        uni.showToast({
          title: "开始训练失败，请重试",
          icon: "none",
        });
        // 回退到原有逻辑
        this.startTrainingFallback();
      }
    },

    // 备选开始训练逻辑
    startTrainingFallback() {
      this.currentStage = "training";
      this.currentScenario = 1;
      this.totalScenarios = this.selectedMode.scenarios;
      this.currentScore = 0;
      this.initializeTraining();
    },

    loadCurrentQuestion() {
      if (this.currentQuestionIndex < this.trainingQuestions.length) {
        const question = this.trainingQuestions[this.currentQuestionIndex];
        this.currentTrainingStep = {
          title: question.title,
          description: question.description,
          dialogue: question.dialogue,
          question: {
            title: question.question_title,
            text: question.question_text,
            options: question.options,
          },
        };
      }
    },

    async selectAnswer(option) {
      try {
        if (!this.currentSessionId) {
          // 如果没有会话ID，使用原有逻辑
          this.selectAnswerFallback(option);
          return;
        }

        const currentQuestion =
          this.trainingQuestions[this.currentQuestionIndex];

        const response = await uni.request({
          url: `http://localhost:8000/api/protection-drill/session/${this.currentSessionId}/answer`,
          method: "POST",
          data: {
            question_id: currentQuestion.id,
            selected_option_id: option.id,
          },
          header: {
            Authorization: "Bearer " + uni.getStorageSync("token"),
          },
        });

        if (response.data.code !== 200) {
          throw new Error(response.data.message || "提交答案失败");
        }

        const feedback = response.data.data;
        const scoreGained = feedback.is_correct ? 10 : 3;
        this.currentScore += scoreGained;

        this.feedbackResult = {
          isCorrect: feedback.is_correct,
          scoreGained,
          correctAnalysis: feedback.analysis,
          riskExplanation: feedback.risk_explanation,
          protectionAdvice: feedback.protection_advice,
          betterChoice: feedback.is_correct
            ? null
            : feedback.correct_option?.text,
        };

        this.currentStage = "feedback";
      } catch (error) {
        console.error("提交答案失败:", error);
        uni.showToast({
          title: "提交失败，请重试",
          icon: "none",
        });
        // 回退到原有逻辑
        this.selectAnswerFallback(option);
      }
    },

    // 备选答案选择逻辑
    selectAnswerFallback(option) {
      const isCorrect = option.isCorrect;
      const scoreGained = isCorrect ? 10 : 3;

      this.currentScore += scoreGained;

      this.feedbackResult = {
        isCorrect,
        scoreGained,
        correctAnalysis: isCorrect
          ? "你正确识别了这个风险信号！"
          : "这个答案需要再考虑一下。",
        riskExplanation:
          "这是典型的情感操控行为，通过威胁分手来控制对方的社交关系。",
        protectionAdvice: [
          "明确表达自己的立场和边界",
          "不被情感威胁所绑架",
          "寻求朋友或专业人士的意见",
          "考虑这种关系是否健康",
        ],
        betterChoice: isCorrect ? null : "正确答案是A：情感操控",
      };

      this.currentStage = "feedback";
    },

    nextScenario() {
      this.currentQuestionIndex++;

      if (this.currentQuestionIndex < this.trainingQuestions.length) {
        this.currentScenario++;
        this.loadCurrentQuestion();
        this.currentStage = "training";
      } else {
        this.finishTraining();
      }
    },

    async finishTraining() {
      try {
        if (this.currentSessionId) {
          const response = await uni.request({
            url: `http://localhost:8000/api/protection-drill/session/${this.currentSessionId}/complete`,
            method: "POST",
            header: {
              Authorization: "Bearer " + uni.getStorageSync("token"),
            },
          });

          if (response.data.code === 200) {
            const result = response.data.data;
            this.finalResult = {
              totalScore: this.currentScore,
              correctAnswers: result.correct_answers,
              totalQuestions: result.total_questions,
              accuracy: result.accuracy_rate,
              skillsMastery: [
                {
                  name: "风险识别",
                  score: Math.min(100, Math.round(result.accuracy_rate + 10)),
                  feedback:
                    result.accuracy_rate >= 80
                      ? "能很好地识别风险信号"
                      : "需要加强风险识别能力",
                },
                {
                  name: "应对策略",
                  score: Math.max(50, Math.round(result.accuracy_rate - 10)),
                  feedback:
                    result.accuracy_rate >= 70
                      ? "应对策略掌握良好"
                      : "需要加强应对技巧的练习",
                },
              ],
              improvements: [
                {
                  area: "防护意识",
                  description: result.performance_message,
                  actions: ["继续学习防护知识", "实践防护技能"],
                },
              ],
            };
          } else {
            throw new Error("获取结果失败");
          }
        } else {
          this.generateFinalResult();
        }

        this.currentStage = "result";
      } catch (error) {
        console.error("完成训练失败:", error);
        this.generateFinalResult();
        this.currentStage = "result";
      }
    },

    initializeTraining() {
      // 初始化训练数据
      this.currentTrainingStep = this.generateTrainingStep();
    },

    generateTrainingStep() {
      // 根据选择的模式生成训练步骤
      const scenarios = {
        1: {
          // 操控识别训练
          title: "情感操控识别",
          description: "小明在和女友交往中遇到了以下情况...",
          dialogue: [
            {
              id: 1,
              speaker: "女友",
              text: "你如果真的爱我，就应该删掉所有异性好友。",
              isRisk: true,
            },
            {
              id: 2,
              speaker: "女友",
              text: "你不删的话，说明你心里还有别人，我们就分手！",
              isRisk: true,
            },
          ],
          question: {
            title: "风险识别",
            text: "这种行为属于什么类型的风险信号？",
            options: [
              {
                id: 1,
                text: "情感操控",
                description: "通过威胁分手来控制对方行为",
                isCorrect: true,
              },
              {
                id: 2,
                text: "正常要求",
                description: "恋人之间的合理期望",
                isCorrect: false,
              },
              {
                id: 3,
                text: "沟通不当",
                description: "只是表达方式有问题",
                isCorrect: false,
              },
            ],
          },
        },
        // 其他场景...
      };

      return scenarios[this.selectedMode.id] || {};
    },

    generateFinalResult() {
      this.finalResult = {
        totalScore: this.currentScore,
        correctAnswers: 6,
        totalQuestions: 8,
        accuracy: 75,
        skillsMastery: [
          {
            name: "风险识别",
            score: 80,
            feedback: "能较好地识别常见风险信号",
          },
          {
            name: "应对策略",
            score: 70,
            feedback: "需要加强应对技巧的练习",
          },
        ],
        improvements: [
          {
            area: "边界设定",
            description: "需要更清楚地设定个人边界",
            actions: ["练习表达拒绝", "明确个人底线"],
          },
        ],
      };
    },

    getHint() {
      uni.showModal({
        title: "💡 提示",
        content:
          "注意观察对方是否试图通过威胁、情感绑架等方式控制你的行为。健康的关系应该基于相互尊重。",
        showCancel: false,
        confirmText: "知道了",
      });
    },

    skipScenario() {
      uni.showModal({
        title: "确认跳过",
        content: "跳过当前场景将不会获得分数，确定要跳过吗？",
        success: (res) => {
          if (res.confirm) {
            this.nextScenario();
          }
        },
      });
    },

    pauseTraining() {
      uni.showActionSheet({
        itemList: ["继续训练", "重新开始", "退出训练"],
        success: (res) => {
          switch (res.tapIndex) {
            case 1:
              this.startTraining();
              break;
            case 2:
              this.backToSelection();
              break;
          }
        },
      });
    },

    retryTraining() {
      this.startTraining();
    },

    shareResult() {
      uni.showToast({
        title: "分享功能开发中",
        icon: "none",
      });
    },

    showEmergencyHelp() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/emergency-resources",
      });
    },

    getLevelText(level) {
      const levelMap = {
        1: "入门",
        2: "进阶",
        3: "高级",
      };
      return levelMap[level] || "未知";
    },

    getScoreLevel(score) {
      if (score >= 80) return "excellent";
      if (score >= 60) return "good";
      if (score >= 40) return "average";
      return "poor";
    },

    getScoreLevelText(score) {
      if (score >= 80) return "优秀";
      if (score >= 60) return "良好";
      if (score >= 40) return "及格";
      return "需努力";
    },
  },
};
</script>

<style scoped>
.protection-container {
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

/* 模式选择阶段 */
.mode-selection {
  padding: 40rpx;
}

.risk-alert {
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
  border: 2rpx solid #ff6b6b;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 32rpx;
  text-align: center;
}

.alert-icon {
  font-size: 32rpx;
  margin-bottom: 12rpx;
  display: block;
}

.alert-text {
  font-size: 26rpx;
  color: #d32f2f;
  line-height: 1.5;
}

.training-modes {
  margin-bottom: 120rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
  display: block;
}

.mode-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.mode-card:active {
  transform: translateY(2rpx);
}

.mode-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.mode-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.mode-info {
  flex: 1;
}

.mode-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.mode-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}

.mode-level {
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
}

.mode-level.level-1 {
  background-color: #f6ffed;
  color: #52c41a;
}

.mode-level.level-2 {
  background-color: #fff7e6;
  color: #fa8c16;
}

.mode-level.level-3 {
  background-color: #fff2f0;
  color: #f5222d;
}

.level-text {
  font-weight: bold;
}

.mode-details {
  margin-top: 20rpx;
}

.mode-stats {
  display: flex;
  gap: 32rpx;
  margin-bottom: 20rpx;
}

.stat-item {
  display: flex;
  align-items: center;
  flex: 1;
}

.stat-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.stat-text {
  font-size: 24rpx;
  color: #666;
}

.mode-skills {
  margin-top: 16rpx;
}

.skills-title {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 12rpx;
  display: block;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background-color: #f0f0f0;
  color: #666;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
}

/* 训练简介阶段 */
.briefing-stage {
  padding: 40rpx;
}

.briefing-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.briefing-header {
  display: flex;
  align-items: center;
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.briefing-icon {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.briefing-title-area {
  flex: 1;
}

.briefing-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.briefing-subtitle {
  font-size: 26rpx;
  color: #666;
}

.briefing-content {
  margin-bottom: 40rpx;
}

.warning-section {
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
  border: 2rpx solid #ff6b6b;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 32rpx;
}

.warning-icon {
  font-size: 28rpx;
  margin-bottom: 12rpx;
  display: block;
}

.warning-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #d32f2f;
  margin-bottom: 12rpx;
  display: block;
}

.warning-text {
  font-size: 26rpx;
  color: #d32f2f;
  line-height: 1.6;
}

.section-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.training-objectives,
.risk-signals,
.protection-strategies {
  margin-bottom: 32rpx;
}

.objectives-list,
.strategies-list {
  background-color: #fafafa;
  border-radius: 12rpx;
  padding: 20rpx;
}

.objective-item,
.strategy-item {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
  margin-bottom: 8rpx;
  display: block;
}

.objective-item:last-child,
.strategy-item:last-child {
  margin-bottom: 0;
}

.signals-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.signal-item {
  background-color: #fafafa;
  border-radius: 12rpx;
  padding: 20rpx;
}

.signal-header {
  display: flex;
  align-items: center;
  margin-bottom: 8rpx;
}

.signal-icon {
  font-size: 24rpx;
  margin-right: 12rpx;
}

.signal-type {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
}

.signal-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.briefing-actions {
  display: flex;
  gap: 20rpx;
}

.action-btn {
  flex: 1;
  padding: 28rpx;
  border-radius: 12rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: bold;
  transition: all 0.3s ease;
}

.action-btn:active {
  transform: translateY(2rpx);
}

.action-btn.primary {
  background-color: #ff6b6b;
  color: white;
}

.action-btn.secondary {
  background-color: #f0f0f0;
  color: #666;
}

.action-btn.tertiary {
  background-color: #fff7e6;
  color: #fa8c16;
  border: 2rpx solid #fa8c16;
}

.btn-text {
  font-size: 28rpx;
}

/* 训练进行中阶段 */
.training-stage {
  padding: 40rpx;
  padding-bottom: 140rpx;
}

.training-header {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-info {
  flex: 1;
}

.progress-text {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 12rpx;
  display: block;
}

.progress-bar {
  height: 8rpx;
  background-color: #f0f0f0;
  border-radius: 4rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #ff6b6b;
  border-radius: 4rpx;
  transition: width 0.3s ease;
}

.training-score {
  display: flex;
  align-items: center;
  margin-left: 32rpx;
}

.score-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.score-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #ff6b6b;
}

.scenario-content {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.scenario-background {
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.scenario-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.scenario-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.scenario-dialogue {
  margin-bottom: 32rpx;
}

.dialogue-item {
  background-color: #fafafa;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 16rpx;
  border-left: 4rpx solid #e0e0e0;
}

.dialogue-item.risk-message {
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
  border-left-color: #ff6b6b;
}

.dialogue-item.normal-message {
  background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
  border-left-color: #52c41a;
}

.speaker-info {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}

.speaker-name {
  font-size: 24rpx;
  font-weight: bold;
  color: #333;
  margin-right: 12rpx;
}

.risk-indicator {
  font-size: 20rpx;
}

.dialogue-text {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
}

.question-section {
  border-top: 2rpx solid #f0f0f0;
  padding-top: 24rpx;
}

.question-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.question-text {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 24rpx;
  line-height: 1.6;
}

.answer-options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.option-item {
  background-color: #fafafa;
  border: 2rpx solid #e0e0e0;
  border-radius: 12rpx;
  padding: 24rpx;
  transition: all 0.3s ease;
}

.option-item:active {
  transform: translateY(2rpx);
  background-color: #f0f4ff;
  border-color: #ff6b6b;
}

.option-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8rpx;
}

.option-letter {
  width: 40rpx;
  height: 40rpx;
  background-color: #ff6b6b;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 16rpx;
  flex-shrink: 0;
}

.option-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
}

.option-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
  margin-left: 56rpx;
}

.training-controls {
  position: fixed;
  bottom: 100rpx;
  left: 40rpx;
  right: 40rpx;
  background-color: white;
  border-radius: 50rpx;
  padding: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  z-index: 100;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16rpx;
  min-width: 120rpx;
  transition: transform 0.2s ease;
}

.control-btn:active {
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

/* 反馈阶段 */
.feedback-stage {
  padding: 40rpx;
}

.feedback-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.feedback-header {
  text-align: center;
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.feedback-icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
  display: block;
}

.feedback-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.feedback-score {
  display: inline-block;
  background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
  border: 2rpx solid #ff6b6b;
  border-radius: 20rpx;
  padding: 8rpx 20rpx;
}

.score-gained {
  font-size: 24rpx;
  font-weight: bold;
  color: #ff6b6b;
}

.feedback-content {
  margin-bottom: 40rpx;
}

.correct-analysis,
.risk-explanation,
.protection-advice,
.better-choice {
  margin-bottom: 24rpx;
}

.analysis-title,
.explanation-title,
.advice-title,
.better-title {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.analysis-text,
.explanation-text,
.better-text {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
}

.advice-list {
  background-color: #f6ffed;
  border-radius: 12rpx;
  padding: 20rpx;
}

.advice-item {
  font-size: 24rpx;
  color: #52c41a;
  line-height: 1.6;
  margin-bottom: 8rpx;
  display: block;
}

.advice-item:last-child {
  margin-bottom: 0;
}

.feedback-actions {
  text-align: center;
}

.feedback-btn {
  background-color: #ff6b6b;
  color: white;
  padding: 32rpx 80rpx;
  border-radius: 50rpx;
  font-size: 28rpx;
  font-weight: bold;
  display: inline-block;
}

/* 结果阶段 */
.result-stage {
  padding: 40rpx;
}

.result-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.result-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
  display: block;
}

.result-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.result-subtitle {
  font-size: 26rpx;
  color: #666;
}

.result-overview {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.final-score {
  text-align: center;
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.score-number {
  font-size: 72rpx;
  font-weight: bold;
  color: #ff6b6b;
  display: block;
  margin-bottom: 8rpx;
}

.score-label {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 16rpx;
  display: block;
}

.score-level {
  display: inline-block;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  font-weight: bold;
}

.score-level.excellent {
  background-color: #f6ffed;
  color: #52c41a;
}

.score-level.good {
  background-color: #f0f4ff;
  color: #1890ff;
}

.score-level.average {
  background-color: #fff7e6;
  color: #fa8c16;
}

.score-level.poor {
  background-color: #fff2f0;
  color: #f5222d;
}

.result-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-number {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 22rpx;
  color: #666;
}

.skills-mastery {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.mastery-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
  display: block;
}

.skill-mastery-item {
  margin-bottom: 24rpx;
}

.skill-mastery-item:last-child {
  margin-bottom: 0;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.skill-name {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
}

.skill-score {
  font-size: 24rpx;
  font-weight: bold;
  color: #ff6b6b;
}

.skill-progress {
  height: 12rpx;
  background-color: #f0f0f0;
  border-radius: 6rpx;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.skill-progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  border-radius: 6rpx;
  transition: width 0.3s ease;
}

.skill-feedback {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.improvement-suggestions {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.improvement-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
  display: block;
}

.improvement-item {
  background-color: #fafafa;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
}

.improvement-item:last-child {
  margin-bottom: 0;
}

.improvement-area {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.improvement-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16rpx;
}

.improvement-actions {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.improvement-action {
  font-size: 22rpx;
  color: #888;
  line-height: 1.5;
}

.result-actions {
  display: flex;
  gap: 20rpx;
  margin-bottom: 120rpx;
}

/* 紧急求助 */
.emergency-help {
  position: fixed;
  bottom: 40rpx;
  right: 40rpx;
  z-index: 200;
}

.help-btn {
  background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
  color: white;
  padding: 20rpx 32rpx;
  border-radius: 50rpx;
  box-shadow: 0 4rpx 16rpx rgba(255, 71, 87, 0.3);
  display: flex;
  align-items: center;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 4rpx 16rpx rgba(255, 71, 87, 0.3);
  }

  50% {
    box-shadow: 0 4rpx 20rpx rgba(255, 71, 87, 0.5);
  }

  100% {
    box-shadow: 0 4rpx 16rpx rgba(255, 71, 87, 0.3);
  }
}

.help-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.help-text {
  font-size: 24rpx;
  font-weight: bold;
}

/* 响应式适配 */
@media screen and (max-width: 750rpx) {
  .mode-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .mode-level {
    margin-top: 12rpx;
    align-self: flex-start;
  }

  .mode-stats {
    flex-direction: column;
    gap: 16rpx;
  }

  .result-stats {
    flex-direction: column;
    gap: 24rpx;
  }

  .result-actions {
    flex-direction: column;
  }
}

/* 安全区域适配 */
.protection-container {
  padding-bottom: env(safe-area-inset-bottom);
}

/* 无障碍支持 */
.option-item:focus,
.action-btn:focus,
.control-btn:focus {
  outline: 2rpx solid #ff6b6b;
  outline-offset: 2rpx;
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .protection-container {
    background-color: #121212;
  }

  .mode-card,
  .briefing-card,
  .scenario-content,
  .feedback-card,
  .result-overview,
  .skills-mastery,
  .improvement-suggestions {
    background-color: #1e1e1e;
    color: #ffffff;
  }

  .mode-title,
  .briefing-title,
  .scenario-title,
  .feedback-title,
  .result-title,
  .section-label,
  .mastery-title,
  .improvement-title {
    color: #ffffff;
  }

  .mode-desc,
  .scenario-description,
  .analysis-text,
  .explanation-text,
  .better-text,
  .skill-feedback,
  .improvement-desc {
    color: #b3b3b3;
  }
}
</style>
