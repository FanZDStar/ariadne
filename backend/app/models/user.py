#file:ariadne/backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True)
    avatar_url = Column(String(255))
    nickname = Column(String(100))
    bio = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # 添加聊天记录关联
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    # whispers = relationship("TreeHoleWhisper", back_populates="user")  # 暂时注释避免初始化问题
    
    # 添加危机预警关联
    crisis_warnings = relationship("CrisisWarning", back_populates="user", cascade="all, delete-orphan")
    
    # 添加风险评估报告关联
    risk_reports = relationship("RiskAssessmentReport", back_populates="user", cascade="all, delete-orphan")
    
    # 添加关系健康评估报告关联
    relationship_reports = relationship("RelationshipAssessmentReport", back_populates="user", cascade="all, delete-orphan")
    
    # 添加心情记录关联
    mood_records = relationship("MoodTracker", back_populates="user", cascade="all, delete-orphan")
    
    # 添加日记背景图片关联
    diary_backgrounds = relationship("UserDiaryBackground", back_populates="user", cascade="all, delete-orphan")