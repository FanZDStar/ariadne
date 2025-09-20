<template>
  <view class="diary-container">
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="back-to-journey" v-if="isAtTop" @click="goBackToJourney">
          <text class="back-icon">←</text>
        </view>
        <view class="back-to-top-hint" v-if="showBackToTopHint" @click="scrollToTop">
          <text class="back-icon">↑</text>
          <text class="back-text">回到顶部</text>
        </view>

        <text class="navbar-title" :class="{ 'hidden': showBackToTopHint }">
          碎碎念
        </text>

        <view class="manage-btn" @click="toggleManagementMode">
          <text class="manage-icon">{{ managementMode ? '完成' : '管理' }}</text>
        </view>

        <view class="background-manager-btn" @click="toggleBackgroundManager">
          <text class="bg-manage-icon">🎨</text>
        </view>
      </view>
    </view>

    <view class="background-section" :style="{ height: backgroundHeight + 'px' }">
      <!-- 当前背景显示 -->
      <view class="current-background" :style="getCurrentBackgroundStyle()">
        <text class="background-label" v-if="allBackgrounds[currentBackgroundIndex]">
          {{ allBackgrounds[currentBackgroundIndex].name || allBackgrounds[currentBackgroundIndex].original_filename }}
        </text>
      </view>

      <!-- 背景指示点 -->
      <view class="background-indicators" v-if="allBackgrounds.length > 1">
        <view 
          v-for="(bg, index) in allBackgrounds" 
          :key="bg.id || bg.name" 
          class="indicator-dot" 
          :class="{ active: index === currentBackgroundIndex }"
          @click="changeBackground(index)"
        ></view>
      </view>

      <!-- 自动播放控制 -->
      <view class="auto-play-control" v-if="allBackgrounds.length > 1" @click="toggleAutoPlay">
        <text class="auto-play-icon">{{ isAutoPlay ? '⏸️' : '▶️' }}</text>
      </view>

      <view class="new-diary-btn" @click="createNewDiary">
        <text class="btn-text">✍️ 写日记</text>
      </view>
    </view>

    <!-- 背景管理界面 -->
    <view class="background-manager" v-if="showBackgroundManager">
      <view class="manager-header">
        <text class="manager-title">背景管理</text>
        <view class="close-btn" @click="toggleBackgroundManager">
          <text>×</text>
        </view>
      </view>
      
      <scroll-view class="background-grid" scroll-y>
        <!-- 当前使用的背景类型提示 -->
        <view class="current-status">
          <text class="status-text">
            {{ userBackgrounds.length > 0 ? '当前使用：自定义背景' : '当前使用：默认背景' }}
          </text>
        </view>

        <!-- 自定义背景管理 -->
        <view class="bg-section">
          <view class="section-header">
            <text class="section-title">自定义背景 ({{ userBackgrounds.length }}/9)</text>
            <view class="action-buttons">
              <view class="add-bg-btn" @click="chooseBackgroundImage" v-if="userBackgrounds.length < 9">
                <text>+ 添加</text>
              </view>
              <view class="restore-btn" @click="restoreDefaultBackgrounds" v-if="userBackgrounds.length > 0">
                <text>恢复默认</text>
              </view>
            </view>
          </view>
          
          <view class="bg-list" v-if="userBackgrounds.length > 0">
            <view 
              v-for="(bg, index) in userBackgrounds" 
              :key="bg.id" 
              class="bg-item user-bg"
              :style="{ backgroundImage: `url(${getImageUrl(bg.url)})` }"
              @click="changeBackground(index)"
            >
              <view class="bg-overlay">
                <text class="bg-name">{{ bg.original_filename || '自定义背景' }}</text>
                <view class="delete-bg-btn" @click.stop="confirmDeleteBackground(bg)">
                  <text>🗑️</text>
                </view>
              </view>
            </view>
          </view>
          
          <view class="empty-custom" v-if="userBackgrounds.length === 0">
            <text class="empty-text">暂无自定义背景，点击"+ 添加"上传你的背景图片</text>
          </view>
        </view>

        <!-- 默认背景预览（仅在没有自定义背景时显示当前轮播效果） -->
        <view class="bg-section" v-if="userBackgrounds.length === 0">
          <text class="section-title">默认背景预览</text>
          <view class="bg-list">
            <view 
              v-for="(bg, index) in defaultBackgrounds" 
              :key="bg.id" 
              class="bg-item"
              :style="{ backgroundColor: bg.color }"
              @click="changeBackground(index)"
            >
              <text class="bg-name">{{ bg.name }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>

    <view class="diary-content">
      <scroll-view class="diary-scroll-view" scroll-y @scroll="onScroll" :scroll-top="scrollTop"
        :enable-back-to-top="true" ref="scrollView" id="scrollView">
        <view class="diary-list">
          <view class="diary-item" v-for="diary in diaryList" :key="diary.diary_id">
            <view class="diary-header">
              <text class="diary-date">{{ formatDiaryDate(diary.created_at) }}</text>
              <text class="diary-time">{{ formatDiaryTime(diary.created_at) }}</text>
            </view>
            <view class="diary-main-content">
              <text class="content-text">{{ diary.content }}</text>
            </view>

            <view class="diary-images" v-if="diary.images && diary.images.length > 0">
              <view class="image-grid"
                :class="{ 'single-image': diary.images.length === 1, 'multi-images': diary.images.length > 1 }">
                <view class="image-wrapper" v-for="image in diary.images.slice(0, 9)" :key="image.image_id">
                  <image :src="getImageUrl(image.image_url)" class="diary-image" mode="aspectFill"
                    @click="previewImage(diary.images, image.image_url)" />
                </view>

                <view class="image-wrapper more-images" v-if="diary.images.length > 9">
                  <text class="more-count">+{{ diary.images.length - 9 }}</text>
                </view>
              </view>
            </view>

            <view class="diary-footer">
              <view class="mood-tag">
                <text>{{ getMoodEmoji(diary.mood) }}</text>
              </view>
              <view v-if="managementMode" class="delete-btn" @click="confirmDelete(diary.diary_id)">
                <text class="delete-icon">🗑️</text>
              </view>
            </view>
          </view>

          <view v-if="diaryList.length === 0" class="empty-diary">
            <text class="empty-text">还没有写过日记，点击右上角开始记录吧！</text>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { api, storage } from '../../utils/api.js';

export default {
  data() {
    return {
      diaryList: [],
      scrollTop: 0,
      backgroundHeight: Math.round(uni.getSystemInfoSync().windowHeight * 0.4), // 初始高度为40%屏幕高度
      maxBackgroundHeight: Math.round(uni.getSystemInfoSync().windowHeight * 0.4), // 最大高度
      minBackgroundHeight: 80, // 最小高度
      showBackToTopHint: false, // 是否显示回到顶部提示
      scrollThreshold: 300, // 滚动多少距离后显示回到顶部提示
      isAtTop: true, // 是否位于顶部
      managementMode: false, // 是否处于管理模式
      
      // 背景图片相关
      defaultBackgrounds: [
        { id: "default_1", name: "粉色心情", color: "#ffafcc", type: "color" },
        { id: "default_2", name: "蓝色忧郁", color: "#a2d2ff", type: "color" },
        { id: "default_3", name: "温柔时光", color: "#ffcad4", type: "color" },
        { id: "default_4", name: "紫色梦境", color: "#cdb4db", type: "color" },
      ],
      userBackgrounds: [], // 用户自定义背景图片
      allBackgrounds: [], // 所有背景（默认+用户自定义）
      currentBackgroundIndex: 0, // 当前显示的背景索引
      showBackgroundManager: false, // 是否显示背景管理界面
      isAutoPlay: true, // 是否自动轮播
      autoPlayTimer: null, // 自动轮播定时器
      autoPlayInterval: 3000, // 轮播间隔时间（毫秒）- 加快到3秒
    }
  },

  onLoad() {
    this.loadDiaries();
    this.loadBackgrounds();
    this.startAutoPlay();
  },

  onShow() {
    // 页面显示时重新加载日记，确保新建或删除后能刷新
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
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      try {
        const diaries = await api.getUserDiaries(token);
        this.diaryList = diaries;
      } catch (error) {
        console.error('获取日记失败:', error);
        uni.showToast({
          title: '获取日记失败',
          icon: 'none'
        });
      }
    },

    toggleManagementMode() {
      this.managementMode = !this.managementMode;
    },

    confirmDelete(diaryId) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这篇碎碎念吗？',
        success: (res) => {
          if (res.confirm) {
            this.deleteDiary(diaryId);
          }
        }
      });
    },

    async deleteDiary(diaryId) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      try {
        // 后端删除成功后，前端直接移除对应项
        await api.deleteDiary(token, diaryId);
        this.diaryList = this.diaryList.filter(diary => diary.diary_id !== diaryId);
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        });
      } catch (error) {
        console.error('删除日记失败:', error);
        uni.showToast({
          title: '删除失败',
          icon: 'none'
        });
      }
    },

    createNewDiary() {
      uni.navigateTo({
        url: '/pages/diary/write-diary'
      });
    },
    goBackToJourney() {
      uni.switchTab({
        url: '/pages/journey/journey'
      });
    },
    formatDiaryDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
    },

    formatDiaryTime(dateString) {
      const date = new Date(dateString);
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    },

    getMoodEmoji(mood) {
      const moodMap = {
        'very_happy': '😄',
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'very_sad': '😭'
      };
      return moodMap[mood] || '😊';
    },

    getImageUrl(imageUrl) {
      if (imageUrl.startsWith('http')) {
        return imageUrl;
      }
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

    previewImage(images, currentImage) {
      const urls = images.map(img => this.getImageUrl(img.image_url));
      uni.previewImage({
        urls: urls,
        current: this.getImageUrl(currentImage)
      });
    },

    onScroll(e) {
      const scrollTop = e.detail.scrollTop;
      const scrollRatio = Math.min(scrollTop / 200, 1);
      const newHeight = Math.max(
        this.minBackgroundHeight,
        this.maxBackgroundHeight - (this.maxBackgroundHeight - this.minBackgroundHeight) * scrollRatio
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

    // 加载背景图片
    async loadBackgrounds() {
      const token = storage.getToken();
      if (!token) {
        this.allBackgrounds = [...this.defaultBackgrounds];
        return;
      }

      try {
        // 获取用户自定义背景
        const userBgs = await api.getUserBackgrounds(token);
        this.userBackgrounds = userBgs.map(bg => ({
          ...bg,
          type: 'image'
        }));
        
        // 如果用户有自定义背景，只显示自定义背景；否则显示默认背景
        if (this.userBackgrounds.length > 0) {
          this.allBackgrounds = [...this.userBackgrounds];
        } else {
          this.allBackgrounds = [...this.defaultBackgrounds];
        }
      } catch (error) {
        console.error('获取背景图片失败:', error);
        this.allBackgrounds = [...this.defaultBackgrounds];
      }
    },

    // 选择背景图片上传
    chooseBackgroundImage() {
      // 检查用户背景图片数量
      if (this.userBackgrounds.length >= 9) {
        uni.showToast({
          title: '最多只能上传9张背景图片',
          icon: 'none'
        });
        return;
      }

      uni.chooseImage({
        count: Math.min(9 - this.userBackgrounds.length, 3), // 一次最多选择3张
        sizeType: ['compressed'],
        sourceType: ['camera', 'album'],
        success: (res) => {
          this.uploadBackgroundImages(res.tempFilePaths);
        },
        fail: (error) => {
          console.error('选择图片失败:', error);
        }
      });
    },

    // 批量上传背景图片
    async uploadBackgroundImages(filePaths) {
      const token = storage.getToken();
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }

      uni.showLoading({ title: '上传中...' });

      try {
        for (const filePath of filePaths) {
          await api.uploadDiaryBackground(filePath, token);
        }
        
        uni.hideLoading();
        uni.showToast({
          title: '上传成功',
          icon: 'success'
        });
        
        // 重新加载背景图片
        await this.loadBackgrounds();
      } catch (error) {
        uni.hideLoading();
        console.error('上传背景图片失败:', error);
        uni.showToast({
          title: error.message || '上传失败',
          icon: 'none'
        });
      }
    },

    // 删除背景图片
    async deleteBackgroundImage(backgroundId) {
      const token = storage.getToken();
      if (!token) return;

      try {
        await api.deleteDiaryBackground(token, backgroundId);
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        });
        await this.loadBackgrounds();
      } catch (error) {
        console.error('删除背景图片失败:', error);
        uni.showToast({
          title: '删除失败',
          icon: 'none'
        });
      }
    },

    // 确认删除背景图片
    confirmDeleteBackground(background) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这张背景图片吗？',
        success: (res) => {
          if (res.confirm) {
            this.deleteBackgroundImage(background.id);
          }
        }
      });
    },

    // 切换背景管理界面
    toggleBackgroundManager() {
      this.showBackgroundManager = !this.showBackgroundManager;
      if (this.showBackgroundManager) {
        this.stopAutoPlay();
      } else {
        this.startAutoPlay();
      }
    },

    // 开始自动轮播
    startAutoPlay() {
      if (this.isAutoPlay && this.allBackgrounds.length > 1) {
        this.stopAutoPlay(); // 先清除现有定时器
        this.autoPlayTimer = setInterval(() => {
          this.currentBackgroundIndex = (this.currentBackgroundIndex + 1) % this.allBackgrounds.length;
        }, this.autoPlayInterval);
      }
    },

    // 停止自动轮播
    stopAutoPlay() {
      if (this.autoPlayTimer) {
        clearInterval(this.autoPlayTimer);
        this.autoPlayTimer = null;
      }
    },

    // 切换自动轮播
    toggleAutoPlay() {
      this.isAutoPlay = !this.isAutoPlay;
      if (this.isAutoPlay) {
        this.startAutoPlay();
      } else {
        this.stopAutoPlay();
      }
    },

    // 手动切换背景
    changeBackground(index) {
      this.currentBackgroundIndex = index;
      if (this.isAutoPlay) {
        this.startAutoPlay(); // 重新开始自动播放
      }
    },

    // 恢复默认背景
    async restoreDefaultBackgrounds() {
      uni.showModal({
        title: '恢复默认背景',
        content: '确定要删除所有自定义背景图片，恢复默认背景吗？此操作不可撤销。',
        success: async (res) => {
          if (res.confirm) {
            const token = storage.getToken();
            if (!token) {
              uni.showToast({
                title: '请先登录',
                icon: 'none'
              });
              return;
            }

            uni.showLoading({ title: '恢复中...' });

            try {
              await api.restoreDefaultBackgrounds(token);
              
              uni.hideLoading();
              uni.showToast({
                title: '已恢复默认背景',
                icon: 'success'
              });
              
              // 重新加载背景
              await this.loadBackgrounds();
              
              // 重置当前背景索引
              this.currentBackgroundIndex = 0;
              
            } catch (error) {
              uni.hideLoading();
              console.error('恢复默认背景失败:', error);
              uni.showToast({
                title: error.message || '恢复失败',
                icon: 'none'
              });
            }
          }
        }
      });
    },

    // 获取当前背景样式
    getCurrentBackgroundStyle() {
      const current = this.allBackgrounds[this.currentBackgroundIndex];
      if (!current) return { backgroundColor: '#ffafcc' };
      
      if (current.type === 'color') {
        return { backgroundColor: current.color };
      } else {
        return { 
          backgroundImage: `url(${this.getImageUrl(current.url)})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        };
      }
    }
  }
}
</script>

<style scoped>
/* 新增返回上一级按钮样式 */
.back-to-journey {
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

.diary-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  position: relative;
  padding-top: var(--status-bar-height);
}

/* 自定义导航栏 */
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

/* 回到顶部提示 */
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

/* 上半屏：背景图片选择区域 */
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

.auto-play-control {
  position: absolute;
  top: 30rpx;
  left: 30rpx;
  width: 60rpx;
  height: 60rpx;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.auto-play-icon {
  font-size: 24rpx;
}

.background-swiper {
  height: 100%;
}

.background-item {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
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

/* 日记内容区域 */
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

/* 图片展示样式 */
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
}

.manage-icon {
  font-size: 28rpx;
  color: white;
}

.background-manager-btn {
  position: absolute;
  right: 100rpx;
  display: flex;
  align-items: center;
  height: 100%;
}

.bg-manage-icon {
  font-size: 28rpx;
  color: white;
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

/* 背景管理界面样式 */
.background-manager {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  padding-top: var(--status-bar-height);
}

.manager-header {
  height: 88rpx;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30rpx;
  border-bottom: 1px solid #eee;
}

.manager-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.close-btn {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #666;
}

.background-grid {
  flex: 1;
  background-color: white;
  padding: 30rpx;
}

.bg-section {
  margin-bottom: 40rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.add-bg-btn {
  padding: 12rpx 20rpx;
  background-color: #007aff;
  color: white;
  border-radius: 20rpx;
  font-size: 24rpx;
  margin-left: 12rpx;
}

.restore-btn {
  padding: 12rpx 20rpx;
  background-color: #ff9500;
  color: white;
  border-radius: 20rpx;
  font-size: 24rpx;
  margin-left: 12rpx;
}

.action-buttons {
  display: flex;
  align-items: center;
}

.current-status {
  padding: 20rpx 30rpx;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.status-text {
  font-size: 26rpx;
  color: #666;
}

.empty-custom {
  padding: 60rpx 20rpx;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 16rpx;
  margin: 20rpx 0;
}

.empty-text {
  font-size: 24rpx;
  color: #999;
  line-height: 1.5;
}

.bg-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
}

.bg-item {
  aspect-ratio: 16/9;
  border-radius: 16rpx;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.user-bg {
  position: relative;
}

.bg-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  padding: 20rpx 16rpx 16rpx;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.bg-name {
  font-size: 20rpx;
  color: white;
  font-weight: 500;
  max-width: 120rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.delete-bg-btn {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
}
</style>