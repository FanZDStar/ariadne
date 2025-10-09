<template>
  <view class="write-diary-container">
    <view class="header">
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
      <!-- 日记标题输入 -->
      <view class="title-input-section">
        <input class="diary-title" placeholder="给日记起个标题吧..." v-model="diaryTitle" maxlength="50" />
      </view>

      <!-- 日记内容输入 -->
      <textarea class="diary-content" placeholder="记录你的心情..." v-model="diaryContent" maxlength="500" />

      <view class="content-info">
        <text class="word-count">{{ diaryContent.length }}/500</text>
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

      <view class="mood-selector">
        <text class="mood-label">心情：</text>
        <view class="mood-options">
          <view class="mood-option" v-for="mood in moodOptions" :key="mood.value"
            :class="{ selected: selectedMood === mood.value }" @click="selectMood(mood.value)">
            <text class="mood-emoji">{{ mood.emoji }}</text>
          </view>
        </view>
      </view>

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
          <view class="image-upload-btn" v-if="uploadedImages.length < 6" @click="chooseImage">
            <text class="upload-icon">+</text>
          </view>
        </view>
      </view>

      <!-- 已移除：私密设置功能 -->
      <!-- <view class="privacy-setting">
        <label class="privacy-label">
          <checkbox :checked="isPrivate" @click="togglePrivacy" color="#007aff" />
          <text>设为私密</text>
        </label>
      </view> -->
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      diaryTitle: '',
      diaryContent: '',
      selectedMood: 'neutral',
      // isPrivate: true,  // 已移除：不再支持私密日记功能
      uploadedImages: [],
      isPublishing: false,
      selectedTags: [],
      currentTag: '',
      showTagInput: false,
      presetTags: ['日常', '心情', '学习', '工作', '旅行', '美食', '运动', '思考'],
      moodOptions: [
        { value: 'very_happy', emoji: '😄' },
        { value: 'happy', emoji: '😊' },
        { value: 'neutral', emoji: '😐' },
        { value: 'sad', emoji: '😢' },
        { value: 'very_sad', emoji: '😭' }
      ]
    }
  },

  computed: {
    canPublish() {
      return this.diaryContent.trim().length > 0;
    }
  },

  methods: {
    selectMood(mood) {
      this.selectedMood = mood;
    },

    // 已移除：私密日记功能
    // togglePrivacy() {
    //   this.isPrivate = !this.isPrivacy;
    // },

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

    chooseImage() {
      uni.chooseImage({
        count: 6 - this.uploadedImages.length,
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

    // 修改removeImage方法中的图片显示
    removeImage(index) {
      this.uploadedImages.splice(index, 1);
    },

    cancel() {
      uni.navigateBack();
    },

    // 添加这个方法
    getImageUrl(imageUrl) {
      // 如果已经是完整URL，直接返回
      if (imageUrl.startsWith('http')) {
        return imageUrl;
      }

      // 如果是相对路径，拼接基础URL
      const baseUrl = process.env.VUE_APP_API_BASE_URL;
      // const baseUrl = 'http://127.0.0.1:8000';
      if (!baseUrl) {
        console.error('❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!');
        return imageUrl; // 返回原始路径
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
          title: '请输入日记内容',
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

        // 创建日记（已移除私密功能）
        const diaryData = {
          title: this.diaryTitle.trim() || this.diaryContent.substring(0, 20) + (this.diaryContent.length > 20 ? '...' : ''),
          content: this.diaryContent,
          mood: this.selectedMood,
          // is_private: this.isPrivate,  // 已移除：不再支持私密日记
          tags: this.selectedTags.length > 0 ? this.selectedTags : null,
          images: imageUrls
        };

        const result = await api.createDiary(token, diaryData);

        if (result.diary_id) {
          uni.hideLoading();
          
          // 显示发布成功消息
          uni.showToast({
            title: '发布成功',
            icon: 'success'
          });

          // 如果获得了星星奖励，显示奖励消息
          if (result.star_awarded && result.star_points > 0) {
            setTimeout(() => {
              uni.showToast({
                title: result.star_message || `获得了${result.star_points}颗星星 ⭐`,
                icon: 'none',
                duration: 3000
              });
            }, 1500);
          }

          // 3秒后跳转到日记页面
          setTimeout(() => {
            uni.redirectTo({
              url: '/pages/diary/diary'
            });
          }, 3000);
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
    }
  }
}
</script>

<style scoped>
.write-diary-container {
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

.diary-title {
  width: 100%;
  height: 80rpx;
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
}

.diary-content {
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

/* 已移除：私密日记功能相关样式 */
/* .privacy-setting {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
}

.privacy-label {
  display: flex;
  align-items: center;
  font-size: 30rpx;
  color: #333;
}

.privacy-label checkbox {
  margin-right: 20rpx;
} */
</style>