<template>
  <view class="assessment-list-container">
    <view class="header">
      <text class="title">心理测评</text>
      <text class="subtitle">多维度了解自己的心理状态</text>
    </view>

    <view class="assessment-categories">
      <view
        class="category-section"
        v-for="category in assessmentCategories"
        :key="category.id"
      >
        <view class="category-header">
          <text class="category-icon">{{ category.icon }}</text>
          <text class="category-title">{{ category.name }}</text>
        </view>

        <view class="assessment-list">
          <view
            class="assessment-item"
            v-for="assessment in category.assessments"
            :key="assessment.id"
            @click="openAssessment(assessment)"
          >
            <view class="item-content">
              <view class="item-header">
                <text class="item-title">{{ assessment.name }}</text>
                <view class="item-tags">
                  <text class="tag" v-for="tag in assessment.tags" :key="tag">{{
                    tag
                  }}</text>
                </view>
              </view>
              <text class="item-desc">{{ assessment.description }}</text>
              <view class="item-info">
                <text class="info-text">约 {{ assessment.duration }} 分钟</text>
                <text class="info-text">{{ assessment.questions }} 题</text>
              </view>
            </view>
            <view class="item-arrow">
              <text class="arrow">→</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 温馨提示 -->
    <view class="notice-card">
      <view class="notice-header">
        <text class="notice-icon">💡</text>
        <text class="notice-title">温馨提示</text>
      </view>
      <text class="notice-text"
        >测评结果仅供参考，如有专业需求建议咨询心理健康专家</text
      >
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      assessmentCategories: [
        {
          id: 1,
          name: "性格特质",
          icon: "🎭",
          assessments: [
            {
              id: "mbti",
              name: "MBTI 人格类型测试",
              description: "探索你的性格类型，了解自己的行为模式和思维方式",
              duration: 15,
              questions: 93,
              tags: ["经典", "权威"],
              url: "https://www.16personalities.com/ch",
            },
            {
              id: "big-five",
              name: "大五人格测试",
              description: "从五个维度全面分析你的人格特征",
              duration: 10,
              questions: 44,
              tags: ["科学", "全面"],
              url: "https://www.truity.com/test/big-five-personality-test",
            },
            {
              id: "enneagram",
              name: "九型人格测试",
              description: "发现你的核心动机和内在驱动力",
              duration: 12,
              questions: 108,
              tags: ["深度", "自我认知"],
              url: "https://www.eclecticenergies.com/chinese/enneagram/test",
            },
          ],
        },
        {
          id: 2,
          name: "情感心理",
          icon: "💝",
          assessments: [
            {
              id: "eq-test",
              name: "情商测试 (EQ)",
              description: "评估你的情绪智能和人际交往能力",
              duration: 8,
              questions: 68,
              tags: ["情商", "人际"],
              url: "https://www.mindtools.com/pages/article/ei-quiz.htm",
            },
            {
              id: "attachment-style",
              name: "依恋类型测试",
              description: "了解你在亲密关系中的依恋模式",
              duration: 6,
              questions: 36,
              tags: ["关系", "依恋"],
              url: "https://www.web-research-design.net/cgi-bin/crq/crq.pl",
            },
            {
              id: "love-language",
              name: "爱的语言测试",
              description: "发现你表达和接收爱意的主要方式",
              duration: 5,
              questions: 30,
              tags: ["爱情", "沟通"],
              url: "https://www.5lovelanguages.com/quizzes/",
            },
          ],
        },
        {
          id: 3,
          name: "心理健康",
          icon: "🧘",
          assessments: [
            {
              id: "depression-scale",
              name: "PHQ-9 抑郁自评量表",
              description: "评估近期的抑郁症状和严重程度",
              duration: 3,
              questions: 9,
              tags: ["抑郁", "筛查"],
              url: "https://www.mdcalc.com/phq-9-patient-health-questionnaire-9",
            },
            {
              id: "anxiety-scale",
              name: "GAD-7 焦虑自评量表",
              description: "评估广泛性焦虑障碍的症状",
              duration: 3,
              questions: 7,
              tags: ["焦虑", "筛查"],
              url: "https://www.mdcalc.com/gad-7-general-anxiety-disorder-7",
            },
            {
              id: "stress-scale",
              name: "压力感知量表",
              description: "评估你对生活压力的感知程度",
              duration: 5,
              questions: 14,
              tags: ["压力", "生活"],
              url: "https://www.mindgarden.com/pss-10-perceived-stress-scale",
            },
          ],
        },
        {
          id: 4,
          name: "职业发展",
          icon: "🚀",
          assessments: [
            {
              id: "career-interest",
              name: "霍兰德职业兴趣测试",
              description: "发现适合你的职业类型和发展方向",
              duration: 12,
              questions: 60,
              tags: ["职业", "兴趣"],
              url: "https://www.mynextmove.org/explore/ip",
            },
            {
              id: "leadership-style",
              name: "领导力风格测试",
              description: "了解你的领导风格和管理特点",
              duration: 8,
              questions: 40,
              tags: ["领导力", "管理"],
              url: "https://www.mindtools.com/pages/article/leadership-style-quiz.htm",
            },
            {
              id: "work-values",
              name: "工作价值观测试",
              description: "探索你在工作中最看重的价值观",
              duration: 6,
              questions: 21,
              tags: ["价值观", "职场"],
              url: "https://www.mynextmove.org/explore/work-values-matcher",
            },
          ],
        },
      ],
    };
  },

  methods: {
    openAssessment(assessment) {
      // 显示确认对话框
      uni.showModal({
        title: "跳转提示",
        content: `即将跳转到 ${assessment.name} 测试页面，是否继续？`,
        confirmText: "确定",
        cancelText: "取消",
        success: (res) => {
          if (res.confirm) {
            // 复制链接到剪贴板
            uni.setClipboardData({
              data: assessment.url,
              success: () => {
                uni.showToast({
                  title: "链接已复制到剪贴板",
                  icon: "success",
                  duration: 2000,
                });

                // 延迟后打开浏览器
                setTimeout(() => {
                  // 尝试直接打开链接
                  // #ifdef H5
                  window.open(assessment.url, "_blank");
                  // #endif

                  // #ifdef APP-PLUS
                  plus.runtime.openURL(assessment.url);
                  // #endif

                  // #ifdef MP
                  uni.showModal({
                    title: "提示",
                    content: "请在浏览器中打开复制的链接完成测试",
                    showCancel: false,
                  });
                  // #endif
                }, 500);
              },
            });
          }
        },
      });
    },
  },
};
</script>

<style scoped>
.assessment-list-container {
  padding: 40rpx;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.header {
  margin-bottom: 40rpx;
  text-align: center;
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

.assessment-categories {
  margin-bottom: 40rpx;
}

.category-section {
  margin-bottom: 40rpx;
}

.category-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 0 10rpx;
}

.category-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.category-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.assessment-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.assessment-item {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.assessment-item:active {
  background-color: #f5f5f5;
  transform: translateY(2rpx);
}

.item-content {
  flex: 1;
}

.item-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.item-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
}

.item-tags {
  display: flex;
  gap: 8rpx;
  flex-shrink: 0;
  margin-left: 20rpx;
}

.tag {
  padding: 4rpx 12rpx;
  background-color: #e3f2fd;
  color: #1976d2;
  font-size: 22rpx;
  border-radius: 12rpx;
  font-weight: 500;
}

.item-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16rpx;
}

.item-info {
  display: flex;
  gap: 24rpx;
}

.info-text {
  font-size: 24rpx;
  color: #999;
  background-color: #f5f5f5;
  padding: 6rpx 12rpx;
  border-radius: 8rpx;
}

.item-arrow {
  margin-left: 20rpx;
  display: flex;
  align-items: center;
}

.arrow {
  font-size: 28rpx;
  color: #ccc;
  font-weight: bold;
}

.notice-card {
  background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-top: 20rpx;
}

.notice-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.notice-icon {
  font-size: 24rpx;
  margin-right: 12rpx;
}

.notice-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.notice-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .item-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .item-tags {
    margin-left: 0;
    margin-top: 12rpx;
  }
}
</style>
