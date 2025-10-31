"""
用户树洞能量模型
"""
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.session import Base


class TreeEnergy(Base):
    """用户树洞能量表"""
    __tablename__ = "user_tree_energy"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    energy = Column(Integer, nullable=False, default=0, comment="当前能量值")
    level = Column(Integer, nullable=False, default=1, comment="浇水等级")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
