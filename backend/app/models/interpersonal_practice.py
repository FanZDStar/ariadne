from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum

class PracticeType(str, enum.Enum):
    communication = "communication"
    emotional_expression = "emotional_expression"  
    relationship_building = "relationship_building"
    special_scenarios = "special_scenarios"

class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class InterpersonalPracticeSession(Base):
    """人际智慧练习会话模型"""
    __tablename__ = "interpersonal_practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    scenario_id = Column(String(50), nullable=False)
    scenario_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    messages = Column(JSON, nullable=False)  # 完整对话记录
    practice_type = Column(Enum(PracticeType), nullable=False, default=PracticeType.communication)
    difficulty_level = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.beginner)
    session_duration = Column(Integer, nullable=True)  # 会话时长(秒)
    message_count = Column(Integer, nullable=False, default=0)
    quality_score = Column(Numeric(3, 2), nullable=True)  # 练习质量评分(0-10)
    ai_feedback = Column(Text, nullable=True)
    improvement_suggestions = Column(JSON, nullable=True)
    skills_practiced = Column(JSON, nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    is_favorite = Column(Boolean, nullable=False, default=False)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # 关联关系
    user = relationship("User", back_populates="interpersonal_practice_sessions")
