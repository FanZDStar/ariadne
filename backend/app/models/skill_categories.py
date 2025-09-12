from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class SkillCategory(Base):
    __tablename__ = "skill_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, comment="分类描述")
    icon = Column(String(50), comment="分类图标")
    sort_order = Column(Integer, default=0, comment="排序序号")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联技能
    skills = relationship("Skill", back_populates="category", cascade="all, delete-orphan")