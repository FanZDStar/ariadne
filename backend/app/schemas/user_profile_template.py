# file: ariadne/backend/app/schemas/user_profile_template.py
"""
用户个性化档案Pydantic schema
用于API请求/响应的数据验证和序列化
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ZodiacSignResponse(BaseModel):
    """星座选项响应"""
    id: int
    sign_name: str
    date_range: Optional[str]
    emoji: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class PersonalityTagResponse(BaseModel):
    """性格标签选项响应"""
    id: int
    tag_name: str
    description: Optional[str]
    category: Optional[str]
    
    class Config:
        from_attributes = True


class HobbyTagResponse(BaseModel):
    """爱好标签选项响应"""
    id: int
    tag_name: str
    description: Optional[str]
    category: Optional[str]
    emoji: Optional[str]
    
    class Config:
        from_attributes = True


class ProfessionTagResponse(BaseModel):
    """职业标签选项响应"""
    id: int
    tag_name: str
    description: Optional[str]
    category: Optional[str]
    related_skills: Optional[List[str]]
    
    class Config:
        from_attributes = True


# ========== 用户档案模板相关 Schema ==========

class UserProfileTemplateCreate(BaseModel):
    """创建/更新用户档案"""
    gender: Optional[str] = Field(None, description="性别 (男/女/其他)")
    birth_date: Optional[str] = Field(None, description="生日 (格式: YYYY-MM-DD)")
    zodiac_sign: Optional[str] = Field(None, description="星座")
    
    personality_tags: Optional[List[str]] = Field(default_factory=list, description="性格标签列表")
    personality_custom_description: Optional[str] = Field(None, description="自定义性格描述")
    
    hobby_tags: Optional[List[str]] = Field(default_factory=list, description="爱好标签列表")
    hobby_custom_description: Optional[str] = Field(None, description="自定义爱好描述")
    
    profession_tags: Optional[List[str]] = Field(default_factory=list, description="职业标签列表")
    profession_custom_description: Optional[str] = Field(None, description="自定义职业描述")
    job_title: Optional[str] = Field(None, description="具体工作职位")
    
    life_stage: Optional[str] = Field(None, description="生活阶段")
    location: Optional[str] = Field(None, description="城市/地区")
    personal_motto: Optional[str] = Field(None, description="个人座右铭")
    main_focus_areas: Optional[List[str]] = Field(default_factory=list, description="主要关注领域")


class UserProfileTemplateUpdate(BaseModel):
    """更新用户档案（支持部分更新）"""
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    zodiac_sign: Optional[str] = None
    personality_tags: Optional[List[str]] = None
    personality_custom_description: Optional[str] = None
    hobby_tags: Optional[List[str]] = None
    hobby_custom_description: Optional[str] = None
    profession_tags: Optional[List[str]] = None
    profession_custom_description: Optional[str] = None
    job_title: Optional[str] = None
    life_stage: Optional[str] = None
    location: Optional[str] = None
    personal_motto: Optional[str] = None
    main_focus_areas: Optional[List[str]] = None


class UserProfileTemplateResponse(BaseModel):
    """用户档案响应"""
    id: int
    user_id: int
    
    gender: Optional[str]
    birth_date: Optional[str]
    zodiac_sign: Optional[str]
    
    personality_tags: Optional[List[str]]
    personality_custom_description: Optional[str]
    
    hobby_tags: Optional[List[str]]
    hobby_custom_description: Optional[str]
    
    profession_tags: Optional[List[str]]
    profession_custom_description: Optional[str]
    job_title: Optional[str]
    
    life_stage: Optional[str]
    location: Optional[str]
    personal_motto: Optional[str]
    main_focus_areas: Optional[List[str]]
    
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileSummary(BaseModel):
    """用户档案简化摘要（用于AI prompt）"""
    gender: Optional[str]
    birth_date: Optional[str]
    zodiac_sign: Optional[str]
    personality_summary: str
    hobby_summary: str
    profession_summary: str
    location: Optional[str]
    personal_motto: Optional[str]
    
    class Config:
        from_attributes = True


# ========== 标签管理 Schema ==========

class TagOptionsResponse(BaseModel):
    """所有标签选项响应"""
    personality_tags: List[PersonalityTagResponse]
    hobby_tags: List[HobbyTagResponse]
    profession_tags: List[ProfessionTagResponse]
    zodiac_signs: List[ZodiacSignResponse]


# ========== 档案完成度 Schema ==========

class ProfileCompletenessResponse(BaseModel):
    """档案完成度响应"""
    is_complete: bool
    completion_percentage: float  # 0-100
    missing_fields: List[str]  # 缺少的字段
    total_fields: int
    filled_fields: int
