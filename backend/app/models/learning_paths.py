from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="学习路径名称")
    description = Column(Text, comment="学习路径描述")
    level = Column(String(20), comment="适用水平: beginner/intermediate/advanced")
    estimated_duration = Column(String(50), comment="预估完成时间")
    
    # 路径内容
    skill_sequence = Column(JSON, comment="技能学习序列")
    milestones = Column(JSON, comment="里程碑节点")
    prerequisites = Column(JSON, comment="前置要求")
    
    # 状态管理
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序序号")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联用户学习路径进度
    user_progresses = relationship("UserLearningPathProgress", back_populates="learning_path", cascade="all, delete-orphan")