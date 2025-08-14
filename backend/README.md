# Backend
## 一 注意：在backend文件下下创建一个.env文件，并在其中添加以下内容并将下文中的root改成你的mysql账号名，admin123改为你的数据库密码
```
# 数据库配置
DATABASE_URL=mysql+pymysql://root:admin123@localhost/ariadne
# JWT配置
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=True
```

## 二 准备数据库
SQL文件见database文件夹，导入到mysql中即可

## 三 运行项目
建议在虚拟环境下安装，可以直接使用python自带的工具来创建虚拟环境
下面的是没有使用虚拟环境的代码
```bash
cd ariadne/backend
pip install -r requirements.txt
```
下面是使用虚拟环境的代码
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

# 启动开发服务器
uvicorn app.main:app --reload

# 退出虚拟环境
deactivate
```