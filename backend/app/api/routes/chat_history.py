from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
import aiohttp
import re
import asyncio

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
from app.services.psychological_assessment_service import psychological_assessment_service

router = APIRouter()

def detect_risk_keywords(content: str) -> bool:
    """检测消息中是否包含风险关键词"""
    risk_keywords = [
        # 自杀相关
        "自杀", "想死", "死了算了", "不想活", "结束生命", "了结自己", "自我了断", 
        "想要死", "我想死", "去死", "寻死", "轻生", "自尽", "一死了之",
        
        # 自残相关  
        "自残", "自伤", "割腕", "割手", "伤害自己", "弄伤自己", "自己伤害",
        "切割自己", "划伤自己", "撞墙", "撞头",
        
        # 绝望相关
        "没有希望", "绝望", "无望", "看不到未来", "没有未来", "活着没意思",
        "人生无意义", "生无可恋", "痛不欲生", "万念俱灰", "心如死灰",
        
        # 药物滥用
        "过量服药", "吃安眠药", "药物自杀", "服毒", "吞药",
        
        # 其他危险行为
        "跳楼", "跳河", "撞车", "上吊", "跳桥", "煤气中毒"
    ]
    
    content_lower = content.lower()
    for keyword in risk_keywords:
        if keyword in content_lower:
            return True
    return False

async def generate_psychological_report_task(session_id: int):
    """后台任务：生成心理评估报告"""
    try:
        from app.database.session import SessionLocal
        db = SessionLocal()
        try:
            print(f"🧠 开始为会话 {session_id} 生成心理评估报告...")
            report = await psychological_assessment_service.generate_report(session_id, db)
            if report:
                print(f"✅ 心理评估报告生成成功: {report.report_id}")
            else:
                print(f"ℹ️ 会话 {session_id} 无需生成心理评估报告")
        finally:
            db.close()
    except Exception as e:
        print(f"❌ 生成心理评估报告失败: {str(e)}")

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
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存对话记录"""
    print(f"📥 收到保存请求 - 用户ID: {current_user.user_id}")
    print(f"📥 场景: {request.scene}")
    print(f"📥 会话ID: {request.session_id}")
    print(f"📥 消息数量: {len(request.messages)}")
    print(f"📥 消息内容: {[{'role': msg.role, 'content': msg.content[:50] + '...' if len(msg.content) > 50 else msg.content} for msg in request.messages]}")
    
    if not request.messages:
        raise HTTPException(status_code=400, detail="对话内容不能为空")
    
    # 如果提供了session_id，则更新现有会话
    if request.session_id:
        print(f"🔄 更新现有会话: {request.session_id}")
        # 查找现有会话
        existing_session = db.query(ChatSession).filter(
            ChatSession.id == request.session_id,
            ChatSession.user_id == current_user.user_id
        ).first()
        
        if not existing_session:
            print(f"❌ 会话不存在: {request.session_id}")
            raise HTTPException(status_code=404, detail="对话记录不存在")
        
        print(f"✅ 找到现有会话: {existing_session.id}")
        
        # 检查消息中是否有风险关键词
        has_risk = False
        for msg in request.messages:
            if detect_risk_keywords(msg.content):
                has_risk = True
                print(f"🚨 检测到风险关键词在消息: {msg.content[:50]}...")
                break
        
        # 如果检测到风险，启用自动保存
        if has_risk and not existing_session.auto_save_enabled:
            existing_session.auto_save_enabled = True
            print(f"🔒 为会话 {existing_session.id} 启用自动保存")
        
        # 更新会话标题（如果提供了新标题）
        if request.title:
            existing_session.title = request.title
            
        # 更新时间
        existing_session.updated_at = datetime.utcnow()
        
        # 删除原有消息
        deleted_count = db.query(ChatMessage).filter(ChatMessage.session_id == request.session_id).delete()
        print(f"🗑️ 删除原有消息数量: {deleted_count}")
        
        # 添加新消息
        for i, msg in enumerate(request.messages):
            chat_message = ChatMessage(
                session_id=existing_session.id,
                role=msg.role,
                content=msg.content
            )
            db.add(chat_message)
            print(f"➕ 添加消息 {i+1}: {msg.role} - {msg.content[:50]}...")
        
        db.commit()
        db.refresh(existing_session)
        print(f"✅ 会话更新完成: {existing_session.id}")
        
        # 如果检测到风险或会话已启用自动保存，则生成心理评估报告
        if has_risk or existing_session.auto_save_enabled:
            print(f"🧠 触发心理评估报告生成 - 会话ID: {existing_session.id}")
            background_tasks.add_task(generate_psychological_report_task, existing_session.id)
        
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

    # 检查消息中是否有风险关键词
    has_risk = False
    for msg in request.messages:
        if detect_risk_keywords(msg.content):
            has_risk = True
            print(f"🚨 检测到风险关键词在新会话消息: {msg.content[:50]}...")
            break

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
        title=title,
        auto_save_enabled=has_risk  # 如果检测到风险，立即启用自动保存
    )
    
    if has_risk:
        print(f"🔒 新会话因检测到风险关键词，启用自动保存")
    
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
    
    # 如果检测到风险，则生成心理评估报告
    if has_risk:
        print(f"🧠 触发心理评估报告生成 - 新会话ID: {chat_session.id}")
        background_tasks.add_task(generate_psychological_report_task, chat_session.id)
    
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

@router.get("/chat-sessions/{session_id}/auto-save-status")
async def get_auto_save_status(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取会话的自动保存状态"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="对话记录不存在")
    
    return {"auto_save_enabled": session.auto_save_enabled}

@router.put("/chat-sessions/{session_id}/enable-auto-save")
async def enable_auto_save(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """为会话启用自动保存"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="对话记录不存在")
    
    session.auto_save_enabled = True
    session.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "自动保存已启用", "auto_save_enabled": True}
