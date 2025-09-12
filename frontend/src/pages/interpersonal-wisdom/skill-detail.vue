<template>
    <view class="skill-detail-container">
        <view class="header">
            <view class="skill-header">
                <view class="skill-basic-info">
                    <text class="skill-title">{{ skillData.name }}</text>
                    <view class="skill-meta">
                        <view class="difficulty-badge" :class="skillData.difficulty">
                            <text class="difficulty-text">{{ getDifficultyText(skillData.difficulty) }}</text>
                        </view>
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
                <view class="skill-progress" v-if="skillData.status === 'learning'">
                    <view class="progress-circle">
                        <text class="progress-text">{{ skillData.progress }}%</text>
                    </view>
                </view>
                <view class="skill-status" v-else-if="skillData.status === 'mastered'">
                    <text class="status-icon">✅</text>
                    <text class="status-text">已掌握</text>
                </view>
            </view>

            <text class="skill-description">{{ skillData.description }}</text>

            <view class="skill-tags">
                <text v-for="tag in skillData.tags" :key="tag" class="skill-tag">{{ tag }}</text>
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
            <view class="section">
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
            <view class="section">
                <view class="section-header">
                    <text class="section-title">🎭 场景应用</text>
                </view>
                <view class="scenarios">
                    <view v-for="scenario in skillData.scenarios" :key="scenario.id" class="scenario-card"
                        @click="practiceScenario(scenario)">
                        <view class="scenario-header">
                            <text class="scenario-title">{{ scenario.title }}</text>
                            <text class="scenario-difficulty">{{ scenario.difficulty }}</text>
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
                        <view class="related-skill-status" :class="skill.status">
                            <text class="status-text">{{ getStatusText(skill.status) }}</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 底部操作区域 -->
        <view class="bottom-actions">
            <view v-if="skillData.status === 'new'" class="action-btn primary" @click="startLearning">
                <text class="btn-text">开始学习</text>
            </view>
            <view v-else-if="skillData.status === 'learning'" class="action-btn primary" @click="continueLearning">
                <text class="btn-text">继续学习</text>
            </view>
            <view v-else class="action-btn secondary" @click="reviewSkill">
                <text class="btn-text">复习技能</text>
            </view>

            <view class="action-btn tertiary" @click="generatePracticeScenario">
                <text class="btn-text">AI生成场景</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            skillId: '',
            categoryId: '',
            skillData: {},
            relatedSkills: []
        }
    },

    onLoad(options) {
        this.skillId = options.skillId;
        this.categoryId = options.categoryId;
        this.loadSkillDetail();
    },

    methods: {
        async loadSkillDetail() {
            try {
                uni.showLoading({ title: '加载中...' });

                // 模拟API调用
                await this.mockLoadSkillDetail();

            } catch (error) {
                console.error('加载技能详情失败:', error);
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        // async mockLoadSkillDetail() {
        //     // 模拟数据
        //     this.skillData = {
        //         id: this.skillId,
        //         name: '主动倾听',
        //         description: '主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。',
        //         difficulty: 'basic',
        //         estimatedTime: 15,
        //         learnerCount: 1234,
        //         status: 'learning',
        //         progress: 65,
        //         tags: ['倾听', '沟通基础', '理解'],
        //         objectives: [
        //             '学会集中注意力倾听对方说话',
        //             '理解言语背后的情感和需求',
        //             '通过肢体语言展现倾听态度',
        //             '运用复述和确认技巧验证理解'
        //         ],
        //         keyPoints: [
        //             {
        //                 icon: '👀',
        //                 title: '眼神交流',
        //                 content: '保持适当的眼神交流，表达对对方的关注和尊重',
        //                 example: '看着对方的眼睛，偶尔点头表示理解'
        //             },
        //             {
        //                 icon: '🤐',
        //                 title: '避免打断',
        //                 content: '让对方完整表达想法，不要急于插话或给建议',
        //                 example: '等对方说完后再回应："我理解你的意思是..."'
        //             },
        //             {
        //                 icon: '🔄',
        //                 title: '反馈确认',
        //                 content: '用自己的话复述对方的观点，确认理解正确',
        //                 example: '"如果我理解正确，你是想说..."'
        //             }
        //         ],
        //         practiceSteps: [
        //             {
        //                 title: '营造倾听环境',
        //                 description: '选择安静、舒适的环境，放下手机等干扰物',
        //                 tips: '将手机调至静音模式，身体面向对方'
        //             },
        //             {
        //                 title: '专注关注对方',
        //                 description: '用眼神、肢体语言表达关注，避免思维游离',
        //                 tips: '点头、"嗯"等简单回应表示你在听'
        //             },
        //             {
        //                 title: '理解情感层面',
        //                 description: '不仅听懂字面意思，更要理解对方的感受',
        //                 tips: '注意对方的语调、表情变化'
        //             },
        //             {
        //                 title: '适当回馈确认',
        //                 description: '用复述、提问等方式确认理解正确',
        //                 tips: '使用"我听到你说..."、"你的意思是..."等句式'
        //             }
        //         ],
        //         scenarios: [
        //             {
        //                 id: 1,
        //                 title: '朋友倾诉工作压力',
        //                 description: '朋友向你抱怨工作中的困难和压力，需要你的倾听和理解',
        //                 difficulty: '基础'
        //             },
        //             {
        //                 id: 2,
        //                 title: '家人分享生活感受',
        //                 description: '家人想要分享一天的见闻和感受，需要你的关注',
        //                 difficulty: '基础'
        //             },
        //             {
        //                 id: 3,
        //                 title: '同事讨论项目分歧',
        //                 description: '同事对项目有不同看法，需要倾听并理解各方观点',
        //                 difficulty: '进阶'
        //             }
        //         ]
        //     };

        //     this.relatedSkills = [
        //         {
        //             id: 2,
        //             name: '情感表达',
        //             brief: '学会准确表达自己的情感和需求',
        //             status: 'new'
        //         },
        //         {
        //             id: 3,
        //             name: '有效提问',
        //             brief: '通过恰当的提问深入了解对方',
        //             status: 'learning'
        //         }
        //     ];
        // },

        async mockLoadSkillDetail() {
            // 根据不同的 skillId 返回不同的技能数据
            const skillDataMap = {
                // 沟通表达类技能
                1: {
                    id: 1,
                    name: '主动倾听',
                    description: '主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。',
                    difficulty: 'basic',
                    estimatedTime: 15,
                    learnerCount: 1234,
                    status: 'mastered',
                    progress: 100,
                    tags: ['倾听', '沟通基础', '理解'],
                    objectives: [
                        '学会集中注意力倾听对方说话',
                        '理解言语背后的情感和需求',
                        '通过肢体语言展现倾听态度',
                        '运用复述和确认技巧验证理解'
                    ],
                    keyPoints: [
                        {
                            icon: '👀',
                            title: '眼神交流',
                            content: '保持适当的眼神交流，表达对对方的关注和尊重',
                            example: '看着对方的眼睛，偶尔点头表示理解'
                        },
                        {
                            icon: '🤐',
                            title: '避免打断',
                            content: '让对方完整表达想法，不要急于插话或给建议',
                            example: '等对方说完后再回应："我理解你的意思是..."'
                        },
                        {
                            icon: '🔄',
                            title: '反馈确认',
                            content: '用自己的话复述对方的观点，确认理解正确',
                            example: '"如果我理解正确，你是想说..."'
                        }
                    ],
                    practiceSteps: [
                        {
                            title: '营造倾听环境',
                            description: '选择安静、舒适的环境，放下手机等干扰物',
                            tips: '将手机调至静音模式，身体面向对方'
                        },
                        {
                            title: '专注关注对方',
                            description: '用眼神、肢体语言表达关注，避免思维游离',
                            tips: '点头、"嗯"等简单回应表示你在听'
                        },
                        {
                            title: '理解情感层面',
                            description: '不仅听懂字面意思，更要理解对方的感受',
                            tips: '注意对方的语调、表情变化'
                        },
                        {
                            title: '适当回馈确认',
                            description: '用复述、提问等方式确认理解正确',
                            tips: '使用"我听到你说..."、"你的意思是..."等句式'
                        }
                    ],
                    scenarios: [
                        {
                            id: 1,
                            title: '朋友倾诉工作压力',
                            description: '朋友向你抱怨工作中的困难和压力，需要你的倾听和理解',
                            difficulty: '基础'
                        },
                        {
                            id: 2,
                            title: '家人分享生活感受',
                            description: '家人想要分享一天的见闻和感受，需要你的关注',
                            difficulty: '基础'
                        },
                        {
                            id: 3,
                            title: '同事讨论项目分歧',
                            description: '同事对项目有不同看法，需要倾听并理解各方观点',
                            difficulty: '进阶'
                        }
                    ]
                },
                2: {
                    id: 2,
                    name: '情感表达',
                    description: '学会准确、恰当地表达自己的情感和需求，避免指责和批评，建立更好的情感连接。',
                    difficulty: 'intermediate',
                    estimatedTime: 20,
                    learnerCount: 956,
                    status: 'learning',
                    progress: 65,
                    tags: ['情感', '表达', 'I语句'],
                    objectives: [
                        '学会使用"我"开头的表达方式',
                        '准确识别和表达自己的感受',
                        '避免指责性语言',
                        '清楚表达自己的需求和期望'
                    ],
                    keyPoints: [
                        {
                            icon: '🗣️',
                            title: 'I语句技巧',
                            content: '使用"我感到..."而不是"你让我..."的表达方式',
                            example: '"我感到被忽视了"而不是"你总是不理我"'
                        },
                        {
                            icon: '💭',
                            title: '情感词汇',
                            content: '丰富情感词汇，准确描述复杂的感受',
                            example: '不只是"不高兴"，可以说"失望"、"焦虑"、"困惑"'
                        },
                        {
                            icon: '🎯',
                            title: '具体表达',
                            content: '避免模糊表达，说出具体的情况和需求',
                            example: '"我希望你能在做决定前征求我的意见"'
                        }
                    ],
                    practiceSteps: [
                        {
                            title: '识别内心感受',
                            description: '花时间思考自己真正的感受是什么',
                            tips: '可以用情感轮盘或情感词汇表帮助识别'
                        },
                        {
                            title: '选择合适时机',
                            description: '在双方都冷静的时候进行情感表达',
                            tips: '避免在争吵或情绪激动时表达'
                        },
                        {
                            title: '使用I语句',
                            description: '以"我"开头，描述自己的感受而不是对方的行为',
                            tips: '"我感到..."、"我需要..."、"我希望..."'
                        },
                        {
                            title: '倾听对方回应',
                            description: '表达完后给对方回应的机会',
                            tips: '保持开放态度，准备进行对话而非独白'
                        }
                    ],
                    scenarios: [
                        {
                            id: 4,
                            title: '向伴侣表达不满',
                            description: '伴侣经常迟到，你需要表达自己的感受',
                            difficulty: '进阶'
                        },
                        {
                            id: 5,
                            title: '向朋友表达关心',
                            description: '朋友最近状态不好，你想表达关心',
                            difficulty: '基础'
                        },
                        {
                            id: 6,
                            title: '工作中表达异议',
                            description: '对同事的做法有不同看法，需要表达意见',
                            difficulty: '高级'
                        }
                    ]
                },
                3: {
                    id: 3,
                    name: '非暴力沟通',
                    description: '学习非暴力沟通的四个步骤：观察、感受、需要、请求，以善意和理解进行沟通。',
                    difficulty: 'advanced',
                    estimatedTime: 30,
                    learnerCount: 567,
                    status: 'new',
                    progress: 0,
                    tags: ['沟通技巧', '冲突处理', 'NVC'],
                    objectives: [
                        '掌握非暴力沟通四步法',
                        '学会客观观察而非评判',
                        '准确表达感受和需要',
                        '提出具体可行的请求'
                    ],
                    keyPoints: [
                        {
                            icon: '👁️',
                            title: '客观观察',
                            content: '描述具体事实而不加入个人判断和评价',
                            example: '"你这周有3天晚回家"而不是"你总是很晚回家"'
                        },
                        {
                            icon: '❤️',
                            title: '表达感受',
                            content: '说出自己的真实感受，而不是想法或评判',
                            example: '"我感到孤单"而不是"你不关心我"'
                        },
                        {
                            icon: '🎯',
                            title: '说出需要',
                            content: '明确表达自己的需要和价值观',
                            example: '"我需要更多的陪伴和关注"'
                        },
                        {
                            icon: '🤝',
                            title: '具体请求',
                            content: '提出明确、具体、可行的请求',
                            example: '"你能否每周安排两个晚上和我一起度过？"'
                        }
                    ],
                    practiceSteps: [
                        {
                            title: '观察练习',
                            description: '练习客观描述事实，不加入个人解释',
                            tips: '区分观察和评价，避免使用"总是"、"从不"等词'
                        },
                        {
                            title: '感受识别',
                            description: '学会区分感受和想法、评判',
                            tips: '真正的感受是身体的感觉，如难过、愤怒、喜悦'
                        },
                        {
                            title: '需要探索',
                            description: '深入了解感受背后的需要和价值观',
                            tips: '问自己"我为什么有这种感受？我真正需要什么？"'
                        },
                        {
                            title: '请求制定',
                            description: '提出积极、具体、可行的请求',
                            tips: '说出你希望对方做什么，而不是不要做什么'
                        }
                    ],
                    scenarios: [
                        {
                            id: 7,
                            title: '解决家庭冲突',
                            description: '家人之间发生分歧，需要用非暴力沟通解决',
                            difficulty: '高级'
                        },
                        {
                            id: 8,
                            title: '职场沟通障碍',
                            description: '与同事合作出现问题，需要有效沟通',
                            difficulty: '高级'
                        },
                        {
                            id: 9,
                            title: '朋友关系维护',
                            description: '朋友的行为让你困扰，需要真诚沟通',
                            difficulty: '进阶'
                        }
                    ]
                },
                4: {
                    id: 4,
                    name: '情绪识别',
                    description: '通过观察面部表情、语调、肢体语言等线索，准确识别自己和他人的情绪状态。',
                    difficulty: 'basic',
                    estimatedTime: 12,
                    learnerCount: 890,
                    status: 'mastered',
                    progress: 100,
                    tags: ['情绪识别', '观察力', '情商'],
                    objectives: [
                        '识别基础情绪：喜怒哀惧',
                        '观察非语言情绪信号',
                        '提升自我情绪觉察',
                        '理解情绪的层次和复杂性'
                    ],
                    keyPoints: [
                        {
                            icon: '😊',
                            title: '面部表情',
                            content: '观察眉毛、眼睛、嘴巴的细微变化',
                            example: '皱眉可能表示困惑或不满，眼睛放光表示兴奋'
                        },
                        {
                            icon: '🗣️',
                            title: '语调变化',
                            content: '注意说话的音调、语速、音量变化',
                            example: '语速加快可能表示紧张，音调提高可能表示兴奋'
                        },
                        {
                            icon: '🤲',
                            title: '肢体语言',
                            content: '观察姿态、手势、身体距离等信号',
                            example: '双臂交叉可能表示防御，靠近表示亲近'
                        }
                    ],
                    practiceSteps: [
                        {
                            title: '自我情绪监测',
                            description: '每天定时检查自己的情绪状态',
                            tips: '设置提醒，问自己"我现在感觉如何？"'
                        },
                        {
                            title: '他人观察练习',
                            description: '在日常交往中观察他人的情绪信号',
                            tips: '注意一致性，语言和非语言信号是否匹配'
                        },
                        {
                            title: '情绪词汇积累',
                            description: '学习更多情绪词汇，精确描述感受',
                            tips: '从基础的喜怒哀乐扩展到更细致的情绪'
                        }
                    ],
                    scenarios: [
                        {
                            id: 10,
                            title: '识别朋友的真实感受',
                            description: '朋友说"我很好"，但你感觉不对劲',
                            difficulty: '基础'
                        },
                        {
                            id: 11,
                            title: '工作会议情绪解读',
                            description: '在团队会议中观察同事们的情绪反应',
                            difficulty: '进阶'
                        }
                    ]
                },
                5: {
                    id: 5,
                    name: '情感共鸣',
                    description: '学会站在对方角度思考，与他人产生情感共鸣和深层理解。',
                    difficulty: 'intermediate',
                    estimatedTime: 25,
                    learnerCount: 675,
                    status: 'learning',
                    progress: 40,
                    tags: ['共情', '理解', '换位思考'],
                    objectives: [
                        '提升换位思考能力',
                        '学会情感镜像技巧',
                        '建立深层情感连接',
                        '避免过度共情的风险'
                    ],
                    keyPoints: [
                        {
                            icon: '🔄',
                            title: '换位思考',
                            content: '尝试从对方的角度理解事情',
                            example: '"如果我是他，我会有什么感受？"'
                        },
                        {
                            icon: '🪞',
                            title: '情感镜像',
                            content: '反映对方的情感状态，表达理解',
                            example: '"我能感受到你很沮丧"'
                        },
                        {
                            icon: '🛡️',
                            title: '保持边界',
                            content: '共情但不被对方情绪完全淹没',
                            example: '理解但保持自己的情绪稳定'
                        }
                    ],
                    practiceSteps: [
                        {
                            title: '暂停判断',
                            description: '停止对他人行为的立即评判',
                            tips: '先理解，再评价'
                        },
                        {
                            title: '询问了解',
                            description: '主动询问对方的感受和想法',
                            tips: '"你现在的感受是什么？"'
                        },
                        {
                            title: '反馈确认',
                            description: '确认你的理解是否正确',
                            tips: '"你的意思是...对吗？"'
                        }
                    ],
                    scenarios: [
                        {
                            id: 12,
                            title: '安慰失恋的朋友',
                            description: '朋友刚分手，情绪低落，需要你的理解',
                            difficulty: '进阶'
                        },
                        {
                            id: 13,
                            title: '理解家人的焦虑',
                            description: '家人对未来很担心，你需要理解他们的感受',
                            difficulty: '基础'
                        }
                    ]
                }
            };

            // 根据 skillId 获取对应数据，如果没有匹配则使用默认数据
            const skillData = skillDataMap[this.skillId] || skillDataMap[1];
            this.skillData = skillData;

            // 相关技能推荐
            const relatedSkillsMap = {
                1: [
                    { id: 2, name: '情感表达', brief: '准确表达自己的情感和需求', status: 'new' },
                    { id: 4, name: '情绪识别', brief: '准确识别自己和他人的情绪状态', status: 'mastered' }
                ],
                2: [
                    { id: 1, name: '主动倾听', brief: '学会用心倾听对方的话语和情感', status: 'mastered' },
                    { id: 3, name: '非暴力沟通', brief: '以善意和理解进行沟通', status: 'new' }
                ],
                3: [
                    { id: 2, name: '情感表达', brief: '准确表达自己的情感和需求', status: 'learning' },
                    { id: 5, name: '情感共鸣', brief: '与他人产生情感共鸣和理解', status: 'learning' }
                ],
                4: [
                    { id: 5, name: '情感共鸣', brief: '与他人产生情感共鸣和理解', status: 'learning' },
                    { id: 1, name: '主动倾听', brief: '学会用心倾听对方的话语和情感', status: 'mastered' }
                ],
                5: [
                    { id: 4, name: '情绪识别', brief: '准确识别自己和他人的情绪状态', status: 'mastered' },
                    { id: 1, name: '主动倾听', brief: '学会用心倾听对方的话语和情感', status: 'mastered' }
                ]
            };

            this.relatedSkills = relatedSkillsMap[this.skillId] || relatedSkillsMap[1];
        },

        startLearning() {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&type=learning`
            });
        },

        continueLearning() {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&type=continue`
            });
        },

        reviewSkill() {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&type=review`
            });
        },

        async generatePracticeScenario() {
            try {
                uni.showLoading({ title: 'AI生成场景中...' });

                // 模拟AI生成场景
                setTimeout(() => {
                    uni.hideLoading();
                    uni.navigateTo({
                        url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&type=ai-scenario`
                    });
                }, 2000);

            } catch (error) {
                console.error('生成场景失败:', error);
                uni.showToast({
                    title: '生成失败',
                    icon: 'none'
                });
            }
        },

        practiceScenario(scenario) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${this.skillId}&scenarioId=${scenario.id}&type=scenario`
            });
        },

        viewRelatedSkill(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.id}&categoryId=${this.categoryId}`
            });
        },

        getDifficultyText(difficulty) {
            const map = {
                'basic': '基础',
                'intermediate': '进阶',
                'advanced': '高级'
            };
            return map[difficulty] || '未知';
        },

        getStatusText(status) {
            const map = {
                'new': '未开始',
                'learning': '学习中',
                'mastered': '已掌握'
            };
            return map[status] || '未知';
        }
    }
}
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

.difficulty-badge {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
    font-size: 22rpx;
}

.difficulty-badge.basic {
    background-color: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1rpx solid rgba(76, 175, 80, 0.3);
}

.difficulty-badge.intermediate {
    background-color: rgba(255, 152, 0, 0.2);
    color: #ff9800;
    border: 1rpx solid rgba(255, 152, 0, 0.3);
}

.difficulty-badge.advanced {
    background-color: rgba(244, 67, 54, 0.2);
    color: #f44336;
    border: 1rpx solid rgba(244, 67, 54, 0.3);
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

.skill-progress {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.progress-circle {
    width: 80rpx;
    height: 80rpx;
    border-radius: 50%;
    border: 4rpx solid rgba(255, 255, 255, 0.3);
    border-top-color: #4caf50;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: rotate 2s linear infinite;
}

@keyframes rotate {
    to {
        transform: rotate(360deg);
    }
}

.progress-text {
    font-size: 20rpx;
    font-weight: bold;
}

.skill-status {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;
}

.status-icon {
    font-size: 32rpx;
}

.status-text {
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

.scenario-difficulty {
    font-size: 22rpx;
    color: #667eea;
    background-color: #f0f4ff;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
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

.related-skill-status {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
    font-size: 22rpx;
}

.related-skill-status.new {
    background-color: #f0f0f0;
    color: #666;
}

.related-skill-status.learning {
    background-color: #fff3e0;
    color: #ff9800;
}

.related-skill-status.mastered {
    background-color: #e8f5e8;
    color: #4caf50;
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
    gap: 16rpx;
}

.action-btn {
    flex: 1;
    padding: 24rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 28rpx;
    font-weight: bold;
    transition: all 0.2s ease;
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