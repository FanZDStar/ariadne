from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class InterpersonalPracticeSession(Base):
    __tablename__ = "interpersonal_practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    session_title = Column(String(200), nullable=False)
    
    # 练习场景信息
    practice_scenario = Column(String(50), nullable=False)  # 场景类型
    practice_scenario_name = Column(String(100), nullable=False)  # 场景名称
    scenario_description = Column(Text)  # 场景描述
    
    # 对话内容
    messages = Column(JSON, nullable=False)  # 存储对话消息数组
    total_messages = Column(Integer, default=0)  # 消息总数
    
    # 练习统计
    practice_duration = Column(Integer, default=0)  # 练习时长(秒)
    start_time = Column(DateTime, server_default=func.now())
    end_time = Column(DateTime)
    
    # 质量评估
    practice_quality_score = Column(Float)  # 练习质量评分(0-100)
    ai_feedback = Column(Text)  # AI反馈
    strengths = Column(JSON)  # 优势点数组
    improvements = Column(JSON)  # 改进建议数组
    
    # 技能标签
    skills_practiced = Column(JSON)  # 练习的技能标签数组
    skill_improvements = Column(JSON)  # 技能改进记录
    
    # 元数据
    practice_type = Column(String(50), default='ai_dialog')  # 练习类型
    difficulty_level = Column(String(20))  # 难度等级
    completion_status = Column(String(20), default='completed')  # 完成状态
    
    # 用户交互
    is_favorite = Column(Boolean, default=False)  # 是否收藏
    user_rating = Column(Integer)  # 用户评分(1-5)
    user_notes = Column(Text)  # 用户笔记
    
    # 系统字段
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    # 关联关系
    user = relationship("User", back_populates="interpersonal_practice_sessions")