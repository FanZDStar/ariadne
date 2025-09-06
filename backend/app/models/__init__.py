#file:ariadne/backend/app/models/__init__.py

# 导入所有模型，确保SQLAlchemy能够正确识别关系
from .user import User
from .chat_history import ChatSession, ChatMessage
from .crisis_warning import CrisisWarning
from .risk_assessment_report import RiskAssessmentReport
from .emotional_diary import EmotionalDiary
from .diary_image import DiaryImage
from .user_feedback import UserFeedback
from .feedback_image import FeedbackImage
from .tree_hole import TreeHoleWhisper
from .tree_hole_chat import TreeHoleChat

# 导出所有模型
__all__ = [
    "User",
    "ChatSession", 
    "ChatMessage",
    "CrisisWarning",
    "RiskAssessmentReport",
    "EmotionalDiary",
    "DiaryImage", 
    "UserFeedback",
    "FeedbackImage",
    "TreeHoleWhisper",
    "TreeHoleChat"
]