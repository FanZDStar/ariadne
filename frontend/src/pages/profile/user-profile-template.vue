<!-- frontend/src/pages/profile/user-profile-template.vue -->
<template>
    <view class="profile-template-page">
        <!-- 生日选择器 -->
        <BirthdayPicker :visible="showBirthdayPicker" :model-value="form.birth_date"
            @update:modelValue="onBirthdaySelected" @close="showBirthdayPicker = false" />

        <!-- 页头 -->
        <view class="page-header">
            <view class="header-top">
                <text class="back-btn" @click="goBack">←</text>
                <text class="page-title">个人档案</text>
                <text class="save-btn" @click="saveProfile" v-if="hasChanges">保存</text>
            </view>
            <view class="completeness-bar">
                <view class="bar-container">
                    <view class="progress" :style="{ width: completeness + '%' }"></view>
                </view>
                <text class="completeness-text">完成度 {{ completeness.toFixed(0) }}%</text>
            </view>
        </view>

        <!-- 滚动内容 -->
        <scroll-view class="scroll-content" scroll-y>
            <!-- 基本信息部分 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">📅 基本信息</text>
                    <view class="section-status" v-if="isBasicInfoComplete">✓</view>
                </view>

                <view class="form-group">
                    <text class="form-label">性别</text>
                    <picker :range="genders" :value="selectedGenderIndex" @change="onGenderChange">
                        <view class="picker-input">
                            {{ form.gender || '选择性别' }}
                            <text class="arrow">▼</text>
                        </view>
                    </picker>
                </view>

                <view class="form-group">
                    <text class="form-label">生日</text>
                    <view class="input-wrapper" @click="showBirthdayPicker = true">
                        <view class="picker-input">
                            {{ form.birth_date || '选择生日' }}
                            <text class="arrow">▼</text>
                        </view>
                    </view>
                </view>

                <view class="form-group">
                    <text class="form-label">星座</text>
                    <view class="picker-input" style="color: #999; cursor: not-allowed;">
                        {{ form.zodiac_sign || '选择生日后自动生成' }}
                        <text class="info-icon" style="font-size: 12px; margin-left: 5px;">ℹ️</text>
                    </view>
                    <text class="form-hint">根据生日自动生成，无需手动选择</text>
                </view>
            </view>

            <!-- 性格特征部分 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">✨ 性格特征</text>
                    <view class="section-status" v-if="isPersonalityComplete">✓</view>
                </view>
                <text class="section-hint">可选择多个标签，也可自己描述</text>

                <view class="tags-container">
                    <view v-for="tag in personalityTags" :key="tag.id" class="tag-item"
                        :class="{ active: form.personality_tags.includes(tag.tag_name) }"
                        @click="toggleTag('personality_tags', tag.tag_name)">
                        {{ tag.tag_name }}
                    </view>
                </view>

                <view class="form-group">
                    <text class="form-label">自定义描述</text>
                    <textarea class="textarea" placeholder="描述您的性格特点（如：虽然外向，但也很谨慎）"
                        v-model="form.personality_custom_description" maxlength="100" />
                    <text class="char-count">{{ form.personality_custom_description.length }}/100</text>
                </view>
            </view>

            <!-- 兴趣爱好部分 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">🎯 兴趣爱好</text>
                    <view class="section-status" v-if="isHobbyComplete">✓</view>
                </view>

                <!-- 按分类显示爱好标签 -->
                <view v-for="category in hobbyCategories" :key="category" class="category-group">
                    <text class="category-name">{{ getCategoryEmoji(category) }} {{ category }}</text>
                    <view class="tags-container">
                        <view v-for="tag in getHobbysByCategory(category)" :key="tag.id" class="tag-item"
                            :class="{ active: form.hobby_tags.includes(tag.tag_name) }"
                            @click="toggleTag('hobby_tags', tag.tag_name)">
                            {{ tag.emoji }} {{ tag.tag_name }}
                        </view>
                    </view>
                </view>

                <view class="form-group">
                    <text class="form-label">自定义描述</text>
                    <textarea class="textarea" placeholder="详细描述您的爱好（如：特别喜欢晚上编程，周末喜欢户外运动）"
                        v-model="form.hobby_custom_description" maxlength="100" />
                    <text class="char-count">{{ form.hobby_custom_description.length }}/100</text>
                </view>
            </view>

            <!-- 职业背景部分 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">💼 职业背景</text>
                    <view class="section-status" v-if="isProfessionComplete">✓</view>
                </view>

                <!-- 按分类显示职业标签 -->
                <view v-for="category in professionCategories" :key="category" class="category-group">
                    <text class="category-name">{{ getProfessionCategoryEmoji(category) }} {{ category }}</text>
                    <view class="tags-container">
                        <view v-for="tag in getProfessionsByCategory(category)" :key="tag.id" class="tag-item"
                            :class="{ active: form.profession_tags.includes(tag.tag_name) }"
                            @click="toggleTag('profession_tags', tag.tag_name)">
                            {{ tag.tag_name }}
                        </view>
                    </view>
                </view>

                <view class="form-group">
                    <text class="form-label">具体职位/工作</text>
                    <input class="input" type="text" placeholder="如：前端开发工程师" v-model="form.job_title" />
                </view>

                <view class="form-group">
                    <text class="form-label">职业描述</text>
                    <textarea class="textarea" placeholder="如：从事互联网产品开发，对用户体验特别感兴趣"
                        v-model="form.profession_custom_description" maxlength="100" />
                    <text class="char-count">{{ form.profession_custom_description.length }}/100</text>
                </view>
            </view>

            <!-- 其他信息部分 -->
            <view class="section">
                <view class="section-header">
                    <text class="section-title">🌟 其他信息</text>
                </view>

                <view class="form-group">
                    <text class="form-label">生活阶段</text>
                    <picker :range="lifeStages" :value="selectedLifeStageIndex" @change="onLifeStageChange">
                        <view class="picker-input">
                            {{ form.life_stage || '选择生活阶段' }}
                            <text class="arrow">▼</text>
                        </view>
                    </picker>
                </view>

                <!-- 城市/地区 已注释
        <view class="form-group">
          <text class="form-label">城市/地区</text>
          <input
            class="input"
            type="text"
            placeholder="如：北京"
            v-model="form.location"
          />
        </view>
        -->

                <view class="form-group">
                    <text class="form-label">个人座右铭</text>
                    <textarea class="textarea" placeholder="如：持续学习，保持好奇" v-model="form.personal_motto"
                        maxlength="100" />
                    <text class="char-count">{{ form.personal_motto.length }}/100</text>
                </view>

                <view class="form-group">
                    <text class="form-label">当前主要关注领域</text>
                    <view class="focus-tags-container">
                        <view v-for="(focus, idx) in form.main_focus_areas" :key="idx" class="focus-tag">
                            <text>{{ focus }}</text>
                            <text class="remove-btn" @click="removeFocus(idx)">×</text>
                        </view>
                        <input class="focus-input" type="text" placeholder="输入后按Enter添加" @keydown.enter="addFocus"
                            v-model="focusInput" />
                    </view>
                </view>
            </view>

            <!-- 底部空间 -->
            <view class="bottom-spacing"></view>
        </scroll-view>

        <!-- 底部按钮 -->
        <view class="footer-buttons">
            <button class="btn btn-secondary" @click="resetForm">重置</button>
            <button class="btn btn-primary" @click="saveProfile">保存档案</button>
        </view>

        <!-- 加载提示 -->
        <view v-if="loading" class="loading-overlay">
            <view class="loading-spinner">
                <text>加载中...</text>
            </view>
        </view>

        <!-- 成功提示 -->
        <view v-if="successMessage" class="toast" :class="{ show: successMessage }">
            {{ successMessage }}
        </view>

        <!-- 错误提示 -->
        <view v-if="errorMessage" class="toast error" :class="{ show: errorMessage }">
            {{ errorMessage }}
        </view>
    </view>
</template>

<script>
import { api, storage } from '../../utils/api';
import BirthdayPicker from '../../components/BirthdayPicker.vue';

export default {
    components: {
        BirthdayPicker
    },
    data() {
        return {
            form: {
                gender: '',
                birth_date: '',
                zodiac_sign: '',
                personality_tags: [],
                personality_custom_description: '',
                hobby_tags: [],
                hobby_custom_description: '',
                profession_tags: [],
                profession_custom_description: '',
                job_title: '',
                life_stage: '',
                location: '',
                personal_motto: '',
                main_focus_areas: []
            },
            originalForm: {}, // 用于检测变化
            personalityTags: [],
            hobbyTags: [],
            professionTags: [],
            zodiacSigns: [],
            genders: ['男', '女', '其他'],
            lifeStages: ['高中', '大学', '工作', '已婚', '其他'],
            focusInput: '',
            selectedZodiacIndex: 0,
            selectedLifeStageIndex: 0,
            selectedGenderIndex: 0,
            completeness: 0,
            loading: false,
            successMessage: '',
            errorMessage: '',
            hasChanges: false,
            showBirthdayPicker: false
        };
    },

    computed: {
        hobbyCategories() {
            const categories = new Set(this.hobbyTags.map(tag => tag.category));
            return Array.from(categories).sort();
        },

        professionCategories() {
            const categories = new Set(this.professionTags.map(tag => tag.category));
            return Array.from(categories).sort();
        },

        isBasicInfoComplete() {
            return this.form.gender && this.form.birth_date && this.form.zodiac_sign;
        },

        isPersonalityComplete() {
            return this.form.personality_tags.length > 0 || this.form.personality_custom_description;
        },

        isHobbyComplete() {
            return this.form.hobby_tags.length > 0 || this.form.hobby_custom_description;
        },

        isProfessionComplete() {
            return (
                this.form.profession_tags.length > 0 ||
                this.form.job_title ||
                this.form.profession_custom_description
            );
        }
    },

    onLoad() {
        this.initPage();
    },

    methods: {
        async initPage() {
            this.loading = true;
            try {
                // 加载标签选项
                await this.loadTagOptions();
                // 加载用户现有档案
                await this.loadUserProfile();
                // 保存原始数据用于比对
                this.originalForm = JSON.parse(JSON.stringify(this.form));
            } catch (error) {
                console.error('初始化页面失败:', error);
                this.errorMessage = '加载失败，请重试';
            } finally {
                this.loading = false;
            }
        },

        async loadTagOptions() {
            try {
                const response = await api.getTagOptions();
                this.personalityTags = response.personality_tags || [];
                this.hobbyTags = response.hobby_tags || [];
                this.professionTags = response.profession_tags || [];
                this.zodiacSigns = response.zodiac_signs || [];
            } catch (error) {
                console.error('加载标签选项失败:', error);
                throw error;
            }
        },

        async loadUserProfile() {
            try {
                const response = await api.getUserProfileTemplate();
                if (response) {
                    this.form = {
                        gender: response.gender || '',
                        birth_date: response.birth_date || '',
                        zodiac_sign: response.zodiac_sign || '',
                        personality_tags: response.personality_tags || [],
                        personality_custom_description: response.personality_custom_description || '',
                        hobby_tags: response.hobby_tags || [],
                        hobby_custom_description: response.hobby_custom_description || '',
                        profession_tags: response.profession_tags || [],
                        profession_custom_description: response.profession_custom_description || '',
                        job_title: response.job_title || '',
                        life_stage: response.life_stage || '',
                        location: response.location || '',
                        personal_motto: response.personal_motto || '',
                        main_focus_areas: response.main_focus_areas || []
                    };
                    // 更新picker的选中索引
                    this.updatePickerIndices();
                }
                this.updateCompleteness();
            } catch (error) {
                console.log('档案未创建或加载失败');
            }
        },

        updatePickerIndices() {
            if (this.form.gender) {
                this.selectedGenderIndex = this.genders.indexOf(this.form.gender);
            }
            if (this.form.zodiac_sign) {
                this.selectedZodiacIndex = this.zodiacSigns.findIndex(
                    z => z.sign_name === this.form.zodiac_sign
                );
            }
            if (this.form.life_stage) {
                this.selectedLifeStageIndex = this.lifeStages.indexOf(this.form.life_stage);
            }
        },

        getHobbysByCategory(category) {
            return this.hobbyTags.filter(tag => tag.category === category);
        },

        getProfessionsByCategory(category) {
            return this.professionTags.filter(tag => tag.category === category);
        },

        getCategoryEmoji(category) {
            const emojiMap = {
                '学习娱乐': '📚',
                '运动健身': '🏃',
                '艺术创意': '🎨',
                '技术': '💻',
                '娱乐': '🎬',
                '生活': '👨‍🍳'
            };
            return emojiMap[category] || '📌';
        },

        getProfessionCategoryEmoji(category) {
            const emojiMap = {
                '学生': '👨‍🎓',
                '技术': '💻',
                '创意': '🎨',
                '商业': '📊',
                '文创': '✍️',
                '教育': '🏫',
                '医疗': '🏥',
                '其他': '🌟'
            };
            return emojiMap[category] || '📌';
        },

        toggleTag(fieldName, tagName) {
            const tags = this.form[fieldName];
            const index = tags.indexOf(tagName);
            if (index > -1) {
                tags.splice(index, 1);
            } else {
                tags.push(tagName);
            }
            this.checkChanges();
            this.updateCompleteness();
        },

        // 根据生日计算星座
        calculateZodiacFromBirthDate(birthDate) {
            if (!birthDate) return '';

            const [year, month, day] = birthDate.split('-').map(Number);
            const zodiacData = [
                { name: '摩羯座', start: [12, 22], end: [1, 19] },
                { name: '水瓶座', start: [1, 20], end: [2, 18] },
                { name: '双鱼座', start: [2, 19], end: [3, 20] },
                { name: '白羊座', start: [3, 21], end: [4, 19] },
                { name: '金牛座', start: [4, 20], end: [5, 20] },
                { name: '双子座', start: [5, 21], end: [6, 20] },
                { name: '巨蟹座', start: [6, 21], end: [7, 22] },
                { name: '狮子座', start: [7, 23], end: [8, 22] },
                { name: '处女座', start: [8, 23], end: [9, 22] },
                { name: '天秤座', start: [9, 23], end: [10, 22] },
                { name: '天蝎座', start: [10, 23], end: [11, 21] },
                { name: '射手座', start: [11, 22], end: [12, 21] }
            ];

            for (let zodiac of zodiacData) {
                const [startMonth, startDay] = zodiac.start;
                const [endMonth, endDay] = zodiac.end;

                if (startMonth === endMonth) {
                    if (month === startMonth && day >= startDay && day <= endDay) {
                        return zodiac.name;
                    }
                } else {
                    if ((month === startMonth && day >= startDay) || (month === endMonth && day <= endDay)) {
                        return zodiac.name;
                    }
                }
            }

            return '';
        },

        onBirthdaySelected(birthDate) {
            this.form.birth_date = birthDate;
            // 自动计算星座
            const calculatedZodiac = this.calculateZodiacFromBirthDate(birthDate);
            if (calculatedZodiac) {
                this.form.zodiac_sign = calculatedZodiac;
                // 更新选中的星座索引
                this.selectedZodiacIndex = this.zodiacSigns.findIndex(
                    z => z.sign_name === calculatedZodiac
                );
            }
            this.checkChanges();
            this.updateCompleteness();
        },

        onZodiacChange(event) {
            this.selectedZodiacIndex = event.detail.value;
            if (this.zodiacSigns[this.selectedZodiacIndex]) {
                this.form.zodiac_sign = this.zodiacSigns[this.selectedZodiacIndex].sign_name;
            }
            this.checkChanges();
            this.updateCompleteness();
        },

        onLifeStageChange(event) {
            this.selectedLifeStageIndex = event.detail.value;
            this.form.life_stage = this.lifeStages[this.selectedLifeStageIndex];
            this.checkChanges();
        },

        onGenderChange(event) {
            this.selectedGenderIndex = event.detail.value;
            this.form.gender = this.genders[this.selectedGenderIndex];
            this.checkChanges();
        },

        addFocus(event) {
            if (this.focusInput.trim()) {
                this.form.main_focus_areas.push(this.focusInput.trim());
                this.focusInput = '';
                this.checkChanges();
            }
        },

        removeFocus(index) {
            this.form.main_focus_areas.splice(index, 1);
            this.checkChanges();
        },

        updateCompleteness() {
            let filled = 0;
            const total = 5;

            if (this.form.birth_date) filled++;
            if (this.form.zodiac_sign) filled++;
            if (this.isPersonalityComplete) filled++;
            if (this.isHobbyComplete) filled++;
            if (this.isProfessionComplete) filled++;

            this.completeness = (filled / total) * 100;
        },

        checkChanges() {
            this.hasChanges = JSON.stringify(this.form) !== JSON.stringify(this.originalForm);
        },

        async saveProfile() {
            this.loading = true;
            try {
                // 先尝试获取现有档案
                let hasProfile = false;
                try {
                    await api.getUserProfileTemplate();
                    hasProfile = true;
                } catch (error) {
                    // 档案不存在，准备创建
                    hasProfile = false;
                }

                // 根据是否存在档案选择创建或更新
                if (hasProfile) {
                    await api.updateUserProfileTemplate(this.form);
                } else {
                    // 创建新档案
                    await api.createUserProfileTemplate(this.form);
                }

                // ✨ 关键：将用户模板信息保存到本地存储，供聊天功能使用
                const userProfileForChat = {
                    name: this.form.user_name || '',
                    gender: this.form.gender || '',
                    star_sign: this.form.zodiac_sign || '',
                    personality_tags: this.form.personality_tags || [],
                    hobby_tags: this.form.hobby_tags || [],
                    personal_motto: this.form.personal_motto || ''
                };

                try {
                    uni.setStorageSync('user_profile_template', JSON.stringify(userProfileForChat));
                    console.log('✅ 用户模板已保存到本地存储，供聊天使用:', userProfileForChat);
                } catch (e) {
                    console.error('⚠️ 保存到本地存储失败:', e);
                }

                this.successMessage = '档案保存成功！';
                this.originalForm = JSON.parse(JSON.stringify(this.form));
                this.hasChanges = false;
                this.updateCompleteness();
                setTimeout(() => {
                    this.successMessage = '';
                }, 2000);
            } catch (error) {
                console.error('保存失败:', error);
                this.errorMessage = '保存失败，请重试: ' + (error.message || '未知错误');
                setTimeout(() => {
                    this.errorMessage = '';
                }, 2000);
            } finally {
                this.loading = false;
            }
        },

        resetForm() {
            this.form = JSON.parse(JSON.stringify(this.originalForm));
            this.hasChanges = false;
            this.updatePickerIndices();
        },

        goBack() {
            if (this.hasChanges) {
                uni.showModal({
                    title: '提示',
                    content: '您有未保存的修改，确定要返回吗？',
                    success: (res) => {
                        if (res.confirm) {
                            uni.navigateBack();
                        }
                    }
                });
            } else {
                uni.navigateBack();
            }
        }
    }
};
</script>

<style scoped lang="scss">
.profile-template-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f5f5f5;
}

.page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    color: white;

    .back-btn {
        font-size: 24px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .page-title {
        font-size: 18px;
        font-weight: bold;
        flex: 1;
        text-align: center;
    }

    .save-btn {
        font-size: 14px;
        width: 50px;
        text-align: right;
    }
}

.completeness-bar {
    padding: 10px 15px;

    .bar-container {
        width: 100%;
        height: 6px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 8px;

        .progress {
            height: 100%;
            background: linear-gradient(90deg, #84fab0 0%, #8fd3f4 100%);
            transition: width 0.3s ease;
        }
    }

    .completeness-text {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
    }
}

.scroll-content {
    flex: 1;
    overflow-y: auto;
}

.section {
    margin: 20px 15px;
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;

    .section-title {
        font-size: 16px;
        font-weight: bold;
        color: #333;
    }

    .section-status {
        color: #84fab0;
        font-size: 18px;
        font-weight: bold;
    }
}

.section-hint {
    font-size: 12px;
    color: #999;
    margin-bottom: 12px;
    display: block;
}

.form-group {
    margin-bottom: 20px;

    &:last-child {
        margin-bottom: 0;
    }
}

.form-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
}

.form-hint {
    display: block;
    font-size: 12px;
    color: #999;
    margin-top: 4px;
}

.input-wrapper,
.picker-input {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .arrow {
        color: #999;
        margin-left: 8px;
    }
}

.input {
    width: 100%;
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #333;
    box-sizing: border-box;

    &::placeholder {
        color: #ccc;
    }
}

.textarea {
    width: 100%;
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #333;
    resize: none;
    min-height: 80px;
    box-sizing: border-box;
    font-family: inherit;

    &::placeholder {
        color: #ccc;
    }
}

.char-count {
    display: block;
    text-align: right;
    font-size: 12px;
    color: #999;
    margin-top: 4px;
}

.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}

.tag-item {
    padding: 8px 16px;
    background-color: #f0f0f0;
    border: 2px solid #e0e0e0;
    border-radius: 20px;
    font-size: 13px;
    color: #666;
    transition: all 0.3s ease;

    &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
}

.category-group {
    margin-bottom: 20px;

    .category-name {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
}

.focus-tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 12px;
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

.focus-tag {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 16px;
    font-size: 12px;

    .remove-btn {
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
}

.focus-input {
    flex: 1;
    background: transparent;
    border: none;
    font-size: 13px;
    color: #333;
    min-width: 100px;

    &::placeholder {
        color: #ccc;
    }
}

.footer-buttons {
    display: flex;
    gap: 10px;
    padding: 15px;
    background: white;
    border-top: 1px solid #f0f0f0;

    .btn {
        flex: 1;
        padding: 14px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .btn-secondary {
        background-color: #f0f0f0;
        color: #333;
    }
}

.bottom-spacing {
    height: 20px;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;

    .loading-spinner {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }
}

.toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #333;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 999;

    &.show {
        opacity: 1;
    }

    &.error {
        background-color: #ff4444;
    }
}
</style>
