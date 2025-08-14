#file:ariadne/backend/app/config.py
from app.core.config import settings

# 数据库配置
DATABASE_URL = settings.database_url

# JWT配置
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes