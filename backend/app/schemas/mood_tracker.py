from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field

class MoodTrackerCreate(BaseModel):
    """创建心情记录"""
    mood_level: int = Field(..., ge=1, le=5, description="心情档位，1-5档")
    mood_date: Optional[date] = Field(None, description="心情记录日期，默认为今天")

class MoodTrackerResponse(BaseModel):
    """心情记录响应"""
    id: int
    user_id: int
    mood_date: date
    mood_level: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MoodTrackerWithStarResponse(BaseModel):
    """包含星星奖励的心情记录响应"""
    id: int
    user_id: int
    mood_date: date
    mood_level: int
    created_at: datetime
    updated_at: datetime
    star_awarded: bool = False
    star_points: int = 0
    star_message: str = "心情记录成功 💫"

class WeeklyMoodResponse(BaseModel):
    """7天心情记录响应"""
    dates: List[str] = Field(..., description="7天的日期列表")
    levels: List[Optional[int]] = Field(..., description="对应的心情档位，None表示未记录")
