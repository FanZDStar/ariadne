"""
用户水滴模型
"""
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.session import Base


class UserWaterDrops(Base):
    """用户水滴表"""
    __tablename__ = "user_water_drops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    water_drops = Column(Integer, nullable=False, default=0, comment="用户当前拥有的水滴数量")
    total_earned = Column(Integer, nullable=False, default=0, comment="累计获得的水滴总数")
    total_used = Column(Integer, nullable=False, default=0, comment="累计使用的水滴总数")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
