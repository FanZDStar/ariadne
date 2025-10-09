#file:ariadne/backend/app/models/__init__.py

# 导入所有模型，确保SQLAlchemy能够正确识别关系
from .user import User
from .chat_history import ChatSession, ChatMessage
from .crisis_warning import CrisisWarning
from .risk_assessment_report import RiskAssessmentReport
from .relationship_assessment_report import RelationshipAssessmentReport  # 新增关系评估报告模型
from .emotional_diary import EmotionalDiary
from .diary_image import DiaryImage
from .user_feedback import UserFeedback
from .feedback_image import FeedbackImage
from .tree_hole import TreeHoleWhisper
from .tree_hole_chat import TreeHoleChat
from .skill_categories import SkillCategory
from .skills import Skill
from .user_skill_progress import UserSkillProgress
from .learning_paths import LearningPath
from .user_learning_path_progress import UserLearningPathProgress
from .achievements import Achievement
from .user_achievements import UserAchievement
from .mood_tracker import MoodTracker
from .user_diary_backgrounds import UserDiaryBackground
from .interpersonal_practice_session import InterpersonalPracticeSession
from .protection_drill_report import ProtectionDrillReport
from .star_points import UserStarPoints, StarPointLog, DailyStarLimits
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
    "TreeHoleChat",
    "SkillCategory",
    "Skill",
    "UserSkillProgress",
    "LearningPath",
    "UserLearningPathProgress",
    "Achievement",
    "UserAchievement",
    "MoodTracker",
    "UserDiaryBackground",
    "InterpersonalPracticeSession",
    "ProtectionDrillReport",
    "UserStarPoints",
    "StarPointLog", 
    "DailyStarLimits"
]