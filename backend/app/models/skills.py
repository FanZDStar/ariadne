from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="技能名称")
    brief = Column(String(200), comment="技能简介")
    description = Column(Text, comment="技能详细描述")
    difficulty = Column(String(20), default='basic', comment="难度级别: basic/intermediate/advanced")
    estimated_time = Column(Integer, comment="预估学习时间(分钟)")
    learner_count = Column(Integer, default=0, comment="学习人数")
    
    # 技能内容
    objectives = Column(JSON, comment="学习目标列表")
    key_points = Column(JSON, comment="核心要点")
    practice_steps = Column(JSON, comment="实践步骤")
    scenarios = Column(JSON, comment="应用场景")
    tags = Column(JSON, comment="技能标签")
    
    # 分类关联
    category_id = Column(Integer, ForeignKey('skill_categories.id'), nullable=False)
    category = relationship("SkillCategory", back_populates="skills")
    
    # 状态管理
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序序号")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联用户学习进度
    user_progresses = relationship("UserSkillProgress", back_populates="skill", cascade="all, delete-orphan")