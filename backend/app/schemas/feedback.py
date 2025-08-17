from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 反馈图片基础模型
class FeedbackImageBase(BaseModel):
    image_url: str

class FeedbackImageCreate(FeedbackImageBase):
    pass

class FeedbackImageResponse(FeedbackImageBase):
    image_id: int
    feedback_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 反馈基础模型
class FeedbackBase(BaseModel):
    title: str
    content: str
    contact_info: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    images: List[FeedbackImageCreate] = []

class FeedbackUpdate(BaseModel):
    status: Optional[str] = None

class FeedbackResponse(FeedbackBase):
    feedback_id: int
    user_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime
    images: List[FeedbackImageResponse] = []
    
    class Config:
        from_attributes = True