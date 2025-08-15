#file:ariadne/backend/app/models/diary_image.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class DiaryImage(Base):
    __tablename__ = "diary_images"
    
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("emotional_diaries.diary_id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    diary = relationship("EmotionalDiary", back_populates="images")