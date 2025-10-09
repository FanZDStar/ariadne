"""
星星积分系统相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class UserStarPoints(Base):
    """用户星星积分表"""
    __tablename__ = "user_star_points"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True, comment="用户ID")
    current_points = Column(Integer, nullable=False, default=10, comment="当前星星积分")
    total_earned = Column(Integer, nullable=False, default=10, comment="总获得积分")
    total_spent = Column(Integer, nullable=False, default=0, comment="总消费积分")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="star_points")
    # 通过user_id关联到日志记录
    logs = relationship("StarPointLog", foreign_keys="StarPointLog.user_id", 
                       primaryjoin="UserStarPoints.user_id == StarPointLog.user_id",
                       overlaps="star_logs", cascade="all, delete-orphan")


class StarPointLog(Base):
    """星星积分变动日志表"""
    __tablename__ = "star_point_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    action_type = Column(String(50), nullable=False, index=True, comment="行为类型")
    points_change = Column(Integer, nullable=False, comment="积分变化(正数为获得，负数为消费)")
    description = Column(String(255), nullable=False, comment="描述信息")
    source_id = Column(String(100), nullable=True, comment="来源ID(如日记ID、会话ID等)")
    source_type = Column(String(50), nullable=True, comment="来源类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="star_logs", overlaps="logs")


class DailyStarLimits(Base):
    """每日星星积分限制表"""
    __tablename__ = "daily_star_limits"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    date = Column(Date, nullable=False, comment="日期")
    
    # 各种行为的每日完成状态
    daily_login = Column(Boolean, default=False, comment="每日登录(1星)")
    mood_tracking = Column(Boolean, default=False, comment="晴雨表打卡(1星)")
    diary_count = Column(Integer, default=0, comment="日记篇数(第1篇3星,第2-3篇各1星)")
    background_change = Column(Boolean, default=False, comment="背景修改(1星)")
    emotion_chat_count = Column(Integer, default=0, comment="情感对话次数")
    emotion_chat_points = Column(Integer, default=0, comment="情感对话获得积分")
    skill_training = Column(Boolean, default=False, comment="技能综合训练(1星)")
    relationship_assessment = Column(Boolean, default=False, comment="关系健康评估(2星)")
    personalized_advice = Column(Boolean, default=False, comment="个性化建议(2星)")
    ai_scenario_training = Column(Boolean, default=False, comment="AI情景模拟训练(2星)")
    protection_training = Column(Boolean, default=False, comment="防护技能训练(2星)")
    tree_hole_interaction_count = Column(Integer, default=0, comment="树洞互动次数")
    tree_hole_whisper = Column(Boolean, default=False, comment="发表悄悄话(2星)")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
    
    # 关系
    user = relationship("User", back_populates="daily_star_limits")
