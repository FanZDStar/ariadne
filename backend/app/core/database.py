"""
数据库连接工具
"""
import mysql.connector
from contextlib import contextmanager
from urllib.parse import urlparse
from app.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """获取MySQL数据库连接"""
    conn = None
    try:
        # 处理SQLAlchemy格式的数据库URL (mysql+pymysql://)
        db_url = DATABASE_URL
        if 'mysql+pymysql://' in db_url:
            db_url = db_url.replace('mysql+pymysql://', 'mysql://')
        
        # 解析数据库URL
        parsed = urlparse(db_url)
        
        # 创建连接
        conn = mysql.connector.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:] if parsed.path else 'ariadne',
            charset='utf8mb4',
            autocommit=False
        )
        
        yield conn
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"数据库连接错误: {e}")
        raise
    finally:
        if conn:
            conn.close()
