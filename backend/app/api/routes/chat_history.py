from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
import aiohttp

from app.database.session import get_db
from app.models.chat_history import ChatSession, ChatMessage
from app.schemas.chat_history import (
    ChatSession as ChatSessionSchema, 
    SaveChatRequest, 
    ChatHistoryResponse
)
from app.api.deps import get_current_user
from app.models.user import User
from app.core.config import settings

router = APIRouter()

async def generate_title_with_ai(messages: List[dict]) -> str:
    """使用AI为对话生成标题"""
    try:
        # 获取对话内容摘要（最多取前3轮对话）
        conversation_text = ""
        count = 0
        for msg in messages:
            if count >= 6:  # 最多3轮对话（每轮用户+助手）
                break
            conversation_text += f"{msg['role']}: {msg['content']}\n"
            count += 1
        
        # 构建标题生成的prompt
        title_prompt = f"""
请为以下对话生成一个简洁的标题（不超过15个字）：

{conversation_text}

要求：
1. 标题要能概括对话的主要内容或情感主题
2. 不超过15个字
3. 语言简洁、有吸引力
4. 只返回标题内容，不要其他说明

标题："""

        # 调用AI API
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {settings.ai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "qwen-plus",
                "messages": [
                    {
                        "role": "user",
                        "content": title_prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 30
            }
            
            async with session.post(
                'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    ai_title = result['choices'][0]['message']['content'].strip()
                    # 移除可能的引号和多余字符
                    ai_title = ai_title.replace('"', '').replace("'", '').strip()
                    return ai_title[:15]  # 确保不超过15个字
                else:
                    print(f"AI API调用失败: {response.status}")
                    return None
                    
    except Exception as e:
        print(f"AI标题生成失败: {e}")
        return None

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
    
    # 生成对话标题
    title = request.title
    if not title:
        # 尝试使用AI生成标题
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        ai_title = await generate_title_with_ai(messages_dict)
        
        if ai_title:
            title = ai_title
        else:
            # AI生成失败，使用兜底方案
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
