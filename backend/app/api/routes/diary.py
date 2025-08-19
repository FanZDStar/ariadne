# file:ariadne/backend/app/api/routes/diary.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta, date
from app.database.session import get_db
from app.models.user import User
from app.models.emotional_diary import EmotionalDiary
from app.models.diary_image import DiaryImage
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/diary", tags=["碎碎念"])

# ... (保留原有的创建、获取、更新、删除日记的接口) ...
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的碎碎念"""
    db_diary = EmotionalDiary(
        user_id=current_user.user_id,
        title=diary.title,
        content=diary.content,
        mood=diary.mood,
        is_private=diary.is_private,
        image_count=len(diary.images)
    )
    
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    
    # 添加图片
    for i, image_data in enumerate(diary.images):
        db_image = DiaryImage(
            diary_id=db_diary.diary_id,
            image_url=image_data.image_url,
            image_order=i
        )
        db.add(db_image)
    
    db.commit()
    db.refresh(db_diary)
    return db_diary

@router.get("/", response_model=List[DiaryResponse])
def get_user_diaries(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有碎碎念，按时间倒序排列"""
    query = db.query(EmotionalDiary)\
                .filter(EmotionalDiary.user_id == current_user.user_id)\
                .order_by(EmotionalDiary.created_at.desc())
    if limit is not None:
        query = query.offset(skip).limit(limit)
    else:
        query = query.offset(skip)
    
    diaries = query.all()
    return diaries

@router.get("/{diary_id}", response_model=DiaryResponse)
def get_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定的碎碎念"""
    diary = db.query(EmotionalDiary)\
              .filter(EmotionalDiary.diary_id == diary_id)\
              .filter(EmotionalDiary.user_id == current_user.user_id)\
              .first()
    
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    return diary

@router.put("/{diary_id}", response_model=DiaryResponse)
def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新碎碎念"""
    db_diary = db.query(EmotionalDiary)\
                 .filter(EmotionalDiary.diary_id == diary_id)\
                 .filter(EmotionalDiary.user_id == current_user.user_id)\
                 .first()
    
    if not db_diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    update_data = diary_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != 'images':
            setattr(db_diary, key, value)
    
    if diary_update.images is not None:
        db.query(DiaryImage).filter(DiaryImage.diary_id == diary_id).delete()
        for i, image_data in enumerate(diary_update.images):
            db_image = DiaryImage(
                diary_id=diary_id,
                image_url=image_data.image_url,
                image_order=i
            )
            db.add(db_image)
        db_diary.image_count = len(diary_update.images)
    
    db.commit()
    db.refresh(db_diary)
    return db_diary

@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除碎碎念"""
    db_diary = db.query(EmotionalDiary)\
                 .filter(EmotionalDiary.diary_id == diary_id)\
                 .filter(EmotionalDiary.user_id == current_user.user_id)\
                 .first()
    
    if not db_diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    db.delete(db_diary)
    db.commit()
    return

@router.get("/mood-stats/{period}")
def get_mood_statistics(
    period: str,  # "3days", "7days", "30days", "60days"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取心情统计数据，补全缺失日期的默认值"""
    # 确保查询范围覆盖当天的所有时间
    end_date = datetime.utcnow().replace(hour=23, minute=59, second=59)
    days = 0
    if period == "3days":
        days = 3
    elif period == "7days":
        days = 7
    elif period == "30days":
        days = 30
    elif period == "60days":
        days = 60
    else:
        raise HTTPException(status_code=400, detail="Invalid period")

    # 计算起始日期
    start_date = (end_date - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0)
    
    mood_score_case = EmotionalDiary.get_mood_score_case()

    stats_query = db.query(
        func.date(EmotionalDiary.created_at).label('date'),
        func.avg(mood_score_case).label('avg_mood')
    ).filter(
        and_(
            EmotionalDiary.user_id == current_user.user_id,
            EmotionalDiary.created_at >= start_date,
            EmotionalDiary.created_at <= end_date
        )
    ).group_by('date').order_by('date').all()
    
    stats_map = {stat.date: round(float(stat.avg_mood), 2) for stat in stats_query}
    
    result = []
    current_date = start_date.date()
    end_date_date = end_date.date()
    
    while current_date <= end_date_date:
        result.append({
            "time": current_date.strftime('%Y-%m-%d'),
            "mood_score": stats_map.get(current_date, 3.0)
        })
        current_date += timedelta(days=1)

    return {"period": period, "data": result}