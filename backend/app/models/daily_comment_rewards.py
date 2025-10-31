"""
每日评论奖励记录模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base


class DailyCommentRewards(Base):
    """每日评论奖励记录表"""
    __tablename__ = 'daily_comment_rewards'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    reward_date = Column(Date, nullable=False, index=True, comment='奖励日期')
    comment_count = Column(Integer, default=0, nullable=False, comment='当日已奖励评论数')
    water_drops_earned = Column(Integer, default=0, nullable=False, comment='当日获得的水滴数')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<DailyCommentRewards(user_id={self.user_id}, date={self.reward_date}, count={self.comment_count})>"
