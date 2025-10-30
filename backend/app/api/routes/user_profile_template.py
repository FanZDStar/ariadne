# file: ariadne/backend/app/api/routes/user_profile_template.py
"""
用户个性化档案模板API路由
包括档案CRUD、标签管理、档案预览等功能
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.user_profile_template import (
    UserProfileTemplate,
    PersonalityTagOption,
    HobbyTagOption,
    ProfessionTagOption,
    ZodiacSignOption
)
from app.schemas.user_profile_template import (
    UserProfileTemplateCreate,
    UserProfileTemplateUpdate,
    UserProfileTemplateResponse,
    TagOptionsResponse,
    PersonalityTagResponse,
    HobbyTagResponse,
    ProfessionTagResponse,
    ZodiacSignResponse,
    ProfileCompletenessResponse
)
from app.core.personalized_prompt import PersonalizedPromptService

router = APIRouter(
    prefix="/api/user-profile-template",
    tags=["user-profile-template"]
)


# ========== 标签选项相关接口 ==========

@router.get("/tag-options", response_model=TagOptionsResponse)
async def get_tag_options(db: Session = Depends(get_db)):
    """
    获取所有可用的标签选项
    包括性格标签、爱好标签、职业标签和星座选项
    """
    try:
        personality_tags = db.query(PersonalityTagOption).filter(
            PersonalityTagOption.is_active == True
        ).all()
        
        hobby_tags = db.query(HobbyTagOption).filter(
            HobbyTagOption.is_active == True
        ).all()
        
        profession_tags = db.query(ProfessionTagOption).filter(
            ProfessionTagOption.is_active == True
        ).all()
        
        zodiac_signs = db.query(ZodiacSignOption).filter(
            ZodiacSignOption.is_active == True
        ).all()
        
        return TagOptionsResponse(
            personality_tags=[PersonalityTagResponse.from_orm(t) for t in personality_tags],
            hobby_tags=[HobbyTagResponse.from_orm(t) for t in hobby_tags],
            profession_tags=[ProfessionTagResponse.from_orm(t) for t in profession_tags],
            zodiac_signs=[ZodiacSignResponse.from_orm(t) for t in zodiac_signs]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tag-options/personality", response_model=List[PersonalityTagResponse])
async def get_personality_tags(category: Optional[str] = None, db: Session = Depends(get_db)):
    """获取性格标签选项"""
    query = db.query(PersonalityTagOption).filter(PersonalityTagOption.is_active == True)
    
    if category:
        query = query.filter(PersonalityTagOption.category == category)
    
    tags = query.all()
    return [PersonalityTagResponse.from_orm(t) for t in tags]


@router.get("/tag-options/hobby", response_model=List[HobbyTagResponse])
async def get_hobby_tags(category: Optional[str] = None, db: Session = Depends(get_db)):
    """获取爱好标签选项"""
    query = db.query(HobbyTagOption).filter(HobbyTagOption.is_active == True)
    
    if category:
        query = query.filter(HobbyTagOption.category == category)
    
    tags = query.all()
    return [HobbyTagResponse.from_orm(t) for t in tags]


@router.get("/tag-options/profession", response_model=List[ProfessionTagResponse])
async def get_profession_tags(category: Optional[str] = None, db: Session = Depends(get_db)):
    """获取职业标签选项"""
    query = db.query(ProfessionTagOption).filter(ProfessionTagOption.is_active == True)
    
    if category:
        query = query.filter(ProfessionTagOption.category == category)
    
    tags = query.all()
    return [ProfessionTagResponse.from_orm(t) for t in tags]


@router.get("/tag-options/zodiac", response_model=List[ZodiacSignResponse])
async def get_zodiac_signs(db: Session = Depends(get_db)):
    """获取十二星座选项"""
    signs = db.query(ZodiacSignOption).filter(
        ZodiacSignOption.is_active == True
    ).order_by(ZodiacSignOption.id).all()
    
    return [ZodiacSignResponse.from_orm(s) for s in signs]


# ========== 用户档案CRUD接口 ==========

@router.post("/", response_model=UserProfileTemplateResponse)
async def create_or_update_profile(
    profile_data: UserProfileTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建或更新用户个性化档案
    如果已存在档案则更新，否则创建新档案
    """
    try:
        # 查找现有档案
        profile = db.query(UserProfileTemplate).filter(
            UserProfileTemplate.user_id == current_user.user_id
        ).first()
        
        if profile:
            # 更新现有档案
            update_data = profile_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(profile, key, value)
        else:
            # 创建新档案
            profile = UserProfileTemplate(
                user_id=current_user.user_id,
                **profile_data.dict()
            )
            db.add(profile)
        
        # 计算档案完整度
        profile.is_complete = _is_profile_complete(profile)
        
        db.commit()
        db.refresh(profile)
        
        return UserProfileTemplateResponse.from_orm(profile)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=UserProfileTemplateResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的个性化档案"""
    try:
        profile = db.query(UserProfileTemplate).filter(
            UserProfileTemplate.user_id == current_user.user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户档案不存在"
            )
        
        return UserProfileTemplateResponse.from_orm(profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/", response_model=UserProfileTemplateResponse)
async def update_profile(
    profile_data: UserProfileTemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """部分更新用户档案"""
    try:
        profile = db.query(UserProfileTemplate).filter(
            UserProfileTemplate.user_id == current_user.user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户档案不存在，请先创建档案"
            )
        
        # 只更新提供的字段
        update_data = profile_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(profile, key, value)
        
        profile.is_complete = _is_profile_complete(profile)
        
        db.commit()
        db.refresh(profile)
        
        return UserProfileTemplateResponse.from_orm(profile)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除用户档案"""
    try:
        profile = db.query(UserProfileTemplate).filter(
            UserProfileTemplate.user_id == current_user.user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户档案不存在"
            )
        
        db.delete(profile)
        db.commit()
        
        return {"message": "档案已删除"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ========== 档案完整度相关接口 ==========

@router.get("/completeness", response_model=ProfileCompletenessResponse)
async def get_profile_completeness(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户档案的完整度信息"""
    try:
        profile = db.query(UserProfileTemplate).filter(
            UserProfileTemplate.user_id == current_user.user_id
        ).first()
        
        if not profile:
            # 如果档案不存在，返回0%完成度
            return ProfileCompletenessResponse(
                is_complete=False,
                completion_percentage=0,
                missing_fields=[
                    "birth_date",
                    "zodiac_sign",
                    "personality_tags",
                    "hobby_tags",
                    "profession_tags"
                ],
                total_fields=5,
                filled_fields=0
            )
        
        filled_fields = _count_filled_fields(profile)
        total_fields = 5  # birth_date, zodiac_sign, 性格, 爱好, 职业
        completion_percentage = (filled_fields / total_fields) * 100
        
        missing_fields = _get_missing_fields(profile)
        
        return ProfileCompletenessResponse(
            is_complete=profile.is_complete,
            completion_percentage=completion_percentage,
            missing_fields=missing_fields,
            total_fields=total_fields,
            filled_fields=filled_fields
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== 辅助函数 ==========

def _is_profile_complete(profile: UserProfileTemplate) -> bool:
    """
    判断档案是否完整
    至少需要填写：生日、星座、性格标签或描述、爱好标签或描述、职业标签或描述
    """
    has_birth = bool(profile.birth_date)
    has_zodiac = bool(profile.zodiac_sign)
    has_personality = bool(profile.personality_tags) or bool(profile.personality_custom_description)
    has_hobby = bool(profile.hobby_tags) or bool(profile.hobby_custom_description)
    has_profession = bool(profile.profession_tags) or bool(profile.job_title) or bool(profile.profession_custom_description)
    
    return has_birth and has_zodiac and has_personality and has_hobby and has_profession


def _count_filled_fields(profile: UserProfileTemplate) -> int:
    """计算已填充的主要字段数"""
    count = 0
    if profile.birth_date:
        count += 1
    if profile.zodiac_sign:
        count += 1
    if profile.personality_tags or profile.personality_custom_description:
        count += 1
    if profile.hobby_tags or profile.hobby_custom_description:
        count += 1
    if profile.profession_tags or profile.job_title or profile.profession_custom_description:
        count += 1
    return count


def _get_missing_fields(profile: UserProfileTemplate) -> List[str]:
    """获取缺失的字段列表"""
    missing = []
    
    if not profile.birth_date:
        missing.append("birth_date")
    if not profile.zodiac_sign:
        missing.append("zodiac_sign")
    if not (profile.personality_tags or profile.personality_custom_description):
        missing.append("personality_tags")
    if not (profile.hobby_tags or profile.hobby_custom_description):
        missing.append("hobby_tags")
    if not (profile.profession_tags or profile.job_title or profile.profession_custom_description):
        missing.append("profession_tags")
    
    return missing
