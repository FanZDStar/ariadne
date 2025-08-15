#file:ariadne/backend/app/models/emotional_diary.py
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class EmotionalDiary(Base):
    __tablename__ = "emotional_diaries"
    
    diary_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    mood = Column(Enum("very_happy", "happy", "neutral", "sad", "very_sad"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_private = Column(Boolean, default=True)
    image_count = Column(Integer, default=0)
    
    # 关联图片
    images = relationship("DiaryImage", back_populates="diary")