<!-- 
  心灵预警集成示例 - 悄悄话发布页面
  展示如何集成心灵预警气泡组件
-->
<template>
  <view class="write-whisper-page">
    <!-- 内容输入区域 -->
    <view class="content-section">
      <textarea
        v-model="whisperContent"
        placeholder="分享你的心情..."
        class="content-input"
        @input="onContentInput"
      />
    </view>

    <!-- 提交按钮 -->
    <view class="submit-section">
      <button class="submit-btn" @click="handleSubmit">发布</button>
    </view>

    <!-- 心灵预警气泡 -->
    <crisis-warning-bubble
      :show="showCrisisBubble"
      :risk-level="crisisRiskLevel"
      :message="crisisBubbleMessage"
      :ai-analysis="crisisAiAnalysis"
      :mascot-avatar="currentMascotAvatar"
      @close="handleCloseCrisisBubble"
      @ok="handleCloseCrisisBubble"
      @view-resources="handleViewResources"
    />
  </view>
</template>

<script>
import { api, storage } from "@/utils/api.js";
import CrisisWarningBubble from "@/components/crisis-warning-bubble.vue";

export default {
  name: "WriteWhisperExample",

  components: {
    CrisisWarningBubble,
  },

  data() {
    return {
      whisperContent: "",

      // 心灵预警相关
      showCrisisBubble: false,
      crisisRiskLevel: "low",
      crisisBubbleMessage: "",
      crisisAiAnalysis: "",
      currentMascotAvatar: "/static/images/mascot-default.png",

      // 实时检测防抖定时器
      quickCheckTimer: null,
    };
  },

  methods: {
    /**
     * 内容输入时的实时关键词检测（可选功能）
     */
    onContentInput(e) {
      const content = e.detail.value;

      // 清除之前的定时器
      if (this.quickCheckTimer) {
        clearTimeout(this.quickCheckTimer);
      }

      // 内容长度不足，不检测
      if (content.length < 10) return;

      // 防抖：500ms后执行检测
      this.quickCheckTimer = setTimeout(async () => {
        await this.performQuickCheck(content);
      }, 500);
    },

    /**
     * 快速关键词检测（不使用AI，适合实时）
     */
    async performQuickCheck(content) {
      const token = storage.getToken();
      if (!token) return;

      try {
        const result = await api.quickCrisisCheck(token, content, "tree-hole");

        if (result.has_risk && result.detected_keywords.length > 0) {
          // 检测到风险关键词，显示轻提示
          console.log("⚠️ 检测到敏感关键词:", result.detected_keywords);

          // 可以在这里显示一个小提示（不打断用户输入）
          // 例如：轻微的颜色变化或小图标
        }
      } catch (error) {
        console.error("快速检测失败:", error);
      }
    },

    /**
     * 提交悄悄话
     */
    async handleSubmit() {
      if (!this.whisperContent.trim()) {
        uni.showToast({
          title: "请输入内容",
          icon: "none",
        });
        return;
      }

      const token = storage.getToken();
      if (!token) {
        uni.navigateTo({
          url: "/pages/login/login",
        });
        return;
      }

      uni.showLoading({
        title: "发布中...",
      });

      try {
        // 构建悄悄话数据
        const whisperData = {
          content: this.whisperContent,
          mood: "neutral",
          is_anonymous: true,
          anonymous_name: this.generateRandomName(),
          anonymous_avatar: this.generateRandomAvatar(),
          tags: [],
          images: [],
        };

        // 调用API发布悄悄话
        const response = await api.createWhisper(token, whisperData);

        uni.hideLoading();

        // ============ 心灵预警处理 ============
        if (
          response.crisis_warning &&
          response.crisis_warning.should_show_bubble
        ) {
          // 显示心灵预警气泡
          this.showCrisisBubble = true;
          this.crisisRiskLevel = response.crisis_warning.risk_level;
          this.crisisBubbleMessage = response.crisis_warning.bubble_message;
          this.crisisAiAnalysis = response.crisis_warning.ai_brief_analysis;

          console.log("🔍 心灵预警触发:", {
            level: this.crisisRiskLevel,
            message: this.crisisBubbleMessage,
          });

          // 根据风险等级给予不同反馈
          if (response.crisis_warning.risk_level === "critical") {
            // 严重风险：额外提示
            setTimeout(() => {
              uni.showModal({
                title: "我们关心你",
                content:
                  "如果你正在经历困难时刻，请不要犹豫，及时寻求帮助。心理健康热线：400-161-9995",
                showCancel: true,
                confirmText: "我知道了",
                cancelText: "拨打热线",
                success: (res) => {
                  if (res.cancel) {
                    uni.makePhoneCall({
                      phoneNumber: "4001619995",
                    });
                  }
                },
              });
            }, 3000); // 3秒后显示
          }
        }

        // 发布成功提示
        uni.showToast({
          title: "发布成功",
          icon: "success",
        });

        // 清空输入
        this.whisperContent = "";

        // 延迟返回（给用户时间看气泡）
        setTimeout(() => {
          if (!this.showCrisisBubble) {
            uni.navigateBack();
          }
        }, 1500);
      } catch (error) {
        uni.hideLoading();

        console.error("发布失败:", error);

        let errorMsg = "发布失败，请稍后重试";
        if (error.responseData && error.responseData.detail) {
          errorMsg = error.responseData.detail;
        }

        uni.showToast({
          title: errorMsg,
          icon: "none",
          duration: 2000,
        });
      }
    },

    /**
     * 关闭心灵预警气泡
     */
    handleCloseCrisisBubble() {
      this.showCrisisBubble = false;

      // 气泡关闭后返回
      setTimeout(() => {
        uni.navigateBack();
      }, 300);
    },

    /**
     * 查看心理健康资源
     */
    handleViewResources(riskLevel) {
      console.log("查看资源，风险等级:", riskLevel);

      // 可以跳转到资源页面或显示资源列表
      uni.showModal({
        title: "心理健康资源",
        content:
          "全国心理援助热线：400-161-9995\n\n提供24小时免费专业心理咨询服务\n\n如果你正在经历心理危机，请不要犹豫，及时寻求帮助。",
        showCancel: true,
        cancelText: "我知道了",
        confirmText: "拨打热线",
        success: (res) => {
          if (res.confirm) {
            uni.makePhoneCall({
              phoneNumber: "4001619995",
            });
          }
        },
      });
    },

    /**
     * 生成随机匿名昵称
     */
    generateRandomName() {
      const names = ["匿名用户", "路过的小透明", "树洞里的声音", "神秘人"];
      return names[Math.floor(Math.random() * names.length)];
    },

    /**
     * 生成随机匿名头像
     */
    generateRandomAvatar() {
      const avatars = [
        "/static/images/avatar1.png",
        "/static/images/avatar2.png",
        "/static/images/avatar3.png",
      ];
      return avatars[Math.floor(Math.random() * avatars.length)];
    },
  },

  onLoad() {
    // 获取当前看板娘头像（用于气泡显示）
    const token = storage.getToken();
    if (token) {
      api
        .getCurrentMascotOutfit(token)
        .then((outfit) => {
          if (outfit && outfit.avatar_url) {
            this.currentMascotAvatar = outfit.avatar_url;
          }
        })
        .catch((err) => {
          console.log("获取看板娘头像失败:", err);
        });
    }
  },

  beforeUnmount() {
    // 清理定时器
    if (this.quickCheckTimer) {
      clearTimeout(this.quickCheckTimer);
    }
  },
};
</script>

<style scoped lang="scss">
.write-whisper-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 30rpx;
}

.content-section {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.content-input {
  width: 100%;
  min-height: 400rpx;
  font-size: 28rpx;
  line-height: 1.6;
}

.submit-section {
  padding: 20rpx 0;
}

.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: #fff;
  border: none;
  border-radius: 12rpx;
  font-size: 32rpx;
  font-weight: 600;
  height: 88rpx;
  line-height: 88rpx;
}
</style>
