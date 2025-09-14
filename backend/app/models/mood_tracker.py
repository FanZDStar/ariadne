from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class MoodTracker(Base):
    """心情晴雨表模型"""
    __tablename__ = "mood_tracker"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    mood_date = Column(Date, nullable=False, comment="心情记录日期")
    mood_level = Column(Integer, nullable=False, comment="心情档位(1-5档)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 设置联合唯一约束：用户每天只能记录一次心情
    __table_args__ = (
        UniqueConstraint('user_id', 'mood_date', name='unique_user_date'),
    )
    
    # 关联用户表
    user = relationship("User", back_populates="mood_records")

    def __repr__(self):
        return f"<MoodTracker(user_id={self.user_id}, mood_date={self.mood_date}, mood_level={self.mood_level})>"
