from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False)
    
    # 解锁状态
    is_unlocked = Column(Boolean, default=False, comment="是否已解锁")
    progress_data = Column(JSON, comment="进度数据")
    
    # 时间记录
    unlocked_at = Column(DateTime, comment="解锁时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", backref="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")