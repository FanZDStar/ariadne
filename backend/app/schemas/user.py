#file:ariadne/backend/app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 用户基础模型
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    bio: Optional[str] = None

# 用户创建模型
class UserCreate(UserBase):
    password: str

# 用户登录模型
class UserLogin(BaseModel):
    username: str
    password: str

# 用户响应模型
class UserResponse(UserBase):
    user_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Token模型
class Token(BaseModel):
    access_token: str
    token_type: str

# Token数据模型
class TokenData(BaseModel):
    username: Optional[str] = None