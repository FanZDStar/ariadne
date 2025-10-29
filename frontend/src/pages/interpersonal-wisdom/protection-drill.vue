<template>
  <view class="protection-container">    <!-- 训练模式选择 -->
    <view v-if="currentStage === 'selection'" class="mode-selection">
      <view class="risk-alert">
        <text class="alert-text">学习识别和应对人际关系中的潜在风险</text>
      </view>

      <view class="training-modes">
        <text class="section-title">选择训练模式</text>
        <view v-for="mode in trainingModes" :key="mode.id" class="mode-card" @click="selectMode(mode)">
          <view class="mode-header">
            <view class="mode-info">
              <text class="mode-title">{{ mode.title }}</text>
              <text class="mode-desc">{{ mode.description }}</text>
            </view>
          </view>

          <view class="mode-details">
            <view class="mode-stats">
              <view class="stat-item">
                <text class="stat-text">{{ mode.scenarios }}个场景</text>
              </view>
              <view class="stat-item">
                <text class="stat-text">{{ mode.duration }}</text>
              </view>
            </view>

            <view class="mode-skills">
              <text class="skills-title">训练技能：</text>
              <view class="skills-tags">
                <text v-for="skill in mode.skills" :key="skill" class="skill-tag">
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
          <view class="briefing-title-area">
            <text class="briefing-title">{{ selectedMode.title }}</text>
            <text class="briefing-subtitle">训练说明</text>
          </view>
        </view>

        <view class="briefing-content">
          <view class="warning-section">
            <text class="warning-title">重要提醒</text>
            <text class="warning-text">这是模拟训练，帮助你在安全环境中学习识别和应对风险。真实情况下如遇到危险，请立即寻求帮助。</text>
          </view>

          <view class="training-objectives">
            <text class="section-label">训练目标</text>
            <view class="objectives-list">
              <text v-for="objective in selectedMode.objectives" :key="objective" class="objective-item">
                • {{ objective }}
              </text>
            </view>
          </view>

          <view class="risk-signals">
            <text class="section-label">重点识别信号</text>
            <view class="signals-list">
              <view v-for="signal in selectedMode.riskSignals" :key="signal.type" class="signal-item">
                <view class="signal-header">
                  <text class="signal-type">{{ signal.type }}</text>
                </view>
                <text class="signal-desc">{{ signal.description }}</text>
              </view>
            </view>
          </view>

          <view class="protection-strategies">
            <text class="section-label">保护策略</text>
            <view class="strategies-list">
              <text v-for="strategy in selectedMode.strategies" :key="strategy" class="strategy-item">
                • {{ strategy }}
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
          <text class="progress-text">场景 {{ currentScenario }}/{{ totalScenarios }}</text>
          <view class="progress-bar">
            <view class="progress-fill" :style="{ width: (currentScenario / totalScenarios) * 100 + '%' }">
            </view>
          </view>
        </view>
        <view class="training-score">
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
          <view v-for="message in currentTrainingStep.dialogue" :key="message.id" class="dialogue-item" :class="{
            'risk-message': message.isRisk,
            'normal-message': !message.isRisk,
          }">
            <view class="speaker-info">
              <text class="speaker-name">{{ message.speaker }}</text>
              <text v-if="message.isRisk" class="risk-indicator">风险</text>
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
            <view v-for="option in currentTrainingStep.question.options" :key="option.id" class="option-item"
              @click="selectAnswer(option)">
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
          <text class="control-text">提示</text>
        </view>
        <view class="control-btn" @click="skipScenario">
          <text class="control-text">跳过</text>
        </view>
        <view class="control-btn" @click="pauseTraining">
          <text class="control-text">暂停</text>
        </view>
      </view>
    </view>

    <!-- 答案反馈 -->
    <view v-if="currentStage === 'feedback'" class="feedback-stage">
      <view class="feedback-card">
        <view class="feedback-header">
          <text class="feedback-title">{{
            feedbackResult.isCorrect ? "回答正确！" : "需要改进"
          }}</text>
          <view class="feedback-score">
            <text class="score-gained">+{{ feedbackResult.scoreGained }}分</text>
          </view>
        </view>

        <view class="feedback-content">
          <view class="correct-analysis">
            <text class="analysis-title">{{ feedbackResult.isCorrect ? '正确分析：' : '错误提示：' }}</text>
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
              <text v-for="advice in feedbackResult.protectionAdvice" :key="advice" class="advice-item">
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
              currentScenario < totalScenarios ? "下一个场景" : "查看结果" }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 训练结果 -->
    <view v-if="currentStage === 'result'" class="result-stage">
      <view class="result-header">
        <text class="result-title">训练完成！</text>
        <text class="result-subtitle">{{ selectedMode.title }}</text>
      </view>

      <view class="result-overview">
        <view class="final-score">
          <text class="score-number">{{ finalResult.totalScore }}</text>
          <text class="score-label">总分</text>
          <view class="score-level" :class="getScoreLevel(finalResult.totalScore)">
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
            <text class="stat-number">{{ Math.round(finalResult.accuracy) }}%</text>
            <text class="stat-label">准确率</text>
          </view>
        </view>
      </view>

      <view class="skills-mastery">
        <text class="mastery-title">技能掌握度</text>
        <view v-for="skill in finalResult.skillsMastery" :key="skill.name" class="skill-mastery-item">
          <view class="skill-header">
            <text class="skill-name">{{ skill.name }}</text>
            <text class="skill-score">{{ skill.score }}%</text>
          </view>
          <view class="skill-progress">
            <view class="skill-progress-fill" :style="{ width: skill.score + '%' }"></view>
          </view>
          <text class="skill-feedback">{{ skill.feedback }}</text>
        </view>
      </view>

      <view class="improvement-suggestions">
        <text class="improvement-title">提升建议</text>
        <view v-for="suggestion in finalResult.improvements" :key="suggestion.area" class="improvement-item">
          <text class="improvement-area">{{ suggestion.area }}</text>
          <text class="improvement-desc">{{ suggestion.description }}</text>
          <view class="improvement-actions">
            <text v-for="action in suggestion.actions" :key="action" class="improvement-action">
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
      // 新增变量支持报告保存
      correctAnswers: 0,
      trainingDuration: 0,
      questionAnalysis: [],
      trainingStartTime: null,
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
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/api/protection-drill/training-types`,
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
        // 记录训练开始时间
        this.trainingStartTime = Date.now();
        this.correctAnswers = 0;
        this.questionAnalysis = [];

        // 创建训练会话
        const sessionResponse = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/api/protection-drill/session/start`,
          method: "POST",
          data: {
            training_type_id: this.selectedMode.id,
          },
          header: {
            Authorization: "Bearer " + uni.getStorageSync("access_token"),
          },
        });

        if (sessionResponse.data.code !== 200) {
          throw new Error(sessionResponse.data.message || "创建会话失败");
        }

        this.currentSessionId = sessionResponse.data.data.session_id;

        // 获取训练题目
        const questionsResponse = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/api/protection-drill/questions/${this.selectedMode.id}`,
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
      console.log("使用备选训练逻辑");
      this.currentStage = "training";
      this.currentScenario = 1;
      this.totalScenarios = this.selectedMode.scenarios;
      this.currentScore = 0;
      this.currentQuestionIndex = 0;

      // 初始化备选题目数据
      this.trainingQuestions = this.generateFallbackQuestions();

      this.initializeTraining();
    },

    generateFallbackQuestions() {
      // 生成备选题目数据
      return [
        {
          id: 1,
          title: "情感操控识别",
          question_title: "情感操控识别",
          question_text: "这种行为属于什么类型的风险信号？",
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
        {
          id: 2,
          title: "边界设定",
          question_title: "边界设定",
          question_text: "如何应对情感操控行为？",
          options: [
            {
              id: 1,
              text: "设定边界",
              description: "明确表达个人底线",
              isCorrect: true,
            },
            {
              id: 2,
              text: "妥协退让",
              description: "为了关系和谐而妥协",
              isCorrect: false,
            },
            {
              id: 3,
              text: "忽略不理",
              description: "当作没听见",
              isCorrect: false,
            },
          ],
        },
        {
          id: 3,
          title: "风险识别",
          question_title: "风险识别",
          question_text: "以下哪个是情感操控的典型特征？",
          options: [
            {
              id: 1,
              text: "威胁分手",
              description: "用分手威胁来控制对方",
              isCorrect: true,
            },
            {
              id: 2,
              text: "温柔体贴",
              description: "关心对方的表现",
              isCorrect: false,
            },
            {
              id: 3,
              text: "开放沟通",
              description: "坦诚交流想法",
              isCorrect: false,
            },
          ],
        },
        {
          id: 4,
          title: "应对策略",
          question_title: "应对策略",
          question_text: "发现被情感操控时应该怎么做？",
          options: [
            {
              id: 1,
              text: "寻求支持",
              description: "向朋友或专业人士求助",
              isCorrect: true,
            },
            {
              id: 2,
              text: "默默忍受",
              description: "不想破坏关系",
              isCorrect: false,
            },
            {
              id: 3,
              text: "报复回击",
              description: "以牙还牙",
              isCorrect: false,
            },
          ],
        },
        {
          id: 5,
          title: "自我保护",
          question_title: "自我保护",
          question_text: "哪种做法有助于自我保护？",
          options: [
            {
              id: 1,
              text: "保持独立",
              description: "维持自己的生活和朋友圈",
              isCorrect: true,
            },
            {
              id: 2,
              text: "完全依赖",
              description: "把对方当作生活的全部",
              isCorrect: false,
            },
            {
              id: 3,
              text: "避免冲突",
              description: "任何情况下都不争论",
              isCorrect: false,
            },
          ],
        },
        {
          id: 6,
          title: "警示信号",
          question_title: "警示信号",
          question_text: "以下哪个是关系中的红旗信号？",
          options: [
            {
              id: 1,
              text: "孤立朋友",
              description: "阻止你与朋友接触",
              isCorrect: true,
            },
            {
              id: 2,
              text: "关心安全",
              description: "担心你的安全",
              isCorrect: false,
            },
            {
              id: 3,
              text: "分享感受",
              description: "愿意表达内心想法",
              isCorrect: false,
            },
          ],
        },
        {
          id: 7,
          title: "健康关系",
          question_title: "健康关系",
          question_text: "健康关系的特征是什么？",
          options: [
            {
              id: 1,
              text: "相互尊重",
              description: "尊重彼此的选择和边界",
              isCorrect: true,
            },
            {
              id: 2,
              text: "完全控制",
              description: "一方完全听从另一方",
              isCorrect: false,
            },
            {
              id: 3,
              text: "避免沟通",
              description: "不谈论问题",
              isCorrect: false,
            },
          ],
        },
        {
          id: 8,
          title: "求助资源",
          question_title: "求助资源",
          question_text: "遇到情感困扰时应该向谁求助？",
          options: [
            {
              id: 1,
              text: "专业咨询师",
              description: "寻求专业心理帮助",
              isCorrect: true,
            },
            {
              id: 2,
              text: "网络陌生人",
              description: "在网上随便找人倾诉",
              isCorrect: false,
            },
            {
              id: 3,
              text: "完全自己解决",
              description: "不告诉任何人",
              isCorrect: false,
            },
          ],
        },
      ];
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
      console.log("用户选择答案:", option);

      try {
        if (!this.currentSessionId) {
          // 如果没有会话ID，使用原有逻辑
          this.selectAnswerFallback(option);
          return;
        }

        const currentQuestion =
          this.trainingQuestions[this.currentQuestionIndex];
        console.log("当前题目:", currentQuestion);

        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/api/protection-drill/session/${this.currentSessionId}/answer`,
          method: "POST",
          data: {
            question_id: currentQuestion.id,
            selected_option_id: option.id,
          },
          header: {
            Authorization: "Bearer " + uni.getStorageSync("access_token"),
          },
        });

        if (response.data.code !== 200) {
          throw new Error(response.data.message || "提交答案失败");
        }

        const feedback = response.data.data;
        const scoreGained = feedback.is_correct ? 10 : 3;
        this.currentScore += scoreGained;

        console.log("答案反馈:", feedback);
        console.log("是否正确:", feedback.is_correct);

        // 记录答题分析 - 修复正确率计算
        if (feedback.is_correct) {
          this.correctAnswers++;
          console.log("正确答案数增加到:", this.correctAnswers);
        }

        // 记录每题的详细分析
        this.questionAnalysis.push({
          question_id: currentQuestion.id,
          question_title:
            currentQuestion.title || currentQuestion.question_title,
          question_text: currentQuestion.question_text,
          is_correct: feedback.is_correct,
          selected_option: option.text,
          selected_option_id: option.id,
          correct_option: feedback.correct_answer,
          correct_option_id: feedback.correct_option_id,
          explanation: feedback.explanation || feedback.analysis,
          risk_explanation: feedback.risk_explanation,
          score_gained: scoreGained,
          options: currentQuestion.options
            ? currentQuestion.options.map((opt) => ({
              id: opt.id,
              text: opt.text,
              description: opt.description,
              is_selected: opt.id === option.id,
              is_correct: opt.id === feedback.correct_option_id,
            }))
            : [],
        });

        console.log("当前答题分析记录:", this.questionAnalysis);

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
      console.log("使用备选答案逻辑:", option);

      const currentQuestion = this.trainingQuestions[this.currentQuestionIndex];
      const isCorrect = option.isCorrect === true || option.is_correct === true;
      const scoreGained = isCorrect ? 10 : 3;

      this.currentScore += scoreGained;

      // 更新正确答案计数
      if (isCorrect) {
        this.correctAnswers++;
        console.log("备选逻辑 - 正确答案数增加到:", this.correctAnswers);
      }

      // 查找正确答案，兼容不同的字段名
      const correctOption = currentQuestion?.options?.find(opt =>
        opt.isCorrect === true || opt.is_correct === true
      );

      // 收集答题分析数据
      this.questionAnalysis.push({
        question_id: currentQuestion?.id || this.currentQuestionIndex + 1,
        question_title:
          currentQuestion?.title ||
          currentQuestion?.question_title ||
          `题目${this.currentQuestionIndex + 1}`,
        question_text: currentQuestion?.question_text || "风险识别题目",
        is_correct: isCorrect,
        selected_option: option.text,
        selected_option_id: option.id,
        correct_option: correctOption?.text || "未知正确答案", // 从数据中获取正确答案
        correct_option_id: correctOption?.id || 1,
        explanation: correctOption?.description || (isCorrect
          ? "你正确识别了这个风险信号！"
          : `正确答案是：${correctOption?.text || '未知'}`),
        risk_explanation: currentQuestion?.risk_explanation ||
          "这是典型的情感操控行为，通过威胁分手来控制对方的社交关系。",
        score_gained: scoreGained,
        options:
          currentQuestion?.options?.map((opt) => ({
            id: opt.id,
            text: opt.text,
            description: opt.description,
            is_selected: opt.id === option.id,
            is_correct: opt.isCorrect === true || opt.is_correct === true,
          })) || [],
      });

      console.log("备选逻辑 - 答题分析记录:", this.questionAnalysis);

      this.feedbackResult = {
        isCorrect,
        scoreGained,
        correctAnalysis: isCorrect
          ? (currentQuestion?.correct_analysis || "你正确识别了这个风险信号！")
          : "这个答案需要再考虑一下。不要灰心，通过练习你会越来越敏锐地识别这些风险信号。",
        riskExplanation: currentQuestion?.risk_explanation ||
          "这是典型的情感操控行为，通过威胁分手来控制对方的社交关系。",
        protectionAdvice: currentQuestion?.protection_advice || [
          "明确表达自己的立场和边界",
          "不被情感威胁所绑架",
          "寻求朋友或专业人士的意见",
          "考虑这种关系是否健康",
        ],
        betterChoice: isCorrect ? null : (currentQuestion?.better_choice || `正确答案：${correctOption?.text}`),
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
      console.log("开始完成训练流程");

      try {
        // 计算训练时长
        if (this.trainingStartTime) {
          this.trainingDuration = Math.floor(
            (Date.now() - this.trainingStartTime) / 1000
          );
          console.log("训练时长:", this.trainingDuration, "秒");
        }

        if (this.currentSessionId) {
          console.log("使用会话ID完成训练:", this.currentSessionId);

          const response = await uni.request({
            url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/api/protection-drill/session/${this.currentSessionId}/complete`,
            method: "POST",
            header: {
              Authorization: "Bearer " + uni.getStorageSync("access_token"),
            },
          });

          console.log("完成训练API响应:", response);

          if (response.data.code === 200) {
            const result = response.data.data;
            console.log("训练结果数据:", result);

            // 处理积分奖励信息
            if (result.star_reward) {
              const starReward = result.star_reward;
              console.log("🌟 积分奖励信息:", starReward);

              // 只有在show_toast为true时才显示Toast提示
              if (starReward.show_toast && starReward.is_rewarded && starReward.earned_points > 0) {
                // 显示积分奖励Toast
                uni.showToast({
                  title: `🌟 ${starReward.message}`,
                  icon: 'none',
                  duration: 3000
                });
              }
              // 不再显示进度提示，避免重复提醒
            }

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

            console.log("准备保存训练报告...");
            // 保存训练报告
            await this.saveTrainingReport(result);
            console.log("训练报告保存完成");
          } else {
            throw new Error("获取结果失败");
          }
        } else {
          console.log("没有会话ID，使用本地数据");
          this.generateFinalResult();
          // 即使没有会话ID也要尝试保存报告
          const mockResult = {
            accuracy_rate:
              (this.correctAnswers / this.trainingQuestions.length) * 100,
            total_questions: this.trainingQuestions.length,
            correct_answers: this.correctAnswers,
            performance_message: "基于本地数据的训练完成",
          };
          console.log("使用模拟结果保存报告:", mockResult);
          await this.saveTrainingReport(mockResult);
        }

        console.log("切换到结果页面");
        this.currentStage = "result";
      } catch (error) {
        console.error("完成训练失败:", error);
        this.generateFinalResult();
        this.currentStage = "result";
      }
    },

    async saveTrainingReport(result) {
      console.log("开始保存训练报告，输入参数:", result);

      try {
        const token = uni.getStorageSync("access_token");
        console.log("获取到的token:", token ? "Token存在" : "Token不存在");

        if (!token) {
          console.log("No token available for saving report");
          uni.showToast({
            title: "请先登录以保存训练记录",
            icon: "none",
            duration: 3000,
          });
          return;
        }

        // 准备报告数据
        const actualAccuracy =
          this.trainingQuestions.length > 0
            ? (this.correctAnswers / this.trainingQuestions.length) * 100
            : 0;

        console.log("实际统计 - 正确答案数:", this.correctAnswers);
        console.log("实际统计 - 总题数:", this.trainingQuestions.length);
        console.log("实际统计 - 准确率:", actualAccuracy);
        console.log("答题分析数据:", this.questionAnalysis);

        const reportData = {
          drill_type: this.selectedMode ? this.selectedMode.title : "防护训练",
          scenario_name: this.selectedMode
            ? this.selectedMode.description
            : null,
          total_questions: this.trainingQuestions.length,
          correct_answers: this.correctAnswers,
          score: actualAccuracy,
          completion_time: this.trainingDuration || null,
          report_content: JSON.stringify({
            final_result: this.finalResult || {},
            question_analysis: this.questionAnalysis || [],
            skills_mastery: this.finalResult?.skillsMastery || [],
            improvements: this.finalResult?.improvements || [],
            actual_accuracy: actualAccuracy,
            total_score: this.currentScore,
          }),
          suggestions: this.generateSuggestions(actualAccuracy),
          question_analysis: this.questionAnalysis || [], // 添加详细的答题分析
        };

        console.log("准备保存训练报告:", reportData);
        console.log(
          "API请求URL:",
          `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/protection-drill/reports`
        );

        const saveResponse = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL || "http://localhost:8000"}/protection-drill/reports`,
          method: "POST",
          header: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          data: reportData,
        });

        console.log("API响应状态码:", saveResponse.statusCode);
        console.log("API响应数据:", saveResponse.data);

        if (saveResponse.statusCode === 200) {
          console.log("训练报告保存成功:", saveResponse.data);

          // 处理积分奖励信息
          if (saveResponse.data.star_reward) {
            const starReward = saveResponse.data.star_reward;
            console.log("🌟 积分奖励信息:", starReward);

            // 只有在show_toast为true时才显示Toast提示
            if (starReward.show_toast && starReward.is_rewarded && starReward.earned_points > 0) {
              // 显示积分奖励Toast
              uni.showToast({
                title: `🌟 ${starReward.message}`,
                icon: 'none',
                duration: 3000
              });
            } else {
              // 没有积分奖励，显示普通保存成功提示
              uni.showToast({
                title: "训练记录已保存",
                icon: "success",
                duration: 2000,
              });
            }
          } else {
            // 没有积分奖励信息，显示普通保存成功提示
            uni.showToast({
              title: "训练记录已保存",
              icon: "success",
              duration: 2000,
            });
          }
        } else {
          console.error("保存训练报告失败，状态码:", saveResponse.statusCode);
          console.error("失败响应数据:", saveResponse.data);
          uni.showToast({
            title: "记录保存失败: " + (saveResponse.data?.detail || "未知错误"),
            icon: "error",
            duration: 3000,
          });
        }
      } catch (error) {
        console.error("保存训练报告出错:", error);
        console.error("错误详情:", error.message, error.stack);
        uni.showToast({
          title: "记录保存出错: " + error.message,
          icon: "none",
          duration: 3000,
        });
      }
    },

    generateSuggestions(accuracy) {
      let suggestions = "";

      if (accuracy >= 90) {
        suggestions =
          "表现优秀！你已经具备了很强的防护意识和风险识别能力。建议继续保持警觉，并帮助其他人提高防护意识。";
      } else if (accuracy >= 80) {
        suggestions =
          "表现良好！你具备了基本的防护能力。建议加强对细微风险信号的识别，继续提升应对策略的多样性。";
      } else if (accuracy >= 70) {
        suggestions =
          "表现一般。你对明显的风险信号有一定识别能力，但需要加强对隐性风险的敏感度。建议多学习防护知识，练习应对技巧。";
      } else if (accuracy >= 60) {
        suggestions =
          "表现有待提高。你的风险识别能力还需要加强。建议系统学习人际关系中的风险信号，多进行防护训练。";
      } else {
        suggestions =
          "表现需要大幅改进。建议重点学习基础的风险识别知识，寻求专业指导，并在日常生活中加强防护意识。";
      }

      return suggestions;
    },

    initializeTraining() {
      // 初始化训练数据
      if (this.trainingQuestions && this.trainingQuestions.length > 0) {
        // 如果有API题目数据，加载第一题
        this.loadCurrentQuestion();
      } else {
        // 否则使用硬编码数据
        this.currentTrainingStep = this.generateTrainingStep();
      }
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
  padding: 40rpx 0 0;
  background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 50%, #ffffff 100%);
  min-height: 100vh;
}

/* 模式选择阶段 */
.mode-selection {
  padding: 40rpx;
}

.risk-alert {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border: 1rpx solid rgba(59, 130, 246, 0.2);
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 32rpx;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(59, 130, 246, 0.1);
}

.alert-text {
  font-size: 26rpx;
  color: #3b82f6;
  line-height: 1.5;
  font-weight: 500;
}

.training-modes {
  margin-bottom: 120rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #1e40af;
  margin-bottom: 24rpx;
  display: block;
}

.mode-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 8rpx 32rpx rgba(59, 130, 246, 0.15);
  border: 1rpx solid rgba(59, 130, 246, 0.1);
  transition: all 0.3s ease;
}

.mode-card:active {
  transform: translateY(-2rpx) scale(0.98);
  box-shadow: 0 12rpx 40rpx rgba(59, 130, 246, 0.25);
}

.mode-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.mode-info {
  flex: 1;
}

.mode-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #1e40af;
  margin-bottom: 8rpx;
  display: block;
}

.mode-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
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
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
  padding: 12rpx 16rpx;
  border-radius: 12rpx;
  border: 1rpx solid rgba(59, 130, 246, 0.1);
}

.stat-text {
  font-size: 24rpx;
  color: #1e40af;
  font-weight: 500;
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
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
  color: #1e40af;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  border: 1rpx solid rgba(59, 130, 246, 0.2);
}

/* 训练简介阶段 */
.briefing-stage {
  padding: 40rpx;
}

.briefing-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(59, 130, 246, 0.15);
  border: 1rpx solid rgba(59, 130, 246, 0.1);
}

.briefing-header {
  display: flex;
  align-items: center;
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 1rpx solid rgba(59, 130, 246, 0.1);
}

.briefing-title-area {
  flex: 1;
}

.briefing-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #1e40af;
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
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
  border: 1rpx solid rgba(59, 130, 246, 0.3);
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 32rpx;
}

.warning-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #1e40af;
  margin-bottom: 12rpx;
  display: block;
}

.warning-text {
  font-size: 26rpx;
  color: #1e40af;
  line-height: 1.6;
}

.section-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #1e40af;
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
  border-radius: 16rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: bold;
  transition: all 0.3s ease;
}

.action-btn:active {
  transform: translateY(2rpx) scale(0.98);
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 8rpx 24rpx rgba(59, 130, 246, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  color: #1e40af;
  border: 1rpx solid rgba(59, 130, 246, 0.3);
}

.action-btn.tertiary {
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
  color: #1e40af;
  border: 1rpx solid rgba(59, 130, 246, 0.3);
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
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
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
  color: #3b82f6;
}

.scenario-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 8rpx 32rpx rgba(59, 130, 246, 0.15);
  border: 1rpx solid rgba(59, 130, 246, 0.1);
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
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(59, 130, 246, 0.15);
  border: 1rpx solid rgba(59, 130, 246, 0.1);
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
  color: #1e40af;
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
