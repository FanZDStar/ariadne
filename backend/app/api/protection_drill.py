"""
防护训练API路由
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from app.services.protection_drill_service import ProtectionDrillService

logger = logging.getLogger(__name__)

def get_performance_message(accuracy_rate):
    """根据准确率生成表现评价信息"""
    if accuracy_rate >= 90:
        return "表现优秀！你已经具备了很强的防护意识和风险识别能力。"
    elif accuracy_rate >= 80:
        return "表现良好！你具备了基本的防护能力，继续保持！"
    elif accuracy_rate >= 70:
        return "表现一般，需要加强对风险信号的识别能力。"
    elif accuracy_rate >= 60:
        return "表现有待提高，建议多练习提升防护意识。"
    else:
        return "需要继续努力提升防护意识和风险识别能力。"

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
        
        # 从数据库获取题目信息并验证答案
        from app.services.protection_drill_service import ProtectionDrillService
        
        # 获取题目详细信息
        question_info = ProtectionDrillService.get_question_by_id(question_id)
        if not question_info:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        # 验证答案
        is_correct = False
        correct_option = None
        user_option = None
        
        for option in question_info.get('options', []):
            if option.get('id') == selected_option_id:
                user_option = option
            if option.get('isCorrect', False):
                correct_option = option
        
        if user_option and correct_option:
            is_correct = user_option.get('id') == correct_option.get('id')
        
        # 构建反馈数据
        feedback = {
            "is_correct": is_correct,
            "analysis": question_info.get('correct_analysis', '答案分析') if is_correct else '这个答案需要再考虑一下。让我们来看看正确的分析。',
            "explanation": correct_option.get('description', '') if correct_option else '',
            "risk_explanation": question_info.get('risk_explanation', ''),
            "protection_advice": question_info.get('protection_advice', []),
            "correct_answer": correct_option.get('text', '') if correct_option else '',
            "correct_option_id": correct_option.get('id') if correct_option else None,
            "better_choice": question_info.get('better_choice', ''),
            "user_answer": user_option.get('text', '') if user_option else '',
            "user_option_id": selected_option_id
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
        # 这里应该从实际的会话数据中获取结果
        # 暂时返回合理的模拟数据，实际应用中需要从数据库获取
        
        # 模拟根据会话ID获取实际答题数据
        # 实际实现时，这些数据应该从 protection_drill_sessions 表中获取
        total_questions = 8
        
        # 这里应该根据实际的答题记录计算正确答案数
        # 暂时使用随机值模拟，实际应该查询用户答题记录
        import random
        correct_answers = random.randint(5, 8)  # 临时模拟，实际需要从数据库计算
        
        accuracy_rate = (correct_answers / total_questions) * 100
        
        result = {
            "session_id": session_id,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy_rate": round(accuracy_rate, 1),
            "score": round(accuracy_rate, 1),
            "performance_message": get_performance_message(accuracy_rate),
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
