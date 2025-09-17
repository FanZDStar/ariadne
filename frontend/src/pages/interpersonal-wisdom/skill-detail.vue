<template>
  <view class="skill-detail-container">
    <view class="header">
      <view class="skill-header">
        <view class="skill-basic-info">
          <text class="skill-title">{{ skillData.name }}</text>
          <view class="skill-meta">
            <view class="meta-item">
              <text class="meta-icon">⏱️</text>
              <text class="meta-text">{{ skillData.estimatedTime }}分钟</text>
            </view>
            <view class="meta-item">
              <text class="meta-icon">👥</text>
              <text class="meta-text">{{ skillData.learnerCount }}人学习</text>
            </view>
          </view>
        </view>
      </view>

      <text class="skill-description">{{ skillData.description }}</text>

      <view class="skill-tags">
        <text v-for="tag in skillData.tags" :key="tag" class="skill-tag">{{
          tag
        }}</text>
      </view>
    </view>

    <view class="content">
      <!-- 学习目标 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">🎯 学习目标</text>
        </view>
        <view class="objectives-list">
          <view v-for="objective in skillData.objectives" :key="objective" class="objective-item">
            <text class="objective-icon">•</text>
            <text class="objective-text">{{ objective }}</text>
          </view>
        </view>
      </view>

      <!-- 核心要点 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">💡 核心要点</text>
        </view>
        <view class="key-points">
          <view v-for="point in skillData.keyPoints" :key="point.title" class="point-card">
            <view class="point-header">
              <text class="point-icon">{{ point.icon }}</text>
              <text class="point-title">{{ point.title }}</text>
            </view>
            <text class="point-content">{{ point.content }}</text>
            <view v-if="point.example" class="point-example">
              <text class="example-label">示例：</text>
              <text class="example-text">{{ point.example }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 实践步骤 -->
      <view class="section" v-if="skillData.practiceSteps && skillData.practiceSteps.length > 0">
        <view class="section-header">
          <text class="section-title">📋 实践步骤</text>
        </view>
        <view class="practice-steps">
          <view v-for="(step, index) in skillData.practiceSteps" :key="index" class="step-item">
            <view class="step-number">
              <text class="step-text">{{ index + 1 }}</text>
            </view>
            <view class="step-content">
              <text class="step-title">{{ step.title }}</text>
              <text class="step-description">{{ step.description }}</text>
              <view v-if="step.tips" class="step-tips">
                <text class="tips-label">💡 小贴士：</text>
                <text class="tips-text">{{ step.tips }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 场景应用 -->
      <view class="section" v-if="skillData.scenarios && skillData.scenarios.length > 0">
        <view class="section-header">
          <text class="section-title">🎭 场景应用</text>
        </view>
        <view class="scenarios">
          <view v-for="scenario in skillData.scenarios" :key="scenario.id" class="scenario-card"
            @click="practiceScenario(scenario)">
            <view class="scenario-header">
              <text class="scenario-title">{{ scenario.title }}</text>
            </view>
            <text class="scenario-description">{{ scenario.description }}</text>
            <view class="scenario-action">
              <text class="action-text">开始练习</text>
              <text class="action-arrow">→</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 实践场景 (fallback for practiceScenarios) -->
      <view class="section"
        v-if="skillData.practiceScenarios && skillData.practiceScenarios.length > 0 && (!skillData.scenarios || skillData.scenarios.length === 0)">
        <view class="section-header">
          <text class="section-title">🎭 实践场景</text>
        </view>
        <view class="scenarios">
          <view v-for="(scenario, index) in skillData.practiceScenarios" :key="index" class="scenario-card"
            @click="practiceScenario(scenario)">
            <view class="scenario-header">
              <text class="scenario-title">{{ scenario.title }}</text>
            </view>
            <text class="scenario-description">{{ scenario.description }}</text>
            <view class="scenario-action">
              <text class="action-text">开始练习</text>
              <text class="action-arrow">→</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 相关技能 -->
      <view class="section" v-if="relatedSkills.length > 0">
        <view class="section-header">
          <text class="section-title">🔗 相关技能</text>
        </view>
        <view class="related-skills">
          <view v-for="skill in relatedSkills" :key="skill.id" class="related-skill-card"
            @click="viewRelatedSkill(skill)">
            <text class="related-skill-name">{{ skill.name }}</text>
            <text class="related-skill-desc">{{ skill.brief }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部操作区域 -->
    <view class="bottom-actions">
      <view class="action-btn primary" @click="startScenarioPractice">
        <text class="btn-text">情景演练</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      skillId: "",
      categoryId: "",
      skillData: {},
      relatedSkills: [],
    };
  },

  onLoad(options) {
    this.skillId = options.skillId;
    this.categoryId = options.categoryId;
    this.loadSkillDetail();
  },

  methods: {
    async loadSkillDetail() {
      try {
        uni.showLoading({ title: "加载中..." });

        // 模拟API调用
        await this.mockLoadSkillDetail();
      } catch (error) {
        console.error("加载技能详情失败:", error);
        uni.showToast({
          title: "加载失败",
          icon: "none",
        });
      } finally {
        uni.hideLoading();
      }
    },

    async mockLoadSkillDetail() {
      // 根据不同的 skillId 返回不同的技能数据
      const skillDataMap = {
        // 沟通表达类技能 (communication)
        "listen_actively": {
          id: "listen_actively",
          name: "主动倾听",
          description:
            "主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。",
          estimatedTime: 15,
          learnerCount: 1234,
          tags: ["倾听", "沟通基础", "理解"],
          objectives: [
            "学会集中注意力倾听对方说话",
            "理解言语背后的情感和需求",
            "通过肢体语言展现倾听态度",
            "运用复述和确认技巧验证理解",
          ],
          keyPoints: [
            {
              icon: "👀",
              title: "眼神交流",
              content: "保持适当的眼神交流，表达对对方的关注和尊重",
              example: "看着对方的眼睛，偶尔点头表示理解",
            },
            {
              icon: "🤐",
              title: "避免打断",
              content: "让对方完整表达想法，不要急于插话或给建议",
              example: '等对方说完后再回应："我理解你的意思是..."',
            },
            {
              icon: "🔄",
              title: "反馈确认",
              content: "用自己的话复述对方的观点，确认理解正确",
              example: '"如果我理解正确，你是想说..."',
            },
          ],
          practiceSteps: [
            {
              title: "营造倾听环境",
              description: "选择安静、舒适的环境，放下手机等干扰物",
              tips: "将手机调至静音模式，身体面向对方",
            },
            {
              title: "专注关注对方",
              description: "用眼神、肢体语言表达关注，避免思维游离",
              tips: '点头、"嗯"等简单回应表示你在听',
            },
            {
              title: "理解情感层面",
              description: "不仅听懂字面意思，更要理解对方的感受",
              tips: "注意对方的语调、表情变化",
            },
            {
              title: "适当回馈确认",
              description: "用复述、提问等方式确认理解正确",
              tips: '使用"我听到你说..."、"你的意思是..."等句式',
            },
          ],
          scenarios: [
            {
              id: 1,
              title: "朋友倾诉工作压力",
              description: "朋友向你抱怨工作中的困难和压力，需要你的倾听和理解",

            },
            {
              id: 2,
              title: "家人分享生活感受",
              description: "家人想要分享一天的见闻和感受，需要你的关注",

            },
            {
              id: 3,
              title: "同事讨论项目分歧",
              description: "同事对项目有不同看法，需要倾听并理解各方观点",

            },
          ],
        },
        "express_clearly": {
          id: "express_clearly",
          name: "情感表达",
          description:
            "学会准确、恰当地表达自己的情感和需求，避免指责和批评，建立更好的情感连接。",
          estimatedTime: 20,
          learnerCount: 956,
          tags: ["情感", "表达", "I语句"],
          objectives: [
            '学会使用"我"开头的表达方式',
            "准确识别和表达自己的感受",
            "避免指责性语言",
            "清楚表达自己的需求和期望",
          ],
          keyPoints: [
            {
              icon: "🗣️",
              title: "I语句技巧",
              content: '使用"我感到..."而不是"你让我..."的表达方式',
              example: '"我感到被忽视了"而不是"你总是不理我"',
            },
            {
              icon: "💭",
              title: "情感词汇",
              content: "丰富情感词汇，准确描述复杂的感受",
              example: '不只是"不高兴"，可以说"失望"、"焦虑"、"困惑"',
            },
            {
              icon: "🎯",
              title: "具体表达",
              content: "避免模糊表达，说出具体的情况和需求",
              example: '"我希望你能在做决定前征求我的意见"',
            },
          ],
          practiceSteps: [
            {
              title: "识别内心感受",
              description: "花时间思考自己真正的感受是什么",
              tips: "可以用情感轮盘或情感词汇表帮助识别",
            },
            {
              title: "选择合适时机",
              description: "在双方都冷静的时候进行情感表达",
              tips: "避免在争吵或情绪激动时表达",
            },
            {
              title: "使用I语句",
              description: '以"我"开头，描述自己的感受而不是对方的行为',
              tips: '"我感到..."、"我需要..."、"我希望..."',
            },
            {
              title: "倾听对方回应",
              description: "表达完后给对方回应的机会",
              tips: "保持开放态度，准备进行对话而非独白",
            },
          ],
          scenarios: [
            {
              id: 4,
              title: "向伴侣表达不满",
              description: "伴侣经常迟到，你需要表达自己的感受",

            },
            {
              id: 5,
              title: "向朋友表达关心",
              description: "朋友最近状态不好，你想表达关心",

            },
            {
              id: 6,
              title: "工作中表达异议",
              description: "对同事的做法有不同看法，需要表达意见",

            },
          ],
        },
        "topic_transition": {
          id: "topic_transition",
          name: "非暴力沟通",
          description:
            "学习非暴力沟通的四个步骤：观察、感受、需要、请求，以善意和理解进行沟通。",
          estimatedTime: 30,
          learnerCount: 567,
          tags: ["沟通技巧", "冲突处理", "NVC"],
          objectives: [
            "掌握非暴力沟通四步法",
            "学会客观观察而非评判",
            "准确表达感受和需要",
            "提出具体可行的请求",
          ],
          keyPoints: [
            {
              icon: "👁️",
              title: "客观观察",
              content: "描述具体事实而不加入个人判断和评价",
              example: '"你这周有3天晚回家"而不是"你总是很晚回家"',
            },
            {
              icon: "❤️",
              title: "表达感受",
              content: "说出自己的真实感受，而不是想法或评判",
              example: '"我感到孤单"而不是"你不关心我"',
            },
            {
              icon: "🎯",
              title: "说出需要",
              content: "明确表达自己的需要和价值观",
              example: '"我需要更多的陪伴和关注"',
            },
            {
              icon: "🤝",
              title: "具体请求",
              content: "提出明确、具体、可行的请求",
              example: '"你能否每周安排两个晚上和我一起度过？"',
            },
          ],
          practiceSteps: [
            {
              title: "观察练习",
              description: "练习客观描述事实，不加入个人解释",
              tips: '区分观察和评价，避免使用"总是"、"从不"等词',
            },
            {
              title: "感受识别",
              description: "学会区分感受和想法、评判",
              tips: "真正的感受是身体的感觉，如难过、愤怒、喜悦",
            },
            {
              title: "需要探索",
              description: "深入了解感受背后的需要和价值观",
              tips: '问自己"我为什么有这种感受？我真正需要什么？"',
            },
            {
              title: "请求制定",
              description: "提出积极、具体、可行的请求",
              tips: "说出你希望对方做什么，而不是不要做什么",
            },
          ],
          scenarios: [
            {
              id: 7,
              title: "解决家庭冲突",
              description: "家人之间发生分歧，需要用非暴力沟通解决",

            },
            {
              id: 8,
              title: "职场沟通障碍",
              description: "与同事合作出现问题，需要有效沟通",

            },
            {
              id: 9,
              title: "朋友关系维护",
              description: "朋友的行为让你困扰，需要真诚沟通",

            },
          ],
        },
        "sincere_gratitude": {
          id: "sincere_gratitude",
          name: "情绪识别",
          description:
            "通过观察面部表情、语调、肢体语言等线索，准确识别自己和他人的情绪状态。",
          estimatedTime: 12,
          learnerCount: 890,
          tags: ["情绪识别", "观察力", "情商"],
          objectives: [
            "识别基础情绪：喜怒哀惧",
            "观察非语言情绪信号",
            "提升自我情绪觉察",
            "理解情绪的层次和复杂性",
          ],
          keyPoints: [
            {
              icon: "😊",
              title: "面部表情",
              content: "观察眉毛、眼睛、嘴巴的细微变化",
              example: "皱眉可能表示困惑或不满，眼睛放光表示兴奋",
            },
            {
              icon: "🗣️",
              title: "语调变化",
              content: "注意说话的音调、语速、音量变化",
              example: "语速加快可能表示紧张，音调提高可能表示兴奋",
            },
            {
              icon: "🤲",
              title: "肢体语言",
              content: "观察姿态、手势、身体距离等信号",
              example: "双臂交叉可能表示防御，靠近表示亲近",
            },
          ],
          practiceSteps: [
            {
              title: "自我情绪监测",
              description: "每天定时检查自己的情绪状态",
              tips: '设置提醒，问自己"我现在感觉如何？"',
            },
            {
              title: "他人观察练习",
              description: "在日常交往中观察他人的情绪信号",
              tips: "注意一致性，语言和非语言信号是否匹配",
            },
            {
              title: "情绪词汇积累",
              description: "学习更多情绪词汇，精确描述感受",
              tips: "从基础的喜怒哀乐扩展到更细致的情绪",
            },
          ],
          scenarios: [
            {
              id: 10,
              title: "识别朋友的真实感受",
              description: '朋友说"我很好"，但你感觉不对劲',

            },
            {
              id: 11,
              title: "工作会议情绪解读",
              description: "在团队会议中观察同事们的情绪反应",

            },
          ],
        },
        "romantic_expression": {
          id: "romantic_expression",
          name: "情感共鸣",
          description: "学会站在对方角度思考，与他人产生情感共鸣和深层理解。",

          estimatedTime: 25,
          learnerCount: 675,


          tags: ["共情", "理解", "换位思考"],
          objectives: [
            "提升换位思考能力",
            "学会情感镜像技巧",
            "建立深层情感连接",
            "避免过度共情的风险",
          ],
          keyPoints: [
            {
              icon: "🔄",
              title: "换位思考",
              content: "尝试从对方的角度理解事情",
              example: '"如果我是他，我会有什么感受？"',
            },
            {
              icon: "🪞",
              title: "情感镜像",
              content: "反映对方的情感状态，表达理解",
              example: '"我能感受到你很沮丧"',
            },
            {
              icon: "🛡️",
              title: "保持边界",
              content: "共情但不被对方情绪完全淹没",
              example: "理解但保持自己的情绪稳定",
            },
          ],
          practiceSteps: [
            {
              title: "暂停判断",
              description: "停止对他人行为的立即评判",
              tips: "先理解，再评价",
            },
            {
              title: "询问了解",
              description: "主动询问对方的感受和想法",
              tips: '"你现在的感受是什么？"',
            },
            {
              title: "反馈确认",
              description: "确认你的理解是否正确",
              tips: '"你的意思是...对吗？"',
            },
          ],
          scenarios: [
            {
              id: 12,
              title: "安慰失恋的朋友",
              description: "朋友刚分手，情绪低落，需要你的理解",

            },
            {
              id: 13,
              title: "理解家人的焦虑",
              description: "家人对未来很担心，你需要理解他们的感受",

            },
          ],
        },
        // 添加 category-detail.vue 中缺失的技能数据
        "emotion_sharing": {
          id: "emotion_sharing",
          name: "非暴力沟通",
          description: "学习非暴力沟通的四个步骤：观察、感受、需要、请求，以善意和理解进行沟通。",

          estimatedTime: 30,
          learnerCount: 567,


          tags: ["沟通技巧", "冲突处理"],
          objectives: [
            "掌握观察与评判的区别",
            "准确表达感受而非想法",
            "识别真正的需要",
            "提出具体可行的请求",
          ],
          keyPoints: [
            {
              icon: "👁️",
              title: "客观观察",
              content: "区分观察和评判，只描述具体发生的事情",
              example: "说'你迟到了20分钟'而不是'你总是不守时'",
            },
            {
              icon: "💗",
              title: "表达感受",
              content: "用情感词汇表达内心感受",
              example: "我感到担心，而不是'你让我很生气'",
            },
            {
              icon: "🎯",
              title: "识别需要",
              content: "找到感受背后的真正需要",
              example: "我需要安全感和可预测性",
            },
            {
              icon: "🙏",
              title: "具体请求",
              content: "提出具体、可行的行动请求",
              example: "你愿意提前告诉我如果会迟到吗？",
            },
          ],
          practiceSteps: [
            {
              title: "观察练习",
              description: "练习客观描述事件，不加评判",
              tips: "用录像机视角描述发生的事情",
            },
            {
              title: "感受识别",
              description: "学会区分感受和想法",
              tips: "使用感受词汇表，避免'我觉得你...'的表达",
            },
            {
              title: "需要探索",
              description: "深入了解感受背后的需要",
              tips: "问自己'我真正需要的是什么？'",
            },
            {
              title: "请求表达",
              description: "提出具体的行动请求",
              tips: "确保请求是具体、可行、积极的",
            },
          ],
          scenarios: [
            {
              id: 14,
              title: "处理同事分歧",
              description: "与同事在工作方式上有分歧，需要协调",

            },
            {
              id: 15,
              title: "家庭沟通冲突",
              description: "家人之间因为生活习惯产生矛盾",

            },
          ],
        },
        "ice_breaking": {
          id: "ice_breaking",
          name: "情绪识别",
          description: "通过观察面部表情、语调、肢体语言等准确识别自己和他人的情绪状态。",

          estimatedTime: 12,
          learnerCount: 890,


          tags: ["情绪识别", "观察力"],
          objectives: [
            "识别基本情绪表达",
            "观察非言语信号",
            "理解情绪的层次性",
            "提高情绪觉察能力",
          ],
          keyPoints: [
            {
              icon: "😊",
              title: "面部表情",
              content: "学会从面部表情读取情绪信息",
              example: "紧皱的眉头可能表示困惑或担忧",
            },
            {
              icon: "🗣️",
              title: "语调变化",
              content: "注意语调、语速的变化传达的情绪",
              example: "语速加快可能表示紧张或兴奋",
            },
            {
              icon: "🤲",
              title: "肢体语言",
              content: "观察姿态和手势传达的信息",
              example: "交叉双臂可能表示防御或不满",
            },
          ],
          practiceSteps: [
            {
              title: "情绪词汇学习",
              description: "扩展情绪词汇量，精确表达情绪",
              tips: "使用情绪轮盘或情绪词汇表",
            },
            {
              title: "观察练习",
              description: "在日常互动中练习观察他人情绪",
              tips: "关注一致性和不一致性的信号",
            },
          ],
          scenarios: [
            {
              id: 16,
              title: "识别朋友的隐藏情绪",
              description: "朋友说没事，但表情和语调显示有问题",

            },
          ],
        },
        "trust_building": {
          id: "trust_building",
          name: "情感共鸣",
          description: "学会站在对方角度思考，理解对方的感受，与他人产生情感共鸣和理解。",

          estimatedTime: 25,
          learnerCount: 675,


          tags: ["共情", "理解"],
          objectives: [
            "发展换位思考能力",
            "理解他人的情感体验",
            "表达共情和理解",
            "建立情感连接",
          ],
          keyPoints: [
            {
              icon: "🔄",
              title: "换位思考",
              content: "尝试从对方的角度理解情况",
              example: "如果我是他/她，我会有什么感受？",
            },
            {
              icon: "💭",
              title: "情感反映",
              content: "反映对方的情感，让其感受到被理解",
              example: "听起来你感到很沮丧...",
            },
          ],
          practiceSteps: [
            {
              title: "角色扮演",
              description: "通过角色扮演体验不同立场",
              tips: "想象自己处在对方的处境中",
            },
            {
              title: "情感反映练习",
              description: "练习反映他人的情感",
              tips: "使用'你感到...'的句式",
            },
          ],
          scenarios: [
            {
              id: 17,
              title: "理解失业朋友的感受",
              description: "朋友失业了，需要情感支持",

            },
          ],
        },
        "boundary_setting": {
          id: "boundary_setting",
          name: "情绪调节",
          description: "掌握深呼吸、认知重构等情绪调节技巧，有效管理和调节自己的情绪。",

          estimatedTime: 35,
          learnerCount: 445,


          tags: ["情绪管理", "自我调节"],
          objectives: [
            "掌握情绪调节技巧",
            "提高情绪稳定性",
            "学会自我安抚",
            "培养情绪弹性",
          ],
          keyPoints: [
            {
              icon: "🫁",
              title: "深呼吸技巧",
              content: "通过调节呼吸来平静情绪",
              example: "4-7-8呼吸法：吸气4秒，憋气7秒，呼气8秒",
            },
            {
              icon: "🧠",
              title: "认知重构",
              content: "改变对事件的看法来调节情绪",
              example: "将'糟糕透了'改为'这是个挑战，我能应对'",
            },
          ],
          practiceSteps: [
            {
              title: "呼吸练习",
              description: "每天练习深呼吸技巧",
              tips: "在感到压力时立即使用",
            },
            {
              title: "认知练习",
              description: "练习识别和改变负面思维",
              tips: "问自己'还有其他看法吗？'",
            },
          ],
          scenarios: [
            {
              id: 18,
              title: "应对工作压力",
              description: "工作截止日期临近，感到焦虑",

            },
          ],
        },
        "conflict_resolution": {
          id: "conflict_resolution",
          name: "破冰技巧",
          description: "掌握开场白、话题引导等社交技巧，在新环境中快速与他人建立联系。",

          estimatedTime: 18,
          learnerCount: 1123,


          tags: ["破冰", "社交"],
          objectives: [
            "掌握有效的开场白",
            "学会话题转换",
            "建立初步信任",
            "营造轻松氛围",
          ],
          keyPoints: [
            {
              icon: "👋",
              title: "友好开场",
              content: "用温暖的问候开始对话",
              example: "你好，我是...很高兴认识你",
            },
            {
              icon: "❓",
              title: "开放性问题",
              content: "使用开放性问题引导对话",
              example: "你觉得今天的活动怎么样？",
            },
          ],
          practiceSteps: [
            {
              title: "开场白练习",
              description: "准备几个适用于不同场合的开场白",
              tips: "保持自然和真诚",
            },
          ],
          scenarios: [
            {
              id: 19,
              title: "聚会认识新朋友",
              description: "在朋友聚会上主动认识新朋友",

            },
          ],
        },
        "digital_communication": {
          id: "digital_communication",
          name: "信任建立",
          description: "通过真诚、一致性、可靠性在关系中建立互相信任的基础。",

          estimatedTime: 28,
          learnerCount: 789,


          tags: ["信任", "关系维护"],
          objectives: [
            "展现真诚态度",
            "保持行为一致性",
            "建立可靠形象",
            "培养信任关系",
          ],
          keyPoints: [
            {
              icon: "💯",
              title: "真诚沟通",
              content: "保持诚实和透明的沟通方式",
              example: "承认自己的错误和不足",
            },
            {
              icon: "⚖️",
              title: "言行一致",
              content: "确保说到做到，建立可信度",
              example: "承诺的事情一定要履行",
            },
          ],
          practiceSteps: [
            {
              title: "承诺践行",
              description: "严格履行对他人的承诺",
              tips: "不轻易承诺，承诺了就要做到",
            },
          ],
          scenarios: [
            {
              id: 20,
              title: "建立工作伙伴关系",
              description: "与新同事建立信任的工作关系",

            },
          ],
        },
        "group_social": {
          id: "group_social",
          name: "冲突解决",
          description: "学会协商、妥协、寻找双赢解决方案，有效处理人际冲突和分歧。",

          estimatedTime: 40,
          learnerCount: 234,


          tags: ["冲突处理", "协商"],
          objectives: [
            "识别冲突根源",
            "掌握协商技巧",
            "寻找双赢方案",
            "修复关系",
          ],
          keyPoints: [
            {
              icon: "🔍",
              title: "根源分析",
              content: "深入了解冲突的真正原因",
              example: "区分立场和利益",
            },
            {
              icon: "🤝",
              title: "协商技巧",
              content: "运用有效的协商策略",
              example: "寻找共同点，扩大共同利益",
            },
          ],
          practiceSteps: [
            {
              title: "倾听练习",
              description: "在冲突中先倾听对方观点",
              tips: "理解对方的需求和担忧",
            },
          ],
          scenarios: [
            {
              id: 21,
              title: "解决团队分歧",
              description: "团队成员对项目方向有不同意见",

            },
          ],
        },
        10: {
          id: "listen_actively",
          name: "职场沟通",
          description: "掌握正式场合的沟通技巧和职场礼仪，在职场环境中有效沟通。",

          estimatedTime: 22,
          learnerCount: 1567,


          tags: ["职场", "正式沟通"],
          objectives: [
            "掌握职场礼仪",
            "学会正式沟通",
            "提高专业表达",
            "建立职业形象",
          ],
          keyPoints: [
            {
              icon: "💼",
              title: "专业表达",
              content: "使用恰当的职场语言",
              example: "用'建议'代替'觉得'",
            },
          ],
          practiceSteps: [
            {
              title: "邮件写作",
              description: "练习写作正式的工作邮件",
              tips: "注意格式和用词的专业性",
            },
          ],
          scenarios: [
            {
              id: 22,
              title: "向上级汇报工作",
              description: "向领导汇报项目进展",

            },
          ],
        },
        11: {
          id: "express_clearly",
          name: "异地恋维护",
          description: "学会通过技术手段保持亲密度和信任，维护异地恋关系的特殊技巧。",

          estimatedTime: 45,
          learnerCount: 456,


          tags: ["异地恋", "关系维护"],
          objectives: [
            "保持情感连接",
            "建立沟通节奏",
            "处理距离焦虑",
            "规划未来",
          ],
          keyPoints: [
            {
              icon: "📱",
              title: "有效沟通",
              content: "利用各种技术手段保持联系",
              example: "视频通话、语音消息、共享日常",
            },
          ],
          practiceSteps: [
            {
              title: "沟通计划",
              description: "制定规律的沟通时间表",
              tips: "考虑双方的时区和作息",
            },
          ],
          scenarios: [
            {
              id: 23,
              title: "应对思念情绪",
              description: "处理因距离产生的思念和孤独",

            },
          ],
        },
        12: {
          id: "topic_transition",
          name: "危机干预",
          description: "学会识别危机信号，提供适当的支持和帮助，在他人遇到情感危机时提供支持。",

          estimatedTime: 50,
          learnerCount: 123,


          tags: ["危机干预", "支持技巧"],
          objectives: [
            "识别危机信号",
            "提供情感支持",
            "知晓求助渠道",
            "保护自身安全",
          ],
          keyPoints: [
            {
              icon: "🚨",
              title: "危机识别",
              content: "学会识别情感危机的警告信号",
              example: "持续的绝望感、自伤想法等",
            },
            {
              icon: "🤗",
              title: "支持技巧",
              content: "提供适当的情感支持",
              example: "倾听、陪伴，避免说教",
            },
          ],
          practiceSteps: [
            {
              title: "倾听技巧",
              description: "学会在危机时刻有效倾听",
              tips: "给予充分的关注和耐心",
            },
          ],
          scenarios: [
            {
              id: 24,
              title: "朋友情绪危机",
              description: "朋友表达了自伤想法",

            },
          ],
        },
        // 沟通表达新增技能 (ID 13-25)
        13: {
          id: "sincere_gratitude",
          name: "清晰表达",
          description: "用简洁明了的语言传达想法，让听众易于理解你的观点和意图。",

          estimatedTime: 18,
          learnerCount: 892,


          tags: ["表达", "逻辑", "清晰"],
          objectives: [
            "掌握逻辑清晰的表达结构",
            "学会用简洁的语言说明复杂概念",
            "运用合适的例子和比喻",
            "确保信息传递的准确性"
          ],
          keyPoints: [
            {
              icon: "📝",
              title: "结构化表达",
              content: "使用总分总、递进等逻辑结构组织语言",
              example: "首先说明主要观点，然后提供支持论据，最后总结"
            }
          ],
          practiceScenarios: [
            {
              title: "工作汇报",
              description: "向上级汇报项目进展，需要简洁明了",

            }
          ]
        },
        14: {
          id: "romantic_expression",
          name: "提问技巧",
          description: "学会问出有价值的问题，引导深度对话，获取更多信息。",

          estimatedTime: 22,
          learnerCount: 723,


          tags: ["提问", "引导", "深度"],
          objectives: [
            "掌握开放式和封闭式提问的使用时机",
            "学会循序渐进的提问策略",
            "运用提问引导对话方向",
            "通过提问获取关键信息"
          ],
          keyPoints: [
            {
              icon: "❓",
              title: "5W1H提问法",
              content: "运用什么、谁、何时、何地、为什么、如何的提问框架",
              example: "这个问题的核心是什么？涉及哪些人？"
            }
          ],
          practiceScenarios: [
            {
              title: "客户需求调研",
              description: "通过提问了解客户真正需求",

            }
          ]
        },
        15: {
          id: "emotion_sharing",
          name: "肢体语言",
          description: "运用非言语沟通增强表达力，让沟通更有感染力和说服力。",

          estimatedTime: 25,
          learnerCount: 654,


          tags: ["肢体语言", "非言语", "表达力"],
          objectives: [
            "了解常见肢体语言的含义",
            "学会运用手势支持口语表达",
            "掌握眼神交流的技巧",
            "协调表情与语言内容"
          ],
          keyPoints: [
            {
              icon: "🤲",
              title: "手势运用",
              content: "用自然的手势强调重点，辅助语言表达",
              example: "说到大小时用手势比划，谈到方向时指向相应位置"
            }
          ],
          practiceScenarios: [
            {
              title: "演讲表达",
              description: "在公众场合运用肢体语言增强表达效果",

            }
          ]
        },
        16: {
          id: "ice_breaking",
          name: "故事叙述",
          description: "用故事让沟通更有感染力，通过生动的叙述传递信息和情感。",

          estimatedTime: 28,
          learnerCount: 543,


          tags: ["故事", "感染力", "叙述"],
          objectives: [
            "掌握故事的基本结构",
            "学会选择合适的故事支持观点",
            "运用细节增强故事真实感",
            "控制故事节奏和情感起伏"
          ],
          keyPoints: [
            {
              icon: "📚",
              title: "故事三要素",
              content: "人物、情节、环境三要素构建完整故事",
              example: "明确主人公、发生的事件和具体场景"
            }
          ],
          practiceScenarios: [
            {
              title: "团队激励",
              description: "用励志故事激发团队士气",

            }
          ]
        },
        17: {
          id: "trust_building",
          name: "反馈给予",
          description: "提供建设性的反馈意见，帮助他人成长而不伤害关系。",

          estimatedTime: 20,
          learnerCount: 432,


          tags: ["反馈", "建设性", "成长"],
          objectives: [
            "学会STAR反馈模型",
            "区分正面和改进性反馈",
            "选择合适的反馈时机",
            "关注行为而非个人品格"
          ],
          keyPoints: [
            {
              icon: "💡",
              title: "三明治反馈法",
              content: "正面反馈+改进建议+鼓励结尾",
              example: "你的报告很详细+建议增加图表+期待你的改进版本"
            }
          ],
          practiceScenarios: [
            {
              title: "员工绩效反馈",
              description: "向下属提供工作表现反馈",

            }
          ]
        },
        18: {
          id: "boundary_setting",
          name: "说服技巧",
          description: "以理服人的说服艺术，通过逻辑和情感双重途径影响他人观点。",

          estimatedTime: 35,
          learnerCount: 321,


          tags: ["说服", "影响力", "逻辑"],
          objectives: [
            "掌握逻辑论证的基本方法",
            "学会运用情感共鸣",
            "了解听众心理和需求",
            "建立个人可信度"
          ],
          keyPoints: [
            {
              icon: "🧠",
              title: "三重说服法",
              content: "理性论证+情感感化+道德感召",
              example: "用数据证明+讲述故事+呼应价值观"
            }
          ],
          practiceScenarios: [
            {
              title: "项目提案",
              description: "说服领导支持新项目方案",

            }
          ]
        },
        19: {
          id: 19,
          name: "会议沟通",
          description: "在会议中有效表达观点，参与建设性讨论，推动会议目标达成。",

          estimatedTime: 26,
          learnerCount: 467,


          tags: ["会议", "团队", "讨论"],
          objectives: [
            "掌握会议发言的时机",
            "学会简洁有力的观点表达",
            "运用引导技巧推动讨论",
            "处理会议中的不同意见"
          ],
          keyPoints: [
            {
              icon: "🗣️",
              title: "PREP结构",
              content: "观点+理由+例证+重申",
              example: "我认为...因为...举例来说...所以..."
            }
          ],
          practiceScenarios: [
            {
              title: "部门例会",
              description: "在部门会议中提出改进建议",

            }
          ]
        },
        20: {
          id: 20,
          name: "演讲技巧",
          description: "克服演讲恐惧，掌握公众演讲的基本技巧和方法。",

          estimatedTime: 40,
          learnerCount: 289,


          tags: ["演讲", "公众", "自信"],
          objectives: [
            "克服演讲紧张情绪",
            "掌握演讲结构设计",
            "学会与观众互动",
            "运用声音和语调技巧"
          ],
          keyPoints: [
            {
              icon: "🎤",
              title: "开场技巧",
              content: "用问题、故事或数据吸引听众注意",
              example: "你知道吗？每天我们...或者想象一下..."
            }
          ],
          practiceScenarios: [
            {
              title: "公司年会发言",
              description: "在年会上做部门工作总结",

            }
          ]
        },
        21: {
          id: 21,
          name: "电话沟通",
          description: "在缺乏视觉线索的情况下，保持清晰有效的电话沟通。",

          estimatedTime: 15,
          learnerCount: 378,


          tags: ["电话", "远程", "声音"],
          objectives: [
            "掌握电话沟通的基本礼仪",
            "学会通过声音传递情感",
            "提高语言表达的准确性",
            "处理电话沟通中的干扰"
          ],
          keyPoints: [
            {
              icon: "📞",
              title: "声音表达",
              content: "用语调和语速传达情感和态度",
              example: "适当停顿、语调上扬表示疑问"
            }
          ],
          practiceScenarios: [
            {
              title: "客户服务电话",
              description: "处理客户投诉或咨询",

            }
          ]
        },
        22: {
          id: 22,
          name: "书面表达",
          description: "通过文字进行有效沟通，确保信息准确传达。",

          estimatedTime: 30,
          learnerCount: 198,


          tags: ["书面", "文字", "准确"],
          objectives: [
            "掌握商务写作基本规范",
            "学会结构化组织文字内容",
            "提高文字表达的准确性",
            "适应不同文体的写作要求"
          ],
          keyPoints: [
            {
              icon: "✍️",
              title: "邮件结构",
              content: "主题+称呼+正文+结尾+签名",
              example: "简洁明了的主题行，礼貌的称呼和结尾"
            }
          ],
          practiceScenarios: [
            {
              title: "工作邮件",
              description: "撰写项目进展汇报邮件",

            }
          ]
        },
        23: {
          id: 23,
          name: "跨文化沟通",
          description: "理解文化差异，在跨文化环境中进行敏感而有效的沟通。",

          estimatedTime: 32,
          learnerCount: 156,


          tags: ["跨文化", "多元", "敏感"],
          objectives: [
            "了解主要文化差异类型",
            "学会文化敏感的表达方式",
            "避免文化冒犯和误解",
            "建立跨文化信任关系"
          ],
          keyPoints: [
            {
              icon: "🌍",
              title: "文化维度",
              content: "权力距离、个人主义、不确定性规避等",
              example: "了解不同文化对时间、权威的不同理解"
            }
          ],
          practiceScenarios: [
            {
              title: "国际会议",
              description: "与来自不同国家的同事合作",

            }
          ]
        },
        24: {
          id: 24,
          name: "谈判沟通",
          description: "掌握谈判技巧，通过有效沟通找到互利共赢的解决方案。",

          estimatedTime: 45,
          learnerCount: 134,


          tags: ["谈判", "双赢", "策略"],
          objectives: [
            "掌握谈判前的准备工作",
            "学会识别各方真实需求",
            "运用让步和交换策略",
            "达成双方满意的协议"
          ],
          keyPoints: [
            {
              icon: "🤝",
              title: "BATNA策略",
              content: "最佳替代方案，增强谈判底气",
              example: "明确如果谈判失败的其他选择"
            }
          ],
          practiceScenarios: [
            {
              title: "合同谈判",
              description: "与供应商进行合同条款谈判",

            }
          ]
        },
        25: {
          id: 25,
          name: "数字化沟通",
          description: "适应数字时代，掌握视频会议、即时通讯等在线沟通工具。",

          estimatedTime: 24,
          learnerCount: 267,


          tags: ["数字化", "在线", "工具"],
          objectives: [
            "熟悉各种在线沟通平台",
            "掌握视频会议礼仪",
            "学会在线协作技巧",
            "处理技术故障干扰"
          ],
          keyPoints: [
            {
              icon: "💻",
              title: "视频会议礼仪",
              content: "适当着装、稳定网络、静音管理",
              example: "会议开始前测试设备，不发言时静音"
            }
          ],
          practiceScenarios: [
            {
              title: "远程团队会议",
              description: "主持在线团队例会",

            }
          ]
        },
        // 情感理解新增技能 (ID 26-38)
        26: {
          id: 26,
          name: "情感词汇",
          description: "扩展情感词汇，更精确地描述和表达复杂的情感状态。",

          estimatedTime: 20,
          learnerCount: 523,


          tags: ["词汇", "精确表达", "情感"],
          objectives: [
            "建立丰富的情感词汇库",
            "学会区分相似情感的差别",
            "准确描述情感强度",
            "在交流中运用精确的情感表达"
          ],
          keyPoints: [
            {
              icon: "📖",
              title: "情感词汇轮盘",
              content: "从基础情感扩展到具体情感",
              example: "从'生气'细分为'恼怒''愤怒''烦躁'"
            }
          ],
          practiceSteps: [
            {
              title: "建立情感词汇库",
              description: "收集和学习不同层次的情感词汇",
              tips: "从基础情感词开始，逐步扩展到更具体的表达"
            },
            {
              title: "日常情感标记",
              description: "在日常生活中用精确词汇标记自己的情感",
              tips: "每天至少用三个不同的情感词汇描述心情"
            },
            {
              title: "情感强度练习",
              description: "学会区分同一种情感的不同强度",
              tips: "用1-10的强度等级来描述情感程度"
            },
            {
              title: "实际应用练习",
              description: "在与他人交流时运用精确的情感表达",
              tips: "避免使用'好'、'不好'等模糊词汇"
            }
          ],
          scenarios: [
            {
              id: 1,
              title: "情感日记",
              description: "用精确的词汇记录每日情感体验",

            },
            {
              id: 2,
              title: "情感词汇卡片",
              description: "制作情感词汇卡片，日常练习区分相似情感",

            },
            {
              id: 3,
              title: "情感强度标记",
              description: "为同一种情感标记不同强度等级",

            }
          ]
        },
        27: {
          id: 27,
          name: "同理心训练",
          description: "通过练习增强同理心，更好地理解和回应他人的情感需求。",

          estimatedTime: 28,
          learnerCount: 467,


          tags: ["同理心", "理解", "回应"],
          objectives: [
            "提升情感敏感度",
            "学会换位思考",
            "准确识别他人情感状态",
            "给予恰当的情感回应"
          ],
          keyPoints: [
            {
              icon: "💝",
              title: "共情地图",
              content: "观察他人的说、做、想、感",
              example: "他说什么、做什么、想什么、感受什么"
            }
          ],
          practiceSteps: [
            {
              title: "观察练习",
              description: "仔细观察他人的非语言信号和情绪表现",
              tips: "注意面部表情、肢体语言、语调变化"
            },
            {
              title: "换位思考",
              description: "尝试站在对方的角度理解问题",
              tips: "问自己：如果我是他们，我会有什么感受？"
            },
            {
              title: "情感反映",
              description: "用语言反映你观察到的对方情感",
              tips: "使用'你似乎感到...'、'我注意到你...'等表达"
            },
            {
              title: "恰当回应",
              description: "根据对方的情感状态给予合适的回应",
              tips: "倾听而不急于给建议，陪伴而不试图解决"
            }
          ],
          practiceScenarios: [
            {
              title: "朋友倾诉",
              description: "朋友遇到困难时提供情感支持",

            },
            {
              title: "观察陌生人情绪",
              description: "在公共场所观察他人情绪表达，练习换位思考",

            },
            {
              title: "共情对话练习",
              description: "与家人进行共情对话，理解不同观点",

            },
            {
              title: "同理心反馈",
              description: "在团队中练习给予同理心反馈",

            }
          ]
        },
        28: {
          id: 28,
          name: "情感边界",
          description: "学会在情感交流中保护自己，避免情感过载和耗竭。",

          estimatedTime: 30,
          learnerCount: 389,


          tags: ["边界", "保护", "平衡"],
          objectives: [
            "识别自己的情感边界",
            "学会说不的技巧",
            "保持情感投入的平衡",
            "预防情感耗竭"
          ],
          keyPoints: [
            {
              icon: "🛡️",
              title: "情感防护",
              content: "在帮助他人时保护自己的情感健康",
              example: "设定支持他人的时间和精力限制"
            }
          ],
          practiceScenarios: [
            {
              title: "过度依赖",
              description: "应对他人过度的情感依赖",

            },
            {
              title: "工作情感边界",
              description: "在职场中保持专业的情感距离",

            },
            {
              title: "家庭边界设定",
              description: "在亲密关系中建立健康边界",

            },
            {
              title: "自我保护练习",
              description: "识别情感耗竭信号并采取行动",

            }
          ]
        },
        29: {
          id: 29,
          name: "情绪传染",
          description: "理解和管理情绪的传染性，学会保持情绪稳定。",

          estimatedTime: 22,
          learnerCount: 312,


          tags: ["情绪传染", "稳定", "管理"],
          objectives: [
            "了解情绪传染的机制",
            "识别情绪传染的情况",
            "保持自己的情绪稳定",
            "积极影响团队情绪"
          ],
          keyPoints: [
            {
              icon: "🌊",
              title: "情绪隔离",
              content: "在负面情绪环境中保持内心平静",
              example: "深呼吸、正念观察、心理暗示"
            }
          ],
          practiceScenarios: [
            {
              title: "团队危机",
              description: "在团队焦虑时保持冷静和乐观",

            },
            {
              title: "负面环境隔离",
              description: "在充满抱怨的环境中保持积极心态",

            },
            {
              title: "情绪引导练习",
              description: "用积极情绪影响身边的人",

            },
            {
              title: "压力传导阻断",
              description: "阻止工作压力向家庭传导",

            }
          ]
        },
        30: {
          id: 30,
          name: "情感支持",
          description: "学会在他人需要时给予恰当的情感支持和安慰。",

          estimatedTime: 25,
          learnerCount: 456,


          tags: ["支持", "安慰", "陪伴"],
          objectives: [
            "识别他人的支持需求",
            "掌握不同类型的支持方式",
            "学会倾听而不是建议",
            "提供持续的情感陪伴"
          ],
          keyPoints: [
            {
              icon: "🤗",
              title: "临在陪伴",
              content: "用心陪伴，不急于给出解决方案",
              example: "我在这里陪你、你的感受我理解"
            }
          ],
          practiceScenarios: [
            {
              title: "失恋安慰",
              description: "安慰经历感情挫折的朋友",

            },
            {
              title: "工作挫折支持",
              description: "支持遭遇职场困难的同事",

            },
            {
              title: "家庭变故陪伴",
              description: "陪伴经历家庭变故的亲人",

            },
            {
              title: "持续关怀",
              description: "为长期困难的朋友提供持续支持",

            }
          ]
        },
        31: {
          id: 31,
          name: "创伤敏感",
          description: "理解创伤对情感的影响，在交流中保持敏感和谨慎。",

          estimatedTime: 35,
          learnerCount: 234,


          tags: ["创伤", "敏感", "谨慎"],
          objectives: [
            "了解创伤的基本知识",
            "识别创伤反应的表现",
            "学会创伤知情的沟通方式",
            "避免二次创伤"
          ],
          keyPoints: [
            {
              icon: "🕊️",
              title: "安全空间",
              content: "创造心理安全的对话环境",
              example: "避免强迫分享、尊重沉默、给予控制权"
            }
          ],
          practiceScenarios: [
            {
              title: "创伤康复",
              description: "与经历创伤的人进行支持性对话",

            },
            {
              title: "敏感话题处理",
              description: "谨慎处理可能触发创伤的话题",

            },
            {
              title: "安全环境营造",
              description: "为创伤康复者创造安全的交流环境",

            },
            {
              title: "专业资源链接",
              description: "识别需要专业帮助的情况并做好转介",

            }
          ]
        },
        32: {
          id: 32,
          name: "情感复原",
          description: "掌握从负面情感经历中恢复和成长的方法。",

          estimatedTime: 40,
          learnerCount: 198,


          tags: ["复原", "成长", "韧性"],
          objectives: [
            "建立情感韧性",
            "学会从挫折中学习",
            "发展积极应对策略",
            "寻求适当的支持资源"
          ],
          keyPoints: [
            {
              icon: "🌱",
              title: "创伤后成长",
              content: "从困难经历中发现意义和成长",
              example: "识别经历带来的新视角和能力"
            }
          ],
          practiceScenarios: [
            {
              title: "职场挫折",
              description: "从工作失败中恢复并成长",

            },
            {
              title: "关系破裂复原",
              description: "从重要关系的结束中重新开始",

            },
            {
              title: "失去亲人哀伤",
              description: "处理失去重要人物的哀伤过程",

            },
            {
              title: "意外创伤处理",
              description: "从突发事件中恢复并重建生活",

            }
          ]
        },
        33: {
          id: 33,
          name: "情感表达艺术",
          description: "学会用绘画、音乐、写作等艺术形式表达和处理情感。",

          estimatedTime: 45,
          learnerCount: 167,


          tags: ["艺术", "创意表达", "处理"],
          objectives: [
            "探索不同的艺术表达形式",
            "学会通过创作释放情感",
            "发展个人的表达风格",
            "用艺术促进情感疗愈"
          ],
          keyPoints: [
            {
              icon: "🎨",
              title: "表达性艺术",
              content: "不追求技巧，重在情感表达",
              example: "用颜色表达心情、用音乐释放情感"
            }
          ],
          practiceScenarios: [
            {
              title: "情感绘画",
              description: "通过绘画表达内心复杂情感",

            },
            {
              title: "音乐情感日记",
              description: "用音乐记录和表达每日情感",

            },
            {
              title: "诗歌创作疗愈",
              description: "通过写诗处理内心困扰",

            },
            {
              title: "舞蹈情感释放",
              description: "用身体动作表达和释放压抑情感",

            }
          ]
        },
        34: {
          id: 34,
          name: "情感记忆",
          description: "学会处理痛苦的情感记忆，保留积极的情感体验。",

          estimatedTime: 38,
          learnerCount: 145,


          tags: ["记忆", "处理", "保留"],
          objectives: [
            "理解情感记忆的形成机制",
            "学会重构负面记忆",
            "强化积极情感记忆",
            "建立情感记忆管理策略"
          ],
          keyPoints: [
            {
              icon: "🧠",
              title: "记忆重构",
              content: "改变对过去事件的情感解读",
              example: "从失败中看到学习机会"
            }
          ],
          practiceScenarios: [
            {
              title: "童年创伤",
              description: "处理童年的负面情感记忆",

            },
            {
              title: "记忆重新叙述",
              description: "用新视角重新理解过去事件",

            },
            {
              title: "积极记忆强化",
              description: "培养和强化美好的情感记忆",

            },
            {
              title: "记忆日记疗法",
              description: "通过写作处理复杂的情感记忆",

            }
          ]
        },
        35: {
          id: 35,
          name: "情感成熟",
          description: "培养情感成熟度，在复杂情况下保持理智。",

          estimatedTime: 42,
          learnerCount: 123,


          tags: ["成熟", "理智", "复杂"],
          objectives: [
            "发展情感自我调节能力",
            "学会延迟满足",
            "在冲突中保持冷静",
            "承担情感责任"
          ],
          keyPoints: [
            {
              icon: "⚖️",
              title: "情感平衡",
              content: "在理性和感性之间找到平衡",
              example: "承认情感同时运用理性思考"
            }
          ],
          practiceScenarios: [
            {
              title: "关系冲突",
              description: "在亲密关系冲突中保持成熟",

            },
            {
              title: "工作压力管理",
              description: "在高压工作环境中保持情感稳定",

            },
            {
              title: "延迟满足练习",
              description: "训练在诱惑面前的自控能力",

            },
            {
              title: "责任承担",
              description: "学会为自己的情感反应负责",

            }
          ]
        },
        36: {
          id: 36,
          name: "情感智慧",
          description: "整合各种情感技能，在生活中智慧地处理情感问题。",

          estimatedTime: 50,
          learnerCount: 89,


          tags: ["智慧", "综合", "应用"],
          objectives: [
            "整合情感认知和技能",
            "在复杂情况下做出明智决策",
            "指导他人情感发展",
            "建立情感智慧的生活方式"
          ],
          keyPoints: [
            {
              icon: "🔮",
              title: "情感洞察",
              content: "深度理解情感背后的需求和意义",
              example: "从愤怒中看到受伤，从焦虑中看到关爱"
            }
          ],
          practiceScenarios: [
            {
              title: "人生指导",
              description: "为他人提供情感智慧指导",

            },
            {
              title: "复杂决策",
              description: "在情感和理性冲突时做出明智选择",

            },
            {
              title: "团队情感管理",
              description: "运用情感智慧管理团队氛围",

            },
            {
              title: "生活导师",
              description: "成为他人的情感智慧导师",

            }
          ]
        },
        37: {
          id: 37,
          name: "正念情感",
          description: "学会不带判断地观察和体验情感，培养情感觉察力。",

          estimatedTime: 32,
          learnerCount: 234,


          tags: ["正念", "觉察", "观察"],
          objectives: [
            "掌握正念观察技巧",
            "学会不评判地体验情感",
            "提高情感觉察敏感度",
            "在日常生活中应用正念"
          ],
          keyPoints: [
            {
              icon: "🧘",
              title: "正念观察",
              content: "如观察云朵般观察情感的来去",
              example: "注意到愤怒升起、经历、消退的过程"
            }
          ],
          practiceScenarios: [
            {
              title: "情绪冥想",
              description: "在冥想中观察情绪的流动",

            },
            {
              title: "日常觉察练习",
              description: "在日常活动中练习情感觉察",

            },
            {
              title: "身体扫描",
              description: "通过身体感觉观察情感变化",

            },
            {
              title: "情感标记",
              description: "正念地标记和命名情感状态",

            }
          ]
        },
        38: {
          id: 38,
          name: "情感沟通",
          description: "学会在亲密关系中开诚布公地讨论情感话题。",

          estimatedTime: 33,
          learnerCount: 178,


          tags: ["沟通", "亲密关系", "开放"],
          objectives: [
            "创造安全的情感对话环境",
            "学会表达脆弱和需求",
            "处理情感对话中的冲突",
            "深化情感连接"
          ],
          keyPoints: [
            {
              icon: "💬",
              title: "情感透明",
              content: "诚实分享内心真实感受",
              example: "我感到被忽视时会很难过"
            }
          ],
          practiceScenarios: [
            {
              title: "伴侣对话",
              description: "与伴侣深入讨论情感需求",

            },
            {
              title: "家庭情感分享",
              description: "在家庭中开放地讨论情感话题",

            },
            {
              title: "友谊深化",
              description: "与朋友分享更深层的情感体验",

            },
            {
              title: "情感冲突处理",
              description: "在情感分歧时保持开放沟通",

            }
          ]
        },
        // 关系建立新增技能 (ID 39-51)
        39: {
          id: 39,
          name: "自我介绍",
          description: "学会在不同场合进行恰当且有吸引力的自我介绍。",

          estimatedTime: 15,
          learnerCount: 612,


          tags: ["介绍", "第一印象", "基础"],
          objectives: [
            "掌握自我介绍的基本结构",
            "根据场合调整介绍内容",
            "展现自信和真实的形象",
            "留下积极的第一印象"
          ],
          keyPoints: [
            {
              icon: "👋",
              title: "简洁有力",
              content: "30秒内传达关键信息",
              example: "我是小王，资深产品经理，专注用户体验设计"
            }
          ],
          practiceScenarios: [
            {
              title: "职场聚会",
              description: "在公司新人欢迎会上自我介绍",

            }
          ]
        },
        40: {
          id: 40,
          name: "破冰对话",
          description: "掌握开启对话的技巧，在各种社交场合自然地开始交流。",

          estimatedTime: 18,
          learnerCount: 578,


          tags: ["破冰", "开场", "社交"],
          objectives: [
            "学会观察环境寻找话题",
            "掌握安全的开场话题",
            "营造轻松的对话氛围",
            "建立初步的连接"
          ],
          keyPoints: [
            {
              icon: "🧊",
              title: "环境观察",
              content: "从当下情境中寻找自然话题",
              example: "这个活动很有趣呢，你是怎么知道的？"
            }
          ],
          practiceSteps: [
            {
              title: "环境扫描",
              description: "进入新环境时先观察周围的人和事",
              tips: "注意活动主题、装饰、其他人的状态等可聊的话题"
            },
            {
              title: "安全开场",
              description: "选择中性、积极的话题开始对话",
              tips: "避免个人隐私话题，从当下共同体验开始"
            },
            {
              title: "观察反应",
              description: "注意对方的回应，调整对话方向",
              tips: "如果对方回应积极就继续，如果冷淡就礼貌结束"
            },
            {
              title: "自然过渡",
              description: "从破冰话题自然过渡到更深入的交流",
              tips: "根据对方的兴趣点展开进一步的对话"
            }
          ],
          practiceScenarios: [
            {
              title: "电梯偶遇",
              description: "在电梯里与陌生同事开始对话",

            }
          ]
        },
        41: {
          id: 41,
          name: "共同话题",
          description: "快速找到和他人的共同兴趣点，建立话题连接。",

          estimatedTime: 22,
          learnerCount: 445,


          tags: ["共同点", "兴趣", "连接"],
          objectives: [
            "学会探索对方的兴趣爱好",
            "发现共同经历和观点",
            "利用共同话题深化交流",
            "建立情感共鸣"
          ],
          keyPoints: [
            {
              icon: "🎯",
              title: "兴趣探测",
              content: "通过开放式问题了解对方喜好",
              example: "你平时喜欢什么样的音乐/电影？"
            }
          ],
          practiceScenarios: [
            {
              title: "咖啡厅邂逅",
              description: "与邻桌客人发现共同兴趣",

            }
          ]
        },
        42: {
          id: 42,
          name: "信任建立",
          description: "通过言行一致和真诚沟通，逐步建立他人对你的信任。",

          estimatedTime: 35,
          learnerCount: 367,


          tags: ["信任", "真诚", "一致性"],
          objectives: [
            "展现真实可靠的品格",
            "保持言行一致",
            "尊重承诺和约定",
            "建立长期信任关系"
          ],
          keyPoints: [
            {
              icon: "🤝",
              title: "言行一致",
              content: "说到做到，建立可信形象",
              example: "承诺的事情按时完成，坦诚自己的局限"
            }
          ],
          practiceScenarios: [
            {
              title: "团队协作",
              description: "在项目中建立队友信任",

            }
          ]
        },
        43: {
          id: 43,
          name: "社交恐惧",
          description: "克服社交焦虑，在人群中保持自然和自信。",

          estimatedTime: 40,
          learnerCount: 523,


          tags: ["恐惧", "焦虑", "自信"],
          objectives: [
            "理解社交恐惧的根源",
            "学会放松和自我调节技巧",
            "逐步扩大舒适圈",
            "建立社交自信"
          ],
          keyPoints: [
            {
              icon: "😰",
              title: "渐进暴露",
              content: "从小规模社交开始练习",
              example: "从一对一对话到小组讨论再到大型聚会"
            }
          ],
          practiceScenarios: [
            {
              title: "大型聚会",
              description: "在陌生人很多的派对中社交",

            }
          ]
        },
        44: {
          id: 44,
          name: "网络社交",
          description: "在数字化时代学会线上社交，建立虚拟关系。",

          estimatedTime: 25,
          learnerCount: 734,


          tags: ["线上", "数字", "虚拟"],
          objectives: [
            "掌握线上沟通的特点",
            "学会通过文字表达情感",
            "维护线上关系的温度",
            "将线上关系转化为线下友谊"
          ],
          keyPoints: [
            {
              icon: "💻",
              title: "数字表达",
              content: "用文字、表情符号传达情感",
              example: "合理使用表情包、及时回复、主动关心"
            }
          ],
          practiceScenarios: [
            {
              title: "微信群聊",
              description: "在工作群中建立良好关系",

            }
          ]
        },
        45: {
          id: 45,
          name: "跨文化交流",
          description: "在多元文化环境中建立跨文化的友谊和合作关系。",

          estimatedTime: 45,
          learnerCount: 289,


          tags: ["文化", "多元", "国际"],
          objectives: [
            "了解不同文化的社交习俗",
            "学会尊重文化差异",
            "找到跨文化的共同点",
            "建立国际化视野"
          ],
          keyPoints: [
            {
              icon: "🌍",
              title: "文化敏感",
              content: "尊重不同文化背景的交流方式",
              example: "了解问候方式、时间观念、个人空间等差异"
            }
          ],
          practiceScenarios: [
            {
              title: "国际会议",
              description: "与来自不同国家的同事建立关系",

            }
          ]
        },
        46: {
          id: 46,
          name: "关系维护",
          description: "学会维持长期的人际关系，保持联系和关心。",

          estimatedTime: 30,
          learnerCount: 456,


          tags: ["维护", "长期", "关心"],
          objectives: [
            "建立定期联系的习惯",
            "记住重要的日子和事件",
            "在关键时刻提供支持",
            "保持关系的新鲜感"
          ],
          keyPoints: [
            {
              icon: "📱",
              title: "主动关心",
              content: "定期主动联系，关心近况",
              example: "生日问候、工作关心、分享有趣内容"
            }
          ],
          practiceScenarios: [
            {
              title: "老友重聚",
              description: "与多年未见的朋友重新建立联系",

            }
          ]
        },
        47: {
          id: 47,
          name: "关系边界",
          description: "在建立关系的同时保持适当的个人边界。",

          estimatedTime: 28,
          learnerCount: 334,


          tags: ["边界", "平衡", "个人空间"],
          objectives: [
            "识别自己的交往边界",
            "学会说不而不伤害关系",
            "平衡亲密与独立",
            "尊重他人的边界"
          ],
          keyPoints: [
            {
              icon: "🚧",
              title: "健康边界",
              content: "在亲密和独立之间找到平衡",
              example: "可以拒绝不合理要求，保留个人时间和空间"
            }
          ],
          practiceScenarios: [
            {
              title: "过度依赖",
              description: "应对朋友的过度情感依赖",

            }
          ]
        },
        48: {
          id: 48,
          name: "群体融入",
          description: "快速融入新的群体或团队，建立归属感。",

          estimatedTime: 32,
          learnerCount: 567,


          tags: ["融入", "群体", "归属感"],
          objectives: [
            "观察群体的文化和规则",
            "找到自己在群体中的位置",
            "为群体贡献价值",
            "建立多重连接"
          ],
          keyPoints: [
            {
              icon: "👥",
              title: "观察适应",
              content: "先观察群体动态再主动融入",
              example: "了解群体的沟通方式、价值观和潜规则"
            }
          ],
          practiceScenarios: [
            {
              title: "新部门入职",
              description: "快速融入新的工作团队",

            }
          ]
        },
        49: {
          id: 49,
          name: "社交影响力",
          description: "学会在群体中发挥积极影响，成为受欢迎的人。",

          estimatedTime: 38,
          learnerCount: 234,


          tags: ["影响力", "魅力", "领导力"],
          objectives: [
            "发展个人魅力和感染力",
            "学会鼓舞和激励他人",
            "在群体中发挥正面作用",
            "建立个人品牌形象"
          ],
          keyPoints: [
            {
              icon: "⭐",
              title: "正向影响",
              content: "用积极态度感染和鼓舞他人",
              example: "分享正能量、支持他人成长、解决群体问题"
            }
          ],
          practiceScenarios: [
            {
              title: "团队士气",
              description: "在团队低潮时提升大家的士气",

            }
          ]
        },
        50: {
          id: 50,
          name: "关系修复",
          description: "学会修复受损的人际关系，重建信任和友谊。",

          estimatedTime: 35,
          learnerCount: 198,


          tags: ["修复", "和解", "重建"],
          objectives: [
            "勇敢面对关系中的问题",
            "学会道歉和原谅的艺术",
            "找到双方都能接受的解决方案",
            "重建更强的关系基础"
          ],
          keyPoints: [
            {
              icon: "🔧",
              title: "诚心和解",
              content: "真诚地承认错误并寻求和解",
              example: "我意识到我的行为伤害了你，我很抱歉"
            }
          ],
          practiceScenarios: [
            {
              title: "友谊危机",
              description: "修复因误解而破裂的友谊",

            }
          ]
        },
        51: {
          id: 51,
          name: "社交礼仪",
          description: "掌握各种场合的社交礼仪，展现良好的个人修养。",

          estimatedTime: 20,
          learnerCount: 678,


          tags: ["礼仪", "修养", "场合"],
          objectives: [
            "了解基本的社交礼仪规范",
            "在不同场合表现得体",
            "展现尊重和教养",
            "给他人留下良好印象"
          ],
          keyPoints: [
            {
              icon: "🎩",
              title: "得体表现",
              content: "在各种场合都保持适当的言行",
              example: "握手、用餐、着装、时间观念等方面的礼仪"
            }
          ],
          practiceScenarios: [
            {
              title: "商务晚宴",
              description: "在正式商务晚宴中展现礼仪",

            }
          ]
        },
        // 特殊情境新增技能 (ID 52-65)
        52: {
          id: 52,
          name: "医患沟通",
          description: "在医疗环境中进行有效的医患沟通，建立信任和理解。",

          estimatedTime: 45,
          learnerCount: 234,


          tags: ["医疗", "专业", "信任"],
          objectives: [
            "学会用患者能理解的语言解释病情",
            "建立医患之间的信任关系",
            "处理患者的焦虑和恐惧情绪",
            "在紧急情况下保持冷静沟通"
          ],
          keyPoints: [
            {
              icon: "🏥",
              title: "专业关怀",
              content: "结合专业知识与人文关怀",
              example: "用简单词汇解释复杂病情，给予情感支持"
            }
          ],
          practiceScenarios: [
            {
              title: "告知诊断",
              description: "向患者告知重大疾病诊断",

            }
          ]
        },
        53: {
          id: 53,
          name: "师生互动",
          description: "在教育环境中建立良好的师生关系，促进学习效果。",

          estimatedTime: 35,
          learnerCount: 456,


          tags: ["教育", "师生", "学习"],
          objectives: [
            "创造开放包容的学习环境",
            "激发学生的学习兴趣",
            "给予恰当的指导和反馈",
            "处理课堂管理问题"
          ],
          keyPoints: [
            {
              icon: "📚",
              title: "教学相长",
              content: "在教学中建立平等互动关系",
              example: "鼓励提问、尊重不同观点、个性化指导"
            }
          ],
          practiceScenarios: [
            {
              title: "课堂讨论",
              description: "引导学生进行深度课堂讨论",

            }
          ]
        },
        54: {
          id: 54,
          name: "客服技巧",
          description: "在客户服务中处理各种客户问题，维护良好的客户关系。",

          estimatedTime: 30,
          learnerCount: 567,


          tags: ["服务", "客户", "问题解决"],
          objectives: [
            "保持耐心和专业的服务态度",
            "有效解决客户问题",
            "处理客户投诉和不满",
            "提升客户满意度"
          ],
          keyPoints: [
            {
              icon: "📞",
              title: "服务至上",
              content: "以客户需求为中心提供解决方案",
              example: "主动倾听、快速响应、超出期待的服务"
            }
          ],
          practiceScenarios: [
            {
              title: "产品投诉",
              description: "处理客户对产品质量的投诉",

            }
          ]
        },
        55: {
          id: 55,
          name: "销售沟通",
          description: "在销售过程中建立客户信任，实现双赢的销售结果。",

          estimatedTime: 40,
          learnerCount: 389,


          tags: ["销售", "说服", "双赢"],
          objectives: [
            "了解客户真实需求",
            "建立产品价值认知",
            "处理客户异议和担忧",
            "达成互利共赢的协议"
          ],
          keyPoints: [
            {
              icon: "💼",
              title: "顾问式销售",
              content: "以解决客户问题为出发点",
              example: "深入了解需求、提供专业建议、建立长期关系"
            }
          ],
          practiceScenarios: [
            {
              title: "大客户谈判",
              description: "与重要客户进行合作洽谈",

            }
          ]
        },
        56: {
          id: 56,
          name: "法庭辩论",
          description: "在法律环境中进行有效的论证和辩护，保护当事人权益。",

          estimatedTime: 50,
          learnerCount: 156,


          tags: ["法律", "辩论", "逻辑"],
          objectives: [
            "构建清晰的论证逻辑",
            "有效反驳对方观点",
            "控制情绪保持理性",
            "说服法官和陪审团"
          ],
          keyPoints: [
            {
              icon: "⚖️",
              title: "逻辑严密",
              content: "用事实和法律条文支撑论点",
              example: "证据链完整、逻辑清晰、情理并茂"
            }
          ],
          practiceScenarios: [
            {
              title: "民事诉讼",
              description: "在民事案件中为当事人辩护",

            }
          ]
        },
        57: {
          id: 57,
          name: "媒体采访",
          description: "在媒体面前表达观点，管理公众形象和信息传递。",

          estimatedTime: 35,
          learnerCount: 234,


          tags: ["媒体", "公关", "形象"],
          objectives: [
            "准备关键信息和观点",
            "控制采访节奏和方向",
            "处理尖锐或敏感问题",
            "维护个人或组织形象"
          ],
          keyPoints: [
            {
              icon: "🎤",
              title: "信息控制",
              content: "传达核心信息同时避免误导",
              example: "准备关键话术、预判问题、保持冷静"
            }
          ],
          practiceScenarios: [
            {
              title: "危机公关",
              description: "在公司危机时接受媒体采访",

            }
          ]
        },
        58: {
          id: 58,
          name: "心理咨询",
          description: "在心理咨询中建立安全的治疗关系，帮助来访者成长。",

          estimatedTime: 60,
          learnerCount: 178,


          tags: ["心理", "治疗", "成长"],
          objectives: [
            "建立安全的咨询关系",
            "运用专业的咨询技术",
            "促进来访者的自我探索",
            "维护专业边界和伦理"
          ],
          keyPoints: [
            {
              icon: "🧠",
              title: "专业陪伴",
              content: "提供无条件的积极关注",
              example: "倾听、共情、反映、澄清、解释"
            }
          ],
          practiceScenarios: [
            {
              title: "抑郁咨询",
              description: "帮助抑郁症来访者重建希望",

            }
          ]
        },
        59: {
          id: 59,
          name: "跨国商务",
          description: "在国际商务环境中进行有效的跨文化商务沟通。",

          estimatedTime: 45,
          learnerCount: 267,


          tags: ["国际", "商务", "文化"],
          objectives: [
            "了解不同国家的商务文化",
            "适应不同的谈判风格",
            "建立国际商务关系",
            "处理跨文化误解"
          ],
          keyPoints: [
            {
              icon: "🌐",
              title: "文化智慧",
              content: "结合商务目标与文化敏感性",
              example: "尊重时间观念、礼仪习俗、决策方式差异"
            }
          ],
          practiceScenarios: [
            {
              title: "国际合作",
              description: "与日本公司洽谈合作项目",

            }
          ]
        },
        60: {
          id: 60,
          name: "家庭调解",
          description: "在家庭矛盾中发挥调解作用，促进家庭和谐。",

          estimatedTime: 40,
          learnerCount: 345,


          tags: ["家庭", "调解", "和谐"],
          objectives: [
            "理解家庭动力学",
            "保持中立的调解立场",
            "促进家庭成员相互理解",
            "寻找共赢的解决方案"
          ],
          keyPoints: [
            {
              icon: "🏠",
              title: "家庭智慧",
              content: "平衡情感与理性，维护家庭关系",
              example: "倾听各方诉求、寻找共同点、建立规则"
            }
          ],
          practiceScenarios: [
            {
              title: "婆媳矛盾",
              description: "调解家庭中的婆媳关系问题",

            }
          ]
        },
        61: {
          id: 61,
          name: "团队建设",
          description: "在团队建设活动中促进成员间的信任和合作。",

          estimatedTime: 35,
          learnerCount: 456,


          tags: ["团队", "建设", "合作"],
          objectives: [
            "设计有效的团建活动",
            "促进团队成员相互了解",
            "建立团队共同目标",
            "提升团队凝聚力"
          ],
          keyPoints: [
            {
              icon: "🤝",
              title: "团队融合",
              content: "通过活动促进深度交流",
              example: "破冰游戏、挑战任务、分享环节"
            }
          ],
          practiceScenarios: [
            {
              title: "新团队组建",
              description: "为新成立的项目团队进行团建",

            }
          ]
        },
        62: {
          id: 62,
          name: "志愿服务",
          description: "在志愿服务中与受助者建立尊重平等的关系。",

          estimatedTime: 30,
          learnerCount: 523,


          tags: ["志愿", "服务", "平等"],
          objectives: [
            "以尊重的态度提供帮助",
            "了解受助者的真实需求",
            "建立平等的服务关系",
            "促进受助者的自主发展"
          ],
          keyPoints: [
            {
              icon: "❤️",
              title: "平等服务",
              content: "尊重受助者的尊严和选择权",
              example: "询问需求、提供选择、尊重决定"
            }
          ],
          practiceScenarios: [
            {
              title: "社区服务",
              description: "为社区独居老人提供帮助",

            }
          ]
        },
        63: {
          id: 63,
          name: "学术交流",
          description: "在学术环境中进行有效的学术讨论和知识分享。",

          estimatedTime: 40,
          learnerCount: 198,


          tags: ["学术", "研究", "交流"],
          objectives: [
            "清晰表达研究观点",
            "进行建设性的学术辩论",
            "接受同行评议和建议",
            "促进学术合作"
          ],
          keyPoints: [
            {
              icon: "🎓",
              title: "学术严谨",
              content: "以开放态度进行学术探讨",
              example: "数据支撑、逻辑清晰、承认局限性"
            }
          ],
          practiceScenarios: [
            {
              title: "学术会议",
              description: "在国际学术会议上展示研究成果",

            }
          ]
        },
        64: {
          id: 64,
          name: "危机干预",
          description: "在心理危机情况下进行有效的干预和支持。",

          estimatedTime: 55,
          learnerCount: 145,


          tags: ["危机", "干预", "支持"],
          objectives: [
            "识别自杀或自伤风险",
            "提供即时的心理支持",
            "连接专业资源",
            "确保当事人安全"
          ],
          keyPoints: [
            {
              icon: "🚨",
              title: "生命第一",
              content: "优先保障当事人的生命安全",
              example: "评估风险、建立联系、寻求帮助、持续关注"
            }
          ],
          practiceScenarios: [
            {
              title: "自杀预防",
              description: "帮助有自杀倾向的朋友",

            }
          ]
        },
        65: {
          id: 65,
          name: "网络调解",
          description: "在网络争议中发挥调解作用，化解网络冲突。",

          estimatedTime: 30,
          learnerCount: 234,


          tags: ["网络", "调解", "冲突"],
          objectives: [
            "理解网络沟通的特点",
            "冷静处理网络争议",
            "促进理性对话",
            "维护网络环境和谐"
          ],
          keyPoints: [
            {
              icon: "💻",
              title: "理性引导",
              content: "用理性和善意化解网络冲突",
              example: "客观分析、理性回应、私下沟通"
            }
          ],
          practiceScenarios: [
            {
              title: "网络争论",
              description: "调解社交媒体上的激烈争论",

            }
          ]
        }
      };

      // 根据 skillId 获取对应数据，如果没有匹配则使用默认数据
      const skillData = skillDataMap[this.skillId] || skillDataMap[1];
      this.skillData = skillData;

      // 相关技能推荐 - 基于分类的动态推荐
      this.relatedSkills = this.generateRelatedSkills();
    },

    generateRelatedSkills() {
      // 根据分类定义技能范围
      const categorySkillRanges = {
        'communication': { start: 1, end: 25, name: '沟通表达' },
        'emotional_expression': { start: 26, end: 38, name: '情感理解' },
        'relationship_building': { start: 39, end: 51, name: '关系建立' },
        'special_scenarios': { start: 52, end: 65, name: '特殊情境' }
      };

      // 确定当前技能的分类
      let currentCategory = null;
      for (const [categoryId, range] of Object.entries(categorySkillRanges)) {
        if (this.skillId >= range.start && this.skillId <= range.end) {
          currentCategory = categoryId;
          break;
        }
      }

      // 如果没有找到分类，使用传入的categoryId
      if (!currentCategory) {
        currentCategory = this.categoryId || 'communication';
      }

      // 获取当前分类下所有技能的ID列表
      const categoryRange = categorySkillRanges[currentCategory];
      const skillIds = [];
      for (let i = categoryRange.start; i <= categoryRange.end; i++) {
        if (i !== parseInt(this.skillId)) { // 排除当前技能
          skillIds.push(i);
        }
      }

      // 如果技能数量不足2个，从其他分类补充
      if (skillIds.length < 2) {
        const otherCategories = Object.keys(categorySkillRanges).filter(cat => cat !== currentCategory);
        for (const otherCategory of otherCategories) {
          const otherRange = categorySkillRanges[otherCategory];
          for (let i = otherRange.start; i <= otherRange.end; i++) {
            if (skillIds.length >= 4) break; // 最多准备4个候选
            skillIds.push(i);
          }
          if (skillIds.length >= 4) break;
        }
      }

      // 随机选择2个技能
      const selectedSkills = this.getRandomSkills(skillIds, 2);

      // 构建技能详情数据
      return selectedSkills.map(skillId => this.getSkillBrief(skillId));
    },

    getRandomSkills(skillIds, count) {
      const shuffled = [...skillIds].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    },

    getSkillBrief(skillId) {
      // 技能名称和简介数据
      const skillBriefs = {
        // 沟通表达 (1-25)
        1: { name: "主动倾听", brief: "学会用心倾听对方的话语和情感" },
        2: { name: "情感表达", brief: "准确表达自己的情感和需求" },
        3: { name: "非暴力沟通", brief: "以善意和理解进行沟通" },
        4: { name: "情绪识别", brief: "准确识别自己和他人的情绪状态" },
        5: { name: "情感共鸣", brief: "与他人产生情感共鸣和理解" },
        6: { name: "情绪调节", brief: "学会管理和调节自己的情绪" },
        7: { name: "破冰技巧", brief: "在新环境中快速与他人建立联系" },
        8: { name: "信任建立", brief: "在关系中建立互相信任的基础" },
        9: { name: "冲突解决", brief: "有效处理人际冲突和分歧" },
        10: { name: "职场沟通", brief: "在工作环境中进行专业有效的沟通" },
        11: { name: "异地恋维护", brief: "维护远距离恋爱关系的技巧" },
        12: { name: "危机干预", brief: "在紧急情况下提供心理支持" },
        13: { name: "清晰表达", brief: "用简洁明了的语言传达想法" },
        14: { name: "提问技巧", brief: "学会问出有价值的问题" },
        15: { name: "肢体语言", brief: "运用身体语言增强沟通效果" },
        16: { name: "故事叙述", brief: "用故事让沟通更有感染力" },
        17: { name: "公众演讲", brief: "在公众场合自信地表达观点" },
        18: { name: "说服技巧", brief: "学会以理服人的说服方法" },
        19: { name: "谈判协商", brief: "在谈判中达成双赢结果" },
        20: { name: "书面表达", brief: "通过文字清晰传达思想" },
        21: { name: "跨文化沟通", brief: "与不同文化背景的人有效交流" },
        22: { name: "团队协作沟通", brief: "在团队中促进有效协作" },
        23: { name: "客户沟通", brief: "与客户建立良好的沟通关系" },
        24: { name: "反馈技巧", brief: "给予和接受建设性反馈" },
        25: { name: "在线沟通", brief: "掌握数字化时代的沟通技巧" },

        // 情感理解 (26-38)
        26: { name: "情感词汇", brief: "扩展情感词汇，精确表达感受" },
        27: { name: "同理心训练", brief: "增强理解他人情感的能力" },
        28: { name: "情感边界", brief: "在情感交流中保护自己" },
        29: { name: "情绪传染", brief: "理解和管理情绪的传染性" },
        30: { name: "情感支持", brief: "给予他人恰当的情感支持" },
        31: { name: "创伤敏感", brief: "在交流中保持创伤敏感性" },
        32: { name: "情感复原", brief: "从负面情感经历中恢复" },
        33: { name: "情感表达艺术", brief: "用艺术形式表达和处理情感" },
        34: { name: "情感记忆", brief: "处理痛苦的情感记忆" },
        35: { name: "情感成熟", brief: "在复杂情况下保持情感理智" },
        36: { name: "情感智慧", brief: "智慧地处理各种情感问题" },
        37: { name: "正念情感", brief: "不带判断地观察和体验情感" },
        38: { name: "情感沟通", brief: "在亲密关系中开诚布公交流" },

        // 关系建立 (39-51)
        39: { name: "自我介绍", brief: "在不同场合进行恰当的自我介绍" },
        40: { name: "破冰对话", brief: "自然地开启对话和交流" },
        41: { name: "共同话题", brief: "快速找到和他人的共同兴趣点" },
        42: { name: "信任建立", brief: "通过真诚沟通建立信任" },
        43: { name: "社交恐惧", brief: "克服社交焦虑，保持自信" },
        44: { name: "网络社交", brief: "建立和维护线上人际关系" },
        45: { name: "跨文化交流", brief: "建立跨文化的友谊和合作" },
        46: { name: "关系维护", brief: "维持长期的人际关系" },
        47: { name: "关系边界", brief: "保持适当的个人边界" },
        48: { name: "群体融入", brief: "快速融入新的群体或团队" },
        49: { name: "社交影响力", brief: "在群体中发挥积极影响" },
        50: { name: "关系修复", brief: "修复受损的人际关系" },
        51: { name: "社交礼仪", brief: "掌握各种场合的社交礼仪" },

        // 特殊情境 (52-65)
        52: { name: "医患沟通", brief: "在医疗环境中进行有效沟通" },
        53: { name: "师生互动", brief: "建立良好的教育关系" },
        54: { name: "客服技巧", brief: "处理客户问题和投诉" },
        55: { name: "销售沟通", brief: "在销售中建立客户信任" },
        56: { name: "法庭辩论", brief: "在法律环境中进行有效论证" },
        57: { name: "媒体采访", brief: "面对媒体表达观点和管理形象" },
        58: { name: "心理咨询", brief: "建立安全的治疗关系" },
        59: { name: "跨国商务", brief: "进行跨文化商务沟通" },
        60: { name: "家庭调解", brief: "在家庭矛盾中发挥调解作用" },
        61: { name: "团队建设", brief: "促进团队成员间的信任合作" },
        62: { name: "志愿服务", brief: "与受助者建立尊重平等关系" },
        63: { name: "学术交流", brief: "进行有效的学术讨论" },
        64: { name: "危机干预", brief: "在心理危机中进行有效干预" },
        65: { name: "网络调解", brief: "化解网络争议和冲突" }
      };

      const skillData = skillBriefs[skillId];
      if (!skillData) {
        return {
          id: skillId,
          name: `技能${skillId}`,
          brief: "暂无描述",
        };
      }

      return {
        id: skillId,
        name: skillData.name,
        brief: skillData.brief
      };
    },

    startScenarioPractice() {
      // 传递完整的技能信息到练习页面
      const skillParams = {
        skillId: this.skillData.id,
        type: "practice",
        skillTitle: encodeURIComponent(this.skillData.name),
        skillContent: encodeURIComponent(this.skillData.description),
        skillTags: encodeURIComponent(JSON.stringify(this.skillData.tags)),
        skillScenarios: encodeURIComponent(
          JSON.stringify(this.skillData.scenarios || [])
        ),
      };

      const queryString = Object.entries(skillParams)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-practice?${queryString}`,
      });
    },

    startLearning() {
      this.startScenarioPractice();
    },

    continueLearning() {
      this.startScenarioPractice();
    },

    reviewSkill() {
      this.startScenarioPractice();
    },

    async generatePracticeScenario() {
      this.startScenarioPractice();
    },

    practiceScenario(scenario) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&scenarioId=${scenario.id}&type=scenario`,
      });
    },

    viewRelatedSkill(skill) {
      uni.navigateTo({
        url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.id}&categoryId=${this.categoryId}`,
      });
    },
  },
};
</script>

<style scoped>
.skill-detail-container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx;
  color: white;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.skill-basic-info {
  flex: 1;
}

.skill-title {
  font-size: 42rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
}

.skill-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
}

.meta-icon {
  font-size: 18rpx;
}

.meta-text {
  font-size: 22rpx;
  opacity: 0.9;
}

.skill-description {
  font-size: 26rpx;
  line-height: 1.6;
  opacity: 0.95;
  margin-bottom: 20rpx;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.skill-tag {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 22rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.3);
}

.content {
  padding: 0 40rpx;
}

.section {
  margin-bottom: 48rpx;
}

.section-header {
  margin-bottom: 24rpx;
  padding-top: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.objectives-list {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.objective-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.objective-item:last-child {
  margin-bottom: 0;
}

.objective-icon {
  color: #667eea;
  margin-right: 12rpx;
  font-size: 24rpx;
  line-height: 1.5;
}

.objective-text {
  flex: 1;
  font-size: 26rpx;
  color: #333;
  line-height: 1.5;
}

.key-points {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.point-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.point-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.point-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.point-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.point-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.point-example {
  background-color: #f8f9ff;
  padding: 16rpx;
  border-radius: 12rpx;
  border-left: 4rpx solid #667eea;
}

.example-label {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  margin-right: 8rpx;
}

.example-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.practice-steps {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.step-item {
  display: flex;
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.step-number {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
}

.step-text {
  color: white;
  font-size: 24rpx;
  font-weight: bold;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.step-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16rpx;
}

.step-tips {
  background-color: #f0f4ff;
  padding: 16rpx;
  border-radius: 12rpx;
  border-left: 4rpx solid #667eea;
}

.tips-label {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  margin-right: 8rpx;
}

.tips-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.scenarios {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.scenario-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.scenario-card:active {
  transform: translateY(2rpx);
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.scenario-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.scenario-description {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 20rpx;
}

.scenario-action {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8rpx;
  color: #667eea;
}

.action-text {
  font-size: 26rpx;
}

.action-arrow {
  font-size: 24rpx;
}

.related-skills {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.related-skill-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s ease;
}

.related-skill-card:active {
  transform: translateY(2rpx);
}

.related-skill-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.related-skill-desc {
  font-size: 24rpx;
  color: #666;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 24rpx 40rpx;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
}

.action-btn {
  width: 60%;
  padding: 28rpx 40rpx;
  border-radius: 16rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: bold;
  transition: all 0.2s ease;
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.3);
}

.action-btn:active {
  transform: translateY(2rpx);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background-color: #4caf50;
  color: white;
}

.action-btn.tertiary {
  background-color: #f0f0f0;
  color: #666;
  border: 2rpx solid #e0e0e0;
}

.btn-text {
  font-size: 28rpx;
}
</style>
