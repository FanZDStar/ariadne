"""
防护技能训练相关的路由和视图
"""
from flask import Blueprint, request, jsonify
from app.services.protection_drill_service import ProtectionDrillService
from app.utils.response import success_response, error_response
import uuid

protection_drill_bp = Blueprint('protection_drill', __name__, url_prefix='/api/protection-drill')

@protection_drill_bp.route('/training-types', methods=['GET'])
def get_training_types():
    """获取所有训练类型"""
    try:
        service = ProtectionDrillService()
        training_types = service.get_all_training_types()
        return success_response(data=training_types)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/start-session', methods=['POST'])
def start_training_session():
    """开始训练会话"""
    try:
        data = request.get_json()
        training_type_id = data.get('training_type_id')
        user_id = data.get('user_id')  # 可选，如果有用户系统
        
        if not training_type_id:
            return error_response(message="训练类型ID不能为空")
        
        service = ProtectionDrillService()
        session_data = service.start_training_session(training_type_id, user_id)
        return success_response(data=session_data)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/questions/<session_uuid>', methods=['GET'])
def get_session_questions(session_uuid):
    """获取训练会话的题目"""
    try:
        service = ProtectionDrillService()
        questions = service.get_session_questions(session_uuid)
        return success_response(data=questions)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    try:
        data = request.get_json()
        session_uuid = data.get('session_uuid')
        question_id = data.get('question_id')
        selected_option_id = data.get('selected_option_id')
        
        if not all([session_uuid, question_id, selected_option_id]):
            return error_response(message="缺少必要参数")
        
        service = ProtectionDrillService()
        result = service.submit_answer(session_uuid, question_id, selected_option_id)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/session-result/<session_uuid>', methods=['GET'])
def get_session_result(session_uuid):
    """获取训练会话结果"""
    try:
        service = ProtectionDrillService()
        result = service.get_session_result(session_uuid)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/complete-session', methods=['POST'])
def complete_session():
    """完成训练会话"""
    try:
        data = request.get_json()
        session_uuid = data.get('session_uuid')
        
        if not session_uuid:
            return error_response(message="会话UUID不能为空")
        
        service = ProtectionDrillService()
        result = service.complete_session(session_uuid)
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))

@protection_drill_bp.route('/user-history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """获取用户训练历史"""
    try:
        service = ProtectionDrillService()
        history = service.get_user_training_history(user_id)
        return success_response(data=history)
    except Exception as e:
        return error_response(message=str(e))
