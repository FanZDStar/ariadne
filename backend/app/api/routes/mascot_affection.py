"""
看板娘好感度系统API路由示例
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.session import get_db
from app.services.mascot_affection_service import MascotAffectionService
from app.utils.affection_types import MascotAffectionAction, AffectionSourceType
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


class AffectionResponse(BaseModel):
    """好感度响应模型"""
    current_affection: int
    total_earned_affection: int
    current_level: int
    level_name: str
    level_progress: float
    next_level_required: int
    next_level_name: str
    last_interaction_at: str = None


class AffectionRewardResponse(BaseModel):
    """好感度奖励响应模型"""
    rewarded: bool
    message: str
    affection_awarded: int
    level_up: bool = False
    old_level: int = 1
    new_level: int = 1


class AffectionLogResponse(BaseModel):
    """好感度日志响应模型"""
    id: int
    action_type: str
    affection_change: int
    before_affection: int
    after_affection: int
    before_level: int
    after_level: int
    is_level_up: bool
    description: str
    created_at: str


@router.get("/affection/summary", response_model=AffectionResponse)
async def get_affection_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户好感度概览"""
    affection_service = MascotAffectionService(db)
    summary = affection_service.get_user_affection_summary(current_user.user_id)
    
    return AffectionResponse(
        current_affection=summary["current_affection"],
        total_earned_affection=summary["total_earned_affection"],
        current_level=summary["current_level"],
        level_name=summary["level_name"],
        level_progress=summary["level_progress"],
        next_level_required=summary["next_level_required"],
        next_level_name=summary["next_level_name"],
        last_interaction_at=summary["last_interaction_at"].isoformat() if summary["last_interaction_at"] else None
    )


@router.get("/affection/logs", response_model=List[AffectionLogResponse])
async def get_affection_logs(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户好感度变动记录"""
    affection_service = MascotAffectionService(db)
    logs = affection_service.get_affection_logs(current_user.user_id, limit)
    
    return [
        AffectionLogResponse(
            id=log.id,
            action_type=log.action_type,
            affection_change=log.affection_change,
            before_affection=log.before_affection,
            after_affection=log.after_affection,
            before_level=log.before_level,
            after_level=log.after_level,
            is_level_up=log.is_level_up,
            description=log.description,
            created_at=log.created_at.isoformat()
        )
        for log in logs
    ]


@router.post("/affection/daily-login", response_model=AffectionRewardResponse)
async def award_daily_login_affection(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励每日登录好感度"""
    affection_service = MascotAffectionService(db)
    
    result = affection_service.award_affection(
        user_id=current_user.user_id,
        action=MascotAffectionAction.DAILY_LOGIN,
        source_type=AffectionSourceType.LOGIN
    )
    
    return AffectionRewardResponse(
        rewarded=result.rewarded,
        message=result.message,
        affection_awarded=result.affection_awarded,
        level_up=result.level_up,
        old_level=result.old_level,
        new_level=result.new_level
    )


@router.post("/affection/emotion-chat", response_model=AffectionRewardResponse)
async def award_emotion_chat_affection(
    chat_session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励情感对话好感度"""
    affection_service = MascotAffectionService(db)
    
    result = affection_service.award_affection(
        user_id=current_user.user_id,
        action=MascotAffectionAction.EMOTION_CHAT,
        source_id=chat_session_id,
        source_type=AffectionSourceType.CHAT
    )
    
    return AffectionRewardResponse(
        rewarded=result.rewarded,
        message=result.message,
        affection_awarded=result.affection_awarded,
        level_up=result.level_up,
        old_level=result.old_level,
        new_level=result.new_level
    )


@router.post("/affection/diary-complete", response_model=AffectionRewardResponse)  
async def award_diary_complete_affection(
    diary_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励完成日记好感度"""
    affection_service = MascotAffectionService(db)
    
    result = affection_service.award_affection(
        user_id=current_user.user_id,
        action=MascotAffectionAction.DIARY_COMPLETE,
        source_id=diary_id,
        source_type=AffectionSourceType.DIARY
    )
    
    return AffectionRewardResponse(
        rewarded=result.rewarded,
        message=result.message,
        affection_awarded=result.affection_awarded,
        level_up=result.level_up,
        old_level=result.old_level,
        new_level=result.new_level
    )


@router.post("/affection/mood-tracking", response_model=AffectionRewardResponse)
async def award_mood_tracking_affection(
    mood_record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励心情记录好感度"""
    affection_service = MascotAffectionService(db)
    
    result = affection_service.award_affection(
        user_id=current_user.user_id,
        action=MascotAffectionAction.MOOD_TRACKING,
        source_id=mood_record_id,
        source_type=AffectionSourceType.MOOD
    )
    
    return AffectionRewardResponse(
        rewarded=result.rewarded,
        message=result.message,
        affection_awarded=result.affection_awarded,
        level_up=result.level_up,
        old_level=result.old_level,
        new_level=result.new_level
    )


@router.post("/affection/outfit-purchase", response_model=AffectionRewardResponse)
async def award_outfit_purchase_affection(
    outfit_id: str,
    star_cost: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励购买服装好感度"""
    affection_service = MascotAffectionService(db)
    
    result = affection_service.award_outfit_purchase_affection(
        user_id=current_user.user_id,
        star_cost=star_cost,
        source_id=outfit_id
    )
    
    return AffectionRewardResponse(
        rewarded=result.rewarded,
        message=result.message,
        affection_awarded=result.affection_awarded,
        level_up=result.level_up,
        old_level=result.old_level,
        new_level=result.new_level
    )


@router.get("/affection/rewards")
async def get_unclaimed_rewards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户未领取的好感度奖励"""
    affection_service = MascotAffectionService(db)
    rewards = affection_service.get_unclaimed_rewards(current_user.user_id)
    
    return [
        {
            "id": reward.id,
            "reward_type": reward.reward_type,
            "reward_category": reward.reward_category,
            "reward_content": reward.reward_content,
            "reward_value": reward.reward_value,
            "trigger_level": reward.trigger_level,
            "created_at": reward.created_at.isoformat()
        }
        for reward in rewards
    ]


@router.post("/affection/rewards/{reward_id}/claim")
async def claim_affection_reward(
    reward_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """领取好感度奖励"""
    affection_service = MascotAffectionService(db)
    
    success = affection_service.claim_reward(current_user.user_id, reward_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="奖励不存在或已被领取"
        )
    
    return {"message": "奖励领取成功！"}





@router.get("/affection/levels")
async def get_affection_levels(db: Session = Depends(get_db)):
    """获取所有好感度等级配置"""
    from app.models.mascot_affection import MascotAffectionLevel
    
    levels = db.query(MascotAffectionLevel).filter(
        MascotAffectionLevel.is_active == True
    ).order_by(MascotAffectionLevel.level).all()
    
    return [
        {
            "level": level.level,
            "level_name": level.level_name,
            "required_affection": level.required_affection,
            "level_description": level.level_description,
            "unlock_rewards": level.unlock_rewards,
            "special_actions": level.special_actions,
            "random_drop_config": level.random_drop_config
        }
        for level in levels
    ]
