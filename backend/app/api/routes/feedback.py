from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.models.user_feedback import UserFeedback
from app.models.feedback_image import FeedbackImage
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/feedback", tags=["用户反馈"])

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的用户反馈"""
    db_feedback = UserFeedback(
        user_id=current_user.user_id,
        title=feedback.title,
        content=feedback.content,
        contact_info=feedback.contact_info
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    # 添加图片
    for image_data in feedback.images:
        db_image = FeedbackImage(
            feedback_id=db_feedback.feedback_id,
            image_url=image_data.image_url
        )
        db.add(db_image)
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=List[FeedbackResponse])
def get_user_feedbacks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有反馈"""
    feedbacks = db.query(UserFeedback)\
                  .filter(UserFeedback.user_id == current_user.user_id)\
                  .order_by(UserFeedback.created_at.desc())\
                  .offset(skip)\
                  .limit(limit)\
                  .all()
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定的反馈"""
    feedback = db.query(UserFeedback)\
                 .filter(UserFeedback.feedback_id == feedback_id)\
                 .filter(UserFeedback.user_id == current_user.user_id)\
                 .first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新反馈状态（仅管理员）"""
    feedback = db.query(UserFeedback)\
                 .filter(UserFeedback.feedback_id == feedback_id)\
                 .first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # 检查是否是管理员或反馈创建者
    if feedback.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # 更新字段
    update_data = feedback_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(feedback, key, value)
    
    db.commit()
    db.refresh(feedback)
    return feedback