from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.mood_tracker import MoodTrackerCreate, MoodTrackerResponse, MoodTrackerWithStarResponse, WeeklyMoodResponse
from app.services.mood_tracker_service import MoodTrackerService

router = APIRouter()

@router.post("/mood", response_model=MoodTrackerWithStarResponse, summary="记录心情")
async def create_mood_record(
    mood_data: MoodTrackerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """记录用户的心情档位"""
    try:
        result = MoodTrackerService.create_mood_record(db, current_user.user_id, mood_data)
        
        # 返回心情记录和积分奖励信息
        return {
            "id": result["mood_record"].id,
            "user_id": result["mood_record"].user_id,
            "mood_date": result["mood_record"].mood_date,
            "mood_level": result["mood_record"].mood_level,
            "created_at": result["mood_record"].created_at,
            "updated_at": result["mood_record"].updated_at,
            "star_awarded": result["star_awarded"],
            "star_points": result["star_points"],
            "star_message": result["star_message"],
            "affection_awarded": result["affection_awarded"],
            "affection_points": result["affection_points"],
            "affection_message": result["affection_message"],
            "affection_level_up": result["affection_level_up"]
        }
    except Exception as e:
        print(f"记录心情失败: {e}")
        raise HTTPException(status_code=500, detail="记录心情失败")

@router.get("/mood/weekly", response_model=WeeklyMoodResponse, summary="获取7天心情数据")
async def get_weekly_mood_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取最近7天的心情数据"""
    try:
        return MoodTrackerService.get_weekly_mood_data(db, current_user.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="获取心情数据失败")
