<template>
  <view class="edit-whisper-container">    <!-- 美化的头部导航 -->
    <view class="header">
      <view class="header-content">
        <view class="header-right" @click="saveChanges">
          <view class="save-btn" :class="{ disabled: !canSave || isSaving }">
            <text class="save-text">{{ isSaving ? '保存中...' : '保存' }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="content" v-if="!loading">
      <!-- 美化的标题输入区域 -->
      <view class="input-section title-section">
        <view class="section-header">
          <text class="section-title">标题</text>
          <text class="title-hint">可选</text>
        </view>
        <view class="input-wrapper">
          <input class="whisper-title" placeholder="给悄悄话起个标题吧..." v-model="whisperTitle" maxlength="50" />
        </view>
      </view>

      <!-- 美化的内容输入区域 -->
      <view class="input-section content-section">
        <view class="section-header">
          <text class="section-title">内容</text>
          <text class="word-count">{{ whisperContent.length }}/1000</text>
        </view>
        <view class="input-wrapper">
          <textarea class="whisper-content" placeholder="向树洞倾诉你的心声..." v-model="whisperContent" maxlength="1000" />
        </view>
      </view>

      <!-- 美化的心情选择器 -->
      <view class="input-section mood-section">
        <view class="section-header">
          <text class="section-title">心情</text>
        </view>
        <view class="mood-options">
          <view class="mood-item" v-for="mood in moodOptions" :key="mood.value"
            :class="{ selected: selectedMood === mood.value }" @click="selectMood(mood.value)">
            <text class="mood-emoji">{{ mood.emoji }}</text>
            <text class="mood-name">{{ mood.name }}</text>
          </view>
        </view>
      </view>

      <!-- 美化的标签选择器 -->
      <view class="input-section tag-section">
        <view class="section-header">
          <text class="section-title">标签</text>
          <text class="tag-count">{{ selectedTags.length }}/5</text>
        </view>
        
        <!-- 已选择的标签 -->
        <view class="selected-tags" v-if="selectedTags.length > 0">
          <view class="tag-item selected-tag" v-for="tag in selectedTags" :key="tag" @click="removeTag(tag)">
            <text class="tag-text">{{ tag }}</text>
            <text class="tag-remove">×</text>
          </view>
        </view>

        <!-- 标签输入 -->
        <view class="tag-input-area">
          <input v-if="showTagInput" class="tag-input" placeholder="输入自定义标签" 
            v-model="currentTag" @confirm="addTag" @blur="hideTagInput" />
          <view v-if="!showTagInput" class="add-tag-btn" @click="showTagInput = true">
            <text>+ 添加标签</text>
          </view>
        </view>

        <!-- 预设标签 -->
        <view class="preset-tags">
          <text class="preset-title">推荐标签：</text>
          <view class="preset-tag-list">
            <view class="preset-tag" v-for="tag in presetTags" :key="tag" 
              :class="{ disabled: selectedTags.includes(tag) || selectedTags.length >= 5 }"
              @click="selectPresetTag(tag)">
              <text>{{ tag }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 美化的加载状态 -->
    <view v-if="loading" class="loading-container">
      <view class="loading-content">
        <view class="loading-spinner"></view>
        <text class="loading-text">加载中...</text>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      whisperId: null,
      whisperTitle: '',
      whisperContent: '',
      selectedMood: 'neutral',
      selectedTags: [],
      currentTag: '',
      showTagInput: false,
      presetTags: ['心情', '秘密', '困扰', '感悟', '日常', '吐槽', '想法', '回忆'],
      isSaving: false,
      loading: true,
      // 存储原始数据用于修改检测
      originalData: {
        title: '',
        content: '',
        mood: 'neutral',
        tags: []
      },
      moodOptions: [
        { value: 'very_happy', emoji: '😄', name: '开心' },
        { value: 'happy', emoji: '😊', name: '愉快' },
        { value: 'neutral', emoji: '😐', name: '平静' },
        { value: 'sad', emoji: '😢', name: '难过' },
        { value: 'very_sad', emoji: '😭', name: '伤心' }
      ]
    };
  },

  computed: {
    hasChanges() {
      const currentTitle = this.whisperTitle.trim();
      const currentContent = this.whisperContent.trim();
      const currentMood = this.selectedMood;
      const currentTags = JSON.stringify([...this.selectedTags].sort());
      const originalTags = JSON.stringify([...this.originalData.tags].sort());
      
      return (
        currentTitle !== this.originalData.title ||
        currentContent !== this.originalData.content ||
        currentMood !== this.originalData.mood ||
        currentTags !== originalTags
      );
    },
    
    canSave() {
      if (this.loading) return false;
      if (this.whisperContent.trim().length === 0) return false;
      
      // 检测是否有修改
      return this.hasChanges;
    }
  },

  onLoad(options) {
    if (options.whisper_id) {
      this.whisperId = options.whisper_id;
      this.loadWhisperData();
    } else {
      uni.showToast({
        title: '参数错误',
        icon: 'none'
      });
      setTimeout(() => {
        uni.navigateBack();
      }, 1500);
    }
  },

  methods: {
    // 加载悄悄话数据
    async loadWhisperData() {
      try {
        const token = storage.getToken();
        if (!token) {
          uni.showToast({
            title: '请先登录',
            icon: 'none'
          });
          setTimeout(() => {
            uni.navigateBack();
          }, 1500);
          return;
        }

        const whisper = await api.getWhisperDetail(token, this.whisperId);
        
        console.log('加载的悄悄话数据:', whisper);
        console.log('title字段:', whisper.title);
        
        // 检查是否是用户自己的悄悄话
        const userInfo = storage.getUserInfo();
        if (whisper.user_id !== userInfo.user_id) {
          uni.showToast({
            title: '无权限编辑',
            icon: 'none'
          });
          setTimeout(() => {
            uni.navigateBack();
          }, 1500);
          return;
        }

        // 填充数据
        this.whisperTitle = whisper.title || '';
        this.whisperContent = whisper.content || '';
        this.selectedMood = whisper.mood || 'neutral';
        
        console.log('填充后的数据:');
        console.log('whisperTitle:', this.whisperTitle);
        console.log('whisperContent:', this.whisperContent);
        console.log('selectedMood:', this.selectedMood);
        
        // 简化标签处理逻辑
        this.selectedTags = Array.isArray(whisper.tags) ? whisper.tags : 
          (whisper.tags ? (typeof whisper.tags === 'string' ? JSON.parse(whisper.tags) : []) : []);

        // 存储原始数据用于修改检测
        this.originalData = {
          title: this.whisperTitle,
          content: this.whisperContent,
          mood: this.selectedMood,
          tags: [...this.selectedTags]
        };

        this.loading = false;
      } catch (error) {
        console.error('加载悄悄话失败:', error);
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        });
        setTimeout(() => {
          uni.navigateBack();
        }, 1500);
      }
    },

    // 保存修改
    async saveChanges() {
      if (!this.canSave || this.isSaving) return;

      this.isSaving = true;

      try {
        const token = storage.getToken();
        const updateData = {
          title: this.whisperTitle.trim(),
          content: this.whisperContent.trim(),
          mood: this.selectedMood,
          tags: this.selectedTags
        };

        await api.updateWhisper(token, this.whisperId, updateData);

        uni.showToast({
          title: '保存成功',
          icon: 'success'
        });

        setTimeout(() => {
          uni.navigateBack();
        }, 1500);
      } catch (error) {
        console.error('保存失败:', error);
        uni.showToast({
          title: '保存失败',
          icon: 'none'
        });
      } finally {
        this.isSaving = false;
      }
    },

    // 选择心情
    selectMood(mood) {
      this.selectedMood = mood;
    },

    // 添加标签
    addTag() {
      const tag = this.currentTag.trim();
      if (tag && !this.selectedTags.includes(tag)) {
        if (this.selectedTags.length < 5) {
          this.selectedTags.push(tag);
          this.currentTag = '';
        } else {
          uni.showToast({
            title: '最多添加5个标签',
            icon: 'none'
          });
        }
      }
      this.hideTagInput();
    },

    // 移除标签
    removeTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index > -1) {
        this.selectedTags.splice(index, 1);
      }
    },

    // 选择预设标签
    selectPresetTag(tag) {
      if (!this.selectedTags.includes(tag)) {
        if (this.selectedTags.length < 5) {
          this.selectedTags.push(tag);
        } else {
          uni.showToast({
            title: '最多添加5个标签',
            icon: 'none'
          });
        }
      }
    },

    // 隐藏标签输入
    hideTagInput() {
      this.showTagInput = false;
    }
  }
};
</script>

<style scoped>
.edit-whisper-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #f8f9ff 100%);
}

/* 美化的头部导航 */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(144, 202, 249, 0.2);
  box-shadow: 0 2px 20px rgba(144, 202, 249, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 40rpx;
  max-width: 750rpx;
  margin: 0 auto;
}

.header-right {
  flex: 1;
}

.header-center {
  flex: 2;
  text-align: center;
}

.header-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #1565c0;
}

.save-btn {
  display: flex;
  justify-content: flex-end;
}

.save-text {
  font-size: 30rpx;
  color: #1976d2;
  font-weight: 600;
  padding: 12rpx 24rpx;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-radius: 25rpx;
}

.save-btn.disabled .save-text {
  color: #bdbdbd;
  background: #f5f5f5;
}

/* 内容区域 */
.content {
  flex: 1;
  padding: 40rpx;
  overflow-y: auto;
  max-width: 750rpx;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

/* 输入区域通用样式 */
.input-section {
  margin-bottom: 50rpx;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 8px 32px rgba(144, 202, 249, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(144, 202, 249, 0.2);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
  gap: 16rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #1565c0;
  flex: 1;
}

.word-count, .tag-count, .title-hint {
  font-size: 24rpx;
  color: #90a4ae;
  background: rgba(144, 202, 249, 0.1);
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
}

/* 输入框样式 */
.input-wrapper {
  position: relative;
}

.whisper-title {
  width: 100%;
  padding: 24rpx;
  border: 2px solid rgba(144, 202, 249, 0.3);
  border-radius: 16rpx;
  font-size: 32rpx;
  background: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.whisper-title:focus {
  border-color: #42a5f5;
  outline: none;
}

.whisper-content {
  width: 100%;
  min-height: 320rpx;
  padding: 24rpx;
  border: 2px solid rgba(144, 202, 249, 0.3);
  border-radius: 16rpx;
  font-size: 30rpx;
  line-height: 1.6;
  background: rgba(255, 255, 255, 0.8);
  resize: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.whisper-content:focus {
  border-color: #42a5f5;
  outline: none;
}

/* 心情选择器 */
.mood-options {
  display: flex;
  gap: 20rpx;
  flex-wrap: wrap;
}

.mood-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 20rpx;
  border-radius: 20rpx;
  background: rgba(255, 255, 255, 0.6);
  border: 2px solid rgba(144, 202, 249, 0.2);
  transition: all 0.3s ease;
  min-width: 100rpx;
}

.mood-item.selected {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-color: #42a5f5;
  transform: scale(1.05);
}

.mood-emoji {
  font-size: 40rpx;
}

.mood-name {
  font-size: 24rpx;
  color: #1565c0;
  font-weight: 500;
}

/* 标签区域 */
.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.selected-tag {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1565c0;
  padding: 16rpx 20rpx;
  border-radius: 25rpx;
  font-size: 26rpx;
  font-weight: 500;
  border: 1px solid rgba(144, 202, 249, 0.3);
}

.tag-text {
  flex: 1;
}

.tag-remove {
  font-size: 28rpx;
  font-weight: bold;
  color: #f44336;
  width: 32rpx;
  height: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(244, 67, 54, 0.1);
  border-radius: 50%;
}

.tag-input-area {
  margin-bottom: 24rpx;
}

.tag-input {
  width: 100%;
  padding: 20rpx 24rpx;
  border: 2px solid rgba(144, 202, 249, 0.3);
  border-radius: 25rpx;
  font-size: 26rpx;
  background: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.tag-input:focus {
  border-color: #42a5f5;
  outline: none;
}

.add-tag-btn {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 20rpx 24rpx;
  background: rgba(144, 202, 249, 0.1);
  color: #1976d2;
  border: 2px dashed rgba(144, 202, 249, 0.5);
  border-radius: 25rpx;
  font-size: 26rpx;
  font-weight: 500;
  transition: all 0.3s ease;
  justify-content: center;
}

.add-tag-btn:hover {
  background: rgba(144, 202, 249, 0.2);
}

/* 预设标签 */
.preset-tags {
  margin-top: 24rpx;
}

.preset-title {
  font-size: 26rpx;
  color: #90a4ae;
  margin-bottom: 16rpx;
  display: block;
}

.preset-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.preset-tag {
  padding: 16rpx 20rpx;
  background: rgba(255, 255, 255, 0.8);
  color: #1976d2;
  border: 1px solid rgba(144, 202, 249, 0.3);
  border-radius: 20rpx;
  font-size: 24rpx;
  transition: all 0.3s ease;
}

.preset-tag:not(.disabled):hover {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  transform: translateY(-2rpx);
}

.preset-tag.disabled {
  opacity: 0.5;
  color: #bdbdbd;
}

/* 加载状态 */
.loading-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24rpx;
}

.loading-spinner {
  width: 60rpx;
  height: 60rpx;
  border: 4rpx solid rgba(144, 202, 249, 0.3);
  border-top: 4rpx solid #42a5f5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 28rpx;
  color: #90a4ae;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 500px) {
  .content {
    padding: 32rpx 24rpx;
  }
  
  .input-section {
    padding: 24rpx;
  }
  
  .mood-options {
    gap: 16rpx;
  }
  
  .mood-item {
    min-width: 80rpx;
    padding: 16rpx;
  }
}
</style>