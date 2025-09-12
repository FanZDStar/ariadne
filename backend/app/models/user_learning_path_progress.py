from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserLearningPathProgress(Base):
    __tablename__ = "user_learning_path_progress"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'), nullable=False)
    
    # 路径进度
    status = Column(String(20), default='not_started', comment="状态: not_started/in_progress/completed/paused")
    progress = Column(Float, default=0.0, comment="完成进度 0-100")
    current_step = Column(Integer, default=0, comment="当前步骤")
    
    # 进度详情
    completed_skills = Column(JSON, comment="已完成的技能ID列表")
    milestone_progress = Column(JSON, comment="里程碑完成状态")
    
    # 时间记录
    started_at = Column(DateTime, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
    last_activity_at = Column(DateTime, comment="最后活动时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", backref="learning_path_progresses")
    learning_path = relationship("LearningPath", back_populates="user_progresses")