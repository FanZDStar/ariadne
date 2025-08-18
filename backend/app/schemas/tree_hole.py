#file:ariadne/backend/app/schemas/tree_hole.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.user import UserResponse

# 悄悄话基础模型
class WhisperBase(BaseModel):
    content: str
    is_anonymous: Optional[bool] = True

class WhisperCreate(WhisperBase):
    pass

class WhisperUpdate(BaseModel):
    content: Optional[str] = None
    is_anonymous: Optional[bool] = None

class WhisperResponse(WhisperBase):
    whisper_id: int
    user_id: int
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse
    liked: bool = False  # 添加 liked 字段

    class Config:
        from_attributes = True

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