# backend/app/schemas/user_diary_backgrounds.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserDiaryBackgroundBase(BaseModel):
    """用户日记背景图片基础模型"""
    pass

class UserDiaryBackgroundResponse(UserDiaryBackgroundBase):
    """用户日记背景图片响应模型"""
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    upload_time: datetime
    is_active: bool
    url: str
    
    class Config:
        from_attributes = True

class UserDiaryBackgroundUpdate(UserDiaryBackgroundBase):
    """用户日记背景图片更新模型"""
    is_active: Optional[bool] = None

class UserDiaryBackgroundWithStarResponse(UserDiaryBackgroundResponse):
    """用户日记背景图片响应模型（包含星星奖励信息）"""
    star_awarded: bool = False
    star_points: int = 0
    star_message: str = ""