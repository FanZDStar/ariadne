/**
 * 危机关键词检测器
 * 用于检测用户输入中的心理危机相关关键词
 */

export class CrisisKeywordDetector {
  constructor() {
    // 危机关键词配置
    this.crisisKeywords = {
      critical: [
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
        "跳楼",
        "上吊",
        "割腕",
        "服毒",
        "永远离开",
        "再也不回来",
      ],
      high: [
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
        "抑郁",
        "崩溃",
        "痛苦不堪",
        "撑不下去",
        "受不了",
        "人生无意义",
        "厌世",
        "孤独无助",
        "心理创伤",
        "精神折磨",
      ],
      medium: [
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
        "焦虑",
        "压力大",
        "失眠",
        "噩梦",
        "恐慌",
        "害怕",
        "担心",
        "紧张",
        "不安",
        "烦躁",
        "情绪低落",
      ],
      low: [
        "痛苦",
        "煎熬",
        "折磨",
        "要疯",
        "要死",
        "快死了",
        "死掉算了",
        "疲惫",
        "累",
        "困扰",
        "烦恼",
        "不开心",
        "郁闷",
        "无聊",
        "迷茫",
        "困惑",
        "纠结",
        "犹豫",
        "心烦",
        "闷闷不乐",
        "提不起精神",
        "心情不好",
        "沮丧",
        "难过",
      ],
    };

    // API基础地址
    this.baseUrl = process.env.VUE_APP_API_BASE_URL || "http://localhost:8000";
  }

  /**
   * 检测文本中的危机关键词
   * @param {string} text 要检测的文本
   * @returns {Promise<Object>} 检测结果
   */
  async detectCrisis(text) {
    if (!text || typeof text !== "string") {
      return {
        isRisk: false,
        riskLevel: "low",
        detectedKeywords: [],
        confidence: 0,
      };
    }

    // 本地关键词检测
    const localResult = this.detectKeywordsLocally(text);

    // 暂时只使用本地检测，避免调用不存在的后端API
    console.log("🔍 危机检测结果 (仅本地):", localResult);
    return localResult;

    // TODO: 当后端API可用时启用以下代码
    /*
        // 如果本地检测到高风险，还要调用后端AI分析
        if (localResult.riskLevel === 'critical' || localResult.riskLevel === 'high') {
            try {
                const aiResult = await this.callBackendCrisisDetection(text);
                // 结合本地和AI检测结果
                return this.combineDetectionResults(localResult, aiResult);
            } catch (error) {
                console.warn('后端危机检测调用失败，使用本地结果:', error);
                return localResult;
            }
        }

        return localResult;
        */
  }

  /**
   * 本地关键词检测
   * @param {string} text 要检测的文本
   * @returns {Object} 检测结果
   */
  detectKeywordsLocally(text) {
    const normalizedText = text.toLowerCase().trim();
    let detectedKeywords = [];
    let maxRiskLevel = "low";
    let confidence = 0;

    // 检测各级别关键词
    for (const [level, keywords] of Object.entries(this.crisisKeywords)) {
      for (const keyword of keywords) {
        if (normalizedText.includes(keyword.toLowerCase())) {
          detectedKeywords.push(keyword);

          // 更新风险等级（取最高级别）
          if (
            this.getRiskLevelPriority(level) >
            this.getRiskLevelPriority(maxRiskLevel)
          ) {
            maxRiskLevel = level;
          }
        }
      }
    }

    // 计算置信度
    confidence = this.calculateConfidence(detectedKeywords, maxRiskLevel);

    return {
      isRisk: detectedKeywords.length > 0,
      riskLevel: maxRiskLevel,
      detectedKeywords: [...new Set(detectedKeywords)], // 去重
      confidence: confidence,
      method: "local",
    };
  }

  /**
   * 调用后端危机检测API
   * @param {string} text 要检测的文本
   * @returns {Promise<Object>} AI检测结果
   */
  async callBackendCrisisDetection(text) {
    try {
      const response = await uni.request({
        url: `${this.baseUrl}/crisis/analyze`,
        method: "POST",
        header: {
          Authorization: `Bearer ${uni.getStorageSync("access_token")}`,
          "Content-Type": "application/json",
        },
        data: {
          content: text,
          scene: "self-dialog",
          enable_ai_analysis: true,
        },
      });

      if (response.statusCode === 200) {
        const data = response.data;
        return {
          isRisk: data.risk_level !== "LOW",
          riskLevel: this.convertBackendRiskLevel(data.risk_level),
          detectedKeywords: data.detected_keywords || [],
          confidence: data.confidence || 0,
          aiAnalysis: data.ai_analysis,
          method: "ai",
        };
      }
    } catch (error) {
      console.error("后端危机检测调用失败:", error);
      throw error;
    }

    return null;
  }

  /**
   * 结合本地和AI检测结果
   * @param {Object} localResult 本地检测结果
   * @param {Object} aiResult AI检测结果
   * @returns {Object} 综合结果
   */
  combineDetectionResults(localResult, aiResult) {
    if (!aiResult) return localResult;

    // 取风险等级较高的结果
    const combinedRiskLevel =
      this.getRiskLevelPriority(localResult.riskLevel) >
      this.getRiskLevelPriority(aiResult.riskLevel)
        ? localResult.riskLevel
        : aiResult.riskLevel;

    // 合并检测到的关键词
    const combinedKeywords = [
      ...localResult.detectedKeywords,
      ...aiResult.detectedKeywords,
    ];

    return {
      isRisk: localResult.isRisk || aiResult.isRisk,
      riskLevel: combinedRiskLevel,
      detectedKeywords: [...new Set(combinedKeywords)],
      confidence: Math.max(localResult.confidence, aiResult.confidence),
      aiAnalysis: aiResult.aiAnalysis,
      method: "combined",
    };
  }

  /**
   * 获取风险等级优先级（数值越大风险越高）
   * @param {string} level 风险等级
   * @returns {number} 优先级数值
   */
  getRiskLevelPriority(level) {
    const priorities = {
      low: 1,
      medium: 2,
      high: 3,
      critical: 4,
    };
    return priorities[level] || 0;
  }

  /**
   * 计算置信度
   * @param {Array} keywords 检测到的关键词
   * @param {string} riskLevel 风险等级
   * @returns {number} 置信度(0-1)
   */
  calculateConfidence(keywords, riskLevel) {
    if (keywords.length === 0) return 0;

    const baseConfidence = {
      critical: 0.9,
      high: 0.7,
      medium: 0.5,
      low: 0.3,
    };

    const keywordBonus = Math.min(keywords.length * 0.1, 0.3);
    return Math.min(baseConfidence[riskLevel] + keywordBonus, 1.0);
  }

  /**
   * 转换后端风险等级到前端格式
   * @param {string} backendLevel 后端风险等级
   * @returns {string} 前端风险等级
   */
  convertBackendRiskLevel(backendLevel) {
    const mapping = {
      LOW: "low",
      MEDIUM: "medium",
      HIGH: "high",
      CRITICAL: "critical",
    };
    return mapping[backendLevel] || "low";
  }

  /**
   * 添加自定义关键词
   * @param {string} level 风险等级
   * @param {Array} keywords 关键词数组
   */
  addCustomKeywords(level, keywords) {
    if (this.crisisKeywords[level]) {
      this.crisisKeywords[level].push(...keywords);
    }
  }

  /**
   * 获取所有关键词统计
   * @returns {Object} 关键词统计信息
   */
  getKeywordStats() {
    const stats = {};
    for (const [level, keywords] of Object.entries(this.crisisKeywords)) {
      stats[level] = keywords.length;
    }
    return stats;
  }
}
