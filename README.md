
# Ariadne 念念有声

## 项目简介

念念有声(Ariadne)是一个专注于当代年轻人情感问题的综合型心理健康应用。项目旨在通过AI对话、碎碎念、心灵树洞等功能，帮助用户更好地理解和处理自己的情感问题，提升心理健康水平。

项目名称"Ariadne"来源于希腊神话中的阿里阿德涅，她帮助忒修斯走出迷宫，正如我们希望成为用户在情感迷宫中的引路者。

## 项目成果

https://ariadne.nuyoahming.xyz

## 核心功能

### 1. 情感对话

- **智能AI对话**：与AI进行一对一情感对话，获得专业建议
- **多样化场景**：自我反思、恋爱尝试、自我关爱、学业压力、社交焦虑等
- **完整历史记录**：对话历史永久保存，方便回顾和分析
- **多模态对话**：
  - 支持纯文本、纯图片、图文混合三种模式
  - AI智能分析图片内容，提供个性化建议
  - 图床永久存储，历史记录完整显示

### 2. 人际智慧

- 交往小技巧
  - 提供实用的交往建议和技巧
  - 给出一定的基本人际交往知识
  - 不定期更新帮助用户提升情感技能
  - 借助聊天区域的特定AI针对不同情况提供个性化建议

- 感情防护

  - 识别人际交往中的不公平现象
  - 提供防护建议，帮助用户保护自己
  - 教育用户建立健康的情感边界

### 3. 心灵树洞
- 此情此语
  - 悄悄话匿名倾诉内心秘密和困扰
- 做倾听者，
  - 为他人提供情感支持
  - 构建温暖的互助社区

### 4.碎碎念

记录每日心情和情感变化

支持图片上传，丰富日记内容

情绪追踪，可视化情感变化趋势

隐私保护，日记可设置为私密


### 5. 见心录
可视化展示用户的情感成长历程
分析情绪变化趋势
提供个性化的成长建议

### 6.积分系统

可以通过登录或参与互动等方式来获取积分，积分积攒到一定数量后可购买可爱的看板娘

### 7.心理状态评估

AI分析你的心理健康状态和风险评估

## 技术架构

### 前端
- 使用UniApp框架开发，支持多端部署（H5、小程序、App）
- Vue.js作为核心框架
- 响应式设计，适配不同屏幕尺寸

### 后端
- **Python FastAPI框架**：提供高性能RESTful API
- **MySQL数据库**：存储用户数据、日记、对话记录等
- **JWT Token认证**：确保用户信息安全
- **AI服务集成**：集成阿里云百炼API，提供智能对话功能
- **多模态AI支持**：
  - 集成Qwen3-VL-32B-Thinking视觉语言模型
  - 支持图片内容理解与分析
  - Base64格式传输，确保兼容性
- **PICUI图床服务**：图片上传和存储管理
- **智能容错机制**：网络异常处理、超时设置、降级策略

## 快速开始

### 一、环境准备
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- npm（推荐）
- 阿里云百炼API密钥（用于AI功能）
- PICUI图床token（用于图片存储）

### 二、数据库配置
1. 确保已安装MySQL 8.0+
2. 创建数据库：
   ```sql
   CREATE DATABASE ariadne CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 执行数据库脚本：
   ```bash
   mysql -u [用户名] -p ariadne < database/ariadne.sql
   ```
4. **多模态功能支持**（可选）：
   ```bash
   mysql -u [用户名] -p ariadne < database/add_multimodal_fields.sql
   ```

### 三、后端启动
1. 进入后端目录：
   ```bash
   cd backend
   ```
2. 创建 `.env` 文件，并添加以下内容（改成你的MySQL账号名，`admin123` 改为你的数据库密码）：
   ```env
   # 数据库配置
   DATABASE_URL=mysql+pymysql://root:你的密码@localhost/ariadne
   # JWT配置
   SECRET_KEY=你的key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # 后端AI配置
   ai_api_url=你的url
   ai_api_key=你的key
   ai_model=
   
   # 多模态AI配置（可选，用于图片分析）
   vision_model=qwen-vl-max
   
   # PICUI图床配置（可选，用于图片上传存储）
   picui_api_url=你的图床API地址
   picui_token=你的图床token
   picui_strategy_id=你的策略ID
   picui_album_id=你的相册ID
   ```
3. 安装依赖（推荐使用虚拟环境）：
   ```bash
   # 进入后端目录
   cd ariadne/backend
   
   # 创建虚拟环境（使用Python 3.8+）
   python -m venv venv
   
   # 或者如果你使用的是python3命令
   python3 -m venv venv
   
   # PowerShell
   venv\Scripts\Activate.ps1
   
   # 确保虚拟环境已激活
   pip install -r requirements.txt
   
   # 启动开发服务器（明确指定host和port）
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   
   # 生产环境启动（高性能）
   # gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
   
   # 关闭服务器
   CTRL+C
   
   # 退出虚拟环境
   deactivate
   ```
4. 启动开发服务器：
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. 服务器启动后，访问以下地址查看API文档：
   - 交互式文档: http://localhost:8000/docs
   - ReDoc文档: http://localhost:8000/redoc
   - 基础接口测试: http://localhost:8000/

### 四、前端启动

1. 进入前端目录：
   ```bash
   cd frontend
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 创建 `.env` 文件，并添加以下内容：
   ```env
   # API 访问地址，举例：本机测试环境
   VUE_APP_API_BASE_URL=http://localhost:8000
   ```
4. 启动开发服务器（H5模式）：
   ```bash
   npm run dev:h5
   ```
5. 浏览器访问终端提示的本地地址即可预览前端页面。

### API文档
后端API使用FastAPI自动生成交互式文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 项目结构
```
ariadne/
├── backend/                 # 后端代码
│   ├── app/                 # 应用核心代码
│   │   ├── api/             # API路由
│   │   ├── core/            # 核心配置
│   │   ├── database/        # 数据库连接
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # 数据验证模型
│   │   ├── services/        # 业务逻辑层
│   │   └── utils/           # 工具函数
│   ├── requirements.txt     # Python依赖
│   └── app.main.py          # 应用入口
├── frontend/                # 前端代码
│   ├── src/                 # 源代码
│   │   ├── components/      # 公共组件
│   │   ├── pages/           # 页面组件
│   │   ├── utils/           # 工具函数
│   │   ├── App.vue          # 根组件
│   │   ├── main.js          # 入口文件
│   │   └── pages.json       # 路由配置
│   ├── package.json         # Node.js依赖
│   └── vite.config.js       # 构建配置
├── database/                # 数据库脚本
└── README.md               # 项目说明文档
```

## 注意事项

### 部署安全
1. **密钥安全**：生产环境部署时，请务必修改默认的SECRET_KEY和数据库密码
2. **HTTPS配置**：建议配置HTTPS以确保数据传输安全
3. **数据备份**：定期备份数据库以防数据丢失

### 功能配置
4. **AI服务配置**：根据实际需求调整AI服务配置和模型选择
5. **多模态功能**：
   - 使用多模态功能前，确保已执行数据库迁移脚本 `add_multimodal_fields.sql`
   - 配置PICUI图床的token和相册ID
   - H5环境下图片上传会自动转换为base64，移动端使用文件上传方式
6. **环境变量**：确保所有必要的环境变量已正确配置（参考后端.env配置说明）

## 新增功能

### 多模态对话功能

支持图片+文字的混合对话模式，用户可以上传图片并询问AI相关问题。

#### 使用场景
- **情感日记分享**：拍摄记录心情的照片，与AI分享你的情感状态
- **聊天截图分析**：发送聊天截图，让AI帮助你理解对方的情感信号
- **情境描述**：展示生活中的场景，获取针对性的情感建议
- **图片纯发送**：仅发送图片让AI自由发挥分析

#### 技术特点
- **智能模式切换**：纯文本/纯图片/图文混合三种模式自动识别
- **图床集成**：PICUI图床服务，图片永久存储
- **双格式处理**：Base64发送给AI分析，URL保存到数据库
- **历史记录**：完整的对话和图片历史，随时回顾
- **智能降级**：网络异常时自动降级，保证可用性
- **兼容性好**：自动检测环境（H5/移动端），使用合适的上传方式
- **格式支持**：支持多种图片格式（JPG、PNG、WebP等）
- **图片预览**：点击图片可全屏预览，查看细节

#### 技术实现
1. **数据存储**
   - `msg_type`: ENUM类型（text/img/multimodal）
   - `img_urls`: JSON数组存储图片URL
   - 完整的历史记录显示

2. **工作流程**
   ```
   用户选择图片 → 上传到图床 → 获取URL → Base64发送给AI
   → AI分析回复 → 存储URL到数据库 → 显示图片和回复
   ```

3. **容错机制**
   - 60秒超时设置
   - 网络失败智能降级
   - 旧数据自动兼容
   - 单文件/多文件自适应

详细实现文档请参考 `MULTIMODAL_IMPLEMENTATION.md`

## 未来规划

### 近期优化
1. **多模态能力增强**：支持视频分析和多图理解
2. **AI模型升级**：引入更多专业心理健康AI模型
3. **评估工具扩展**：集成更多心理健康评估工具

### 中期目标
4. **社交功能**：增加用户间互动和互助社区
5. **移动端优化**：开发原生App，提供更流畅体验
6. **多语言支持**：扩大用户群体，国际化布局

### 长期愿景
7. **个性化定制**：AI根据用户画像提供更精准建议
8. **数据可视化**：更丰富的情绪趋势和成长分析
9. **专业资源整合**：连接心理咨询师和机构资源

## 联系方式
如有任何问题或建议，请通过以下方式联系我们：
- 提交Issue到项目仓库
- 发送邮件至项目维护者邮箱

让我们一起关注心理健康，让每个人的情感都有一个温暖的归宿。