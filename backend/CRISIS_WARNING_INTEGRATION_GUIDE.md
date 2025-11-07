# 心灵预警系统集成指南

## 概述

心灵预警系统是一个可复用的组件化危机检测服务，支持悄悄话、日记、聊天等多种场景的心理风险检测。

## 核心功能

1. **模糊匹配检测**：支持同音字、空格变体等模糊匹配
2. **AI 增强分析**：可选的 AI 深度分析，提供专业评估
3. **看板娘气泡提示**：根据风险等级显示温馨提示
4. **高风险记录**：自动记录高风险内容到数据库

## 架构设计

### 后端组件

```
backend/app/
├── services/
│   ├── crisis_warning_service.py          # 核心危机检测服务
│   └── crisis_detector_component.py       # 可复用组件封装
├── api/routes/
│   ├── crisis_detection.py                # 独立检测API
│   └── tree_hole.py                        # 树洞集成示例
└── schemas/
    └── tree_hole.py                        # 响应Schema（含预警信息）
```

### 前端组件

```
frontend/src/
├── components/
│   └── crisis-warning-bubble.vue           # 看板娘气泡组件
└── utils/
    └── api.js                              # API封装
```

## 后端集成步骤

### 1. 在任意路由中集成

```python
from app.services.crisis_detector_component import get_crisis_detector
from app.schemas.tree_hole import CrisisWarningInfo

@router.post("/your-endpoint")
async def your_function(
    data: YourSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 初始化心灵预警信息
    crisis_warning = CrisisWarningInfo()

    try:
        # 获取检测器
        detector = get_crisis_detector(db)

        # 执行风险检测
        crisis_result = await detector.detect_content_risk(
            content=data.content,
            scene="your-scene",  # tree-hole, diary, chat等
            user_id=current_user.user_id,
            enable_ai=True  # 是否启用AI分析
        )

        # 构建响应信息
        crisis_warning = CrisisWarningInfo(
            has_risk=crisis_result.has_risk,
            risk_level=crisis_result.risk_level,
            should_show_bubble=crisis_result.should_show_bubble,
            bubble_message=crisis_result.bubble_message,
            ai_brief_analysis=crisis_result.ai_brief_analysis
        )

    except Exception as e:
        print(f"❌ 心灵预警检测失败: {str(e)}")
        # 不影响主流程

    # ... 你的业务逻辑 ...

    # 在响应中返回预警信息
    return YourResponse(
        # ... 其他字段 ...
        crisis_warning=crisis_warning
    )
```

### 2. 添加响应 Schema

```python
# 在你的schemas文件中
from pydantic import BaseModel
from typing import Optional

class CrisisWarningInfo(BaseModel):
    """心灵预警信息"""
    has_risk: bool = False
    risk_level: str = "low"
    should_show_bubble: bool = False
    bubble_message: Optional[str] = None
    ai_brief_analysis: Optional[str] = None

class YourResponse(BaseModel):
    # ... 其他字段 ...
    crisis_warning: CrisisWarningInfo = CrisisWarningInfo()
```

## 前端集成步骤

### 1. 导入气泡组件

```vue
<template>
  <view>
    <!-- 你的页面内容 -->

    <!-- 心灵预警气泡 -->
    <crisis-warning-bubble
      :show="showCrisisBubble"
      :risk-level="crisisRiskLevel"
      :message="crisisBubbleMessage"
      :ai-analysis="crisisAiAnalysis"
      :mascot-avatar="mascotAvatarUrl"
      @close="handleCloseCrisisBubble"
      @ok="handleCloseCrisisBubble"
      @view-resources="handleViewResources"
    />
  </view>
</template>

<script>
import CrisisWarningBubble from "@/components/crisis-warning-bubble.vue";

export default {
  components: {
    CrisisWarningBubble,
  },

  data() {
    return {
      showCrisisBubble: false,
      crisisRiskLevel: "low",
      crisisBubbleMessage: "",
      crisisAiAnalysis: "",
      mascotAvatarUrl: "/static/images/mascot-default.png",
    };
  },

  methods: {
    async submitContent() {
      const token = storage.getToken();

      try {
        // 提交内容（树洞、日记等）
        const response = await api.createWhisper(token, this.whisperData);

        // 检查是否有心灵预警
        if (
          response.crisis_warning &&
          response.crisis_warning.should_show_bubble
        ) {
          this.showCrisisBubble = true;
          this.crisisRiskLevel = response.crisis_warning.risk_level;
          this.crisisBubbleMessage = response.crisis_warning.bubble_message;
          this.crisisAiAnalysis = response.crisis_warning.ai_brief_analysis;
        }

        // ... 其他处理 ...
      } catch (error) {
        console.error("提交失败:", error);
      }
    },

    handleCloseCrisisBubble() {
      this.showCrisisBubble = false;
    },

    handleViewResources(riskLevel) {
      // 跳转到资源页面或显示资源列表
      console.log("查看资源，风险等级:", riskLevel);
    },
  },
};
</script>
```

### 2. 实时关键词检测（可选）

用于用户输入时的实时提示：

```javascript
methods: {
  async onContentInput(e) {
    const content = e.detail.value;

    // 内容长度达到一定程度才检测
    if (content.length < 10) return;

    const token = storage.getToken();

    try {
      // 快速关键词检测（不使用AI）
      const result = await api.quickCrisisCheck(token, content, 'tree-hole');

      if (result.has_risk) {
        // 显示警告提示
        uni.showToast({
          title: '检测到敏感内容',
          icon: 'none',
          duration: 2000
        });
      }

    } catch (error) {
      console.error('关键词检测失败:', error);
    }
  }
}
```

## API 接口说明

### 1. 完整风险分析

**接口**: `POST /crisis-detection/analyze`

**请求参数**:

```json
{
  "content": "待检测内容",
  "scene": "tree-hole",
  "enable_ai": true
}
```

**响应**:

```json
{
  "has_risk": true,
  "risk_level": "medium",
  "risk_score": 45.0,
  "ai_brief_analysis": "用户表达了一些负面情绪...",
  "should_show_bubble": true,
  "bubble_message": "小念感受到你有些情绪起伏...",
  "detected_keywords": ["孤独", "无助"],
  "recommendations": ["适当宣泄情绪是健康的"]
}
```

### 2. 快速关键词检测

**接口**: `POST /crisis-detection/quick-check`

**请求参数**:

```json
{
  "content": "待检测内容",
  "scene": "tree-hole"
}
```

**响应**:

```json
{
  "has_risk": true,
  "detected_keywords": ["孤独"],
  "fuzzy_matches": ["想 死"],
  "categories": ["孤独", "自伤"],
  "score": 15.0
}
```

## 风险等级说明

| 等级     | 值       | 说明                       | 气泡显示  |
| -------- | -------- | -------------------------- | --------- |
| 低风险   | low      | 无明显风险或轻微负面情绪   | 不显示    |
| 中等风险 | medium   | 有一定负面情绪，需要关注   | 显示      |
| 高风险   | high     | 明显的心理压力或情绪问题   | 显示      |
| 严重风险 | critical | 存在自伤倾向或严重心理危机 | 显示+记录 |

## 配置选项

### 后端配置

在 `crisis_detector_component.py` 中可配置：

1. **气泡消息模板** (`BUBBLE_TEMPLATES`): 不同风险等级的提示语
2. **是否启用 AI**: `enable_ai_analysis` 参数
3. **高风险记录阈值**: 自动记录 HIGH 和 CRITICAL 级别

### 前端配置

气泡组件 Props:

- `show`: 是否显示
- `riskLevel`: 风险等级
- `message`: 气泡消息
- `aiAnalysis`: AI 分析
- `mascotAvatar`: 看板娘头像
- `autoClose`: 自动关闭时间（毫秒）

## 最佳实践

1. **异步非阻塞**: 检测失败不影响主流程
2. **双重检测**: 关键词快速检测 + AI 深度分析
3. **用户体验**: 仅中等及以上风险显示气泡
4. **隐私保护**: 高风险内容记录到数据库，便于后续干预
5. **资源整合**: 高风险提供心理健康资源链接

## 扩展场景

### 日记集成

```python
# backend/app/api/routes/diary.py
from app.services.crisis_detector_component import get_crisis_detector

@router.post("/")
async def create_diary(...):
    detector = get_crisis_detector(db)
    crisis_result = await detector.detect_content_risk(
        content=diary.content,
        scene="diary",
        user_id=current_user.user_id
    )
    # ... 处理结果 ...
```

### 聊天集成

```python
# backend/app/api/routes/ai_dialog.py
from app.services.crisis_detector_component import get_crisis_detector

@router.post("/send")
async def send_message(...):
    detector = get_crisis_detector(db)
    crisis_result = await detector.detect_content_risk(
        content=message.content,
        scene="chat",
        user_id=current_user.user_id
    )
    # ... 处理结果 ...
```

## 故障排查

### 问题 1: AI 分析不返回

**原因**: AI 服务未配置或调用失败
**解决**:

```python
# 设置 enable_ai=False 或检查 ai_api_url 配置
crisis_result = await detector.detect_content_risk(
    content=content,
    enable_ai=False  # 仅使用关键词检测
)
```

### 问题 2: 气泡不显示

**检查清单**:

1. `should_show_bubble` 是否为 true
2. 风险等级是否 >= medium
3. `bubble_message` 是否有内容
4. 前端组件 `show` prop 是否绑定正确

### 问题 3: 模糊匹配不生效

**原因**: 关键词配置问题
**解决**: 检查 `crisis_warning_service.py` 中的 `FUZZY_PATTERNS` 配置

## 更新日志

### v1.0.0 (2025-01-07)

- ✅ 初始版本发布
- ✅ 支持悄悄话场景
- ✅ 模糊匹配检测
- ✅ AI 增强分析
- ✅ 看板娘气泡组件

### 待开发功能

- [ ] 晴雨表连续低分检测
- [ ] 心理健康评估报告生成
- [ ] 危机干预工作流
- [ ] 专业咨询师对接

## 联系支持

如有问题或建议，请联系开发团队。
