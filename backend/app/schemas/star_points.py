"""
星星积分系统的Pydantic模式
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class UserStarPointsResponse(BaseModel):
    """用户积分响应模式"""
    user_id: int
    current_points: int
    total_earned: int
    total_spent: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StarPointLogResponse(BaseModel):
    """积分日志响应模式"""
    id: int
    user_id: int
    action_type: str
    points_change: int
    description: str
    source_id: Optional[str] = None
    source_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AwardPointsRequest(BaseModel):
    """奖励积分请求模式"""
    action_type: str = Field(..., description="行为类型")
    source_id: Optional[str] = Field(None, description="来源ID")
    source_type: Optional[str] = Field(None, description="来源类型")


class SpendPointsRequest(BaseModel):
    """消费积分请求模式"""
    points: int = Field(..., gt=0, description="消费积分数量")
    description: str = Field(..., description="消费描述")
    source_id: Optional[str] = Field(None, description="来源ID")
    source_type: Optional[str] = Field(None, description="来源类型")


class DailyStarLimitsResponse(BaseModel):
    """每日积分限制响应模式"""
    user_id: int
    date: date
    daily_login: bool
    mood_tracking: bool
    diary_count: int
    background_change: bool
    emotion_chat_count: int
    emotion_chat_points: int
    skill_training: bool
    relationship_assessment: bool
    personalized_advice: bool
    ai_scenario_training: bool
    protection_training: bool
    tree_hole_interaction_count: int
    tree_hole_whisper: bool

    class Config:
        from_attributes = True
