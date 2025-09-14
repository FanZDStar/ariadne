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

class WeeklyMoodResponse(BaseModel):
    """7天心情记录响应"""
    dates: List[str] = Field(..., description="7天的日期列表")
    levels: List[Optional[int]] = Field(..., description="对应的心情档位，None表示未记录")
