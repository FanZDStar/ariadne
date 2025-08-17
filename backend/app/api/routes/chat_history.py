from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.session import get_db
from app.models.chat_history import ChatSession, ChatMessage
from app.schemas.chat_history import (
    ChatSession as ChatSessionSchema, 
    SaveChatRequest, 
    ChatHistoryResponse
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/save-chat", response_model=ChatSessionSchema)
async def save_chat_session(
    request: SaveChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存对话记录"""
    if not request.messages:
        raise HTTPException(status_code=400, detail="对话内容不能为空")
    
    # 如果提供了session_id，则更新现有会话
    if request.session_id:
        # 查找现有会话
        existing_session = db.query(ChatSession).filter(
            ChatSession.id == request.session_id,
            ChatSession.user_id == current_user.user_id
        ).first()
        
        if not existing_session:
            raise HTTPException(status_code=404, detail="对话记录不存在")
        
        # 更新会话标题（如果提供了新标题）
        if request.title:
            existing_session.title = request.title
            
        # 更新时间
        existing_session.updated_at = datetime.utcnow()
        
        # 删除原有消息
        db.query(ChatMessage).filter(ChatMessage.session_id == request.session_id).delete()
        
        # 添加新消息
        for msg in request.messages:
            chat_message = ChatMessage(
                session_id=existing_session.id,
                role=msg.role,
                content=msg.content
            )
            db.add(chat_message)
        
        db.commit()
        db.refresh(existing_session)
        return existing_session
    
    # 如果没有提供session_id，则创建新会话
    # 检查用户在该场景下是否已有6个对话记录，如果是则删除最旧的
    existing_sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.user_id,
        ChatSession.scene == request.scene
    ).order_by(ChatSession.created_at.desc()).all()
    
    if len(existing_sessions) >= 6:
        # 删除最旧的对话
        oldest_session = existing_sessions[-1]
        db.delete(oldest_session)
        db.flush()
    
    # 生成对话标题（取第一条用户消息的前30个字符）
    title = request.title
    if not title:
        first_user_message = next((msg for msg in request.messages if msg.role == "user"), None)
        if first_user_message:
            title = first_user_message.content[:30] + ("..." if len(first_user_message.content) > 30 else "")
        else:
            title = f"{request.scene}对话"
    
    # 创建新的对话会话
    chat_session = ChatSession(
        user_id=current_user.user_id,
        scene=request.scene,
        title=title
    )
    db.add(chat_session)
    db.flush()  # 获取session id
    
    # 保存消息
    for msg in request.messages:
        chat_message = ChatMessage(
            session_id=chat_session.id,
            role=msg.role,
            content=msg.content
        )
        db.add(chat_message)
    
    db.commit()
    db.refresh(chat_session)
    
    return chat_session
@router.get("/chat-sessions", response_model=List[ChatSessionSchema])
async def get_chat_sessions(
    scene: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的对话历史"""
    query = db.query(ChatSession).filter(ChatSession.user_id == current_user.user_id)
    
    if scene:
        query = query.filter(ChatSession.scene == scene)
    
    sessions = query.order_by(ChatSession.updated_at.desc()).all()
    return sessions

@router.get("/chat-sessions/{session_id}", response_model=ChatSessionSchema)
async def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定对话会话的详细信息"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="对话记录不存在")
    
    return session

@router.delete("/chat-sessions/{session_id}")
async def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除对话记录"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="对话记录不存在")
    
    db.delete(session)
    db.commit()
    
    return {"message": "删除成功"}

@router.put("/chat-sessions/{session_id}/title")
async def update_chat_session_title(
    session_id: int,
    title: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新对话标题"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="对话记录不存在")
    
    session.title = title
    session.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "标题更新成功"}
