<template>
  <view class="write-whisper-container">    <view class="header">
      <view class="header-left" @click="cancel">
        <text class="cancel-btn">取消</text>
      </view>
      <view class="header-right" @click="publish">
        <text class="publish-btn" :class="{ disabled: !canPublish || isPublishing }">
          {{ isPublishing ? '发布中...' : '发布' }}
        </text>
      </view>
    </view>

    <view class="content">
      <!-- 悄悄话标题输入 -->
      <view class="title-input-section">
        <input class="whisper-title" placeholder="给悄悄话起个标题吧..." v-model="whisperTitle" maxlength="50" />
      </view>

      <!-- 悄悄话内容输入 -->
      <textarea class="whisper-content" placeholder="向树洞倾诉你的心声..." v-model="whisperContent" maxlength="1000" />

      <view class="content-info">
        <text class="word-count">{{ whisperContent.length }}/1000</text>
      </view>

      <!-- 标签选择器 -->
      <view class="tag-selector">
        <text class="tag-label">标签：</text>
        <view class="tag-container">
          <view class="tag-item" v-for="tag in selectedTags" :key="tag" @click="removeTag(tag)">
            <text class="tag-text">{{ tag }}</text>
            <text class="tag-remove">×</text>
          </view>
          <input v-if="showTagInput || selectedTags.length === 0" class="tag-input" placeholder="添加标签..."
            v-model="currentTag" @confirm="addTag" @blur="hideTagInput" />
          <view v-else class="add-tag-btn" @click="showTagInput = true">
            <text>+ 添加标签</text>
          </view>
        </view>
        <!-- 预设标签 -->
        <view class="preset-tags">
          <view class="preset-tag" v-for="tag in presetTags" :key="tag" @click="selectPresetTag(tag)">
            <text>{{ tag }}</text>
          </view>
        </view>
      </view>

      <!-- 心情选择器 -->
      <view class="mood-selector">
        <text class="mood-label">心情：</text>
        <view class="mood-options">
          <view class="mood-option" v-for="mood in moodOptions" :key="mood.value"
            :class="{ selected: selectedMood === mood.value }" @click="selectMood(mood.value)">
            <text class="mood-emoji">{{ mood.emoji }}</text>
          </view>
        </view>
      </view>

      <!-- 图片上传 -->
      <view class="image-upload">
        <text class="image-label">图片：</text>
        <view class="image-grid">
          <view class="image-item" v-for="(image, index) in uploadedImages" :key="index">
            <image :src="image.tempUrl || image.url" class="uploaded-image" mode="aspectFill" />
            <view class="remove-image" @click="removeImage(index)">×</view>
            <view v-if="!image.uploaded" class="uploading-overlay">
              <text class="uploading-text">上传中...</text>
            </view>
          </view>
          <view class="image-upload-btn" v-if="uploadedImages.length < 9" @click="chooseImage">
            <text class="upload-icon">+</text>
          </view>
        </view>
      </view>

      <!-- 匿名设置 -->
      <view class="anonymous-setting">
        <label class="anonymous-label">
          <checkbox :checked="isAnonymous" @click="toggleAnonymous" color="#007aff" />
          <text>匿名发布</text>
        </label>

        <!-- 匿名配置 -->
        <view v-if="isAnonymous" class="anonymous-config">
          <view class="avatar-section">
            <text class="config-label">匿名头像：</text>
            <view class="avatar-grid">
              <view class="avatar-item" v-for="(avatar, index) in anonymousAvatars" :key="index"
                :class="{ selected: selectedAvatarIndex === index }" @click="selectAvatar(index)">
                <image :src="avatar" class="avatar-image" mode="aspectFill" />
              </view>
            </view>
          </view>

          <view class="name-section">
            <text class="config-label">匿名名称：</text>
            <view class="name-config">
              <input class="anonymous-name-input" v-model="customAnonymousName" :placeholder="defaultAnonymousName"
                maxlength="20" />
              <view class="name-regenerate" @click="generateRandomName">
                <text>🎲</text>
              </view>
            </view>
            <text class="name-hint">留空使用默认名称，或自定义名称</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      whisperTitle: '',
      whisperContent: '',
      selectedMood: 'neutral',
      selectedTags: [],
      currentTag: '',
      showTagInput: false,
      presetTags: ['心情', '秘密', '困扰', '感悟', '日常', '吐槽', '想法', '回忆'],
      uploadedImages: [],
      isAnonymous: true,
      isPublishing: false,
      moodOptions: [
        { value: 'very_happy', emoji: '😄' },
        { value: 'happy', emoji: '😊' },
        { value: 'neutral', emoji: '😐' },
        { value: 'sad', emoji: '😢' },
        { value: 'very_sad', emoji: '😭' }
      ],
      // 匿名相关 - 使用实际存在的头像路径
      anonymousAvatars: [
        '/src/static/avatar/头像.png',
        '/src/static/avatar/头像 (2).png',
        '/src/static/avatar/头像 (3).png',
        '/src/static/avatar/头像 (4).png',
        '/src/static/avatar/头像 (5).png',
        '/src/static/avatar/头像 (6).png',
        '/src/static/avatar/头像 (7).png',
        '/src/static/avatar/头像 (8).png',
        '/src/static/avatar/头像 (9).png'
      ],
      selectedAvatarIndex: 0,
      customAnonymousName: '',
      defaultAnonymousName: ''
    }
  },

  computed: {
    canPublish() {
      return this.whisperContent.trim().length > 0;
    },

    finalAnonymousName() {
      return this.customAnonymousName.trim() || this.defaultAnonymousName;
    }
  },

  mounted() {
    this.generateRandomName();
  },

  methods: {
    // 心情选择
    selectMood(mood) {
      this.selectedMood = mood;
    },

    // 标签相关方法
    addTag() {
      const tag = this.currentTag.trim();
      if (tag && !this.selectedTags.includes(tag) && this.selectedTags.length < 5) {
        this.selectedTags.push(tag);
        this.currentTag = '';
      }
    },

    removeTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index > -1) {
        this.selectedTags.splice(index, 1);
      }
    },

    selectPresetTag(tag) {
      if (!this.selectedTags.includes(tag) && this.selectedTags.length < 5) {
        this.selectedTags.push(tag);
      }
    },

    hideTagInput() {
      setTimeout(() => {
        if (!this.currentTag.trim()) {
          this.showTagInput = false;
        }
      }, 200);
    },

    // 图片上传相关方法
    chooseImage() {
      uni.chooseImage({
        count: 9 - this.uploadedImages.length,
        sizeType: ['original', 'compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          // 将选择的图片添加到uploadedImages数组中
          const newImages = res.tempFilePaths.map((path) => ({
            tempUrl: path,    // 临时路径用于预览
            url: '',          // 实际URL（上传后填充）
            uploaded: false   // 标记是否已上传
          }));
          this.uploadedImages = [...this.uploadedImages, ...newImages];

          // 自动上传新选择的图片
          this.uploadNewImages();
        }
      });
    },

    async uploadNewImages() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      // 上传还未上传的图片
      for (let i = 0; i < this.uploadedImages.length; i++) {
        const image = this.uploadedImages[i];
        if (!image.uploaded && image.tempUrl) {
          try {
            const result = await api.uploadImage(image.tempUrl, token);
            // 更新图片信息
            this.uploadedImages[i].url = result.url;
            this.uploadedImages[i].uploaded = true;
          } catch (error) {
            console.error('图片上传失败:', error);
            uni.showToast({
              title: '图片上传失败',
              icon: 'none'
            });
          }
        }
      }
    },

    removeImage(index) {
      this.uploadedImages.splice(index, 1);
    },

    // 匿名相关方法
    toggleAnonymous() {
      this.isAnonymous = !this.isAnonymous;
    },

    selectAvatar(index) {
      this.selectedAvatarIndex = index;
    },

    generateRandomName() {
      const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for (let i = 0; i < 5; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      this.defaultAnonymousName = `ariadne_${result}`;
    },

    cancel() {
      uni.navigateBack();
    },

    getImageUrl(imageUrl) {
      if (imageUrl.startsWith('http')) {
        return imageUrl;
      }
      const baseUrl = process.env.VUE_APP_API_BASE_URL;
      if (!baseUrl) {
        console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
        return imageUrl;
      }
      if (imageUrl.startsWith('/')) {
        return baseUrl + imageUrl;
      } else {
        return baseUrl + '/' + imageUrl;
      }
    },

    async publish() {
      if (!this.canPublish) {
        uni.showToast({
          title: '请输入悄悄话内容',
          icon: 'none'
        });
        return;
      }

      if (this.isPublishing) {
        return; // 防止重复点击
      }

      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      // 检查是否所有图片都已上传
      const uploadingImages = this.uploadedImages.filter(img => !img.uploaded);
      if (uploadingImages.length > 0) {
        uni.showToast({
          title: '请等待图片上传完成',
          icon: 'none'
        });
        return;
      }

      this.isPublishing = true;
      uni.showLoading({
        title: '发布中...'
      });

      try {
        // 准备图片数据
        const imageUrls = this.uploadedImages.map((image, index) => ({
          image_url: image.url,
          image_order: index
        }));

        // 创建悄悄话数据
        const whisperData = {
          title: this.whisperTitle.trim() || this.whisperContent.substring(0, 20) + (this.whisperContent.length > 20 ? '...' : ''),
          content: this.whisperContent,
          mood: this.selectedMood,
          tags: this.selectedTags.length > 0 ? this.selectedTags : null,
          is_anonymous: this.isAnonymous,
          anonymous_name: this.isAnonymous ? this.finalAnonymousName : null,
          anonymous_avatar: this.isAnonymous ? this.anonymousAvatars[this.selectedAvatarIndex] : null,
          images: imageUrls
        };

        const result = await api.createWhisper(token, whisperData);

        if (result.whisper_id) {
          uni.hideLoading();
          
          // 发布成功后,领取奖励
          this.claimWhisperReward(token);
          
          uni.showToast({
            title: '发布成功',
            icon: 'success'
          });

          // 发布成功后跳转到我的悄悄话页面
          setTimeout(() => {
            uni.navigateBack({
              delta: 1
            });
          }, 1500);
        }
      } catch (error) {
        this.isPublishing = false;
        uni.hideLoading();
        console.error('发布失败:', error);
        uni.showToast({
          title: '发布失败: ' + (error.message || ''),
          icon: 'none'
        });
      }
    },

    // 领取发布悄悄话奖励
    async claimWhisperReward(token) {
      try {
        const response = await api.claimWhisperReward(token);

        if (response.success) {
          // 显示奖励提示
          console.log(`💧 发布奖励: 获得${response.water_drops_earned}水滴, 今日剩余${response.remaining_rewards_today}次机会`);
          
          // 可选：在发布成功提示后显示奖励
          setTimeout(() => {
            uni.showToast({
              title: `+${response.water_drops_earned}💧`,
              icon: 'none',
              duration: 1500
            });
          }, 800);
        } else {
          // 已达上限,不显示提示
          console.log(`💧 ${response.message}`);
        }
      } catch (error) {
        console.error("Failed to claim whisper reward:", error);
        // 奖励失败不影响发布功能,静默处理
      }
    }
  }
}
</script>

<style scoped>
.write-whisper-container {
  height: 100vh;
  background-color: #f8f8f8;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 30rpx;
  background-color: white;
  border-bottom: 1rpx solid #eee;
}

.header-left,
.header-right {
  flex: 1;
}

.cancel-btn,
.publish-btn {
  font-size: 32rpx;
  color: #007aff;
}

.publish-btn.disabled {
  color: #ccc;
}

.content {
  padding: 30rpx;
}

.title-input-section {
  background-color: white;
  border-radius: 20rpx;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
}

.whisper-title {
  width: 100%;
  height: 80rpx;
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
}

.whisper-content {
  width: 100%;
  height: 300rpx;
  padding: 20rpx;
  background-color: white;
  border-radius: 20rpx;
  box-sizing: border-box;
  font-size: 30rpx;
  margin-bottom: 20rpx;
  line-height: 1.6;
}

.content-info {
  text-align: right;
  margin-bottom: 30rpx;
}

.word-count {
  font-size: 24rpx;
  color: #999;
}

.tag-selector {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.tag-label {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
  margin-bottom: 20rpx;
}

.tag-item {
  display: flex;
  align-items: center;
  background-color: #007aff;
  color: white;
  padding: 10rpx 20rpx;
  border-radius: 30rpx;
  font-size: 26rpx;
}

.tag-text {
  margin-right: 10rpx;
}

.tag-remove {
  font-size: 32rpx;
  font-weight: bold;
}

.tag-input {
  flex: 1;
  min-width: 150rpx;
  height: 50rpx;
  padding: 10rpx 20rpx;
  background-color: #f5f5f5;
  border-radius: 30rpx;
  font-size: 26rpx;
}

.add-tag-btn {
  padding: 10rpx 20rpx;
  background-color: #f5f5f5;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #666;
}

.preset-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.preset-tag {
  padding: 10rpx 20rpx;
  background-color: #f0f0f0;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #666;
}

.mood-selector {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.mood-label {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.mood-options {
  display: flex;
  gap: 20rpx;
}

.mood-option {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  font-size: 40rpx;
}

.mood-option.selected {
  background-color: #007aff;
  color: white;
}

.image-upload {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.image-label {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.image-item {
  position: relative;
  width: 150rpx;
  height: 150rpx;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  border-radius: 10rpx;
}

.remove-image {
  position: absolute;
  top: -15rpx;
  right: -15rpx;
  width: 40rpx;
  height: 40rpx;
  background-color: #ff4d4f;
  border-radius: 50%;
  color: white;
  font-size: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.uploading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 10rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.uploading-text {
  color: white;
  font-size: 20rpx;
}

.image-upload-btn {
  width: 150rpx;
  height: 150rpx;
  border: 2rpx dashed #ccc;
  border-radius: 10rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  font-size: 60rpx;
  color: #ccc;
}

.anonymous-setting {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
}

.anonymous-label {
  display: flex;
  align-items: center;
  font-size: 30rpx;
  color: #333;
  margin-bottom: 20rpx;
}

.anonymous-label checkbox {
  margin-right: 20rpx;
}

.anonymous-config {
  margin-top: 20rpx;
}

.avatar-section {
  margin-bottom: 30rpx;
}

.config-label {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 15rpx;
  display: block;
}

.avatar-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15rpx;
  margin-bottom: 20rpx;
}

.avatar-item {
  aspect-ratio: 1;
  border: 3rpx solid transparent;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-item.selected {
  border-color: #007aff;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.name-section {
  margin-top: 20rpx;
}

.name-config {
  display: flex;
  align-items: center;
  gap: 15rpx;
  margin-bottom: 10rpx;
}

.anonymous-name-input {
  flex: 1;
  padding: 15rpx;
  border: 1rpx solid #ddd;
  border-radius: 10rpx;
  font-size: 28rpx;
  background-color: #f8f8f8;
}

.name-regenerate {
  padding: 15rpx;
  background-color: #f0f0f0;
  border-radius: 10rpx;
  font-size: 28rpx;
}

.name-hint {
  font-size: 24rpx;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .avatar-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>