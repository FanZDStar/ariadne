# file: ariadne/backend/app/models/tree_hole_images.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class TreeHoleWhisperImage(Base):
    __tablename__ = "tree_hole_whisper_images"
    
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    whisper = relationship("TreeHoleWhisper", back_populates="images")
