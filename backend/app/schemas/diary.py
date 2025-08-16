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

class DiaryImageBase(BaseModel):
    image_url: str
    image_order: int = 0

class DiaryImageCreate(DiaryImageBase):
    pass

class DiaryImageResponse(DiaryImageBase):
    image_id: int
    diary_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DiaryBase(BaseModel):
    title: str
    content: str
    mood: MoodEnum
    is_private: bool = True

class DiaryCreate(DiaryBase):
    images: List[DiaryImageCreate] = []

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[MoodEnum] = None
    is_private: Optional[bool] = None
    images: Optional[List[DiaryImageCreate]] = None

class DiaryResponse(DiaryBase):
    diary_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    images: List[DiaryImageResponse] = []
    image_count: int = 0
    
    class Config:
        from_attributes = True