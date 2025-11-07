# 🚨 AI 对话危机检测问题修复

## 问题诊断

### 根本原因

前端 `uni.getStorageSync('user_id')` 返回空值，导致后端危机检测逻辑未执行。

**原因分析**：

1. 后端登录接口 `/auth/login` 未返回 `user_id`
2. 前端登录成功后未保存 `user_id` 到本地存储
3. AI 对话请求时 `user_id` 为 `null`，触发了后端的条件检查 `if latest_user_message and data.user_id`

### 影响范围

- ❌ AI 对话危机检测不执行
- ❌ 无危机预警气泡显示
- ✅ AI 对话功能正常
- ✅ 旧版危机关键词检测正常（chatMixin 中的本地检测）

## 修复方案

### 修复 1: 后端返回 user_id

**文件**: `backend/app/api/routes/auth.py`

```python
# 第157-168行
return {
    "access_token": access_token,
    "token_type": "bearer",
    "user_id": db_user.user_id,  # 🆕 新增
    "username": db_user.username,  # 🆕 新增
    "star_awarded": star_awarded,
    "star_points": star_points,
    "star_message": star_message,
    "affection_awarded": affection_awarded,
    "affection_points": affection_points,
    "affection_message": affection_message,
    "affection_level_up": affection_level_up
}
```

### 修复 2: 前端保存 user_id

**文件**: `frontend/src/pages/login/login.vue`

```javascript
// 第176-189行
if (res.access_token) {
  // 保存token
  storage.setToken(res.access_token);

  // 🆕 保存用户ID（用于危机检测等功能）
  if (res.user_id) {
    uni.setStorageSync("user_id", res.user_id);
    console.log("✅ 已保存用户ID:", res.user_id);
  }

  // 🆕 保存用户名（可选）
  if (res.username) {
    uni.setStorageSync("username", res.username);
  }
  // ...
}
```

### 修复 3: 后端增强日志（已完成）

**文件**: `backend/app/api/routes/ai_dialog.py`

添加了详细的调试日志：

- 危机检测前置检查
- 危机检测结果详情
- 响应准备信息

## 测试步骤

### 1. 重启后端服务

```bash
# 如果使用uvicorn
cd backend
# 停止现有服务 Ctrl+C
uvicorn app.main:app --reload

# 如果使用pm2
pm2 restart ariadne-backend
```

### 2. 前端重新编译

```bash
cd frontend
# H5编译会自动热更新
# 或者手动刷新浏览器 Ctrl+Shift+R
```

### 3. 清除旧数据

在浏览器控制台执行：

```javascript
// 清除旧的存储数据
uni.clearStorageSync();

// 或者只清除相关数据
uni.removeStorageSync("access_token");
uni.removeStorageSync("user_id");
uni.removeStorageSync("username");
```

### 4. 重新登录

1. 访问登录页面: `http://localhost:5173/#/pages/login/login`
2. 输入账号密码登录
3. **关键检查**：打开控制台，应该看到：
   ```
   ✅ 已保存用户ID: 1  # 或其他数字
   ```

### 5. 验证 user_id 存储

在控制台执行：

```javascript
uni.getStorageSync("user_id");
// 应该返回数字，如: 1
```

### 6. 测试危机检测

1. 进入 AI 对话页面: `http://localhost:5173/#/pages/AI-emotional-chat/self-dialog/self-dialog?scene=self-dialog`
2. 输入测试消息: `"感觉zi sha也没什么"`
3. 点击发送

**预期结果**：

#### 后端日志（控制台）：

```
🔍 危机检测前置检查:
  - 最新用户消息: 感觉zi sha也没什么...
  - 用户ID: 1
  - 是否有用户消息: True
🚨 开始进行危机检测...
🔍 危机检测结果:
  - should_show_bubble: True
  - risk_level: MEDIUM/HIGH
  - bubble_message: 💛 我感受到您可能正在经历一些困扰...
⚠️ 检测到危机信号 - 用户ID: 1, 风险等级: MEDIUM
📤 准备返回响应:
  - AI内容长度: 150
  - 危机预警 should_show_bubble: True
  - 危机预警 risk_level: MEDIUM
```

#### 前端控制台：

```
✅ AI对话响应成功
📦 完整响应数据: {content: "...", crisis_warning: {...}}
🔍 危机预警检查: {
  存在: true,
  should_show_bubble: true,
  risk_level: "MEDIUM",
  bubble_message: "💛 我感受到您可能正在经历一些困扰..."
}
🚨 收到危机预警: {should_show_bubble: true, ...}
🚨 处理危机预警信息: {should_show_bubble: true, ...}
```

#### 前端页面：

- AI 正常回复
- **弹出 Modal 气泡**：
  - 标题: "💙 看板娘关怀"
  - 内容: "💛 我感受到您可能正在经历一些困扰，建议与朋友或专业人士交流"
  - 按钮: "我知道了" / "获取帮助"

### 7. 测试其他风险等级

#### 低风险（不显示气泡）：

输入: `"今天天气真好"`
预期: 无气泡显示

#### 高风险：

输入: `"我想自杀"`
预期:

- 气泡: "🧡 您提到的内容让我担心，强烈建议寻求专业心理健康支持"

#### 紧急风险：

输入: `"我现在就要自杀"`
预期:

- 气泡: "❤️ 请立即寻求专业帮助！如有紧急情况，请拨打心理危机干预热线：400-161-9995"

## 故障排查

### 问题 1: 登录后仍然没有 user_id

**检查**：

```javascript
// 控制台
uni.getStorageSync("user_id");
```

**解决**：

1. 确认后端已重启
2. 清除浏览器缓存 `Ctrl+Shift+R`
3. 重新登录
4. 检查网络请求响应（F12 → Network → login 请求）

### 问题 2: 后端日志显示 user_id 为 None

**检查后端代码**：

```python
# ai_dialog.py 第302行附近
logger.info(f"  - 用户ID: {data.user_id}")
```

**解决**：

1. 检查前端请求数据（F12 → Network → ai-dialog 请求 → Payload）
2. 确认 `user_id` 字段存在且有值
3. 检查 `chatMixin.js` 第 86 行是否正确获取

### 问题 3: 危机检测执行但不显示气泡

**检查后端日志**：

```
should_show_bubble: False
```

**原因**：检测到的风险等级为 LOW，不触发气泡

**验证**：使用更明确的危机关键词测试

### 问题 4: 前端控制台无危机预警日志

**检查**：

```javascript
// chatMixin.js 第111-124行
console.log("✅ AI对话响应成功");
console.log("📦 完整响应数据:", res.data);
```

**解决**：

1. 检查是否使用了正确的 `chatMixin.js`（不是 `chatMixin_enhanced.js`）
2. 清除浏览器缓存
3. 硬刷新页面 `Ctrl+Shift+R`

## 代码变更总结

### 后端变更

| 文件                                  | 变更                              | 行号             |
| ------------------------------------- | --------------------------------- | ---------------- |
| `backend/app/api/routes/auth.py`      | 添加 `user_id` 和 `username` 返回 | 157-168          |
| `backend/app/api/routes/ai_dialog.py` | 移除 `user_id` 强制检查           | 328              |
| `backend/app/api/routes/ai_dialog.py` | 添加详细调试日志                  | 302-359, 431-436 |

### 前端变更

| 文件                                 | 变更                      | 行号    |
| ------------------------------------ | ------------------------- | ------- |
| `frontend/src/pages/login/login.vue` | 保存 `user_id` 到本地存储 | 176-189 |
| `frontend/src/utils/chatMixin.js`    | 添加详细调试日志          | 111-124 |

## 验证清单

- [ ] 后端返回 `user_id` 字段
- [ ] 前端成功保存 `user_id`
- [ ] 控制台显示 `✅ 已保存用户ID: X`
- [ ] `uni.getStorageSync('user_id')` 返回数字
- [ ] AI 对话请求包含 `user_id` 参数
- [ ] 后端日志显示危机检测执行
- [ ] 前端控制台显示危机预警日志
- [ ] 输入危机关键词后显示气泡
- [ ] 点击"获取帮助"显示资源信息

## 额外优化建议

### 1. 注销时清除 user_id

在注销逻辑中添加：

```javascript
// 注销函数
logout() {
  uni.removeStorageSync('access_token');
  uni.removeStorageSync('user_id');  // 🆕
  uni.removeStorageSync('username');  // 🆕
  uni.reLaunch({ url: '/pages/login/login' });
}
```

### 2. 页面加载时验证 user_id

在 `self-dialog.vue` 的 `onLoad` 中添加：

```javascript
onLoad() {
  const userId = uni.getStorageSync('user_id');
  if (!userId) {
    console.warn('⚠️ 未检测到用户ID，部分功能可能受限');
  } else {
    console.log('✅ 用户ID已加载:', userId);
  }
}
```

### 3. 使用自定义气泡组件

将来可以替换 `uni.showModal` 为自定义的 `crisis-warning-bubble.vue` 组件，提供更好的视觉效果。

---

**修复完成时间**: 2025-11-07  
**修复者**: AI Coding Agent  
**测试状态**: ⏳ 待测试  
**下一步**: 执行上述测试步骤，验证修复效果
