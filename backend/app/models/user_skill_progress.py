from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    
    # 学习状态
    status = Column(String(20), default='new', comment="状态: new/learning/mastered")
    progress = Column(Float, default=0.0, comment="学习进度 0-100")
    
    # 学习统计
    practice_count = Column(Integer, default=0, comment="练习次数")
    correct_rate = Column(Float, default=0.0, comment="正确率")
    total_time_spent = Column(Integer, default=0, comment="总学习时间(分钟)")
    
    # 时间记录
    started_at = Column(DateTime, comment="开始学习时间")
    last_practiced_at = Column(DateTime, comment="最后练习时间")
    mastered_at = Column(DateTime, comment="掌握时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", backref="skill_progresses")
    skill = relationship("Skill", back_populates="user_progresses")