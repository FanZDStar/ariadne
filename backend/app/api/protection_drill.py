"""
防护训练API路由
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from app.services.protection_drill_service import ProtectionDrillService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/protection-drill", tags=["防护训练"])

@router.get("/training-types", summary="获取训练类型列表")
async def get_training_types():
    """获取所有防护训练类型"""
    try:
        types = ProtectionDrillService.get_training_types()
        return {
            "code": 200,
            "message": "获取成功",
            "data": types
        }
    except Exception as e:
        logger.error(f"获取训练类型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions/{training_type_id}", summary="获取训练题目")
async def get_training_questions(training_type_id: int, count: int = 8):
    """获取指定类型的随机训练题目"""
    try:
        if count < 1 or count > 20:
            raise HTTPException(status_code=400, detail="题目数量必须在1-20之间")
            
        questions = ProtectionDrillService.get_training_questions(training_type_id, count)
        if not questions:
            raise HTTPException(status_code=404, detail="该训练类型暂无题目")
            
        return {
            "code": 200,
            "message": "获取成功",
            "data": questions
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取训练题目失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/start", summary="开始训练会话")
async def start_training_session(request: dict):
    """开始新的训练会话"""
    try:
        training_type_id = request.get('training_type_id')
        if not training_type_id:
            raise HTTPException(status_code=400, detail="训练类型ID不能为空")
        
        # 生成会话ID
        import uuid
        session_uuid = str(uuid.uuid4())
        
        # 获取训练题目
        questions = ProtectionDrillService.get_training_questions(training_type_id, 8)
        if not questions:
            raise HTTPException(status_code=404, detail="该训练类型暂无题目")
        
        return {
            "code": 200,
            "message": "会话创建成功",
            "data": {
                "session_uuid": session_uuid,
                "training_type_id": training_type_id,
                "questions": questions
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建训练会话失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/answer", summary="提交答案")
async def submit_answer(session_id: str, request: dict):
    """提交题目答案"""
    try:
        question_id = request.get('question_id')
        selected_option_id = request.get('selected_option_id')
        
        if not question_id or not selected_option_id:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        # 这里可以添加答案验证逻辑
        # 暂时返回模拟的反馈数据
        feedback = {
            "is_correct": True,  # 可以根据实际答案验证
            "analysis": "答案分析",
            "explanation": "详细解释"
        }
        
        return {
            "code": 200,
            "message": "答案提交成功",
            "data": feedback
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"提交答案失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/complete", summary="完成训练")
async def complete_training_session(session_id: str):
    """完成训练会话并获取结果"""
    try:
        # 这里可以添加会话完成逻辑
        # 暂时返回模拟的结果数据
        result = {
            "session_id": session_id,
            "total_questions": 8,
            "correct_answers": 6,
            "score": 75,
            "completed_at": "2025-01-02T10:30:00Z"
        }
        
        return {
            "code": 200,
            "message": "训练完成",
            "data": result
        }
    except Exception as e:
        logger.error(f"完成训练会话失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
