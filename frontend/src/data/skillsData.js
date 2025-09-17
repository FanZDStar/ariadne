// 统一的技能数据映射文件
// 确保 category-detail.vue 和 skill-detail.vue 使用相同的数据源

export const skillsData = {
    // 沟通表达类技能 (1-25)
    1: {
        id: 1,
        name: "主动倾听",
        brief: "学会用心倾听对方的话语和情感",
        description: "主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。",
        estimatedTime: 15,
        learnerCount: 1234,
        tags: ["倾听", "沟通基础", "理解"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "学会集中注意力倾听对方说话",
            "理解言语背后的情感和需求",
            "通过肢体语言展现倾听态度",
            "运用复述和确认技巧验证理解"
        ],
        keyPoints: [
            {
                icon: "👀",
                title: "眼神交流",
                content: "保持适当的眼神交流，表达对对方的关注和尊重",
                example: "看着对方的眼睛，偶尔点头表示理解"
            },
            {
                icon: "🤐",
                title: "避免打断",
                content: "让对方完整表达想法，不要急于插话或给建议",
                example: '等对方说完后再回应："我理解你的意思是..."'
            },
            {
                icon: "🔄",
                title: "反馈确认",
                content: "用自己的话复述对方的观点，确认理解正确",
                example: '"如果我理解正确，你是想说..."'
            }
        ],
        practiceScenarios: [
            {
                title: "朋友倾诉",
                description: "朋友向你分享工作中的困扰"
            },
            {
                title: "家庭对话",
                description: "与家人讨论重要决定"
            }
        ]
    },

    2: {
        id: 2,
        name: "情感表达",
        brief: "准确表达自己的情感和需求",
        description: "学会用'我'的句式表达情感，避免指责和批评。",
        estimatedTime: 20,
        learnerCount: 956,
        tags: ["情感", "表达"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "学会识别和命名自己的情感",
            "掌握'我'语句的表达技巧",
            "在不同情境下恰当表达需求",
            "避免指责性语言"
        ],
        keyPoints: [
            {
                icon: "❤️",
                title: "情感识别",
                content: "准确识别当下的情感状态",
                example: "我现在感到失望和困惑"
            },
            {
                icon: "🗣️",
                title: "我语句",
                content: "用'我'开头表达感受，避免'你'指责",
                example: "我感到被忽视了，而不是'你总是不理我'"
            }
        ],
        practiceScenarios: [
            {
                title: "职场反馈",
                description: "向同事表达对工作安排的不满"
            },
            {
                title: "恋爱沟通",
                description: "与伴侣分享内心的不安全感"
            }
        ]
    },

    3: {
        id: 3,
        name: "非暴力沟通",
        brief: "以善意和理解进行沟通",
        description: "学习非暴力沟通的四个步骤：观察、感受、需要、请求。",
        estimatedTime: 30,
        learnerCount: 567,
        tags: ["沟通技巧", "冲突处理"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握非暴力沟通的四个步骤",
            "学会客观观察而非评判",
            "准确表达感受和需要",
            "提出具体可行的请求"
        ],
        keyPoints: [
            {
                icon: "👁️",
                title: "客观观察",
                content: "描述事实而非评判",
                example: "你昨天没有回我的消息（观察）vs 你不关心我（评判）"
            },
            {
                icon: "💭",
                title: "表达感受",
                content: "分享内心的真实感受",
                example: "我感到担心和焦虑"
            },
            {
                icon: "🎯",
                title: "明确需要",
                content: "识别感受背后的需要",
                example: "我需要感到被重视和关心"
            },
            {
                icon: "🙏",
                title: "具体请求",
                content: "提出明确可行的行动请求",
                example: "你能在今晚7点前回复我的消息吗？"
            }
        ],
        practiceScenarios: [
            {
                title: "工作冲突",
                description: "与同事因为工作分配产生分歧"
            },
            {
                title: "家庭矛盾",
                description: "与家人因为生活习惯发生争执"
            }
        ]
    },

    4: {
        id: 4,
        name: "情绪识别",
        brief: "准确识别自己和他人的情绪状态",
        description: "发展情绪觉察能力，学会识别情绪的细微差别和变化。",
        estimatedTime: 25,
        learnerCount: 789,
        tags: ["情绪", "觉察", "识别"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "扩展情绪词汇库",
            "识别情绪的身体信号",
            "觉察情绪的变化过程",
            "理解情绪背后的需求"
        ],
        keyPoints: [
            {
                icon: "🌡️",
                title: "情绪温度",
                content: "感受情绪的强度变化",
                example: "从轻微不安到强烈焦虑的过程"
            },
            {
                icon: "🎭",
                title: "情绪层次",
                content: "识别表面情绪下的深层感受",
                example: "愤怒背后可能是受伤或恐惧"
            }
        ],
        practiceScenarios: [
            {
                title: "压力时刻",
                description: "在高压工作环境中觉察自己的情绪"
            }
        ]
    },

    5: {
        id: 5,
        name: "情感共鸣",
        brief: "与他人产生情感共鸣和理解",
        description: "培养同理心，学会感受和理解他人的情感世界。",
        estimatedTime: 28,
        learnerCount: 645,
        tags: ["同理心", "共鸣", "理解"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "发展同理心能力",
            "学会情感反映技巧",
            "创造安全的情感空间",
            "建立深层情感连接"
        ],
        keyPoints: [
            {
                icon: "🤝",
                title: "情感反映",
                content: "反映对方的情感状态",
                example: "听起来你现在很失落"
            }
        ],
        practiceScenarios: [
            {
                title: "朋友失恋",
                description: "安慰刚分手的朋友"
            }
        ]
    },

    6: {
        id: 6,
        name: "情绪调节",
        brief: "学会管理和调节自己的情绪",
        description: "掌握情绪调节技巧，在困难情况下保持情绪平衡。",
        estimatedTime: 35,
        learnerCount: 523,
        tags: ["调节", "管理", "平衡"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "学会情绪调节策略",
            "建立情绪缓冲机制",
            "在压力下保持冷静",
            "转化负面情绪为正面能量"
        ],
        keyPoints: [
            {
                icon: "🧘",
                title: "深呼吸",
                content: "通过呼吸调节情绪状态",
                example: "4-7-8呼吸法：吸气4秒，屏气7秒，呼气8秒"
            }
        ],
        practiceScenarios: [
            {
                title: "考试焦虑",
                description: "考试前的紧张情绪调节"
            }
        ]
    },

    7: {
        id: 7,
        name: "破冰技巧",
        brief: "在新环境中快速与他人建立联系",
        description: "掌握破冰对话技巧，轻松开启人际交往。",
        estimatedTime: 20,
        learnerCount: 678,
        tags: ["破冰", "初次见面", "社交"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握开场白技巧",
            "学会寻找共同话题",
            "克服初次交往的紧张",
            "建立良好的第一印象"
        ],
        keyPoints: [
            {
                icon: "😊",
                title: "热情开场",
                content: "用积极的态度开始对话",
                example: "你好！这个活动很有趣呢"
            }
        ],
        practiceScenarios: [
            {
                title: "聚会社交",
                description: "在朋友聚会上认识新朋友"
            }
        ]
    },

    8: {
        id: 8,
        name: "信任建立",
        brief: "在关系中建立互相信任的基础",
        description: "通过一致的言行和真诚的态度建立他人的信任。",
        estimatedTime: 35,
        learnerCount: 456,
        tags: ["信任", "真诚", "关系"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "展现真实的自己",
            "保持言行一致",
            "尊重他人的隐私",
            "逐步加深关系"
        ],
        keyPoints: [
            {
                icon: "🤝",
                title: "言行一致",
                content: "说到做到，建立可信度",
                example: "承诺了就要兑现"
            }
        ],
        practiceScenarios: [
            {
                title: "新同事关系",
                description: "与新同事建立工作信任"
            }
        ]
    },

    9: {
        id: 9,
        name: "冲突解决",
        brief: "有效处理人际冲突和分歧",
        description: "学会在冲突中寻找双赢的解决方案。",
        estimatedTime: 40,
        learnerCount: 334,
        tags: ["冲突", "调解", "解决"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "理解冲突的根源",
            "学会冷静应对争执",
            "寻找共同利益点",
            "达成互利解决方案"
        ],
        keyPoints: [
            {
                icon: "⚖️",
                title: "公平调解",
                content: "站在中立立场寻找平衡",
                example: "让双方都能接受的方案"
            }
        ],
        practiceScenarios: [
            {
                title: "团队争议",
                description: "解决团队内部的意见分歧"
            }
        ]
    },

    10: {
        id: 10,
        name: "职场沟通",
        brief: "在工作环境中进行专业有效的沟通",
        description: "掌握职场沟通的专业技巧和礼仪。",
        estimatedTime: 30,
        learnerCount: 1234,
        tags: ["职场", "专业", "沟通"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握正式沟通技巧",
            "学会汇报工作进展",
            "处理职场人际关系",
            "提升职业形象"
        ],
        keyPoints: [
            {
                icon: "💼",
                title: "专业表达",
                content: "使用恰当的职场语言",
                example: "条理清晰地汇报工作"
            }
        ],
        practiceScenarios: [
            {
                title: "工作汇报",
                description: "向领导汇报项目进展"
            }
        ]
    },

    11: {
        id: 11,
        name: "异地恋维护",
        brief: "维护远距离恋爱关系的技巧",
        description: "学会在距离中保持情感连接和关系温度。",
        estimatedTime: 35,
        learnerCount: 456,
        tags: ["异地恋", "维护", "距离"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "保持定期沟通",
            "创造共同体验",
            "处理思念情绪",
            "规划未来见面"
        ],
        keyPoints: [
            {
                icon: "📱",
                title: "定期联系",
                content: "建立固定的沟通时间",
                example: "每天晚上的视频通话"
            }
        ],
        practiceScenarios: [
            {
                title: "情侣沟通",
                description: "与异地伴侣的日常联系"
            }
        ]
    },

    12: {
        id: 12,
        name: "危机干预",
        brief: "在紧急情况下提供心理支持",
        description: "学会在他人面临心理危机时给予适当的支持。",
        estimatedTime: 50,
        learnerCount: 234,
        tags: ["危机", "干预", "支持"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "识别危机信号",
            "提供即时支持",
            "寻求专业帮助",
            "陪伴度过难关"
        ],
        keyPoints: [
            {
                icon: "🆘",
                title: "及时响应",
                content: "快速识别并回应危机",
                example: "我在这里陪着你"
            }
        ],
        practiceScenarios: [
            {
                title: "朋友危机",
                description: "帮助情绪崩溃的朋友"
            }
        ]
    },

    13: {
        id: 13,
        name: "清晰表达",
        brief: "用简洁明了的语言传达想法",
        description: "掌握逻辑清晰、条理分明的表达技巧，让听众易于理解。",
        estimatedTime: 18,
        learnerCount: 892,
        tags: ["表达", "逻辑"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "组织清晰的表达结构",
            "使用简洁的语言",
            "突出重点信息",
            "确认听众理解"
        ],
        keyPoints: [
            {
                icon: "📋",
                title: "结构化表达",
                content: "按照逻辑顺序组织语言",
                example: "首先...其次...最后..."
            }
        ],
        practiceScenarios: [
            {
                title: "会议发言",
                description: "在会议上清晰表达观点"
            }
        ]
    },

    14: {
        id: 14,
        name: "提问技巧",
        brief: "学会问出有价值的问题",
        description: "掌握不同类型的提问技巧，引导有效的对话。",
        estimatedTime: 18,
        learnerCount: 567,
        tags: ["提问", "技巧", "对话"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握开放式提问",
            "学会引导性问题",
            "使用澄清问题",
            "避免诱导性提问"
        ],
        keyPoints: [
            {
                icon: "❓",
                title: "开放式提问",
                content: "用开放式问题获取更多信息",
                example: "你对这件事有什么想法？"
            }
        ],
        practiceScenarios: [
            {
                title: "深度交流",
                description: "与朋友进行深入对话"
            }
        ]
    },

    15: {
        id: 15,
        name: "肢体语言",
        brief: "运用身体语言增强沟通效果",
        description: "学会读懂和运用肢体语言，提升沟通的说服力。",
        estimatedTime: 25,
        learnerCount: 489,
        tags: ["肢体语言", "非言语", "沟通"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "理解身体语言含义",
            "控制自己的肢体表达",
            "观察他人的非言语信号",
            "协调言语和肢体语言"
        ],
        keyPoints: [
            {
                icon: "🤲",
                title: "手势配合",
                content: "用手势强化语言表达",
                example: "开放的手掌表示诚意"
            }
        ],
        practiceScenarios: [
            {
                title: "面试表现",
                description: "在面试中展现自信的肢体语言"
            }
        ]
    },

    // 添加更多技能...
    16: {
        id: 16,
        name: "故事叙述",
        brief: "用故事让沟通更有感染力",
        description: "学会通过故事传达观点，增强表达的感染力。",
        estimatedTime: 25,
        learnerCount: 345,
        tags: ["故事", "叙述", "感染力"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握故事结构",
            "选择合适的故事",
            "生动地讲述故事",
            "通过故事传达观点"
        ],
        keyPoints: [
            {
                icon: "📖",
                title: "故事结构",
                content: "起承转合的叙述结构",
                example: "开头吸引注意，结尾点明主题"
            }
        ],
        practiceScenarios: [
            {
                title: "说服他人",
                description: "用故事说服朋友接受建议"
            }
        ]
    },

    17: {
        id: 17,
        name: "公众演讲",
        brief: "在公众场合自信地表达观点",
        description: "克服演讲恐惧，掌握公众演讲的基本技巧。",
        estimatedTime: 40,
        learnerCount: 289,
        tags: ["演讲", "公众", "自信"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "克服演讲紧张",
            "组织演讲内容",
            "掌握演讲技巧",
            "与观众互动"
        ],
        keyPoints: [
            {
                icon: "🎤",
                title: "声音控制",
                content: "掌握音量和语调变化",
                example: "重点内容适当提高音量"
            }
        ],
        practiceScenarios: [
            {
                title: "会议发言",
                description: "在大型会议上发言"
            }
        ]
    },

    18: {
        id: 18,
        name: "说服技巧",
        brief: "以理服人的说服艺术",
        description: "掌握逻辑论证、情感共鸣等说服技巧，影响他人观点。",
        estimatedTime: 35,
        learnerCount: 321,
        tags: ["说服", "影响力", "逻辑"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握逻辑论证的基本方法",
            "学会运用情感共鸣技巧",
            "理解说服的心理学原理",
            "培养影响他人观点的能力"
        ],
        keyPoints: [
            {
                icon: "🧠",
                title: "逻辑论证",
                content: "运用事实、数据和逻辑推理支持观点",
                example: "用具体数据说明提案的可行性"
            },
            {
                icon: "❤️",
                title: "情感共鸣",
                content: "理解对方的情感需求并产生共鸣",
                example: "理解对方的担忧并表示认同"
            },
            {
                icon: "🎯",
                title: "关键利益",
                content: "找到对方真正关心的核心利益点",
                example: "发现对方最重视的价值或需求"
            }
        ],
        practiceScenarios: [
            {
                title: "工作提案",
                description: "向上级说明新项目的必要性"
            },
            {
                title: "家庭决策",
                description: "说服家人接受重要决定"
            }
        ]
    },

    19: {
        id: 19,
        name: "会议沟通",
        brief: "在会议中有效表达观点",
        description: "学会在团队会议中清晰表达想法，参与建设性讨论。",
        estimatedTime: 26,
        learnerCount: 467,
        tags: ["会议", "团队", "表达"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握会议发言的时机和技巧",
            "学会简洁有力地表达观点",
            "培养建设性讨论的能力",
            "提升团队协作沟通效率"
        ],
        keyPoints: [
            {
                icon: "⏰",
                title: "把握时机",
                content: "选择合适的时机发言，避免打断他人",
                example: "等待发言空档或举手示意"
            },
            {
                icon: "📝",
                title: "要点明确",
                content: "用简洁的语言表达核心观点",
                example: "我认为应该..., 理由有三点"
            },
            {
                icon: "🤝",
                title: "建设性参与",
                content: "提出解决方案而非仅仅指出问题",
                example: "除了这个问题，我建议我们可以..."
            }
        ],
        practiceScenarios: [
            {
                title: "项目讨论",
                description: "在项目会议中提出改进建议"
            },
            {
                title: "头脑风暴",
                description: "参与创意讨论会议"
            }
        ]
    },

    20: {
        id: 20,
        name: "演讲技巧",
        brief: "公众场合的自信表达",
        description: "克服演讲恐惧，掌握公众演讲的基本技巧和方法。",
        estimatedTime: 40,
        learnerCount: 289,
        tags: ["演讲", "公众", "自信"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "克服公众演讲的恐惧心理",
            "掌握演讲的基本结构和技巧",
            "学会运用肢体语言增强表达力",
            "培养自信的台风和气场"
        ],
        keyPoints: [
            {
                icon: "💪",
                title: "克服恐惧",
                content: "通过充分准备和练习减少紧张感",
                example: "提前熟悉演讲内容和场地环境"
            },
            {
                icon: "📊",
                title: "结构清晰",
                content: "采用开头-主体-结尾的经典结构",
                example: "介绍主题-展开论述-总结要点"
            },
            {
                icon: "🎭",
                title: "肢体表达",
                content: "运用手势、表情、姿态增强表达效果",
                example: "用手势强调重点，保持自信姿态"
            }
        ],
        practiceScenarios: [
            {
                title: "工作汇报",
                description: "向全体员工汇报项目进展"
            },
            {
                title: "学术演讲",
                description: "在学术会议上发表研究成果"
            }
        ]
    },

    21: {
        id: 21,
        name: "电话沟通",
        brief: "通过电话进行有效沟通",
        description: "在缺乏视觉线索的情况下，保持清晰有效的电话沟通。",
        estimatedTime: 15,
        learnerCount: 378,
        tags: ["电话", "远程", "沟通"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握电话沟通的基本礼仪",
            "学会在无视觉线索下有效表达",
            "提升电话中的倾听和理解能力",
            "处理电话沟通中的技术问题"
        ],
        keyPoints: [
            {
                icon: "📞",
                title: "开场礼仪",
                content: "礼貌的开场白和自我介绍",
                example: "您好，我是张三，来自ABC公司"
            },
            {
                icon: "🗣️",
                title: "语音清晰",
                content: "保持语速适中，吐字清晰",
                example: "放慢语速，确保对方能听清每个字"
            },
            {
                icon: "🔄",
                title: "确认理解",
                content: "定期确认对方是否理解内容",
                example: "这个方案您觉得怎么样？"
            }
        ],
        practiceScenarios: [
            {
                title: "客户咨询",
                description: "接听客户的产品咨询电话"
            },
            {
                title: "远程会议",
                description: "参与电话会议讨论"
            }
        ]
    },

    22: {
        id: 22,
        name: "书面表达",
        brief: "通过文字进行有效沟通",
        description: "掌握邮件、报告等书面沟通的技巧，确保信息准确传达。",
        estimatedTime: 30,
        learnerCount: 198,
        tags: ["书面", "文字", "准确"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握不同书面沟通的格式要求",
            "学会组织逻辑清晰的文字内容",
            "提升文字表达的准确性和简洁性",
            "适应不同场合的写作风格"
        ],
        keyPoints: [
            {
                icon: "📋",
                title: "格式规范",
                content: "遵循邮件、报告等的标准格式",
                example: "邮件包含明确主题、称谓、正文、结尾"
            },
            {
                icon: "🎯",
                title: "主题明确",
                content: "开门见山，突出核心信息",
                example: "在开头段落说明写作目的"
            },
            {
                icon: "✂️",
                title: "简洁精准",
                content: "避免冗长句子，用词准确",
                example: "删除不必要的修饰词，直接表达"
            }
        ],
        practiceScenarios: [
            {
                title: "工作邮件",
                description: "给同事或客户发送工作邮件"
            },
            {
                title: "项目报告",
                description: "撰写项目进展报告"
            }
        ]
    },

    23: {
        id: 23,
        name: "跨文化沟通",
        brief: "在多元文化环境中沟通",
        description: "理解文化差异，在跨文化环境中进行敏感而有效的沟通。",
        estimatedTime: 32,
        learnerCount: 156,
        tags: ["跨文化", "多元", "敏感"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "理解不同文化的沟通习惯",
            "学会识别和避免文化偏见",
            "掌握跨文化沟通的基本原则",
            "培养文化敏感性和包容性"
        ],
        keyPoints: [
            {
                icon: "🌍",
                title: "文化意识",
                content: "了解不同文化的价值观和习俗",
                example: "尊重不同的节日传统和礼仪习惯"
            },
            {
                icon: "🤲",
                title: "包容心态",
                content: "以开放包容的心态对待差异",
                example: "避免用自己的文化标准评判他人"
            },
            {
                icon: "🔍",
                title: "细节观察",
                content: "注意非言语沟通的文化差异",
                example: "了解不同文化中手势和眼神的含义"
            }
        ],
        practiceScenarios: [
            {
                title: "国际合作",
                description: "与国外同事协作完成项目"
            },
            {
                title: "多元团队",
                description: "在多文化背景团队中工作"
            }
        ]
    },

    24: {
        id: 24,
        name: "谈判沟通",
        brief: "在谈判中达成双赢",
        description: "掌握谈判技巧，通过有效沟通找到互利共赢的解决方案。",
        estimatedTime: 45,
        learnerCount: 134,
        tags: ["谈判", "双赢", "策略"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "掌握谈判的基本策略和技巧",
            "学会寻找双方的共同利益点",
            "培养在压力下的冷静沟通能力",
            "提升问题解决和妥协的技能"
        ],
        keyPoints: [
            {
                icon: "🎯",
                title: "明确目标",
                content: "清楚自己的底线和期望目标",
                example: "提前设定最低接受条件和理想结果"
            },
            {
                icon: "🤝",
                title: "寻找共赢",
                content: "寻找双方都能接受的解决方案",
                example: "探索能满足双方核心需求的方案"
            },
            {
                icon: "🧘",
                title: "保持冷静",
                content: "在紧张氛围中保持理性和耐心",
                example: "遇到分歧时暂停，冷静分析"
            }
        ],
        practiceScenarios: [
            {
                title: "商务谈判",
                description: "与供应商谈判合作条件"
            },
            {
                title: "薪资谈判",
                description: "与雇主讨论薪资待遇"
            }
        ]
    },

    25: {
        id: 25,
        name: "数字化沟通",
        brief: "在线上平台进行有效沟通",
        description: "适应数字时代，掌握视频会议、即时通讯等在线沟通工具。",
        estimatedTime: 24,
        learnerCount: 267,
        tags: ["数字化", "在线", "工具"],
        category: "communication",
        categoryName: "沟通表达",
        objectives: [
            "熟练使用各种在线沟通工具",
            "掌握视频会议的沟通技巧",
            "学会在线协作和远程沟通",
            "适应数字化工作环境"
        ],
        keyPoints: [
            {
                icon: "💻",
                title: "技术熟练",
                content: "熟练操作视频会议和协作软件",
                example: "掌握屏幕共享、静音等基本功能"
            },
            {
                icon: "📱",
                title: "及时响应",
                content: "在即时通讯中保持适当的回复速度",
                example: "在合理时间内回复重要信息"
            },
            {
                icon: "🎥",
                title: "视频礼仪",
                content: "在视频会议中保持专业形象",
                example: "注意背景整洁，保持良好仪态"
            }
        ],
        practiceScenarios: [
            {
                title: "远程会议",
                description: "主持或参与在线团队会议"
            },
            {
                title: "在线协作",
                description: "使用协作工具完成团队项目"
            }
        ]
    },

    // 继续添加所有其他技能到65...
    // 为了节省篇幅，我会添加关键的几个技能

    26: {
        id: 26,
        name: "情感词汇",
        brief: "扩展情感词汇，精确表达感受",
        description: "建立丰富的情感词汇库，更准确地表达内心感受。",
        estimatedTime: 20,
        learnerCount: 456,
        tags: ["词汇", "表达", "精确"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "学习多样化的情感词汇",
            "区分相似情感的细微差别",
            "在不同情境下使用恰当词汇",
            "帮助他人准确表达情感"
        ],
        keyPoints: [
            {
                icon: "📚",
                title: "词汇丰富",
                content: "用具体词汇替代模糊表达",
                example: "沮丧、失落、绝望比'不开心'更准确"
            }
        ],
        practiceScenarios: [
            {
                title: "情感日记",
                description: "用丰富词汇记录每日情感"
            }
        ]
    },

    27: {
        id: 27,
        name: "同理心训练",
        brief: "增强理解他人情感的能力",
        description: "通过练习增强同理心，更好地理解他人的情感世界。",
        estimatedTime: 30,
        learnerCount: 345,
        tags: ["同理心", "理解", "训练"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "提高情感敏感度",
            "学会换位思考",
            "避免过度共情",
            "保持情感边界"
        ],
        keyPoints: [
            {
                icon: "💝",
                title: "换位思考",
                content: "站在对方角度理解情况",
                example: "如果我是他，我会怎么感受"
            }
        ],
        practiceScenarios: [
            {
                title: "朋友困扰",
                description: "理解朋友的工作压力"
            }
        ]
    },

    28: {
        id: 28,
        name: "情感边界",
        brief: "建立健康的情感边界",
        description: "学会在情感交流中保护自己，避免情感过载和耗竭。",
        estimatedTime: 30,
        learnerCount: 389,
        tags: ["边界", "保护", "健康"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "理解情感边界的重要性",
            "学会识别情感过载的信号",
            "掌握保护自己的方法",
            "维护健康的人际关系"
        ],
        keyPoints: [
            {
                icon: "🛡️",
                title: "自我保护",
                content: "识别并设置个人情感界限",
                example: "明确告知不舒服的话题或行为"
            },
            {
                icon: "⚖️",
                title: "平衡关系",
                content: "在关爱他人和自我保护间找平衡",
                example: "帮助他人时也要保护自己的情感"
            },
            {
                icon: "🚫",
                title: "学会拒绝",
                content: "礼貌但坚定地拒绝过度的情感需求",
                example: "对过度依赖的朋友说不"
            }
        ],
        practiceScenarios: [
            {
                title: "过度依赖",
                description: "应对朋友的过度情感依赖"
            },
            {
                title: "工作边界",
                description: "在工作中保持适当的情感距离"
            }
        ]
    },

    29: {
        id: 29,
        name: "情绪传染",
        brief: "理解和管理情绪的传染性",
        description: "认识情绪如何在人群中传播，学会保持情绪稳定。",
        estimatedTime: 22,
        learnerCount: 312,
        tags: ["情绪传染", "稳定", "管理"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "理解情绪传染的机制",
            "学会识别他人情绪对自己的影响",
            "掌握保持情绪稳定的技巧",
            "帮助营造积极的情绪氛围"
        ],
        keyPoints: [
            {
                icon: "🌊",
                title: "传染机制",
                content: "了解情绪如何在人际间传播",
                example: "观察团队中一个人的坏情绪如何影响全体"
            },
            {
                icon: "🧘",
                title: "情绪隔离",
                content: "学会不被他人的负面情绪影响",
                example: "遇到愤怒的人时保持内心平静"
            },
            {
                icon: "☀️",
                title: "积极影响",
                content: "通过自己的积极情绪影响他人",
                example: "用乐观态度感染周围的人"
            }
        ],
        practiceScenarios: [
            {
                title: "团队氛围",
                description: "在低落的团队中保持积极"
            },
            {
                title: "家庭和谐",
                description: "处理家庭中的负面情绪传染"
            }
        ]
    },

    30: {
        id: 30,
        name: "情感支持",
        brief: "为他人提供有效的情感支持",
        description: "学会在他人需要时给予恰当的情感支持和安慰。",
        estimatedTime: 25,
        learnerCount: 456,
        tags: ["支持", "安慰", "陪伴"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "学会识别他人的情感需求",
            "掌握提供支持的不同方式",
            "了解何时该提供建议何时该倾听",
            "培养同理心和耐心"
        ],
        keyPoints: [
            {
                icon: "👂",
                title: "专注倾听",
                content: "全神贯注地倾听对方的感受",
                example: "放下手机，专心听朋友倾诉"
            },
            {
                icon: "🤗",
                title: "情感确认",
                content: "确认和理解对方的情感体验",
                example: "我能理解你现在一定很难过"
            },
            {
                icon: "💪",
                title: "实际支持",
                content: "在适当时候提供具体的帮助",
                example: "除了倾听，询问是否需要实际帮助"
            }
        ],
        practiceScenarios: [
            {
                title: "朋友失恋",
                description: "安慰刚失恋的朋友"
            },
            {
                title: "同事压力",
                description: "支持工作压力大的同事"
            }
        ]
    },

    31: {
        id: 31,
        name: "创伤敏感",
        brief: "对他人创伤经历保持敏感",
        description: "理解创伤对情感的影响，在交流中保持敏感和谨慎。",
        estimatedTime: 35,
        learnerCount: 234,
        tags: ["创伤", "敏感", "谨慎"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "了解创伤对心理的长期影响",
            "学会识别创伤的隐性信号",
            "掌握与有创伤经历者的沟通技巧",
            "避免二次伤害的言行"
        ],
        keyPoints: [
            {
                icon: "🔍",
                title: "敏感识别",
                content: "留意可能触发创伤回忆的话题",
                example: "注意对方对某些话题的过激反应"
            },
            {
                icon: "🤲",
                title: "温柔对待",
                content: "用温和、理解的态度进行交流",
                example: "避免强迫对方分享痛苦经历"
            },
            {
                icon: "🚪",
                title: "尊重边界",
                content: "尊重对方设置的情感边界",
                example: "当对方不愿谈论时立即停止"
            }
        ],
        practiceScenarios: [
            {
                title: "创伤倾诉",
                description: "倾听有创伤经历的朋友分享"
            },
            {
                title: "敏感话题",
                description: "在涉及敏感话题时保持谨慎"
            }
        ]
    },

    32: {
        id: 32,
        name: "情感复原",
        brief: "从情感创伤中恢复的技能",
        description: "掌握从负面情感经历中恢复和成长的方法。",
        estimatedTime: 40,
        learnerCount: 198,
        tags: ["复原", "成长", "恢复"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "理解情感复原的基本过程",
            "学会处理负面情感的技巧",
            "培养从挫折中成长的能力",
            "建立情感复原的支持系统"
        ],
        keyPoints: [
            {
                icon: "🌱",
                title: "接受现实",
                content: "接受痛苦经历并开始愈合过程",
                example: "承认伤痛，不否认或压抑情感"
            },
            {
                icon: "💪",
                title: "寻求支持",
                content: "主动寻求专业或朋友的帮助",
                example: "向信任的人分享内心感受"
            },
            {
                icon: "🌈",
                title: "重建希望",
                content: "逐步重建对未来的积极期待",
                example: "制定小目标，逐步恢复生活节奏"
            }
        ],
        practiceScenarios: [
            {
                title: "失去亲人",
                description: "从失去重要的人中慢慢恢复"
            },
            {
                title: "重大挫折",
                description: "从事业或学业挫折中重新站起"
            }
        ]
    },

    33: {
        id: 33,
        name: "情感表达艺术",
        brief: "通过艺术形式表达情感",
        description: "学会用绘画、音乐、写作等艺术形式表达和处理情感。",
        estimatedTime: 45,
        learnerCount: 167,
        tags: ["艺术", "创意表达", "治疗"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "探索不同的艺术表达方式",
            "学会通过创作处理情感",
            "理解艺术的治疗作用",
            "培养创意表达的习惯"
        ],
        keyPoints: [
            {
                icon: "🎨",
                title: "视觉表达",
                content: "通过绘画、摄影等视觉艺术表达",
                example: "画出内心的感受和情绪状态"
            },
            {
                icon: "🎵",
                title: "听觉表达",
                content: "通过音乐、歌唱表达情感",
                example: "创作或演奏表达心情的音乐"
            },
            {
                icon: "✍️",
                title: "文字表达",
                content: "通过写作、诗歌表达内心世界",
                example: "写日记或诗歌表达复杂情感"
            }
        ],
        practiceScenarios: [
            {
                title: "情感日记",
                description: "用艺术日记记录每天的情感变化"
            },
            {
                title: "创作治疗",
                description: "通过创作处理难以言喻的情感"
            }
        ]
    },

    34: {
        id: 34,
        name: "情感记忆",
        brief: "管理和处理情感记忆",
        description: "学会处理痛苦的情感记忆，保留积极的情感体验。",
        estimatedTime: 38,
        learnerCount: 145,
        tags: ["记忆", "处理", "管理"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "理解情感记忆的形成机制",
            "学会处理负面情感记忆",
            "培养积极情感记忆的能力",
            "建立健康的记忆管理习惯"
        ],
        keyPoints: [
            {
                icon: "🧠",
                title: "记忆理解",
                content: "了解情感记忆如何影响现在",
                example: "认识过去经历对当前情绪的影响"
            },
            {
                icon: "🔄",
                title: "重新框定",
                content: "从新角度理解过去的经历",
                example: "将挫折看作成长的机会"
            },
            {
                icon: "💎",
                title: "珍藏美好",
                content: "有意识地收集和保存积极记忆",
                example: "记录生活中的美好瞬间"
            }
        ],
        practiceScenarios: [
            {
                title: "童年阴影",
                description: "处理童年时期的负面记忆"
            },
            {
                title: "美好回忆",
                description: "培养收集积极记忆的习惯"
            }
        ]
    },

    35: {
        id: 35,
        name: "情感成熟",
        brief: "培养情感成熟度",
        description: "发展成熟的情感处理能力，在复杂情况下保持理智。",
        estimatedTime: 42,
        learnerCount: 123,
        tags: ["成熟", "理智", "稳定"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "理解情感成熟的标志",
            "培养情绪稳定性",
            "学会理性处理情感冲突",
            "发展长远的情感视角"
        ],
        keyPoints: [
            {
                icon: "🎯",
                title: "理性分析",
                content: "在情绪激动时保持理性思考",
                example: "生气时先冷静分析原因再行动"
            },
            {
                icon: "⚖️",
                title: "情理平衡",
                content: "在情感和理智间找到平衡",
                example: "既要感受情感，也要理性处理"
            },
            {
                icon: "🌱",
                title: "持续成长",
                content: "从每次情感经历中学习成长",
                example: "反思情感反应，寻找改进空间"
            }
        ],
        practiceScenarios: [
            {
                title: "工作冲突",
                description: "成熟地处理工作中的人际冲突"
            },
            {
                title: "关系危机",
                description: "理智地应对感情关系中的问题"
            }
        ]
    },

    36: {
        id: 36,
        name: "情感智慧",
        brief: "综合运用情感理解技能",
        description: "整合各种情感技能，在生活中智慧地处理情感问题。",
        estimatedTime: 50,
        learnerCount: 89,
        tags: ["智慧", "综合", "应用"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "整合各种情感技能",
            "在复杂情况下灵活运用",
            "培养情感洞察力",
            "成为情感智慧的人"
        ],
        keyPoints: [
            {
                icon: "🧩",
                title: "技能整合",
                content: "综合运用各种情感技能",
                example: "在一次对话中运用倾听、共情、边界设置"
            },
            {
                icon: "👁️",
                title: "深度洞察",
                content: "看透情感表象，理解深层需求",
                example: "理解愤怒背后的伤痛或恐惧"
            },
            {
                icon: "🎭",
                title: "情境适应",
                content: "根据不同情境调整情感策略",
                example: "在不同场合选择合适的情感表达方式"
            }
        ],
        practiceScenarios: [
            {
                title: "复杂关系",
                description: "处理多方面情感需求的复杂关系"
            },
            {
                title: "团队领导",
                description: "作为领导者处理团队的情感问题"
            }
        ]
    },

    37: {
        id: 37,
        name: "正念情感",
        brief: "以正念方式体验情感",
        description: "学会不带判断地观察和体验情感，培养情感觉察力。",
        estimatedTime: 32,
        learnerCount: 234,
        tags: ["正念", "觉察", "观察"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "学会正念观察情感的技巧",
            "培养不判断的情感觉察",
            "理解情感的无常性",
            "发展内在的情感智慧"
        ],
        keyPoints: [
            {
                icon: "🧘‍♀️",
                title: "觉察当下",
                content: "专注于当下的情感体验",
                example: "注意此刻身体的感受和情绪状态"
            },
            {
                icon: "☁️",
                title: "如云观情",
                content: "如观察天空的云朵般观察情感",
                example: "看着愤怒如云朵般升起又消散"
            },
            {
                icon: "🚫",
                title: "无判断",
                content: "不对情感进行好坏对错的判断",
                example: "接受所有情感都是正常的人类体验"
            }
        ],
        practiceScenarios: [
            {
                title: "冥想练习",
                description: "通过冥想培养情感觉察力"
            },
            {
                title: "日常觉察",
                description: "在日常生活中练习正念观察情感"
            }
        ]
    },

    38: {
        id: 38,
        name: "情感沟通",
        brief: "在关系中进行情感沟通",
        description: "学会在亲密关系中开诚布公地讨论情感话题。",
        estimatedTime: 33,
        learnerCount: 178,
        tags: ["沟通", "亲密关系", "开放"],
        category: "emotional_expression",
        categoryName: "情感理解",
        objectives: [
            "学会表达真实的情感需求",
            "培养情感话题的沟通技巧",
            "建立安全的情感交流环境",
            "深化亲密关系的情感连接"
        ],
        keyPoints: [
            {
                icon: "💭",
                title: "真实表达",
                content: "诚实地表达自己的感受和需求",
                example: "我感到被忽视了，希望得到更多关注"
            },
            {
                icon: "🛡️",
                title: "安全空间",
                content: "创造安全的情感分享环境",
                example: "承诺不会因对方的情感表达而批评"
            },
            {
                icon: "🔄",
                title: "双向交流",
                content: "既表达自己也倾听对方的情感",
                example: "分享后询问对方的感受和想法"
            }
        ],
        practiceScenarios: [
            {
                title: "伴侣对话",
                description: "与伴侣讨论关系中的情感需求"
            },
            {
                title: "家庭沟通",
                description: "在家庭中开展深层的情感交流"
            }
        ]
    },

    39: {
        id: 39,
        name: "自我介绍",
        brief: "在不同场合进行恰当的自我介绍",
        description: "学会在各种社交场合进行有效的自我介绍，留下良好第一印象。",
        estimatedTime: 15,
        learnerCount: 612,
        tags: ["介绍", "第一印象", "基础"],
        category: "relationship_building",
        categoryName: "关系建立",
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
                content: "简短而有亮点的自我介绍",
                example: "我是张三，热爱设计的产品经理"
            }
        ],
        practiceScenarios: [
            {
                title: "职场社交",
                description: "在公司聚会上自我介绍"
            }
        ]
    },

    40: {
        id: 40,
        name: "破冰对话",
        brief: "自然地开启对话和交流",
        description: "掌握开启对话的技巧，在社交场合自然交流。",
        estimatedTime: 18,
        learnerCount: 578,
        tags: ["破冰", "开场"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握破冰对话的基本技巧",
            "学会选择合适的开场话题",
            "培养自然交流的能力",
            "克服社交初期的紧张感"
        ],
        keyPoints: [
            {
                icon: "👋",
                title: "自然开场",
                content: "选择轻松自然的话题开启对话",
                example: "从环境、天气或当前活动开始话题"
            },
            {
                icon: "😊",
                title: "积极态度",
                content: "保持友善和开放的态度",
                example: "微笑、眼神交流，展现友好形象"
            },
            {
                icon: "❓",
                title: "开放问题",
                content: "使用开放性问题引导对话",
                example: "你觉得这个活动怎么样？"
            }
        ],
        practiceScenarios: [
            {
                title: "聚会初识",
                description: "在朋友聚会上与陌生人开始对话"
            },
            {
                title: "职场社交",
                description: "在公司活动中与同事破冰交流"
            }
        ]
    },

    41: {
        id: 41,
        name: "共同话题",
        brief: "快速找到和他人的共同兴趣点",
        description: "快速找到和他人的共同兴趣点，建立连接。",
        estimatedTime: 22,
        learnerCount: 445,
        tags: ["共同点", "兴趣"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "学会发现共同兴趣和经历",
            "掌握话题转换的技巧",
            "建立有意义的连接点",
            "深化对话的深度"
        ],
        keyPoints: [
            {
                icon: "🔍",
                title: "主动探索",
                content: "主动了解对方的兴趣和背景",
                example: "你平时喜欢做什么运动？"
            },
            {
                icon: "🎯",
                title: "敏锐观察",
                content: "从对话中捕捉共同点的线索",
                example: "注意对方提到的爱好、经历、观点"
            },
            {
                icon: "🌉",
                title: "建立桥梁",
                content: "用共同点作为深入交流的桥梁",
                example: "我也喜欢这个，我们可以聊聊..."
            }
        ],
        practiceScenarios: [
            {
                title: "兴趣发现",
                description: "在咖啡厅与邻桌发现共同的读书爱好"
            },
            {
                title: "经历分享",
                description: "发现和同事有相似的工作经历"
            }
        ]
    },

    42: {
        id: 42,
        name: "深度对话",
        brief: "与他人进行有意义的深层交流",
        description: "学会与他人进行有意义的深层交流。",
        estimatedTime: 35,
        learnerCount: 367,
        tags: ["深度", "对话"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "超越表面寒暄进入深层对话",
            "学会提出有深度的问题",
            "培养倾听和回应的技巧",
            "建立更深层的人际连接"
        ],
        keyPoints: [
            {
                icon: "💭",
                title: "深层提问",
                content: "提出能引发思考的开放性问题",
                example: "什么事情最能让你感到充实？"
            },
            {
                icon: "👂",
                title: "专注倾听",
                content: "全神贯注地倾听对方的分享",
                example: "不急于分享自己，先充分理解对方"
            },
            {
                icon: "🤝",
                title: "真诚回应",
                content: "给予真诚而有深度的回应",
                example: "分享相关的个人体验和感受"
            }
        ],
        practiceScenarios: [
            {
                title: "价值观探讨",
                description: "与朋友讨论人生价值观和目标"
            },
            {
                title: "情感分享",
                description: "在适当时机分享内心的感受和想法"
            }
        ]
    },

    43: {
        id: 43,
        name: "关系修复",
        brief: "修复受损的人际关系",
        description: "学会在关系出现问题时进行有效的修复和重建。",
        estimatedTime: 42,
        learnerCount: 198,
        tags: ["修复", "重建"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "勇敢面对关系问题",
            "学会真诚道歉",
            "寻找解决方案",
            "重建信任基础"
        ],
        keyPoints: [
            {
                icon: "🔧",
                title: "诚心道歉",
                content: "真诚承认错误并道歉",
                example: "我为我的行为道歉，我想修复我们的关系"
            }
        ],
        practiceScenarios: [
            {
                title: "友谊修复",
                description: "修复因误解破裂的友谊"
            }
        ]
    },

    44: {
        id: 44,
        name: "团队合作",
        brief: "在团队中发挥协作精神",
        description: "在团队中发挥协作精神，促进团队和谐。",
        estimatedTime: 30,
        learnerCount: 523,
        tags: ["团队", "合作"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握团队协作的基本原则",
            "学会在团队中发挥个人优势",
            "促进团队成员间的和谐",
            "共同实现团队目标"
        ],
        keyPoints: [
            {
                icon: "🤝",
                title: "协作精神",
                content: "主动配合团队成员工作",
                example: "分享资源，互相支持，共同完成任务"
            },
            {
                icon: "🎯",
                title: "目标一致",
                content: "将个人目标与团队目标对齐",
                example: "优先考虑团队利益，服务大局"
            },
            {
                icon: "💪",
                title: "优势互补",
                content: "发挥各自优势，弥补团队短板",
                example: "认识自己的长处，补充他人不足"
            }
        ],
        practiceScenarios: [
            {
                title: "项目协作",
                description: "在跨部门项目中协调合作"
            },
            {
                title: "团队建设",
                description: "参与团队建设活动"
            }
        ]
    },

    45: {
        id: 45,
        name: "代际沟通",
        brief: "与不同年龄段的人有效沟通",
        description: "学会与不同年龄段的人有效沟通。",
        estimatedTime: 25,
        learnerCount: 234,
        tags: ["跨代", "理解"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "理解不同年龄段的特点",
            "掌握跨代沟通技巧",
            "促进代际理解和融合",
            "建立跨代友谊"
        ],
        keyPoints: [
            {
                icon: "🌱",
                title: "年龄敏感",
                content: "理解不同年龄段的成长背景",
                example: "了解各代人的时代特征和价值观"
            },
            {
                icon: "🔄",
                title: "双向学习",
                content: "既向年长者学习，也与年轻人交流",
                example: "从经验中学习，向创新思维开放"
            },
            {
                icon: "🤝",
                title: "求同存异",
                content: "寻找共同点，尊重差异",
                example: "找到共同兴趣，理解时代差异"
            }
        ],
        practiceScenarios: [
            {
                title: "职场融合",
                description: "在多代同堂的工作环境中协作"
            },
            {
                title: "家庭和谐",
                description: "促进家庭中不同年龄成员的理解"
            }
        ]
    },

    46: {
        id: 46,
        name: "关系维护",
        brief: "维持长期的人际关系",
        description: "学会维持长期的人际关系。",
        estimatedTime: 30,
        learnerCount: 345,
        tags: ["维护", "长期"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握关系维护的基本技巧",
            "学会投资长期关系",
            "处理关系中的问题",
            "保持关系的活力"
        ],
        keyPoints: [
            {
                icon: "📞",
                title: "定期联系",
                content: "保持适度而持续的联系",
                example: "定期问候，分享生活动态"
            },
            {
                icon: "🎁",
                title: "情感投资",
                content: "在重要时刻给予关心和支持",
                example: "记住重要日期，及时表达祝福"
            },
            {
                icon: "🔧",
                title: "问题处理",
                content: "及时处理关系中的小矛盾",
                example: "主动沟通，化解误会"
            }
        ],
        practiceScenarios: [
            {
                title: "老友重聚",
                description: "与多年不见的朋友重新连接"
            },
            {
                title: "关系修复",
                description: "修复因误会而疏远的关系"
            }
        ]
    },

    47: {
        id: 47,
        name: "关系边界",
        brief: "在建立关系时保持适当边界",
        description: "在建立关系的同时保持适当的个人边界。",
        estimatedTime: 28,
        learnerCount: 289,
        tags: ["边界", "平衡"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "学会设置健康的关系边界",
            "在亲密和独立间找平衡",
            "保护个人隐私和空间",
            "建立可持续的关系模式"
        ],
        keyPoints: [
            {
                icon: "🚧",
                title: "边界设置",
                content: "明确个人的底线和原则",
                example: "清晰表达个人需要的空间"
            },
            {
                icon: "⚖️",
                title: "平衡艺术",
                content: "在给予和接受间保持平衡",
                example: "避免过度付出或过度依赖"
            },
            {
                icon: "🔒",
                title: "隐私保护",
                content: "保护个人隐私信息",
                example: "选择性分享个人信息"
            }
        ],
        practiceScenarios: [
            {
                title: "亲密关系",
                description: "在恋爱关系中保持个人空间"
            },
            {
                title: "友谊边界",
                description: "与朋友保持适当的距离"
            }
        ]
    },

    48: {
        id: 48,
        name: "群体融入",
        brief: "快速融入新的群体或团队",
        description: "快速融入新的群体或团队，建立归属感。",
        estimatedTime: 32,
        learnerCount: 456,
        tags: ["融入", "群体"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握快速融入群体的技巧",
            "建立群体归属感",
            "适应群体文化和规范",
            "在群体中找到自己的位置"
        ],
        keyPoints: [
            {
                icon: "👀",
                title: "观察学习",
                content: "观察群体的文化和规范",
                example: "了解群体的沟通方式和价值观"
            },
            {
                icon: "🤝",
                title: "主动参与",
                content: "积极参与群体活动",
                example: "主动参加团队建设和社交活动"
            },
            {
                icon: "💝",
                title: "贡献价值",
                content: "为群体提供独特价值",
                example: "发挥个人专长，帮助团队"
            }
        ],
        practiceScenarios: [
            {
                title: "新工作环境",
                description: "在新公司快速融入团队"
            },
            {
                title: "社交圈融入",
                description: "加入新的朋友圈或兴趣小组"
            }
        ]
    },

    49: {
        id: 49,
        name: "文化差异",
        brief: "理解和尊重文化差异",
        description: "理解和尊重不同文化背景的差异。",
        estimatedTime: 35,
        learnerCount: 123,
        tags: ["文化", "差异"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "增进对不同文化的理解",
            "学会尊重文化差异",
            "避免文化冲突",
            "促进文化交流与融合"
        ],
        keyPoints: [
            {
                icon: "🌍",
                title: "文化学习",
                content: "主动学习了解不同文化",
                example: "了解不同文化的习俗和禁忌"
            },
            {
                icon: "🤝",
                title: "尊重差异",
                content: "尊重并欣赏文化差异",
                example: "不对其他文化做价值判断"
            },
            {
                icon: "🌉",
                title: "桥梁作用",
                content: "成为不同文化间的沟通桥梁",
                example: "帮助不同文化背景的人相互理解"
            }
        ],
        practiceScenarios: [
            {
                title: "国际合作",
                description: "与来自不同国家的同事合作"
            },
            {
                title: "文化活动",
                description: "参与多元文化交流活动"
            }
        ]
    },

    50: {
        id: 50,
        name: "文化适应",
        brief: "在不同文化环境中建立关系",
        description: "学会在多元文化环境中建立跨文化的人际关系。",
        estimatedTime: 35,
        learnerCount: 156,
        tags: ["跨文化", "适应"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "了解不同文化背景",
            "尊重文化差异",
            "寻找文化共同点",
            "建立跨文化友谊"
        ],
        keyPoints: [
            {
                icon: "🌍",
                title: "文化敏感",
                content: "尊重不同文化的交流方式",
                example: "了解不同文化的问候方式和禁忌"
            },
            {
                icon: "🤝",
                title: "寻找共同点",
                content: "发现跨越文化的共同兴趣",
                example: "用普世的兴趣如音乐、美食建立连接"
            },
            {
                icon: "🗣️",
                title: "语言适应",
                content: "调整语言表达方式适应对方",
                example: "使用简单清晰的语言，避免俚语"
            }
        ],
        practiceScenarios: [
            {
                title: "国际交流",
                description: "与外国同事建立友谊"
            },
            {
                title: "多元社区",
                description: "在多文化社区中融入和交流"
            }
        ]
    },

    51: {
        id: 51,
        name: "社交礼仪",
        brief: "掌握各种场合的社交礼仪",
        description: "掌握各种场合的社交礼仪，展现良好修养。",
        estimatedTime: 20,
        learnerCount: 567,
        tags: ["礼仪", "修养"],
        category: "relationship_building",
        categoryName: "关系建立",
        objectives: [
            "掌握基本社交礼仪规范",
            "了解不同场合的礼仪要求",
            "培养优雅得体的举止",
            "建立良好的第一印象"
        ],
        keyPoints: [
            {
                icon: "👤",
                title: "形象管理",
                content: "保持整洁得体的外在形象",
                example: "穿着得体，仪态端庄"
            },
            {
                icon: "🤝",
                title: "见面礼仪",
                content: "掌握正确的见面问候方式",
                example: "主动问候，适当握手，记住姓名"
            },
            {
                icon: "🍽️",
                title: "用餐礼仪",
                content: "了解正式场合的用餐规范",
                example: "正确使用餐具，保持用餐礼貌"
            }
        ],
        practiceScenarios: [
            {
                title: "商务宴请",
                description: "参加正式的商务晚宴"
            },
            {
                title: "社交聚会",
                description: "在高端社交场合展现礼仪"
            }
        ]
    },

    52: {
        id: 52,
        name: "客户服务",
        brief: "在服务行业中的沟通技巧",
        description: "学会在服务客户时保持专业和耐心，处理各种客户需求。",
        estimatedTime: 30,
        learnerCount: 789,
        tags: ["客服", "专业"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握专业的服务态度",
            "学会处理客户投诉",
            "提升客户满意度",
            "维护公司形象"
        ],
        keyPoints: [
            {
                icon: "😊",
                title: "服务态度",
                content: "始终保持友善和专业的态度",
                example: "主动问候，微笑服务，耐心回答"
            },
            {
                icon: "👂",
                title: "需求理解",
                content: "准确理解客户的真实需求",
                example: "仔细倾听，确认理解，提供解决方案"
            },
            {
                icon: "🔧",
                title: "问题解决",
                content: "快速有效地解决客户问题",
                example: "分析问题根源，提供多种解决选择"
            }
        ],
        practiceScenarios: [
            {
                title: "投诉处理",
                description: "处理不满客户的投诉"
            },
            {
                title: "需求咨询",
                description: "为客户提供产品咨询服务"
            }
        ]
    },

    53: {
        id: 53,
        name: "医患沟通",
        brief: "医疗环境中的特殊沟通",
        description: "学会在医疗场景中进行敏感而有效的沟通。",
        estimatedTime: 40,
        learnerCount: 234,
        tags: ["医疗", "敏感"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握医疗沟通的特殊性",
            "学会传达敏感医疗信息",
            "建立医患信任关系",
            "处理医疗冲突"
        ],
        keyPoints: [
            {
                icon: "❤️",
                title: "同理心",
                content: "理解患者的焦虑和恐惧",
                example: "用温和的语调，表达关怀和理解"
            },
            {
                icon: "📋",
                title: "信息传达",
                content: "清晰准确地传达医疗信息",
                example: "用患者能理解的语言解释病情"
            },
            {
                icon: "🤝",
                title: "信任建立",
                content: "建立患者对医疗团队的信任",
                example: "展现专业性，履行承诺"
            }
        ],
        practiceScenarios: [
            {
                title: "坏消息告知",
                description: "向患者告知不良诊断结果"
            },
            {
                title: "治疗解释",
                description: "向家属解释复杂的治疗方案"
            }
        ]
    },

    54: {
        id: 54,
        name: "法律咨询",
        brief: "法律场景中的沟通技巧",
        description: "学会在法律咨询和诉讼中进行准确清晰的沟通。",
        estimatedTime: 45,
        learnerCount: 156,
        tags: ["法律", "准确"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握法律沟通的专业性",
            "确保信息的准确传达",
            "保护客户权益",
            "处理法律纠纷"
        ],
        keyPoints: [
            {
                icon: "⚖️",
                title: "专业术语",
                content: "准确使用法律专业术语",
                example: "用准确的法律概念解释案件"
            },
            {
                icon: "📝",
                title: "文档记录",
                content: "详细记录沟通内容",
                example: "记录重要对话，保留证据"
            },
            {
                icon: "🛡️",
                title: "权益保护",
                content: "始终以客户权益为重",
                example: "提醒客户潜在风险和权利"
            }
        ],
        practiceScenarios: [
            {
                title: "案件咨询",
                description: "为客户提供法律案件咨询"
            },
            {
                title: "庭审沟通",
                description: "在法庭上进行有效陈述"
            }
        ]
    },

    55: {
        id: 55,
        name: "教育沟通",
        brief: "教育环境中的沟通方法",
        description: "学会在教学和培训中进行有效的知识传递和互动。",
        estimatedTime: 35,
        learnerCount: 567,
        tags: ["教育", "传递"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握有效的教学沟通技巧",
            "激发学习者的兴趣",
            "处理课堂互动",
            "评估学习效果"
        ],
        keyPoints: [
            {
                icon: "🎯",
                title: "目标明确",
                content: "清晰传达学习目标和要求",
                example: "开课前明确说明学习目标"
            },
            {
                icon: "🧠",
                title: "因材施教",
                content: "根据学习者特点调整沟通方式",
                example: "用不同方式解释同一概念"
            },
            {
                icon: "💡",
                title: "启发引导",
                content: "用提问引导学习者思考",
                example: "通过问题引导学生发现答案"
            }
        ],
        practiceScenarios: [
            {
                title: "课堂教学",
                description: "在课堂上进行有效教学"
            },
            {
                title: "培训指导",
                description: "为员工提供技能培训"
            }
        ]
    },

    56: {
        id: 56,
        name: "销售沟通",
        brief: "销售场景中的说服技巧",
        description: "学会在销售过程中建立信任，了解需求，促成交易。",
        estimatedTime: 38,
        learnerCount: 678,
        tags: ["销售", "说服"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握销售沟通的核心技巧",
            "建立客户信任关系",
            "了解客户真实需求",
            "促成成功交易"
        ],
        keyPoints: [
            {
                icon: "🎯",
                title: "需求挖掘",
                content: "深入了解客户的真实需求",
                example: "通过开放性问题了解客户痛点"
            },
            {
                icon: "🤝",
                title: "信任建立",
                content: "通过专业性建立客户信任",
                example: "展示产品知识，提供专业建议"
            },
            {
                icon: "💡",
                title: "价值传达",
                content: "清晰传达产品价值和优势",
                example: "用客户语言解释产品价值"
            }
        ],
        practiceScenarios: [
            {
                title: "产品介绍",
                description: "向潜在客户介绍产品特点"
            },
            {
                title: "异议处理",
                description: "处理客户的购买疑虑"
            }
        ]
    },

    57: {
        id: 57,
        name: "媒体应对",
        brief: "面对媒体时的沟通策略",
        description: "学会在面对媒体采访时保持冷静，传达准确信息。",
        estimatedTime: 42,
        learnerCount: 89,
        tags: ["媒体", "策略"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握媒体沟通的特殊技巧",
            "学会应对媒体提问",
            "维护个人或组织形象",
            "传达准确清晰的信息"
        ],
        keyPoints: [
            {
                icon: "📺",
                title: "镜头意识",
                content: "在摄像机前保持自然状态",
                example: "眼神交流，姿态自然，语速适中"
            },
            {
                icon: "🎤",
                title: "信息控制",
                content: "掌控采访节奏和信息传达",
                example: "准备核心信息，回到主要观点"
            },
            {
                icon: "🛡️",
                title: "危机应对",
                content: "面对棘手问题的应对策略",
                example: "承认问题，表达解决方案"
            }
        ],
        practiceScenarios: [
            {
                title: "新闻采访",
                description: "接受电视台记者采访"
            },
            {
                title: "危机发布",
                description: "在危机时期举行新闻发布会"
            }
        ]
    },

    58: {
        id: 58,
        name: "社区沟通",
        brief: "在社区活动中的沟通技巧",
        description: "学会在社区建设和邻里关系中进行有效沟通。",
        estimatedTime: 25,
        learnerCount: 345,
        tags: ["社区", "邻里"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "促进社区和谐发展",
            "建立良好邻里关系",
            "参与社区事务",
            "解决社区矛盾"
        ],
        keyPoints: [
            {
                icon: "🏘️",
                title: "社区意识",
                content: "培养集体利益优先的意识",
                example: "考虑行为对邻居的影响"
            },
            {
                icon: "🤝",
                title: "友善交往",
                content: "与邻居保持友善的日常交往",
                example: "主动问候，互相帮助"
            },
            {
                icon: "🗣️",
                title: "参与表达",
                content: "在社区会议中表达意见",
                example: "理性发言，尊重不同观点"
            }
        ],
        practiceScenarios: [
            {
                title: "社区会议",
                description: "参加业主大会表达意见"
            },
            {
                title: "邻里调解",
                description: "协调邻居间的小摩擦"
            }
        ]
    },

    59: {
        id: 59,
        name: "志愿服务",
        brief: "志愿服务中的沟通方式",
        description: "学会在志愿活动中与受助者和其他志愿者有效沟通。",
        estimatedTime: 28,
        learnerCount: 234,
        tags: ["志愿", "服务"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握志愿服务的沟通方式",
            "与受助者建立信任",
            "协调志愿者团队",
            "传递正能量"
        ],
        keyPoints: [
            {
                icon: "❤️",
                title: "服务精神",
                content: "以真诚的心态提供帮助",
                example: "不带偏见，平等对待每个人"
            },
            {
                icon: "🤝",
                title: "尊重尊严",
                content: "在帮助中保护受助者的尊严",
                example: "避免居高临下，尊重个人选择"
            },
            {
                icon: "👥",
                title: "团队协作",
                content: "与其他志愿者有效协作",
                example: "分工合作，相互支持"
            }
        ],
        practiceScenarios: [
            {
                title: "慈善活动",
                description: "在慈善机构做志愿服务"
            },
            {
                title: "社区服务",
                description: "为社区老人提供帮助"
            }
        ]
    },

    60: {
        id: 60,
        name: "应急沟通",
        brief: "紧急情况下的沟通方法",
        description: "学会在紧急情况下保持冷静，进行有效的危机沟通。",
        estimatedTime: 35,
        learnerCount: 167,
        tags: ["应急", "危机"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握危机沟通的基本原则",
            "在紧急情况下保持冷静",
            "快速传达关键信息",
            "协调应急响应"
        ],
        keyPoints: [
            {
                icon: "🚨",
                title: "快速反应",
                content: "在紧急情况下快速做出反应",
                example: "迅速评估情况，确定优先级"
            },
            {
                icon: "📢",
                title: "清晰传达",
                content: "用简洁明确的语言传达信息",
                example: "避免专业术语，确保信息准确"
            },
            {
                icon: "🧘",
                title: "情绪控制",
                content: "在高压环境下保持情绪稳定",
                example: "深呼吸，保持语调稳定"
            }
        ],
        practiceScenarios: [
            {
                title: "火灾疏散",
                description: "在火灾时指导人员疏散"
            },
            {
                title: "医疗急救",
                description: "协助医疗急救沟通"
            }
        ]
    },

    61: {
        id: 61,
        name: "政府沟通",
        brief: "与政府部门沟通的技巧",
        description: "学会在与政府机构交涉时使用恰当的沟通方式。",
        estimatedTime: 32,
        learnerCount: 123,
        tags: ["政府", "交涉"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "了解政府部门的工作流程",
            "掌握正式沟通的技巧",
            "维护合法权益",
            "建立良好的政民关系"
        ],
        keyPoints: [
            {
                icon: "📋",
                title: "程序规范",
                content: "了解并遵循官方程序",
                example: "准备齐全的文件，按流程办事"
            },
            {
                icon: "🎯",
                title: "目标明确",
                content: "清晰表达诉求和期望",
                example: "准备书面材料，逻辑清晰"
            },
            {
                icon: "🤝",
                title: "尊重合作",
                content: "保持尊重和合作的态度",
                example: "理解公务员的工作约束"
            }
        ],
        practiceScenarios: [
            {
                title: "办事申请",
                description: "到政府部门办理证件"
            },
            {
                title: "政策咨询",
                description: "咨询相关政策和规定"
            }
        ]
    },

    62: {
        id: 62,
        name: "国际交流",
        brief: "国际环境中的沟通技巧",
        description: "学会在国际交流中展现文化敏感性和专业素养。",
        estimatedTime: 48,
        learnerCount: 78,
        tags: ["国际", "文化敏感"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "掌握跨文化沟通技巧",
            "展现国际化视野",
            "建立国际友谊",
            "促进文化交流"
        ],
        keyPoints: [
            {
                icon: "🌍",
                title: "文化尊重",
                content: "深入了解和尊重不同文化",
                example: "学习对方文化的基本礼仪"
            },
            {
                icon: "🗣️",
                title: "语言适应",
                content: "调整语言表达适应国际交流",
                example: "使用国际通用的表达方式"
            },
            {
                icon: "🤝",
                title: "友好开放",
                content: "展现开放友好的中国形象",
                example: "分享中国文化，学习他国文化"
            }
        ],
        practiceScenarios: [
            {
                title: "国际会议",
                description: "参加国际学术或商务会议"
            },
            {
                title: "文化交流",
                description: "参与国际文化交流活动"
            }
        ]
    },

    63: {
        id: 63,
        name: "老年沟通",
        brief: "与老年人沟通的特殊技巧",
        description: "学会与老年人进行耐心、尊重的沟通，考虑其特殊需求。",
        estimatedTime: 30,
        learnerCount: 345,
        tags: ["老年", "耐心"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "理解老年人的沟通特点",
            "展现尊重和耐心",
            "帮助老年人表达需求",
            "促进代际理解"
        ],
        keyPoints: [
            {
                icon: "👴",
                title: "尊重经验",
                content: "尊重老年人的人生经验和智慧",
                example: "倾听他们的故事和建议"
            },
            {
                icon: "🔊",
                title: "清晰表达",
                content: "使用清晰缓慢的语言表达",
                example: "适当提高音量，语速放慢"
            },
            {
                icon: "⏰",
                title: "充足时间",
                content: "给予老年人充足的思考时间",
                example: "不催促，耐心等待回应"
            }
        ],
        practiceScenarios: [
            {
                title: "养老服务",
                description: "在养老院与老人交流"
            },
            {
                title: "家庭沟通",
                description: "与家中长辈深入交流"
            }
        ]
    },

    64: {
        id: 64,
        name: "儿童沟通",
        brief: "与儿童有效沟通的方法",
        description: "学会用儿童能理解的方式进行沟通，建立信任关系。",
        estimatedTime: 33,
        learnerCount: 456,
        tags: ["儿童", "信任"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "了解儿童的认知特点",
            "建立与儿童的信任关系",
            "用适合的方式表达",
            "保护儿童的身心健康"
        ],
        keyPoints: [
            {
                icon: "👶",
                title: "平等视角",
                content: "以平等的视角与儿童交流",
                example: "蹲下与孩子保持同一高度"
            },
            {
                icon: "🎨",
                title: "生动表达",
                content: "用生动有趣的方式表达",
                example: "用故事、游戏传达信息"
            },
            {
                icon: "🛡️",
                title: "保护意识",
                content: "时刻关注儿童的安全和感受",
                example: "及时察觉孩子的情绪变化"
            }
        ],
        practiceScenarios: [
            {
                title: "教育指导",
                description: "为儿童提供学习指导"
            },
            {
                title: "心理疏导",
                description: "帮助儿童处理情感问题"
            }
        ]
    },

    65: {
        id: 65,
        name: "残障沟通",
        brief: "与残障人士沟通的技巧",
        description: "学会以尊重和包容的态度与残障人士进行有效沟通。",
        estimatedTime: 28,
        learnerCount: 234,
        tags: ["残障", "包容"],
        category: "special_scenarios",
        categoryName: "特殊情境",
        objectives: [
            "了解不同残障类型的沟通需求",
            "消除沟通障碍",
            "展现尊重和包容",
            "促进无障碍交流"
        ],
        keyPoints: [
            {
                icon: "♿",
                title: "无障碍意识",
                content: "主动创造无障碍沟通环境",
                example: "确保轮椅用户的视线高度"
            },
            {
                icon: "👁️",
                title: "多元方式",
                content: "使用多种沟通方式",
                example: "手语、文字、图像等多种方式"
            },
            {
                icon: "❤️",
                title: "尊重包容",
                content: "以平等尊重的态度交流",
                example: "不因残障而改变正常交流方式"
            }
        ],
        practiceScenarios: [
            {
                title: "无障碍服务",
                description: "为残障人士提供服务"
            },
            {
                title: "融合活动",
                description: "参与残健融合活动"
            }
        ]
    }
};

// 根据分类获取技能列表
export function getSkillsByCategory(categoryId) {
    const categoryMaps = {
        'communication': { start: 1, end: 25 },
        'emotional_expression': { start: 26, end: 38 },
        'relationship_building': { start: 39, end: 51 },
        'special_scenarios': { start: 52, end: 65 }
    };

    const range = categoryMaps[categoryId];
    if (!range) return [];

    const skills = [];
    for (let i = range.start; i <= range.end; i++) {
        if (skillsData[i]) {
            skills.push(skillsData[i]);
        }
    }
    return skills;
}

// 获取单个技能数据
export function getSkillById(skillId) {
    const id = parseInt(skillId);
    return skillsData[id] || null;
}

// 获取推荐的相关技能
export function getRelatedSkills(skillId, count = 2) {
    const currentSkill = getSkillById(skillId);
    if (!currentSkill) return [];

    const categorySkills = getSkillsByCategory(currentSkill.category);
    const relatedSkills = categorySkills.filter(skill => skill.id !== currentSkill.id);

    // 随机选择相关技能
    const shuffled = relatedSkills.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

// 分类信息
export const categories = {
    'communication': {
        id: 'communication',
        name: '沟通表达',
        icon: '💬',
        description: '提升语言表达和沟通技巧'
    },
    'emotional_expression': {
        id: 'emotional_expression',
        name: '情感理解',
        icon: '❤️',
        description: '深入理解和表达情感'
    },
    'relationship_building': {
        id: 'relationship_building',
        name: '关系建立',
        icon: '🤝',
        description: '建立和维护人际关系'
    },
    'special_scenarios': {
        id: 'special_scenarios',
        name: '特殊情境',
        icon: '🎯',
        description: '应对特殊场合的沟通挑战'
    }
};

export default {
    skillsData,
    getSkillsByCategory,
    getSkillById,
    getRelatedSkills,
    categories
};
