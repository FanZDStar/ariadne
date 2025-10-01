from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.post("/sessions")
async def create_practice_session(
    session_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的人际沟通练习会话"""
    try:
        # 使用原生SQL
        from sqlalchemy import text
        
        insert_sql = """
        INSERT INTO interpersonal_practice_sessions 
        (user_id, title, scenario_id, scenario_name, 
         messages, message_count, session_duration, practice_type, is_completed)
        VALUES (:user_id, :title, :scenario_id, :scenario_name, 
         :messages, :message_count, :session_duration, :practice_type, :is_completed)
        """
        
        result = db.execute(text(insert_sql), {
            'user_id': current_user.user_id,
            'title': session_data.get('session_title', '未命名练习'),
            'scenario_id': session_data.get('practice_scenario', 'general'),
            'scenario_name': session_data.get('practice_scenario_name', '通用练习'),
            'messages': json.dumps(session_data.get('messages', [])),
            'message_count': len(session_data.get('messages', [])),
            'session_duration': session_data.get('practice_duration', 0),
            'practice_type': 'communication',  # 固定使用communication，这是数据库ENUM的有效值
            'is_completed': 1
        })
        
        db.commit()
        
        return {
            "id": result.lastrowid,
            "message": "练习会话创建成功",
            "title": session_data.get('session_title', '未命名练习')
        }
        
    except Exception as e:
        db.rollback()
        print(f"创建会话出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@router.get("/sessions")
async def get_practice_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取练习会话列表"""
    try:
        from sqlalchemy import text
        
        query_sql = """
        SELECT id, title, scenario_id, scenario_name,
               message_count, session_duration, created_at, is_completed
        FROM interpersonal_practice_sessions 
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT 50
        """
        
        result = db.execute(text(query_sql), {'user_id': current_user.user_id})
        sessions = []
        
        for row in result:
            sessions.append({
                'id': row[0],
                'session_title': row[1],
                'practice_scenario': row[2],
                'practice_scenario_name': row[3],
                'total_messages': row[4],
                'practice_duration': row[5],
                'created_at': row[6].isoformat() if row[6] else None,
                'completion_status': 'completed' if row[7] else 'in_progress'
            })
        
        return {
            "sessions": sessions,
            "total": len(sessions),
            "skip": 0,
            "limit": 50
        }
        
    except Exception as e:
        print(f"获取会话列表出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@router.get("/sessions/{session_id}")
async def get_practice_session_detail(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个练习会话的详细信息"""
    try:
        from sqlalchemy import text
        
        query_sql = """
        SELECT id, title, scenario_id, scenario_name,
               messages, message_count, session_duration, 
               created_at, is_completed, practice_type
        FROM interpersonal_practice_sessions 
        WHERE id = :session_id AND user_id = :user_id
        """
        
        result = db.execute(text(query_sql), {
            'session_id': session_id,
            'user_id': current_user.user_id
        })
        
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="练习会话不存在")
        
        # 解析JSON消息
        messages = json.loads(row[4]) if row[4] else []
        
        session_detail = {
            'id': row[0],
            'session_title': row[1],
            'practice_scenario': row[2],
            'practice_scenario_name': row[3],
            'messages': messages,
            'total_messages': row[5],
            'practice_duration': row[6],
            'created_at': row[7].isoformat() if row[7] else None,
            'completion_status': 'completed' if row[8] else 'in_progress',
            'practice_type': row[9]
        }
        
        return session_detail
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"获取会话详情出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取会话详情失败: {str(e)}")

