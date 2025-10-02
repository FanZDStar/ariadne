#file:ariadne/backend/app/schemas/tree_hole.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.schemas.user import UserResponse

class MoodEnum(str, Enum):
    very_happy = "very_happy"
    happy = "happy"
    neutral = "neutral"
    sad = "sad"
    very_sad = "very_sad"

# 图片模型
class WhisperImageBase(BaseModel):
    image_url: str
    image_order: int = 0

class WhisperImageCreate(WhisperImageBase):
    pass

class WhisperImageResponse(WhisperImageBase):
    image_id: int
    whisper_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 悄悄话基础模型
class WhisperBase(BaseModel):
    title: Optional[str] = None
    content: str
    mood: Optional[MoodEnum] = MoodEnum.neutral
    tags: Optional[List[str]] = None
    is_anonymous: Optional[bool] = True
    anonymous_name: Optional[str] = None
    anonymous_avatar: Optional[str] = None

class WhisperCreate(WhisperBase):
    images: Optional[List[WhisperImageCreate]] = None

class WhisperUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[MoodEnum] = None
    tags: Optional[List[str]] = None
    is_anonymous: Optional[bool] = None
    anonymous_name: Optional[str] = None
    anonymous_avatar: Optional[str] = None

class WhisperResponse(WhisperBase):
    whisper_id: int
    user_id: int
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse
    images: List[WhisperImageResponse] = []
    liked: bool = False  # 添加 liked 字段
    interaction_type: Optional[str] = None  # 添加互动类型字段

    class Config:
        from_attributes = True
        # 设置字段别名，让content字段从decrypted_content属性读取
        fields = {
            'content': {'alias': 'decrypted_content'}
        }

# 评论模型
class CommentBase(BaseModel):
    content: str
    is_anonymous: Optional[bool] = True

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    comment_id: int
    whisper_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 点赞模型
class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    like_id: int
    whisper_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True