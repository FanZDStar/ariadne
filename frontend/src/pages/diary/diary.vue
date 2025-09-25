<template>
  <view class="diary-container">
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="back-to-journey" v-if="isAtTop" @click="goBackToJourney">
          <text class="back-icon">←</text>
        </view>
        <view
          class="back-to-top-hint"
          v-if="showBackToTopHint"
          @click="scrollToTop"
        >
          <text class="back-icon">↑</text>
          <text class="back-text">回到顶部</text>
        </view>

        <text class="navbar-title" :class="{ hidden: showBackToTopHint }">
          碎碎念
        </text>

        <view class="manage-btn" @click="toggleManagementMode">
          <view class="manage-icon-wrapper">
            <text class="manage-icon">{{
              managementMode ? "完成" : "管理"
            }}</text>
          </view>
        </view>

        <view class="background-settings-btn" @click="goToBackgroundSettings">
          <view class="settings-icon-wrapper">
            <text class="bg-settings-icon">🎨</text>
          </view>
        </view>
      </view>
    </view>

    <view
      class="background-section"
      :style="{ height: backgroundHeight + 'px' }"
    >
      <!-- 当前背景显示 -->
      <view class="current-background" :style="getCurrentBackgroundStyle()">
        <text
          class="background-label"
          v-if="allBackgrounds[currentBackgroundIndex]"
        >
          {{ allBackgrounds[currentBackgroundIndex].name || "自定义背景" }}
        </text>
      </view>

      <!-- 背景指示点 -->
      <view class="background-indicators" v-if="allBackgrounds.length > 1">
        <view
          v-for="(bg, index) in allBackgrounds"
          :key="bg.id || bg.name"
          class="indicator-dot"
          :class="{ active: index === currentBackgroundIndex }"
        ></view>
      </view>

      <view class="new-diary-btn" @click="createNewDiary">
        <text class="btn-text">✍️ 写日记</text>
      </view>
    </view>

    <view class="diary-content">
      <scroll-view
        class="diary-scroll-view"
        scroll-y
        @scroll="onScroll"
        :scroll-top="scrollTop"
        :enable-back-to-top="true"
        ref="scrollView"
        id="scrollView"
      >
        <view class="diary-list">
          <view
            class="diary-item"
            v-for="diary in diaryList"
            :key="diary.diary_id"
          >
            <view class="diary-header">
              <text class="diary-date">{{
                formatDiaryDate(diary.created_at)
              }}</text>
              <text class="diary-time">{{
                formatDiaryTime(diary.created_at)
              }}</text>
            </view>
            <view class="diary-main-content">
              <text class="content-text">{{ diary.content }}</text>
            </view>

            <view
              class="diary-images"
              v-if="diary.images && diary.images.length > 0"
            >
              <view
                class="image-grid"
                :class="{
                  'single-image': diary.images.length === 1,
                  'multi-images': diary.images.length > 1,
                }"
              >
                <view
                  class="image-wrapper"
                  v-for="image in diary.images.slice(0, 9)"
                  :key="image.image_id"
                >
                  <image
                    :src="getImageUrl(image.image_url)"
                    class="diary-image"
                    mode="aspectFill"
                    @click="previewImage(diary.images, image.image_url)"
                  />
                </view>

                <view
                  class="image-wrapper more-images"
                  v-if="diary.images.length > 9"
                >
                  <text class="more-count">+{{ diary.images.length - 9 }}</text>
                </view>
              </view>
            </view>

            <view class="diary-footer">
              <view class="mood-tag">
                <text>{{ getMoodEmoji(diary.mood) }}</text>
              </view>
              <view
                v-if="managementMode"
                class="delete-btn"
                @click="confirmDelete(diary.diary_id)"
              >
                <text class="delete-icon">🗑️</text>
              </view>
            </view>
          </view>

          <view v-if="diaryList.length === 0" class="empty-diary">
            <text class="empty-text"
              >还没有写过日记，点击右上角开始记录吧！</text
            >
          </view>
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
      diaryList: [],
      scrollTop: 0,
      backgroundHeight: Math.round(uni.getSystemInfoSync().windowHeight * 0.4),
      maxBackgroundHeight: Math.round(
        uni.getSystemInfoSync().windowHeight * 0.4
      ),
      minBackgroundHeight: 80,
      showBackToTopHint: false,
      scrollThreshold: 300,
      isAtTop: true,
      managementMode: false,

      // 简化的背景配置
      defaultBackgrounds: [
        { id: "default_1", name: "粉色心情", color: "#ffafcc", type: "color" },
        { id: "default_2", name: "蓝色忧郁", color: "#a2d2ff", type: "color" },
        { id: "default_3", name: "温柔时光", color: "#ffcad4", type: "color" },
        { id: "default_4", name: "紫色梦境", color: "#cdb4db", type: "color" },
      ],
      userBackgrounds: [],
      allBackgrounds: [],
      currentBackgroundIndex: 0,
      autoPlayTimer: null,
      autoPlayInterval: 5000, // 5秒轮播间隔
    };
  },

  onLoad() {
    this.loadDiaries();
    this.loadBackgrounds();
    this.startAutoPlay();
  },

  onShow() {
    this.loadDiaries();
    this.loadBackgrounds();
    this.startAutoPlay();
  },

  onHide() {
    this.stopAutoPlay();
  },

  onUnload() {
    this.stopAutoPlay();
  },

  methods: {
    async loadDiaries() {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      try {
        const diaries = await api.getUserDiaries(token);
        this.diaryList = diaries;
      } catch (error) {
        console.error("获取日记失败:", error);
        uni.showToast({
          title: "获取日记失败",
          icon: "none",
        });
      }
    },

    async loadBackgrounds() {
      const token = storage.getToken();
      if (!token) {
        this.allBackgrounds = [...this.defaultBackgrounds];
        this.currentBackgroundIndex = 0; // 重置索引
        this.$nextTick(() => {
          this.startAutoPlay(); // 重新启动轮播
        });
        return;
      }

      try {
        // 使用新的API获取用户背景
        const userBgs = await api.getUserDiaryBackgrounds(token);
        this.userBackgrounds = userBgs;

        // 如果用户有自定义背景，只显示自定义背景；否则显示默认背景
        if (this.userBackgrounds.length > 0) {
          this.allBackgrounds = this.userBackgrounds.map((bg) => ({
            ...bg,
            type: "image",
          }));
        } else {
          this.allBackgrounds = [...this.defaultBackgrounds];
        }

        // 重置背景索引并重新启动轮播
        this.currentBackgroundIndex = 0;
        this.$nextTick(() => {
          this.startAutoPlay();
        });
      } catch (error) {
        console.error("获取背景图片失败:", error);
        this.allBackgrounds = [...this.defaultBackgrounds];
        this.currentBackgroundIndex = 0;
        this.$nextTick(() => {
          this.startAutoPlay();
        });
      }
    },

    startAutoPlay() {
      this.stopAutoPlay(); // 先停止之前的轮播

      if (this.allBackgrounds.length > 1) {
        this.autoPlayTimer = setInterval(() => {
          this.currentBackgroundIndex =
            (this.currentBackgroundIndex + 1) % this.allBackgrounds.length;
        }, this.autoPlayInterval);
      }
    },

    stopAutoPlay() {
      if (this.autoPlayTimer) {
        clearInterval(this.autoPlayTimer);
        this.autoPlayTimer = null;
      }
    },

    getCurrentBackgroundStyle() {
      const current = this.allBackgrounds[this.currentBackgroundIndex];
      if (!current) return { backgroundColor: "#ffafcc" };

      if (current.type === "color") {
        return { backgroundColor: current.color };
      } else {
        return {
          backgroundImage: `url(${this.getImageUrl(current.url)})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        };
      }
    },

    goToBackgroundSettings() {
      uni.navigateTo({
        url: "/pages/diary/diary-background-settings",
      });
    },

    toggleManagementMode() {
      this.managementMode = !this.managementMode;
    },

    confirmDelete(diaryId) {
      uni.showModal({
        title: "确认删除",
        content: "确定要删除这篇碎碎念吗？",
        success: (res) => {
          if (res.confirm) {
            this.deleteDiary(diaryId);
          }
        },
      });
    },

    async deleteDiary(diaryId) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        return;
      }

      try {
        await api.deleteDiary(token, diaryId);
        this.diaryList = this.diaryList.filter(
          (diary) => diary.diary_id !== diaryId
        );
        uni.showToast({
          title: "删除成功",
          icon: "success",
        });
      } catch (error) {
        console.error("删除日记失败:", error);
        uni.showToast({
          title: "删除失败",
          icon: "none",
        });
      }
    },

    createNewDiary() {
      uni.navigateTo({
        url: "/pages/diary/write-diary",
      });
    },

    goBackToJourney() {
      uni.switchTab({
        url: "/pages/journey/journey",
      });
    },

    formatDiaryDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
    },

    formatDiaryTime(dateString) {
      const date = new Date(dateString);
      return `${date.getHours().toString().padStart(2, "0")}:${date
        .getMinutes()
        .toString()
        .padStart(2, "0")}`;
    },

    getMoodEmoji(mood) {
      const moodMap = {
        very_happy: "😄",
        happy: "😊",
        neutral: "😐",
        sad: "😢",
        very_sad: "😭",
      };
      return moodMap[mood] || "😊";
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

    previewImage(images, currentImage) {
      const urls = images.map((img) => this.getImageUrl(img.image_url));
      uni.previewImage({
        urls: urls,
        current: this.getImageUrl(currentImage),
      });
    },

    onScroll(e) {
      const scrollTop = e.detail.scrollTop;
      const scrollRatio = Math.min(scrollTop / 200, 1);
      const newHeight = Math.max(
        this.minBackgroundHeight,
        this.maxBackgroundHeight -
          (this.maxBackgroundHeight - this.minBackgroundHeight) * scrollRatio
      );

      this.backgroundHeight = newHeight;
      this.showBackToTopHint = scrollTop > this.scrollThreshold;
      this.isAtTop = scrollTop === 0;
    },

    scrollToTop() {
      this.scrollTop = 1;
      this.$nextTick(() => {
        this.scrollTop = 0;
      });
    },
  },
};
</script>

<style scoped>
.diary-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  position: relative;
  padding-top: var(--status-bar-height);
}

.custom-navbar {
  position: fixed;
  top: var(--status-bar-height);
  left: 0;
  right: 0;
  height: 44px;
  background-color: #ffafcc;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.navbar-title {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
  transition: opacity 0.3s ease;
}

.navbar-title.hidden {
  opacity: 0;
}

.back-to-journey {
  position: absolute;
  left: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.back-to-top-hint {
  position: absolute;
  left: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.back-icon {
  font-size: 32rpx;
  color: white;
  margin-right: 10rpx;
}

.back-text {
  font-size: 28rpx;
  color: white;
}

.background-section {
  position: relative;
  transition: height 0.1s ease-out;
  flex-shrink: 0;
  margin-top: calc(var(--status-bar-height) + 44px);
}

.current-background {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
  position: relative;
}

.background-label {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.5);
}

.background-indicators {
  position: absolute;
  bottom: 80rpx;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10rpx;
  z-index: 10;
}

.indicator-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
}

.indicator-dot.active {
  background-color: white;
  transform: scale(1.2);
}

.new-diary-btn {
  position: absolute;
  bottom: 30rpx;
  right: 30rpx;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20rpx 30rpx;
  border-radius: 50rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
  z-index: 100;
  transition: all 0.1s ease-out;
}

.btn-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.diary-content {
  flex: 1;
  background-color: #f5f5f5;
  padding: 30rpx;
  padding-top: 0;
  border-top-left-radius: 40rpx;
  border-top-right-radius: 40rpx;
  margin-top: -20rpx;
  overflow: hidden;
}

.diary-scroll-view {
  height: 100%;
}

.diary-list {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
  padding-bottom: 30rpx;
  padding-top: 20rpx;
}

.diary-item {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.diary-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.diary-date {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.diary-time {
  font-size: 24rpx;
  color: #999;
}

.diary-main-content .content-text {
  font-size: 30rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 20rpx;
  word-wrap: break-word;
}

.diary-images {
  margin-bottom: 20rpx;
  margin-top: 20rpx;
}

.image-grid {
  display: grid;
  gap: 10rpx;
}

.single-image {
  width: 60%;
}

.single-image .image-wrapper {
  width: 100%;
  height: 300rpx;
}

.multi-images {
  grid-template-columns: repeat(3, 1fr);
}

.multi-images .image-wrapper {
  aspect-ratio: 1;
}

.image-wrapper {
  position: relative;
  border-radius: 10rpx;
  overflow: hidden;
}

.diary-image {
  width: 100%;
  height: 100%;
  vertical-align: middle;
}

.more-images {
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.more-count {
  color: white;
  font-size: 28rpx;
  font-weight: bold;
}

.diary-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mood-tag {
  font-size: 36rpx;
}

.empty-diary {
  text-align: center;
  padding: 60rpx 0;
  background-color: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.manage-btn {
  position: absolute;
  right: 30rpx;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 8rpx;
}

.manage-icon-wrapper {
  padding: 12rpx 24rpx;
  border-radius: 32rpx;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.1)
  );
  backdrop-filter: blur(10rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.manage-btn:active .manage-icon-wrapper {
  transform: scale(0.95);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4),
    rgba(255, 255, 255, 0.2)
  );
}

.manage-icon {
  font-size: 26rpx;
  color: white;
  font-weight: 500;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.background-settings-btn {
  position: absolute;
  right: 150rpx;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 8rpx;
}

.settings-icon-wrapper {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.1)
  );
  backdrop-filter: blur(10rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.background-settings-btn:active .settings-icon-wrapper {
  transform: scale(0.95);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4),
    rgba(255, 255, 255, 0.2)
  );
}

.bg-settings-icon {
  font-size: 32rpx;
  color: white;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.delete-btn {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete-icon {
  font-size: 30rpx;
}
</style>
