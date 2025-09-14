from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.mood_tracker import MoodTrackerCreate, MoodTrackerResponse, WeeklyMoodResponse
from app.services.mood_tracker_service import MoodTrackerService

router = APIRouter()

@router.post("/mood", response_model=MoodTrackerResponse, summary="记录心情")
async def create_mood_record(
    mood_data: MoodTrackerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """记录用户的心情档位"""
    try:
        mood_record = MoodTrackerService.create_mood_record(db, current_user.user_id, mood_data)
        return mood_record
    except Exception as e:
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
