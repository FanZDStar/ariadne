"""
每日互动奖励记录模型（评论+发布悄悄话）
"""
from sqlalchemy import Column, Integer, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.session import Base


class DailyCommentReward(Base):
    """每日互动奖励记录表"""
    __tablename__ = "daily_comment_rewards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    comment_date = Column(Date, nullable=False, comment="日期", index=True)
    comment_count = Column(Integer, nullable=False, default=0, comment="当日评论次数")
    comment_rewards_earned = Column(Integer, nullable=False, default=0, comment="当日评论获得的水滴奖励")
    whisper_count = Column(Integer, nullable=False, default=0, comment="当日发布悄悄话次数")
    whisper_rewards_earned = Column(Integer, nullable=False, default=0, comment="当日发布悄悄话获得的水滴奖励")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
