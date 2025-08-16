# #file:ariadne/backend/app/models/emotional_diary.py
# from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, Boolean, ForeignKey
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from app.database.session import Base

# class EmotionalDiary(Base):
#     __tablename__ = "emotional_diaries"
    
#     diary_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     title = Column(String(255), nullable=False)
#     content = Column(Text, nullable=False)
#     mood = Column(Enum("very_happy", "happy", "neutral", "sad", "very_sad"), nullable=False)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
#     is_private = Column(Boolean, default=True)
#     image_count = Column(Integer, default=0)
    
#     # 关联图片
#     images = relationship("DiaryImage", back_populates="diary")

#file:ariadne/backend/app/models/emotional_diary.py
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, Boolean, ForeignKey, func, case
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
    
    # # 定义心情分数的映射（用于类方法）
    # MOOD_SCORES = {
    #     "very_happy": 5,
    #     "happy": 4,
    #     "neutral": 3,
    #     "sad": 2,
    #     "very_sad": 1
    # }
    
    @classmethod
    def get_mood_score_case(cls):
        """返回SQL CASE表达式来计算心情分数"""
        return case(
            (cls.mood == "very_happy", 5),
            (cls.mood == "happy", 4),
            (cls.mood == "neutral", 3),
            (cls.mood == "sad", 2),
            (cls.mood == "very_sad", 1),
            else_=3  # 默认值
        )
    
    
    # 保留实例方法用于其他用途
    def get_mood_score(self):
        """获取单个日记的心情分数"""
        mood_scores = {
            "very_happy": 5,
            "happy": 4,
            "neutral": 3,
            "sad": 2,
            "very_sad": 1
        }
        return mood_scores.get(self.mood, 3)