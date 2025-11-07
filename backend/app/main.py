from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from app.api import api_router
from app.database.session import Base, engine
from app.core.config import settings
from app.middleware.crisis_monitoring import CrisisMonitoringMiddleware
from app.services.crisis_monitoring_task import crisis_monitor
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# 导入模型预加载函数
from app.services.offensive_content_detector import preload_model

# ==================== 配置日志系统 ====================
# 确保logs目录存在
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# 配置根日志器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # 控制台处理器
        logging.StreamHandler(),
        # 文件处理器 - 使用RotatingFileHandler自动轮转
        RotatingFileHandler(
            filename=os.path.join(LOGS_DIR, 'app.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,  # 保留5个备份文件
            encoding='utf-8'
        )
    ]
)

# 获取根日志器
logger = logging.getLogger(__name__)
logger.info(f"📝 日志系统已初始化 - 日志文件: {os.path.join(LOGS_DIR, 'app.log')}")
# ====================================================

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
    logger.info("=" * 60)
    logger.info("🚀 应用启动中...")
    logger.info("=" * 60)
    
    # 预加载冒犯性内容检测模型（在后台线程中加载，不阻塞启动）
    asyncio.create_task(asyncio.to_thread(preload_model))
    
    # 启动心理危机监控任务（可选，根据需要启用）
    # asyncio.create_task(crisis_monitor.start_monitoring(check_interval_hours=6))
    
    logger.info("✅ 应用启动完成！")
    logger.info("=" * 60)

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 打印详细定位信息
    print("❗RequestValidationError", exc.errors())
    body = await request.body()
    print("❗Request body bytes:", body)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})