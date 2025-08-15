# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api import api_router
# from app.database.session import Base, engine
# from app.core.config import settings

# # 创建数据库表
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.project_name,
#     debug=settings.debug
# )

# # 添加CORS中间件
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 在生产环境中应该指定具体的域名
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# app.include_router(api_router)

# @app.get("/")
# def root():
#     return {"message": "欢迎使用恋恋有声后端API"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

#file:ariadne/backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import api_router
from app.database.session import Base, engine
from app.core.config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)


# 确保上传目录存在
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI(
    title=settings.project_name,
    debug=settings.debug
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 挂载上传目录为静态文件目录
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "欢迎使用恋恋有声后端API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test-upload")
def test_upload():
    """测试上传目录是否存在文件"""
    import os
    files = []
    if os.path.exists("uploads"):
        files = os.listdir("uploads")
    return {"upload_dir_exists": os.path.exists("uploads"), "files": files}