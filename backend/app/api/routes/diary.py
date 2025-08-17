#file:ariadne/backend/app/api/routes/diary.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.user import User
from app.models.emotional_diary import EmotionalDiary
from app.models.diary_image import DiaryImage
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/diary", tags=["情感日记"])

# ... 保留原有的创建、获取、更新、删除日记的接口 ...
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的情感日记"""
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
    """获取当前用户的所有情感日记，按时间倒序排列"""
    query = db.query(EmotionalDiary)\
                .filter(EmotionalDiary.user_id == current_user.user_id)\
                .order_by(EmotionalDiary.created_at.desc())
    if limit is not None:  # 如果提供了 limit 参数，则应用限制
        query = query.offset(skip).limit(limit)
    else:  # 如果未提供 limit 参数，则仅应用 offset
        query = query.offset(skip)
    
    diaries = query.all()
    return diaries

@router.get("/{diary_id}", response_model=DiaryResponse)
def get_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定的情感日记"""
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
    """更新情感日记"""
    db_diary = db.query(EmotionalDiary)\
                 .filter(EmotionalDiary.diary_id == diary_id)\
                 .filter(EmotionalDiary.user_id == current_user.user_id)\
                 .first()
    
    if not db_diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary not found"
        )
    
    # 更新字段
    update_data = diary_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != 'images':  # 图片单独处理
            setattr(db_diary, key, value)
    
    # 更新图片（如果提供了）
    if diary_update.images is not None:
        # 删除现有图片
        db.query(DiaryImage)\
          .filter(DiaryImage.diary_id == diary_id)\
          .delete()
        
        # 添加新图片
        for i, image_data in enumerate(diary_update.images):
            db_image = DiaryImage(
                diary_id=diary_id,
                image_url=image_data.image_url,
                image_order=i
            )
            db.add(db_image)
        
        # 更新图片计数
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
    """删除情感日记"""
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
    period: str,  # "today", "7days", "30days", "60days", "365days", "3days"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取心情统计数据"""
    # 确定时间范围
    end_date = datetime.utcnow()
    if period == "today":
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "3days":
        start_date = end_date - timedelta(days=3)
    elif period == "7days":
        start_date = end_date - timedelta(days=7)
    elif period == "30days":
        start_date = end_date - timedelta(days=30)
    elif period == "60days":
        start_date = end_date - timedelta(days=60)
    elif period == "365days":
        start_date = end_date - timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Invalid period")
    
    # 创建心情分数的CASE表达式
    mood_score_case = EmotionalDiary.get_mood_score_case()
    
    if period == "today":
        # 今天的心情数据，按小时分组
        stats = db.query(
            func.hour(EmotionalDiary.created_at).label('hour'),
            func.avg(mood_score_case).label('avg_mood')
        ).filter(
            and_(
                EmotionalDiary.user_id == current_user.user_id,
                EmotionalDiary.created_at >= start_date,
                EmotionalDiary.created_at <= end_date
            )
        ).group_by(
            func.hour(EmotionalDiary.created_at)
        ).order_by(
            func.hour(EmotionalDiary.created_at)
        ).all()
        
        # 格式化数据
        result = []
        for stat in stats:
            result.append({
                "time": f"{stat.hour}:00",
                "mood_score": round(float(stat.avg_mood), 2) if stat.avg_mood else 3.0
            })
    else:
        # 多天的心情数据，按天分组
        stats = db.query(
            func.date(EmotionalDiary.created_at).label('date'),
            func.avg(mood_score_case).label('avg_mood')
        ).filter(
            and_(
                EmotionalDiary.user_id == current_user.user_id,
                EmotionalDiary.created_at >= start_date,
                EmotionalDiary.created_at <= end_date
            )
        ).group_by(
            func.date(EmotionalDiary.created_at)
        ).order_by(
            func.date(EmotionalDiary.created_at)
        ).all()
        
        # 格式化数据
        result = []
        for stat in stats:
            result.append({
                "time": stat.date.strftime('%Y-%m-%d'),
                "mood_score": round(float(stat.avg_mood), 2) if stat.avg_mood else 3.0
            })
    
    return {
        "period": period,
        "data": result
    }
