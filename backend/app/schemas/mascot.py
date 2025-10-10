"""
看板娘服装相关的数据模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MascotOutfitBase(BaseModel):
    """看板娘服装基础模型"""
    id: int
    name: str
    description: Optional[str] = None
    preview_image: str
    mascot_image: str
    star_cost: int
    is_default: bool
    is_active: bool
    sort_order: Optional[int] = None


class MascotOutfitResponse(MascotOutfitBase):
    """看板娘服装响应模型"""
    is_equipped: Optional[bool] = None
    purchased_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserCurrentOutfitResponse(MascotOutfitBase):
    """用户当前服装响应模型"""
    
    class Config:
        from_attributes = True


class SetCurrentOutfitRequest(BaseModel):
    """设置当前服装请求模型"""
    outfit_id: int


class PurchaseOutfitResponse(BaseModel):
    """购买服装响应模型"""
    message: str
    success: bool = True


class MascotOutfitListResponse(BaseModel):
    """服装列表响应模型"""
    outfits: list[MascotOutfitResponse]
    total_count: int
