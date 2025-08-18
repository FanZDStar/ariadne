from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class UserFeedback(Base):
    __tablename__ = "user_feedbacks"
    
    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    contact_info = Column(String(255), nullable=True)
    status = Column(Enum("pending", "processing", "resolved", "closed"), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联图片
    images = relationship("FeedbackImage", back_populates="feedback")