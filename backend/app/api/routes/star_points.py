"""
星星积分系统API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.star_point_service import get_star_point_service
from app.utils.star_point_types import StarPointAction, SourceType
from app.schemas.star_points import (
    UserStarPointsResponse, StarPointLogResponse, 
    AwardPointsRequest, SpendPointsRequest
)

router = APIRouter(prefix="/star-points", tags=["星星积分"])


@router.get("/balance", response_model=UserStarPointsResponse)
def get_user_star_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户当前积分余额"""
    service = get_star_point_service(db)
    user_points = service.get_or_create_user_points(current_user.user_id)
    
    return UserStarPointsResponse(
        user_id=user_points.user_id,
        current_points=user_points.current_points,
        total_earned=user_points.total_earned,
        total_spent=user_points.total_spent,
        created_at=user_points.created_at,
        updated_at=user_points.updated_at
    )


@router.get("/logs", response_model=List[StarPointLogResponse])
def get_user_point_logs(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户积分变动日志"""
    service = get_star_point_service(db)
    logs = service.get_point_logs(current_user.user_id, limit)
    
    return [
        StarPointLogResponse(
            id=log.id,
            user_id=log.user_id,
            action_type=log.action_type,
            points_change=log.points_change,
            description=log.description,
            source_id=log.source_id,
            source_type=log.source_type,
            created_at=log.created_at
        ) for log in logs
    ]


@router.post("/award")
def award_points(
    request: AwardPointsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """奖励用户积分（内部接口，用于各功能模块调用）"""
    service = get_star_point_service(db)
    
    try:
        action = StarPointAction(request.action_type)
        source_type = SourceType(request.source_type) if request.source_type else None
        
        success, message, points = service.award_points(
            user_id=current_user.user_id,
            action=action,
            source_id=request.source_id,
            source_type=source_type
        )
        
        return {
            "success": success,
            "message": message,
            "points_awarded": points if success else 0
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的行为类型或来源类型: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"积分奖励失败: {str(e)}"
        )


@router.post("/spend")
def spend_points(
    request: SpendPointsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """消费用户积分"""
    service = get_star_point_service(db)
    
    try:
        source_type = SourceType(request.source_type) if request.source_type else None
        
        success, message = service.spend_points(
            user_id=current_user.user_id,
            points=request.points,
            description=request.description,
            source_id=request.source_id,
            source_type=source_type
        )
        
        return {
            "success": success,
            "message": message
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"积分消费失败: {str(e)}"
        )


@router.get("/daily-status")
def get_daily_status(
    target_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户每日积分获取状态"""
    service = get_star_point_service(db)
    daily_limits = service.get_daily_limits(current_user.user_id, target_date)
    
    return {
        "date": daily_limits.date,
        "daily_login": daily_limits.daily_login,
        "mood_tracking": daily_limits.mood_tracking,
        "diary_count": daily_limits.diary_count,
        "background_change": daily_limits.background_change,
        "emotion_chat_count": daily_limits.emotion_chat_count,
        "emotion_chat_points": daily_limits.emotion_chat_points,
        "skill_training": daily_limits.skill_training,
        "relationship_assessment": daily_limits.relationship_assessment,
        "personalized_advice": daily_limits.personalized_advice,
        "ai_scenario_training": daily_limits.ai_scenario_training,
        "protection_training": daily_limits.protection_training,
        "tree_hole_interaction_count": daily_limits.tree_hole_interaction_count,
        "tree_hole_whisper": daily_limits.tree_hole_whisper
    }


# 内部工具函数，供其他模块调用
def award_user_points(
    db: Session, 
    user_id: int, 
    action: StarPointAction,
    source_id: str = None,
    source_type: SourceType = None
) -> tuple[bool, str, int]:
    """供其他模块调用的积分奖励函数"""
    service = get_star_point_service(db)
    result = service.award_points(user_id, action, source_id, source_type)
    return result.rewarded, result.message, result.points_awarded
