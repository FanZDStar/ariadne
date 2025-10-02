"""
防护训练服务
处理防护训练相关的业务逻辑
"""
import random
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.core.database import get_db_connection
import logging

logger = logging.getLogger(__name__)

class ProtectionDrillService:
    """防护训练服务类"""
    
    @staticmethod
    def get_training_types() -> List[Dict[str, Any]]:
        """获取所有训练类型"""
        try:
            with get_db_connection() as conn:
                query = """
                SELECT id, title, icon, description, level, duration, skills, objectives, risk_signals, strategies
                FROM protection_training_types 
                ORDER BY id
                """
                cursor = conn.cursor()
                cursor.execute(query)
                types = []
                for row in cursor.fetchall():
                    types.append({
                        'id': row[0],
                        'title': row[1],
                        'icon': row[2],
                        'description': row[3],
                        'level': row[4],
                        'duration': row[5],
                        'skills': json.loads(row[6]) if row[6] else [],
                        'objectives': json.loads(row[7]) if row[7] else [],
                        'risk_signals': json.loads(row[8]) if row[8] else [],
                        'strategies': json.loads(row[9]) if row[9] else []
                    })
                return types
        except Exception as e:
            logger.error(f"获取训练类型失败: {e}")
            return []  # 返回空列表而不是抛出异常
    
    @staticmethod
    def get_training_questions(training_type_id: int, count: int = 8) -> List[Dict[str, Any]]:
        """获取指定类型的随机题目"""
        try:
            with get_db_connection() as conn:
                # 随机获取指定数量的题目
                query = """
                SELECT id, title, description, dialogue, question_title, question_text, 
                       options, correct_analysis, risk_explanation, protection_advice, 
                       better_choice, difficulty
                FROM protection_drill_questions 
                WHERE training_type_id = %s
                ORDER BY RAND()
                LIMIT %s
                """
                cursor = conn.cursor()
                cursor.execute(query, (training_type_id, count))
                
                questions = []
                for row in cursor.fetchall():
                    questions.append({
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'dialogue': json.loads(row[3]) if row[3] else [],
                        'question_title': row[4],
                        'question_text': row[5],
                        'options': json.loads(row[6]) if row[6] else [],
                        'correct_analysis': row[7],
                        'risk_explanation': row[8],
                        'protection_advice': json.loads(row[9]) if row[9] else [],
                        'better_choice': row[10],
                        'difficulty': row[11]
                    })
                return questions
        except Exception as e:
            logger.error(f"获取训练题目失败: {e}")
            return []
