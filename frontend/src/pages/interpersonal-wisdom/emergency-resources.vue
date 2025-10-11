<template>
  <view class="emergency-container">
    <!-- 专业热线 -->
    <view class="hotline-section">
      <text class="section-title">专业求助热线</text>
      <view
        v-for="hotline in hotlines"
        :key="hotline.id"
        class="hotline-card"
        @click="callHotline(hotline)"
      >
        <view class="hotline-info">
          <text class="hotline-name">{{ hotline.name }}</text>
          <text class="hotline-desc">{{ hotline.description }}</text>
          <view class="hotline-details">
            <text class="hotline-time">{{ hotline.time }}</text>
            <text class="hotline-type">{{ hotline.type }}</text>
          </view>
        </view>
        <view class="hotline-action">
          <text class="hotline-number">{{ hotline.number }}</text>
          <text class="call-icon">拨打</text>
        </view>
      </view>
    </view>

    <!-- 在线服务 -->

    <!-- 自助工具 -->
    <view class="tools-section">
      <text class="section-title">心理自助工具</text>
      <view class="tools-grid">
        <view
          v-for="tool in selfHelpTools"
          :key="tool.id"
          class="tool-card"
          @click="useTool(tool)"
        >
          <text class="tool-icon">{{ tool.icon }}</text>
          <text class="tool-name">{{ tool.name }}</text>
          <text class="tool-desc">{{ tool.description }}</text>
        </view>
      </view>
    </view>

    <!-- 紧急联系人 -->


    <!-- 安全计划 -->

    <!-- 资源库 -->
    <view class="resources-section">
      <text class="section-title">心理健康资源</text>
      <!-- 隐藏标签横条，因为只有一个分类 -->
      <!-- <view class="resources-tabs">
        <view
          v-for="tab in resourceTabs"
          :key="tab.id"
          class="tab-item"
          :class="{ active: currentResourceTab === tab.id }"
          @click="switchResourceTab(tab.id)"
        >
          <text class="tab-text">{{ tab.name }}</text>
        </view>
      </view> -->
      <view class="resources-content">
        <view
          v-for="resource in currentResources"
          :key="resource.id"
          class="resource-item"
          @click="viewResource(resource)"
        >
          <text class="resource-title">{{ resource.title }}</text>
          <text class="resource-desc">{{ resource.description }}</text>
          <view class="resource-meta">
            <text class="resource-type">{{ resource.type }}</text>
            <text class="resource-time">{{ resource.readTime }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      hotlines: [
        {
          id: 1,
          name: "国家心理危机干预热线",
          number: "400-161-9995",
          description: "24小时免费心理危机干预服务",
          time: "24小时",
          type: "免费",
        },
        {
          id: 2,
          name: "北京心理危机研究与干预热线",
          number: "400-658-9995",
          description: "专业心理危机干预和情感支持",
          time: "24小时",
          type: "免费",
        },
        {
          id: 3,
          name: "上海心理援助热线",
          number: "021-64387250",
          description: "心理咨询和危机干预服务",
          time: "9:00-23:00",
          type: "免费",
        },
        {
          id: 4,
          name: "青少年心理健康热线",
          number: "12355",
          description: "专门为青少年提供心理支持",
          time: "9:00-17:00",
          type: "免费",
        },
      ],
      onlineServices: [
        {
          id: 1,
          name: "在线心理咨询",
          icon: "",
          description: "与专业心理咨询师一对一在线交流",
          status: "online",
          features: ["实时对话", "隐私保护", "专业认证"],
        },
        {
          id: 2,
          name: "情绪支持聊天室",
          icon: "",
          description: "与其他用户分享经历，互相支持",
          status: "online",
          features: ["匿名交流", "同伴支持", "监管安全"],
        },
        {
          id: 3,
          name: "视频心理咨询",
          icon: "",
          description: "通过视频与心理专家面对面交流",
          status: "busy",
          features: ["面对面交流", "专业诊断", "预约制"],
        },
      ],
      selfHelpTools: [
        {
          id: 1,
          name: "呼吸练习",
          icon: "",
          description: "缓解焦虑的呼吸技巧",
        },
        {
          id: 2,
          name: "情绪记录",
          icon: "",
          description: "追踪和分析情绪变化",
        },
        {
          id: 3,
          name: "冥想指导",
          icon: "",
          description: "正念冥想练习",
        },
        {
          id: 6,
          name: "压力测试",
          icon: "",
          description: "评估当前压力水平",
        },
        // {
        //   id: 5,
        //   name: "睡眠助手",
        //   icon: "😴",
        //   description: "改善睡眠质量的工具",
        // },
        // {
        //   id: 4,
        //   name: "积极思维",
        //   icon: "💭",
        //   description: "培养积极心态的练习",
        // },
      ],
      emergencyContacts: [],
      hasSafetyPlan: false,
      currentResourceTab: "all",
      resourceTabs: [
        { id: "all", name: "心理健康资源" },
      ],
      resources: {
        all: [
          {
            id: 1,
            title: "小心人际间的\"情绪感染\"",
            description: "了解情绪感染的机制，学会保护自己的情绪边界",
            type: "科普文章",
            readTime: "5分钟",
            url: "https://mp.weixin.qq.com/s/FHpwSh5_dIPxl5uLUzAeTw",
          },
          {
            id: 2,
            title: "如何对待并应对孩子过度使用手机",
            description: "专家指导如何帮助孩子合理使用数字设备，建立健康的使用习惯",
            type: "实用指南",
            readTime: "8分钟",
            url: "https://ncmhc.org.cn/channel/newsinfo/6319",
          },
          {
            id: 3,
            title: "正念冥想入门教程",
            description: "跟随专家学习基础的冥想技巧",
            type: "教学视频",
            readTime: "15分钟",
          },
          {
            id: 4,
            title: "《感受的治愈力》",
            description: "了解情绪的本质和调节方法",
            type: "心理学著作",
            readTime: "推荐阅读",
          },
          {
            id: 5,
            title: "Headspace",
            description: "专业的冥想和正念练习应用",
            type: "冥想应用",
            readTime: "免费试用",
          },
        ],
      },
    };
  },

  computed: {
    currentResources() {
      return this.resources[this.currentResourceTab] || [];
    },
  },

  onLoad() {
    this.loadEmergencyContacts();
    this.checkSafetyPlan();
  },

  methods: {
    callEmergencyHotline() {
      uni.showModal({
        title: "紧急求助",
        content:
          "将拨打国家心理危机干预热线：400-161-9995\n\n24小时免费服务，请放心拨打。",
        confirmText: "立即拨打",
        cancelText: "取消",
        success: (res) => {
          if (res.confirm) {
            uni.makePhoneCall({
              phoneNumber: "400-161-9995",
            });
          }
        },
      });
    },

    startCrisisAssessment() {
      uni.navigateTo({
        url: "/pages/interpersonal-wisdom/crisis-assessment",
      });
    },

    callHotline(hotline) {
      uni.makePhoneCall({
        phoneNumber: hotline.number,
      });
    },

    accessOnlineService(service) {
      if (service.status === "offline") {
        uni.showToast({
          title: "服务暂时不可用",
          icon: "none",
        });
        return;
      }

      uni.showModal({
        title: service.name,
        content: service.description + "\n\n是否现在开始使用？",
        success: (res) => {
          if (res.confirm) {
            // 这里可以跳转到相应的在线服务页面
            uni.showToast({
              title: "正在连接服务...",
              icon: "loading",
            });
          }
        },
      });
    },

    getStatusText(status) {
      const statusMap = {
        online: "在线",
        busy: "繁忙",
        offline: "离线",
      };
      return statusMap[status] || "未知";
    },

    useTool(tool) {
      // 跳转到心理自助工具详情页面，传递工具ID
      uni.navigateTo({
        url: `/pages/tools/self-help-tool?id=${tool.id}`,
      });
    },

    addEmergencyContact() {
      uni.navigateTo({
        url: "/pages/emergency/add-contact",
      });
    },

    loadEmergencyContacts() {
      const contacts = uni.getStorageSync("emergencyContacts") || [];
      this.emergencyContacts = contacts;
    },

    callContact(contact) {
      uni.makePhoneCall({
        phoneNumber: contact.phone,
      });
    },

    messageContact(contact) {
      uni.showModal({
        title: "发送消息",
        content: `向 ${contact.name} 发送求助消息？\n\n"我现在需要帮助，能联系我吗？"`,
        success: (res) => {
          if (res.confirm) {
            // 这里可以集成短信API或其他消息服务
            uni.showToast({
              title: "消息已发送",
              icon: "success",
            });
          }
        },
      });
    },

    checkSafetyPlan() {
      const plan = uni.getStorageSync("safetyPlan");
      this.hasSafetyPlan = !!plan;
    },

    manageSafetyPlan() {
      uni.navigateTo({
        url: "/pages/emergency/safety-plan",
      });
    },

    switchResourceTab(tabId) {
      this.currentResourceTab = tabId;
    },

    viewResource(resource) {
      console.log('viewResource called with:', resource);
      
      // 如果资源包含外部链接
      if (resource.url) {
        console.log('Opening external URL:', resource.url);
        
        // H5 环境下用 window.open
        // #ifdef H5
        window.open(resource.url, '_blank');
        // #endif
        
        // App 环境下用 plus.runtime.openURL
        // #ifdef APP-PLUS
        plus.runtime.openURL(resource.url);
        // #endif
        
        // 小程序环境下提示用户
        // #ifndef H5 || APP-PLUS
        uni.showModal({
          title: '提示',
          content: '将为您复制链接地址，请在浏览器中粘贴访问',
          confirmText: '复制链接',
          success: (res) => {
            if (res.confirm) {
              uni.setClipboardData({
                data: resource.url,
                success: () => {
                  uni.showToast({
                    title: '链接已复制到剪贴板',
                    icon: 'success'
                  });
                }
              });
            }
          }
        });
        // #endif
      } else {
        console.log('Internal navigation for resource:', resource.id);
        // 原有的内部导航逻辑
        uni.navigateTo({
          url: `/pages/resources/resource-detail?id=${resource.id}&type=${this.currentResourceTab}`,
        });
      }
    },
  },
};
</script>

<style scoped>
.emergency-container {
  padding: 40rpx 0 0;
  background: linear-gradient(135deg, #ffe6e6 0%, #fff5f5 50%, #ffffff 100%);
  min-height: 100vh;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #c53030;
  margin-bottom: 24rpx;
  padding: 0 40rpx;
  display: block;
}

.hotline-section {
  margin-bottom: 40rpx;
}

.hotline-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  margin: 0 40rpx 16rpx;
  border-radius: 20rpx;
  padding: 32rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 8rpx 32rpx rgba(197, 48, 48, 0.15);
  border: 1rpx solid rgba(197, 48, 48, 0.1);
  transition: all 0.3s ease;
}

.hotline-card:active {
  transform: translateY(2rpx) scale(0.98);
  box-shadow: 0 4rpx 16rpx rgba(197, 48, 48, 0.25);
}

.hotline-info {
  flex: 1;
}

.hotline-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #c53030;
  margin-bottom: 8rpx;
  display: block;
}

.hotline-desc {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 12rpx;
  display: block;
}

.hotline-details {
  display: flex;
  gap: 20rpx;
}

.hotline-time {
  font-size: 22rpx;
  color: #999;
}

.hotline-type {
  font-size: 22rpx;
  color: #e53e3e;
  background: linear-gradient(135deg, #fed7d7 0%, #fee2e2 100%);
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  border: 1rpx solid rgba(229, 62, 62, 0.2);
}

.hotline-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.hotline-number {
  font-size: 24rpx;
  font-weight: bold;
  color: #c53030;
}

.call-icon {
  font-size: 24rpx;
  color: #e53e3e;
  background: linear-gradient(135deg, #fed7d7 0%, #fee2e2 100%);
  padding: 8rpx 12rpx;
  border-radius: 8rpx;
  border: 1rpx solid rgba(229, 62, 62, 0.2);
}

.online-section {
  margin-bottom: 40rpx;
}

.service-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  margin: 0 40rpx 16rpx;
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(197, 48, 48, 0.1);
  border: 1rpx solid rgba(197, 48, 48, 0.1);
}

.service-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.service-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.service-info {
  flex: 1;
}

.service-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #c53030;
  margin-bottom: 4rpx;
  display: block;
}

.service-status {
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
}

.service-status.online {
  background-color: #f6ffed;
  color: #52c41a;
}

.service-status.busy {
  background-color: #fff7e6;
  color: #fa8c16;
}

.service-status.offline {
  background-color: #f5f5f5;
  color: #999;
}

.service-desc {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 16rpx;
  line-height: 1.6;
}

.service-features {
  display: flex;
  gap: 12rpx;
  flex-wrap: wrap;
}

.feature-tag {
  font-size: 20rpx;
  color: #e53e3e;
  background: linear-gradient(135deg, #fed7d7 0%, #fee2e2 100%);
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  border: 1rpx solid rgba(229, 62, 62, 0.2);
}

.tools-section {
  margin-bottom: 40rpx;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
  padding: 0 40rpx;
}

.tool-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx 24rpx;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(197, 48, 48, 0.1);
  border: 1rpx solid rgba(197, 48, 48, 0.1);
  transition: all 0.3s ease;
}

.tool-card:active {
  transform: scale(0.95);
  box-shadow: 0 4rpx 16rpx rgba(197, 48, 48, 0.2);
}

.tool-icon {
  font-size: 48rpx;
  margin-bottom: 16rpx;
  display: block;
  color: #c53030;
}

.tool-name {
  font-size: 26rpx;
  font-weight: bold;
  color: #c53030;
  margin-bottom: 8rpx;
  display: block;
}

.tool-desc {
  font-size: 22rpx;
  color: #666;
  line-height: 1.4;
}

.contacts-section {
  margin-bottom: 40rpx;
}

.contacts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40rpx;
  margin-bottom: 24rpx;
}

.add-contact {
  font-size: 26rpx;
  color: #667eea;
  background-color: #f0f4ff;
  padding: 12rpx 20rpx;
  border-radius: 20rpx;
}

.no-contacts {
  background-color: white;
  margin: 0 40rpx;
  border-radius: 16rpx;
  padding: 60rpx 32rpx;
  text-align: center;
}

.no-contacts-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
  display: block;
  opacity: 0.5;
}

.no-contacts-text {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.no-contacts-desc {
  font-size: 24rpx;
  color: #666;
}

.contact-card {
  background-color: white;
  margin: 0 40rpx 16rpx;
  border-radius: 16rpx;
  padding: 32rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.contact-relation {
  font-size: 24rpx;
  color: #666;
}

.contact-actions {
  display: flex;
  gap: 12rpx;
}

.contact-btn {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
}

.contact-btn.call {
  background-color: #52c41a;
  color: white;
}

.contact-btn.message {
  background-color: #1890ff;
  color: white;
}

.safety-plan {
  margin-bottom: 40rpx;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40rpx;
  margin-bottom: 24rpx;
}

.plan-status {
  font-size: 22rpx;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  background-color: #f5f5f5;
  color: #999;
}

.plan-status.has-plan {
  background-color: #f6ffed;
  color: #52c41a;
}

.plan-card {
  background-color: white;
  margin: 0 40rpx;
  border-radius: 16rpx;
  padding: 32rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.plan-icon {
  font-size: 48rpx;
  margin-right: 24rpx;
}

.plan-content {
  flex: 1;
}

.plan-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.plan-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.plan-arrow {
  font-size: 32rpx;
  color: #ccc;
}

.resources-section {
  margin-bottom: 40rpx;
}

.resources-tabs {
  display: flex;
  padding: 0 40rpx;
  margin-bottom: 24rpx;
  gap: 8rpx;
}

.tab-item {
  flex: 1;
  padding: 16rpx;
  text-align: center;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10rpx);
  border-radius: 16rpx;
  border: 1rpx solid rgba(197, 48, 48, 0.1);
  transition: all 0.3s ease;
}

.tab-item.active {
  background: linear-gradient(135deg, #c53030 0%, #e53e3e 100%);
  color: white;
  box-shadow: 0 4rpx 16rpx rgba(197, 48, 48, 0.3);
}

.tab-text {
  font-size: 26rpx;
  color: #666;
}

.tab-item.active .tab-text {
  color: white;
  font-weight: bold;
}

.resources-content {
  padding: 0 40rpx;
}

.resource-item {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 8rpx 32rpx rgba(197, 48, 48, 0.1);
  border: 1rpx solid rgba(197, 48, 48, 0.1);
  transition: all 0.3s ease;
}

.resource-item:active {
  transform: translateY(-2rpx);
  box-shadow: 0 12rpx 40rpx rgba(197, 48, 48, 0.2);
}

.resource-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #c53030;
  margin-bottom: 12rpx;
  display: block;
  line-height: 1.4;
}

.resource-desc {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 16rpx;
  line-height: 1.6;
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-type {
  font-size: 22rpx;
  color: #e53e3e;
  background: linear-gradient(135deg, #fed7d7 0%, #fee2e2 100%);
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  border: 1rpx solid rgba(229, 62, 62, 0.2);
}

.resource-time {
  font-size: 22rpx;
  color: #999;
}

.btn-text {
  font-size: inherit;
  color: inherit;
}

.btn-icon {
  font-size: inherit;
  color: inherit;
}

/* 动画效果 */
.assessment-card {
  animation: bounceIn 0.6s ease-out;
}

.hotline-card,
.service-card {
  animation: fadeInUp 0.5s ease-out;
}

.tool-card {
  animation: zoomIn 0.4s ease-out;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(-20rpx);
  }

  50% {
    transform: scale(1.05) translateY(0);
  }

  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 紧急状态高亮效果 */
.action-btn.emergency {
  position: relative;
  overflow: hidden;
}

.action-btn.emergency::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.5s;
}

.action-btn.emergency:active::before {
  left: 100%;
}

/* 热线卡片悬停效果 */
.hotline-card {
  border-left: 4rpx solid transparent;
  transition: all 0.3s ease;
}

.hotline-card:hover {
  border-left-color: #ff6b6b;
  box-shadow: 0 8rpx 24rpx rgba(255, 107, 107, 0.2);
}

/* 服务状态指示器 */
.service-status {
  position: relative;
}

.service-status.online::before {
  content: "";
  position: absolute;
  left: -16rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  background-color: #52c41a;
  animation: pulse 2s infinite;
}

.service-status.busy::before {
  content: "";
  position: absolute;
  left: -16rpx;
  top: 50%;
  transform: translateY(-50%);
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  background-color: #fa8c16;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(82, 196, 26, 0.7);
  }

  70% {
    box-shadow: 0 0 0 10rpx rgba(82, 196, 26, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(82, 196, 26, 0);
  }
}

/* 工具网格布局优化 */
@media (max-width: 750rpx) {
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12rpx;
  }

  .tool-card {
    padding: 24rpx 16rpx;
  }

  .tool-icon {
    font-size: 40rpx;
  }
}

@media (max-width: 480rpx) {
  .assessment-actions {
    flex-direction: column;
    gap: 16rpx;
  }

  .action-btn {
    width: 100%;
  }

  .hotline-card {
    flex-direction: column;
    text-align: center;
    gap: 20rpx;
  }

  .hotline-info {
    text-align: center;
  }

  .resources-tabs {
    flex-wrap: wrap;
    gap: 8rpx;
  }

  .tab-item {
    min-width: 120rpx;
  }
}

/* 紧急联系人按钮样式增强 */
.contact-btn {
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.contact-btn:active {
  transform: scale(0.95);
  box-shadow: 0 1rpx 4rpx rgba(0, 0, 0, 0.2);
}

.contact-btn.call:active {
  background-color: #389e0d;
}

.contact-btn.message:active {
  background-color: #096dd9;
}

/* 安全计划卡片增强 */
.plan-card {
  border: 2rpx solid transparent;
  transition: all 0.3s ease;
}

.plan-card:active {
  border-color: #667eea;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.2);
  transform: translateY(-2rpx);
}

/* 资源标签样式优化 */
.feature-tag {
  transition: all 0.3s ease;
}

.service-card:active .feature-tag {
  background-color: #667eea;
  color: white;
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
  background: #c53030;
  border-radius: 3rpx;
}

::-webkit-scrollbar-thumb:hover {
  background: #e53e3e;
}

/* 焦点状态 */
.action-btn:focus,
.tab-item:focus {
  outline: 2rpx solid #c53030;
  outline-offset: 2rpx;
}

/* 无障碍访问增强 */
.hotline-card[aria-pressed="true"] {
  background: linear-gradient(135deg, #fed7d7 0%, #fee2e2 100%);
  border-color: #c53030;
}

/* 文字选择样式 */
::selection {
  background-color: rgba(255, 107, 107, 0.3);
  color: #333;
}

/* 长按效果 */
.hotline-card:active {
  transform: translateY(2rpx) scale(0.98);
}

.service-card:active {
  transform: translateY(2rpx) scale(0.98);
}

/* 加载状态 */
.emergency-container[data-loading="true"] {
  pointer-events: none;
  opacity: 0.8;
}

/* 错误状态 */
.service-card[data-error="true"] {
  background-color: #fff2f0;
  border: 1rpx solid #ffccc7;
}

.service-card[data-error="true"] .service-name {
  color: #cf1322;
}

/* 成功状态 */
.contact-card[data-success="true"] {
  background-color: #f6ffed;
  border: 1rpx solid #d9f7be;
}

/* 危险状态高亮 */
.assessment-card.urgent {
  animation: urgentPulse 2s infinite;
}

@keyframes urgentPulse {
  0%,
  100% {
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  }

  50% {
    box-shadow: 0 8rpx 24rpx rgba(255, 107, 107, 0.3);
  }
}

/* 底部安全间距 */
.emergency-container {
  padding-bottom: env(safe-area-inset-bottom);
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .action-btn.emergency {
    border: 2rpx solid #000;
  }

  .hotline-card,
  .service-card,
  .tool-card {
    border: 1rpx solid #333;
  }
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
