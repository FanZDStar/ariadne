# AI 对话危机检测集成文档

## 📋 概述

本文档描述了如何在 AI 对话中集成危机检测功能,使用新的模块化危机检测组件。

## 🎯 实现目标

- ✅ 在 AI 对话时自动检测用户消息中的危机信号
- ✅ 支持模糊检测(同音字、空格变体等)
- ✅ 启用 AI 增强分析获取更准确的风险评估
- ✅ 通过看板娘气泡向用户显示温暖的关怀提示
- ✅ 提供专业心理健康资源链接

## 🔧 技术实现

### 后端实现

#### 1. 修改响应模式 (`backend/app/api/routes/ai_dialog.py`)

```python
from app.schemas.tree_hole import CrisisWarningInfo
from app.services.crisis_detector_component import get_crisis_detector

class DialogResponse(BaseModel):
    content: str
    crisis_warning: Optional[CrisisWarningInfo] = Field(default=None, description="危机预警信息")
```

#### 2. 集成危机检测逻辑

在 `ai_dialog()` 函数中:

```python
@router.post("/ai-dialog", response_model=DialogResponse)
async def ai_dialog(data: DialogRequest, request: Request):
    # ... 现有代码 ...

    # 🚨 提取用户最新消息进行危机检测
    user_messages = [msg.content for msg in data.messages if msg.role == "user"]
    latest_user_message = user_messages[-1] if user_messages else ""

    # 初始化危机预警信息(默认安全值)
    crisis_warning = CrisisWarningInfo()

    # 如果有用户消息且提供了用户ID,进行危机检测
    if latest_user_message and data.user_id:
        try:
            logger.info("🚨 开始进行危机检测...")
            from app.database.session import get_db
            db = next(get_db())

            detector = get_crisis_detector(db)
            crisis_result = await detector.detect_content_risk(
                content=latest_user_message,
                scene="chat",
                user_id=data.user_id,
                enable_ai=True  # 启用AI增强分析
            )

            crisis_warning = CrisisWarningInfo(
                should_show_bubble=crisis_result.should_show_bubble,
                bubble_message=crisis_result.bubble_message,
                risk_level=crisis_result.risk_level,
                ai_analysis=crisis_result.ai_analysis
            )

            if crisis_result.should_show_bubble:
                logger.warning(f"⚠️ 检测到危机信号 - 用户ID: {data.user_id}, 风险等级: {crisis_result.risk_level}")
            else:
                logger.info("✅ 危机检测完成 - 无明显风险")

        except Exception as e:
            logger.error(f"❌ 危机检测失败: {e}")
            # 不阻塞主流程,使用默认安全值
            crisis_warning = CrisisWarningInfo()

    # ... AI调用逻辑 ...

    # 返回时包含危机预警信息
    return DialogResponse(content=optimized, crisis_warning=crisis_warning)
```

#### 3. 关键特性

- **非阻塞**: 使用 try-except 确保危机检测失败不影响 AI 对话
- **模糊检测**: 自动识别同音字替换(如"zi sha" → "自杀")
- **AI 增强**: `enable_ai=True` 启用 AI 深度分析,提供 30 字左右的专业建议
- **默认安全值**: 检测失败时返回 `CrisisWarningInfo()`,不显示气泡

### 前端实现

#### 1. 修改 `chatMixin.js`

在 `callAIAPI` 方法中添加:

```javascript
async callAIAPI(messages, scene = 'general', userProfile = null) {
    return new Promise((resolve, reject) => {
        const requestData = {
            messages: messages,
            scene: scene,
            user_id: uni.getStorageSync('user_id') || null  // 🚨 添加用户ID
        };

        // ... 现有代码 ...

        success: (res) => {
            if (res.statusCode === 200) {
                // 🚨 处理危机预警信息
                if (res.data.crisis_warning && res.data.crisis_warning.should_show_bubble) {
                    console.log('🚨 收到危机预警:', res.data.crisis_warning);
                    this.handleCrisisWarning(res.data.crisis_warning);
                }
                resolve(res.data);
            }
        }
    });
}
```

#### 2. 添加危机预警处理方法

```javascript
methods: {
    /**
     * 🚨 处理后端返回的危机预警信息
     */
    handleCrisisWarning(crisisWarning) {
        console.log('🚨 处理危机预警信息:', crisisWarning);

        this.backendCrisisWarning = crisisWarning;
        this.riskDetectedInSession = true;

        const riskLevelMessages = {
            'LOW': '💙 我注意到您的情绪状态,如需帮助请随时告诉我',
            'MEDIUM': '💛 我感受到您可能正在经历一些困扰,建议与朋友或专业人士交流',
            'HIGH': '🧡 您提到的内容让我担心,强烈建议寻求专业心理健康支持',
            'CRITICAL': '❤️ 请立即寻求专业帮助！如有紧急情况,请拨打心理危机干预热线:400-161-9995'
        };

        const message = crisisWarning.bubble_message ||
                       riskLevelMessages[crisisWarning.risk_level] ||
                       riskLevelMessages['MEDIUM'];

        // 显示气泡提示
        uni.showModal({
            title: '💙 看板娘关怀',
            content: message,
            showCancel: true,
            cancelText: '我知道了',
            confirmText: '获取帮助',
            success: (res) => {
                if (res.confirm) {
                    this.showHelpResources(crisisWarning);
                }
            }
        });
    },

    /**
     * 🚨 显示帮助资源
     */
    showHelpResources(crisisWarning) {
        const helpContent = `💙 心理健康支持资源

📞 心理危机干预热线
400-161-9995(24小时)

🏥 专业心理咨询
建议寻求专业心理咨询师帮助

${crisisWarning.ai_analysis ? '\n🤖 AI分析建议:\n' + crisisWarning.ai_analysis : ''}

请记住:
• 您并不孤单
• 寻求帮助是勇敢的表现
• 专业支持可以帮助您`;

        uni.showModal({
            title: '💙 帮助资源',
            content: helpContent,
            showCancel: false,
            confirmText: '我知道了'
        });
    }
}
```

## 📊 与 Tree-hole 对比

| 特性             | AI Dialog (新)               | Tree-hole Whisper              |
| ---------------- | ---------------------------- | ------------------------------ |
| **检测位置**     | 路由处理器 ✅                | 路由处理器 ✅                  |
| **检测组件**     | `CrisisDetectorComponent` ✅ | `CrisisDetectorComponent` ✅   |
| **返回气泡信息** | ✅ `crisis_warning` 字段     | ✅ `crisis_warning` 字段       |
| **模糊检测**     | ✅ 支持同音字/空格变体       | ✅ 支持同音字/空格变体         |
| **AI 增强分析**  | ✅ `enable_ai=True`          | ✅ 可选                        |
| **前端展示**     | ✅ Modal 气泡                | ✅ `crisis-warning-bubble.vue` |
| **用户 ID 来源** | 请求参数 `user_id`           | JWT token                      |

## 🔍 检测流程

```
用户发送消息
    ↓
前端携带user_id调用 /ai-dialog
    ↓
后端提取最新用户消息
    ↓
调用 CrisisDetectorComponent.detect_content_risk()
    ├─ 模糊关键词检测
    ├─ AI深度分析(可选)
    └─ 返回 CrisisDetectionResult
    ↓
构建 CrisisWarningInfo
    ↓
包含在 DialogResponse 中返回
    ↓
前端检查 should_show_bubble
    ↓
显示看板娘关怀气泡
```

## 🎨 用户体验

### 危机检测触发场景

用户输入包含以下内容时会触发检测:

**精确匹配**:

- "自杀"、"自伤"、"不想活了"等直接表述

**模糊匹配**:

- "zi sha"、"自 杀"(空格变体)
- "想 s i"(拼音+字母组合)

**语义检测**(AI 分析):

- "感觉生活没有意义"
- "每天都很痛苦,看不到希望"

### 气泡显示策略

- **LOW**: 不显示气泡(仅记录日志)
- **MEDIUM**: 显示温和提示"💛 我感受到您可能正在经历一些困扰..."
- **HIGH**: 显示关切提示"🧡 您提到的内容让我担心..."
- **CRITICAL**: 显示紧急提示"❤️ 请立即寻求专业帮助!..."

## 🚀 部署检查清单

### 后端

- [x] 安装依赖: `CrisisDetectorComponent` 已存在
- [x] 导入模块: `from app.services.crisis_detector_component import get_crisis_detector`
- [x] 修改响应模式: `DialogResponse` 包含 `crisis_warning` 字段
- [x] 集成检测逻辑: 在 `ai_dialog()` 函数中调用检测器
- [x] 添加日志: 记录检测结果
- [ ] 测试 API: 使用 Swagger UI 测试 `/ai-dialog` 端点

### 前端

- [x] 修改 API 调用: `callAIAPI` 添加 `user_id` 参数
- [x] 添加处理方法: `handleCrisisWarning()` 和 `showHelpResources()`
- [x] 添加数据字段: `backendCrisisWarning` 在 `data()`
- [ ] 测试页面: 在 `self-dialog.vue` 中测试危机检测
- [ ] UI 优化: 可选替换 Modal 为自定义气泡组件

## 📝 测试用例

### 测试场景 1: 无风险对话

**输入**: "今天天气真好"
**预期**:

- 后端: `crisis_warning.should_show_bubble = false`
- 前端: 不显示气泡

### 测试场景 2: 中等风险(模糊检测)

**输入**: "感觉 zi sha 也没什么"
**预期**:

- 后端: 检测到"zi sha" → "自杀",风险等级 MEDIUM/HIGH
- 前端: 显示"💛 我感受到您可能正在经历一些困扰..."

### 测试场景 3: 高风险(直接表述)

**输入**: "我想自杀"
**预期**:

- 后端: 检测到"自杀",风险等级 CRITICAL
- 前端: 显示"❤️ 请立即寻求专业帮助!..."

### 测试场景 4: AI 语义检测

**输入**: "每天都很痛苦,感觉生活没有任何意义"
**预期**:

- 后端: AI 分析检测到抑郁倾向,风险等级 MEDIUM/HIGH
- 前端: 显示气泡 + AI 分析建议

## 🔧 故障排查

### 问题 1: 危机检测不触发

**可能原因**:

- `user_id` 未传递或为 null
- 危机检测组件导入失败

**解决方案**:

```python
# 检查日志
logger.info(f"用户ID: {data.user_id}")
logger.info(f"最新消息: {latest_user_message}")

# 确认导入
from app.services.crisis_detector_component import get_crisis_detector
```

### 问题 2: 前端不显示气泡

**可能原因**:

- `should_show_bubble = false`
- 前端未正确处理响应

**解决方案**:

```javascript
// 添加调试日志
console.log("API响应:", res.data);
console.log("危机预警:", res.data.crisis_warning);
console.log("是否显示气泡:", res.data.crisis_warning?.should_show_bubble);
```

### 问题 3: AI 分析失败

**可能原因**:

- AI 服务超时
- API 密钥无效

**解决方案**:

```python
# 危机检测使用try-except,AI失败不影响主流程
try:
    crisis_result = await detector.detect_content_risk(
        content=latest_user_message,
        scene="chat",
        user_id=data.user_id,
        enable_ai=True
    )
except Exception as e:
    logger.error(f"AI分析失败: {e}")
    # 仍然返回基于关键词的检测结果
```

## 📚 相关文档

- `CRISIS_WARNING_INTEGRATION_GUIDE.md` - 完整的危机预警集成指南
- `backend/app/services/crisis_detector_component.py` - 危机检测组件源码
- `frontend/src/components/crisis-warning-bubble.vue` - 气泡组件(可选)
- `.github/copilot-instructions.md` - 项目架构文档

## 🎯 下一步优化

- [ ] 集成到日记(`diary`)场景
- [ ] 集成到心情追踪(`mood_tracker`)场景
- [ ] 使用自定义气泡组件替代 Modal
- [ ] 添加危机检测历史记录查看
- [ ] 优化 AI 分析 prompt,提供更个性化建议
- [ ] 连续低分心情自动触发预警

## ✅ 完成标记

- [x] 后端危机检测集成
- [x] 前端危机预警处理
- [x] 文档编写
- [ ] 单元测试
- [ ] 端到端测试
- [ ] 生产环境部署

---

**最后更新**: 2025-11-07
**维护者**: AI Coding Agent
**版本**: v1.0.0
