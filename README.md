# Ariadne 念念有声

## 项目简介

念念有声(Ariadne)是一个专注于当代年轻人情感问题的综合型心理健康应用。项目旨在通过AI对话、碎碎念、心灵树洞等功能，帮助用户更好地理解和处理自己的情感问题，提升心理健康水平。

项目名称"Ariadne"来源于希腊神话中的阿里阿德涅，她帮助忒修斯走出迷宫，正如我们希望成为用户在情感迷宫中的引路者。

## 项目创意

在当今快节奏的社会中，年轻人面临着各种情感困扰，如恋爱问题、人际关系、自我认知等。然而，许多人缺乏倾诉的渠道或专业的指导。念念有声项目应运而生，致力于：

1. 提供一个安全、私密的情感倾诉空间
2. 通过AI技术为用户提供专业的情感建议和引导
3. 构建一个互相倾听、共鸣的社区环境
4. 帮助用户记录情感历程，促进自我成长

## 项目成果

https://ariadne.nuyoahming.xyz

## 核心功能

### 1. 情感对话

- 与AI进行一对一情感对话，获得专业建议
- 多种对话场景：自我反思、恋爱尝试、自我关爱等
- 对话历史记录，方便回顾和分析

### 2. 碎碎念

- 记录每日心情和情感变化
- 支持图片上传，丰富日记内容
- 情绪追踪，可视化情感变化趋势
- 隐私保护，日记可设置为私密

### 3.交往小技巧

- 提供实用的交往建议和技巧
- 给出一定的基本人际交往知识，不定期更新帮助用户提升情感技能
- 借助聊天区域的特定AI针对不同情况提供个性化建议

### 4. 感情防护

- 识别人际交往中的不公平现象
- 提供防护建议，帮助用户保护自己
- 教育用户建立健康的情感边界

### 5. 心灵树洞

- 匿名倾诉内心秘密和困扰
- 做倾听者，为他人提供情感支持
- 构建温暖的互助社区

### 6. 见心录

- 可视化展示用户的情感成长历程
- 分析情绪变化趋势
- 提供个性化的成长建议

## 技术架构

### 前端

- 使用UniApp框架开发，支持多端部署（H5、小程序、App）
- Vue.js作为核心框架
- 响应式设计，适配不同屏幕尺寸

### 后端

- Python FastAPI框架，提供高性能RESTful API
- MySQL数据库存储用户数据、日记、对话记录等
- JWT Token认证机制，确保用户信息安全
- 集成第三方AI服务，提供智能对话功能

## 运行/部署指南

### 环境要求

- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- npm 或 yarn

### 后端部署

1. 进入后端目录：

   ```bash
   cd backend
   ```
2. 创建并配置环境变量文件：

   在 `.env`文件中配置以下内容：

   ```
   # 数据库配置
   DATABASE_URL=mysql+pymysql://[用户名]:[密码]@localhost/ariadne

   # JWT配置
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # 后端AI配置(可更换为其它大模型)
   ai_api_url=https://api.suanli.cn/v1/chat/completions
   ai_api_key=your-api-key
   ai_model=free:Qwen3-30B-A3B
   ```
3. 创建数据库：

   - 创建名为 `ariadne`的MySQL数据库
   - 执行 `database/ariadne.sql`文件初始化表结构和基础数据
4. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

   或

   ```bash
   conda env create -f environment.yml
   ```
5. 启动服务：

   ```bash
   uvicorn app.main:app --reload
   ```

   后端服务默认运行在 `http://localhost:8000`

### 前端部署

1. 进入前端目录：

   ```bash
   cd frontend
   ```
2. 安装依赖：

   ```bash
   npm install
   ```
3. 启动开发服务器：

   ```bash
   npm run dev:h5
   ```

   访问终端提示的本地地址即可预览前端页面
4. 构建生产版本：

   ```bash
   npm run build:h5
   ```

### 数据库配置

1. 确保已安装MySQL 8.0+
2. 创建数据库：
   ```sql
   CREATE DATABASE ariadne CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 执行数据库脚本：
   ```bash
   mysql -u [用户名] -p ariadne < database/ariadne.sql
   ```

## API文档

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
│   │   └── utils/           # 工具函数
│   ├── uploads/             # 用户上传文件
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

1. 生产环境部署时，请务必修改默认的SECRET_KEY和数据库密码
2. 建议配置HTTPS以确保数据传输安全
3. 定期备份数据库以防数据丢失
4. 根据实际需求调整AI服务配置

## 未来规划

1. 引入更多AI模型，提供更精准的情感分析
2. 增加社交功能，支持用户间互动
3. 开发移动端App，提供更便捷的使用体验
4. 增加多语言支持，扩大用户群体
5. 集成更多心理健康评估工具

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 提交Issue到项目仓库
- 发送邮件至项目维护者邮箱

让我们一起关注心理健康，让每个人的情感都有一个温暖的归宿。
