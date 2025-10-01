from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from typing import List, Dict, Any

router = APIRouter()

@router.post("/sessions")
async def create_practice_session(
    session_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的人际沟通练习会话 - 简化版本"""
    try:
        # 直接使用原生SQL插入，避免ORM问题
        from sqlalchemy import text
        
        insert_sql = """
        INSERT INTO interpersonal_practice_sessions 
        (user_id, session_title, practice_scenario, practice_scenario_name, 
         messages, total_messages, practice_duration, practice_type, completion_status, created_at)
        VALUES (:user_id, :session_title, :practice_scenario, :practice_scenario_name, 
         :messages, :total_messages, :practice_duration, :practice_type, :completion_status, NOW())
        """
        
        import json
        
        result = db.execute(text(insert_sql), {
            'user_id': current_user.user_id,
            'session_title': session_data.get('session_title', '未命名练习'),
            'practice_scenario': session_data.get('practice_scenario', 'general'),
            'practice_scenario_name': session_data.get('practice_scenario_name', '通用练习'),
            'messages': json.dumps(session_data.get('messages', [])),
            'total_messages': len(session_data.get('messages', [])),
            'practice_duration': session_data.get('practice_duration', 0),
            'practice_type': session_data.get('practice_type', 'ai_dialog'),
            'completion_status': session_data.get('completion_status', 'completed')
        })
        
        db.commit()
        
        return {
            "id": result.lastrowid,
            "message": "练习会话创建成功",
            "session_title": session_data.get('session_title', '未命名练习')
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
    """获取练习会话列表 - 简化版本"""
    try:
        from sqlalchemy import text
        
        query_sql = """
        SELECT id, session_title, practice_scenario, practice_scenario_name,
               total_messages, practice_duration, created_at, completion_status
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
                'completion_status': row[7]
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
