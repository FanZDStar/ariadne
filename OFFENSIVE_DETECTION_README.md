# 冒犯性内容检测功能 - 快速开始

## ✅ 已完成的工作

### 1. 后端实现

- ✅ 创建冒犯性检测服务 (`backend/app/services/offensive_content_detector.py`)
- ✅ 集成到树洞评论 API (`backend/app/api/routes/tree_hole.py`)
- ✅ 添加测试脚本 (`backend/scripts/test_offensive_detector.py`)
- ✅ 更新依赖配置 (`backend/requirements.txt`)

### 2. 前端实现

- ✅ 优化评论提交错误处理 (`frontend/src/pages/tree-hole/whisper-detail.vue`)
- ✅ 添加友好的拦截提示弹窗

### 3. 文档

- ✅ 详细使用文档 (`backend/OFFENSIVE_CONTENT_DETECTION.md`)
- ✅ 更新 AI 指南 (`.github/copilot-instructions.md`)

## 🚀 快速启动

### 步骤 1: 安装依赖

```bash
cd backend
pip install transformers>=4.30.0 torch>=2.0.0
```

### 步骤 2: 下载模型到本地

```bash
# 下载模型到项目本地（推荐）
python scripts/download_offensive_model.py
```

**模型下载说明**：

- 📦 模型大小：约 400MB
- 📁 保存位置：`backend/models/offensive_detector/local_model/`
- ⏱️ 下载时间：首次约 3-5 分钟（取决于网络速度）
- 🔄 自动使用：服务会优先使用本地模型

**国内网络优化**：

```bash
# 设置镜像加速下载
export HF_ENDPOINT=https://hf-mirror.com
python scripts/download_offensive_model.py
```

### 步骤 3: 测试功能（可选）

```bash
python scripts/test_offensive_detector.py
```

### 步骤 4: 启动服务

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**启动时会自动预加载模型**：

- 🚀 模型会在后台线程中自动加载
- ⚡ 不会阻塞应用启动
- 📊 查看日志可以看到加载进度
- ✅ 首次评论检测无需等待

**启动日志示例**：

```
============================================================
🚀 应用启动中...
============================================================
🚀 开始预加载冒犯性内容检测模型...
✅ 使用本地模型: D:\project\ariadne\backend\models\offensive_detector\local_model
Device set to use cpu
✅ 冒犯性内容检测模型加载成功
✅ 模型测试通过: NORMAL
✅ 冒犯性内容检测模型预加载成功！
✅ 应用启动完成！
============================================================
```

## 📋 功能说明

### 自动拦截场景

当用户在树洞发表评论时，系统会自动检测内容：

1. **正常内容** → ✅ 允许发布

   - 示例："你这个观点真不错！"

2. **冒犯性内容** → 🚫 拦截并提示
   - 示例："傻逼"、"你是不是脑子有病"
   - 用户看到: "您的评论包含不当内容，请文明发言"

### 检测原理

- 使用清华大学 COAI 的 `roberta-base-cold` 模型
- 置信度阈值: 70% (可调整)
- 支持中文侮辱性、攻击性语言识别

## 🎯 用户体验

### 评论被拦截时

用户会看到以下弹窗：

```
┌─────────────────────┐
│   评论被拦截        │
├─────────────────────┤
│ 您的评论包含不当内容 │
│ 请文明发言          │
│                     │
│    [我知道了]        │
└─────────────────────┘
```

### 优雅降级

如果检测服务异常：

- ✅ 评论仍然可以正常发布
- 📝 后台记录错误日志
- 👤 用户体验不受影响

## ⚙️ 配置选项

### 调整检测严格程度

编辑 `backend/app/api/routes/tree_hole.py`:

```python
# 当前配置 (平衡模式)
detection_result = check_offensive_content(comment_data.content, threshold=0.7)

# 更严格 (拦截更多)
detection_result = check_offensive_content(comment_data.content, threshold=0.5)

# 更宽松 (仅拦截明显侮辱)
detection_result = check_offensive_content(comment_data.content, threshold=0.9)
```

## 📊 性能指标

### CPU 模式 (默认)

- 检测速度: ~0.1-0.3 秒/次
- 内存占用: ~500MB
- 适合: 中小型应用

### GPU 模式 (可选)

- 检测速度: ~0.01-0.05 秒/次
- 需要: NVIDIA GPU
- 适合: 高并发场景

启用 GPU: 编辑 `offensive_content_detector.py`，取消注释 `device=0`

## 🧪 测试用例

测试脚本会验证以下场景：

| 测试内容               | 预期结果 | 说明     |
| ---------------------- | -------- | -------- |
| "你这个观点真是太棒了" | ✅ 通过  | 正常评论 |
| "今天天气不错"         | ✅ 通过  | 日常内容 |
| "你是不是脑子有病？"   | 🚫 拦截  | 直接侮辱 |
| "傻逼，滚出去"         | 🚫 拦截  | 脏话     |
| "NMSL"                 | 🚫 拦截  | 网络用语 |

## 🔄 扩展到其他场景

该功能可轻松应用到:

1. **日记内容检测**
2. **AI 对话输入过滤**
3. **用户昵称审核**
4. **悄悄话标题检测**

参考 `backend/OFFENSIVE_CONTENT_DETECTION.md` 查看代码示例。

## ❓ 常见问题

### Q1: 模型下载太慢怎么办？

使用国内镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### Q2: 检测到误判怎么办？

可以调整阈值 (threshold) 或联系开发者收集误判案例。

### Q3: 会不会影响启动速度？

不会！模型采用**延迟加载**，只在首次使用时才加载。

### Q4: 检测失败会影响用户发评论吗？

不会！检测失败时会自动跳过，评论正常发布。

## 📚 详细文档

完整文档请查看: `backend/OFFENSIVE_CONTENT_DETECTION.md`

包含:

- 技术架构详解
- API 使用示例
- 性能优化指南
- 故障排除方法

## 🎉 总结

冒犯性内容检测功能已完全集成，具备以下特点：

- ✅ 自动化检测，无需人工审核
- ✅ 智能拦截，保护社区环境
- ✅ 优雅降级，不影响用户体验
- ✅ 性能优秀，延迟加载机制
- ✅ 易于扩展到其他场景

---

**最后更新**: 2025 年 11 月 4 日
