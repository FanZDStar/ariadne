#file:ariadne/backend/app/schemas/diary.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MoodEnum(str, Enum):
    very_happy = "very_happy"
    happy = "happy"
    neutral = "neutral"
    sad = "sad"
    very_sad = "very_sad"

class DiaryBase(BaseModel):
    title: str
    content: str
    mood: MoodEnum
    is_private: bool = True

class DiaryCreate(DiaryBase):
    pass

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[MoodEnum] = None
    is_private: Optional[bool] = None

class DiaryResponse(DiaryBase):
    diary_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True