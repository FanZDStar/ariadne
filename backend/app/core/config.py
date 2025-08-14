#file:ariadne/backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str
    
    # JWT配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    debug: bool = False
    project_name: str = "恋恋有声"
    
    class Config:
        env_file = ".env"

settings = Settings()