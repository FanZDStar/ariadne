"""
看板娘好感度系统相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey, UniqueConstraint, DECIMAL, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class UserMascotAffection(Base):
    """用户看板娘好感度表"""
    __tablename__ = "user_mascot_affection"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True, comment="用户ID")
    current_affection = Column(Integer, nullable=False, default=0, comment="当前好感度值")
    total_earned_affection = Column(Integer, nullable=False, default=0, comment="累计获得好感度")
    current_level = Column(Integer, nullable=False, default=1, comment="当前好感度等级")
    level_progress = Column(DECIMAL(5, 2), nullable=False, default=0.00, comment="当前等级进度百分比")
    next_level_required = Column(Integer, nullable=False, default=100, comment="升级到下一等级所需好感度")
    last_interaction_at = Column(DateTime(timezone=True), nullable=True, comment="最后互动时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="mascot_affection")
    # 通过user_id关联到日志记录
    logs = relationship("MascotAffectionLog", foreign_keys="MascotAffectionLog.user_id", 
                       primaryjoin="UserMascotAffection.user_id == MascotAffectionLog.user_id",
                       overlaps="affection_logs", cascade="all, delete-orphan")


class MascotAffectionLog(Base):
    """好感度变化记录表"""
    __tablename__ = "mascot_affection_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    action_type = Column(String(50), nullable=False, index=True, comment="行为类型")
    affection_change = Column(Integer, nullable=False, comment="好感度变化值(正数为增加，负数为减少)")
    before_affection = Column(Integer, nullable=False, comment="变化前好感度")
    after_affection = Column(Integer, nullable=False, comment="变化后好感度")
    before_level = Column(Integer, nullable=False, comment="变化前等级")
    after_level = Column(Integer, nullable=False, comment="变化后等级")
    is_level_up = Column(Boolean, nullable=False, default=False, comment="是否升级")
    description = Column(String(255), nullable=False, comment="描述信息")
    source_id = Column(String(100), nullable=True, comment="来源ID(如订单ID、活动ID等)")
    source_type = Column(String(50), nullable=True, comment="来源类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="affection_logs", overlaps="logs")


class MascotAffectionLevel(Base):
    """好感度等级配置表"""
    __tablename__ = "mascot_affection_levels"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(Integer, nullable=False, unique=True, comment="等级")
    level_name = Column(String(50), nullable=False, comment="等级名称")
    required_affection = Column(Integer, nullable=False, comment="达到该等级所需好感度")
    level_description = Column(String(255), nullable=True, comment="等级描述")
    unlock_rewards = Column(JSON, nullable=True, comment="解锁奖励(动作、道具等)")
    special_actions = Column(JSON, nullable=True, comment="特殊动作列表")
    random_drop_config = Column(JSON, nullable=True, comment="随机掉落配置")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")


class DailyAffectionLimits(Base):
    """每日好感度限制表"""
    __tablename__ = "daily_affection_limits"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    date = Column(Date, nullable=False, comment="日期")
    
    # 各种行为的每日完成状态
    daily_login = Column(Boolean, default=False, comment="每日登录好感度")
    outfit_purchase_count = Column(Integer, default=0, comment="服装购买次数")
    outfit_purchase_affection = Column(Integer, default=0, comment="服装购买获得好感度")
    emotion_chat_count = Column(Integer, default=0, comment="情感对话次数")
    emotion_chat_affection = Column(Integer, default=0, comment="情感对话获得好感度")
    diary_complete = Column(Boolean, default=False, comment="完成日记好感度")
    mood_tracking = Column(Boolean, default=False, comment="心情记录好感度")
    total_daily_affection = Column(Integer, default=0, comment="当日总获得好感度")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 联合唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date_affection'),
    )
    
    # 关系
    user = relationship("User", back_populates="daily_affection_limits")


class UserAffectionRewards(Base):
    """用户好感度奖励记录表"""
    __tablename__ = "user_affection_rewards"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    reward_type = Column(String(50), nullable=False, comment="奖励类型(level_reward/random_drop)")
    reward_category = Column(String(50), nullable=False, comment="奖励分类(action/points/water_drops/outfit等)")
    reward_content = Column(JSON, nullable=False, comment="奖励内容详情")
    reward_value = Column(Integer, nullable=True, comment="奖励数值(如积分数、水滴数)")
    trigger_level = Column(Integer, nullable=True, comment="触发等级(等级奖励时使用)")
    trigger_action = Column(String(50), nullable=True, comment="触发动作(随机掉落时使用)")
    is_claimed = Column(Boolean, nullable=False, default=False, comment="是否已领取")
    claimed_at = Column(DateTime(timezone=True), nullable=True, comment="领取时间")
    expires_at = Column(DateTime(timezone=True), nullable=True, comment="过期时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="affection_rewards")
