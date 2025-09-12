from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="成就名称")
    description = Column(Text, comment="成就描述")
    icon = Column(String(50), comment="成就图标")
    category = Column(String(50), comment="成就分类")
    
    # 成就条件
    unlock_conditions = Column(JSON, comment="解锁条件")
    reward_points = Column(Integer, default=0, comment="奖励积分")
    
    # 状态管理
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序序号")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联用户成就
    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")