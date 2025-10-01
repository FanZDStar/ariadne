from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from app.api import api_router
from app.database.session import Base, engine
from app.core.config import settings
from app.middleware.crisis_monitoring import CrisisMonitoringMiddleware
from app.services.crisis_monitoring_task import crisis_monitor

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

# 添加心理危机监控中间件
app.add_middleware(CrisisMonitoringMiddleware)

# 挂载上传目录为静态文件目录
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 挂载前端静态文件目录
frontend_static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "src", "static")
if os.path.exists(frontend_static_path):
    app.mount("/static", StaticFiles(directory=frontend_static_path), name="static")
    print(f"✅ 静态文件目录已挂载: {frontend_static_path}")

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    # 启动心理危机监控任务（可选，根据需要启用）
    # asyncio.create_task(crisis_monitor.start_monitoring(check_interval_hours=6))
    pass

@app.on_event("shutdown") 
async def shutdown_event():
    """应用关闭时的事件处理"""
    # 停止监控任务
    crisis_monitor.stop_monitoring()

@app.get("/")
def root():
    return {"message": "欢迎使用念念有声后端API"}

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