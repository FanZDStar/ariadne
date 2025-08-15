#file:ariadne/backend/app/api/routes/diary.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.api.deps import get_current_user
from app.models.emotional_diary import EmotionalDiary

router = APIRouter(prefix="/diary", tags=["情感日记"])

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
        is_private=diary.is_private
    )
    
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary

@router.get("/", response_model=List[DiaryResponse])
def get_user_diaries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有情感日记，按时间倒序排列"""
    diaries = db.query(EmotionalDiary)\
                .filter(EmotionalDiary.user_id == current_user.user_id)\
                .order_by(EmotionalDiary.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()
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
        setattr(db_diary, key, value)
    
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