<template>
  <view class="background-settings-container">
    <!-- 导航栏 -->
    <view class="navbar">
      <view class="navbar-left" @click="goBack">
        <text class="back-icon">←</text>
        <text class="back-text">返回</text>
      </view>
      <text class="navbar-title">背景设置</text>
    </view>

    <!-- 当前背景预览 -->
    <view class="current-preview" :style="getCurrentBackgroundStyle()">
      <text class="preview-label">当前背景预览</text>
    </view>

    <!-- 背景管理内容 -->
    <view class="settings-content">
      <scroll-view class="settings-scroll" scroll-y>
        <!-- 状态提示 -->
        <view class="status-section">
          <text class="status-title">
            {{
              userBackgrounds.length > 0
                ? "当前使用：自定义背景"
                : "当前使用：默认背景"
            }}
          </text>
          <text class="status-desc">
            {{
              userBackgrounds.length > 0
                ? `已上传 ${userBackgrounds.length}/4 张自定义背景，自动轮播`
                : "使用默认的4种颜色背景，自动轮播"
            }}
          </text>
        </view>

        <!-- 自定义背景管理 -->
        <view class="section">
          <view class="section-header">
            <text class="section-title">自定义背景 ({{ userBackgrounds.length }}/4)</text>
            <view class="action-buttons">
              <view class="add-btn" @click="chooseBackgroundImage" v-if="userBackgrounds.length < 4">
                <text class="btn-text">+ 添加</text>
              </view>
              <view class="restore-btn" @click="restoreDefaultBackgrounds" v-if="userBackgrounds.length > 0">
                <text class="btn-text">恢复默认</text>
              </view>
            </view>
          </view>

          <!-- 自定义背景列表 -->
          <view class="backgrounds-grid" v-if="userBackgrounds.length > 0">
            <view v-for="(bg, index) in userBackgrounds" :key="bg.id" class="background-item user-bg"
              :style="{ backgroundImage: `url(${getImageUrl(bg.url)})` }">
              <view class="bg-overlay">
                <text class="bg-name">{{
                  bg.original_filename || "自定义背景"
                }}</text>
                <view class="delete-btn" @click="confirmDeleteBackground(bg)">
                  <text class="delete-icon">🗑️</text>
                </view>
              </view>
            </view>

            <!-- 空位显示（最多4个） -->
            <view v-for="n in 4 - userBackgrounds.length" :key="'empty-' + n" class="background-item empty-slot"
              @click="chooseBackgroundImage">
              <text class="add-icon">+</text>
              <text class="add-text">添加背景</text>
            </view>
          </view>

          <!-- 无自定义背景时的提示 -->
          <view class="empty-section" v-if="userBackgrounds.length === 0">
            <text class="empty-title">暂无自定义背景</text>
            <text class="empty-desc">点击"+ 添加"上传你喜欢的背景图片，最多可上传4张</text>
            <view class="upload-btn" @click="chooseBackgroundImage">
              <text class="upload-text">📷 选择图片</text>
            </view>
          </view>
        </view>

        <!-- 默认背景预览（仅在没有自定义背景时显示） -->
        <view class="section" v-if="userBackgrounds.length === 0">
          <view class="section-header">
            <text class="section-title">默认背景预览</text>
          </view>

          <view class="backgrounds-grid">
            <view v-for="bg in defaultBackgrounds" :key="bg.id" class="background-item default-bg"
              :style="{ backgroundColor: bg.color }">
              <text class="bg-name">{{ bg.name }}</text>
            </view>
          </view>
        </view>

        <!-- 使用说明 -->
        <view class="help-section">
          <text class="help-title">使用说明</text>
          <text class="help-item">• 背景图片会自动轮播，每5秒切换一次</text>
          <text class="help-item">• 最多可上传4张自定义背景图片</text>
          <text class="help-item">• 支持 JPG、PNG、GIF、WebP 格式</text>
          <text class="help-item">• 单张图片最大5MB</text>
          <text class="help-item">• 恢复默认会删除所有自定义背景</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { api, storage } from "../../utils/api.js";

export default {
  data() {
    return {
      userBackgrounds: [],
      defaultBackgrounds: [
        { id: "default_1", name: "粉色心情", color: "#ffafcc" },
        { id: "default_2", name: "蓝色忧郁", color: "#a2d2ff" },
        { id: "default_3", name: "温柔时光", color: "#ffcad4" },
        { id: "default_4", name: "紫色梦境", color: "#cdb4db" },
      ],
    };
  },

  onLoad() {
    this.loadBackgrounds();
  },

  onShow() {
    this.loadBackgrounds();
  },

  methods: {
    async loadBackgrounds() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      try {
        const userBgs = await api.getUserDiaryBackgrounds(token);
        this.userBackgrounds = userBgs;
      } catch (error) {
        console.error("获取背景图片失败:", error);
        uni.showToast({
          title: "获取背景失败",
          icon: "none",
        });
      }
    },

    chooseBackgroundImage() {
      if (this.userBackgrounds.length >= 4) {
        uni.showToast({
          title: "最多只能上传4张背景图片",
          icon: "none",
        });
        return;
      }

      uni.chooseImage({
        count: Math.min(4 - this.userBackgrounds.length, 3),
        sizeType: ["compressed"],
        sourceType: ["camera", "album"],
        success: (res) => {
          this.uploadBackgroundImages(res.tempFilePaths);
        },
        fail: (error) => {
          console.error("选择图片失败:", error);
        },
      });
    },

    async uploadBackgroundImages(filePaths) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      uni.showLoading({ title: "上传中..." });

      try {
        let starMessageShown = false;
        for (const filePath of filePaths) {
          const result = await api.uploadUserDiaryBackground(filePath, token);

          // 处理星星奖励
          if (result && result.star_awarded && !starMessageShown) {
            // 显示星星奖励提示
            uni.showToast({
              title: result.star_message || "获得1颗星星！",
              icon: "success",
              duration: 2000
            });
            starMessageShown = true;
          }
        }

        uni.hideLoading();

        if (!starMessageShown) {
          uni.showToast({
            title: "上传成功",
            icon: "success",
          });
        }

        await this.loadBackgrounds();
      } catch (error) {
        uni.hideLoading();
        console.error("上传背景图片失败:", error);
        uni.showToast({
          title: error.message || "上传失败",
          icon: "none",
        });
      }
    },

    confirmDeleteBackground(background) {
      uni.showModal({
        title: "确认删除",
        content: "确定要删除这张背景图片吗？",
        success: (res) => {
          if (res.confirm) {
            this.deleteBackground(background.id);
          }
        },
      });
    },

    async deleteBackground(backgroundId) {
      const token = storage.getToken();
      if (!token) return;

      try {
        uni.showLoading({ title: "删除中..." });
        await api.deleteUserDiaryBackground(token, backgroundId);

        uni.hideLoading();
        uni.showToast({
          title: "删除成功",
          icon: "success",
        });

        await this.loadBackgrounds();
      } catch (error) {
        uni.hideLoading();
        console.error("删除背景图片失败:", error);
        uni.showToast({
          title: "删除失败",
          icon: "none",
        });
      }
    },

    restoreDefaultBackgrounds() {
      uni.showModal({
        title: "恢复默认背景",
        content:
          "确定要删除所有自定义背景图片，恢复默认背景吗？此操作不可撤销。",
        success: async (res) => {
          if (res.confirm) {
            const token = storage.getToken();
            if (!token) {
              uni.showToast({
                title: "请先登录",
                icon: "none",
              });
              return;
            }

            try {
              uni.showLoading({ title: "恢复中..." });
              await api.restoreDefaultDiaryBackgrounds(token);

              uni.hideLoading();
              uni.showToast({
                title: "已恢复默认背景",
                icon: "success",
              });

              await this.loadBackgrounds();
            } catch (error) {
              uni.hideLoading();
              console.error("恢复默认背景失败:", error);
              uni.showToast({
                title: error.message || "恢复失败",
                icon: "none",
              });
            }
          }
        },
      });
    },

    getCurrentBackgroundStyle() {
      if (this.userBackgrounds.length > 0) {
        const bg = this.userBackgrounds[0];
        return {
          backgroundImage: `url(${this.getImageUrl(bg.url)})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        };
      } else {
        return { backgroundColor: "#ffafcc" };
      }
    },

    getImageUrl(imageUrl) {
      if (imageUrl.startsWith("http")) {
        return imageUrl;
      }
      const baseUrl = process.env.VUE_APP_API_BASE_URL;
      if (!baseUrl) {
        console.error("❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!");
        return imageUrl;
      }
      if (imageUrl.startsWith("/")) {
        return baseUrl + imageUrl;
      } else {
        return baseUrl + "/" + imageUrl;
      }
    },

    goBack() {
      uni.navigateBack();
    },
  },
};
</script>

<style scoped>
.background-settings-container {
  height: 100vh;
  background-color: #f5f5f5;
  padding-top: var(--status-bar-height);
}

.navbar {
  height: 44px;
  background-color: #ffafcc;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.navbar-left {
  position: absolute;
  left: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.back-icon {
  font-size: 32rpx;
  color: white;
  margin-right: 8rpx;
}

.back-text {
  font-size: 28rpx;
  color: white;
}

.navbar-title {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
}

.current-preview {
  height: 300rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.preview-label {
  font-size: 32rpx;
  color: white;
  font-weight: bold;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.5);
}

.settings-content {
  flex: 1;
  height: calc(100vh - var(--status-bar-height) - 44px - 300rpx);
}

.settings-scroll {
  height: 100%;
  padding: 30rpx;
}

.status-section {
  background-color: white;
  padding: 30rpx;
  border-radius: 20rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.status-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.status-desc {
  display: block;
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}

.section {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 16rpx;
}

.add-btn {
  padding: 12rpx 24rpx;
  background-color: #007aff;
  border-radius: 24rpx;
}

.restore-btn {
  padding: 12rpx 24rpx;
  background-color: #ff9500;
  border-radius: 24rpx;
}

.btn-text {
  font-size: 24rpx;
  color: white;
  font-weight: 500;
}

.backgrounds-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.background-item {
  aspect-ratio: 16/9;
  border-radius: 16rpx;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-bg {
  background-size: cover;
  background-position: center;
}

.default-bg {
  color: white;
  font-weight: bold;
}

.empty-slot {
  border: 2rpx dashed #ccc;
  background-color: #f8f9fa;
  flex-direction: column;
  color: #999;
}

.add-icon {
  font-size: 48rpx;
  margin-bottom: 8rpx;
}

.add-text {
  font-size: 24rpx;
}

.bg-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  padding: 24rpx 16rpx 16rpx;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.bg-name {
  font-size: 20rpx;
  color: white;
  font-weight: 500;
  max-width: 200rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.delete-btn {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
}

.delete-icon {
  font-size: 24rpx;
}

.empty-section {
  text-align: center;
  padding: 60rpx 30rpx;
}

.empty-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.empty-desc {
  display: block;
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 30rpx;
}

.upload-btn {
  display: inline-block;
  padding: 20rpx 40rpx;
  background-color: #007aff;
  border-radius: 30rpx;
}

.upload-text {
  font-size: 28rpx;
  color: white;
  font-weight: 500;
}

.help-section {
  background-color: #f8f9fa;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.help-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.help-item {
  display: block;
  font-size: 24rpx;
  color: #666;
  line-height: 1.8;
  margin-bottom: 8rpx;
}
</style>
