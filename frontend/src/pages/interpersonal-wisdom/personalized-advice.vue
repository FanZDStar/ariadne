<template>
    <view class="advice-container">        <!-- 用户情况收集 -->
        <view v-if="currentStep === 'input'" class="input-section">
            <view class="form-card">
                <text class="form-title">请描述你的情况</text>
                <text class="form-subtitle">为了给出更精准的建议，请简单描述一下你目前遇到的问题</text>

                <view class="form-item">
                    <text class="form-label">当前情况描述</text>
                    <textarea v-model="formData.situation" class="form-textarea"
                        placeholder="例如：最近和朋友相处时总是感觉很尴尬，不知道该聊什么..." maxlength="500"></textarea>
                    <text class="char-count">{{ formData.situation.length }}/500</text>
                </view>

                <view class="form-item">
                    <text class="form-label">关系类型</text>
                    <view class="relation-types">
                        <view v-for="type in relationTypes" :key="type.id" class="type-chip"
                            :class="{ active: formData.relationType === type.id }" @click="selectRelationType(type.id)">
                            <text class="type-icon">{{ type.icon }}</text>
                            <text class="type-name">{{ type.name }}</text>
                        </view>
                    </view>
                </view>

                <view class="form-item">
                    <text class="form-label">情感状态</text>
                    <view class="emotion-slider">
                        <view class="emotion-labels">
                            <text class="emotion-label">焦虑</text>
                            <text class="emotion-label">平静</text>
                            <text class="emotion-label">开心</text>
                        </view>
                        <slider v-model="formData.emotionLevel" min="1" max="5" step="1" show-value
                            activeColor="#87ceeb" backgroundColor="#f0f8ff" @change="handleEmotionChange" />
                    </view>
                </view>

                <view class="form-item">
                    <text class="form-label">具体担忧</text>
                    <textarea v-model="formData.concerns" class="form-textarea small"
                        placeholder="你最担心的是什么？例如：害怕被拒绝、不知道如何开口..." maxlength="200"></textarea>
                    <text class="char-count">{{ formData.concerns.length }}/200</text>
                </view>

                <view class="form-item">
                    <text class="form-label">紧急程度</text>
                    <view class="urgency-options">
                        <view v-for="urgency in urgencyLevels" :key="urgency.id" class="urgency-item"
                            :class="{ selected: formData.urgency === urgency.id }" @click="selectUrgency(urgency.id)">
                            <text class="urgency-icon">{{ urgency.icon }}</text>
                            <text class="urgency-name">{{ urgency.name }}</text>
                            <text class="urgency-desc">{{ urgency.desc }}</text>
                        </view>
                    </view>
                </view>
            </view>

            <view class="input-actions">
                <view class="submit-btn" :class="{ disabled: !canSubmit }" @click="submitAdviceRequest">
                    <text class="btn-text">获取个性化建议</text>
                </view>
            </view>
        </view>

        <!-- 建议展示 -->
        <view v-if="currentStep === 'advice'" class="advice-section">
            <view class="advice-header">
                <text class="advice-title">为你定制的建议</text>
                <text class="advice-subtitle">基于你的情况，我们为你准备了以下建议</text>
            </view>

            <!-- 核心建议卡片 -->
            <view v-if="adviceResult.core_advice" class="core-advice">
                <view class="advice-card primary">
                    <view class="card-header">
                        <text class="card-icon"></text>
                        <text class="card-title">核心建议</text>
                    </view>
                    <text class="card-content">{{ adviceResult.core_advice }}</text>
                </view>
            </view>

            <!-- 具体行动建议 -->
            <view v-if="adviceResult.action_steps" class="action-steps">
                <text class="section-title">具体行动步骤</text>
                <view v-for="(step, index) in adviceResult.action_steps" :key="index" class="step-item">
                    <view class="step-number">{{ index + 1 }}</view>
                    <view class="step-content">
                        <text class="step-title">{{ step.title }}</text>
                        <text class="step-desc">{{ step.description }}</text>
                        <view v-if="step.tips" class="step-tips">
                            <text v-for="tip in step.tips" :key="tip" class="tip-item">• {{ tip }}</text>
                        </view>
                    </view>
                </view>
            </view>

            <!-- AI深度分析 -->
            <view v-if="adviceResult.ai_analysis" class="ai-analysis">
                <view class="analysis-card">
                    <view class="analysis-header">
                        <text class="analysis-icon"></text>
                        <text class="analysis-title">AI深度分析</text>
                    </view>
                    <text class="analysis-content">{{ adviceResult.ai_analysis }}</text>
                </view>
            </view>

            <!-- 推荐技巧 -->
            <view v-if="adviceResult.recommended_skills" class="recommended-skills">
                <text class="section-title">推荐学习技巧</text>
                <view v-for="skill in adviceResult.recommended_skills" :key="skill.id" class="skill-recommendation"
                    @click="practiceSkill(skill)">
                    <view class="skill-info">
                        <text class="skill-name">{{ skill.title }}</text>
                        <text class="skill-reason">{{ skill.reason }}</text>
                    </view>
                    <view class="skill-action">
                        <text class="action-text">立即练习</text>
                        <text class="action-arrow">→</text>
                    </view>
                </view>
            </view>

            <!-- 情感支持 -->
            <view v-if="adviceResult.emotional_support" class="emotional-support">
                <view class="support-card">
                    <view class="support-header">
                        <text class="support-icon"></text>
                        <text class="support-title">情感支持</text>
                    </view>
                    <text class="support-content">{{ adviceResult.emotional_support }}</text>
                </view>
            </view>

            <!-- 行动按钮 -->
            <view class="advice-actions">
                <view class="action-btn secondary" @click="restartAdviceInput">
                    <text class="btn-text">重新咨询</text>
                </view>
                <view class="action-btn primary" @click="saveAdvice">
                    <text class="btn-text">保存建议</text>
                </view>
            </view>
        </view>

        <!-- 历史建议 -->
        <view v-if="currentStep === 'history'" class="history-section">
            <text class="history-title">历史建议记录</text>
            <view v-for="record in adviceHistory" :key="record.id" class="history-item"
                @click="viewHistoryAdvice(record)">
                <view class="history-header">
                    <text class="history-date">{{ formatDate(record.date) }}</text>
                    <view class="history-status" :class="record.status">
                        <text class="status-text">{{ getStatusText(record.status) }}</text>
                    </view>
                </view>
                <text class="history-situation">{{ record.situation.substring(0, 50) }}...</text>
                <text class="history-type">{{ getRelationTypeName(record.relationType) }}</text>
            </view>
        </view>

        <!-- 加载状态 -->
        <view v-if="isGenerating" class="loading-overlay">
            <view class="loading-content">
                <text class="loading-icon"></text>
                <text class="loading-text">AI正在为你生成个性化建议...</text>
                <text class="loading-subtext">分析你的情况并匹配最适合的解决方案</text>
                <view class="loading-progress">
                    <view class="progress-bar">
                        <view class="progress-fill" :style="{ width: loadingProgress + '%' }"></view>
                    </view>
                    <text class="progress-text">{{ loadingProgress }}%</text>
                </view>
            </view>
        </view>

        <!-- 底部导航 -->
        <view class="bottom-nav">
            <view class="nav-item" :class="{ active: currentStep === 'input' }" @click="currentStep = 'input'">
                <text class="nav-icon"></text>
                <text class="nav-text">咨询建议</text>
            </view>
            <view class="nav-item" :class="{ active: currentStep === 'history' }" @click="viewHistory">
                <text class="nav-icon"></text>
                <text class="nav-text">历史记录</text>
            </view>
        </view>
    </view>
</template>

<script>
import { getSkillById } from '@/data/skillsData.js';

export default {
    data() {
        return {
            currentStep: 'input', // input, advice, history
            isGenerating: false,
            loadingProgress: 0,
            formData: {
                situation: '',
                relationType: '',
                emotionLevel: 3,
                concerns: '',
                urgency: 'normal'
            },
            adviceResult: null,
            adviceHistory: [],
            relationTypes: [
                { id: 'romantic', name: '恋爱关系', icon: '' },
                { id: 'friendship', name: '友谊关系', icon: '' },
                { id: 'family', name: '家庭关系', icon: '' },
                { id: 'colleague', name: '同事关系', icon: '' },
                { id: 'roommate', name: '室友关系', icon: '' }
            ],
            urgencyLevels: [
                {
                    id: 'low',
                    name: '一般咨询',
                    desc: '想了解一些建议',
                    icon: ''
                },
                {
                    id: 'normal',
                    name: '需要帮助',
                    desc: '遇到了一些困难',
                    icon: ''
                },
                {
                    id: 'urgent',
                    name: '比较紧急',
                    desc: '情况让我很困扰',
                    icon: ''
                }
            ]
        }
    },

    computed: {
        canSubmit() {
            return this.formData.situation.trim().length > 10 &&
                this.formData.relationType &&
                this.formData.urgency;
        }
    },

    onLoad(options) {
        // 如果从评估页面跳转过来，预填充一些信息
        if (options.fromAssessment === 'true') {
            this.formData.situation = '刚完成了关系健康评估，希望获得更具体的改善建议';
            this.formData.urgency = 'normal';
        }

        this.loadAdviceHistory();
    },

    onShow() {
        // 检查星点奖励
        this.checkStarReward();
    },

    methods: {
        selectRelationType(typeId) {
            this.formData.relationType = typeId;
        },

        selectUrgency(urgencyId) {
            this.formData.urgency = urgencyId;
        },

        handleEmotionChange(e) {
            this.formData.emotionLevel = e.detail.value;
        },

        async submitAdviceRequest() {
            if (!this.canSubmit) {
                uni.showToast({
                    title: '请完善必要信息',
                    icon: 'none'
                });
                return;
            }

            this.isGenerating = true;
            this.loadingProgress = 0;

            // 模拟进度加载
            const progressInterval = setInterval(() => {
                this.loadingProgress += 10;
                if (this.loadingProgress >= 90) {
                    clearInterval(progressInterval);
                }
            }, 200);

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/emotional-protection/protection/personalized-advice`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('access_token')}`,
                        'Content-Type': 'application/json'
                    },
                    data: {
                        situation: this.formData.situation,
                        relationship_type: this.formData.relationType,
                        concerns: this.formData.concerns,
                        urgency: this.formData.urgency
                    }
                });

                this.loadingProgress = 100;

                if (response.statusCode === 200) {
                    this.adviceResult = this.parseAdviceResult(response.data.personalized_advice);
                    this.currentStep = 'advice';

                    // 检查星点奖励
                    if (response.data.star_reward && response.data.star_reward.is_rewarded) {
                        // 立即显示星点奖励Toast
                        setTimeout(() => {
                            uni.showToast({
                                title: response.data.star_reward.description,
                                icon: 'none',
                                duration: 2500
                            });
                        }, 500); // 延迟500ms显示，让加载完成
                    }

                    // 保存到历史记录
                    this.saveToHistory();

                    // 重置表单
                    this.resetForm();
                }
            } catch (error) {
                console.error('获取建议失败:', error);
                uni.showToast({
                    title: '获取建议失败，请重试',
                    icon: 'none'
                });
            } finally {
                this.isGenerating = false;
                clearInterval(progressInterval);
            }
        },

        parseAdviceResult(adviceText) {
            // 这里应该解析AI返回的文本，提取结构化信息
            // 简化示例，实际项目中可能需要更复杂的解析逻辑

            // 根据用户的关系类型和情况，智能推荐相关技能
            const recommendedSkills = this.getRecommendedSkillsBasedOnSituation();

            return {
                core_advice: "基于你的情况，建议你先从建立基本的沟通信心开始。",
                action_steps: [
                    {
                        title: "练习基础对话技巧",
                        description: "从简单的日常问候开始，逐步增加对话深度",
                        tips: ["保持眼神接触", "主动倾听对方", "适时提问"]
                    },
                    {
                        title: "创造合适的交流机会",
                        description: "选择舒适的环境和合适的时机进行交流",
                        tips: ["选择轻松的环境", "避免压力过大的场合"]
                    }
                ],
                ai_analysis: adviceText,
                recommended_skills: recommendedSkills,
                emotional_support: "记住，每个人在人际交往中都会遇到困难，这是成长的一部分。你已经迈出了寻求帮助的第一步，这很棒！"
            };
        },

        // 根据用户情况智能推荐技能
        getRecommendedSkillsBasedOnSituation() {
            const relationType = this.formData.relationType;
            const urgency = this.formData.urgency;
            const situation = this.formData.situation.toLowerCase();

            // 基础推荐技能池 - 每种关系只推荐一个最核心的技能
            let recommendedSkills = [];

            // 根据关系类型推荐最核心的一个技能
            if (relationType === 'romantic') {
                recommendedSkills.push(
                    { id: "romantic_expression", title: "情感智力提升", reason: "帮助你更好地理解和表达恋爱中的情感" }
                );
            } else if (relationType === 'friendship') {
                recommendedSkills.push(
                    { id: "listen_actively", title: "积极倾听技巧", reason: "友谊的基础是相互理解，倾听是第一步" }
                );
            } else if (relationType === 'family') {
                recommendedSkills.push(
                    { id: "topic_transition", title: "非暴力沟通", reason: "家庭沟通中避免冲突，和谐表达很重要" }
                );
            } else if (relationType === 'colleague') {
                recommendedSkills.push(
                    { id: "express_clearly", title: "建设性反馈", reason: "职场中需要给出和接受专业的反馈意见" }
                );
            } else if (relationType === 'roommate') {
                recommendedSkills.push(
                    { id: "boundary_setting", title: "边界设定技巧", reason: "室友关系需要明确的生活边界" }
                );
            }

            // 根据问题描述关键词优先推荐最相关的技能（覆盖基础推荐）
            if (situation.includes('尴尬') || situation.includes('不知道说什么')) {
                recommendedSkills = [
                    { id: "ice_breaking", title: "赞美与认可", reason: "学会开启和维持对话，减少尴尬" }
                ];
            } else if (situation.includes('倾听') || situation.includes('理解')) {
                recommendedSkills = [
                    { id: "listen_actively", title: "积极倾听技巧", reason: "针对你提到的倾听问题，这个技能最为重要" }
                ];
            } else if (situation.includes('冲突') || situation.includes('争吵') || situation.includes('分歧')) {
                recommendedSkills = [
                    { id: "conflict_resolution", title: "冲突解决策略", reason: "直接针对你遇到的冲突问题" }
                ];
            }

            // 如果没有特定推荐，使用通用推荐
            if (recommendedSkills.length === 0) {
                recommendedSkills = [
                    { id: "listen_actively", title: "积极倾听技巧", reason: "人际交往的基础，适用于所有关系类型" },
                    { id: "topic_transition", title: "非暴力沟通", reason: "学会和谐表达，减少误解和冲突" },
                    { id: "emotion_sharing", title: "共情能力培养", reason: "理解他人感受，建立更深层的连接" }
                ];
            }

            // 只推荐1个最相关的技能，避免选择困难和系统问题
            return recommendedSkills.slice(0, 1);
        },

        saveToHistory() {
            const record = {
                id: Date.now(),
                date: new Date(),
                situation: this.formData.situation,
                relationType: this.formData.relationType,
                urgency: this.formData.urgency,
                advice: this.adviceResult,
                status: 'new'
            };

            this.adviceHistory.unshift(record);
            uni.setStorageSync('adviceHistory', this.adviceHistory);
        },

        loadAdviceHistory() {
            const history = uni.getStorageSync('adviceHistory') || [];
            this.adviceHistory = history;
        },

        restartAdviceInput() {
            this.currentStep = 'input';
            this.resetForm();
            this.adviceResult = null;
        },

        async saveAdvice() {
            uni.showToast({
                title: '建议已保存',
                icon: 'success'
            });

            // 更新历史记录状态
            if (this.adviceHistory.length > 0) {
                this.adviceHistory[0].status = 'saved';
                uni.setStorageSync('adviceHistory', this.adviceHistory);
            }
        },

        practiceSkill(skill) {
            // 从统一数据源获取完整的技能信息
            const skillData = this.getSkillDataById(skill.id);

            if (!skillData) {
                uni.showToast({
                    title: '技能数据加载失败',
                    icon: 'none'
                });
                return;
            }

            // 构建完整的参数，参考 interpersonal-wisdom.vue 的实现
            const skillParams = {
                skillId: skill.id,
                type: "practice",
                skillTitle: encodeURIComponent(skillData.name || skillData.title),
                skillContent: encodeURIComponent(skillData.description || skillData.brief),
                skillTags: encodeURIComponent(JSON.stringify(skillData.tags || [])),
                skillScenarios: encodeURIComponent(JSON.stringify(skillData.practiceScenarios || skillData.scenarios || []))
            };

            const queryString = Object.entries(skillParams)
                .map(([key, value]) => `${key}=${value}`)
                .join("&");

            uni.navigateTo({
                url: `/pages/interpersonal-wisdom/skill-practice?${queryString}`
            });
        },

        // 根据技能ID获取完整技能数据的辅助方法
        getSkillDataById(skillId) {
            // 首先尝试从统一数据源获取
            const skillData = getSkillById(skillId);
            if (skillData) {
                return {
                    id: skillData.id,
                    name: skillData.name,
                    title: skillData.name,
                    description: skillData.description,
                    brief: skillData.brief,
                    tags: skillData.tags || [],
                    scenarios: skillData.scenarios || [],
                    practiceScenarios: skillData.practiceScenarios || []
                };
            }

            // 如果统一数据源没有，使用技能ID映射表作为后备
            const skillMappings = {
                "listen_actively": {
                    id: 1,
                    name: "积极倾听技巧",
                    title: "积极倾听技巧",
                    description: "学习如何专注、理解并回应他人的话语，建立更深层的连接",
                    brief: "学会用心倾听对方的话语和情感",
                    tags: ["沟通", "倾听", "理解"],
                    scenarios: ["日常对话", "深度交流", "冲突解决"],
                    practiceScenarios: [
                        { title: "朋友倾诉烦恼", description: "朋友向你倾诉工作上的困扰" },
                        { title: "家人分享心情", description: "家人跟你分享今天发生的事情" }
                    ]
                },
                "topic_transition": {
                    id: 2,
                    name: "非暴力沟通",
                    title: "非暴力沟通",
                    description: "用非批判性的方式表达需求和感受，减少冲突",
                    brief: "以和谐的方式表达需求和感受",
                    tags: ["沟通", "和谐", "表达"],
                    scenarios: ["意见分歧", "需求表达", "冲突解决"],
                    practiceScenarios: [
                        { title: "工作意见分歧", description: "与同事在项目方向上有不同看法" },
                        { title: "家庭沟通", description: "与家人就某个问题进行讨论" }
                    ]
                },
                "emotion_sharing": {
                    id: 5,
                    name: "共情能力培养",
                    title: "共情能力培养",
                    description: "理解和感受他人情感，增进人际关系的深度",
                    brief: "提升理解他人情感的能力",
                    tags: ["理解", "情感", "连接"],
                    scenarios: ["情感支持", "关系深化", "人际理解"],
                    practiceScenarios: [
                        { title: "安慰伤心朋友", description: "朋友失恋了，需要你的理解和支持" },
                        { title: "理解他人压力", description: "感受并理解他人面临的压力" }
                    ]
                },
                "express_clearly": {
                    id: 2,
                    name: "建设性反馈",
                    title: "建设性反馈",
                    description: "以支持性的方式提供反馈，促进他人成长",
                    brief: "学会给出有效的建设性意见",
                    tags: ["反馈", "成长", "支持"],
                    scenarios: ["工作反馈", "学习指导", "关系改善"],
                    practiceScenarios: [
                        { title: "给下属反馈", description: "为团队成员的工作表现提供建设性意见" },
                        { title: "朋友建议", description: "朋友请你对他的某个决定给出意见" }
                    ]
                },
                "conflict_resolution": {
                    id: 4,
                    name: "冲突解决策略",
                    title: "冲突解决策略",
                    description: "有效处理分歧和冲突，寻找双赢解决方案",
                    brief: "学会妥善处理人际冲突",
                    tags: ["冲突", "解决", "合作"],
                    scenarios: ["工作争议", "朋友矛盾", "家庭分歧"],
                    practiceScenarios: [
                        { title: "同事间争议", description: "两个同事因为工作分配产生矛盾" },
                        { title: "朋友误会", description: "朋友对你的某个行为产生了误解" }
                    ]
                },
                "romantic_expression": {
                    id: 27,
                    name: "情感智力提升",
                    title: "情感智力提升",
                    description: "识别、理解和管理自己及他人的情感",
                    brief: "提升情感认知和管理能力",
                    tags: ["情感", "智力", "管理"],
                    scenarios: ["情感表达", "情绪管理", "关系维护"],
                    practiceScenarios: [
                        { title: "情绪管理", description: "在压力情况下管理自己的情绪反应" },
                        { title: "情感表达", description: "向重要的人表达你的真实感受" }
                    ]
                },
                "boundary_setting": {
                    id: 6,
                    name: "边界设定技巧",
                    title: "边界设定技巧",
                    description: "在关系中建立健康的边界，保护自己的情感安全",
                    brief: "学会在关系中设定合理边界",
                    tags: ["边界", "保护", "安全"],
                    scenarios: ["关系边界", "个人空间", "情感保护"],
                    practiceScenarios: [
                        { title: "拒绝过分要求", description: "朋友提出了让你感到不舒服的要求" },
                        { title: "维护个人时间", description: "同事总是在下班时间找你处理工作" }
                    ]
                },
                "sincere_gratitude": {
                    id: 12,
                    name: "有效道歉方式",
                    title: "有效道歉方式",
                    description: "真诚地承认错误并修复关系裂痕",
                    brief: "学会真诚有效地道歉",
                    tags: ["道歉", "修复", "真诚"],
                    scenarios: ["错误承认", "关系修复", "信任重建"],
                    practiceScenarios: [
                        { title: "工作失误道歉", description: "因为你的疏忽导致项目出现问题" },
                        { title: "朋友关系修复", description: "因为误解伤害了朋友的感情" }
                    ]
                },
                "ice_breaking": {
                    id: 7,
                    name: "赞美与认可",
                    title: "赞美与认可",
                    description: "恰当地表达欣赏和认可，增强他人的自信",
                    brief: "学会真诚地赞美和认可他人",
                    tags: ["赞美", "认可", "鼓励"],
                    scenarios: ["日常交流", "鼓励他人", "关系建立"],
                    practiceScenarios: [
                        { title: "赞美同事", description: "同事完成了一个出色的项目" },
                        { title: "鼓励朋友", description: "朋友在困难时期需要鼓励和认可" }
                    ]
                },
                "trust_building": {
                    id: 42,
                    name: "情感表达艺术",
                    title: "情感表达艺术",
                    description: "以恰当的方式表达情感，增进理解",
                    brief: "学会艺术化地表达情感",
                    tags: ["表达", "情感", "艺术"],
                    scenarios: ["情感分享", "深度交流", "关系深化"],
                    practiceScenarios: [
                        { title: "表达关心", description: "向朋友表达你对他的关心和在乎" },
                        { title: "分享喜悦", description: "与重要的人分享你的快乐和成就" }
                    ]
                }
            };

            return skillMappings[skillId] || null;
        },

        viewHistory() {
            this.currentStep = 'history';
            this.loadAdviceHistory();
        },

        viewHistoryAdvice(record) {
            this.adviceResult = record.advice;
            this.currentStep = 'advice';
        },

        formatDate(date) {
            return new Date(date).toLocaleDateString('zh-CN', {
                month: 'numeric',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        getStatusText(status) {
            const statusMap = {
                'new': '新建议',
                'saved': '已保存',
                'applied': '已应用'
            };
            return statusMap[status] || '未知';
        },

        getRelationTypeName(typeId) {
            const type = this.relationTypes.find(t => t.id === typeId);
            return type ? type.name : '未知';
        },

        checkStarReward() {
            // 检查是否有星星奖励信息
            const { storage } = require('@/utils/api.js');
            const starReward = storage.getStarReward();
            if (starReward && starReward.message) {
                // 显示星星奖励提示
                uni.showToast({
                    title: starReward.message,
                    icon: 'none',
                    duration: 2500
                });

                // 清除奖励信息，避免重复显示
                storage.clearStarReward();
            }
        },

        resetForm() {
            // 重置表单数据
            this.formData = {
                situation: '',
                relationType: '',
                emotionLevel: 3,
                concerns: '',
                urgency: 'normal'
            };
        }
    }
}
</script>

<style scoped>
.advice-container {
    padding: 0;
    background: linear-gradient(180deg, #f0f8ff 0%, #ffffff 100%);
    min-height: 100vh;
    padding-bottom: 160rpx;
    position: relative;
}

.advice-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 50% 0%, rgba(135, 206, 235, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

.input-section {
    padding: 40rpx;
}

.form-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 24rpx;
    padding: 40rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 8rpx 32rpx rgba(135, 206, 235, 0.15);
    border: 1rpx solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.form-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4rpx;
    background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
}

.form-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 12rpx;
    display: block;
}

.form-subtitle {
    font-size: 26rpx;
    color: #5a6c7d;
    margin-bottom: 32rpx;
}

.form-item {
    margin-bottom: 32rpx;
}

.form-label {
    font-size: 28rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 16rpx;
    display: block;
}

.form-textarea {
    width: 100%;
    min-height: 140rpx;
    padding: 24rpx;
    border: 2rpx solid #e6f3ff;
    border-radius: 16rpx;
    font-size: 28rpx;
    color: #2c3e50;
    background: rgba(255, 255, 255, 0.9);
    box-sizing: border-box;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    line-height: 1.6;
    resize: none;
}

.form-textarea:focus {
    border-color: #87ceeb;
    box-shadow: 0 0 0 6rpx rgba(135, 206, 235, 0.12);
    outline: none;
    background: #ffffff;
    transform: translateY(-2rpx);
}

.form-textarea::placeholder {
    color: #a0a9c0;
    font-size: 26rpx;
}

.form-textarea.small {
    min-height: 80rpx;
}

.char-count {
    font-size: 22rpx;
    color: #7f8c8d;
    text-align: right;
    margin-top: 8rpx;
    display: block;
}

.relation-types {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
}

.type-chip {
    display: flex;
    align-items: center;
    padding: 20rpx 28rpx;
    background: rgba(255, 255, 255, 0.8);
    border: 2rpx solid #e6f3ff;
    border-radius: 50rpx;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.type-chip::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(135, 206, 235, 0.1), transparent);
    transition: left 0.5s ease;
}

.type-chip:hover::before {
    left: 100%;
}

.type-chip.active {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-color: #87ceeb;
    color: #2c3e50;
    transform: translateY(-4rpx);
    box-shadow: 0 8rpx 20rpx rgba(135, 206, 235, 0.3);
}

.type-chip:active {
    transform: translateY(-2rpx) scale(0.98);
}

.type-icon {
    font-size: 24rpx;
    margin-right: 8rpx;
}

.type-name {
    font-size: 24rpx;
}

.emotion-slider {
    margin-top: 16rpx;
}

.emotion-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16rpx;
}

.emotion-label {
    font-size: 24rpx;
    color: #5a6c7d;
}

.urgency-options {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}

.urgency-item {
    display: flex;
    align-items: center;
    padding: 28rpx;
    background: rgba(255, 255, 255, 0.8);
    border: 2rpx solid #e6f3ff;
    border-radius: 16rpx;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.urgency-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(135, 206, 235, 0.08), transparent);
    transition: left 0.5s ease;
}

.urgency-item:hover::before {
    left: 100%;
}

.urgency-item:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 6rpx 20rpx rgba(135, 206, 235, 0.12);
}

.urgency-item.selected {
    background: rgba(240, 248, 255, 0.9);
    border-color: #87ceeb;
    transform: translateY(-4rpx);
    box-shadow: 0 8rpx 24rpx rgba(135, 206, 235, 0.2);
}

.urgency-item.selected::after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 6rpx;
    background: linear-gradient(180deg, #87ceeb 0%, #add8e6 100%);
}

.urgency-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.urgency-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-right: 16rpx;
}

.urgency-desc {
    font-size: 24rpx;
    color: #5a6c7d;
    flex: 1;
}

.input-actions {
    text-align: center;
}

.submit-btn {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    padding: 36rpx 100rpx;
    border-radius: 60rpx;
    font-size: 32rpx;
    font-weight: 600;
    display: inline-block;
    box-shadow: 0 8rpx 24rpx rgba(135, 206, 235, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.submit-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.submit-btn:hover::before {
    left: 100%;
}

.submit-btn:active {
    transform: translateY(2rpx) scale(0.98);
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.4);
}

.submit-btn.disabled {
    background: linear-gradient(135deg, #d4d4d8 0%, #a1a1aa 100%);
    color: #71717a;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    cursor: not-allowed;
}

.advice-section {
    padding: 40rpx;
}

.advice-header {
    text-align: center;
    margin-bottom: 40rpx;
}

.advice-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 12rpx;
    display: block;
}

.advice-subtitle {
    font-size: 26rpx;
    color: #5a6c7d;
}

.advice-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 24rpx;
    padding: 40rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 8rpx 32rpx rgba(135, 206, 235, 0.12);
    border: 1rpx solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.advice-card:hover {
    transform: translateY(-4rpx);
    box-shadow: 0 12rpx 40rpx rgba(135, 206, 235, 0.18);
}

.advice-card.primary {
    background: rgba(240, 248, 255, 0.9);
    border: 2rpx solid #87ceeb;
    box-shadow: 0 12rpx 40rpx rgba(135, 206, 235, 0.2);
}

.advice-card.primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6rpx;
    background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.card-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.card-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
}

.card-content {
    font-size: 28rpx;
    color: #5a6c7d;
    line-height: 1.7;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 24rpx;
    display: block;
}

.step-item {
    display: flex;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20rpx;
    padding: 36rpx;
    margin-bottom: 24rpx;
    box-shadow: 0 6rpx 24rpx rgba(135, 206, 235, 0.1);
    border: 1rpx solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.step-item:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 10rpx 32rpx rgba(135, 206, 235, 0.15);
}

.step-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 6rpx;
    background: linear-gradient(180deg, #87ceeb 0%, #add8e6 100%);
}

.step-number {
    width: 64rpx;
    height: 64rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26rpx;
    font-weight: 700;
    margin-right: 28rpx;
    flex-shrink: 0;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.3);
    position: relative;
}

.step-number::before {
    content: '';
    position: absolute;
    top: -2rpx;
    left: -2rpx;
    right: -2rpx;
    bottom: -2rpx;
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 50%;
    z-index: -1;
    opacity: 0.3;
}

.step-content {
    flex: 1;
}

.step-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 12rpx;
    display: block;
}

.step-desc {
    font-size: 26rpx;
    color: #5a6c7d;
    line-height: 1.6;
    margin-bottom: 16rpx;
}

.step-tips {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
}

.tip-item {
    font-size: 24rpx;
    color: #7f8c8d;
    padding-left: 16rpx;
}

.analysis-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.1);
}

.analysis-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.analysis-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.analysis-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
}

.analysis-content {
    font-size: 28rpx;
    color: #5a6c7d;
    line-height: 1.7;
}

.skill-recommendation {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20rpx;
    padding: 36rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 6rpx 24rpx rgba(135, 206, 235, 0.1);
    border: 1rpx solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.skill-recommendation::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(135, 206, 235, 0.05), transparent);
    transition: left 0.5s ease;
}

.skill-recommendation:hover::before {
    left: 100%;
}

.skill-recommendation:hover {
    transform: translateY(-4rpx) translateX(8rpx);
    box-shadow: 0 12rpx 40rpx rgba(135, 206, 235, 0.18);
    border-color: rgba(135, 206, 235, 0.3);
}

.skill-recommendation:active {
    transform: translateY(-2rpx) scale(0.98);
}

.skill-info {
    flex: 1;
}

.skill-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 8rpx;
    display: block;
}

.skill-reason {
    font-size: 26rpx;
    color: #5a6c7d;
}

.skill-action {
    display: flex;
    align-items: center;
    color: #4682b4;
}

.action-text {
    font-size: 26rpx;
    margin-right: 8rpx;
}

.action-arrow {
    font-size: 24rpx;
}

.support-card {
    background: linear-gradient(135deg, #f0f8ff 0%, #ffffff 100%);
    border: 2rpx solid #add8e6;
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 32rpx;
}

.support-header {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
}

.support-icon {
    font-size: 32rpx;
    margin-right: 16rpx;
}

.support-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
}

.support-content {
    font-size: 28rpx;
    color: #5a6c7d;
    line-height: 1.7;
}

.advice-actions {
    display: flex;
    gap: 20rpx;
    margin-top: 40rpx;
}

.action-btn {
    flex: 1;
    padding: 32rpx;
    border-radius: 16rpx;
    text-align: center;
    font-size: 30rpx;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.action-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.action-btn:hover::before {
    left: 100%;
}

.action-btn.primary {
    background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
    color: #2c3e50;
    box-shadow: 0 8rpx 24rpx rgba(135, 206, 235, 0.3);
}

.action-btn.primary:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 12rpx 32rpx rgba(135, 206, 235, 0.4);
}

.action-btn.secondary {
    background: rgba(255, 255, 255, 0.85);
    color: #4682b4;
    border: 2rpx solid #e6f3ff;
    box-shadow: 0 4rpx 16rpx rgba(135, 206, 235, 0.1);
}

.action-btn.secondary:hover {
    transform: translateY(-2rpx);
    border-color: #87ceeb;
    box-shadow: 0 8rpx 24rpx rgba(135, 206, 235, 0.2);
}

.action-btn:active {
    transform: translateY(0) scale(0.98);
}

.history-section {
    padding: 40rpx;
}

.history-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 32rpx;
    display: block;
}

.history-item {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 16rpx;
    padding: 32rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(135, 206, 235, 0.1);
    transition: transform 0.2s ease;
}

.history-item:active {
    transform: translateY(2rpx);
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.history-date {
    font-size: 24rpx;
    color: #7f8c8d;
}

.history-status {
    padding: 8rpx 16rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
}

.history-status.new {
    background-color: #e6f3ff;
    color: #4682b4;
}

.history-status.saved {
    background-color: #f0f8ff;
    color: #87ceeb;
}

.history-status.applied {
    background-color: #e1f0ff;
    color: #5a9fd4;
}

.status-text {
    font-size: 20rpx;
}

.history-situation {
    font-size: 28rpx;
    color: #2c3e50;
    margin-bottom: 12rpx;
    display: block;
    line-height: 1.5;
}

.history-type {
    font-size: 24rpx;
    color: #4682b4;
    padding: 6rpx 12rpx;
    background-color: #f0f8ff;
    border-radius: 12rpx;
    display: inline-block;
}

.loading-overlay {
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

.loading-content {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 32rpx;
    padding: 80rpx 50rpx;
    text-align: center;
    max-width: 650rpx;
    margin: 0 40rpx;
    box-shadow: 0 20rpx 60rpx rgba(135, 206, 235, 0.3);
    border: 1rpx solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.loading-content::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6rpx;
    background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
}

.loading-icon {
    font-size: 80rpx;
    margin-bottom: 20rpx;
    display: block;
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}

.loading-text {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 12rpx;
    display: block;
}

.loading-subtext {
    font-size: 26rpx;
    color: #5a6c7d;
    margin-bottom: 40rpx;
    display: block;
}

.loading-progress {
    margin-top: 40rpx;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #87ceeb 0%, #add8e6 100%);
    border-radius: 6rpx;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.progress-fill::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% {
        left: -100%;
    }

    100% {
        left: 100%;
    }
}

.progress-bar {
    width: 100%;
    height: 12rpx;
    background: linear-gradient(145deg, #f0f0f0 0%, #e0e0e0 100%);
    border-radius: 6rpx;
    overflow: hidden;
    margin-bottom: 20rpx;
    box-shadow: inset 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.progress-text {
    font-size: 24rpx;
    color: #4682b4;
    font-weight: bold;
}

.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 248, 255, 0.95) 100%);
    border-top: 1rpx solid rgba(135, 206, 235, 0.2);
    padding: 24rpx 0;
    display: flex;
    z-index: 100;
    backdrop-filter: blur(20px);
    box-shadow: 0 -8rpx 32rpx rgba(135, 206, 235, 0.1);
}

.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    border-radius: 16rpx;
    margin: 0 8rpx;
}

.nav-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(173, 216, 230, 0.1) 100%);
    border-radius: 16rpx;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.nav-item.active::before {
    opacity: 1;
}

.nav-item.active {
    color: #4682b4;
    transform: translateY(-4rpx);
}

.nav-item.active .nav-icon {
    transform: scale(1.15);
}

.nav-icon {
    font-size: 44rpx;
    margin-bottom: 12rpx;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    z-index: 10;
}

.nav-text {
    font-size: 24rpx;
    color: #5a6c7d;
    position: relative;
    z-index: 10;
    font-weight: 500;
}

.nav-item.active .nav-text {
    color: #4682b4;
    font-weight: 600;
}

.btn-text {
    font-size: inherit;
    color: inherit;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .advice-actions {
        flex-direction: column;
    }

    .relation-types {
        justify-content: center;
    }

    .type-chip {
        min-width: 140rpx;
        justify-content: center;
    }
}

/* 动画效果 */
.advice-card {
    animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.step-item {
    animation: fadeInLeft 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.skill-recommendation {
    animation: fadeInRight 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-card {
    animation: fadeInScale 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(40rpx);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-40rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInRight {
    from {
        opacity: 0;
        transform: translateX(40rpx);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6rpx;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 3rpx;
}

::-webkit-scrollbar-thumb:hover {
    background: #5a67d8;
}

/* 焦点状态 */
.form-textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3rpx rgba(102, 126, 234, 0.1);
    outline: none;
}

/* 禁用状态 */
.submit-btn.disabled:active {
    transform: none;
}

/* 触摸反馈 */
.type-chip:active,
.urgency-item:active,
.submit-btn:active,
.action-btn:active {
    transform: scale(0.98);
}

/* 长文本处理 */
.history-situation {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 安全区域适配 */
.bottom-nav {
    padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
}

.advice-container {
    padding-bottom: calc(160rpx + env(safe-area-inset-bottom));
}

/* 响应式优化 */
@media (max-width: 750rpx) {
    .advice-actions {
        flex-direction: column;
    }

    .relation-types {
        justify-content: center;
    }

    .type-chip {
        min-width: 160rpx;
        justify-content: center;
    }

    .header {
        padding: 60rpx 30rpx 50rpx;
    }

    .title {
        font-size: 48rpx;
    }

    .form-card {
        padding: 32rpx;
        margin: 0 20rpx 40rpx;
    }
}
</style>