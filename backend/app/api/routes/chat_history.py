from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta
import json
import aiohttp
import re
import asyncio

from app.database.session import get_db
from app.models.chat_history import ChatSession, ChatMessage
from app.schemas.chat_history import (
    ChatSession as ChatSessionSchema, 
    SaveChatRequest, 
    ChatHistoryResponse,
    ChatSessionWithStarResponse,
    StarRewardInfo
)
from app.api.deps import get_current_user
from app.models.user import User
from app.core.config import settings
from app.services.psychological_assessment_service import psychological_assessment_service
from app.services.star_point_service import StarPointService
from app.utils.star_point_types import StarPointAction, SourceType

router = APIRouter()

def count_rewarded_user_messages_today(user_id: int, db: Session) -> int:
    """统计用户今天已经奖励过的消息数量，通过daily_star_limits表的emotion_chat_count字段"""
    star_service = StarPointService(db)
    daily_limits = star_service.get_daily_limits(user_id)
    return daily_limits.emotion_chat_count

def get_new_user_messages_count(session_id: Optional[int], request_messages: list, db: Session) -> int:
    """
    通过对比数据库中现有消息数量来识别新增的用户消息数量
    返回: 新增的用户消息数量
    """
    if not session_id:
        # 新会话，所有用户消息都是新的
        return sum(1 for msg in request_messages if msg.role == "user")
    
    # 获取数据库中该会话现有的消息数量
    current_db_message_count = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).count()
    
    # 前端传来的消息总数
    total_messages_from_frontend = len(request_messages)
    
    # 计算新增消息数量
    new_messages_count = total_messages_from_frontend - current_db_message_count
    
    if new_messages_count <= 0:
        return 0
    
    # 从新增消息中统计用户消息数量
    new_messages = request_messages[-new_messages_count:]
    new_user_messages = sum(1 for msg in new_messages if msg.role == "user")
    
    print(f"📊 会话 {session_id}: 数据库现有 {current_db_message_count} 条消息，前端传来 {total_messages_from_frontend} 条消息")
    print(f"📊 新增 {new_messages_count} 条消息，其中 {new_user_messages} 条用户消息")
    
    return new_user_messages

def calculate_single_message_reward(message_number: int) -> int:
    """
    计算单条消息的奖励
    返回: 奖励星点数
    """
    if message_number <= 3:
        # 前3条消息，每条奖励2星点
        return 2
    elif message_number <= 10:
        # 第4-10条消息，每条奖励1星点
        return 1
    else:
        # 超过10条消息不再奖励
        return 0

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

@router.post("/save-chat", response_model=ChatSessionWithStarResponse)
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
        
        # ⚠️ 重要：在删除消息之前先计算新增的用户消息数量
        new_user_messages = get_new_user_messages_count(request.session_id, request.messages, db)
        
        # 统计用户今天已经奖励过的消息数量
        user_message_count_today = count_rewarded_user_messages_today(current_user.user_id, db)
        
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
        
        # 初始化奖励信息
        star_reward = StarRewardInfo()
        
        # 只有当确实有新的用户消息时才进行处理
        if new_user_messages > 0:
            try:
                star_service = StarPointService(db)
                user_points = star_service.get_or_create_user_points(current_user.user_id)
                daily_limits = star_service.get_daily_limits(current_user.user_id)
                
                # 计算这次新增用户消息应该获得的奖励
                total_reward_points = 0
                
                for i in range(new_user_messages):
                    # 计算这是用户今天第几条消息（基于已奖励的消息数量）
                    message_number = user_message_count_today + i + 1
                    reward_for_this_message = calculate_single_message_reward(message_number)
                    total_reward_points += reward_for_this_message
                    
                    print(f"📝 用户消息 #{message_number}: +{reward_for_this_message}星点")
                
                # 前7条用户消息显示toast提示
                show_toast = (user_message_count_today + new_user_messages) <= 7
                
                # 检查今日聊天积分限制（最多10星点）
                if daily_limits.emotion_chat_points + total_reward_points <= 10 and total_reward_points > 0:
                    # 更新用户积分
                    user_points.current_points += total_reward_points
                    user_points.total_earned += total_reward_points
                    
                    # 更新每日限制
                    daily_limits.emotion_chat_count += new_user_messages
                    daily_limits.emotion_chat_points += total_reward_points
                    
                    # 添加积分日志
                    star_service.add_point_log(
                        user_id=current_user.user_id,
                        action=StarPointAction.EMOTION_CHAT_PREMIUM if user_message_count_today + 1 <= 3 else StarPointAction.EMOTION_CHAT_NORMAL,
                        points_change=total_reward_points,
                        source_type=SourceType.CHAT,
                        source_id=str(existing_session.id)
                    )
                    
                    star_reward = StarRewardInfo(
                        earned_points=total_reward_points,
                        is_rewarded=True,
                        action_type="emotion_chat",
                        description=f"聊天互动获得{total_reward_points}星点",
                        show_toast=show_toast
                    )
                    print(f"⭐ 聊天奖励成功: {total_reward_points}星点")
                else:
                    # 没有获得奖励，但前5条消息仍需要显示提示
                    if total_reward_points == 0:
                        # 更新消息计数（即使没有奖励积分）
                        daily_limits.emotion_chat_count += new_user_messages
                        
                        star_reward = StarRewardInfo(
                            earned_points=0,
                            is_rewarded=False,
                            action_type="emotion_chat",
                            description="聊天互动暂无奖励",
                            show_toast=show_toast
                        )
                        print(f"⭐ 聊天消息超出奖励范围")
                    else:
                        # 达到积分上限
                        star_reward = StarRewardInfo(
                            earned_points=0,
                            is_rewarded=False,
                            action_type="emotion_chat",
                            description="今日聊天奖励已达上限",
                            show_toast=show_toast
                        )
                        print(f"⭐ 聊天奖励已达到今日上限(10星点)")
            except Exception as e:
                print(f"❌ 聊天奖励失败: {str(e)}")
        
        db.commit()
        db.refresh(existing_session)
        print(f"✅ 会话更新完成: {existing_session.id}")
        
        # 如果检测到风险或会话已启用自动保存，则生成心理评估报告
        if has_risk or existing_session.auto_save_enabled:
            print(f"🧠 触发心理评估报告生成 - 会话ID: {existing_session.id}")
            background_tasks.add_task(generate_psychological_report_task, existing_session.id)
        
        # 创建包含星点奖励信息的响应
        result = ChatSessionWithStarResponse(**existing_session.__dict__, star_reward=star_reward)
        return result
    
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
    
    # 对于新会话，所有用户消息都是新的
    new_user_messages = sum(1 for msg in request.messages if msg.role == "user")
    
    # 统计用户今天已经奖励过的消息数量
    user_message_count_today = count_rewarded_user_messages_today(current_user.user_id, db)
    
    # 初始化奖励信息
    star_reward = StarRewardInfo()
    
    # 只有当确实有新的用户消息时才进行处理
    if new_user_messages > 0:
        try:
            star_service = StarPointService(db)
            user_points = star_service.get_or_create_user_points(current_user.user_id)
            daily_limits = star_service.get_daily_limits(current_user.user_id)
            
            # 计算这次新增用户消息应该获得的奖励
            total_reward_points = 0
            
            for i in range(new_user_messages):
                # 计算这是用户今天第几条消息（基于已奖励的消息数量）
                message_number = user_message_count_today + i + 1
                reward_for_this_message = calculate_single_message_reward(message_number)
                total_reward_points += reward_for_this_message
                
                print(f"📝 用户消息 #{message_number}: +{reward_for_this_message}星点")
            
            # 前7条用户消息显示toast提示
            show_toast = (user_message_count_today + new_user_messages) <= 7
            
            # 检查今日聊天积分限制（最多10星点）
            if daily_limits.emotion_chat_points + total_reward_points <= 10 and total_reward_points > 0:
                # 更新用户积分
                user_points.current_points += total_reward_points
                user_points.total_earned += total_reward_points
                
                # 更新每日限制
                daily_limits.emotion_chat_count += new_user_messages
                daily_limits.emotion_chat_points += total_reward_points
                
                # 添加积分日志
                star_service.add_point_log(
                    user_id=current_user.user_id,
                    action=StarPointAction.EMOTION_CHAT_PREMIUM if user_message_count_today + 1 <= 3 else StarPointAction.EMOTION_CHAT_NORMAL,
                    points_change=total_reward_points,
                    source_type=SourceType.CHAT,
                    source_id=str(chat_session.id)
                )
                
                star_reward = StarRewardInfo(
                    earned_points=total_reward_points,
                    is_rewarded=True,
                    action_type="emotion_chat",
                    description=f"聊天互动获得{total_reward_points}星点",
                    show_toast=show_toast
                )
                print(f"⭐ 聊天奖励成功: {total_reward_points}星点")
            else:
                # 没有获得奖励，但前5条消息仍需要显示提示
                if total_reward_points == 0:
                    # 更新消息计数（即使没有奖励积分）
                    daily_limits.emotion_chat_count += new_user_messages
                    
                    star_reward = StarRewardInfo(
                        earned_points=0,
                        is_rewarded=False,
                        action_type="emotion_chat",
                        description="聊天互动暂无奖励",
                        show_toast=show_toast
                    )
                    print(f"⭐ 聊天消息超出奖励范围")
                else:
                    # 达到积分上限
                    star_reward = StarRewardInfo(
                        earned_points=0,
                        is_rewarded=False,
                        action_type="emotion_chat",
                        description="今日聊天奖励已达上限",
                        show_toast=show_toast
                    )
                    print(f"⭐ 聊天奖励已达到今日上限(10星点)")
        except Exception as e:
            print(f"❌ 聊天奖励失败: {str(e)}")
    
    db.commit()
    db.refresh(chat_session)
    
    # 如果检测到风险，则生成心理评估报告
    if has_risk:
        print(f"🧠 触发心理评估报告生成 - 新会话ID: {chat_session.id}")
        background_tasks.add_task(generate_psychological_report_task, chat_session.id)
    
    # 创建包含星点奖励信息的响应
    result = ChatSessionWithStarResponse(**chat_session.__dict__, star_reward=star_reward)
    return result
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
