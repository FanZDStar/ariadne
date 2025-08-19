# file:ariadne/backend/app/api/routes/tree_hole_chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.user import User
from app.models.tree_hole import TreeHoleWhisper
from app.models.tree_hole_chat import TreeHoleChat, TreeHoleChatParticipant
from app.schemas.tree_hole_chat import TreeHoleChatCreate, TreeHoleChat as TreeHoleChatSchema
from app.schemas.tree_hole import WhisperResponse 
from app.api.deps import get_current_user
import random

router = APIRouter(prefix="/tree-hole-chat", tags=["心灵树洞聊天"])

# 预定义的匿名昵称和头像列表
ANONYMOUS_NICKNAMES = ["听风者", "寄梦人", "观星者", "捕云者", "寻光者"]
ANONYMOUS_AVATARS = [
    "/uploads/anonymous_avatar_1.png",
    "/uploads/anonymous_avatar_2.png",
    "/uploads/anonymous_avatar_3.png",
    "/uploads/anonymous_avatar_4.png",
    "/uploads/anonymous_avatar_5.png",
]


def get_or_create_participant(db: Session, whisper_id: int, user_id: int):
    participant = db.query(TreeHoleChatParticipant).filter(
        TreeHoleChatParticipant.whisper_id == whisper_id,
        TreeHoleChatParticipant.user_id == user_id
    ).first()

    if not participant:
        anonymous_nickname = random.choice(ANONYMOUS_NICKNAMES)
        anonymous_avatar = random.choice(ANONYMOUS_AVATARS)
        participant = TreeHoleChatParticipant(
            whisper_id=whisper_id,
            user_id=user_id,
            anonymous_nickname=anonymous_nickname,
            anonymous_avatar=anonymous_avatar
        )
        db.add(participant)
        db.commit()
        db.refresh(participant)

    return participant


@router.post("/{whisper_id}", response_model=TreeHoleChatSchema)
def create_chat_message(
    whisper_id: int,
    chat: TreeHoleChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送悄悄话聊天消息"""
    db_whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()
    if not db_whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    # Get or create a participant entry for the current user
    get_or_create_participant(db, whisper_id, current_user.user_id)
    
    # Mark the whisper as having been chatted on
    if not db_whisper.chatted:
        db_whisper.chatted = True
        db.commit()

    db_chat = TreeHoleChat(**chat.dict(), whisper_id=whisper_id, user_id=current_user.user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.get("/{whisper_id}", response_model=List[TreeHoleChatSchema])
def get_chat_messages(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取悄悄话的聊天记录"""
    # 验证用户是否有权查看此聊天
    participant = db.query(TreeHoleChatParticipant).filter(
        TreeHoleChatParticipant.whisper_id == whisper_id,
        TreeHoleChatParticipant.user_id == current_user.user_id
    ).first()
    whisper = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.whisper_id == whisper_id).first()

    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    if not participant and whisper.user_id != current_user.user_id:
        # If the user is the author, create a participant entry for them
        if whisper.user_id == current_user.user_id:
            get_or_create_participant(db, whisper_id, current_user.user_id)
        else:
            raise HTTPException(status_code=403, detail="Not authorized to view this chat")

    chats = db.query(TreeHoleChat).filter(TreeHoleChat.whisper_id == whisper_id).order_by(TreeHoleChat.created_at).all()
    return chats

@router.delete("/{whisper_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_chat(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """用户退出一个悄悄话聊天"""
    participant = db.query(TreeHoleChatParticipant).filter(
        TreeHoleChatParticipant.whisper_id == whisper_id,
        TreeHoleChatParticipant.user_id == current_user.user_id
    ).first()

    if not participant:
        raise HTTPException(status_code=404, detail="你不在这个聊天中")

    db.delete(participant)
    db.commit()
    return
@router.get("/chats/", response_model=List[WhisperResponse]) # 修改 response_model
def get_user_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户参与的所有聊天"""
    # 我发起的
    my_whispers = db.query(TreeHoleWhisper).filter(TreeHoleWhisper.user_id == current_user.user_id, TreeHoleWhisper.chatted == True).all()

    # 我参与的
    participated_whisper_ids = db.query(TreeHoleChatParticipant.whisper_id).filter(
        TreeHoleChatParticipant.user_id == current_user.user_id
    ).distinct().all()
    participated_whispers = db.query(TreeHoleWhisper).filter(
        TreeHoleWhisper.whisper_id.in_([item[0] for item in participated_whisper_ids])
    ).all()

    # 合并并去重
    all_whispers_map = {whisper.whisper_id: whisper for whisper in my_whispers}
    for whisper in participated_whispers:
        all_whispers_map[whisper.whisper_id] = whisper
        
    all_whispers = list(all_whispers_map.values())

    # 为每个聊天计算消息总数
    for whisper in all_whispers:
        message_count = db.query(TreeHoleChat).filter(TreeHoleChat.whisper_id == whisper.whisper_id).count()
        whisper.comment_count = message_count

    return all_whispers