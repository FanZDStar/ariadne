# 心理危机预警系统使用指南

## 🎯 系统概述

心理危机预警系统是一个基于AI和关键词检测的智能预警系统，能够：
- 实时监控用户的情绪状态和内容表达
- 检测潜在的心理危机信号
- 提供分级预警和干预建议
- 保护用户隐私的同时确保及时响应

## 🚀 快速开始

### 1. 后端API测试

后端服务已启动，你可以通过以下方式测试API：

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试风险评估（需要登录token）
curl -X POST "http://localhost:8000/api/crisis/assess-risk?days=14" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### 2. 前端组件集成

在需要显示心理健康状态的页面中集成：

```vue
<template>
  <view class="health-monitor">
    <!-- 心理健康评估组件 -->
    <CrisisWarning 
      :auto-assess="true" 
      :show-history="true" 
    />
  </view>
</template>

<script>
import CrisisWarning from '@/components/CrisisWarning.vue'

export default {
  components: {
    CrisisWarning
  }
}
</script>
```

## 📊 功能特性

### 1. 多维度风险评估

- **心情趋势分析**：基于用户情绪日记的历史数据
- **关键词检测**：实时检测危险词汇和表达
- **行为模式识别**：分析用户活动和互动模式
- **AI智能分析**：结合大模型进行深度内容理解

### 2. 分级预警机制

| 风险等级   | 评分范围 | 响应措施           |
| ---------- | -------- | ------------------ |
| 🟢 低风险   | 0-39     | 常规关怀提醒       |
| 🟡 中等风险 | 40-59    | 主动关怀，提供资源 |
| 🟠 高风险   | 60-79    | 专业建议，密切关注 |
| 🔴 紧急风险 | 80-100   | 立即干预，紧急联系 |

### 3. 智能关键词库

系统预置了5大类危机关键词：

- **自伤类**：自杀、自残、轻生等（高权重）
- **绝望类**：绝望、无望、没希望等
- **孤独类**：孤独、孤单、被遗弃等
- **无价值感**：没用、废物、无价值等
- **极端情绪**：崩溃、疯了、受不了等

## 🔧 集成步骤

### 步骤1：在现有页面中添加监控

在用户输入内容的地方（如日记、聊天）添加实时检测：

```javascript
// 在用户输入时进行实时检测
import { CrisisKeywordDetector } from '@/utils/crisisApi.js'

onInput(content) {
  const detection = CrisisKeywordDetector.quickDetect(content)
  
  if (detection.hasCrisis) {
    // 显示温和提醒或求助信息
    this.showCrisisAlert(detection)
  }
}
```

### 步骤2：在个人中心添加健康评估

```vue
<!-- 在个人中心页面 -->
<template>
  <view class="user-center">
    <!-- 其他个人信息 -->
    
    <!-- 心理健康模块 -->
    <view class="health-section">
      <view class="section-title">心理健康</view>
      <CrisisWarning :auto-assess="true" />
    </view>
  </view>
</template>
```

### 步骤3：配置后台监控（可选）

在 `app/main.py` 中启用定时监控：

```python
@app.on_event("startup")
async def startup_event():
    # 启动心理危机监控任务
    asyncio.create_task(crisis_monitor.start_monitoring(check_interval_hours=6))
```

## 🛡️ 隐私和安全

### 1. 数据加密
- 所有敏感预警数据都经过加密存储
- 使用与现有系统一致的加密机制

### 2. 权限控制
- 用户只能访问自己的预警记录
- 管理员可配置系统级别的监控参数

### 3. 用户控制
- 用户可以选择关闭自动监控
- 可以手动删除或标记预警为已解决

## 📱 前端使用示例

### 基础使用

```javascript
import { CrisisAPI } from '@/utils/crisisApi.js'

// 执行风险评估
const assessment = await CrisisAPI.assessRisk(14)
console.log('风险等级:', assessment.risk_level)

// 获取预警记录
const warnings = await CrisisAPI.getWarnings({ unresolvedOnly: true })

// 解决预警
await CrisisAPI.resolveWarning(warningId, '用户反馈已改善')
```

### 实时关键词检测

```javascript
import { CrisisKeywordDetector } from '@/utils/crisisApi.js'

// 检测用户输入
function checkUserInput(text) {
  const result = CrisisKeywordDetector.quickDetect(text)
  
  if (result.hasCrisis) {
    switch (result.riskLevel) {
      case 'critical':
        // 显示紧急求助信息
        showEmergencyHelp()
        break
      case 'high':
        // 显示关怀提醒
        showCareReminder()
        break
      default:
        // 温和提醒
        showGentleReminder()
    }
  }
}
```

## 🔄 API接口详情

### 1. 风险评估接口

```http
POST /api/crisis/assess-risk?days=14
Authorization: Bearer {token}

Response:
{
  "risk_level": "medium",
  "score": 65.0,
  "reasons": ["近14天平均心情偏低", "检测到孤独相关表达"],
  "recommendations": ["建议寻求专业心理咨询", "保持与亲友联系"],
  "assessment_date": "2025-09-04T10:30:00"
}
```

### 2. 预警记录接口

```http
GET /api/crisis/warnings?days=30&unresolved_only=false
Authorization: Bearer {token}

Response:
[
  {
    "warning_id": 1,
    "warning_type": "keyword_alert",
    "risk_level": "high",
    "score": 75.0,
    "title": "HIGH风险预警",
    "description": "检测到自伤相关表达",
    "is_resolved": false,
    "created_at": "2025-09-04T09:15:00"
  }
]
```

### 3. 统计信息接口

```http
GET /api/crisis/statistics?days=30
Authorization: Bearer {token}

Response:
{
  "period_days": 30,
  "total_warnings": 5,
  "unresolved_warnings": 2,
  "risk_level_distribution": {
    "low": 1,
    "medium": 2,
    "high": 2,
    "critical": 0
  },
  "current_risk_level": "medium",
  "current_risk_score": 45.5
}
```

## 🎨 界面自定义

### 自定义风险等级样式

```css
/* 风险等级颜色 */
.risk-low { background: linear-gradient(135deg, #E8F5E8, #C8E6C9); }
.risk-medium { background: linear-gradient(135deg, #FFF3E0, #FFD54F); }
.risk-high { background: linear-gradient(135deg, #FFEBEE, #FFAB91); }
.risk-critical { background: linear-gradient(135deg, #FFEBEE, #E57373); }
```

### 自定义提醒文案

```javascript
const CRISIS_MESSAGES = {
  low: "注意调节情绪，保持积极心态",
  medium: "如有困扰，可以找朋友聊聊",
  high: "建议寻求专业心理支持",
  critical: "请立即联系心理援助热线：400-161-9995"
}
```

## 🔧 配置和调优

### 1. 调整风险阈值

在 `crisis_warning_service.py` 中修改：

```python
# 调整关键词权重
base_scores = {
    "自伤": 40,      # 可根据实际需要调整
    "绝望": 25,
    "孤独": 15,
    "无价值感": 20,
    "极端情绪": 10
}
```

### 2. 添加自定义关键词

```python
# 在 CRISIS_KEYWORDS 中添加新类别
"自定义类别": ["关键词1", "关键词2", "关键词3"]
```

### 3. 配置监控频率

```python
# 在 main.py 中调整检查间隔
crisis_monitor.start_monitoring(check_interval_hours=6)  # 6小时检查一次
```

## 📞 紧急联系资源

系统内置了以下紧急联系方式：

- **国家心理健康热线**：400-161-9995
- **青少年心理健康热线**：12355
- **紧急救援**：110
- **医疗急救**：120

## 🎯 最佳实践

### 1. 渐进式集成
- 先在一个页面测试基础功能
- 逐步扩展到其他页面
- 根据用户反馈调整参数

### 2. 用户体验优化
- 避免过于频繁的预警提醒
- 提供关闭监控的选项
- 使用温和友善的提醒文案

### 3. 响应流程设计
- 制定不同风险等级的应对流程
- 准备专业心理资源的联系方式
- 建立用户反馈和改进机制

## 🐛 故障排除

### 常见问题

1. **API调用失败**
   - 检查token是否有效
   - 确认服务器是否正常运行

2. **关键词检测不准确**
   - 调整关键词权重
   - 添加更多相关词汇

3. **预警过于频繁**
   - 提高风险阈值
   - 调整检查频率

---

🎉 **恭喜！** 心理危机预警系统已成功集成到你的项目中。这个系统将帮助及时发现和响应用户的心理健康需求，为用户提供更好的关怀和支持。
