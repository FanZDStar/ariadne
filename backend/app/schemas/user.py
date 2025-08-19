from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re

# 用户名和密码的正则表达式
USERNAME_REGEX = r"^(?=[a-zA-Z0-9]{2,15}$)(?!^[0-9]+$)(?!^[a-zA-Z]+$)"
# 更新后的密码正则表达式
PASSWORD_REGEX = r"^(((?=.*[a-zA-Z])(?=.*[0-9]))|((?=.*[a-zA-Z])(?=.*[!]))|((?=.*[0-9])(?=.*[!])))[a-zA-Z0-9!]{6,15}$"

class UserBase(BaseModel):
    username: str = Field(..., max_length=15)
    email: Optional[str] = None
    nickname: Optional[str] = Field(None, max_length=6)
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @validator('username')
    def validate_username(cls, v):
        if not re.match(USERNAME_REGEX, v):
            raise ValueError('用户名必须是2-15位的大小写字母和数字的组合')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError('密码必须是6-15位的大小写字母、数字和英文感叹号的两种或以上组合')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if v and not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('邮箱格式不正确')
        return v

class UserLogin(BaseModel):
    username: str # This can be username or email
    password: str

class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=6)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class UserUpdateEmail(BaseModel):
    email: str

    @validator('email')
    def validate_email(cls, v):
        if v and not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('邮箱格式不正确')
        return v

class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str

    @validator('new_password')
    def validate_password(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError('密码必须是6-15位的大小写字母、数字和英文感叹号的两种或以上组合')
        return v