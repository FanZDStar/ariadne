<template>
  <view class="emotional-trend-chart">
    <view class="chart-header">
      <text class="chart-title">{{ getCurrentPeriodLabel() }}情感变化趋势</text>
      <view class="chart-controls">
        <!-- 单项模式才显示数据源选择器 -->
        <view class="data-source-selector" v-if="chartMode === 'single'">
          <scroll-view class="source-scroll" scroll-x>
            <view class="source-list">
              <view
                class="source-item"
                v-for="source in dataSources"
                :key="source.value"
                :class="{
                  active: activeSources.includes(source.value),
                  disabled: !source.enabled,
                  loading: loadingStates[source.value],
                }"
                @click="toggleDataSource(source.value)"
              >
                <view class="source-content">
                  <text
                    class="source-icon"
                    v-if="!loadingStates[source.value]"
                    >{{ source.icon }}</text
                  >
                  <view
                    class="loading-spinner"
                    v-if="loadingStates[source.value]"
                  >
                    <text class="spinner">⏳</text>
                  </view>
                  <text class="source-text">{{ source.label }}</text>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>
        <!-- 综合模式显示说明文字 -->
        <view class="combined-mode-info" v-if="chartMode === 'combined'">
          <text class="info-text">🧠 综合分析三个维度的心理状态</text>
      </view>
        <view class="chart-mode-toggle">
          <view
            class="mode-btn"
            :class="{ active: chartMode === 'single' }"
            @click="setChartMode('single')"
          >
            <text class="mode-text">单项</text>
          </view>
          <view
            class="mode-btn"
            :class="{ active: chartMode === 'combined' }"
            @click="setChartMode('combined')"
          >
            <text class="mode-text">综合</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 全局加载状态 -->
    <view class="loading-overlay" v-if="isLoading">
      <view class="loading-content">
        <text class="loading-spinner">⏳</text>
        <text class="loading-text">加载数据中...</text>
      </view>
    </view>

    <!-- 统计信息 - 移到图表上方 -->
    <view class="stats-container" v-if="hasChartData && !isLoading">
      <view class="stats-card">
        <text class="stats-title">统计信息</text>
        <view class="stats-content">
          <view class="stats-item">
            <text class="stats-label">平均心情值</text>
            <text class="stats-value">{{ averageMood }}</text>
          </view>
          <view class="stats-item">
            <text class="stats-label">最高心情值</text>
            <text class="stats-value">{{ maxMood }}</text>
          </view>
          <view class="stats-item">
            <text class="stats-label">最低心情值</text>
            <text class="stats-value">{{ minMood }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="chart-wrapper" v-if="hasChartData && !isLoading">
      <view class="enhanced-chart">
        <view class="y-axis">
          <text class="y-label" v-for="label in yAxisLabels" :key="label">{{
            label
          }}</text>
        </view>
        <view class="chart-content">
          <canvas
            class="chart-canvas"
            :canvas-id="canvasId"
            :id="canvasId"
            disable-scroll="true"
            @touchstart="onChartTouchStart"
            @touchmove="onChartTouchMove"
            @touchend="onChartTouchEnd"
          ></canvas>
          <view class="x-axis">
            <text
              class="x-label"
              v-for="(point, index) in getVisibleXLabels()"
              :key="index"
              :style="{ left: `${getPointX(point.index)}%` }"
            >
              {{ point.label }}
            </text>
          </view>
          <!-- 数据点提示 -->
          <view
            class="data-tooltip"
            v-if="tooltipData.show"
            :style="{ left: tooltipData.x + 'px', top: tooltipData.y + 'px' }"
          >
            <text class="tooltip-date">{{ tooltipData.date }}</text>
            <view
              class="tooltip-item"
              v-for="item in tooltipData.data"
              :key="item.source"
            >
              <view
                class="tooltip-color"
                :style="{ backgroundColor: item.color }"
              ></view>
              <text class="tooltip-text"
                >{{ item.label }}: {{ item.value }}</text
              >
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="empty-chart" v-else-if="!isLoading">
      <text class="empty-text">暂无数据</text>
      <text class="empty-desc" v-if="activeSources.length === 0"
        >请选择数据源开始查看情感趋势</text
      >
      <text class="empty-desc" v-else
        >所选数据源暂无数据，请等待数据加载或选择其他数据源</text
      >
      <view class="empty-tips">
        <text class="tip-text">💡 提示：</text>
        <text class="tip-text">• 记录一些心情和日记来生成数据</text>
        <text class="tip-text">• 尝试切换不同的时间段</text>
      </view>
    </view>
  </view>
</template>

<script>
import { api, storage } from "../utils/api.js";

export default {
  name: "EmotionalTrendChart",
  props: {
    currentPeriod: {
      type: String,
      default: "7days",
    },
    periods: {
      type: Array,
      default: () => [
        { value: "3days", label: "近3天" },
        { value: "7days", label: "近7天" },
        { value: "30days", label: "近30天" },
        { value: "60days", label: "近60天" },
      ],
    },
    isLoggedIn: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      canvasId: `emotionalTrendChart_${Date.now()}`, // 唯一的canvas id

      // 数据源配置
      dataSources: [
        {
          value: "mood_tracker",
          label: "心情晴雨表",
          icon: "🌤️",
          color: "#007aff",
          enabled: true,
        },
        {
          value: "diary_emotion",
          label: "碎碎念情感",
          icon: "📝",
          color: "#ff6b9d",
          enabled: true,
        },
        {
          value: "risk_assessment",
          label: "心理状态",
          icon: "🧠",
          color: "#ff9500",
          enabled: true,
        },
      ],

      activeSources: ["mood_tracker"], // 默认激活心情晴雨表
      chartMode: "single", // 'single' 或 'combined'

      // 图表数据
      chartDataSets: {
        mood_tracker: [],
        diary_emotion: [],
        risk_assessment: [],
      },

      // 综合得分数据
      combinedScoreData: [],

      // 统计数据
      averageMood: "0.00",
      maxMood: "0.00",
      minMood: "0.00",

      // 加载状态
      loadingStates: {
        mood_tracker: false,
        diary_emotion: false,
        risk_assessment: false,
      },

      // 交互数据
      tooltipData: {
        show: false,
        x: 0,
        y: 0,
        date: "",
        data: [],
      },

      touchData: {
        touching: false,
        startX: 0,
      },

      // 数据缓存相关
      loadingTimeout: null, // 防抖定时器
      cachedDiaries: null, // 缓存的日记数据
      diaryLastFetchTime: null, // 日记数据最后获取时间
      processedDiaries: null, // 缓存的处理后日记数据
      cachedRiskReports: null, // 缓存的风险评估报告
      riskLastFetchTime: null, // 风险评估最后获取时间
    };
  },

  computed: {
    hasChartData() {
      if (this.chartMode === "combined") {
        // 综合模式检查综合得分数据
        return this.combinedScoreData && this.combinedScoreData.length > 0;
      } else {
        // 单项模式检查激活数据源
        return this.activeSources.some(
          (source) =>
            this.chartDataSets[source] && this.chartDataSets[source].length > 0
        );
      }
    },

    yAxisLabels() {
      return ["5.0", "4.0", "3.0", "2.0", "1.0"];
    },

    // 是否有数据源正在加载
    isLoading() {
      return Object.values(this.loadingStates).some((loading) => loading);
    },

    // 获取当前激活的数据源是否都已加载完成
    activeSourcesLoaded() {
      return this.activeSources.every((source) => !this.loadingStates[source]);
    },
  },

  watch: {
    chartDataSets: {
      handler(newVal) {
        if (newVal) {
          this.$nextTick(() => this.drawEnhancedChart());
        }
      },
      deep: true,
    },

    activeSources(newVal) {
      this.calculateCombinedStats();
      this.$nextTick(() => this.drawEnhancedChart());
    },

    chartMode(newVal) {
      this.$nextTick(() => this.drawEnhancedChart());
    },

    currentPeriod: {
      handler(newVal) {
        if (newVal) {
          this.loadAllData();
        }
      },
      immediate: false,
    },
  },

  mounted() {
    this.loadAllData();
  },

  methods: {
    toggleDataSource(sourceValue) {
      // 只在单项模式下允许切换数据源
      if (this.chartMode !== "single") return;

      const source = this.dataSources.find((s) => s.value === sourceValue);
      if (!source || !source.enabled) return;

      // 单项模式：只能选择一个数据源
      this.activeSources = [sourceValue];
      console.log(`单项模式，设置激活源为: [${sourceValue}]`);

      // 重新绘制图表
      this.$nextTick(() => {
        this.drawEnhancedChart();
      });
    },

    setChartMode(mode) {
      this.chartMode = mode;

      // 重新计算统计数据和综合得分
      this.calculateCombinedStats();

      // 重新绘制图表
      this.$nextTick(() => {
        this.drawEnhancedChart();
      });
    },

    getActiveSources() {
      return this.dataSources.filter((source) =>
        this.activeSources.includes(source.value)
      );
    },

    async loadAllData() {
      const token = storage.getToken();

      console.log("=== 开始加载所有数据 ===");
      console.log("Token状态:", token ? "存在" : "不存在");

      if (!token) {
        console.warn("没有token，用户可能未登录");
        // 如果没有token，使用模拟数据
        this.generateMockMoodData();
        this.generateMockDiaryEmotionData();
        this.generateMockRiskAssessmentData();
        return;
      }

      // 防抖处理，避免频繁切换时间段导致重复请求
      if (this.loadingTimeout) {
        clearTimeout(this.loadingTimeout);
      }

      this.loadingTimeout = setTimeout(async () => {
        try {
          // 只加载心情数据，其他数据进行缓存优化
          await Promise.all([
            this.loadMoodTrackerData(token),
            this.loadDiaryEmotionDataOptimized(token),
            this.loadRiskAssessmentDataOptimized(token),
          ]);

          this.calculateCombinedStats();
          console.log("=== 所有数据加载完成 ===");
        } catch (error) {
          console.error("获取数据失败:", error);
        }
      }, 300); // 300ms 防抖延迟
    },

    async loadMoodTrackerData(token) {
      this.loadingStates.mood_tracker = true;
      try {
        const response = await api.getMoodStats(token, this.currentPeriod);
        const moodData = response.data || response.mood_data || [];

        if (moodData.length > 0) {
          this.chartDataSets.mood_tracker = moodData.map((item) => ({
            date: item.time || item.date,
            value: item.mood_score || item.average_mood || item.value,
            source: "mood_tracker",
          }));
        } else {
          // 如果没有真实数据，生成模拟数据
          this.generateMockMoodData();
        }

        console.log(
          "心情晴雨表数据加载成功:",
          this.chartDataSets.mood_tracker.length,
          "条记录"
        );
      } catch (error) {
        console.error("获取心情晴雨表数据失败:", error);
        this.generateMockMoodData();
        uni.showToast({
          title: "使用模拟心情数据",
          icon: "none",
          duration: 2000,
        });
      } finally {
        this.loadingStates.mood_tracker = false;
      }
    },

    // 生成模拟心情数据
    generateMockMoodData() {
      const now = new Date();
      const periodDays = {
        "3days": 3,
        "7days": 7,
        "30days": 30,
        "60days": 60,
      };

      const days = periodDays[this.currentPeriod] || 7;
      const mockData = [];

      for (let i = days - 1; i >= 0; i -= Math.max(1, Math.floor(days / 6))) {
        const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
        const dateStr = date.toISOString().split("T")[0];

        // 生成2.5-4.5分的心情评分
        const score = 2.5 + Math.random() * 2;

        mockData.push({
          date: dateStr,
          value: Math.round(score * 10) / 10,
          source: "mood_tracker",
        });
      }

      this.chartDataSets.mood_tracker = mockData;
    },

    async loadDiaryEmotionDataOptimized(token) {
      this.loadingStates.diary_emotion = true;
      try {
        // 检查是否已经有缓存的日记数据
        if (!this.cachedDiaries || this.shouldRefreshDiaryCache()) {
          console.log("重新获取日记数据...");
          // 获取用户日记并分析情感倾向
          const response = await api.getUserDiaries(token);
          const diaries = Array.isArray(response)
            ? response
            : response.data || [];

          // 缓存原始日记数据
          this.cachedDiaries = diaries;
          this.diaryLastFetchTime = Date.now();

          // 预处理日记数据，避免重复处理
          this.processedDiaries = diaries.map((diary) => ({
            ...diary,
            dateOnly: diary.created_at ? diary.created_at.split(" ")[0] : "",
            emotionScore: this.analyzeDiaryEmotion(diary.content || ""),
          }));
        }

        if (this.processedDiaries && this.processedDiaries.length > 0) {
          // 根据时间段筛选日记
          const filteredDiaries = this.filterDataByPeriod(
            this.processedDiaries
          );

          this.chartDataSets.diary_emotion = filteredDiaries.map((diary) => ({
            date: diary.dateOnly,
            value: diary.emotionScore,
            source: "diary_emotion",
          }));
        } else {
          // 如果没有日记数据，生成模拟数据
          this.generateMockDiaryEmotionData();
        }

        console.log(
          "碎碎念情感数据加载成功:",
          this.chartDataSets.diary_emotion.length,
          "条记录"
        );
      } catch (error) {
        console.error("获取碎碎念情感数据失败:", error);
        this.generateMockDiaryEmotionData();
        uni.showToast({
          title: "使用模拟碎碎念数据",
          icon: "none",
          duration: 2000,
        });
      } finally {
        this.loadingStates.diary_emotion = false;
      }
    },

    // 保持原方法作为备用
    async loadDiaryEmotionData(token) {
      return this.loadDiaryEmotionDataOptimized(token);
    },

    // 生成模拟碎碎念情感数据
    generateMockDiaryEmotionData() {
      const now = new Date();
      const periodDays = {
        "3days": 3,
        "7days": 7,
        "30days": 30,
        "60days": 60,
      };

      const days = periodDays[this.currentPeriod] || 7;
      const mockData = [];

      for (let i = days - 1; i >= 0; i -= Math.max(1, Math.floor(days / 5))) {
        const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
        const dateStr = date.toISOString().split("T")[0];

        // 生成2-4.5分的情感评分（稍微偏向积极）
        const score = 2 + Math.random() * 2.5;

        mockData.push({
          date: dateStr,
          value: Math.round(score * 10) / 10,
          source: "diary_emotion",
        });
      }

      this.chartDataSets.diary_emotion = mockData;
    },

    async loadRiskAssessmentDataOptimized(token) {
      this.loadingStates.risk_assessment = true;
      try {
        console.log(
          "开始加载心理评估数据，token:",
          token ? `存在(${token.substring(0, 10)}...)` : "不存在"
        );

        if (!token) {
          console.warn("没有有效token，无法请求API数据，使用模拟数据");
          this.generateMockRiskAssessmentData();
          return;
        }

        // 检查是否需要重新获取风险评估数据
        if (!this.cachedRiskReports || this.shouldRefreshRiskCache()) {
          console.log("重新获取风险评估数据...");
          // 首先尝试从API获取真实数据
          const reports = await api.getRiskAssessmentReports(token, 50);

          // 缓存原始数据
          this.cachedRiskReports = reports;
          this.riskLastFetchTime = Date.now();
        }

        const reports = this.cachedRiskReports;

        console.log("API返回的原始数据:", reports);

        if (reports && reports.length > 0) {
          console.log("找到心理评估报告:", reports.length, "条");

          this.chartDataSets.risk_assessment = reports.map((report, index) => {
            console.log(`处理第${index + 1}个报告:`, report);

            const date = report.report_generated_time
              ? report.report_generated_time.split("T")[0]
              : report.created_at
              ? report.created_at.split(" ")[0]
              : new Date().toISOString().split("T")[0];

            const value = this.convertRiskToScore(
              report.overall_risk_level || report.overall_risk_score
            );

            console.log(
              `报告${index + 1} - 日期: ${date}, 风险等级: ${
                report.overall_risk_level
              }, 评分: ${value}`
            );

            return {
              date,
              value,
              source: "risk_assessment",
            };
          });

          console.log(
            "心理评估数据处理完成:",
            this.chartDataSets.risk_assessment.length,
            "条记录"
          );

          // 如果处理后仍然没有数据，使用模拟数据
          if (this.chartDataSets.risk_assessment.length === 0) {
            console.log("处理后没有有效数据，使用模拟数据");
            this.generateMockRiskAssessmentData();
          }
        } else {
          // 如果没有真实数据，生成模拟数据用于演示
          console.log("API返回空数据或无数据，使用模拟数据");
          this.generateMockRiskAssessmentData();

          // 显示友好提示
          uni.showToast({
            title: "暂无心理评估记录，显示示例数据",
            icon: "none",
            duration: 3000,
          });
        }
      } catch (error) {
        console.error("获取心理状态数据失败:", error);
        console.log("API调用失败，使用模拟心理评估数据");
        this.generateMockRiskAssessmentData();

        // 在开发环境显示友好提示
        if (process.env.NODE_ENV === "development") {
          uni.showToast({
            title: "开发模式：使用模拟数据",
            icon: "none",
            duration: 2000,
          });
        }
      } finally {
        this.loadingStates.risk_assessment = false;
      }
    },

    // 获取风险评估历史数据（原方法，保持向后兼容）
    async loadRiskAssessmentData(token) {
      return this.loadRiskAssessmentDataOptimized(token);
    },

    // 生成模拟心理评估数据
    generateMockRiskAssessmentData() {
      const now = new Date();
      const periodDays = {
        "3days": 3,
        "7days": 7,
        "30days": 30,
        "60days": 60,
      };

      const days = periodDays[this.currentPeriod] || 7;
      const mockData = [];

      // 生成最近几天的模拟评估数据
      for (let i = days - 1; i >= 0; i -= Math.max(1, Math.floor(days / 5))) {
        const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
        const dateStr = date.toISOString().split("T")[0];

        // 生成3-4分的心理健康评分（相对正常水平）
        const score = 3 + Math.random() * 1.5;

        mockData.push({
          date: dateStr,
          value: Math.round(score * 10) / 10,
          source: "risk_assessment",
        });
      }

      this.chartDataSets.risk_assessment = mockData;
      console.log("生成模拟心理评估数据:", mockData.length, "条记录");
    },

    // 数据处理辅助方法
    filterDataByPeriod(data) {
      const now = new Date();
      const periodDays = {
        "3days": 3,
        "7days": 7,
        "30days": 30,
        "60days": 60,
      };

      const days = periodDays[this.currentPeriod] || 7;
      const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

      return data.filter((item) => {
        // 支持多种时间字段格式
        const dateStr =
          item.report_generated_time || item.created_at || item.time;
        if (!dateStr) {
          console.warn("数据项缺少时间字段:", item);
          return true; // 如果没有时间字段，默认包含
        }

        const itemDate = new Date(dateStr);
        const isValid = itemDate >= startDate;

        console.log(
          `时间过滤: ${dateStr} >= ${startDate.toISOString()} = ${isValid}`
        );
        return isValid;
      });
    },

    analyzeDiaryEmotion(content) {
      // 简单的情感分析评分算法
      const positiveWords = [
        "开心",
        "快乐",
        "高兴",
        "兴奋",
        "满足",
        "幸福",
        "愉快",
        "好",
        "棒",
        "爱",
      ];
      const negativeWords = [
        "难过",
        "伤心",
        "痛苦",
        "失望",
        "沮丧",
        "焦虑",
        "担心",
        "害怕",
        "愤怒",
        "糟糕",
      ];

      let score = 3.0; // 中性基准分
      let positiveCount = 0;
      let negativeCount = 0;

      positiveWords.forEach((word) => {
        if (content.includes(word)) positiveCount++;
      });

      negativeWords.forEach((word) => {
        if (content.includes(word)) negativeCount++;
      });

      // 根据积极/消极词汇调整分数
      score += positiveCount * 0.3 - negativeCount * 0.3;

      // 限制在1-5范围内
      return Math.max(1, Math.min(5, score));
    },

    convertRiskToScore(riskLevel) {
      // 如果是数字类型的风险评分，直接转换
      if (typeof riskLevel === "number") {
        // 假设风险评分是0-5，转换为心理健康评分（反向）
        return Math.max(1, Math.min(5, 5 - riskLevel + 1));
      }

      // 如果是字符串类型的风险等级
      const riskMapping = {
        low: 4.5,
        medium: 3.5,
        high: 2.5,
        critical: 1.5,
        低: 4.5,
        中: 3.5,
        高: 2.5,
        严重: 1.5,
      };

      const score =
        riskMapping[riskLevel?.toLowerCase?.()] ||
        riskMapping[riskLevel] ||
        3.0;
      console.log(`风险等级转换: ${riskLevel} -> ${score}`);
      return score;
    },

    drawEnhancedChart() {
      const query = uni.createSelectorQuery().in(this);
      query
        .select(`#${this.canvasId}`)
        .boundingClientRect((data) => {
          if (!data) return;

          const ctx = uni.createCanvasContext(this.canvasId, this);
          const width = data.width;
          const height = data.height;
          const padding = { top: 20, right: 20, bottom: 60, left: 60 };
          const chartWidth = width - padding.left - padding.right;
          const chartHeight = height - padding.top - padding.bottom;

          ctx.clearRect(0, 0, width, height);

          // 绘制背景网格
          this.drawGrid(ctx, padding, chartWidth, chartHeight);

          if (this.chartMode === "single") {
            this.drawSingleChart(ctx, padding, chartWidth, chartHeight);
          } else {
            this.drawCombinedChart(ctx, padding, chartWidth, chartHeight);
          }

          ctx.draw();
        })
        .exec();
    },

    drawGrid(ctx, padding, chartWidth, chartHeight) {
      ctx.beginPath();
      ctx.setStrokeStyle("#f0f0f0");
      ctx.setLineWidth(1);

      // 水平网格线
      for (let i = 0; i <= 4; i++) {
        const y = padding.top + (i / 4) * chartHeight;
        ctx.moveTo(padding.left, y);
        ctx.lineTo(padding.left + chartWidth, y);
      }

      // 垂直网格线
      let gridCount;
      if (this.chartMode === "combined") {
        // 综合模式：基于综合得分数据
        gridCount = this.combinedScoreData.length;
      } else {
        // 单项模式：基于当前数据源长度
        gridCount = Math.max(
          ...this.activeSources.map(
            (source) => this.chartDataSets[source]?.length || 0
          )
        );
      }

      if (gridCount > 1) {
        for (let i = 0; i <= gridCount - 1; i++) {
          const x = padding.left + (i / (gridCount - 1)) * chartWidth;
          ctx.moveTo(x, padding.top);
          ctx.lineTo(x, padding.top + chartHeight);
        }
      }

      ctx.stroke();
    },

    drawSingleChart(ctx, padding, chartWidth, chartHeight) {
      const activeSource = this.activeSources[0];
      if (!activeSource) return;

      const data = this.chartDataSets[activeSource] || [];
      if (data.length === 0) return;

      const sourceConfig = this.dataSources.find(
        (s) => s.value === activeSource
      );
      this.drawDataLine(
        ctx,
        data,
        sourceConfig.color,
        padding,
        chartWidth,
        chartHeight
      );
    },

    drawCombinedChart(ctx, padding, chartWidth, chartHeight) {
      console.log("绘制综合得分图表");

      // 确保有综合得分数据
      if (!this.combinedScoreData || this.combinedScoreData.length === 0) {
        console.log("没有综合得分数据，跳过绘制");
        return;
      }

      console.log("综合得分数据点数:", this.combinedScoreData.length);

      // 绘制综合得分曲线，使用紫色
      this.drawDataLine(
        ctx,
        this.combinedScoreData,
        "#8B5CF6", // 紫色，表示综合分析
        padding,
        chartWidth,
        chartHeight
      );
    },

    drawDataLine(ctx, data, color, padding, chartWidth, chartHeight) {
      if (data.length === 0) return;

      const points = data.map((point, index) => ({
        x: padding.left + (index / Math.max(data.length - 1, 1)) * chartWidth,
        y: padding.top + (1 - (point.value - 1) / 4) * chartHeight,
      }));

      // 绘制线条
      ctx.beginPath();
      ctx.setStrokeStyle(color);
      ctx.setLineWidth(2);

      if (points.length === 1) {
        // 单点绘制为圆点
        ctx.arc(points[0].x, points[0].y, 4, 0, 2 * Math.PI);
        ctx.setFillStyle(color);
        ctx.fill();
      } else {
        // 多点绘制平滑曲线
        ctx.moveTo(points[0].x, points[0].y);

        for (let i = 0; i < points.length - 1; i++) {
          const current = points[i];
          const next = points[i + 1];
          const controlX = current.x + (next.x - current.x) * 0.5;

          ctx.quadraticCurveTo(controlX, current.y, next.x, next.y);
        }
        ctx.stroke();

        // 绘制数据点
        points.forEach((point) => {
          ctx.beginPath();
          ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
          ctx.setFillStyle(color);
          ctx.fill();
        });
      }
    },

    // 交互事件处理
    onChartTouchStart(e) {
      this.touchData.touching = true;
      this.touchData.startX = e.touches[0].x;
    },

    onChartTouchMove(e) {
      if (!this.touchData.touching) return;
      // 这里可以添加滑动查看数据点的逻辑
    },

    onChartTouchEnd(e) {
      this.touchData.touching = false;
      this.tooltipData.show = false;
    },

    calculateCombinedStats() {
      // 计算综合得分
      this.calculateCombinedScore();

      // 计算统计数据
      let allValues = [];

      if (this.chartMode === "combined") {
        // 综合模式使用综合得分数据
        allValues = this.combinedScoreData.map((item) => item.value);
      } else {
        // 单项模式使用激活数据源
        this.activeSources.forEach((sourceValue) => {
          const data = this.chartDataSets[sourceValue] || [];
          allValues = allValues.concat(data.map((item) => item.value));
        });
      }

      if (allValues.length === 0) {
        this.averageMood = "0.00";
        this.maxMood = "0.00";
        this.minMood = "0.00";
        return;
      }

      const sum = allValues.reduce((a, b) => a + b, 0);
      this.averageMood = (sum / allValues.length).toFixed(2);
      this.maxMood = Math.max(...allValues).toFixed(2);
      this.minMood = Math.min(...allValues).toFixed(2);
    },

    // 计算综合得分
    calculateCombinedScore() {
      console.log("开始计算综合得分");

      // 获取所有数据源的数据
      const moodData = this.chartDataSets.mood_tracker || [];
      const diaryData = this.chartDataSets.diary_emotion || [];
      const riskData = this.chartDataSets.risk_assessment || [];

      // 收集所有日期
      const allDates = new Set();
      moodData.forEach((item) => allDates.add(item.date));
      diaryData.forEach((item) => allDates.add(item.date));
      riskData.forEach((item) => allDates.add(item.date));

      const sortedDates = Array.from(allDates).sort();
      console.log("综合得分计算日期范围:", sortedDates);

      // 为每个日期计算综合得分
      this.combinedScoreData = sortedDates.map((date) => {
        const moodItem = moodData.find((item) => item.date === date);
        const diaryItem = diaryData.find((item) => item.date === date);
        const riskItem = riskData.find((item) => item.date === date);

        const scores = [];
        const weights = [];

        // 心情晴雨表权重：30%
        if (
          moodItem &&
          moodItem.value !== null &&
          moodItem.value !== undefined
        ) {
          scores.push(moodItem.value);
          weights.push(0.3);
        }

        // 碎碎念情感权重：30%
        if (
          diaryItem &&
          diaryItem.value !== null &&
          diaryItem.value !== undefined
        ) {
          scores.push(diaryItem.value);
          weights.push(0.3);
        }

        // 心理状态权重：40% (心理状态相对重要一些)
        if (
          riskItem &&
          riskItem.value !== null &&
          riskItem.value !== undefined
        ) {
          scores.push(riskItem.value);
          weights.push(0.4);
        }

        // 计算加权平均
        let combinedScore;
        if (scores.length === 0) {
          combinedScore = 3; // 默认中性值
        } else {
          // 重新标准化权重
          const totalWeight = weights.reduce((sum, w) => sum + w, 0);
          const normalizedWeights = weights.map((w) => w / totalWeight);

          combinedScore = scores.reduce((sum, score, index) => {
            return sum + score * normalizedWeights[index];
          }, 0);
        }

        console.log(
          `${date}: 心情${moodItem?.value || "N/A"}, 情感${
            diaryItem?.value || "N/A"
          }, 心理${riskItem?.value || "N/A"} -> 综合${combinedScore.toFixed(2)}`
        );

        return {
          date,
          value: Math.round(combinedScore * 100) / 100, // 保留2位小数
          source: "combined",
        };
      });

      console.log(
        "综合得分计算完成，共",
        this.combinedScoreData.length,
        "个数据点"
      );
    },

    getCurrentPeriodLabel() {
      const period = this.periods.find((p) => p.value === this.currentPeriod);
      return period ? period.label : "";
    },

    getPointX(index) {
      let totalLength;
      if (this.chartMode === "combined") {
        totalLength = this.combinedScoreData.length;
      } else {
        const activeSource = this.activeSources[0];
        totalLength = this.chartDataSets[activeSource]?.length || 0;
      }

      if (totalLength <= 1) return 50;
      return (index / (totalLength - 1)) * 100;
    },

    getPointY(score) {
      return ((score - 1) / 4) * 100;
    },

    getVisibleXLabels() {
      let allDates = [];

      if (this.chartMode === "combined") {
        // 综合模式使用综合得分数据的日期
        allDates = this.combinedScoreData.map((item) => item.date);
      } else {
        // 单项模式获取激活数据源的日期
        this.activeSources.forEach((sourceValue) => {
          const data = this.chartDataSets[sourceValue] || [];
          allDates = allDates.concat(data.map((item) => item.date));
        });
      }

      // 去重并排序
      const uniqueDates = [...new Set(allDates)].sort();

      if (uniqueDates.length === 0) return [];

      if (uniqueDates.length <= 7) {
        return uniqueDates.map((date, index) => ({
          index,
          label: this.formatTimeLabel(date),
        }));
      }

      const maxLabels = 7;
      const labels = [];
      const step = Math.floor((uniqueDates.length - 1) / (maxLabels - 1));

      for (let i = 0; i < maxLabels - 1; i++) {
        const index = i * step;
        labels.push({
          index,
          label: this.formatTimeLabel(uniqueDates[index]),
        });
      }

      const lastIndex = uniqueDates.length - 1;
      if (labels.findIndex((l) => l.index === lastIndex) === -1) {
        labels.push({
          index: lastIndex,
          label: this.formatTimeLabel(uniqueDates[lastIndex]),
        });
      }

      return labels;
    },

    formatTimeLabel(dateStr) {
      if (!dateStr) return "";

      // 支持不同的日期格式，提取日期部分
      if (dateStr.includes(" ")) {
        dateStr = dateStr.split(" ")[0];
      }

      // 处理完整日期格式 (YYYY-MM-DD)
      if (dateStr.length >= 10) {
        const parts = dateStr.split("-");
        if (parts.length >= 3) {
          const month = parseInt(parts[1]);
          const day = parseInt(parts[2]);
          return `${month}/${day}`; // 简化为 "M/D" 格式
        }
        return dateStr.substring(5); // 降级为 "MM-DD"
      }

      // 处理其他格式
      if (dateStr.includes("-") && dateStr.length >= 5) {
        return dateStr; // "MM-DD" 保持原样
      }

      return dateStr;
    },

    // 检查是否需要刷新日记缓存
    shouldRefreshDiaryCache() {
      const cacheTimeout = 5 * 60 * 1000; // 5分钟
      return (
        !this.diaryLastFetchTime ||
        Date.now() - this.diaryLastFetchTime > cacheTimeout
      );
    },

    // 检查是否需要刷新风险评估缓存
    shouldRefreshRiskCache() {
      const cacheTimeout = 5 * 60 * 1000; // 5分钟
      return (
        !this.riskLastFetchTime ||
        Date.now() - this.riskLastFetchTime > cacheTimeout
      );
    },
  },
};
</script>

<style scoped>
.emotional-trend-chart {
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
}

.chart-header {
  margin-bottom: 30rpx;
}

.chart-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.chart-controls {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

/* 数据源选择器 */
.data-source-selector {
  width: 100%;
}

.source-scroll {
  width: 100%;
}

.source-list {
  display: flex;
  gap: 12rpx;
  padding: 8rpx 0;
}

.source-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16rpx 20rpx;
  background-color: #f5f5f5;
  border-radius: 12rpx;
  min-width: 100rpx;
  transition: all 0.3s ease;
}

.source-item.active {
  background-color: #e3f2fd;
  border: 2rpx solid #2196f3;
}

.source-item.disabled {
  opacity: 0.5;
  background-color: #f0f0f0;
}

.source-icon {
  font-size: 24rpx;
  margin-bottom: 8rpx;
}

.source-text {
  font-size: 22rpx;
  color: #666;
  text-align: center;
  white-space: nowrap;
}

.source-item.active .source-text {
  color: #2196f3;
  font-weight: bold;
}

/* 综合模式信息 */
.combined-mode-info {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20rpx;
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  border-radius: 12rpx;
  margin: 10rpx 0;
}

.info-text {
  color: white;
  font-size: 28rpx;
  font-weight: 500;
}

/* 图表模式切换 */
.chart-mode-toggle {
  display: flex;
  background-color: #f5f5f5;
  border-radius: 10rpx;
  padding: 4rpx;
  align-self: flex-start;
}

.mode-btn {
  padding: 16rpx 32rpx;
  border-radius: 8rpx;
  transition: all 0.3s ease;
}

.mode-btn.active {
  background-color: #007aff;
}

.mode-text {
  font-size: 26rpx;
  color: #666;
}

.mode-btn.active .mode-text {
  color: white;
  font-weight: bold;
}

.enhanced-chart {
  display: flex;
  height: 500rpx;
  position: relative;
}

.y-axis {
  width: 80rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20rpx 0;
}

.y-label {
  font-size: 24rpx;
  color: #999;
  text-align: center;
}

.chart-content {
  flex: 1;
  position: relative;
  padding: 20rpx 0;
}

.chart-canvas {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.x-axis {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -20rpx;
  height: 40rpx;
}

.x-label {
  font-size: 24rpx;
  color: #999;
  position: absolute;
  transform: translateX(-50%);
  white-space: nowrap;
}

.empty-chart {
  height: 500rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #999;
}

.empty-desc {
  font-size: 26rpx;
  color: #ccc;
}

.empty-tips {
  margin-top: 30rpx;
  padding: 20rpx;
  background-color: #f8f9fa;
  border-radius: 12rpx;
  border: 1px solid #e9ecef;
}

.tip-text {
  display: block;
  font-size: 24rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 8rpx;
}

/* 数据提示框 */
.data-tooltip {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 12rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  pointer-events: none;
  z-index: 10;
  min-width: 120rpx;
}

.tooltip-date {
  font-weight: bold;
  margin-bottom: 8rpx;
  text-align: center;
  display: block;
}

.tooltip-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 4rpx;
}

.tooltip-color {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
}

.tooltip-text {
  font-size: 20rpx;
  white-space: nowrap;
}

.stats-container {
  margin-top: 40rpx;
}

.stats-card {
  width: 100%;
}

.stats-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 30rpx;
}

.stats-content {
  display: flex;
  justify-content: space-between;
}

.stats-item {
  text-align: center;
  flex: 1;
}

.stats-label {
  font-size: 28rpx;
  color: #999;
  display: block;
  margin-bottom: 10rpx;
}

.stats-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #007aff;
}

/* 加载状态样式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  border-radius: 20rpx;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  font-size: 48rpx;
  animation: spin 1s linear infinite;
  display: block;
  margin-bottom: 20rpx;
}

.loading-text {
  font-size: 28rpx;
  color: #666;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 数据源项加载状态 */
.source-item.loading {
  opacity: 0.7;
}

.source-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.spinner {
  font-size: 24rpx;
  animation: spin 1s linear infinite;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40rpx;
  height: 40rpx;
}
</style>
