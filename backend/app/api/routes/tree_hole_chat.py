# # # backend/app/api/routes/tree_hole_chat.py
# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from typing import List
# # from app.database.session import get_db
# # from app.models.user import User
# # from app.models.tree_hole import TreeHoleWhisper
# # from app.models.tree_hole_chat import TreeHoleChat, TreeHoleChatParticipant
# # from app.schemas.tree_hole_chat import TreeHoleChatCreate, TreeHoleChat
# # from app.api.deps import get_current_user
# # import random

# # router = APIRouter(prefix="/tree-hole-chat", tags=["心灵树洞聊天"])

# # # 预定义的匿名昵称和头像列表
# # ANONYMOUS_NICKNAMES = ["听风者", "寄梦人", "观星者", "捕云者", "寻光者"]
# # ANONYMOUS_AVATARS = [
# #     "/uploads/anonymous_avatar_1.png",
# #     "/uploads/anonymous_avatar_2.png",
# #     "/uploads/anonymous_avatar_3.png",
# #     "/uploads/anonymous_avatar_4.png",
# #     "/uploads/anonymous_avatar_5.png",
# # ]


# # def get_or_create_participant(db: Session, whisper_id: int, user_id: int):
# #     participant = db.query(TreeHoleChatParticipant).filter(
# #         TreeHoleChatParticipant.whisper_id == whisper_id,
# #         TreeHoleChatParticipant.user_id == user_id
# #     ).first()

# #     if not participant:
# #         anonymous_nickname = random.choice(ANONYMOUS_NICKNAMES)
# #         anonymous_avatar = random.choice(ANONYMOUS_AVATARS)
# #         participant = TreeHoleChatParticipant(
# #             whisper_id=whisper_id,
# #             user_id=user_id,
# #             anonymous_nickname=anonymous_nickname,
# #             anonymous_avatar=anonymous_avatar
# #         )
# #         db.add(participant)
# #         db.commit()
# #         db.refresh(participant)

# #     return participant


# # @router.post("/{whisper_id}", response_model=TreeHoleChat)
# # def create_chat_message(
# #     whisper_id: int,
# #     chat: TreeHoleChatCreate,
# #     db: Session = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     """发送悄悄话聊天消息"""
# #     db_whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
# #     if not db_whisper:
# #         raise HTTPException(status_code=404, detail="Whisper not found")

# #     # 标记悄悄话为已回复
# #     if not db_whisper.chatted:
# #         db_whisper.chatted = True
# #         db.commit()

# #     db_chat = TreeHoleChat(**chat.dict(), whisper_id=whisper_id, user_id=current_user.user_id)
# #     db.add(db_chat)
# #     db.commit()
# #     db.refresh(db_chat)
# #     return db_chat


# # @router.get("/{whisper_id}", response_model=List[TreeHoleChat])
# # def get_chat_messages(
# #     whisper_id: int,
# #     db: Session = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     """获取悄悄话的聊天记录"""
# #     # 验证用户是否有权查看此聊天
# #     participant = db.query(TreeHoleChatParticipant).filter(
# #         TreeHoleChatParticipant.whisper_id == whisper_id,
# #         TreeHoleChatParticipant.user_id == current_user.user_id
# #     ).first()
# #     whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()

# #     if not whisper:
# #         raise HTTPException(status_code=404, detail="Whisper not found")

# #     if not participant and whisper.user_id != current_user.user_id:
# #         raise HTTPException(status_code=403, detail="Not authorized to view this chat")

# #     chats = db.query(TreeHoleChat).filter(TreeHoleChat.whisper_id == whisper_id).order_by(TreeHoleChat.created_at).all()
# #     return chats


# # @router.get("/chats/")
# # def get_user_chats(
# #     db: Session = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     """获取用户参与的所有聊天"""
# #     # 我发起的
# #     my_whispers = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.user_id == current_user.user_id, TreeHoleWhisper.chatted == True).all()

# #     # 我参与的
# #     participated_whisper_ids = db.query(TreeHoleChatParticipant.whisper_id).filter(
# #         TreeHoleChatParticipant.user_id == current_user.user_id
# #     ).distinct().all()
# #     participated_whispers = db.query(TreeHoleWhisper).filter(
# #         TreeHoleWhisper.whisper_id.in_([item[0] for item in participated_whisper_ids])
# #     ).all()

# #     # 合并并去重
# #     all_whispers = {whisper.whisper_id: whisper for whisper in my_whispers}
# #     for whisper in participated_whispers:
# #         all_whispers[whisper.whisper_id] = whisper

# #     return list(all_whispers.values())

# # backend/app/api/routes/tree_hole.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy import and_, func
# from typing import List
# from app.database.session import get_db
# from app.models.user import User
# from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment, TreeHoleLike
# from app.schemas.tree_hole import WhisperCreate, WhisperUpdate, WhisperResponse
# from app.api.deps import get_current_user

# router = APIRouter(prefix="/tree-hole", tags=["心灵树洞"])


# @router.get("/random", response_model=WhisperResponse)
# def get_random_whisper(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """随机获取一个悄悄话"""
#     whisper = db.query(TreeHoleWhisper).filter(
#         TreeHoleWhisper.user_id != current_user.user_id
#     ).order_by(func.rand()).first()

#     if not whisper:
#         raise HTTPException(status_code=404, detail="No whispers found")

#     return whisper


# @router.post("/{whisper_id}/like", status_code=status.HTTP_204_NO_CONTENT)
# def like_whisper(
#     whisper_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """点赞悄悄话"""
#     db_whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
#     if not db_whisper:
#         raise HTTPException(status_code=404, detail="Whisper not found")

#     like = db.query(TreeHoleLike).filter(
#         TreeHoleLike.whisper_id == whisper_id,
#         TreeHoleLike.user_id == current_user.user_id
#     ).first()

#     if like:
#         # 取消点赞
#         db.delete(like)
#         db_whisper.like_count -= 1
#     else:
#         # 点赞
#         new_like = TreeHoleLike(whisper_id=whisper_id, user_id=current_user.user_id)
#         db.add(new_like)
#         db_whisper.like_count += 1

#     db.commit()


# @router.post("/", response_model=WhisperResponse, status_code=status.HTTP_201_CREATED)
# def create_whisper(
#     whisper: WhisperCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """创建新的悄悄话"""
#     db_whisper = TreeHoleWhisper(
#         user_id=current_user.user_id,
#         content=whisper.content,
#         is_anonymous=whisper.is_anonymous
#     )
    
#     db.add(db_whisper)
#     db.commit()
#     db.refresh(db_whisper)
#     return db_whisper

# @router.get("/my-whispers", response_model=List[WhisperResponse])
# def get_user_whispers(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """获取当前用户的所有悄悄话，按时间倒序排列"""
#     whispers = db.query(TreeHoleWhisper)\
#                 .filter(TreeHoleWhisper.user_id == current_user.user_id)\
#                 .order_by(TreeHoleWhisper.created_at.desc())\
#                 .all()
#     return whispers

# @router.get("/", response_model=List[WhisperResponse])
# def get_public_whispers(
#     skip: int = 0,
#     limit: int = 20,
#     db: Session = Depends(get_db)
# ):
#     """获取公开的悄悄话（用于做倾听者功能）"""
#     whispers = db.query(TreeHoleWhisper)\
#                 .filter(TreeHoleWhisper.is_anonymous == True)\
#                 .order_by(TreeHoleWhisper.created_at.desc())\
#                 .offset(skip)\
#                 .limit(limit)\
#                 .all()
#     return whispers

# @router.get("/{whisper_id}", response_model=WhisperResponse)
# def get_whisper(
#     whisper_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """获取特定的悄悄话"""
#     whisper = db.query(TreeHoleWhisper)\
#               .filter(TreeHoleWhisper.whisper_id == whisper_id)\
#               .first()
    
#     if not whisper:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Whisper not found"
#         )
    
#     # 如果不是匿名悄悄话，检查是否是创建者
#     if not whisper.is_anonymous and whisper.user_id != current_user.user_id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not enough permissions"
#         )
    
#     return whisper

# @router.put("/{whisper_id}", response_model=WhisperResponse)
# def update_whisper(
#     whisper_id: int,
#     whisper_update: WhisperUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """更新悄悄话"""
#     db_whisper = db.query(TreeHoleWhisper)\
#                  .filter(TreeHoleWhisper.whisper_id == whisper_id)\
#                  .filter(TreeHoleWhisper.user_id == current_user.user_id)\
#                  .first()
    
#     if not db_whisper:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Whisper not found"
#         )
    
#     # 更新字段
#     update_data = whisper_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_whisper, key, value)
    
#     db.commit()
#     db.refresh(db_whisper)
#     return db_whisper

# @router.delete("/{whisper_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_whisper(
#     whisper_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """删除悄悄话"""
#     db_whisper = db.query(TreeHoleWhisper)\
#                  .filter(TreeHoleWhisper.whisper_id == whisper_id)\
#                  .filter(TreeHoleWhisper.user_id == current_user.user_id)\
#                  .first()
    
#     if not db_whisper:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Whisper not found"
#         )
    
#     db.delete(db_whisper)
#     db.commit()
#     return
# backend/app/api/routes/tree_hole.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment, TreeHoleLike
from app.schemas.tree_hole import WhisperCreate, WhisperUpdate, WhisperResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/tree-hole", tags=["心灵树洞"])


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

    return whisper


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
    return whispers

@router.get("/", response_model=List[WhisperResponse])
def get_public_whispers(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取公开的悄悄话（用于做倾听者功能）"""
    whispers = db.query(TreeHoleWhisper)\
                .options(joinedload(TreeHoleWhisper.user))\
                .filter(TreeHoleWhisper.is_anonymous == True)\
                .order_by(TreeHoleWhisper.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()
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