<template>
  <view class="my-whispers-container">
    <view class="header">
      <text class="title">此情此语</text>
      <text class="subtitle">记录你的情感轨迹与心灵互动</text>
      <view class="manage-btn" @click="toggleManagementMode">
        <text class="manage-icon">{{ managementMode ? "完成" : "管理" }}</text>
      </view>
    </view>

    <view class="tabs">
      <view class="tab-with-icon">
        <view
          :class="['tab-item', { active: activeTab === 'posted' }]"
          @click="activeTab = 'posted'"
        >
          我发布的
        </view>
        <view
          v-if="activeTab === 'posted'"
          class="calendar-icon"
          @click="showCalendar"
        >
          📅
        </view>
      </view>
      <view
        :class="['tab-item', { active: activeTab === 'interacted' }]"
        @click="activeTab = 'interacted'"
      >
        我互动的
      </view>
      <!-- 聊天功能已隐藏 -->
      <!-- <view
        :class="['tab-item', { active: activeTab === 'chats' }]"
        @click="activeTab = 'chats'"
      >
        聊天
      </view> -->
    </view>

    <scroll-view class="content-scroll-view" scroll-y>
      <view v-if="activeTab === 'posted'" class="whisper-list">
        <view v-if="myPostedWhispers.length === 0" class="empty-state">
          <text class="empty-text">你还没有发布过悄悄话...</text>
        </view>
        <view
          class="whisper-item"
          v-for="whisper in myPostedWhispers"
          :key="whisper.whisper_id"
          @click="!managementMode && goToWhisperDetail(whisper.whisper_id)"
          @longpress="enterManagementMode"
        >
          <!-- 操作按钮区域 - 预留在右上角 -->
          <view class="action-buttons-container">
            <view
              v-show="managementMode"
              class="edit-btn"
              @click.stop="editWhisper(whisper)"
            >
              <text class="edit-icon">✏️</text>
            </view>
            <view
              v-show="managementMode"
              class="delete-btn"
              @click.stop="confirmDelete(whisper, 'whisper')"
            >
              <text class="delete-icon">🗑️</text>
            </view>
          </view>

          <!-- 悄悄话标题 -->
          <view class="whisper-title">{{ whisper.title || "无标题" }}</view>

          <!-- 标签 -->
          <view
            v-if="whisper.tags && whisper.tags.length > 0"
            class="whisper-tags"
          >
            <text v-for="tag in whisper.tags" :key="tag" class="tag-item"
              >#{{ tag }}</text
            >
          </view>

          <!-- 内容 -->
          <view class="whisper-content-wrapper">
            <view class="whisper-content">{{
              truncateContent(whisper.content, 50)
            }}</view>
          </view>

          <!-- 图片展示 -->
          <view
            v-if="getWhisperImages(whisper).length > 0"
            class="whisper-images"
          >
            <image
              v-for="(image, index) in getWhisperImages(whisper).slice(0, 2)"
              :key="index"
              :src="image"
              class="whisper-image"
              mode="aspectFill"
              @click.stop="previewImage(getWhisperImages(whisper), image)"
              @error="onImageError"
              @load="onImageLoad"
            />
          </view>

          <!-- 底部信息 -->
          <view class="whisper-bottom">
            <view class="whisper-stats">
              <text class="stat-item">❤️ {{ whisper.like_count || 0 }}</text>
              <text class="stat-item">💬 {{ whisper.comment_count || 0 }}</text>
            </view>
            <view class="whisper-timestamp">{{
              getTimeDisplayText(whisper)
            }}</view>
          </view>
        </view>
      </view>

      <view v-if="activeTab === 'interacted'" class="whisper-list">
        <view v-if="myInteractedWhispers.length === 0" class="empty-state">
          <text class="empty-text">你还没有与任何悄悄话互动过...</text>
        </view>
        <view
          class="whisper-item"
          v-for="whisper in myInteractedWhispers"
          :key="whisper.whisper_id"
          @click="!managementMode && goToWhisperDetail(whisper.whisper_id)"
          @longpress="enterManagementMode"
        >
          <!-- 操作按钮区域 - 删除互动链接 -->
          <view class="action-buttons-container">
            <view
              v-show="managementMode"
              class="delete-btn"
              @click.stop="confirmDelete(whisper, 'interaction')"
            >
              <text class="delete-icon">🗑️</text>
            </view>
          </view>

          <!-- 发布者信息（新增）-->
          <view class="author-info">
            <image
              :src="getAuthorAvatar(whisper)"
              class="author-avatar"
              mode="aspectFill"
            />
            <text class="author-name">{{ getAuthorName(whisper) }}</text>
            <text class="interaction-badge">{{
              getInteractionBadge(whisper.interaction_type)
            }}</text>
          </view>

          <!-- 悄悄话标题 -->
          <view class="whisper-title">{{ whisper.title || "无标题" }}</view>

          <!-- 标签 -->
          <view
            v-if="whisper.tags && whisper.tags.length > 0"
            class="whisper-tags"
          >
            <text v-for="tag in whisper.tags" :key="tag" class="tag-item"
              >#{{ tag }}</text
            >
          </view>

          <!-- 内容 -->
          <view class="whisper-content-wrapper">
            <view class="whisper-content">{{
              truncateContent(whisper.content, 50)
            }}</view>
          </view>

          <!-- 图片展示 -->
          <view
            v-if="getWhisperImages(whisper).length > 0"
            class="whisper-images"
          >
            <image
              v-for="(image, index) in getWhisperImages(whisper).slice(0, 2)"
              :key="index"
              :src="image"
              class="whisper-image"
              mode="aspectFill"
              @click.stop="previewImage(getWhisperImages(whisper), image)"
              @error="onImageError"
              @load="onImageLoad"
            />
          </view>

          <!-- 底部信息 -->
          <view class="whisper-bottom">
            <view class="whisper-stats">
              <text class="stat-item">❤️ {{ whisper.like_count || 0 }}</text>
              <text class="stat-item">💬 {{ whisper.comment_count || 0 }}</text>
            </view>
            <view class="whisper-timestamp">{{
              getTimeDisplayText(whisper)
            }}</view>
          </view>
        </view>
      </view>

      <!-- 聊天功能已隐藏 -->
      <!-- <view v-if="activeTab === 'chats'" class="whisper-list">
        <view v-if="myChats.length === 0" class="empty-state">
          <text class="empty-text">你还没有参与过任何聊天...</text>
        </view>
        <view
          class="whisper-item"
          v-for="chat in myChats"
          :key="chat.whisper_id"
          @click="!managementMode && goToChat(chat.whisper_id)"
          @longpress="enterManagementMode"
        >
          <view class="whisper-timestamp">{{
            formatTimestamp(chat.created_at)
          }}</view>
          <view class="whisper-content-wrapper">
            <view class="whisper-content">{{ chat.content }}</view>
            <view
              v-if="managementMode"
              class="delete-btn"
              @click.stop="confirmDelete(chat, 'chat')"
            >
              <text class="delete-icon">🗑️</text>
            </view>
          </view>
          <view class="whisper-stats">
            <text class="stat-item">❤️ {{ chat.like_count || 0 }}</text>
            <text class="stat-item">💬 {{ chat.comment_count || 0 }}</text>
          </view>
        </view>
      </view> -->
    </scroll-view>

    <!-- 回到顶部组件 -->
    <BackToTop
      ref="backToTop"
      :threshold="0"
      :bottom="170"
      :right="50"
      @start-scroll-listener="onStartScrollListener"
      @remove-scroll-listener="onRemoveScrollListener"
      @scroll-to-top-success="onScrollToTopSuccess"
    />

    <!-- 发布悄悄话浮动按钮 -->
    <view class="fab" @click="goToWriteWhisper">
      <text class="fab-icon">+</text>
    </view>

    <!-- 日历组件 -->
    <WhisperCalendar
      :visible="calendarVisible"
      :whisperDates="whisperDates"
      @close="calendarVisible = false"
      @date-selected="onDateSelected"
    />
  </view>
</template>

<script>
import { api, storage } from "../../utils/api.js";
import BackToTop from "../../components/BackToTop.vue";
import WhisperCalendar from "../../components/WhisperCalendar.vue";

export default {
  components: {
    BackToTop,
    WhisperCalendar,
  },
  data() {
    return {
      activeTab: "posted",
      myPostedWhispers: [],
      myInteractedWhispers: [],
      myChats: [], // 聊天功能已隐藏，保留数据结构避免错误
      managementMode: false,
      scrollTop: 0,
      calendarVisible: false,
      selectedDate: null,
      allPostedWhispers: [], // 存储所有悄悄话，用于筛选
    };
  },
  computed: {
    // 获取所有有悄悄话的日期
    whisperDates() {
      return this.allPostedWhispers.map((whisper) => whisper.created_at);
    },
    // 根据选择的日期筛选悄悄话
    filteredPostedWhispers() {
      if (!this.selectedDate) {
        return this.allPostedWhispers;
      }
      return this.allPostedWhispers.filter((whisper) => {
        const whisperDate = whisper.created_at.split("T")[0].split(" ")[0];
        return whisperDate === this.selectedDate;
      });
    },
  },
  onLoad() {
    this.loadData();
  },
  onShow() {
    // 每次页面显示时都重新加载数据
    this.loadData();
  },
  onPullDownRefresh() {
    this.loadData().then(() => uni.stopPullDownRefresh());
  },
  onPageScroll(e) {
    this.scrollTop = e.scrollTop;
    // 将滚动事件传递给BackToTop组件
    if (this.$refs.backToTop) {
      this.$refs.backToTop.updateVisibility(e.scrollTop);
    }
  },
  onUnload() {
    // 页面卸载时的清理工作
  },
  methods: {
    async loadData() {
      await this.fetchMyPostedWhispers();
      await this.fetchMyInteractedWhispers();
      // await this.fetchMyChats(); // 聊天功能已隐藏
    },
    async fetchMyPostedWhispers() {
      const token = storage.getToken();
      if (!token) return;
      try {
        const whispers = await api.getMyPostedWhispers(token);
        this.allPostedWhispers = whispers;
        this.myPostedWhispers = whispers;
      } catch (error) {
        console.error("Failed to fetch posted whispers:", error);
      }
    },
    async fetchMyInteractedWhispers() {
      const token = storage.getToken();
      if (!token) return;
      try {
        console.log("00000000000000000000000000");
        this.myInteractedWhispers = await api.getMyInteractedWhispers(token);
      } catch (error) {
        console.error("Failed to fetch interacted whispers:", error);
        // 临时数据，后续需要实现API
        this.myInteractedWhispers = [];
      }
    },
    // 聊天功能已隐藏
    // async fetchMyChats() {
    //   const token = storage.getToken();
    //   if (!token) return;
    //   try {
    //     this.myChats = await api.getMyChats(token);
    //   } catch (error) {
    //     console.error("Failed to fetch chats:", error);
    //   }
    // },
    showCalendar() {
      this.calendarVisible = true;
    },
    onDateSelected(date) {
      this.selectedDate = date;
      if (date) {
        // 根据日期筛选悄悄话
        this.myPostedWhispers = this.allPostedWhispers.filter((whisper) => {
          const whisperDate = whisper.created_at.split("T")[0].split(" ")[0];
          return whisperDate === date;
        });
        uni.showToast({
          title: `已筛选 ${date.split("-")[1]}月${date.split("-")[2]}日`,
          icon: "none",
          duration: 1500,
        });
      } else {
        // 显示全部
        this.myPostedWhispers = this.allPostedWhispers;
        uni.showToast({
          title: "已显示全部",
          icon: "none",
          duration: 1500,
        });
      }
    },
    toggleManagementMode() {
      this.managementMode = !this.managementMode;
    },
    enterManagementMode() {
      if (!this.managementMode) {
        this.managementMode = true;
      }
    },
    editWhisper(whisper) {
      // 跳转到编辑页面，传递悄悄话ID
      uni.navigateTo({
        url: `/pages/tree-hole/edit-whisper?whisper_id=${whisper.whisper_id}`,
      });
    },
    confirmDelete(item, type) {
      const isMyWhisper = item.user_id === storage.getUserInfo().user_id;
      let content = "";

      if (type === "whisper") {
        content = "删除这个悄悄话会一并删除所有相关的聊天，确定吗？";
      } else if (type === "interaction") {
        content = "确定要移除这个互动记录吗？";
      } 
      // 聊天功能已隐藏
      // else {
      //   content = "确定要离开这个聊天吗？";
      // }

      uni.showModal({
        title: "确认操作",
        content: content,
        success: (res) => {
          if (res.confirm) {
            if (type === "whisper") {
              this.deleteWhisper(item.whisper_id);
            } else if (type === "interaction") {
              this.removeInteraction(item.whisper_id);
            } 
            // 聊天功能已隐藏
            // else {
            //   this.leaveChat(item.whisper_id);
            // }
          }
        },
      });
    },
    async deleteWhisper(whisperId) {
      const token = storage.getToken();
      try {
        await api.deleteWhisper(token, whisperId);
        this.myPostedWhispers = this.myPostedWhispers.filter(
          (w) => w.whisper_id !== whisperId
        );
        // this.myChats = this.myChats.filter((c) => c.whisper_id !== whisperId); // 聊天功能已隐藏
        uni.showToast({ title: "删除成功", icon: "success" });
      } catch (error) {
        console.error("Failed to delete whisper:", error);
        uni.showToast({ title: "删除失败", icon: "none" });
      }
    },
    async removeInteraction(whisperId) {
      const token = storage.getToken();
      try {
        await api.removeInteractionLink(token, whisperId);
        this.myInteractedWhispers = this.myInteractedWhispers.filter(
          (w) => w.whisper_id !== whisperId
        );
        uni.showToast({ title: "已移除互动链接", icon: "success" });
      } catch (error) {
        console.error("Failed to remove interaction:", error);
        uni.showToast({ title: "操作失败", icon: "none" });
      }
    },
    // 聊天功能已隐藏
    // async leaveChat(whisperId) {
    //   const token = storage.getToken();
    //   try {
    //     await api.leaveWhisperChat(token, whisperId);
    //     this.myChats = this.myChats.filter((c) => c.whisper_id !== whisperId);
    //     uni.showToast({ title: "已离开聊天", icon: "success" });
    //   } catch (error) {
    //     console.error("Failed to leave chat:", error);
    //     uni.showToast({ title: "操作失败", icon: "none" });
    //   }
    // },
    // goToChat(whisperId) {
    //   uni.navigateTo({
    //     url: `/pages/tree-hole/whisper-chat?whisper_id=${whisperId}`,
    //   });
    // },
    scrollToTop() {
      uni.pageScrollTo({
        scrollTop: 0,
        duration: 300,
      });
    },
    goToWhisperDetail(whisperId) {
      uni.navigateTo({
        url: `/pages/tree-hole/whisper-detail?whisper_id=${whisperId}`,
      });
    },
    goToWriteWhisper() {
      uni.navigateTo({
        url: "/pages/tree-hole/write-whisper",
      });
    },
    formatTimestamp(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");
      return `${year}.${month}.${day} ${hours}:${minutes}`;
    },

    // 获取时间显示文本
    getTimeDisplayText(whisper) {
      const createdTime = new Date(whisper.created_at).getTime();
      const updatedTime = new Date(whisper.updated_at).getTime();

      // 判断是否被编辑过（时间差超过1秒，避免数据库精度问题）
      if (updatedTime - createdTime > 1000) {
        return `于${this.formatTimestamp(whisper.updated_at)}被编辑`;
      } else {
        return `发布于${this.formatTimestamp(whisper.created_at)}`;
      }
    },

    // 截取内容方法
    truncateContent(content, maxLength) {
      if (!content) return "";
      if (content.length <= maxLength) return content;
      return content.substring(0, maxLength) + "...";
    },

    // 获取悄悄话图片
    getWhisperImages(whisper) {
      // 检查各种可能的图片字段名
      const images =
        whisper.images ||
        whisper.image_urls ||
        whisper.imageUrls ||
        whisper.pictures ||
        [];

      // 如果是字符串，尝试解析为JSON
      if (typeof images === "string") {
        try {
          const parsed = JSON.parse(images);
          return this.extractImageUrls(parsed);
        } catch (e) {
          return [images]; // 如果解析失败，当作单个图片URL
        }
      }

      // 确保返回数组并提取图片URL
      if (Array.isArray(images)) {
        return this.extractImageUrls(images);
      }

      return [];
    },

    // 提取图片URL
    extractImageUrls(imageData) {
      if (!Array.isArray(imageData)) return [];

      return imageData
        .map((item) => {
          let url = "";

          // 如果是对象，提取image_url字段
          if (typeof item === "object" && item.image_url) {
            url = item.image_url;
          }
          // 如果是字符串，直接使用
          else if (typeof item === "string") {
            url = item;
          }

          if (!url) return "";

          // 使用与日记页面相同的URL处理逻辑
          return this.getImageUrl(url);
        })
        .filter((url) => url); // 过滤掉空的URL
    },

    // 获取图片URL（参考日记页面的实现）
    getImageUrl(imageUrl) {
      if (!imageUrl) return "";

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

    // 图片预览功能（参考日记页面的实现）
    previewImage(images, currentImage) {
      const urls = images;
      uni.previewImage({
        urls: urls,
        current: currentImage,
      });
    },

    // 图片加载成功
    onImageLoad(e) {
      console.log("图片加载成功:", e);
    },

    // 图片加载失败
    onImageError(e) {
      console.error("图片加载失败:", e);
    },

    // 组件事件处理方法
    onStartScrollListener() {
      // 组件已挂载，准备接收滚动事件
    },

    onRemoveScrollListener() {
      // 组件将要销毁
    },

    onScrollToTopSuccess() {
      console.log("回到顶部成功");
    },

    // 获取作者头像（新增）
    getAuthorAvatar(whisper) {
      // 如果是匿名，使用匿名头像
      if (whisper.is_anonymous && whisper.anonymous_avatar) {
        return this.getImageUrl(whisper.anonymous_avatar);
      }
      // 如果有用户对象且有头像
      if (whisper.user && whisper.user.avatar_url) {
        return this.getImageUrl(whisper.user.avatar_url);
      }
      // 默认头像
      return "/static/default-avatar.png";
    },

    // 获取作者名称（新增）
    getAuthorName(whisper) {
      // 如果是匿名，使用匿名名称
      if (whisper.is_anonymous && whisper.anonymous_name) {
        return whisper.anonymous_name;
      }
      // 如果有用户对象
      if (whisper.user) {
        return whisper.user.nickname || whisper.user.username || "匿名用户";
      }
      return "匿名用户";
    },

    // 获取互动徽章文本（新增）
    getInteractionBadge(interactionType) {
      if (interactionType === "both") {
        return "👍💬";
      } else if (interactionType === "like") {
        return "已点赞";
      } else if (interactionType === "comment") {
        return "已评论";
      }
      return "";
    },
  },
};
</script>

<style scoped>
/* 样式部分无需修改，保持原样即可 */
.my-whispers-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9fa;
}

.header {
  padding: 40rpx;
  background-color: white;
  text-align: center;
  position: relative;
}

.title {
  font-size: 42rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #999;
}

.manage-btn {
  position: absolute;
  right: 40rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 30rpx;
  color: #007aff;
}

.tabs {
  display: flex;
  background-color: white;
  border-bottom: 1rpx solid #eee;
}

.tab-with-icon {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.calendar-icon {
  position: absolute;
  right: 10rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 36rpx;
  padding: 10rpx;
  cursor: pointer;
  transition: transform 0.2s;
}

.calendar-icon:active {
  transform: translateY(-50%) scale(0.9);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 25rpx 0;
  font-size: 30rpx;
  color: #666;
  position: relative;
  cursor: pointer;
  transition: color 0.3s;
}

.tab-item.active {
  color: #007aff;
  font-weight: bold;
}

.tab-item.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 6rpx;
  background-color: #007aff;
  border-radius: 3rpx;
}

.content-scroll-view {
  flex: 1;
  height: 100%;
}

.whisper-list {
  padding: 30rpx;
}

.whisper-item {
  background: #fff;
  padding: 20rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
  position: relative;
}

.delete-btn-container {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  width: 50rpx;
  height: 50rpx;
  z-index: 10;
}

.action-buttons-container {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  display: flex;
  gap: 12rpx;
  z-index: 10;
}

.edit-btn {
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  background-color: #007aff;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 122, 255, 0.3);
}

.edit-btn:active {
  transform: scale(0.9);
  background-color: #0056b3;
}

.edit-icon {
  font-size: 24rpx;
  color: white;
}

.delete-btn {
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  background-color: #999;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(153, 153, 153, 0.3);
}

.delete-btn:active {
  transform: scale(0.9);
  background-color: #777;
}

.delete-icon {
  font-size: 24rpx;
  color: white;
}

.whisper-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  line-height: 1.3;
  padding-right: 130rpx; /* 为两个按钮预留空间 */
}

/* 发布者信息样式（新增）*/
.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
  padding-bottom: 12rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.author-avatar {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  margin-right: 12rpx;
  background-color: #f0f0f0;
}

.author-name {
  font-size: 28rpx;
  color: #666;
  font-weight: 500;
  flex: 1;
}

.whisper-tags {
  margin-bottom: 8rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}

.tag-item {
  background-color: #f0f0f0;
  color: #666;
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 16rpx;
}

.whisper-timestamp {
  font-size: 22rpx;
  color: #999;
  font-style: italic;
}

.whisper-content-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4rpx;
}

.whisper-content {
  font-size: 36rpx;
  color: #555;
  line-height: 1.4;
  flex: 1;
  margin-bottom: 0;
}

.whisper-images {
  display: flex;
  gap: 12rpx;
  margin-bottom: 4rpx;
  margin-top: 8rpx;
}

.whisper-image {
  width: 160rpx;
  height: 160rpx;
  border-radius: 8rpx;
  object-fit: cover;
}

.whisper-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4rpx;
  padding-top: 8rpx;
  border-top: 1rpx solid #f5f5f5;
}

.whisper-stats {
  display: flex;
  align-items: center;
  font-size: 22rpx;
  color: #999;
}

.stat-item {
  margin-right: 20rpx;
}

.interaction-badge {
  background-color: #007aff;
  color: white;
  font-size: 20rpx;
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  margin-left: 20rpx;
}

.empty-state {
  text-align: center;
  padding-top: 200rpx;
  color: #aaa;
}

.empty-text {
  font-size: 28rpx;
}

.fab {
  position: fixed;
  bottom: 50rpx;
  right: 50rpx;
  width: 100rpx;
  height: 100rpx;
  background-color: #007aff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
  z-index: 100;
}

.fab-icon {
  font-size: 60rpx;
  color: white;
  font-weight: bold;
}
</style>
