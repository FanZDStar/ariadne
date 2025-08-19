#file:ariadne/backend/app/api/routes/tree_hole.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.models.tree_hole_chat import TreeHoleChatParticipant 
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment, TreeHoleLike
from app.schemas.tree_hole import WhisperCreate, WhisperUpdate, WhisperResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/tree-hole", tags=["心灵树洞"])

@router.post("/", response_model=WhisperResponse, status_code=status.HTTP_201_CREATED)
def create_whisper(
    whisper: WhisperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的悄悄话"""
    db_whisper = TreeHoleWhisper(
        user_id=current_user.user_id,
        content=whisper.content,
        is_anonymous=whisper.is_anonymous
    )
    
    db.add(db_whisper)
    db.commit()
    db.refresh(db_whisper)
    return db_whisper

@router.get("/my-whispers", response_model=List[WhisperResponse])
def get_user_whispers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有悄悄话，按时间倒序排列"""
    whispers = db.query(TreeHoleWhisper)\
                .options(joinedload(TreeHoleWhisper.user))\
                .filter(TreeHoleWhisper.user_id == current_user.user_id)\
                .order_by(TreeHoleWhisper.created_at.desc())\
                .all()
    
    for whisper in whispers:
        like = db.query(TreeHoleLike).filter(
            TreeHoleLike.whisper_id == whisper.whisper_id,
            TreeHoleLike.user_id == current_user.user_id
        ).first()
        whisper.liked = like is not None
        
        # 计算该悄悄话的聊天数
        chat_count = db.query(TreeHoleChatParticipant).filter(TreeHoleChatParticipant.whisper_id == whisper.whisper_id).count()
        whisper.comment_count = chat_count
        
    return whispers

@router.get("/random", response_model=WhisperResponse)
def get_random_whisper(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """随机获取一个悄悄话"""
    whisper = db.query(TreeHoleWhisper).options(joinedload(TreeHoleWhisper.user)).filter(
        TreeHoleWhisper.user_id != current_user.user_id
    ).order_by(func.rand()).first()

    if not whisper:
        raise HTTPException(status_code=404, detail="No whispers found")

    like = db.query(TreeHoleLike).filter(
        TreeHoleLike.whisper_id == whisper.whisper_id,
        TreeHoleLike.user_id == current_user.user_id
    ).first()
    whisper.liked = like is not None
    
    return whisper

@router.get("/", response_model=List[WhisperResponse])
def get_public_whispers(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取公开的悄悄话（用于做倾听者功能）"""
    whispers = db.query(TreeHoleWhisper)\
                .options(joinedload(TreeHoleWhisper.user))\
                .filter(TreeHoleWhisper.is_anonymous == True)\
                .order_by(TreeHoleWhisper.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()
                
    for whisper in whispers:
        like = db.query(TreeHoleLike).filter(
            TreeHoleLike.whisper_id == whisper.whisper_id,
            TreeHoleLike.user_id == current_user.user_id
        ).first()
        whisper.liked = like is not None

    return whispers

@router.get("/{whisper_id}", response_model=WhisperResponse)
def get_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定的悄悄话"""
    whisper = db.query(TreeHoleWhisper)\
              .options(joinedload(TreeHoleWhisper.user))\
              .filter(TreeHoleWhisper.whisper_id == whisper_id)\
              .first()
    
    if not whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Whisper not found"
        )
    
    # 如果不是匿名悄悄话，检查是否是创建者
    if not whisper.is_anonymous and whisper.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
        
    like = db.query(TreeHoleLike).filter(
        TreeHoleLike.whisper_id == whisper.whisper_id,
        TreeHoleLike.user_id == current_user.user_id
    ).first()
    whisper.liked = like is not None
    
    return whisper

@router.put("/{whisper_id}", response_model=WhisperResponse)
def update_whisper(
    whisper_id: int,
    whisper_update: WhisperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新悄悄话"""
    db_whisper = db.query(TreeHoleWhisper)\
                 .filter(TreeHoleWhisper.whisper_id == whisper_id)\
                 .filter(TreeHoleWhisper.user_id == current_user.user_id)\
                 .first()
    
    if not db_whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Whisper not found"
        )
    
    # 更新字段
    update_data = whisper_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_whisper, key, value)
    
    db.commit()
    db.refresh(db_whisper)
    return db_whisper

@router.delete("/{whisper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除悄悄话"""
    db_whisper = db.query(TreeHoleWhisper)\
                 .filter(TreeHoleWhisper.whisper_id == whisper_id)\
                 .filter(TreeHoleWhisper.user_id == current_user.user_id)\
                 .first()
    
    if not db_whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Whisper not found"
        )
    
    db.delete(db_whisper)
    db.commit()
    return

@router.post("/{whisper_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def like_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """点赞悄悄话"""
    db_whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
    if not db_whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    like = db.query(TreeHoleLike).filter(
        TreeHoleLike.whisper_id == whisper_id,
        TreeHoleLike.user_id == current_user.user_id
    ).first()

    if like:
        # 取消点赞
        db.delete(like)
        db_whisper.like_count -= 1
    else:
        # 点赞
        new_like = TreeHoleLike(whisper_id=whisper_id, user_id=current_user.user_id)
        db.add(new_like)
        db_whisper.like_count += 1

    db.commit()