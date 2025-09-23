<template>
  <view class="tool-container">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="nav-bar">
        <view class="nav-left" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="nav-title">{{ toolData.name }}</text>
        <view class="nav-right">
          <view
            class="collect-btn"
            :class="{ collected: isCollected }"
            @click="toggleCollect"
          >
            <text class="collect-icon">{{ isCollected ? "❤️" : "🤍" }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 工具图标和介绍 -->
    <view class="tool-intro">
      <view class="tool-icon-wrapper">
        <text class="tool-icon">{{ toolData.icon }}</text>
      </view>
      <text class="tool-name">{{ toolData.name }}</text>
      <text class="tool-description">{{ toolData.description }}</text>
      <view class="tool-meta">
        <view class="meta-item">
          <text class="meta-label">难度</text>
          <view class="difficulty-stars">
            <text
              v-for="i in 5"
              :key="i"
              class="star"
              :class="{ active: i <= toolData.difficulty }"
            >
              ★
            </text>
          </view>
        </view>
        <view class="meta-item">
          <text class="meta-label">时长</text>
          <text class="meta-value">{{ toolData.duration }}</text>
        </view>
        <view class="meta-item">
          <text class="meta-label">类型</text>
          <text class="meta-tag">{{ toolData.category }}</text>
        </view>
      </view>
    </view>

    <!-- 工具内容 -->
    <view class="tool-content">
      <!-- 概述 -->
      <view class="content-section">
        <view class="section-header">
          <text class="section-icon">📋</text>
          <text class="section-title">工具概述</text>
        </view>
        <view class="section-content">
          <text class="overview-text">{{ toolData.overview }}</text>
        </view>
      </view>

      <!-- 适用情况 -->
      <view class="content-section">
        <view class="section-header">
          <text class="section-icon">🎯</text>
          <text class="section-title">适用情况</text>
        </view>
        <view class="section-content">
          <view
            v-for="situation in toolData.situations"
            :key="situation"
            class="situation-item"
          >
            <text class="bullet">•</text>
            <text class="situation-text">{{ situation }}</text>
          </view>
        </view>
      </view>

      <!-- 使用步骤 -->
      <view class="content-section">
        <view class="section-header">
          <text class="section-icon">📝</text>
          <text class="section-title">使用步骤</text>
        </view>
        <view class="section-content">
          <view
            v-for="(step, index) in toolData.steps"
            :key="index"
            class="step-item"
          >
            <view class="step-number">{{ index + 1 }}</view>
            <view class="step-content">
              <text class="step-title">{{ step.title }}</text>
              <text class="step-description">{{ step.description }}</text>
              <view v-if="step.tips" class="step-tips">
                <text class="tips-label">💡 小贴士：</text>
                <text class="tips-text">{{ step.tips }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 注意事项 -->
      <view class="content-section">
        <view class="section-header">
          <text class="section-icon">⚠️</text>
          <text class="section-title">注意事项</text>
        </view>
        <view class="section-content">
          <view
            v-for="notice in toolData.notices"
            :key="notice"
            class="notice-item"
          >
            <text class="notice-icon">⚠️</text>
            <text class="notice-text">{{ notice }}</text>
          </view>
        </view>
      </view>

      <!-- 进阶技巧 -->
      <view v-if="toolData.advancedTips" class="content-section">
        <view class="section-header">
          <text class="section-icon">🚀</text>
          <text class="section-title">进阶技巧</text>
        </view>
        <view class="section-content">
          <view
            v-for="tip in toolData.advancedTips"
            :key="tip"
            class="advanced-tip"
          >
            <text class="tip-text">{{ tip }}</text>
          </view>
        </view>
      </view>

      <!-- 相关资源 -->
      <view v-if="toolData.resources" class="content-section">
        <view class="section-header">
          <text class="section-icon">📚</text>
          <text class="section-title">相关资源</text>
        </view>
        <view class="section-content">
          <view
            v-for="resource in toolData.resources"
            :key="resource.id"
            class="resource-item"
            @click="viewResource(resource)"
          >
            <text class="resource-title">{{ resource.title }}</text>
            <text class="resource-type">{{ resource.type }}</text>
            <text class="resource-arrow">→</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部操作按钮 -->
    <view class="bottom-actions">
      <view class="action-btn primary full-width" @click="startPractice">
        <text class="btn-icon">🎯</text>
        <text class="btn-text">开始使用</text>
      </view>
    </view>

    <!-- 收藏成功提示 -->
    <view
      v-if="showCollectTip"
      class="collect-tip"
      :class="{ show: showCollectTip }"
    >
      <text class="tip-text">{{ isCollected ? "已收藏" : "取消收藏" }}</text>
    </view>
    
    <!-- 回到顶部组件 -->
    <BackToTop 
      ref="backToTop"
      :bottom="150"
      @start-scroll-listener="startScrollListener"
      @remove-scroll-listener="removeScrollListener"
    />
  </view>
</template>

<script>
import BackToTop from '../../components/BackToTop.vue'
export default {
  components: {
    BackToTop
  },
  data() {
    return {
      toolId: null,
      toolData: {},
      isCollected: false,
      showCollectTip: false,

      // 默认工具数据模板
      defaultToolsData: {
        1: {
          id: 1,
          name: "深呼吸练习",
          icon: "🫁",
          description: "通过有意识的呼吸调节来缓解焦虑和压力",
          category: "放松技巧",
          difficulty: 2,
          duration: "5-10分钟",
          overview:
            "深呼吸练习是一种简单而有效的放松技巧，通过调节呼吸节奏来激活身体的放松反应，缓解焦虑、紧张和压力。这种技巧可以随时随地使用，无需任何设备或特殊环境。",
          situations: [
            "感到焦虑或紧张时",
            "压力过大需要快速缓解时",
            "失眠或睡眠困难时",
            "愤怒或情绪激动时",
            "准备重要活动前需要放松时",
          ],
          steps: [
            {
              title: "找到舒适位置",
              description:
                "选择一个安静的地方，坐在椅子上或躺下，保持脊背挺直，双肩放松。",
              tips: "如果在公共场所，也可以站立进行，重点是保持身体放松。",
            },
            {
              title: "调整呼吸节奏",
              description:
                "缓慢地用鼻子吸气，让空气填满腹部而不是胸部，吸气4秒钟。",
              tips: "可以将手放在腹部感受呼吸的深度，确保腹部在吸气时向外扩张。",
            },
            {
              title: "屏住呼吸",
              description: "轻轻屏住呼吸4秒钟，不要紧张或用力。",
              tips: "如果感到不适，可以缩短屏气时间或跳过这一步。",
            },
            {
              title: "缓慢呼气",
              description: "通过嘴巴或鼻子慢慢呼气8秒钟，让身体完全放松。",
              tips: '呼气时可以轻轻发出"呼"的声音，这有助于更好地放松。',
            },
            {
              title: "重复练习",
              description: "重复上述步骤5-10次，或直到感到放松为止。",
              tips: "初学者建议从3-5次开始，随着练习增加次数。",
            },
          ],
          notices: [
            "如果感到头晕，请立即停止练习并正常呼吸",
            "患有呼吸系统疾病者请咨询医生后使用",
            "不要过度用力或强迫呼吸节奏",
            "在安全的环境下练习，避免在驾驶等需要注意力集中的活动中使用",
          ],
          advancedTips: [
            "可以配合想象技巧，在吸气时想象正能量进入身体，呼气时想象压力离开身体",
            "结合渐进式肌肉放松，在呼气时有意识地放松身体各个部位",
            "建立日常练习习惯，每天定时进行5-10分钟的呼吸练习",
            "可以使用呼吸练习APP或音乐来辅助练习",
          ],
          resources: [
            {
              id: 1,
              title: "呼吸练习音频指导",
              type: "音频资源",
            },
            {
              id: 2,
              title: "冥想与呼吸的科学原理",
              type: "科普文章",
            },
          ],
        },
        2: {
          id: 2,
          name: "情绪记录",
          icon: "📝",
          description: "记录和追踪情绪变化，提高情绪觉察能力",
          category: "自我觉察",
          difficulty: 1,
          duration: "每日5分钟",
          overview:
            "情绪记录是一种系统性地记录和观察自己情绪变化的工具，通过定期记录情绪状态、触发因素和应对方式，帮助提高情绪觉察能力，识别情绪模式，并制定更有效的情绪管理策略。",
          situations: [
            "情绪波动较大，想了解自己的情绪模式",
            "经常感到情绪困扰，但不知道原因",
            "想要提高情绪管理能力",
            "正在接受心理治疗，需要记录情绪变化",
            "想要培养情绪觉察的习惯",
          ],
          steps: [
            {
              title: "选择记录方式",
              description: "可以使用手机应用、纸质日记或电子文档来记录情绪。",
              tips: "选择自己最方便和习惯的方式，确保能够坚持记录。",
            },
            {
              title: "设定记录时间",
              description:
                "每天固定2-3个时间点进行情绪记录，如早晨、中午和晚上。",
              tips: "可以设置手机提醒，帮助建立记录习惯。",
            },
            {
              title: "记录基本信息",
              description: "记录日期、时间和当前所处的环境或活动。",
            },
            {
              title: "识别情绪状态",
              description:
                "用1-10分来评估当前的情绪强度，并用词语描述具体情绪（如焦虑、愤怒、快乐等）。",
              tips: "可以使用情绪轮盘或情绪词汇表来帮助更准确地识别情绪。",
            },
            {
              title: "分析触发因素",
              description: "记录可能引起这种情绪的事件、想法或身体感受。",
              tips: "即使觉得没有明显原因，也可以记录当时的想法或身体状态。",
            },
            {
              title: "记录应对方式",
              description: "记录自己是如何应对这种情绪的，效果如何。",
            },
            {
              title: "定期回顾分析",
              description: "每周或每月回顾记录，寻找情绪模式和有效的应对策略。",
              tips: "可以制作简单的图表来可视化情绪变化趋势。",
            },
          ],
          notices: [
            '记录应该诚实客观，不要因为追求"积极"而掩饰负面情绪',
            "如果发现记录过程本身引起焦虑，可以简化记录内容",
            "记录是为了了解自己，不是为了判断或批评自己",
            "如果发现严重的情绪问题模式，建议寻求专业帮助",
          ],
          advancedTips: [
            "可以加入身体感受的记录，如头痛、肌肉紧张等",
            "记录睡眠、饮食、运动等生活因素与情绪的关系",
            "使用颜色编码或符号来快速标记不同类型的情绪",
            "建立个人的情绪应对策略库，记录哪些方法最有效",
          ],
        },
        3: {
          id: 3,
          name: "正念冥想",
          icon: "🧘",
          description: "通过专注当下来培养内心平静和觉察力",
          category: "冥想练习",
          difficulty: 3,
          duration: "10-30分钟",
          overview:
            "正念冥想是一种古老而科学的心理训练方法，通过专注于当下的体验，培养对思想、情绪和身体感受的觉察力。定期练习可以减少焦虑、提高专注力、改善情绪调节能力，并增强整体的心理健康。",
          situations: [
            "压力过大需要心理放松时",
            "注意力难以集中时",
            "经常陷入负面思维循环时",
            "想要提高情绪稳定性时",
            "寻求内心平静和自我成长时",
          ],
          steps: [
            {
              title: "准备环境",
              description:
                "选择一个安静、不被打扰的地方，关闭电子设备或调至静音。",
              tips: "可以播放轻柔的背景音乐或自然声音，但不是必需的。",
            },
            {
              title: "调整姿势",
              description:
                "舒适地坐在椅子上或盘腿坐在垫子上，保持脊背挺直但不僵硬。",
              tips: "如果坐着不舒服，也可以选择站立或行走冥想。",
            },
            {
              title: "开始专注呼吸",
              description:
                "闭上眼睛，将注意力放在自然的呼吸上，感受空气进出鼻腔的感觉。",
              tips: "不要试图改变呼吸，只是观察它本来的样子。",
            },
            {
              title: "觉察思维游移",
              description:
                "当发现思维游移到其他地方时，温和地将注意力重新拉回到呼吸上。",
              tips: "思维游移是正常的，不要批判自己，只需要重新开始专注即可。",
            },
            {
              title: "扩大觉察范围",
              description:
                "随着练习深入，可以将觉察扩展到身体感受、声音或整体的存在感。",
              tips: "保持开放和好奇的态度，观察当下的所有体验。",
            },
            {
              title: "温和结束",
              description:
                "练习结束时，慢慢睁开眼睛，活动手指和脚趾，然后起身。",
              tips: "可以花几分钟记录练习中的体验或感受。",
            },
          ],
          notices: [
            "如果感到不适或恐慌，请立即停止练习",
            "初学者建议从5-10分钟开始，逐渐增加时间",
            "不要期望立即看到效果，冥想需要持续练习",
            "如果有严重的心理健康问题，请在专业指导下练习",
          ],
          advancedTips: [
            "可以尝试不同类型的冥想，如身体扫描、慈悲冥想等",
            "建立每日冥想习惯，最好在同一时间同一地点练习",
            "参加冥想小组或使用冥想APP来获得指导和支持",
            "将正念的觉察带到日常活动中，如正念进食、正念行走",
          ],
        },
        4: {
          id: 4,
          name: "积极思维训练",
          icon: "💭",
          description: "识别和改变负面思维模式，培养积极心态",
          category: "认知重构",
          difficulty: 3,
          duration: "15-20分钟",
          overview:
            "积极思维训练是一种认知行为技巧，帮助识别和挑战自动化的负面思维模式，培养更加平衡和现实的思维方式。这种技巧基于认知行为疗法的原理，通过改变思维来改善情绪和行为。",
          situations: [
            "经常陷入负面思维循环时",
            "自我批评过于严厉时",
            "对未来过度担忧时",
            "自信心不足需要提升时",
            "想要培养更积极的人生态度时",
          ],
          steps: [
            {
              title: "觉察负面思维",
              description:
                "注意并记录自己的自动化思维，特别是那些引起负面情绪的想法。",
              tips: "可以设定提醒，定期检查自己的思维状态。",
            },
            {
              title: "识别思维陷阱",
              description:
                "学会识别常见的认知偏差，如全或无思维、灾难化思维、心理过滤等。",
              tips: "了解不同类型的思维陷阱有助于更准确地识别自己的模式。",
            },
            {
              title: "挑战负面思维",
              description:
                "对负面思维提出质疑：这个想法是否真实？是否有其他可能的解释？",
              tips: "可以问自己：如果朋友有这样的想法，我会如何建议他们？",
            },
            {
              title: "寻找证据",
              description: "收集支持和反对这个负面想法的证据，进行客观分析。",
              tips: "写下具体的事实和例子，而不是主观感受。",
            },
            {
              title: "重新构建思维",
              description:
                "基于证据，创建更加平衡和现实的想法来替代原来的负面思维。",
              tips: "新的想法应该是真实的、有帮助的，而不是盲目乐观的。",
            },
            {
              title: "练习新思维",
              description:
                "在日常生活中主动使用新的思维模式，并观察情绪和行为的变化。",
              tips: "需要时间和重复练习才能形成新的思维习惯。",
            },
          ],
          notices: [
            "积极思维不等于否认现实或压制负面情绪",
            "改变思维模式需要时间，不要对自己过于苛刻",
            "如果负面思维严重影响生活，建议寻求专业帮助",
            "要区分合理的担忧和过度的焦虑思维",
          ],
          advancedTips: [
            '建立"思维记录表"来系统地练习认知重构',
            "学习感恩练习，每天记录3件值得感恩的事情",
            "培养成长型思维，将挑战视为学习和成长的机会",
            "使用肯定语句来强化积极的自我对话",
          ],
        },
        5: {
          id: 5,
          name: "睡眠改善指导",
          icon: "😴",
          description: "改善睡眠质量，建立健康的睡眠习惯",
          category: "生活调节",
          difficulty: 2,
          duration: "持续实践",
          overview:
            "良好的睡眠对心理健康至关重要。睡眠改善指导通过建立健康的睡眠习惯、优化睡眠环境和学习放松技巧，帮助改善睡眠质量，从而提升整体的心理和身体健康。",
          situations: [
            "难以入睡或频繁醒来时",
            "睡眠质量不佳影响日常生活时",
            "因压力或焦虑导致失眠时",
            "作息不规律需要调整时",
            "想要优化睡眠质量时",
          ],
          steps: [
            {
              title: "建立规律作息",
              description: "每天在相同时间上床睡觉和起床，包括周末。",
              tips: "即使睡得不好，也要在固定时间起床，这有助于调节生物钟。",
            },
            {
              title: "优化睡眠环境",
              description: "保持卧室安静、黑暗、凉爽，使用舒适的床具。",
              tips: "可以使用遮光窗帘、耳塞或白噪音机来改善睡眠环境。",
            },
            {
              title: "建立睡前仪式",
              description: "睡前1小时进行放松活动，如读书、听音乐或洗澡。",
              tips: "避免刺激性活动，如激烈运动、工作或使用电子设备。",
            },
            {
              title: "控制咖啡因摄入",
              description: "下午2点后避免摄入咖啡因，包括咖啡、茶和巧克力。",
              tips: "咖啡因的影响可以持续6-8小时，所以要提前停止摄入。",
            },
            {
              title: "管理卧室使用",
              description:
                "只在卧室进行睡眠和亲密活动，不要在床上工作或看电视。",
              tips: "如果20分钟内无法入睡，可以起床做安静的活动，直到有睡意再回到床上。",
            },
            {
              title: "练习放松技巧",
              description: "使用深呼吸、渐进式肌肉放松或冥想来帮助入睡。",
              tips: '可以尝试"4-7-8呼吸法"：吸气4秒，屏气7秒，呼气8秒。',
            },
          ],
          notices: [
            "如果睡眠问题持续超过一个月，请咨询医生",
            "避免使用酒精作为助眠工具，它会影响睡眠质量",
            "白天适量运动有助于睡眠，但睡前4小时内避免激烈运动",
            "如果有睡眠呼吸暂停等疾病，需要专业医疗处理",
          ],
          advancedTips: [
            "使用睡眠日记记录睡眠模式，找出影响睡眠的因素",
            "尝试冥想APP或睡眠故事来帮助放松",
            '学习"睡眠限制疗法"来提高睡眠效率',
            "考虑使用蓝光过滤眼镜在晚上使用电子设备时",
          ],
        },
        6: {
          id: 6,
          name: "压力评估测试",
          icon: "📊",
          description: "科学评估当前压力水平，了解压力来源",
          category: "自我评估",
          difficulty: 1,
          duration: "10-15分钟",
          overview:
            "压力评估测试通过科学的问卷和量表，帮助客观地评估当前的压力水平，识别主要的压力来源，并提供相应的应对建议。定期进行压力评估有助于及时发现和管理压力问题。",
          situations: [
            "感到压力大但不确定具体水平时",
            "想要了解压力的主要来源时",
            "需要客观评估自己的心理状态时",
            "定期检查自己的心理健康状况时",
            "为制定压力管理计划做准备时",
          ],
          steps: [
            {
              title: "选择合适时间",
              description:
                "在相对安静、不被打扰的时间进行测试，确保能够专心回答问题。",
              tips: "避免在特别紧张或放松的时候测试，选择平常的状态进行评估。",
            },
            {
              title: "诚实回答问题",
              description:
                '根据最近一周的真实感受回答问题，不要想着"应该"如何回答。',
              tips: "没有标准答案，诚实回答才能得到准确的评估结果。",
            },
            {
              title: "评估生理症状",
              description:
                "记录与压力相关的身体症状，如头痛、肌肉紧张、睡眠问题等。",
            },
            {
              title: "分析情绪状态",
              description: "评估焦虑、抑郁、易怒等情绪的频率和强度。",
            },
            {
              title: "识别行为变化",
              description:
                "注意是否有食欲变化、社交退缩、工作效率下降等行为改变。",
            },
            {
              title: "分析压力源",
              description:
                "识别工作、人际关系、健康、财务等各个领域的压力来源。",
            },
            {
              title: "查看结果和建议",
              description:
                "根据测试结果了解自己的压力水平，并查看相应的应对建议。",
              tips: "测试结果仅供参考，如有严重问题应咨询专业人士。",
            },
          ],
          notices: [
            "测试结果仅供参考，不能替代专业的心理评估",
            "如果测试显示高压力水平，建议寻求专业帮助",
            "定期重新测试可以跟踪压力水平的变化",
            "不要因为测试结果而给自己贴标签或过度担忧",
          ],
          advancedTips: [
            "可以将测试结果记录下来，跟踪长期的变化趋势",
            "结合其他心理健康工具，如情绪记录，来全面了解自己",
            "根据测试结果制定个性化的压力管理计划",
            "定期回顾测试结果，调整个人的压力管理策略",
          ],
        },
      },
    };
  },

  onLoad(options) {
    this.toolId = options.id || "1";
    this.loadToolData();
    this.checkCollectStatus();
  },

  onUnload() {
    this.removeScrollListener();
  },

  methods: {
    loadToolData() {
      // 从传入的参数或默认数据中获取工具信息
      this.toolData =
        this.defaultToolsData[this.toolId] || this.defaultToolsData["1"];
    },

    checkCollectStatus() {
      const collected = uni.getStorageSync("collectedTools") || [];
      this.isCollected = collected.includes(this.toolId);
    },

    goBack() {
      uni.navigateBack();
    },

    toggleCollect() {
      let collected = uni.getStorageSync("collectedTools") || [];

      if (this.isCollected) {
        // 取消收藏
        collected = collected.filter((id) => id !== this.toolId);
        this.isCollected = false;
      } else {
        // 添加收藏
        collected.push(this.toolId);
        this.isCollected = true;
      }

      uni.setStorageSync("collectedTools", collected);
      this.showCollectTip = true;

      setTimeout(() => {
        this.showCollectTip = false;
      }, 2000);
    },

    startPractice() {
      // 根据不同工具跳转到相应的实践页面
      let route = null;
      if (this.toolId == 2) {
        // 情绪记录跳转到碎碎念
        route = "/pages/diary/diary";
      } else {
        const practiceRoutes = {
          1: "/pages/tools/breathing-practice",
          3: "/pages/tools/meditation-practice",
          4: "/pages/tools/positive-thinking-practice",
          5: "/pages/tools/sleep-guide",
          6: "/pages/tools/stress-assessment",
        };
        route = practiceRoutes[this.toolId];
      }
      if (route) {
        uni.navigateTo({
          url: `${route}?toolId=${this.toolId}`,
        });
      } else {
        uni.showModal({
          title: "开始使用",
          content:
            "根据上述步骤开始练习这个工具。建议将页面保存或截图以便随时查看指导。",
          showCancel: false,
          confirmText: "知道了",
        });
      }
    },

    viewResource(resource) {
      uni.showModal({
        title: resource.title,
        content: "该资源正在整理中，敬请期待。",
        showCancel: false,
        confirmText: "知道了",
      });
    },

    // 滚动监听相关方法
    startScrollListener() {
      // H5环境使用window.addEventListener
      if (typeof window !== 'undefined') {
        this.handleScroll = () => {
          const scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
          if (this.$refs.backToTop) {
            this.$refs.backToTop.updateVisibility(scrollTop);
          }
        };
        window.addEventListener('scroll', this.handleScroll);
      } else {
        // 小程序环境使用uni.onPageScroll
        uni.onPageScroll((res) => {
          if (this.$refs.backToTop) {
            this.$refs.backToTop.updateVisibility(res.scrollTop);
          }
        });
      }
    },

    removeScrollListener() {
      if (typeof window !== 'undefined' && this.handleScroll) {
        window.removeEventListener('scroll', this.handleScroll);
      } else if (typeof uni !== 'undefined' && uni.offPageScroll) {
        uni.offPageScroll();
      }
    },
  },
};
</script>

<style scoped>
.tool-container {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

/* 顶部导航 */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-top: env(safe-area-inset-top);
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 40rpx;
  height: 88rpx;
}

.nav-left,
.nav-right {
  width: 80rpx;
  display: flex;
  justify-content: center;
}

.back-icon {
  font-size: 36rpx;
  color: white;
  font-weight: bold;
}

.nav-title {
  font-size: 36rpx;
  font-weight: bold;
  color: white;
  text-align: center;
  flex: 1;
}

.collect-btn {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.collect-btn.collected {
  background-color: rgba(255, 255, 255, 0.3);
}

.collect-icon {
  font-size: 28rpx;
}

/* 工具介绍 */
.tool-intro {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx;
  text-align: center;
  color: white;
}

.tool-icon-wrapper {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24rpx;
}

.tool-icon {
  font-size: 64rpx;
}

.tool-name {
  font-size: 42rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
  display: block;
}

.tool-description {
  font-size: 28rpx;
  opacity: 0.9;
  line-height: 1.6;
  margin-bottom: 32rpx;
  display: block;
}

.tool-meta {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.meta-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.meta-label {
  font-size: 22rpx;
  opacity: 0.8;
}

.meta-value,
.meta-tag {
  font-size: 24rpx;
  font-weight: bold;
}

.meta-tag {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
}

.difficulty-stars {
  display: flex;
  gap: 4rpx;
}

.star {
  font-size: 20rpx;
  color: rgba(255, 255, 255, 0.4);
}

.star.active {
  color: #ffd700;
}

/* 工具内容 */
.tool-content {
  padding: 40rpx;
}

.content-section {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
  padding-bottom: 16rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.section-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.section-content {
  line-height: 1.8;
}

/* 概述文本 */
.overview-text {
  font-size: 28rpx;
  color: #555;
  line-height: 1.8;
}

/* 适用情况 */
.situation-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.bullet {
  font-size: 24rpx;
  color: #667eea;
  margin-right: 12rpx;
  margin-top: 4rpx;
}

.situation-text {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
  flex: 1;
}

/* 使用步骤 */
.step-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 32rpx;
  padding-bottom: 24rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.step-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.step-number {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 24rpx;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
}

.step-description {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
  margin-bottom: 12rpx;
  display: block;
}

.step-tips {
  background-color: #f8f9fa;
  padding: 16rpx;
  border-radius: 8rpx;
  border-left: 4rpx solid #667eea;
}

.tips-label {
  font-size: 24rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 4rpx;
  display: block;
}

.tips-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.6;
}

/* 注意事项 */
.notice-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16rpx;
  padding: 16rpx;
  background-color: #fff7f0;
  border-radius: 8rpx;
  border-left: 4rpx solid #fa8c16;
}

.notice-icon {
  font-size: 24rpx;
  margin-right: 12rpx;
  margin-top: 2rpx;
}

.notice-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  flex: 1;
}

/* 进阶技巧 */
.advanced-tip {
  background-color: #f6ffed;
  padding: 16rpx;
  border-radius: 8rpx;
  margin-bottom: 16rpx;
  border-left: 4rpx solid #52c41a;
}

.tip-text {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
}

/* 相关资源 */
.resource-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx;
  background-color: #f8f9fa;
  border-radius: 8rpx;
  margin-bottom: 12rpx;
  transition: all 0.3s ease;
}

.resource-item:active {
  background-color: #e9ecef;
  transform: translateY(1rpx);
}

.resource-title {
  font-size: 26rpx;
  color: #333;
  font-weight: 500;
  flex: 1;
}

.resource-type {
  font-size: 22rpx;
  color: #667eea;
  background-color: white;
  padding: 6rpx 12rpx;
  border-radius: 12rpx;
  margin-right: 16rpx;
}

.resource-arrow {
  font-size: 24rpx;
  color: #999;
}

/* 底部操作按钮 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 24rpx 40rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  display: flex;
  gap: 20rpx;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.action-btn {
  flex: 1;
  padding: 24rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  font-size: 28rpx;
  font-weight: bold;
  transition: all 0.3s ease;
}

.action-btn.secondary {
  background-color: #f0f0f0;
  color: #666;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.action-btn.full-width {
  width: 100%;
  margin: 0;
}

.action-btn:active {
  transform: scale(0.98);
}

.btn-icon {
  font-size: 24rpx;
}

.btn-text {
  font-size: 28rpx;
}

/* 收藏提示 */
.collect-tip {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 20rpx 32rpx;
  border-radius: 16rpx;
  font-size: 26rpx;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1000;
  pointer-events: none;
}

.collect-tip.show {
  opacity: 1;
}

/* 响应式设计 */
@media (max-width: 480rpx) {
  .tool-meta {
    flex-direction: column;
    gap: 20rpx;
  }

  .meta-item {
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
  }

  .step-item {
    flex-direction: column;
    align-items: stretch;
  }

  .step-number {
    align-self: flex-start;
    margin-bottom: 16rpx;
    margin-right: 0;
  }

  .bottom-actions {
    flex-direction: column;
    gap: 16rpx;
  }
}

/* 动画效果 */
.content-section {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 滚动优化 */
.tool-container {
  scroll-behavior: smooth;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .content-section {
    border: 2rpx solid #333;
  }

  .step-number {
    border: 2rpx solid white;
  }

  .action-btn.primary {
    border: 2rpx solid #333;
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
