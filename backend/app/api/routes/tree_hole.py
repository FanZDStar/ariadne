#file:ariadne/backend/app/api/routes/tree_hole.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.models.tree_hole_chat import TreeHoleChatParticipant 
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment, TreeHoleLike
from app.schemas.tree_hole import WhisperCreate, WhisperUpdate, WhisperResponse, CommentResponse, CommentCreate
from app.api.deps import get_current_user

router = APIRouter(prefix="/tree-hole", tags=["心灵树洞"])

@router.post("/", response_model=WhisperResponse, status_code=status.HTTP_201_CREATED)
def create_whisper(
    whisper: WhisperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的悄悄话"""
    from app.models.tree_hole import TreeHoleWhisperImage
    
    # 创建悄悄话对象
    db_whisper = TreeHoleWhisper(
        user_id=current_user.user_id,
        title=whisper.title,
        mood=whisper.mood,
        tags=whisper.tags,
        is_anonymous=whisper.is_anonymous,
        anonymous_name=whisper.anonymous_name,
        anonymous_avatar=whisper.anonymous_avatar
    )
    
    # 使用加密属性设置内容，自动处理加密
    db_whisper.decrypted_content = whisper.content
    
    db.add(db_whisper)
    db.commit()
    db.refresh(db_whisper)
    
    # 创建关联的图片记录
    if whisper.images:
        for image_data in whisper.images:
            db_image = TreeHoleWhisperImage(
                whisper_id=db_whisper.whisper_id,
                image_url=image_data.image_url,
                image_order=image_data.image_order
            )
            db.add(db_image)
        db.commit()
        db.refresh(db_whisper)
    
    # 确保返回解密后的内容
    db_whisper.content = db_whisper.decrypted_content
    return db_whisper

@router.get("/my-whispers", response_model=List[WhisperResponse])
def get_user_whispers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有悄悄话，按时间倒序排列"""
    whispers = db.query(TreeHoleWhisper)\
                .options(
                    joinedload(TreeHoleWhisper.user),
                    joinedload(TreeHoleWhisper.images)
                )\
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
        
        # 确保返回解密后的内容
        whisper.content = whisper.decrypted_content
        
    return whispers

@router.get("/random", response_model=WhisperResponse)
def get_random_whisper(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """随机获取一个悄悄话"""
    whisper = db.query(TreeHoleWhisper).options(
        joinedload(TreeHoleWhisper.user),
        joinedload(TreeHoleWhisper.images)
    ).filter(
        TreeHoleWhisper.user_id != current_user.user_id
    ).order_by(func.rand()).first()

    if not whisper:
        raise HTTPException(status_code=404, detail="No whispers found")

    like = db.query(TreeHoleLike).filter(
        TreeHoleLike.whisper_id == whisper.whisper_id,
        TreeHoleLike.user_id == current_user.user_id
    ).first()
    whisper.liked = like is not None
    
    # 确保返回解密后的内容
    whisper.content = whisper.decrypted_content
    
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
                .options(
                    joinedload(TreeHoleWhisper.user),
                    joinedload(TreeHoleWhisper.images)
                )\
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
        
        # 确保返回解密后的内容
        whisper.content = whisper.decrypted_content

    return whispers

@router.get("/{whisper_id}", response_model=WhisperResponse)
def get_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定的悄悄话"""
    whisper = db.query(TreeHoleWhisper)\
              .options(
                  joinedload(TreeHoleWhisper.user),
                  joinedload(TreeHoleWhisper.images)
              )\
              .filter(TreeHoleWhisper.whisper_id == whisper_id)\
              .first()
    
    if not whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Whisper not found"
        )
    
    # 权限检查：允许以下情况访问
    # 1. 匿名悄悄话（所有人都可以看）
    # 2. 是创建者本人
    # 3. 用户曾经点赞过这个悄悄话
    # 4. 用户参与过这个悄悄话的聊天
    can_access = (
        whisper.is_anonymous or  # 匿名悄悄话
        whisper.user_id == current_user.user_id or  # 是创建者
        db.query(TreeHoleLike).filter(  # 曾经点赞过
            TreeHoleLike.whisper_id == whisper_id,
            TreeHoleLike.user_id == current_user.user_id
        ).first() is not None or
        db.query(TreeHoleChatParticipant).filter(  # 参与过聊天
            TreeHoleChatParticipant.whisper_id == whisper_id,
            TreeHoleChatParticipant.user_id == current_user.user_id
        ).first() is not None
    )
    
    if not can_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
        
    like = db.query(TreeHoleLike).filter(
        TreeHoleLike.whisper_id == whisper.whisper_id,
        TreeHoleLike.user_id == current_user.user_id
    ).first()
    whisper.liked = like is not None
    
    # 确保返回解密后的内容
    whisper.content = whisper.decrypted_content
    
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
                 .options(joinedload(TreeHoleWhisper.images))\
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
        if key == 'content':
            # 对于内容字段，使用加密属性
            db_whisper.decrypted_content = value
        else:
            setattr(db_whisper, key, value)
    
    db.commit()
    db.refresh(db_whisper)
    
    # 确保返回解密后的内容
    db_whisper.content = db_whisper.decrypted_content
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
    
    return {"message": "操作成功", "liked": like is None}


@router.get("/my-interactions", response_model=List[WhisperResponse])
def get_user_interactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户参与互动的悄悄话（点赞或评论过的）"""
    # 获取用户点赞过的悄悄话
    liked_whispers = db.query(TreeHoleWhisper)\
        .options(
            joinedload(TreeHoleWhisper.user),
            joinedload(TreeHoleWhisper.images)
        )\
        .join(TreeHoleLike, TreeHoleWhisper.whisper_id == TreeHoleLike.whisper_id)\
        .filter(TreeHoleLike.user_id == current_user.user_id)\
        .filter(TreeHoleWhisper.user_id != current_user.user_id)  # 排除自己的悄悄话
    
    # 获取用户参与聊天的悄悄话
    chatted_whispers = db.query(TreeHoleWhisper)\
        .options(
            joinedload(TreeHoleWhisper.user),
            joinedload(TreeHoleWhisper.images)
        )\
        .join(TreeHoleChatParticipant, TreeHoleWhisper.whisper_id == TreeHoleChatParticipant.whisper_id)\
        .filter(TreeHoleChatParticipant.user_id == current_user.user_id)\
        .filter(TreeHoleWhisper.user_id != current_user.user_id)  # 排除自己的悄悄话
    
    # 合并并去重
    all_whispers = liked_whispers.union(chatted_whispers)\
        .order_by(TreeHoleWhisper.created_at.desc())\
        .all()
    
    # 构造响应数据
    result = []
    for whisper in all_whispers:
        # 检查是否点赞
        like = db.query(TreeHoleLike).filter(
            TreeHoleLike.whisper_id == whisper.whisper_id,
            TreeHoleLike.user_id == current_user.user_id
        ).first()
        
        # 检查互动类型
        has_like = like is not None
        has_chat = db.query(TreeHoleChatParticipant).filter(
            TreeHoleChatParticipant.whisper_id == whisper.whisper_id,
            TreeHoleChatParticipant.user_id == current_user.user_id
        ).first() is not None
        
        # 设置互动类型标识
        interaction_type = None
        if has_like and has_chat:
            interaction_type = "both"
        elif has_like:
            interaction_type = "like"
        else:
            interaction_type = "chat"
        
        # 计算该悄悄话的聊天数
        chat_count = db.query(TreeHoleChatParticipant).filter(
            TreeHoleChatParticipant.whisper_id == whisper.whisper_id
        ).count()
        
        # 创建响应对象
        whisper_dict = {
            "whisper_id": whisper.whisper_id,
            "user_id": whisper.user_id,
            "title": whisper.title,
            "content": whisper.decrypted_content,
            "mood": whisper.mood,
            "tags": whisper.tags,
            "is_anonymous": whisper.is_anonymous,
            "anonymous_name": whisper.anonymous_name,
            "anonymous_avatar": whisper.anonymous_avatar,
            "like_count": whisper.like_count,
            "comment_count": chat_count,
            "created_at": whisper.created_at,
            "updated_at": whisper.updated_at,
            "user": whisper.user,
            "images": whisper.images,
            "liked": has_like,
            "interaction_type": interaction_type
        }
        result.append(whisper_dict)
        
    return result


@router.get("/{whisper_id}/comments", response_model=List[CommentResponse])
def get_whisper_comments(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取悄悄话的评论列表"""
    # 先检查悄悄话是否存在
    whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")
    
    # 获取评论列表
    comments = db.query(TreeHoleComment)\
        .options(joinedload(TreeHoleComment.user))\
        .filter(TreeHoleComment.whisper_id == whisper_id)\
        .order_by(TreeHoleComment.created_at.desc())\
        .all()
    
    # 构造评论响应数据
    comment_list = []
    for comment in comments:
        comment_dict = {
            "comment_id": comment.comment_id,
            "whisper_id": comment.whisper_id,
            "user_id": comment.user_id,
            "content": comment.decrypted_content,
            "is_anonymous": comment.is_anonymous,
            "created_at": comment.created_at,
            "user": comment.user
        }
        comment_list.append(comment_dict)
    
    return comment_list


@router.post("/{whisper_id}/comments")
def create_whisper_comment(
    whisper_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建悄悄话评论"""
    # 检查悄悄话是否存在
    whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")
    
    # 创建评论
    db_comment = TreeHoleComment(
        whisper_id=whisper_id,
        user_id=current_user.user_id,
        is_anonymous=comment_data.is_anonymous
    )
    
    # 设置加密内容
    db_comment.decrypted_content = comment_data.content
    
    db.add(db_comment)
    
    # 更新悄悄话的评论数
    whisper.comment_count += 1
    
    db.commit()
    db.refresh(db_comment)
    
    return {"message": "评论创建成功", "comment_id": db_comment.comment_id}