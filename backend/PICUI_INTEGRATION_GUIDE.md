# PICUI 图床集成使用说明

## 配置步骤

### 1. 注册 PICUI 账号
1. 访问 https://picui.cn 注册账号
2. 登录后进入个人中心
3. 获取 API Token

### 2. 配置环境变量
在 `.env` 文件中添加以下配置：

```env
# PICUI 图床配置
PICUI_API_URL=https://picui.cn/api/v1
PICUI_TOKEN=your_picui_token_here
PICUI_STRATEGY_ID=1
PICUI_ALBUM_ID=
```

**配置说明：**
- `PICUI_TOKEN`: 从个人中心获取的 API Token（必须）
- `PICUI_STRATEGY_ID`: 存储策略ID，默认为1
- `PICUI_ALBUM_ID`: 相册ID，留空表示不使用相册

### 3. 安装依赖
确保已安装 `requests` 库：
```bash
pip install requests
```

## 功能说明

### 自动回退机制
系统实现了图床上传失败时的自动回退机制：
1. 优先上传到 PICUI 图床
2. 如果图床上传失败，自动回退到本地存储
3. 数据库中记录的是实际的存储路径（图床URL或本地路径）

### 权限设置
- **通用图片上传**: 设置为公开（permission=1）
- **用户背景图片**: 设置为私有（permission=0）

### 支持的图片格式
- JPEG/JPG
- PNG  
- GIF
- WebP
- BMP

### 文件大小限制
- 最大文件大小：10MB
- 建议文件大小：< 5MB

## 已修改的文件

### 1. 通用图片上传 (`app/api/routes/image.py`)
- 支持图床上传
- 自动回退到本地存储
- 返回图床URL或本地路径

### 2. 日记背景图片 (`app/api/routes/diary_backgrounds.py`)
- 私有权限上传
- 图床失败时本地备份
- 数据库存储实际路径

### 3. 用户自定义背景 (`app/api/routes/user_diary_backgrounds.py`)
- 私有权限上传
- 智能路径处理
- 支持图床和本地混合存储

### 4. 模型更新 (`app/models/user_diary_backgrounds.py`)
- URL返回逻辑优化
- 自动识别图床URL和本地路径

## 使用示例

### 检查配置
```python
from app.services.picui_service import picui_service

# 检查Token是否配置
if picui_service.token:
    print("PICUI配置正常")
else:
    print("请配置PICUI_TOKEN")
```

### 手动上传测试
```python
from app.services.picui_service import picui_service

# 测试上传
with open("test_image.jpg", "rb") as f:
    content = f.read()

result = await picui_service.upload_image(
    file_content=content,
    filename="test.jpg",
    permission=1
)

if result["success"]:
    print(f"上传成功: {result['data']['url']}")
else:
    print(f"上传失败: {result['message']}")
```

## 注意事项

1. **Token安全**: 请妥善保管PICUI Token，不要提交到版本控制
2. **配额限制**: PICUI有请求频率限制，请合理使用
3. **备份策略**: 重要图片建议定期备份
4. **监控日志**: 注意查看上传失败的日志，及时处理问题

## 错误处理

### 常见错误及解决方案

1. **Token未配置**
   ```
   Error: PICUI_TOKEN not configured
   ```
   解决：在.env文件中配置正确的PICUI_TOKEN

2. **网络连接失败**
   ```
   Error: Upload error: Connection timeout
   ```
   解决：检查网络连接，系统会自动回退到本地存储

3. **文件格式不支持**
   ```
   Error: 不支持的图片格式
   ```
   解决：确保上传的是支持的图片格式

4. **文件过大**
   ```
   Error: 文件大小不能超过10MB
   ```
   解决：压缩图片或降低图片质量

## 迁移说明

对于已有的本地图片，系统会继续正常工作：
- 新上传的图片优先使用图床
- 已有的本地图片继续从本地路径访问
- 数据库字段无需修改，兼容新旧存储方式