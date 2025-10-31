"""
用户浇水冷却记录模型
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.session import Base


class UserWateringCooldown(Base):
    """用户浇水冷却记录表"""
    __tablename__ = "user_watering_cooldown"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    last_watering_time = Column(DateTime, nullable=False, comment="最后一次浇水时间", index=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
