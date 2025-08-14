from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.database.session import Base, engine
from app.core.config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    debug=settings.debug
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "欢迎使用恋恋有声后端API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}