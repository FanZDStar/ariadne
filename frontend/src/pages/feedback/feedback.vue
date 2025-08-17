<template>
  <view class="feedback-container">
    <view class="header">
      <view class="header-left" @click="cancel">
        <text class="cancel-btn">取消</text>
      </view>
      <view class="header-title">
        <text class="title">意见反馈</text>
      </view>
      <view class="header-right" @click="submitFeedback">
        <text class="submit-btn" :class="{ disabled: !canSubmit || isSubmitting }">
          {{ isSubmitting ? '提交中...' : '提交' }}
        </text>
      </view>
    </view>

    <view class="content">
      <!-- 标题输入 -->
      <view class="input-section">
        <text class="section-title">反馈标题</text>
        <input 
          class="title-input" 
          placeholder="请输入反馈标题" 
          v-model="feedbackTitle"
          maxlength="50"
        />
      </view>

      <!-- 反馈内容 -->
      <view class="input-section">
        <text class="section-title">反馈内容</text>
        <textarea 
          class="content-textarea" 
          placeholder="请详细描述您遇到的问题或建议..." 
          v-model="feedbackContent"
          maxlength="1000"
        />
        <view class="char-count">
          <text>{{ feedbackContent.length }}/1000</text>
        </view>
      </view>

      <!-- 图片上传 -->
      <view class="input-section">
        <text class="section-title">图片上传（最多6张）</text>
        <view class="image-grid">
          <view 
            class="image-item" 
            v-for="(image, index) in uploadedImages" 
            :key="index"
          >
            <image :src="image.tempUrl || image.url" class="uploaded-image" mode="aspectFill" />
            <view class="remove-image" @click="removeImage(index)">×</view>
            <view v-if="!image.uploaded" class="uploading-overlay">
              <text class="uploading-text">上传中...</text>
            </view>
          </view>
          <view 
            class="image-upload-btn" 
            v-if="uploadedImages.length < 6"
            @click="chooseImage"
          >
            <text class="upload-icon">+</text>
          </view>
        </view>
      </view>

      <!-- 联系方式 -->
      <view class="input-section">
        <text class="section-title">联系方式（可选）</text>
        <input 
          class="contact-input" 
          placeholder="邮箱或手机号，方便我们联系您" 
          v-model="contactInfo"
        />
      </view>

      <!-- 使用心情 -->
      <view class="input-section">
        <text class="section-title">使用应用的心情</text>
        <view class="mood-selector">
          <view 
            class="mood-option" 
            v-for="mood in moodOptions" 
            :key="mood.value"
            :class="{ selected: selectedMood === mood.value }"
            @click="selectMood(mood.value)"
          >
            <text class="mood-emoji">{{ mood.emoji }}</text>
            <text class="mood-label">{{ mood.label }}</text>
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
      feedbackTitle: '',
      feedbackContent: '',
      contactInfo: '',
      selectedMood: 'neutral',
      uploadedImages: [],
      isSubmitting: false,
      moodOptions: [
        { value: 'very_happy', emoji: '😄', label: '非常满意' },
        { value: 'happy', emoji: '😊', label: '满意' },
        { value: 'neutral', emoji: '😐', label: '一般' },
        { value: 'sad', emoji: '😢', label: '不满意' },
        { value: 'very_sad', emoji: '😭', label: '非常不满意' }
      ]
    }
  },

  computed: {
    canSubmit() {
      return this.feedbackTitle.trim().length > 0 && this.feedbackContent.trim().length > 0;
    }
  },

  methods: {
    selectMood(mood) {
      this.selectedMood = mood;
    },

    chooseImage() {
      uni.chooseImage({
        count: 6 - this.uploadedImages.length,
        sizeType: ['compressed'],
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

    cancel() {
      uni.navigateBack();
    },

    async submitFeedback() {
      if (!this.canSubmit) {
        if (!this.feedbackTitle.trim()) {
          uni.showToast({
            title: '请输入反馈标题',
            icon: 'none'
          });
          return;
        }
        if (!this.feedbackContent.trim()) {
          uni.showToast({
            title: '请输入反馈内容',
            icon: 'none'
          });
          return;
        }
        return;
      }

      if (this.isSubmitting) {
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

      this.isSubmitting = true;
      uni.showLoading({
        title: '提交中...'
      });

      try {
        // 准备图片数据
        const imageUrls = this.uploadedImages.map((image) => ({
          image_url: image.url
        }));

        // 创建反馈
        const feedbackData = {
          title: this.feedbackTitle,
          content: this.feedbackContent,
          contact_info: this.contactInfo || null,
          images: imageUrls
        };

        const result = await api.createFeedback(token, feedbackData);

        if (result.feedback_id) {
          uni.hideLoading();
          uni.showToast({
            title: '反馈提交成功',
            icon: 'success'
          });

          // 2秒后返回上一页
          setTimeout(() => {
            uni.navigateBack();
          }, 2000);
        }
      } catch (error) {
        this.isSubmitting = false;
        uni.hideLoading();
        console.error('反馈提交失败:', error);
        uni.showToast({
          title: '提交失败: ' + (error.message || ''),
          icon: 'none'
        });
      }
    }
  }
}
</script>

<style scoped>
.feedback-container {
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

.header-title {
  flex: 2;
  text-align: center;
}

.cancel-btn,
.submit-btn {
  font-size: 32rpx;
  color: #007aff;
}

.submit-btn.disabled {
  color: #ccc;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.content {
  padding: 30rpx;
}

.input-section {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.title-input {
  width: 100%;
  height: 80rpx;
  padding: 20rpx;
  font-size: 30rpx;
  border: 1rpx solid #eee;
  border-radius: 10rpx;
  box-sizing: border-box;
}

.content-textarea {
  width: 100%;
  height: 200rpx;
  padding: 20rpx;
  font-size: 30rpx;
  border: 1rpx solid #eee;
  border-radius: 10rpx;
  box-sizing: border-box;
  margin-bottom: 10rpx;
}

.char-count {
  text-align: right;
  font-size: 24rpx;
  color: #999;
}

.contact-input {
  width: 100%;
  height: 80rpx;
  padding: 20rpx;
  font-size: 30rpx;
  border: 1rpx solid #eee;
  border-radius: 10rpx;
  box-sizing: border-box;
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

.mood-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.mood-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx;
  background-color: #f5f5f5;
  border-radius: 20rpx;
  width: calc(33.33% - 14rpx);
  box-sizing: border-box;
}

.mood-option.selected {
  background-color: #007aff;
  color: white;
}

.mood-emoji {
  font-size: 48rpx;
  margin-bottom: 10rpx;
}

.mood-label {
  font-size: 24rpx;
  text-align: center;
}

.mood-option.selected .mood-label {
  color: white;
}
</style>