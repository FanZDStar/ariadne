<template>
    <view class="category-detail-container">
        <view class="header">
            <view class="category-info">
                <text class="category-icon">{{ categoryData.icon }}</text>
                <view class="category-text">
                    <text class="category-name">{{ categoryData.name }}</text>
                    <text class="category-desc">{{ categoryData.description }}</text>
                </view>
            </view>
        </view>

        <view class="content">
            <view v-if="recommendedSkills.length > 0" class="section">
                <view class="section-header">
                    <text class="section-title">🎯 为你推荐</text>
                </view>
                <view v-for="skill in recommendedSkills" :key="skill.id" class="skill-card recommended">
                    <view class="skill-header">
                        <text class="skill-title">{{ skill.name }}</text>
                        <view class="difficulty-badge" :class="skill.difficulty">
                            <text class="difficulty-text">{{ getDifficultyText(skill.difficulty) }}</text>
                        </view>
                    </view>
                    <text class="skill-description">{{ skill.description }}</text>
                    <view class="skill-meta">
                        <view class="meta-item">
                            <text class="meta-icon">⏱️</text>
                            <text class="meta-text">{{ skill.estimatedTime }}分钟</text>
                        </view>
                    </view>
                    <view class="skill-actions">
                        <view class="action-btn primary" @click.stop="viewSkillDetail(skill)">
                            <text class="btn-text">开始学习</text>
                        </view>
                        <view class="action-btn secondary" @click.stop="addToFavorites(skill)">
                            <text class="btn-text">收藏</text>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 技能列表 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">📚 全部技能</text>
                </view>

                <view class="skills-grid">
                    <view v-for="skill in filteredSkills" :key="skill.id" class="skill-card"
                        :class="{ mastered: skill.status === 'mastered', learning: skill.status === 'learning' }"
                        @click="viewSkillDetail(skill)">

                        <text class="skill-name">{{ skill.name }}</text>
                        <text class="skill-brief">{{ skill.brief }}</text>

                        <view class="skill-tags">
                            <text v-for="tag in skill.tags" :key="tag" class="skill-tag">{{ tag }}</text>
                        </view>

                        <view class="skill-footer">
                            <view class="difficulty-indicator" :class="skill.difficulty">
                                <text class="difficulty-dot">●</text>
                                <text class="difficulty-label">{{ getDifficultyText(skill.difficulty) }}</text>
                            </view>
                        </view>
                    </view>
                </view>
            </view>

            <!-- 学习建议 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">💡 学习建议</text>
                    <view class="tip-controls">
                        <view class="refresh-btn" @click="refreshTip">
                            <text class="refresh-icon">🔄</text>
                        </view>
                    </view>
                </view>
                <view class="suggestion-card">
                    <text class="suggestion-title">{{ learningTip.title }}</text>
                    <text class="suggestion-content">{{ learningTip.content }}</text>
                </view>
            </view>
        </view>

        <BackToTop ref="backToTop" :threshold="50" :bottom="40" :right="40" icon="🔝"
            @scroll-to-top-success="onScrollToTopSuccess" />
    </view>
</template>

<script>
import BackToTop from '@/components/BackToTop.vue'
export default {
    components: {
        BackToTop
    },
    data() {
        return {
            categoryId: '',
            categoryName: '',
            categoryData: {},
            allSkills: [],
            recommendedSkills: [],
            filterType: 'all',
            learningTip: {},
            learningTips: [], // 存储所有学习建议
            currentTipIndex: 0, // 当前显示的建议索引
            tipTimer: null // 定时器
        }
    },

    computed: {
        progressPercentage() {
            if (this.categoryData.totalSkills === 0) return 0;
            return Math.round((this.categoryData.masteredSkills / this.categoryData.totalSkills) * 100);
        },

        filteredSkills() {
            switch (this.filterType) {
                case 'learned':
                    return this.allSkills.filter(skill => skill.status === 'mastered');
                case 'learning':
                    return this.allSkills.filter(skill => skill.status === 'learning');
                default:
                    return this.allSkills;
            }
        }
    },

    onLoad(options) {
        this.categoryId = options.categoryId;
        this.categoryName = options.name || '';
        this.loadCategoryData();
    },

    onUnload() {
        // 页面卸载时清除定时器
        this.clearTipTimer();
    },
    // 监听页面滚动
    onPageScroll(e) {
        // 更新返回顶部按钮的显示状态
        if (this.$refs.backToTop) {
            this.$refs.backToTop.updateShowState(e.scrollTop);
        }
    },
    methods: {
        // 返回顶部成功回调
        onScrollToTopSuccess() {
            uni.showToast({
                title: '已回到顶部',
                icon: 'success',
                duration: 1000
            });
        },
        async loadCategoryData() {
            try {
                uni.showLoading({ title: '加载中...' });

                // 模拟API调用
                await this.mockLoadCategoryData();

            } catch (error) {
                console.error('加载分类数据失败:', error);
                uni.showToast({
                    title: '加载失败',
                    icon: 'none'
                });
            } finally {
                uni.hideLoading();
            }
        },

        async mockLoadCategoryData() {
            // 根据不同的 categoryId 返回不同的分类数据
            const categoryDataMap = {
                'communication': {
                    id: this.categoryId,
                    name: '沟通表达',
                    description: '学会清晰、准确、有效的表达自己的想法和感受',
                    icon: '💬',
                    totalSkills: 12,
                    masteredSkills: 5,
                    skills: [
                        {
                            id: 1,
                            name: '主动倾听',
                            brief: '学会用心倾听对方的话语和情感',
                            description: '主动倾听是建立良好人际关系的基础技能，包括关注对方的言语和非言语信息。',
                            difficulty: 'basic',
                            estimatedTime: 15,
                            learnerCount: 1234,
                            status: 'mastered',
                            tags: ['倾听', '沟通基础'],
                            progress: 100
                        },
                        {
                            id: 2,
                            name: '情感表达',
                            brief: '准确表达自己的情感和需求',
                            description: '学会用"我"的句式表达情感，避免指责和批评。',
                            difficulty: 'intermediate',
                            estimatedTime: 20,
                            learnerCount: 956,
                            status: 'learning',
                            tags: ['情感', '表达'],
                            progress: 65
                        },
                        {
                            id: 3,
                            name: '非暴力沟通',
                            brief: '以善意和理解进行沟通',
                            description: '学习非暴力沟通的四个步骤：观察、感受、需要、请求。',
                            difficulty: 'advanced',
                            estimatedTime: 30,
                            learnerCount: 567,
                            status: 'new',
                            tags: ['沟通技巧', '冲突处理']
                        }
                    ],
                    learningTips: [
                        {
                            title: '循序渐进的学习方法',
                            content: '建议从基础技能开始学习，每天练习15-20分钟，结合实际场景应用，效果更佳。'
                        },
                        {
                            title: '倾听练习技巧',
                            content: '练习时关注对方的语调、语速变化，记住关键词汇，适时给予回应和反馈。'
                        },
                        {
                            title: '镜像练习法',
                            content: '对着镜子练习表达，观察自己的面部表情和肢体语言，提升非言语沟通能力。'
                        },
                        {
                            title: '情感词汇扩展',
                            content: '建立个人情感词汇库，学会用更精确的词语描述自己的感受和情绪状态。'
                        },
                        {
                            title: '日常对话记录',
                            content: '每天记录一次成功的沟通经历，分析什么因素让对话变得顺畅和有效。'
                        },
                        {
                            title: '5W1H提问法',
                            content: '学会使用谁、什么、何时、何地、为何、如何的提问方式，让沟通更加深入。'
                        },
                        {
                            title: '身体语言观察',
                            content: '观察他人的姿态、手势、眼神，练习从非言语信号中获取更多沟通信息。'
                        },
                        {
                            title: '换位思考训练',
                            content: '在每次对话后，尝试站在对方角度重新审视整个对话过程和自己的表现。'
                        },
                        {
                            title: '冲突处理步骤',
                            content: '面对分歧时：先冷静、再倾听、找共同点、提出解决方案、达成共识。'
                        },
                        {
                            title: '积极反馈技巧',
                            content: '使用"我注意到..."、"我欣赏..."的句式给予他人积极的反馈和认可。'
                        },
                        {
                            title: '沉默的力量',
                            content: '学会在对话中适当使用沉默，给对方思考和表达的时间和空间。'
                        },
                        {
                            title: '话题转换技巧',
                            content: '掌握自然过渡话题的方法："说到这个...""这让我想到...""顺便问一下..."'
                        },
                        {
                            title: '情绪调节预备',
                            content: '在重要对话前，先调节自己的情绪状态，保持开放和积极的心态。'
                        },
                        {
                            title: '文化敏感度培养',
                            content: '了解不同文化背景下的沟通习惯，提升跨文化交流的适应能力。'
                        },
                        {
                            title: '反思日志习惯',
                            content: '每周写一次沟通反思日志，记录进步、挑战和下周的改进目标。'
                        },
                        {
                            title: '实践环境创造',
                            content: '主动寻找或创造沟通练习的机会，如参与讨论、志愿服务等活动。'
                        }
                    ]
                },
                'emotional_expression': {
                    id: this.categoryId,
                    name: '情感理解',
                    description: '理解自己和他人的情感，提升情感智慧',
                    icon: '💝',
                    totalSkills: 10,
                    masteredSkills: 3,
                    skills: [
                        {
                            id: 4,
                            name: '情绪识别',
                            brief: '准确识别自己和他人的情绪状态',
                            description: '通过观察面部表情、语调、肢体语言等识别情绪。',
                            difficulty: 'basic',
                            estimatedTime: 12,
                            learnerCount: 890,
                            status: 'mastered',
                            tags: ['情绪识别', '观察力'],
                            progress: 100
                        },
                        {
                            id: 5,
                            name: '情感共鸣',
                            brief: '与他人产生情感共鸣和理解',
                            description: '学会站在对方角度思考，理解对方的感受。',
                            difficulty: 'intermediate',
                            estimatedTime: 25,
                            learnerCount: 675,
                            status: 'learning',
                            tags: ['共情', '理解'],
                            progress: 40
                        },
                        {
                            id: 6,
                            name: '情绪调节',
                            brief: '有效管理和调节自己的情绪',
                            description: '掌握深呼吸、认知重构等情绪调节技巧。',
                            difficulty: 'advanced',
                            estimatedTime: 35,
                            learnerCount: 445,
                            status: 'new',
                            tags: ['情绪管理', '自我调节']
                        }
                    ],
                    learningTips: [
                        {
                            title: '情感智慧提升要点',
                            content: '多观察自己的情绪变化，练习表达感受而非情绪，培养换位思考的习惯。'
                        },
                        {
                            title: '情绪日记记录法',
                            content: '每天记录3-5个情绪瞬间，包括触发事件、情绪名称、身体感受和应对方式。'
                        },
                        {
                            title: '情绪轮盘工具',
                            content: '使用情绪轮盘识别具体情感，从"生气"细分为"恼怒""愤怒""烦躁"等。'
                        },
                        {
                            title: '身体扫描技巧',
                            content: '定期进行身体情绪扫描，注意紧张、疼痛等身体信号传达的情绪信息。'
                        },
                        {
                            title: '呼吸调节练习',
                            content: '掌握4-7-8呼吸法：吸气4秒，屏息7秒，呼气8秒，有效调节情绪状态。'
                        },
                        {
                            title: '情感验证练习',
                            content: '对自己说："我现在感到...这很正常"，学会接纳而非判断自己的情感。'
                        },
                        {
                            title: '共情地图绘制',
                            content: '观察他人时绘制共情地图：他们说什么、做什么、想什么、感受什么。'
                        },
                        {
                            title: '情绪粒度训练',
                            content: '扩大情绪词汇量，学会区分"失望""沮丧""绝望"等细微情感差别。'
                        },
                        {
                            title: '触发点识别',
                            content: '记录个人情绪触发模式，识别哪些情况容易让自己产生强烈情绪反应。'
                        },
                        {
                            title: '正念观察法',
                            content: '如观察云朵般观察情绪的来去，不评判、不抓取、不推拒，只是觉察。'
                        },
                        {
                            title: '情感表达升级',
                            content: '从"我很累"升级为"我感到身心俱疲，需要一些休息和支持"。'
                        },
                        {
                            title: '他人情绪镜像',
                            content: '观察他人时，想象如果自己处于同样情境会有什么感受，提升共情能力。'
                        },
                        {
                            title: '情绪调色板',
                            content: '为不同情绪分配颜色，用视觉化方式理解和表达复杂的情感状态。'
                        },
                        {
                            title: '价值观情感链接',
                            content: '思考强烈情绪背后触及了哪些核心价值观，理解情感的深层意义。'
                        },
                        {
                            title: '情感支持网络',
                            content: '建立情感支持系统，识别在不同情况下能提供情感理解的人群。'
                        },
                        {
                            title: '元情绪认知',
                            content: '观察自己对情绪的情绪：对愤怒感到羞耻、对悲伤感到恐惧等二级情绪。'
                        }
                    ]
                },
                'relationship_building': {
                    id: this.categoryId,
                    name: '关系建立',
                    description: '建立和维护健康、积极的人际关系',
                    icon: '🤝',
                    totalSkills: 8,
                    masteredSkills: 2,
                    skills: [
                        {
                            id: 7,
                            name: '破冰技巧',
                            brief: '在新环境中快速与他人建立联系',
                            description: '掌握开场白、话题引导等社交技巧。',
                            difficulty: 'basic',
                            estimatedTime: 18,
                            learnerCount: 1123,
                            status: 'mastered',
                            tags: ['破冰', '社交'],
                            progress: 100
                        },
                        {
                            id: 8,
                            name: '信任建立',
                            brief: '在关系中建立互相信任的基础',
                            description: '通过真诚、一致性、可靠性建立信任关系。',
                            difficulty: 'intermediate',
                            estimatedTime: 28,
                            learnerCount: 789,
                            status: 'learning',
                            tags: ['信任', '关系维护'],
                            progress: 55
                        },
                        {
                            id: 9,
                            name: '冲突解决',
                            brief: '有效处理人际冲突和分歧',
                            description: '学会协商、妥协、寻找双赢解决方案。',
                            difficulty: 'advanced',
                            estimatedTime: 40,
                            learnerCount: 234,
                            status: 'new',
                            tags: ['冲突处理', '协商']
                        }
                    ],
                    learningTips: [
                        {
                            title: '关系建立核心原则',
                            content: '真诚是最好的社交技巧，保持一致性和可靠性，学会给予和接受。'
                        },
                        {
                            title: '首次印象优化',
                            content: '保持微笑、主动问候、记住对方名字、展现真诚兴趣，为关系打下良好基础。'
                        },
                        {
                            title: '共同点发掘法',
                            content: '主动寻找共同兴趣、经历或价值观，建立连接的桥梁和对话基础。'
                        },
                        {
                            title: '渐进式信任建立',
                            content: '从小事开始兑现承诺，逐步建立可靠形象，让信任在互动中自然增长。'
                        },
                        {
                            title: '积极关注技巧',
                            content: '记住对方提到的重要事情，下次见面时主动询问，显示你的关心和重视。'
                        },
                        {
                            title: '边界意识培养',
                            content: '学会在亲密和独立之间找平衡，尊重彼此的个人空间和隐私需求。'
                        },
                        {
                            title: '冲突预防策略',
                            content: '及时沟通不适感受，避免小问题积累成大矛盾，保持关系的健康状态。'
                        },
                        {
                            title: '感恩表达习惯',
                            content: '定期表达感谢和欣赏，让对方感受到在关系中的价值和重要性。'
                        },
                        {
                            title: '关系投资理念',
                            content: '像投资一样经营关系：定期投入时间、精力和关注，期待长期回报。'
                        },
                        {
                            title: '支持网络构建',
                            content: '主动为他人提供帮助和支持，同时学会在需要时寻求帮助。'
                        },
                        {
                            title: '关系深度分层',
                            content: '识别不同层次的关系需求，从点头之交到深度友谊的不同维护方式。'
                        },
                        {
                            title: '互惠原则应用',
                            content: '在关系中保持给予和接受的平衡，避免单方面付出或接受的失衡。'
                        },
                        {
                            title: '关系修复技能',
                            content: '学会在关系受损时主动修复：承认错误、表达歉意、制定改进计划。'
                        },
                        {
                            title: '社交能量管理',
                            content: '了解自己的社交能量模式，在精力充沛时投入重要关系的建设。'
                        },
                        {
                            title: '关系质量评估',
                            content: '定期评估关系的健康度：是否平等、支持、成长、带来正能量。'
                        },
                        {
                            title: '长期承诺意识',
                            content: '将关系视为长期承诺，在困难时选择坚持和努力而非轻易放弃。'
                        }
                    ]
                },
                'special_scenarios': {
                    id: this.categoryId,
                    name: '特殊情境',
                    description: '应对特殊场合和复杂人际情境',
                    icon: '🎯',
                    totalSkills: 15,
                    masteredSkills: 1,
                    skills: [
                        {
                            id: 10,
                            name: '职场沟通',
                            brief: '在职场环境中有效沟通',
                            description: '掌握正式场合的沟通技巧和职场礼仪。',
                            difficulty: 'intermediate',
                            estimatedTime: 22,
                            learnerCount: 1567,
                            status: 'mastered',
                            tags: ['职场', '正式沟通'],
                            progress: 100
                        },
                        {
                            id: 11,
                            name: '异地恋维护',
                            brief: '维护异地恋关系的特殊技巧',
                            description: '学会通过技术手段保持亲密度和信任。',
                            difficulty: 'advanced',
                            estimatedTime: 45,
                            learnerCount: 456,
                            status: 'learning',
                            tags: ['异地恋', '关系维护'],
                            progress: 30
                        },
                        {
                            id: 12,
                            name: '危机干预',
                            brief: '在他人遇到情感危机时提供支持',
                            description: '学会识别危机信号，提供适当的支持和帮助。',
                            difficulty: 'advanced',
                            estimatedTime: 50,
                            learnerCount: 123,
                            status: 'new',
                            tags: ['危机干预', '支持技巧']
                        }
                    ],
                    learningTips: [
                        {
                            title: '特殊情境应对策略',
                            content: '每种情境都有其特殊性，重要的是保持灵活性和适应性，必要时寻求专业帮助。'
                        },
                        {
                            title: '职场层级沟通',
                            content: '向上沟通简明扼要，平级沟通协作共赢，向下沟通耐心指导，建立良好职场关系。'
                        },
                        {
                            title: '跨文化敏感度',
                            content: '了解不同文化的沟通方式、价值观差异，避免文化误解，增进国际交流效果。'
                        },
                        {
                            title: '数字化沟通礼仪',
                            content: '掌握邮件、即时消息、视频会议的沟通规范，在线上也保持专业和礼貌。'
                        },
                        {
                            title: '危机沟通管理',
                            content: '在突发情况下保持冷静，先倾听理解，再提供支持，必要时引导寻求专业帮助。'
                        },
                        {
                            title: '代际沟通桥梁',
                            content: '理解不同年龄群体的沟通特点，找到共同语言，促进跨代理解和协作。'
                        },
                        {
                            title: '远程关系维护',
                            content: '通过定期视频通话、共同活动、创意表达等方式，克服距离障碍维护亲密关系。'
                        },
                        {
                            title: '高压环境沟通',
                            content: '在紧张、竞争环境中保持专业性，控制情绪，以事实和数据为基础进行沟通。'
                        },
                        {
                            title: '群体动力学应用',
                            content: '在团队或群体中识别不同角色，学会引导讨论、化解分歧、促进共识达成。'
                        },
                        {
                            title: '敏感话题处理',
                            content: '面对争议性话题时保持中性立场，引导理性讨论，避免激化矛盾。'
                        },
                        {
                            title: '权力差异平衡',
                            content: '在上下级关系中找到权力平衡点，既维护权威又保持人文关怀。'
                        },
                        {
                            title: '多元化团队协调',
                            content: '在多元化环境中发挥每个人的优势，创造包容性的沟通氛围。'
                        },
                        {
                            title: '压力下的情绪管理',
                            content: '在高压情境下识别和管理自己的情绪反应，保持理性决策能力。'
                        },
                        {
                            title: '复杂利益协调',
                            content: '在多方利益冲突中寻找平衡点，通过沟通找到各方都能接受的解决方案。'
                        },
                        {
                            title: '创伤知情沟通',
                            content: '识别他人可能的创伤背景，采用安全、支持性的沟通方式，避免二次伤害。'
                        },
                        {
                            title: '紧急情况指挥',
                            content: '在紧急情况下快速建立指挥体系，清晰传达指令，协调各方资源。'
                        }
                    ]
                }
            };

            // 根据 categoryId 获取对应数据，如果没有匹配则使用默认数据
            const categoryData = categoryDataMap[this.categoryId] || categoryDataMap['communication'];

            this.categoryData = {
                id: categoryData.id,
                name: categoryData.name,
                description: categoryData.description,
                icon: categoryData.icon,
                totalSkills: categoryData.totalSkills,
                masteredSkills: categoryData.masteredSkills
            };

            this.allSkills = categoryData.skills;
            this.recommendedSkills = this.allSkills.filter(skill => skill.status === 'new').slice(0, 2);
            this.learningTips = categoryData.learningTips || [];

            // 随机选择一个学习建议
            this.learningTip = this.getRandomTip();

            // 开始定时器
            this.startTipTimer();
        },

        setFilter(type) {
            this.filterType = type;
        },

        viewSkillDetail(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-detail?skillId=${skill.id}&categoryId=${this.categoryId}`
            });
        },

        startLearning(skill) {
            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?skillId=${skill.id}&type=learning`
            });
        },

        addToFavorites(skill) {
            uni.showToast({
                title: '已添加到收藏',
                icon: 'success'
            });
        },

        followSuggestion() {
            uni.navigateTo({
                url: '/pages/interpersonal-wisdom/learning-assistant'
            });
        },

        showLearningPlan() {
            uni.showModal({
                title: '制定学习计划',
                content: `为"${this.categoryData.name}"制定个性化学习计划？\n\n系统将根据你的水平和目标推荐最适合的学习路径。`,
                confirmText: '开始制定',
                success: (res) => {
                    if (res.confirm) {
                        uni.navigateTo({
                            url: `/pages/interpersonal-wisdom/learning-path?categoryId=${this.categoryId}&action=create`
                        });
                    }
                }
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

        // 随机选择一个学习建议
        getRandomTip() {
            if (this.learningTips.length === 0) return {};
            const randomIndex = Math.floor(Math.random() * this.learningTips.length);
            this.currentTipIndex = randomIndex;
            return this.learningTips[randomIndex];
        },

        // 开始定时器
        startTipTimer() {
            this.clearTipTimer(); // 先清除可能存在的定时器
            this.tipTimer = setInterval(() => {
                this.learningTip = this.getRandomTip();
            }, 30000); // 30秒更换一次
        },

        // 清除定时器
        clearTipTimer() {
            if (this.tipTimer) {
                clearInterval(this.tipTimer);
                this.tipTimer = null;
            }
        },

        // 手动刷新建议
        refreshTip() {
            this.learningTip = this.getRandomTip();
            uni.showToast({
                title: '已刷新建议',
                icon: 'success',
                duration: 1000
            });
        }
    }
}
</script>

<style scoped>
.category-detail-container {
    background-color: #f5f5f5;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40rpx;
    color: white;
}

.category-info {
    display: flex;
    align-items: center;
    margin-bottom: 32rpx;
}

.category-icon {
    font-size: 64rpx;
    margin-right: 24rpx;
}

.category-text {
    flex: 1;
}

.category-name {
    font-size: 42rpx;
    font-weight: bold;
    display: block;
    margin-bottom: 8rpx;
}

.category-desc {
    font-size: 26rpx;
    opacity: 0.9;
    line-height: 1.4;
}


.content {
    padding: 0 40rpx 120rpx;
}

.section {
    margin-bottom: 48rpx;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
    padding-top: 24rpx;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.tip-controls {
    display: flex;
    align-items: center;
    gap: 16rpx;
}

.tip-counter {
    font-size: 22rpx;
    color: #999;
    background-color: #f0f0f0;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
}

.refresh-btn {
    padding: 8rpx;
    background-color: #667eea;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
}

.refresh-btn:active {
    transform: scale(0.95);
}

.refresh-icon {
    font-size: 20rpx;
    color: white;
}

.section-subtitle {
    font-size: 24rpx;
    color: #666;
    margin-top: 4rpx;
}

.filter-controls {
    display: flex;
    gap: 12rpx;
}

.filter-btn {
    padding: 12rpx 20rpx;
    background-color: #f0f0f0;
    border-radius: 20rpx;
    font-size: 24rpx;
    color: #666;
    transition: all 0.3s ease;
}

.filter-btn.active {
    background-color: #667eea;
    color: white;
}

.skill-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    position: relative;
    transition: transform 0.2s ease;
}

.skill-card:active {
    transform: translateY(2rpx);
}

.skill-card.recommended {
    border: 2rpx solid #667eea;
    background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
}

.skill-card.mastered {
    border-left: 6rpx solid #4caf50;
}

.skill-card.learning {
    border-left: 6rpx solid #ff9800;
}

.skill-status-indicator {
    position: absolute;
    top: 16rpx;
    right: 16rpx;
}

.status-icon {
    font-size: 24rpx;
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.skill-title,
.skill-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
}

.skill-description,
.skill-brief {
    font-size: 26rpx;
    color: #666;
    line-height: 1.5;
    margin-bottom: 20rpx;
}

.difficulty-badge {
    padding: 8rpx 16rpx;
    border-radius: 12rpx;
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

.skill-meta {
    display: flex;
    gap: 24rpx;
    margin-bottom: 24rpx;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
}

.meta-icon {
    font-size: 20rpx;
}

.meta-text {
    font-size: 22rpx;
    color: #999;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    margin-bottom: 24rpx;
}

.skill-tag {
    background-color: #f0f0f0;
    color: #666;
    padding: 6rpx 12rpx;
    border-radius: 12rpx;
    font-size: 20rpx;
}

.skill-actions {
    display: flex;
    gap: 16rpx;
}

.action-btn {
    flex: 1;
    padding: 20rpx;
    border-radius: 12rpx;
    text-align: center;
    font-size: 26rpx;
}

.action-btn.primary {
    background-color: #667eea;
    color: white;
}

.action-btn.secondary {
    background-color: #f0f0f0;
    color: #666;
}

.skill-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.difficulty-indicator {
    display: flex;
    align-items: center;
    gap: 8rpx;
    font-size: 22rpx;
}

.difficulty-indicator.basic {
    color: #4caf50;
}

.difficulty-indicator.intermediate {
    color: #ff9800;
}

.difficulty-indicator.advanced {
    color: #f44336;
}

.difficulty-dot {
    font-size: 16rpx;
}

.learning-progress {
    font-size: 22rpx;
    color: #667eea;
    font-weight: bold;
}

.skills-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20rpx;
}

.suggestion-card {
    background-color: white;
    border-radius: 16rpx;
    padding: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.suggestion-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
    display: block;
}

.suggestion-content {
    font-size: 26rpx;
    color: #666;
    line-height: 1.6;
    margin-bottom: 24rpx;
}

.suggestion-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20rpx;
}

.auto-refresh-hint {
    font-size: 20rpx;
    color: #999;
}

.suggestion-action {
    display: flex;
    align-items: center;
    gap: 8rpx;
    color: #667eea;
    cursor: pointer;
}

.action-text {
    font-size: 26rpx;
}

.action-arrow {
    font-size: 24rpx;
}


@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-8rpx);
    }
}

/* 响应式设计 */
@media (min-width: 750rpx) {
    .skills-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>