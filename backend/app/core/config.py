#file:ariadne/backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str

    # JWT配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # 应用配置
    debug: bool = False
    project_name: str = "念念有声"

    # AI相关配置
    ai_api_url: str
    ai_api_key: str
    ai_model: str
    ai_temperature: float = 0.7
    ai_max_tokens: int = 800
    ai_top_p: float = 0.9
    ai_timeout: float = 30.0
    
    # 数据加密配置
    encryption_password: str = "ariadne_default_key_2025"
    
    # 隐私保护配置
    data_retention_days: int = 365
    session_timeout_minutes: int = 30
    enable_audit_log: bool = True

    model_config = {
        "env_file": ".env",
        # Pydantic V2 语法 - 字段别名
        "case_sensitive": False,
        "env_prefix": "",
        "extra": "ignore"
    }

settings = Settings()