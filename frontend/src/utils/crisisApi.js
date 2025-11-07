// 心理危机预警API工具函数
// file: ariadne/frontend/src/utils/crisisApi.js

const BASE_URL = process.env.VUE_APP_API_BASE_URL || "http://localhost:8000";

/**
 * 心理危机预警API工具类
 */
export class CrisisAPI {
  /**
   * 获取访问token
   */
  static getAuthHeader() {
    const token = uni.getStorageSync("access_token");
    return {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  }

  /**
   * AI增强型风险评估
   * @param {string} content - 用户输入内容
   * @param {string} scene - 聊天场景
   * @param {number} keywordScore - 关键词得分
   * @returns {Promise} 风险评估结果
   */
  static async assessRiskEnhanced(content, scene = "", keywordScore = 0) {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/assess-risk`,
        method: "POST",
        header: this.getAuthHeader(),
        data: {
          content: content,
          scene: scene,
          keyword_score: keywordScore,
          enable_ai_analysis: true, // 启用AI分析
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`AI评估失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }

  /**
   * 执行风险评估
   * @param {number} days - 分析天数，默认14天
   * @returns {Promise} 风险评估结果
   */
  static async assessRisk(days = 14) {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/assess-risk?days=${days}`,
        method: "POST",
        header: this.getAuthHeader(),
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`评估失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }

  /**
   * 获取用户预警记录
   * @param {Object} options - 查询选项
   * @param {number} options.days - 天数
   * @param {boolean} options.unresolvedOnly - 是否只获取未解决的
   * @returns {Promise} 预警记录列表
   */
  static async getWarnings(options = {}) {
    const { days = 30, unresolvedOnly = false } = options;

    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/warnings`,
        method: "GET",
        data: {
          days: days,
          unresolved_only: unresolvedOnly,
        },
        header: this.getAuthHeader(),
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`获取预警记录失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }

  /**
   * 解决预警
   * @param {number} warningId - 预警ID
   * @param {string} notes - 解决备注
   * @returns {Promise} 操作结果
   */
  static async resolveWarning(warningId, notes = "") {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/warnings/${warningId}/resolve`,
        method: "POST",
        data: {
          resolver_notes: notes,
        },
        header: this.getAuthHeader(),
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`解决预警失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }

  /**
   * 获取风险统计信息
   * @param {number} days - 统计天数
   * @returns {Promise} 统计数据
   */
  static async getStatistics(days = 30) {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/statistics?days=${days}`,
        method: "GET",
        header: this.getAuthHeader(),
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`获取统计失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }

  /**
   * 触发后台风险检查
   * @returns {Promise} 操作结果
   */
  static async triggerBackgroundCheck() {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${BASE_URL}/crisis/background-check`,
        method: "POST",
        header: this.getAuthHeader(),
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`触发检查失败: ${res.statusCode}`));
          }
        },
        fail: (err) => {
          reject(new Error(`网络错误: ${err.errMsg}`));
        },
      });
    });
  }
}

/**
 * 心理危机关键词快速检测工具（增强版）
 */
export class CrisisKeywordDetector {
  constructor() {
    // 初始化同音字映射表和模糊匹配规则
    this.initSimilarityMaps();
  }

  // 危机关键词配置（与后端保持一致）
  static CRISIS_KEYWORDS = {
    自伤: [
      "自杀",
      "自残",
      "自伤",
      "结束生命",
      "不想活",
      "想死",
      "自我了断",
      "轻生",
      "了结",
      "自了",
      "了断",
      "去死",
      "想去死",
      "要去死",
      "寻死",
      "找死",
      "赴死",
      "死了算了",
      "一死了之",
      "以死解脱",
    ],
    绝望: [
      "绝望",
      "无望",
      "没有希望",
      "看不到未来",
      "一片黑暗",
      "无路可走",
      "走投无路",
      "没救",
      "完了",
      "没意思",
      "活着没意义",
      "没活路",
    ],
    孤独: [
      "孤独",
      "孤单",
      "没人理解",
      "没人关心",
      "被遗弃",
      "被抛弃",
      "无人陪伴",
      "一个人",
      "形只影单",
      "无依无靠",
      "孑然一身",
    ],
    无价值感: [
      "没用",
      "无价值",
      "废物",
      "垃圾",
      "拖累",
      "负担",
      "没意义",
      "多余",
      "无能",
      "失败者",
      "活该",
      "该死",
      "不配",
    ],
    极端情绪: [
      "崩溃",
      "疯了",
      "受不了",
      "痛苦",
      "煎熬",
      "折磨",
      "地狱",
      "末日",
      "撑不住",
      "要疯",
      "要死",
      "快死了",
      "死掉算了",
    ],
  };

  // 同音字和近似词映射（增强版）
  static HOMOPHONE_MAP = {
    死: ["4", "si", "Si", "SI", "sǐ", "撕", "丝", "斯"],
    杀: ["sha", "煞", "刹", "沙"],
    痛: ["疼", "tong", "tòng", "痛苦"],
    苦: ["ku", "kǔ", "库", "哭"],
    哭: ["ku", "kū", "库", "苦"],
    累: ["lei", "lèi", "类", "泪"],
    绝: ["jue", "juē", "绝", "决"],
    望: ["wang", "wàng", "忘", "旺"],
    没: ["mei", "méi", "美", "没有"],
    无: ["wu", "wú", "五", "吴", "无"],
    不: ["bu", "bù", "步", "布", "不要"],
    想: ["xiang", "xiǎng", "想要", "想念"],
  };

  // 拆字和变形映射（增强版）
  static VARIANT_MAP = {
    自杀: [
      "zi sha",
      "自 杀",
      "自_杀",
      "自-杀",
      "自*杀",
      "zi4",
      "zisha",
      "自s",
      "自4",
      "zs",
    ],
    想死: [
      "想 死",
      "想4",
      "想si",
      "xiang死",
      "想sǐ",
      "xiang4",
      "想 4",
      "xiang si",
      "xiangsi",
    ],
    去死: ["去 死", "去4", "qu死", "去si", "qu si", "qusi", "qs"],
    要死: ["要 死", "要4", "yao死", "要si", "yao si", "yaosi"],
    绝望: ["绝 望", "jue望", "绝wang", "jué望", "绝 wang", "juewang"],
    崩溃: ["崩 溃", "beng溃", "崩kui", "běng溃", "崩 kui", "bengkui"],
    痛苦: ["痛 苦", "tong苦", "痛ku", "tòng苦", "痛 ku", "tongku"],
    不想活: [
      "不想 活",
      "不 想活",
      "buxianghuo",
      "不想huo",
      "b想活",
      "不xiang活",
    ],
    活着没意义: ["活着 没意义", "活 着没意义", "没 意义"],
    结束生命: ["结束 生命", "结 束生命", "jieshu生命"],
    轻生: ["轻 生", "qing生", "qīng生"],
  };

  /**
   * 初始化相似度映射表
   */
  initSimilarityMaps() {
    this.expandedKeywords = new Set();

    // 扩展原有关键词
    for (const [category, keywords] of Object.entries(
      CrisisKeywordDetector.CRISIS_KEYWORDS
    )) {
      for (const keyword of keywords) {
        this.expandedKeywords.add(keyword);

        // 添加同音字变体
        this.addHomophoneVariants(keyword);

        // 添加拆字变体
        this.addVariantForms(keyword);
      }
    }
  }

  /**
   * 添加同音字变体
   */
  addHomophoneVariants(keyword) {
    for (const [char, variants] of Object.entries(
      CrisisKeywordDetector.HOMOPHONE_MAP
    )) {
      if (keyword.includes(char)) {
        for (const variant of variants) {
          this.expandedKeywords.add(keyword.replace(char, variant));
        }
      }
    }
  }

  /**
   * 添加拆字变体
   */
  addVariantForms(keyword) {
    if (CrisisKeywordDetector.VARIANT_MAP[keyword]) {
      for (const variant of CrisisKeywordDetector.VARIANT_MAP[keyword]) {
        this.expandedKeywords.add(variant);
      }
    }
  }

  /**
   * 增强型关键词检测（支持模糊匹配、同音字等）
   * @param {string} text - 要检测的文本
   * @returns {Object} 检测结果
   */
  detectKeywords(text) {
    if (!text || typeof text !== "string") {
      return {
        level: "low",
        score: 0,
        keywords: [],
        categories: [],
        hasRisk: false,
      };
    }

    const normalizedText = this.normalizeText(text);
    const detectedKeywords = [];
    const categories = [];
    let totalScore = 0;

    // 检测各类关键词
    for (const [category, keywords] of Object.entries(
      CrisisKeywordDetector.CRISIS_KEYWORDS
    )) {
      const foundInCategory = [];
      let categoryScore = 0;

      for (const keyword of keywords) {
        const matches = this.findMatches(normalizedText, keyword);
        if (matches.length > 0) {
          foundInCategory.push(...matches);
          categoryScore +=
            matches.length * this.getKeywordWeight(keyword, category);
        }
      }

      if (foundInCategory.length > 0) {
        detectedKeywords.push(...foundInCategory);
        categories.push(category);
        totalScore += categoryScore;
      }
    }

    // 计算风险等级
    const riskAssessment = this.calculateRiskLevel(totalScore, categories);

    return {
      level: riskAssessment.level,
      score: totalScore,
      keywords: [...new Set(detectedKeywords)],
      categories: [...new Set(categories)],
      hasRisk: riskAssessment.level !== "low",
    };
  }

  /**
   * 文本标准化处理
   */
  normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9]/g, "") // 只保留中文、英文和数字
      .replace(/\s+/g, ""); // 移除空格
  }

  /**
   * 查找匹配项（包括模糊匹配）
   */
  findMatches(normalizedText, keyword) {
    const matches = [];

    // 精确匹配
    if (normalizedText.includes(keyword)) {
      matches.push(keyword);
    }

    // 检查变形映射
    if (CrisisKeywordDetector.VARIANT_MAP[keyword]) {
      for (const variant of CrisisKeywordDetector.VARIANT_MAP[keyword]) {
        const normalizedVariant = this.normalizeText(variant);
        if (normalizedText.includes(normalizedVariant)) {
          matches.push(variant);
        }
      }
    }

    // 同音字替换检查
    for (const [char, variants] of Object.entries(
      CrisisKeywordDetector.HOMOPHONE_MAP
    )) {
      if (keyword.includes(char)) {
        for (const variant of variants) {
          const substituted = keyword.replace(char, variant);
          const normalizedSubstituted = this.normalizeText(substituted);
          if (normalizedText.includes(normalizedSubstituted)) {
            matches.push(substituted);
          }
        }
      }
    }

    // 模糊匹配（编辑距离）
    const fuzzyMatches = this.fuzzyMatch(normalizedText, keyword);
    matches.push(...fuzzyMatches);

    // 扩展关键词匹配
    for (const expandedKeyword of this.expandedKeywords) {
      if (
        expandedKeyword !== keyword &&
        normalizedText.includes(expandedKeyword)
      ) {
        matches.push(expandedKeyword);
      }
    }

    return [...new Set(matches)]; // 去重
  }

  /**
   * 模糊匹配算法
   */
  fuzzyMatch(text, keyword) {
    const matches = [];
    const threshold = 0.7; // 相似度阈值

    // 简单的编辑距离相似度检查
    for (let i = 0; i <= text.length - keyword.length; i++) {
      const substr = text.substr(i, keyword.length);
      const similarity = this.calculateSimilarity(substr, keyword);

      if (similarity >= threshold) {
        matches.push(substr);
      }
    }

    return matches;
  }

  /**
   * 计算字符串相似度（简化版Levenshtein距离）
   */
  calculateSimilarity(str1, str2) {
    const len1 = str1.length;
    const len2 = str2.length;

    if (len1 === 0) return len2 === 0 ? 1 : 0;
    if (len2 === 0) return 0;

    let matches = 0;
    for (let i = 0; i < Math.min(len1, len2); i++) {
      if (str1[i] === str2[i]) matches++;
    }

    return matches / Math.max(len1, len2);
  }

  /**
   * 获取关键词权重
   */
  getKeywordWeight(keyword, category) {
    const weights = {
      自伤: 10,
      绝望: 8,
      极端情绪: 6,
      无价值感: 5,
      孤独: 4,
    };

    return weights[category] || 3;
  }

  /**
   * 计算风险等级
   */
  calculateRiskLevel(score, categories) {
    // 自伤类关键词直接判定为极高风险
    if (categories.includes("自伤")) {
      return { level: "critical", threshold: "self_harm_detected" };
    }

    // 基于分数和类别数量判定风险等级（调整阈值）
    if (score >= 40 || categories.length >= 4) {
      return { level: "critical", threshold: "high_score_multi_category" };
    } else if (score >= 25 || categories.length >= 3) {
      return { level: "high", threshold: "medium_score_multi_category" };
    } else if (score >= 12 || categories.length >= 2) {
      return { level: "medium", threshold: "low_score_multi_category" };
    } else if (score > 0) {
      return { level: "low", threshold: "minimal_risk" };
    }

    return { level: "low", threshold: "no_risk" };
  }

  /**
   * 快速检测文本中的危机关键词（向后兼容）
   * @param {string} text - 要检测的文本
   * @returns {Object} 检测结果
   */
  static quickDetect(text) {
    const detector = new CrisisKeywordDetector();
    const result = detector.detectKeywords(text);

    return {
      hasCrisis: result.hasRisk,
      riskLevel: result.level,
      detectedKeywords: result.keywords,
      categories: result.categories,
    };
  }

  /**
   * 获取风险等级对应的建议
   * @param {string} riskLevel - 风险等级
   * @param {Array} categories - 检测到的关键词类别
   * @returns {Array} 建议列表
   */
  static getRecommendations(riskLevel, categories = []) {
    const recommendations = [];

    // 基于风险等级的通用建议
    switch (riskLevel) {
      case "critical":
        recommendations.push(
          "请立即寻求专业心理危机干预帮助",
          "联系心理健康热线：400-161-9995",
          "如有紧急情况请拨打110或120"
        );
        break;
      case "high":
        recommendations.push(
          "建议预约专业心理咨询师",
          "与信任的亲友保持联系",
          "考虑寻求心理健康专业支持"
        );
        break;
      case "medium":
        recommendations.push(
          "注意调节情绪，保持规律作息",
          "尝试进行一些愉快的活动",
          "可以考虑与心理咨询师交流"
        );
        break;
      default:
        recommendations.push(
          "保持积极的生活态度",
          "如有困扰可寻求朋友或专业人士的帮助"
        );
        break;
    }

    // 基于具体类别的针对性建议
    categories.forEach((category) => {
      switch (category) {
        case "孤独":
          recommendations.push("主动与朋友家人联系，参加社交活动");
          break;
        case "无价值感":
          recommendations.push("记录每日的小成就，培养自我关爱的习惯");
          break;
        case "极端情绪":
          recommendations.push("学习情绪调节技巧，如深呼吸、冥想等");
          break;
      }
    });

    return [...new Set(recommendations)]; // 去重
  }
}

/**
 * 心理危机预警工具类（增强版）
 */
export class CrisisUtils {
  /**
   * 获取风险等级配置（增强版）
   * @param {string} level - 风险等级
   * @returns {Object} 配置信息
   */
  static getWarningConfig(level) {
    const configs = {
      low: {
        title: "轻微情绪波动",
        message: "检测到您可能有一些情绪困扰。建议适当调节，保持积极心态。",
        hint: "注意情绪变化，必要时寻求帮助",
        color: "#52c41a",
        icon: "💙",
        priority: 1,
        actions: ["放松技巧", "情绪日记"],
        recommendations: [
          "尝试深呼吸或冥想",
          "与朋友聊天分享感受",
          "进行适度运动",
        ],
      },
      medium: {
        title: "情绪需要关注",
        message: "检测到您的情绪状态需要关注。建议主动寻求支持和帮助。",
        hint: "建议寻求朋友或专业人士帮助",
        color: "#faad14",
        icon: "⚠️",
        priority: 2,
        actions: ["情绪调节", "寻求支持"],
        recommendations: [
          "与信任的人分享您的感受",
          "考虑寻找专业心理咨询",
          "保持规律作息和健康饮食",
        ],
      },
      high: {
        title: "需要立即关注",
        message: "您的情绪状态令人担忧，强烈建议立即寻求专业心理健康支持。",
        hint: "强烈建议立即寻求专业帮助",
        color: "#ff7875",
        icon: "🚨",
        priority: 3,
        actions: ["专业咨询", "紧急支持"],
        recommendations: [
          "立即联系心理健康专业人士",
          "告诉信任的朋友或家人您的状况",
          "避免独处，寻求陪伴",
        ],
      },
      critical: {
        title: "紧急危机状态",
        message:
          "检测到严重的心理危机信号！请立即寻求紧急心理危机干预帮助。您的生命很珍贵！",
        hint: "立即寻求紧急帮助！",
        color: "#f5222d",
        icon: "🆘",
        priority: 4,
        actions: ["紧急求助", "危机干预"],
        recommendations: [
          "立即拨打心理危机热线",
          "联系紧急医疗服务",
          "通知最亲近的人陪伴您",
        ],
      },
    };

    return configs[level] || configs["low"];
  }

  /**
   * 获取紧急联系方式
   * @returns {Array} 紧急联系信息
   */
  static getEmergencyContacts() {
    return [
      "🆘 全国心理援助热线：400-161-9995",
      "💙 北京危机干预热线：400-161-9995",
      "🚨 紧急救援：110",
      "🏥 医疗急救：120",
      "💚 上海心理援助热线：021-34289888",
      "💛 广州心理危机干预热线：020-81899120",
    ];
  }

  /**
   * 智能预警提示（基于AI分析结果）
   * @param {Object} analysisResult - AI分析结果
   * @param {Object} keywordResult - 关键词检测结果
   */
  static showIntelligentWarning(analysisResult, keywordResult) {
    const config = this.getWarningConfig(analysisResult.risk_level);

    let warningMessage = config.message;

    // 基于AI分析添加个性化建议
    if (analysisResult.ai_analysis) {
      warningMessage += `\n\nAI分析：${analysisResult.ai_analysis}`;
    }

    // 添加检测到的关键词信息
    if (keywordResult && keywordResult.keywords.length > 0) {
      const keywordText = keywordResult.keywords.slice(0, 3).join("、");
      warningMessage += `\n\n检测关键词：${keywordText}`;
    }

    // 根据风险等级选择不同的提示方式
    if (analysisResult.risk_level === "critical") {
      this.showCriticalAlert(warningMessage, config);
    } else if (analysisResult.risk_level === "high") {
      this.showHighRiskModal(warningMessage, config);
    } else {
      this.showStandardWarning(warningMessage, config);
    }
  }

  /**
   * 显示极危险警报
   */
  static showCriticalAlert(message, config) {
    uni.showModal({
      title: `${config.icon} ${config.title}`,
      content: message,
      showCancel: false,
      confirmText: "立即求助",
      confirmColor: config.color,
      success: () => {
        this.showEmergencyActionSheet();
      },
    });
  }

  /**
   * 显示高风险模态框
   */
  static showHighRiskModal(message, config) {
    uni.showModal({
      title: `${config.icon} ${config.title}`,
      content: message,
      cancelText: "稍后处理",
      confirmText: "寻求帮助",
      confirmColor: config.color,
      success: (res) => {
        if (res.confirm) {
          this.showHelpOptions();
        }
      },
    });
  }

  /**
   * 显示标准警告
   */
  static showStandardWarning(message, config) {
    uni.showModal({
      title: `${config.icon} ${config.title}`,
      content: message,
      cancelText: "我知道了",
      confirmText: "了解更多",
      success: (res) => {
        if (res.confirm) {
          this.showSelfHelpResources();
        }
      },
    });
  }

  /**
   * 显示紧急行动选项
   */
  static showEmergencyActionSheet() {
    uni.showActionSheet({
      title: "🆘 紧急求助选项",
      itemList: [
        "📞 心理危机热线 400-161-9995",
        "🚨 紧急救援 110",
        "🏥 医疗急救 120",
        "💙 在线心理咨询",
        "📱 联系紧急联系人",
      ],
      success: (res) => {
        switch (res.tapIndex) {
          case 0:
            uni.makePhoneCall({ phoneNumber: "400-161-9995" });
            break;
          case 1:
            uni.makePhoneCall({ phoneNumber: "110" });
            break;
          case 2:
            uni.makePhoneCall({ phoneNumber: "120" });
            break;
          case 3:
            // 跳转到在线咨询
            this.navigateToOnlineConsultation();
            break;
          case 4:
            // 显示紧急联系人选择
            this.showEmergencyContacts();
            break;
        }
      },
    });
  }

  /**
   * 显示帮助选项
   */
  static showHelpOptions() {
    uni.showActionSheet({
      title: "💙 获取帮助",
      itemList: [
        "📞 心理援助热线",
        "💬 在线心理咨询",
        "🏥 查找附近心理科",
        "📚 自助资源",
        "👥 支持群组",
      ],
      success: (res) => {
        switch (res.tapIndex) {
          case 0:
            this.showPsychologicalHotlines();
            break;
          case 1:
            this.navigateToOnlineConsultation();
            break;
          case 2:
            this.findNearbyMentalHealthServices();
            break;
          case 3:
            this.showSelfHelpResources();
            break;
          case 4:
            this.navigateToSupportGroups();
            break;
        }
      },
    });
  }

  /**
   * 显示自助资源
   */
  static showSelfHelpResources() {
    const resources = [
      "🧘 正念冥想练习",
      "💪 情绪调节技巧",
      "📝 情绪日记",
      "🎵 舒缓音乐",
      "📖 心理健康文章",
    ];

    uni.showActionSheet({
      title: "📚 自助资源",
      itemList: resources,
      success: (res) => {
        // 根据选择导航到相应资源页面
        this.navigateToResource(res.tapIndex);
      },
    });
  }

  /**
   * 显示心理热线列表
   */
  static showPsychologicalHotlines() {
    const hotlines = [
      "全国心理援助热线 400-161-9995",
      "北京危机干预热线 400-161-9995",
      "上海心理援助热线 021-34289888",
      "广州心理危机干预热线 020-81899120",
    ];

    uni.showActionSheet({
      title: "📞 心理援助热线",
      itemList: hotlines,
      success: (res) => {
        const phoneNumbers = [
          "400-161-9995",
          "400-161-9995",
          "021-34289888",
          "020-81899120",
        ];
        uni.makePhoneCall({ phoneNumber: phoneNumbers[res.tapIndex] });
      },
    });
  }

  /**
   * 导航到在线咨询
   */
  static navigateToOnlineConsultation() {
    // 这里可以跳转到在线咨询页面或外部咨询平台
    uni.showToast({
      title: "正在为您连接在线咨询服务...",
      icon: "loading",
      duration: 2000,
    });
  }

  /**
   * 查找附近心理健康服务
   */
  static findNearbyMentalHealthServices() {
    uni.getLocation({
      type: "gcj02",
      success: (res) => {
        // 使用位置信息查找附近的心理健康服务
        uni.showToast({
          title: "正在查找附近的心理健康服务...",
          icon: "loading",
        });
      },
    });
  }

  /**
   * 导航到支持群组
   */
  static navigateToSupportGroups() {
    uni.navigateTo({
      url: "/pages/support/groups",
    });
  }

  /**
   * 导航到自助资源
   */
  static navigateToResource(index) {
    const resourcePages = [
      "/pages/resources/meditation",
      "/pages/resources/emotion-regulation",
      "/pages/resources/mood-diary",
      "/pages/resources/music",
      "/pages/resources/articles",
    ];

    if (resourcePages[index]) {
      uni.navigateTo({
        url: resourcePages[index],
      });
    }
  }

  /**
   * 风险等级颜色映射
   */
  static getRiskColor(level) {
    const colors = {
      low: "#52c41a",
      medium: "#faad14",
      high: "#ff7875",
      critical: "#f5222d",
    };
    return colors[level] || colors["low"];
  }

  /**
   * 格式化风险分数
   */
  static formatRiskScore(score) {
    if (score >= 80) return "极高风险";
    if (score >= 60) return "高风险";
    if (score >= 40) return "中等风险";
    if (score >= 20) return "轻微风险";
    return "安全";
  }

  /**
   * 生成风险报告
   */
  static generateRiskReport(assessmentResult) {
    const config = this.getWarningConfig(assessmentResult.risk_level);

    return {
      summary: `当前风险等级：${config.title}`,
      score: this.formatRiskScore(assessmentResult.risk_score),
      recommendations: config.recommendations,
      emergency_contacts: this.getEmergencyContacts(),
      timestamp: new Date().toLocaleString(),
    };
  }
}

export default {
  CrisisAPI,
  CrisisKeywordDetector,
  CrisisUtils,
};
