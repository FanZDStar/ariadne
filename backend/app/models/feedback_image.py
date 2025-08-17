# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.sql import func
# from app.database.session import Base

# class FeedbackImage(Base):
#     __tablename__ = "feedback_images"
    
#     image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     feedback_id = Column(Integer, ForeignKey("user_feedbacks.feedback_id"), nullable=False)
#     image_url = Column(String(500), nullable=False)
#     created_at = Column(DateTime, server_default=func.now())

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class FeedbackImage(Base):
    __tablename__ = "feedback_images"
    
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_id = Column(Integer, ForeignKey("user_feedbacks.feedback_id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    feedback = relationship("UserFeedback", back_populates="images")