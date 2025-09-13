<template>
  <view class="practice-container">
    <view class="header">
      <text class="title">{{
        skillInfo && skillInfo.title ? skillInfo.title + " - 练习" : "技能练习"
      }}</text>
      <text class="subtitle">{{
        skillInfo && skillInfo.content
          ? "练习" + skillInfo.title + "，" + skillInfo.content
          : "在安全环境中练习交往技巧"
      }}</text>
    </view>

    <!-- 技能信息展示 -->
    <view v-if="skillInfo" class="skill-info">
      <view class="skill-card">
        <view class="skill-header">
          <text class="skill-title">{{ skillInfo.title }}</text>
          <view class="difficulty-badge" :class="skillInfo.difficulty">
            <text class="difficulty-text">{{
              getDifficultyText(skillInfo.difficulty)
            }}</text>
          </view>
        </view>
        <text class="skill-content">{{ skillInfo.content }}</text>
        <view class="skill-tags">
          <text v-for="tag in skillInfo.tags" :key="tag" class="skill-tag">{{
            tag
          }}</text>
        </view>
      </view>
    </view>

    <!-- 场景展示模式 -->
    <!-- <view v-if="practiceType === 'scenario' && scenarioData" class="scenario-section">
            <view class="scenario-card">
                <text class="scenario-title">🎬 练习场景</text>
                <view class="scenario-content">
                    <text class="scenario-text">{{ scenarioData.content }}</text>
                </view>
                <view class="scenario-actions">
                    <view class="action-btn primary" @click="startScenarioPractice">
                        <text class="btn-text">开始练习</text>
                    </view>
                    <view class="action-btn secondary" @click="regenerateScenario">
                        <text class="btn-text">重新生成</text>
                    </view>
                </view>
            </view>
        </view> -->
    <view
      v-if="practiceType === 'scenario' && scenarioData"
      class="scenario-section"
    >
      <view class="scenario-card">
        <view class="scenario-header">
          <text class="scenario-title">🎬 练习场景</text>
          <view class="scenario-source" :class="getScenarioSourceClass()">
            <text class="source-icon">{{ getScenarioSourceIcon() }}</text>
            <text class="source-text">{{ getScenarioSourceText() }}</text>
          </view>
        </view>
        <view class="scenario-content">
          <text class="scenario-text">{{ scenarioData.content }}</text>
        </view>
        <view class="scenario-actions">
          <view class="action-btn primary" @click="startScenarioPractice">
            <text class="btn-text">开始练习</text>
          </view>
          <view class="action-btn secondary" @click="regenerateScenario">
            <text class="btn-text">重新生成</text>
          </view>
        </view>
      </view>
    </view>
    <!-- 交互练习模式 -->
    <view
      v-if="practiceType === 'practice' || practiceMode === 'interactive'"
      class="interactive-section"
    >
      <view class="practice-guide">
        <text class="guide-title">💡 练习指导</text>
        <text class="guide-text">
          请根据以下情景，练习运用"{{
            skillInfo?.title
          }}"技巧。我会扮演对话中的另一方，为你提供反馈。
        </text>
      </view>

      <!-- 聊天区域 -->
      <view class="chat-area">
        <view
          v-for="(message, index) in chatMessages"
          :key="index"
          class="message-item"
          :class="message.role"
        >
          <view class="message-avatar">
            <text class="avatar-text">{{
              message.role === "user" ? "我" : "AI"
            }}</text>
          </view>
          <view class="message-content">
            <text class="message-text">{{ message.content }}</text>
          </view>
        </view>

        <view v-if="isAiTyping" class="message-item ai typing">
          <view class="message-avatar">
            <text class="avatar-text">AI</text>
          </view>
          <view class="message-content">
            <view class="typing-indicator">
              <view class="typing-dot"></view>
              <view class="typing-dot"></view>
              <view class="typing-dot"></view>
            </view>
          </view>
        </view>
      </view>

      <!-- 输入区域 -->
      <view class="input-area">
        <view class="input-container">
          <view class="model-btn" @click="showModelSelector">
            <text class="model-text">选择模型</text>
          </view>
          <textarea
            v-model="userInput"
            class="input-field"
            placeholder="输入你的回应..."
            :disabled="isAiTyping"
            @input="handleInput"
          ></textarea>
          <view
            class="send-btn"
            :class="{ disabled: !userInput.trim() || isAiTyping }"
            @click="sendMessage"
          >
            <text class="send-text">发送</text>
          </view>
        </view>
      </view>

      <!-- 选择模型弹窗 -->
      <view
        v-if="showModelModal"
        class="modal-overlay"
        @click="hideModelSelector"
      >
        <view class="modal-content" @click.stop>
          <view class="modal-header">
            <text class="modal-title">选择角色模型</text>
            <view class="modal-close" @click="hideModelSelector">
              <text class="close-text">×</text>
            </view>
          </view>

          <view class="modal-body">
            <view class="form-group">
              <text class="form-label">选择职业</text>
              <view class="profession-grid">
                <view
                  v-for="profession in professionOptions"
                  :key="profession"
                  class="profession-item"
                  :class="{ active: selectedProfession === profession }"
                  @click="selectedProfession = profession"
                >
                  <text class="profession-text">{{ profession }}</text>
                </view>
              </view>
            </view>

            <view class="form-group">
              <text class="form-label">选择年龄段</text>
              <view class="age-grid">
                <view
                  v-for="age in ageOptions"
                  :key="age"
                  class="age-item"
                  :class="{ active: selectedAge === age }"
                  @click="selectedAge = age"
                >
                  <text class="age-text">{{ age }}</text>
                </view>
              </view>
            </view>
          </view>

          <view class="modal-footer">
            <view class="modal-btn cancel" @click="hideModelSelector">
              <text class="btn-text">取消</text>
            </view>
            <view
              class="modal-btn confirm"
              :class="{ disabled: !selectedProfession || !selectedAge }"
              @click="confirmRoleSelection"
            >
              <text class="btn-text">确认</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 练习完成反馈 -->
    <view v-if="practiceCompleted" class="feedback-section">
      <view class="feedback-card">
        <text class="feedback-title">🎉 练习完成</text>
        <view class="feedback-content">
          <text class="feedback-text">{{ practiceResult.feedback }}</text>
        </view>
        <view class="feedback-actions">
          <view class="action-btn secondary" @click="restartPractice">
            <text class="btn-text">再次练习</text>
          </view>
          <view class="action-btn primary" @click="nextSkill">
            <text class="btn-text">学习下一个技巧</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 练习统计 -->
    <view v-if="practiceStats" class="stats-section">
      <text class="stats-title">📊 练习统计</text>
      <view class="stats-grid">
        <view class="stat-item">
          <text class="stat-number">{{ practiceStats.totalPractices }}</text>
          <text class="stat-label">总练习次数</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ practiceStats.masteredSkills }}</text>
          <text class="stat-label">掌握技巧</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ practiceStats.averageScore }}%</text>
          <text class="stat-label">平均得分</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      skillId: "",
      practiceType: "scenario", // scenario, practice
      skillInfo: null,
      scenarioData: null,
      practiceMode: "", // interactive, guided
      chatMessages: [],
      userInput: "",
      isAiTyping: false,
      practiceCompleted: false,
      practiceResult: null,
      practiceStats: null,
      // 模型选择相关
      showModelModal: false,
      selectedProfession: "",
      selectedAge: "",
      professionOptions: [
        "大学生",
        "上班族",
        "老师",
        "医生",
        "销售员",
        "程序员",
        "设计师",
        "心理咨询师",
        "服务员",
        "经理",
        "创业者",
        "自由职业者",
      ],
      ageOptions: [
        "18-22岁",
        "23-28岁",
        "29-35岁",
        "36-45岁",
        "46-55岁",
        "55岁以上",
      ],
    };
  },

  onLoad(options) {
    this.skillId = options.skillId || "";
    this.practiceType = options.type || "scenario";

    // 接收从URL传递的skill信息
    if (options.skillTitle) {
      this.skillInfo = {
        id: options.skillId,
        title: decodeURIComponent(options.skillTitle),
        content: options.skillContent
          ? decodeURIComponent(options.skillContent)
          : "",
        difficulty: options.skillDifficulty || "basic",
        tags: options.skillTags
          ? JSON.parse(decodeURIComponent(options.skillTags))
          : [],
        scenarios: options.skillScenarios
          ? JSON.parse(decodeURIComponent(options.skillScenarios))
          : [],
      };
    }

    this.initializePractice();
  },

  methods: {
    async initializePractice() {
      // 加载技能信息
      await this.loadSkillInfo();

      // 根据练习类型初始化
      if (this.practiceType === "scenario") {
        await this.loadScenario();
      } else {
        await this.startInteractivePractice();
      }

      // 加载练习统计
      await this.loadPracticeStats();
    },

    // async loadSkillInfo() {
    //     // 从存储中获取技能信息（实际项目中应该调用API）
    //     const cachedScenario = uni.getStorageSync('currentScenario');
    //     if (cachedScenario && cachedScenario.skill) {
    //         this.skillInfo = cachedScenario.skill;
    //     }
    // },

    initializeChat() {
      this.chatMessages = [
        {
          role: "ai",
          content: `现在我们要开始"${this.skillInfo?.title}"的情景练习。我会扮演场景中的角色，请你自然地与我对话，运用你学到的技巧。准备好了吗？`,
          type: "instruction",
        },
      ];
    },

    async loadSkillInfo() {
      // 如果从URL已经获取到skillInfo，则不需要重新加载
      if (this.skillInfo && this.skillInfo.title) {
        return;
      }

      // 从存储中获取技能信息（实际项目中应该调用API）
      const cachedScenario = uni.getStorageSync("currentScenario");
      if (cachedScenario && cachedScenario.skill) {
        this.skillInfo = cachedScenario.skill;
      } else {
        // 如果没有缓存的技能信息，使用默认信息
        this.skillInfo = {
          title: "人际交往技巧",
          content: "通过练习提升你的人际交往能力",
          difficulty: "basic",
          tags: ["沟通", "交往", "技巧"],
        };
      }
    },

    // async loadScenario() {
    //     const cachedScenario = uni.getStorageSync('currentScenario');
    //     if (cachedScenario && cachedScenario.scenario) {
    //         this.scenarioData = cachedScenario.scenario;
    //     }
    // },

    async loadScenario() {
      const cachedScenario = uni.getStorageSync("currentScenario");
      if (cachedScenario && cachedScenario.scenario) {
        this.scenarioData = cachedScenario.scenario;
      } else {
        // 如果没有缓存场景，生成一个默认场景
        this.generateFallbackScenario();
      }
    },

    // async regenerateScenario() {
    //     try {
    //         uni.showLoading({ title: '重新生成中...' });

    //         const response = await uni.request({
    //             url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/${this.skillId}/generate-scenario`,
    //             method: 'POST',
    //             header: {
    //                 'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
    //                 'Content-Type': 'application/json'
    //             }
    //         });

    //         if (response.statusCode === 200) {
    //             this.scenarioData = response.data.scenario;
    //         }
    //     } catch (error) {
    //         console.error('重新生成场景失败:', error);
    //         uni.showToast({
    //             title: '生成失败',
    //             icon: 'none'
    //         });
    //     } finally {
    //         uni.hideLoading();
    //     }
    // },

    async regenerateScenario() {
      try {
        uni.showLoading({ title: "重新生成中..." });

        // 尝试调用API生成AI场景
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/${this.skillId}/generate-scenario`,
          method: "POST",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          // AI生成成功
          this.scenarioData = {
            ...response.data.scenario,
            type: "ai_generated", // 标识为AI生成
            source: "api_service", // 来源标识
            generated_at: new Date().toISOString(),
          };

          uni.showToast({
            title: "AI场景生成成功",
            icon: "success",
          });
        } else {
          // API失败时使用备用场景
          this.generateFallbackScenario();
        }
      } catch (error) {
        console.error("重新生成场景失败:", error);
        // 使用备用场景生成
        this.generateFallbackScenario();
      } finally {
        uni.hideLoading();
      }
    },

    startScenarioPractice() {
      this.practiceMode = "interactive";
      this.initializeChat();
    },

    async startInteractivePractice() {
      this.practiceMode = "interactive";
      this.initializeChat();
    },

    initializeChat() {
      this.chatMessages = [
        {
          role: "ai",
          content: `现在我们开始"${this.skillInfo?.title}"的练习！我会扮演情境中的角色，请你自然地与我对话。让我们开始吧！`,
          type: "instruction",
        },
      ];
    },

    handleInput() {
      // 可以添加实时输入反馈
    },

    // async sendMessage() {
    //     if (!this.userInput.trim() || this.isAiTyping) return;

    //     const userMessage = this.userInput.trim();
    //     this.chatMessages.push({
    //         role: 'user',
    //         content: userMessage
    //     });

    //     this.userInput = '';
    //     this.isAiTyping = true;

    //     try {
    //         // 首先尝试调用API
    //         const response = await uni.request({
    //             url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/interactive-practice`,
    //             method: 'POST',
    //             header: {
    //                 'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
    //                 'Content-Type': 'application/json'
    //             },
    //             data: {
    //                 skill_id: this.skillId,
    //                 user_response: userMessage,
    //                 scenario_context: this.scenarioData?.content || ''
    //             }
    //         });

    //         if (response.statusCode === 200) {
    //             const result = response.data;

    //             this.chatMessages.push({
    //                 role: 'ai',
    //                 content: result.ai_feedback
    //             });

    //             if (result.practice_completed) {
    //                 this.practiceCompleted = true;
    //                 this.practiceResult = result;
    //             }
    //         } else {
    //             // API调用失败，使用备用响应
    //             this.handleFallbackResponse(userMessage);
    //         }
    //     } catch (error) {
    //         console.error('发送消息失败:', error);
    //         // 使用备用AI响应而不是直接显示错误
    //         this.handleFallbackResponse(userMessage);
    //     } finally {
    //         this.isAiTyping = false;
    //     }
    // },

    async sendMessage() {
      if (!this.userInput.trim() || this.isAiTyping) return;

      const userMessage = this.userInput.trim();
      this.chatMessages.push({
        role: "user",
        content: userMessage,
      });

      this.userInput = "";
      this.isAiTyping = true;

      try {
        // 检查是否是第一条用户消息（除了欢迎消息）
        const userMessagesCount = this.chatMessages.filter(
          (msg) => msg.role === "user"
        ).length;
        const isFirstMessage = userMessagesCount === 1;

        // 首先尝试调用API
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/interactive-practice`,
          method: "POST",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
            "Content-Type": "application/json",
          },
          data: {
            skill_id: this.skillId,
            user_response: userMessage,
            scenario_context: this.scenarioData?.content || "",
            chat_history: this.chatMessages.slice(-10), // 发送最近10条历史消息
            is_first_message: isFirstMessage,
          },
        });

        if (response.statusCode === 200) {
          const result = response.data;

          // 根据响应类型处理
          if (result.response_type === "roleplay") {
            // 角色扮演模式：AI作为角色回应
            this.chatMessages.push({
              role: "ai",
              content: result.ai_response,
              type: "roleplay",
            });

            if (result.practice_completed) {
              this.practiceCompleted = true;
              this.practiceResult = {
                feedback: `很棒的练习！你在"${
                  this.skillInfo?.title || this.skillInfo?.name
                }"的情景对话中表现出色。`,
                score: Math.floor(Math.random() * 20) + 80,
                improvements: [
                  "在真实情况下也可以尝试运用这些技巧",
                  "注意观察对方的情绪变化",
                  "保持练习，让技巧更加自然",
                ],
              };
            }
          } else {
            // 其他模式（如反馈指导）
            this.chatMessages.push({
              role: "ai",
              content: result.ai_feedback || result.ai_response,
            });

            if (result.practice_completed) {
              this.practiceCompleted = true;
              this.practiceResult = result;
            }
          }
        } else {
          // API调用失败，使用备用响应
          this.handleFallbackRoleplayResponse(userMessage, isFirstMessage);
        }
      } catch (error) {
        console.error("发送消息失败:", error);
        // 使用备用角色扮演响应
        this.handleFallbackRoleplayResponse(
          userMessage,
          this.chatMessages.filter((msg) => msg.role === "user").length === 1
        );
      } finally {
        this.isAiTyping = false;
      }
    },

    handleFallbackRoleplayResponse(userMessage, isFirstMessage) {
      // 备用角色扮演响应逻辑
      const roleplayResponses = {
        conflict_resolution: [
          "我知道你的想法，但我也有我的考虑。我们能不能找个都满意的解决办法？",
          "好吧，我明白你的意思了。那你觉得我们应该怎么办？",
          "我不是故意要让你不舒服的，我们好好谈谈这个问题吧。",
        ],
        listen_actively: [
          "谢谢你愿意听我说...我真的很需要有人理解我现在的感受。",
          "你这样说让我感觉好一些了，我知道你是在乎我的。",
          "我就是觉得压力太大了，不知道该怎么办才好。",
        ],
        express_clearly: [
          "你这样说我能理解，我们确实需要更好地沟通。",
          "我也感觉到了，可能我们之间确实需要多花时间交流。",
          "我没想到会让你有这种感觉，我们谈谈好吗？",
        ],
        romantic_expression: [
          "你这样说让我很开心，我也很珍惜我们在一起的时光。",
          "我能感受到你的用心，这对我来说很重要。",
          "谢谢你总是这么贴心，有你在我身边我很安心。",
        ],
      };

      const responses = roleplayResponses[this.skillId] || [
        "我理解你的想法，让我们继续聊聊这个话题。",
        "你说得对，我们需要更多的沟通和理解。",
        "这确实是个需要我们一起面对的问题。",
      ];

      // 如果是第一条消息，给出更合适的开场回应
      if (isFirstMessage && this.scenarioData?.content) {
        const greetingResponses = {
          conflict_resolution: "我觉得我们需要好好谈谈这个问题...",
          listen_actively: "我最近真的很累，很多事情让我感到压力很大...",
          express_clearly: "我感觉你好像有话要对我说？",
          romantic_expression: "你今天看起来心情不错呢，有什么开心的事吗？",
        };

        const greeting = greetingResponses[this.skillId] || "我们开始聊聊吧。";
        responses.unshift(greeting);
      }

      // 随机选择一个响应
      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];

      // 模拟AI思考时间
      setTimeout(() => {
        this.chatMessages.push({
          role: "ai",
          content: randomResponse,
          type: "roleplay",
        });

        // 随机决定是否结束练习（8轮对话后30%概率）
        if (Math.random() < 0.3 && this.chatMessages.length > 8) {
          this.practiceCompleted = true;
          this.practiceResult = {
            feedback: `很棒的情景对话练习！你在"${
              this.skillInfo?.title || this.skillInfo?.name
            }"中展现了良好的沟通技巧。`,
            score: Math.floor(Math.random() * 20) + 80,
            improvements: [
              "在真实情况下运用这些技巧",
              "继续观察和回应对方的情感",
              "保持练习让沟通更自然",
            ],
          };
        }
      }, 1000 + Math.random() * 1000);
    },

    handleFallbackResponse(userMessage) {
      // 备用AI响应逻辑
      const skillBasedResponses = {
        1: [
          // 主动倾听
          "很好！我能感受到你在认真倾听。下次可以尝试更多的眼神交流来表达关注。",
          "你的回应显示了良好的理解能力。记住，有时候沉默也是一种有力的倾听方式。",
          "不错的表达！可以尝试用复述的方式确认你的理解是否正确。",
        ],
        2: [
          // 情感表达
          '你使用了"我"开头的句式，这很好！这样能避免让对方感到被指责。',
          "你的情感表达很真诚。记住，具体描述感受比模糊表达更有效果。",
          "很好的尝试！下次可以更具体地说出你的需求，这样对方更容易理解。",
        ],
        3: [
          // 非暴力沟通
          "你正在尝试客观描述，这是非暴力沟通的第一步。继续保持！",
          "很好地表达了感受！现在试着说出你的具体需要。",
          "你的请求很明确，这有助于对方理解你的期望。",
        ],
        4: [
          // 情绪识别
          "你展现了良好的观察力！注意对方的非语言信号也很重要。",
          "很好地识别了情绪线索。继续观察语调和肢体语言的变化。",
          "不错的判断！情绪识别需要综合多个信号来确认。",
        ],
        5: [
          // 情感共鸣
          "你显示了很好的共情能力！记住要保持适当的情感边界。",
          "你能理解对方的感受，这很难得。尝试用自己的话重述对方的情感。",
          "很好的换位思考！这样的理解能够建立更深的情感连接。",
        ],
      };

      const responses = skillBasedResponses[this.skillId] || [
        "很好的尝试！继续练习能让你的技巧更加娴熟。",
        "你正在进步！这个技巧需要不断练习才能掌握。",
        "不错的表现！试着在日常生活中也运用这些技巧。",
      ];

      // 随机选择一个响应
      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];

      // 模拟AI思考时间
      setTimeout(() => {
        this.chatMessages.push({
          role: "ai",
          content: randomResponse,
        });

        // 随机决定是否结束练习（30%概率）
        if (Math.random() < 0.3 && this.chatMessages.length > 6) {
          this.practiceCompleted = true;
          this.practiceResult = {
            feedback: `太棒了！你在"${
              this.skillInfo?.title || this.skillInfo?.name
            }"的练习中表现出色。继续在实际生活中运用这些技巧，会让你的人际关系更加和谐！`,
            score: Math.floor(Math.random() * 20) + 80, // 80-100分
            improvements: [
              "继续在日常对话中练习这些技巧",
              "注意观察对方的反应和反馈",
              "保持耐心，技巧的掌握需要时间",
            ],
          };
        }
      }, 1000 + Math.random() * 1000); // 1-2秒的随机延迟
    },

    async regenerateScenario() {
      try {
        uni.showLoading({ title: "重新生成中..." });

        // 尝试调用API
        const response = await uni.request({
          url: `${process.env.VUE_APP_API_BASE_URL}/social-skills/skills/${this.skillId}/generate-scenario`,
          method: "POST",
          header: {
            Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
            "Content-Type": "application/json",
          },
        });

        if (response.statusCode === 200) {
          this.scenarioData = response.data.scenario;
        } else {
          // API失败时使用备用场景
          this.generateFallbackScenario();
        }
      } catch (error) {
        console.error("重新生成场景失败:", error);
        // 使用备用场景生成
        this.generateFallbackScenario();
      } finally {
        uni.hideLoading();
      }
    },

    // generateFallbackScenario() {
    //     const scenarioTemplates = {
    //         '1': [ // 主动倾听
    //             '你的好朋友小李最近工作压力很大，经常加班到很晚。今天TA主动找你聊天，看起来很疲惫，说："我觉得我快撑不下去了..."',
    //             '你的室友刚刚经历了一次失败的考试，现在坐在你旁边，不停地自责："我就是个笨蛋，什么都做不好..."',
    //             '你的恋人今天情绪不太好，你们走在路上时，TA突然停下说："我觉得我们之间好像有些距离了..."'
    //         ],
    //         '2': [ // 情感表达
    //             '你的恋人经常晚回信息，这让你感到被忽视。你们终于有机会面对面交流，你想表达你的感受...',
    //             '你的好朋友答应帮你一个重要的忙，但临时变卦了，让你很失望。你决定和TA谈谈...',
    //             '你在小组作业中承担了大部分工作，而其他成员贡献很少。你感到不公平，想要表达你的想法...'
    //         ],
    //         '3': [ // 非暴力沟通
    //             '你和室友因为生活习惯问题发生了冲突。TA经常不洗碗，房间很乱，你决定用非暴力沟通的方式解决这个问题...',
    //             '你的伴侣最近经常工作到很晚，你们的相处时间变少了。你想表达你的需要，但不想让TA感到压力...',
    //             '你在团队项目中和同伴有不同的想法，讨论变得有些激烈。你想要化解冲突，寻找共同解决方案...'
    //         ],
    //         '4': [ // 情绪识别
    //             '你在咖啡厅里观察到一位同学。TA坐在角落，不时看手机，眉头紧锁，手指在桌上轻敲。你觉得TA可能...',
    //             '你的朋友在聚会上表现得很活跃，但你注意到TA的笑容有些勉强，眼神时常飘向远方。你感觉...',
    //             '你的同事在会议上发言时声音比平时高，语速也比较快，双手有些颤抖。你观察到...'
    //         ],
    //         '5': [ // 情感共鸣
    //             '你的朋友刚刚失恋了，TA看起来很伤心，对你说："我觉得我永远找不到真爱了..."你想要理解并支持TA...',
    //             '你的同学因为家庭经济困难而感到压力很大，TA羞愧地说："我可能要退学了..."你想要表达理解和支持...',
    //             '你的室友因为找工作屡次被拒而沮丧，TA说："我是不是真的很差劲？"你想要给予TA情感支持...'
    //         ]
    //     };

    //     const scenarios = scenarioTemplates[this.skillId] || scenarioTemplates['1'];
    //     const randomScenario = scenarios[Math.floor(Math.random() * scenarios.length)];

    //     this.scenarioData = {
    //         content: randomScenario,
    //         type: 'generated',
    //         skill_focus: this.skillInfo?.title || '人际交往技巧'
    //     };

    //     uni.showToast({
    //         title: '场景已重新生成',
    //         icon: 'success'
    //     });
    // },

    generateFallbackScenario() {
      // 优先使用skill中的scenarios数据
      if (
        this.skillInfo &&
        this.skillInfo.scenarios &&
        this.skillInfo.scenarios.length > 0
      ) {
        const randomScenarioTitle =
          this.skillInfo.scenarios[
            Math.floor(Math.random() * this.skillInfo.scenarios.length)
          ];
        const scenarioContent = this.generateScenarioContentFromTitle(
          randomScenarioTitle,
          this.skillInfo.title
        );

        this.scenarioData = {
          content: scenarioContent,
          source: "skill-based",
        };
        return;
      }

      // 基于技能类型生成场景
      const skillBasedTemplates = {
        ice_breaking: [
          `你在${
            (this.skillInfo.scenarios && this.skillInfo.scenarios[0]) || "聚会"
          }上遇到了一个看起来很有趣的人，但你们还不认识。现在是开始对话的好时机，尝试用${
            this.skillInfo.title
          }来打破僵局...`,
          `你刚加入一个新的学习小组，大家都在自由交流。你想要融入其中，需要运用${this.skillInfo.title}来开启对话...`,
        ],
        listen_actively: [
          `你的好朋友遇到了困难，主动找你倾诉。现在需要运用${this.skillInfo.title}技巧，真正理解TA的感受和需求...`,
          `在小组讨论中，有同学提出了不同的观点。作为一个好的倾听者，你需要运用${this.skillInfo.title}来理解对方的想法...`,
        ],
        express_clearly: [
          `你对朋友的某个行为感到困扰，但不想伤害你们的友谊。现在是运用${this.skillInfo.title}技巧，真诚而清晰地表达感受的时候...`,
          `在团队合作中，你有不同的想法需要表达。运用${this.skillInfo.title}，让你的观点被准确理解...`,
        ],
      };

      const scenarios = skillBasedTemplates[this.skillInfo.id] || [
        `现在是练习${this.skillInfo.title}的时候。想象一个需要运用这项技能的情况，准备开始你的练习...`,
      ];
      const randomScenario =
        scenarios[Math.floor(Math.random() * scenarios.length)];

      this.scenarioData = {
        content: randomScenario,
        type: "fallback", // 标识为备用场景
        source: "local_template", // 来源标识
        skill_focus: this.skillInfo?.title || "人际交往技巧",
        generated_at: new Date().toISOString(),
      };

      uni.showToast({
        title: "场景已重新生成",
        icon: "success",
      });
    },

    generateScenarioContentFromTitle(scenarioTitle, skillTitle) {
      // 基于scenario标题和技能标题生成具体场景内容
      const scenarioMappings = {
        朋友倾诉烦恼: `你的好朋友最近遇到了一些困难，今天TA主动找你聊天，看起来很苦恼。现在是运用${skillTitle}技巧的好时机，帮助TA感受到被理解和支持...`,
        恋人分享心事: `你的恋人想要和你分享内心的想法，但似乎有些犹豫。作为亲密的伴侣，你需要运用${skillTitle}来创造安全的交流环境...`,
        同学讨论问题: `在课堂讨论中，同学们对某个问题有不同的看法。现在轮到你发言了，如何运用${skillTitle}来有效参与这次讨论？`,
        表达不满: `室友的某些行为让你感到不舒服，但你不想伤害你们的关系。现在需要运用${skillTitle}技巧，真诚而建设性地表达你的感受...`,
        提出需求: `你需要朋友帮助你完成一个重要任务，但不确定如何开口。运用${skillTitle}技巧，清晰而友善地表达你的需求...`,
        分享感受: `你今天有了一个重要的感悟想要分享给身边的人，如何运用${skillTitle}让对方真正理解你的感受？`,
        初次约会: `这是你们的第一次约会，气氛有些紧张。运用${skillTitle}技巧来缓解紧张气氛，让对话自然而愉快地进行...`,
        朋友聚会: `在朋友聚会上，大家正在热烈讨论一个话题。如何运用${skillTitle}加入对话，让交流更加深入和有意义？`,
        课堂讨论: `老师提出了一个开放性问题，课堂上的讨论刚开始。运用${skillTitle}技巧来参与这次学术交流...`,
        新同学: `班上来了新同学，TA看起来有些拘谨。作为班级的一员，你想要主动接近，运用${skillTitle}来建立友好的第一印象...`,
        聚会认识: `在社团活动中，你遇到了一些新面孔。这是拓展社交圈的好机会，如何运用${skillTitle}来开始新的友谊？`,
        社团活动: `社团招新活动正在进行，你既想了解社团，也想展现自己。运用${skillTitle}技巧来进行有效的交流...`,
      };

      return (
        scenarioMappings[scenarioTitle] ||
        `现在是练习${skillTitle}的时候。场景：${scenarioTitle}。请运用你所学的技巧来应对这个情况...`
      );
    },

    async loadPracticeStats() {
      // 模拟练习统计数据
      this.practiceStats = {
        totalPractices: 12,
        masteredSkills: 8,
        averageScore: 85,
      };
    },

    restartPractice() {
      this.practiceCompleted = false;
      this.practiceResult = null;
      this.chatMessages = [];
      this.initializeChat();
    },

    nextSkill() {
      uni.showToast({
        title: "即将推荐下一个技巧",
        icon: "success",
      });

      setTimeout(() => {
        uni.navigateBack();
      }, 1500);
    },

    getDifficultyText(difficulty) {
      const map = {
        basic: "基础",
        intermediate: "进阶",
        advanced: "高级",
      };
      return map[difficulty] || "基础";
    },

    getScenarioSourceIcon() {
      if (!this.scenarioData) return "📝";

      switch (this.scenarioData.type) {
        case "ai_generated":
          return "🤖";
        case "fallback":
          return "📚";
        default:
          return "📝";
      }
    },

    getScenarioSourceText() {
      if (!this.scenarioData) return "标准场景";

      switch (this.scenarioData.type) {
        case "ai_generated":
          return "AI智能生成";
        case "fallback":
          return "经典场景";
        default:
          return "标准场景";
      }
    },

    getScenarioSourceClass() {
      if (!this.scenarioData) return "source-default";

      switch (this.scenarioData.type) {
        case "ai_generated":
          return "source-ai";
        case "fallback":
          return "source-fallback";
        default:
          return "source-default";
      }
    },

    // 添加一个方法来检查当前场景是否为AI生成
    isAIGeneratedScenario() {
      return this.scenarioData && this.scenarioData.type === "ai_generated";
    },

    // 调试方法：在控制台输出场景信息
    debugScenarioInfo() {
      console.log("场景调试信息:", {
        type: this.scenarioData?.type,
        source: this.scenarioData?.source,
        isAI: this.isAIGeneratedScenario(),
        generatedAt: this.scenarioData?.generated_at,
        content: this.scenarioData?.content?.substring(0, 50) + "...",
      });
    },

    // 模型选择相关方法
    showModelSelector() {
      this.showModelModal = true;
      // 重置选择
      this.selectedProfession = "";
      this.selectedAge = "";
    },

    hideModelSelector() {
      this.showModelModal = false;
    },

    confirmRoleSelection() {
      if (!this.selectedProfession || !this.selectedAge) {
        uni.showToast({
          title: "请选择职业和年龄",
          icon: "none",
        });
        return;
      }

      // 构建角色扮演提示语句
      const roleMessage = `我希望你在该场景中扮演一个${this.selectedAge}的${this.selectedProfession}这样的角色配合我练习，请根据这个身份特点来回应我的对话。`;

      // 添加到聊天消息
      this.chatMessages.push({
        role: "user",
        content: roleMessage,
        type: "role_setting",
      });

      // 隐藏弹窗
      this.hideModelSelector();

      // 发送AI响应
      this.isAiTyping = true;

      setTimeout(() => {
        this.chatMessages.push({
          role: "ai",
          content: `好的，我现在会以${this.selectedAge}的${this.selectedProfession}的身份与你对话。让我们开始练习吧！`,
          type: "role_confirmation",
        });
        this.isAiTyping = false;
      }, 1000);

      uni.showToast({
        title: `已设置角色：${this.selectedAge}的${this.selectedProfession}`,
        icon: "success",
      });
    },
  },
};
</script>

<style scoped>
.practice-container {
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

.skill-info {
  padding: 40rpx;
}

.skill-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.skill-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.difficulty-badge {
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 20rpx;
}

.difficulty-badge.basic {
  background-color: #e8f5e8;
  color: #4caf50;
}

.difficulty-badge.intermediate {
  background-color: #fff3e0;
  color: #ff9800;
}

.difficulty-badge.advanced {
  background-color: #ffebee;
  color: #f44336;
}

.skill-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20rpx;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background-color: #f0f0f0;
  color: #666;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
}

.scenario-section {
  padding: 0 40rpx 40rpx;
}

.scenario-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.scenario-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.scenario-content {
  background-color: #f8f9fa;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.scenario-text {
  font-size: 28rpx;
  color: #555;
  line-height: 1.7;
}

.scenario-actions {
  display: flex;
  gap: 16rpx;
}

.interactive-section {
  padding: 0 40rpx 40rpx;
}

.practice-guide {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.guide-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.guide-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.chat-area {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  min-height: 400rpx;
  max-height: 600rpx;
  overflow-y: auto;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.message-item {
  display: flex;
  margin-bottom: 24rpx;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 16rpx;
}

.user .message-avatar {
  background-color: #667eea;
  color: white;
}

.ai .message-avatar {
  background-color: #f0f0f0;
  color: #666;
}

.avatar-text {
  font-size: 20rpx;
  font-weight: bold;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-text {
  background-color: #f8f9fa;
  padding: 20rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.5;
  display: block;
}

.user .message-text {
  background-color: #667eea;
  color: white;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background-color: #f8f9fa;
  border-radius: 16rpx;
  gap: 8rpx;
}

.typing-dot {
  width: 12rpx;
  height: 12rpx;
  background-color: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(1);
    opacity: 0.5;
  }

  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.input-area {
  padding: 0 40rpx 40rpx;
  position: sticky;
  bottom: 0;
  background-color: #f5f5f5;
}

.input-container {
  display: flex;
  background-color: white;
  border-radius: 50rpx;
  padding: 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  align-items: flex-end;
  gap: 12rpx;
}

.model-btn {
  background-color: #f0f0f0;
  color: #666;
  padding: 20rpx 24rpx;
  border-radius: 40rpx;
  font-size: 24rpx;
  white-space: nowrap;
  border: 1rpx solid #e0e0e0;
}

.model-btn:active {
  background-color: #e0e0e0;
}

.input-field {
  flex: 1;
  min-height: 80rpx;
  max-height: 200rpx;
  padding: 20rpx;
  font-size: 28rpx;
  border: none;
  background: transparent;
  resize: none;
}

.send-btn {
  background-color: #667eea;
  color: white;
  padding: 20rpx 32rpx;
  border-radius: 40rpx;
  font-size: 28rpx;
}

.send-btn.disabled {
  background-color: #ccc;
  color: #999;
}

.action-btn {
  flex: 1;
  padding: 20rpx;
  border-radius: 12rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: bold;
}

.action-btn.primary {
  background-color: #667eea;
  color: white;
}

.action-btn.secondary {
  background-color: #f0f0f0;
  color: #666;
}

.feedback-section {
  padding: 0 40rpx 40rpx;
}

.feedback-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.feedback-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.feedback-content {
  margin-bottom: 32rpx;
}

.feedback-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.feedback-actions {
  display: flex;
  gap: 16rpx;
}

.stats-section {
  padding: 0 40rpx 40rpx;
}

.stats-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
  display: block;
}

.stats-grid {
  display: flex;
  gap: 20rpx;
}

.stat-item {
  flex: 1;
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

.scenario-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.scenario-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.scenario-source {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
}

.scenario-source.source-ai {
  background-color: #e8f5e8;
  color: #4caf50;
  border: 1rpx solid #4caf50;
}

.scenario-source.source-fallback {
  background-color: #fff3e0;
  color: #ff9800;
  border: 1rpx solid #ff9800;
}

.scenario-source.source-default {
  background-color: #f0f0f0;
  color: #666;
}

.source-icon {
  font-size: 20rpx;
}

.source-text {
  font-weight: bold;
}

/* 模型选择弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 16rpx;
  width: 90%;
  max-width: 600rpx;
  max-height: 80vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.modal-close {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f5f5f5;
}

.close-text {
  font-size: 36rpx;
  color: #999;
  line-height: 1;
}

.modal-body {
  padding: 32rpx;
  max-height: 60vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 40rpx;
}

.form-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.profession-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.profession-item {
  background-color: #f8f9fa;
  border: 2rpx solid #e9ecef;
  border-radius: 12rpx;
  padding: 16rpx 24rpx;
  font-size: 26rpx;
  color: #666;
  text-align: center;
  min-width: 140rpx;
}

.profession-item.active {
  background-color: #667eea;
  border-color: #667eea;
  color: white;
}

.age-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.age-item {
  background-color: #f8f9fa;
  border: 2rpx solid #e9ecef;
  border-radius: 12rpx;
  padding: 16rpx 24rpx;
  font-size: 26rpx;
  color: #666;
  text-align: center;
  min-width: 120rpx;
}

.age-item.active {
  background-color: #667eea;
  border-color: #667eea;
  color: white;
}

.modal-footer {
  display: flex;
  padding: 32rpx;
  border-top: 1rpx solid #f0f0f0;
  gap: 20rpx;
}

.modal-btn {
  flex: 1;
  padding: 24rpx;
  border-radius: 12rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: bold;
}

.modal-btn.cancel {
  background-color: #f8f9fa;
  color: #666;
  border: 1rpx solid #e9ecef;
}

.modal-btn.confirm {
  background-color: #667eea;
  color: white;
}

.modal-btn.confirm.disabled {
  background-color: #ccc;
  color: #999;
}
</style>
