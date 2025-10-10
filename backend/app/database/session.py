# file:ariadne/backend/app/database/session.py
from sqlalchemy import create_engine, event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config import DATABASE_URL
import os

# 优化数据库连接池配置，解决间歇性连接失败问题
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # 连接池大小（默认5）
    max_overflow=20,  # 最大溢出连接（默认10）
    pool_pre_ping=True,  # 每次取连接时先ping检查有效性
    pool_recycle=3600,  # 1小时回收连接，避免MySQL超时断开
    echo=False,  # 生产环境关闭SQL日志
    connect_args={
        "connect_timeout": 10,  # 连接超时10秒
    },
)


# 监听连接池事件，处理跨进程使用连接的问题
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """连接建立时记录进程ID"""
    connection_record.info["pid"] = os.getpid()


@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """从连接池取连接时，检查进程ID是否匹配"""
    pid = os.getpid()
    if connection_record.info["pid"] != pid:
        # 进程不匹配，说明fork后复用了父进程的连接，需要重建
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(
            f"Connection record belongs to pid {connection_record.info['pid']}, "
            f"attempting to check out in pid {pid}"
        )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
