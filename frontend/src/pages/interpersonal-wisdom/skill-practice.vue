<template>
  <view class="practice-container">    <!-- 技能信息展示 -->
    <view v-if="skillInfo" class="skill-info">
      <view class="skill-card">
        <view class="skill-header">
          <text class="skill-title">{{ skillInfo.title }}</text>
        </view>
        <text class="skill-content">{{ skillInfo.content }}</text>
        <view class="skill-tags">
          <text v-for="tag in skillInfo.tags" :key="tag" class="skill-tag">{{
            tag
          }}</text>
        </view>
      </view>
    </view>

    <view v-if="practiceType === 'scenario' && scenarioData" class="scenario-section">
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
    <view v-if="practiceType === 'practice' || practiceMode === 'interactive'" class="interactive-section">
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
        <view v-for="(message, index) in chatMessages" :key="index" class="message-item" :class="message.role">
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
          <textarea v-model="userInput" class="input-field" placeholder="输入你的回应..." :disabled="isAiTyping"
            @input="handleInput"></textarea>
          <view class="send-btn" :class="{ disabled: !userInput.trim() || isAiTyping }" @click="sendMessage">
            <text class="send-text">发送</text>
          </view>
        </view>
      </view>

      <!-- 选择模型弹窗 -->
      <view v-if="showModelModal" class="modal-overlay" @click="hideModelSelector">
        <view class="modal-content" @click.stop>
          <view class="modal-header">
            <text class="modal-title">选择角色模型</text>
            <view class="modal-close" @click="hideModelSelector">
              <text class="close-text">×</text>
            </view>
          </view>

          <view class="modal-body">
            <view class="form-group">
              <text class="form-label">AI扮演职业</text>
              <view class="profession-grid">
                <view v-for="profession in aiProfessionOptions" :key="profession" class="profession-item"
                  :class="{ active: selectedAiProfession === profession }" @click="selectedAiProfession = profession">
                  <text class="profession-text">{{ profession }}</text>
                </view>
              </view>
            </view>

            <view class="form-group">
              <text class="form-label">我的职业</text>
              <view class="profession-grid">
                <view v-for="profession in myProfessionOptions" :key="profession" class="profession-item"
                  :class="{ active: selectedMyProfession === profession }" @click="selectedMyProfession = profession">
                  <text class="profession-text">{{ profession }}</text>
                </view>
              </view>
            </view>

            <view class="form-group">
              <text class="form-label">选择年龄段</text>
              <view class="age-grid">
                <view v-for="age in ageOptions" :key="age" class="age-item" :class="{ active: selectedAge === age }"
                  @click="selectedAge = age">
                  <text class="age-text">{{ age }}</text>
                </view>
              </view>
            </view>

            <view class="form-group">
              <text class="form-label">AI性格特点</text>
              <view class="personality-grid">
                <view v-for="personality in personalityOptions" :key="personality" class="personality-item"
                  :class="{ active: selectedPersonality === personality }" @click="selectedPersonality = personality">
                  <text class="personality-text">{{ personality }}</text>
                </view>
              </view>
            </view>

            <view class="form-group">
              <text class="form-label">情景设定</text>
              <textarea v-model="aiBackground" class="background-input" :placeholder="aiBackground || '请提供一个合适且具体的情景'"
                maxlength="200"></textarea>
              <text class="char-count">{{ aiBackground.length }}/200</text>
            </view>
          </view>

          <view class="modal-footer">
            <view class="modal-btn cancel" @click="hideModelSelector">
              <text class="btn-text">取消</text>
            </view>
            <view class="modal-btn confirm" :class="{
              disabled:
                !selectedAiProfession ||
                !selectedMyProfession ||
                !selectedAge ||
                !selectedPersonality,
            }" @click="confirmRoleSelection">
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

  </view>
</template>

<script>
export default {
  data() {
    return {
      skillId: "",
      scenarioId: "",
      practiceType: "scenario", // scenario, practice
      skillInfo: null,
      scenarioData: null,
      currentScenario: null, // 添加当前场景信息
      practiceMode: "", // interactive, guided
      chatMessages: [],
      userInput: "",
      isAiTyping: false,
      practiceCompleted: false,
      practiceResult: null,
      practiceStats: null,
      // 模型选择相关
      showModelModal: false,
      selectedAiProfession: "",
      selectedMyProfession: "",
      selectedAge: "",
      selectedPersonality: "",
      aiBackground: "",
      aiProfessionOptions: [
        "大学同学",
        "职场同事",
        "老师",
        "医生",
        "销售专员",
        "程序员",
        "设计师",
        "心理咨询师",
        "服务员",
        "部门经理",
        "创业者",
        "朋友",
        "陌生人",
        "面试官",
        "客户",
        "合作伙伴",
      ],
      myProfessionOptions: [
        "大学生",
        "应届毕业生",
        "职场新人",
        "资深员工",
        "管理者",
        "创业者",
        "自由职业者",
        "求职者",
        "实习生",
        "项目经理",
        "技术专家",
        "销售代表",
      ],
      ageOptions: [
        "18-22岁",
        "23-28岁",
        "29-35岁",
        "36-45岁",
        "46-55岁",
        "55岁以上",
      ],
      personalityOptions: [
        "友善开朗",
        "严肃认真",
        "幽默风趣",
        "温和耐心",
        "直率坦诚",
        "细致体贴",
        "活泼外向",
        "沉稳内敛",
        "专业权威",
        "随和亲切",
        "积极乐观",
        "冷静理性",
      ],
    };
  },

  onLoad(options) {
    this.skillId = options.skillId || "";
    this.practiceType = options.type || "scenario";
    this.scenarioId = options.scenarioId || "";

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

    // 接收场景信息
    if (options.scenarioTitle && options.scenarioDescription) {
      this.currentScenario = {
        id: options.scenarioId,
        title: decodeURIComponent(options.scenarioTitle),
        description: decodeURIComponent(options.scenarioDescription)
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
      // 如果有从detail页面传递的场景信息，优先使用
      if (this.currentScenario) {
        this.scenarioData = {
          title: `${this.skillInfo?.title || '技能'} - ${this.currentScenario.title}`,
          content: `🎯 开始进行「${this.skillInfo?.title || '技能'}」技能练习\n\n📝 练习场景：${this.currentScenario.description}\n\n请准备开始练习，AI将扮演场景中的对话方，你来运用${this.skillInfo?.title || '相关'}技巧与AI进行互动。`,
          source: "detail_page",
          scenario_info: this.currentScenario
        };
        return;
      }

      // 否则尝试从缓存加载
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
      // 生成基础情景
      const baseScenario = this.generateBaseScenario();

      this.chatMessages = [
        {
          role: "ai",
          content: `现在我们开始"${this.skillInfo?.title}"的练习！\n\n【情景设定】\n${baseScenario}\n\n我会扮演情境中的角色，请你自然地与我对话，运用你学到的技巧。准备好了吗？`,
          type: "instruction",
        },
      ];
    },

    generateBaseScenario() {
      // 根据技能类型生成基础情景
      const skillBasedScenarios = {
        ice_breaking: [
          "你在一个朋友的生日聚会上，注意到角落里有个看起来很有趣但还不认识的人。现在是个打破僵局、开始对话的好机会。",
          "你刚加入了一个新的兴趣小组，大家正在自由交流。你想要融入这个群体，需要主动与他人建立联系。",
          "在咖啡厅排队时，你和前面的人因为都在看同一本书而有了共同话题的契机。",
        ],
        listen_actively: [
          "你的朋友看起来心情不太好，主动约你出来聊天。TA似乎有很多话想说，但又有些犹豫。",
          "在小组讨论中，有同学分享了一个比较私人的经历，现在需要有人给予回应和支持。",
          "你的室友刚刚经历了一些挫折，正坐在床边默默流泪，你想要了解情况并给予帮助。",
        ],
        express_clearly: [
          "你对朋友最近的某个行为感到困扰，但不想伤害你们的友谊。现在你们有机会私下谈谈。",
          "在团队项目中，你有不同的想法需要表达，但担心会引起冲突。项目讨论会即将开始。",
          "你需要向家人表达自己的一个重要决定，但担心他们不理解或不支持。",
        ],
      };

      const scenarios = skillBasedScenarios[this.skillInfo?.id] || [
        "你和一个新认识的人在一个轻松的环境中开始对话，双方都希望能够进行有效的交流。",
        "在日常生活的某个场合，你遇到了需要运用人际交往技巧的情况。",
        "你面临一个需要与他人沟通的场景，这是练习和提升交往能力的好机会。",
      ];

      return scenarios[Math.floor(Math.random() * scenarios.length)];
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
                feedback: `很棒的练习！你在"${this.skillInfo?.title || this.skillInfo?.name
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
        // 数字ID映射（来自 category-detail.vue）
        1: [  // 主动倾听
          "谢谢你愿意听我说...我真的很需要有人理解我现在的感受。",
          "你这样说让我感觉好一些了，我知道你是在乎我的。",
          "我就是觉得压力太大了，不知道该怎么办才好。",
        ],
        2: [  // 情感表达
          "你这样说我能理解，我们确实需要更好地沟通。",
          "我也感觉到了，可能我们之间确实需要多花时间交流。",
          "我没想到会让你有这种感觉，我们谈谈好吗？",
        ],
        3: [  // 非暴力沟通
          "我知道你的想法，但我也有我的考虑。我们能不能找个都满意的解决办法？",
          "好吧，我明白你的意思了。那你觉得我们应该怎么办？",
          "我不是故意要让你不舒服的，我们好好谈谈这个问题吧。",
        ],
        4: [  // 情绪识别
          "我现在的心情有点复杂，你能看出来吗？",
          "你觉得我现在是什么感受？",
          "我试着表达我的情绪，你能理解吗？",
        ],
        5: [  // 情感共鸣
          "我需要有人能理解我的感受...",
          "你能想象一下我现在的心情吗？",
          "我希望你能站在我的角度想想。",
        ],
        6: [  // 情绪调节
          "我现在情绪有点激动，需要冷静一下。",
          "我在努力控制自己的情绪，给我一点时间。",
          "这种情况让我很难保持平静。",
        ],
        7: [  // 破冰技巧
          "你好！很高兴认识你，我们聊聊吧。",
          "这个活动怎么样？你玩得开心吗？",
          "我是新来的，你能给我介绍一下这里吗？",
        ],
        8: [  // 信任建立
          "我觉得我们需要建立更深的信任关系。",
          "你相信我会遵守我的承诺吗？",
          "我希望你能信任我，我会证明给你看的。",
        ],
        9: [  // 冲突解决
          "我知道你的想法，但我也有我的考虑。我们能不能找个都满意的解决办法？",
          "好吧，我明白你的意思了。那你觉得我们应该怎么办？",
          "我不是故意要让你不舒服的，我们好好谈谈这个问题吧。",
        ],
        10: [ // 职场沟通
          "关于这个项目，我有一些想法想和你讨论。",
          "我们需要更专业地处理这个问题。",
          "让我们用更正式的方式来沟通这件事。",
        ],
        11: [ // 异地恋维护
          "虽然我们相隔很远，但我一直想着你。",
          "距离让我更珍惜我们在一起的时光。",
          "我们需要找到更好的方式保持联系。",
        ],
        12: [ // 危机干预
          "我很担心你，你现在还好吗？",
          "我注意到你最近情绪不太对，想聊聊吗？",
          "如果你需要帮助，我会一直在这里。",
        ],
        // 保留原有的字符串键以保持兼容性
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
        // 沟通表达新增技能 (ID 13-25)
        13: [ // 非正式场合交流
          "我们今天聊得很轻松，这种感觉真好。",
          "你总是能让谈话变得有趣，我很喜欢这样。",
          "我们可以随便聊聊，不用那么拘束。",
        ],
        14: [ // 正式场合表达
          "感谢您给我这个机会在此发言。",
          "我很荣幸能在这个重要场合与大家分享。",
          "请允许我正式地表达我的观点。",
        ],
        15: [ // 书面沟通
          "您的邮件我已收到，我会仔细考虑您的建议。",
          "关于您提到的事项，我会以书面形式详细回复。",
          "我们还是用文字记录下来比较好。",
        ],
        16: [ // 跨代沟通
          "我想了解您那个年代的经历，能跟我分享吗？",
          "现在的年轻人想法确实和我们那时候不太一样。",
          "我们虽然年龄不同，但我相信能找到共同语言。",
        ],
        17: [ // 群体演讲
          "感谢大家今天的到来，我很激动能在这里分享。",
          "我希望我的分享能给大家带来一些启发。",
          "有什么问题欢迎大家随时提出。",
        ],
        18: [ // 辩论技巧
          "我理解您的观点，但我有不同的看法。",
          "让我从另一个角度来分析这个问题。",
          "证据显示我们需要重新考虑这个问题。",
        ],
        19: [ // 说服技巧
          "我想您一定会看到这个建议的价值。",
          "让我们一起来看看这样做的好处。",
          "我相信您会做出明智的决定。",
        ],
        20: [ // 故事叙述
          "让我给你讲一个有趣的故事。",
          "这让我想起了一件往事...",
          "你的经历让我想起了我自己的故事。",
        ],
        21: [ // 幽默运用
          "你总是能让我笑起来，真是太好了。",
          "哈哈，你这个比喻太生动了！",
          "你的幽默感总是让气氛变得轻松。",
        ],
        22: [ // 情感沟通
          "我想和你分享我内心真实的感受。",
          "能够对你敞开心扉，我感到很安全。",
          "谢谢你愿意听我说这些。",
        ],
        23: [ // 赞美表达
          "谢谢你的夸奖，这让我很开心。",
          "你也很棒，我们互相学习吧。",
          "能得到你的认可对我来说很重要。",
        ],
        24: [ // 批评反馈
          "我知道你是为我好，我会认真考虑的。",
          "谢谢你的诚实反馈，我需要改进。",
          "我会努力改正的，希望你能继续支持我。",
        ],
        25: [ // 远程沟通
          "虽然我们不在一个地方，但我感觉我们很近。",
          "视频通话让我们的交流更加直接。",
          "技术真的让远程交流变得容易多了。",
        ],
        // 情感理解新增技能 (ID 26-38)
        26: [ // 情感词汇
          "你用这个词形容得很准确，我确实是这种感觉。",
          "我需要更精确地表达我的情感状态。",
          "谢谢你帮我找到了合适的词语。",
        ],
        27: [ // 同理心训练
          "你能理解我的感受，这让我很感动。",
          "谢谢你站在我的角度想问题。",
          "你的共情让我感到被理解了。",
        ],
        28: [ // 情感边界
          "我需要一些时间来处理自己的情绪。",
          "我很乐意帮你，但我也要照顾好自己。",
          "我们都需要保持情感的平衡。",
        ],
        29: [ // 情绪传染
          "你的好心情感染了我，我也开心起来了。",
          "我努力不让负面情绪影响到别人。",
          "我们一起保持积极的态度吧。",
        ],
        30: [ // 情感支持
          "有你的支持我感觉好多了。",
          "我知道你会一直在我身边。",
          "谢谢你在我困难时陪伴我。",
        ],
        31: [ // 创伤敏感
          "我需要慢慢来，这对我来说有点难。",
          "谢谢你的耐心和理解。",
          "我还没准备好谈论这个话题。",
        ],
        32: [ // 情感复原
          "我正在从那段经历中慢慢恢复。",
          "虽然很困难，但我相信会好起来的。",
          "我学会了从挫折中成长。",
        ],
        33: [ // 情感表达艺术
          "我想用画画来表达我的心情。",
          "音乐能够表达我无法言喻的感受。",
          "创作让我的情感得到了释放。",
        ],
        34: [ // 情感记忆
          "那段回忆现在对我来说有了不同的意义。",
          "我正在学习如何处理过去的痛苦。",
          "好的回忆让我更有力量面对困难。",
        ],
        35: [ // 情感成熟
          "我学会了控制自己的冲动。",
          "成熟就是学会承担情感责任。",
          "我在理性和感性之间找到了平衡。",
        ],
        36: [ // 情感智慧
          "我开始理解情感背后的深层需求。",
          "智慧地处理情感需要时间和经验。",
          "我愿意分享我的情感智慧。",
        ],
        37: [ // 正念情感
          "我正在观察自己的情绪变化。",
          "不评判地体验情感是很好的练习。",
          "正念让我更了解自己的内心。",
        ],
        38: [ // 情感沟通
          "我想坦诚地和你分享我的感受。",
          "在亲密关系中开放地沟通很重要。",
          "谢谢你愿意听我表达真实的情感。",
        ],
        // 关系建立新增技能 (ID 39-51)
        39: [ // 自我介绍
          "很高兴认识你！让我介绍一下自己。",
          "谢谢你的介绍，现在轮到我了。",
          "我想让你更了解我一些。",
        ],
        40: [ // 破冰对话
          "这个活动很有趣，你觉得呢？",
          "我们聊聊天吧，别那么拘束。",
          "你好！我注意到你也在这里。",
        ],
        41: [ // 共同话题
          "哇，你也喜欢这个！我们有共同爱好呢。",
          "看来我们想法很相似。",
          "这让我想起了我的经历，和你的很像。",
        ],
        42: [ // 信任建立
          "我说到做到，你可以相信我。",
          "建立信任需要时间，我愿意等待。",
          "我希望通过行动证明我的可靠性。",
        ],
        43: [ // 社交恐惧
          "我有点紧张，但我想尝试和你聊天。",
          "虽然我不太擅长社交，但我想努力。",
          "谢谢你的耐心，这对我来说有点困难。",
        ],
        44: [ // 网络社交
          "线上聊天也能感受到你的热情。",
          "虽然不能面对面，但我们的交流很真诚。",
          "技术让我们能够跨越距离交流。",
        ],
        45: [ // 跨文化交流
          "我想了解你的文化背景。",
          "文化差异让我们的交流更有趣。",
          "尽管背景不同，我们还是能找到共同点。",
        ],
        46: [ // 关系维护
          "我想我们应该保持联系。",
          "虽然时间过去了，但我们的友谊依然珍贵。",
          "我会记得这些重要的时刻。",
        ],
        47: [ // 关系边界
          "我需要一些个人空间，希望你能理解。",
          "我们的友谊很重要，但我也需要保持独立。",
          "我尊重你的边界，也希望你尊重我的。",
        ],
        48: [ // 群体融入
          "我想融入这个团队，你能帮我吗？",
          "作为新人，我正在努力适应这里。",
          "我希望能为这个群体贡献自己的力量。",
        ],
        49: [ // 社交影响力
          "我希望能够激励和鼓舞身边的人。",
          "让我们一起创造积极的氛围。",
          "我相信我们能够互相影响，变得更好。",
        ],
        50: [ // 关系修复
          "我想我们需要谈谈我们之间的问题。",
          "我愿意为我的错误道歉。",
          "我们的关系对我很重要，我想修复它。",
        ],
        51: [ // 社交礼仪
          "请允许我按照礼仪来进行这次对话。",
          "我想展现良好的教养和修养。",
          "适当的礼仪让我们的交流更愉快。",
        ],
        // 特殊情境新增技能 (ID 52-65)
        52: [ // 医患沟通
          "医生，我有些担心，能详细解释一下吗？",
          "谢谢您的耐心解释，我现在明白了。",
          "我相信您的专业建议。",
        ],
        53: [ // 师生互动
          "老师，我对这个问题有不同的看法。",
          "感谢您的指导，我学到了很多。",
          "您能再解释一下这个概念吗？",
        ],
        54: [ // 客服技巧
          "谢谢您的耐心服务，问题解决了。",
          "我对服务有些不满意，希望能得到改善。",
          "您的专业态度让我很满意。",
        ],
        55: [ // 销售沟通
          "您的建议很有道理，我需要考虑一下。",
          "这个产品确实符合我的需求。",
          "我想了解更多的细节信息。",
        ],
        56: [ // 法庭辩论
          "我对这个论点有异议。",
          "证据显示情况并非如此。",
          "我要为我的当事人争取权益。",
        ],
        57: [ // 媒体采访
          "我想澄清一下刚才的报道。",
          "这个问题涉及多个方面。",
          "我需要谨慎地回答这个问题。",
        ],
        58: [ // 心理咨询
          "我觉得在这里很安全，可以敞开心扉。",
          "谢谢您的理解和支持。",
          "这个过程对我很有帮助。",
        ],
        59: [ // 跨国商务
          "我们需要考虑文化差异的影响。",
          "这个合作对双方都有益处。",
          "我们用国际化的视野来看这个问题。",
        ],
        60: [ // 家庭调解
          "家庭和睦对所有人都很重要。",
          "我们需要互相理解和包容。",
          "让我们为了家庭的幸福一起努力。",
        ],
        61: [ // 团队建设
          "这个团建活动很有意义。",
          "我们的团队合作越来越好了。",
          "让我们一起为团队目标努力。",
        ],
        62: [ // 志愿服务
          "谢谢您的帮助，我很感激。",
          "我想为社区贡献自己的力量。",
          "帮助他人让我感到很有意义。",
        ],
        63: [ // 学术交流
          "您的研究观点很有启发性。",
          "我们可以在这个领域合作研究。",
          "学术讨论让我们都受益匪浅。",
        ],
        64: [ // 危机干预
          "谢谢您在我最困难时陪伴我。",
          "我现在感觉好一些了。",
          "您的帮助对我来说很重要。",
        ],
        65: [ // 网络调解
          "让我们理性地讨论这个问题。",
          "网络环境需要我们共同维护。",
          "我们应该用善意来化解误解。",
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
          // 数字ID映射
          1: "我最近真的很累，很多事情让我感到压力很大...",  // 主动倾听
          2: "我感觉你好像有话要对我说？",  // 情感表达
          3: "我觉得我们需要好好谈谈这个问题...",  // 非暴力沟通
          4: "你觉得我现在的表情传达了什么信息？",  // 情绪识别
          5: "我需要有人能理解我现在的感受...",  // 情感共鸣
          6: "我现在的情绪有点不稳定，你能帮我吗？",  // 情绪调节
          7: "你好！很高兴在这里遇到你。",  // 破冰技巧
          8: "我希望我们能建立真正的信任关系。",  // 信任建立
          9: "我觉得我们之间有些分歧需要解决...",  // 冲突解决
          10: "我们来讨论一下这个工作项目吧。",  // 职场沟通
          11: "虽然我们相隔很远，但我想和你好好聊聊。",  // 异地恋维护
          12: "我最近感到很困扰，希望能和你谈谈。",  // 危机干预
          // 保留原有字符串键
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
            feedback: `很棒的情景对话练习！你在"${this.skillInfo?.title || this.skillInfo?.name
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
            feedback: `太棒了！你在"${this.skillInfo?.title || this.skillInfo?.name
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
          `你在${(this.skillInfo.scenarios && this.skillInfo.scenarios[0]) || "聚会"
          }上遇到了一个看起来很有趣的人，但你们还不认识。现在是开始对话的好时机，尝试用${this.skillInfo.title
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

      switch (this.scenarioData.source) {
        case "ai_generated":
          return "🤖";
        case "detail_page":
          return "🎯";
        case "fallback":
          return "📚";
        default:
          return "📝";
      }
    },

    getScenarioSourceText() {
      if (!this.scenarioData) return "标准场景";

      switch (this.scenarioData.source) {
        case "ai_generated":
          return "AI智能生成";
        case "detail_page":
          return "场景练习";
        case "fallback":
          return "经典场景";
        default:
          return "标准场景";
      }
    },

    getScenarioSourceClass() {
      if (!this.scenarioData) return "source-default";

      switch (this.scenarioData.source) {
        case "ai_generated":
          return "source-ai";
        case "detail_page":
          return "source-detail";
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

    // 生成具体情景的方法
    generateSpecificScenario() {
      const scenarios = {
        // AI职业 + 我的职业的情景组合
        "大学同学-大学生": [
          "我们在图书馆学习，你注意到我看起来有些焦虑，因为明天有一门重要的考试。",
          "在学校食堂排队时，我们偶然遇到了，我提到最近在准备一个重要的课程作业。",
          "班级小组讨论课上，我们被分在同一组，需要完成一个团队项目。",
        ],
        "职场同事-职场新人": [
          "这是你入职的第一周，我作为你的同事，在茶水间遇到了你。",
          "部门会议结束后，我注意到你对刚才讨论的项目似乎有些困惑。",
          "午休时间，我们在公司楼下的咖啡厅碰面，聊起了工作适应的话题。",
        ],
        "面试官-求职者": [
          "这是一场重要的工作面试，你准时到达了面试地点，我刚刚审阅完你的简历。",
          "面试进行到一半，我想了解你对这个职位的具体看法和期望。",
          "面试即将结束，我准备给你一些提问的机会，看看你对公司还有什么想了解的。",
        ],
        "老师-大学生": [
          "课后，你来到我的办公室，似乎对今天讲的内容有些疑问。",
          "在校园里偶遇，我注意到你最近的学习状态有些不太对劲。",
          "期中考试结束后，我叫你来办公室讨论你的学习情况。",
        ],
        "朋友-大学生": [
          "我们在咖啡厅见面，我注意到你最近心情不太好，想关心一下你的近况。",
          "周末聚会上，大家都在聊各自的近况，轮到你分享时你显得有些犹豫。",
          "深夜时分，我们在宿舍楼下散步，你说有些心事想要倾诉。",
        ],
      };

      const key = `${this.selectedAiProfession}-${this.selectedMyProfession}`;
      const specificScenarios = scenarios[key] || [
        `我们在一个轻松的环境中相遇，你作为${this.selectedMyProfession}，我作为${this.selectedAiProfession}，我们开始了一段自然的对话。`,
        `在日常生活中，我们因为某个共同的话题而开始交流，气氛比较融洽。`,
        `我们在一个需要沟通协作的场合相遇，彼此都希望能够有效地交流。`,
      ];

      return specificScenarios[
        Math.floor(Math.random() * specificScenarios.length)
      ];
    },

    generateOpeningDialogue() {
      const openings = {
        友善开朗: [
          "嗨！看起来我们有机会聊聊了，你最近怎么样？",
          "你好！很高兴见到你，我注意到你好像有什么想法？",
          "哈喽！我觉得我们可以好好聊聊，你觉得呢？",
        ],
        严肃认真: [
          "你好，我想我们需要认真地沟通一下这个问题。",
          "很好，我们来谈谈吧。我希望能听到你的真实想法。",
          "请坐，我们有一些重要的事情需要讨论。",
        ],
        幽默风趣: [
          '哎呀，看来我们又要开始"深度交流"了，准备好了吗？',
          "嘿，我发现聊天总比发呆有趣多了，你说呢？",
          "好吧，既然我们都在这里，不如来场有趣的对话？",
        ],
        温和耐心: [
          "你好，我注意到你可能有些话想说，我很乐意倾听。",
          "别着急，我们有充足的时间慢慢聊，你想从哪里开始？",
          "请放轻松，我们可以随意聊聊，没有压力的。",
        ],
        直率坦诚: [
          "我们直说吧，我觉得有些话需要开诚布公地谈。",
          "我比较喜欢直接的交流，你有什么想法就直说吧。",
          "咱们别绕弯子了，我想听听你真实的想法。",
        ],
      };

      const personalityOpenings = openings[this.selectedPersonality] || [
        "你好，我们开始聊聊吧。",
        "很高兴有机会和你交流。",
        "我们来谈谈这个话题吧。",
      ];

      return personalityOpenings[
        Math.floor(Math.random() * personalityOpenings.length)
      ];
    },

    // 模型选择相关方法
    showModelSelector() {
      this.showModelModal = true;
      // 重置选择
      this.selectedAiProfession = "";
      this.selectedMyProfession = "";
      this.selectedAge = "";
      this.selectedPersonality = "";
      this.aiBackground = "";
    },

    hideModelSelector() {
      this.showModelModal = false;
    },

    confirmRoleSelection() {
      if (
        !this.selectedAiProfession ||
        !this.selectedMyProfession ||
        !this.selectedAge ||
        !this.selectedPersonality
      ) {
        uni.showToast({
          title: "请完善必填信息",
          icon: "none",
        });
        return;
      }

      // 构建详细的角色扮演提示语句
      let roleMessage = `请在这个场景中扮演一个${this.selectedAge}、性格${this.selectedPersonality}的${this.selectedAiProfession}，与我这个${this.selectedMyProfession}进行对话练习。`;

      if (this.aiBackground.trim()) {
        roleMessage += `情景设定：${this.aiBackground.trim()}。`;
      } else {
        roleMessage += `请提供一个合适且具体的情景。`;
      }

      roleMessage += `请根据这个身份特点和情景来自然地回应我的对话，帮助我练习人际交往技巧。`;

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
        // 生成具体情景
        const scenarioContent = this.generateSpecificScenario();

        let confirmMessage = `好的！我现在是一个${this.selectedAge}、${this.selectedPersonality}的${this.selectedAiProfession}。`;

        if (this.aiBackground.trim()) {
          confirmMessage += `\n\n【情景设定】\n${this.aiBackground.trim()}\n\n`;
        } else {
          confirmMessage += `\n\n【情景设定】\n${scenarioContent}\n\n`;
        }

        confirmMessage += this.generateOpeningDialogue();

        this.chatMessages.push({
          role: "ai",
          content: confirmMessage,
          type: "role_confirmation",
        });
        this.isAiTyping = false;
      }, 1000);

      uni.showToast({
        title: `角色设定完成`,
        icon: "success",
      });
    },
  },
};
</script>

<style scoped>
/* 现代化浅蓝色系设计 */
.practice-container {
  padding: 0;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #f5f9ff 100%);
  min-height: 100vh;
  position: relative;
}

.practice-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(135, 206, 235, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(173, 216, 230, 0.08) 0%, transparent 50%);
  pointer-events: none;
}

.skill-info {
  padding: 60rpx 40rpx 40rpx;
  position: relative;
  z-index: 1;
}

.skill-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  position: relative;
  overflow: hidden;
}

.skill-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background: linear-gradient(90deg, #87ceeb 0%, #add8e6 50%, #b0e0e6 100%);
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.skill-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.difficulty-badge {
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 20rpx;
  font-weight: 500;
}

.difficulty-badge.basic {
  background: linear-gradient(135deg, #e8f6f3 0%, #d5f3ec 100%);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.difficulty-badge.intermediate {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
  color: #4682b4;
  border: 1px solid rgba(70, 130, 180, 0.2);
}

.difficulty-badge.advanced {
  background: linear-gradient(135deg, #f0f8ff 0%, #e1f0ff 100%);
  color: #2e5e8c;
  border: 1px solid rgba(46, 94, 140, 0.2);
}

.skill-content {
  font-size: 28rpx;
  color: #5a6c7d;
  line-height: 1.7;
  margin-bottom: 20rpx;
  font-weight: 400;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background: linear-gradient(135deg, rgba(173, 216, 230, 0.2) 0%, rgba(176, 224, 230, 0.15) 100%);
  color: #4682b4;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  font-weight: 500;
  border: 1px solid rgba(70, 130, 180, 0.2);
  backdrop-filter: blur(10px);
}

.scenario-section {
  padding: 0 40rpx 40rpx;
  position: relative;
  z-index: 1;
}

.scenario-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
  position: relative;
  overflow: hidden;
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.scenario-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20rpx;
  display: block;
}

.scenario-source {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.scenario-source.source-ai {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(39, 174, 96, 0.1) 100%);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.scenario-source.source-detail {
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.15) 0%, rgba(41, 128, 185, 0.1) 100%);
  color: #2980b9;
  border: 1px solid rgba(41, 128, 185, 0.2);
}

.scenario-source.source-fallback {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.15) 0%, rgba(211, 84, 0, 0.1) 100%);
  color: #d35400;
  border: 1px solid rgba(211, 84, 0, 0.2);
}

.scenario-source.source-default {
  background: linear-gradient(135deg, rgba(149, 165, 166, 0.15) 0%, rgba(127, 140, 141, 0.1) 100%);
  color: #7f8c8d;
  border: 1px solid rgba(127, 140, 141, 0.2);
}

.source-icon {
  font-size: 20rpx;
}

.source-text {
  font-weight: 600;
}

.scenario-content {
  background: linear-gradient(135deg, rgba(236, 240, 241, 0.6) 0%, rgba(250, 252, 253, 0.8) 100%);
  border: 1px solid rgba(189, 195, 199, 0.2);
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  backdrop-filter: blur(10px);
}

.scenario-text {
  font-size: 28rpx;
  color: #34495e;
  line-height: 1.8;
  font-weight: 400;
}

.scenario-actions {
  display: flex;
  gap: 16rpx;
}

.interactive-section {
  padding: 0 40rpx 40rpx;
  position: relative;
  z-index: 1;
}

.practice-guide {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
}

.guide-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16rpx;
  display: block;
}

.guide-text {
  font-size: 28rpx;
  color: #5a6c7d;
  line-height: 1.7;
  font-weight: 400;
}

.chat-area {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  min-height: 400rpx;
  max-height: 600rpx;
  overflow-y: auto;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 2rpx 8rpx rgba(173, 216, 230, 0.1);
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
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.user .message-avatar {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  color: #2c3e50;
  box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
}

.ai .message-avatar {
  background: linear-gradient(135deg, rgba(236, 240, 241, 0.8) 0%, rgba(255, 255, 255, 0.9) 100%);
  color: #5a6c7d;
  box-shadow: 0 4rpx 12rpx rgba(149, 165, 166, 0.2);
}

.avatar-text {
  font-size: 20rpx;
  font-weight: 600;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-text {
  padding: 20rpx;
  border-radius: 18rpx;
  font-size: 28rpx;
  line-height: 1.6;
  display: block;
  font-weight: 400;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.ai .message-text {
  background: linear-gradient(135deg, rgba(236, 240, 241, 0.6) 0%, rgba(255, 255, 255, 0.8) 100%);
  color: #2c3e50;
  box-shadow: 0 2rpx 8rpx rgba(149, 165, 166, 0.1);
}

.user .message-text {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  color: #2c3e50;
  box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
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
  background: transparent;
}

.input-container {
  display: flex;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(173, 216, 230, 0.3);
  border-radius: 50rpx;
  padding: 16rpx;
  box-shadow: 
    0 8rpx 32rpx rgba(135, 206, 235, 0.15),
    0 4rpx 12rpx rgba(173, 216, 230, 0.1);
  align-items: flex-end;
  gap: 12rpx;
}

.model-btn {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  color: #4682b4;
  padding: 20rpx 24rpx;
  border-radius: 40rpx;
  font-size: 24rpx;
  white-space: nowrap;
  border: 1px solid rgba(173, 216, 230, 0.3);
  font-weight: 500;
  transition: all 0.3s ease;
}

.model-btn:active {
  background: rgba(135, 206, 235, 0.2);
  border-color: #87ceeb;
  transform: scale(0.95);
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
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  color: #2c3e50;
  padding: 20rpx 32rpx;
  border-radius: 40rpx;
  font-size: 28rpx;
  font-weight: 600;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.3),
    0 2rpx 4rpx rgba(173, 216, 230, 0.2);
}

.send-btn:active {
  transform: scale(0.95);
  box-shadow: 
    0 2rpx 8rpx rgba(135, 206, 235, 0.2),
    0 1rpx 2rpx rgba(173, 216, 230, 0.1);
}

.send-btn.disabled {
  opacity: 0.6;
  transform: none;
  cursor: not-allowed;
  background: rgba(149, 165, 166, 0.3);
  color: #7f8c8d;
  box-shadow: 
    0 2rpx 8rpx rgba(149, 165, 166, 0.1),
    0 1rpx 2rpx rgba(127, 140, 141, 0.1);
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

.scenario-source.source-detail {
  background-color: #e3f2fd;
  color: #2196f3;
  border: 1rpx solid #2196f3;
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

/* 模型选择弹窗样式 - uniapp风格 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background-color: white;
  border-radius: 24rpx 24rpx 0 0;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
  box-shadow: 0 -8rpx 32rpx rgba(0, 0, 0, 0.2);
}

.modal-header {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40rpx 32rpx 20rpx;
  border-bottom: 1rpx solid #ebeef5;
}

.modal-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #303133;
}

.modal-close {
  position: absolute;
  right: 32rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f5f7fa;
  transition: background-color 0.2s;
}

.modal-close:active {
  background-color: #e4e7ed;
}

.close-text {
  font-size: 40rpx;
  color: #909399;
  line-height: 1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }

  to {
    transform: translateY(0);
  }
}

.modal-body {
  padding: 20rpx 32rpx 0;
  max-height: 70vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 48rpx;
}

.form-label {
  font-size: 30rpx;
  font-weight: 600;
  color: #606266;
  display: block;
  margin-bottom: 24rpx;
  position: relative;
}

.form-label::before {
  content: "";
  position: absolute;
  left: -16rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 32rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 3rpx;
}

.profession-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.profession-item {
  background-color: #f5f7fa;
  border: 2rpx solid #dcdfe6;
  border-radius: 16rpx;
  padding: 20rpx 28rpx;
  font-size: 28rpx;
  color: #606266;
  text-align: center;
  min-width: 140rpx;
  transition: all 0.2s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.08);
}

.profession-item:active {
  transform: scale(0.95);
}

.profession-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: #2c3e50;
  transform: scale(1.05);
  box-shadow: 0 6rpx 20rpx rgba(135, 206, 235, 0.4);
}

.age-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.age-item {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(173, 216, 230, 0.3);
  border-radius: 16rpx;
  padding: 20rpx 28rpx;
  font-size: 28rpx;
  color: #4682b4;
  text-align: center;
  min-width: 120rpx;
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.15),
    0 2rpx 4rpx rgba(173, 216, 230, 0.1);
  font-weight: 500;
}

.age-item:active {
  transform: scale(0.95);
}

.age-item.active {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  border-color: transparent;
  color: #2c3e50;
  transform: scale(1.05);
  box-shadow: 0 6rpx 20rpx rgba(135, 206, 235, 0.4);
  font-weight: 600;
}

.personality-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.personality-item {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(173, 216, 230, 0.3);
  border-radius: 16rpx;
  padding: 20rpx 28rpx;
  font-size: 28rpx;
  color: #4682b4;
  text-align: center;
  min-width: 120rpx;
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.15),
    0 2rpx 4rpx rgba(173, 216, 230, 0.1);
  font-weight: 500;
}

.personality-item:active {
  transform: scale(0.95);
}

.personality-item.active {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  border-color: transparent;
  color: #2c3e50;
  transform: scale(1.05);
  box-shadow: 0 6rpx 20rpx rgba(135, 206, 235, 0.4);
  font-weight: 600;
}

.background-input {
  width: 100%;
  min-height: 140rpx;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(173, 216, 230, 0.3);
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 28rpx;
  color: #2c3e50;
  line-height: 1.7;
  resize: none;
  box-sizing: border-box;
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.1),
    0 2rpx 4rpx rgba(173, 216, 230, 0.05);
  font-family: inherit;
  font-weight: 400;
}

.background-input:focus {
  border-color: #87ceeb;
  outline: none;
  box-shadow: 
    0 0 0 4rpx rgba(135, 206, 235, 0.2),
    0 4rpx 12rpx rgba(135, 206, 235, 0.15);
  background: rgba(255, 255, 255, 0.95);
}

.background-input::placeholder {
  color: #a0b4c1;
  font-size: 26rpx;
}

.char-count {
  font-size: 24rpx;
  color: #7f8c8d;
  text-align: right;
  margin-top: 12rpx;
  display: block;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  padding: 32rpx;
  border-top: 1px solid rgba(173, 216, 230, 0.2);
  gap: 24rpx;
  background: rgba(248, 252, 255, 0.8);
  backdrop-filter: blur(10px);
}

.modal-btn {
  flex: 1;
  padding: 28rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 
    0 4rpx 12rpx rgba(135, 206, 235, 0.15),
    0 2rpx 4rpx rgba(173, 216, 230, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(173, 216, 230, 0.3);
}

.modal-btn:active {
  transform: scale(0.98);
}

.modal-btn.cancel {
  background: rgba(255, 255, 255, 0.8);
  color: #4682b4;
}

.modal-btn.cancel:active {
  background: rgba(236, 240, 241, 0.6);
  border-color: #a0b4c1;
}

.modal-btn.confirm {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  color: #2c3e50;
  border: none;
  box-shadow: 0 6rpx 20rpx rgba(135, 206, 235, 0.4);
}

.modal-btn.confirm:active {
  box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
}

.modal-btn.confirm.disabled {
  background: rgba(149, 165, 166, 0.3);
  color: #7f8c8d;
  box-shadow: 
    0 2rpx 8rpx rgba(149, 165, 166, 0.1),
    0 1rpx 2rpx rgba(127, 140, 141, 0.1);
  transform: none;
  cursor: not-allowed;
}

/* 响应式设计增强 */
@media (max-width: 750rpx) {
  .profession-grid,
  .age-grid,
  .personality-grid {
    gap: 12rpx;
  }
  
  .profession-item,
  .age-item,
  .personality-item {
    padding: 16rpx 20rpx;
    font-size: 26rpx;
    min-width: 100rpx;
  }
  
  .background-input {
    font-size: 26rpx;
    padding: 20rpx;
    min-height: 120rpx;
  }
  
  .modal-btn {
    font-size: 28rpx;
    padding: 24rpx;
  }
}

/* 滚动条样式 */
.modal-body::-webkit-scrollbar {
  width: 8rpx;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(236, 240, 241, 0.3);
  border-radius: 4rpx;
}

.modal-body::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
  border-radius: 4rpx;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #6bb6cd 0%, #98d4e0 100%);
}

/* 动画增强 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.loading .action-btn {
  animation: pulse 1.5s infinite;
}

/* 焦点和选择样式 */
::selection {
  background: rgba(135, 206, 235, 0.3);
  color: #2c3e50;
}

*:focus {
  outline: none;
}

/* 平滑滚动 */
.modal-body {
  scroll-behavior: smooth;
}
</style>
