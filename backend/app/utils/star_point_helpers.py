"""
积分系统工具函数
供其他模块方便调用
"""
from typing import Tuple
from sqlalchemy.orm import Session
from app.utils.star_point_types import StarPointAction, SourceType


def try_award_points(
    db: Session, 
    user_id: int, 
    action: StarPointAction,
    source_id: str = None,
    source_type: SourceType = None,
    silent: bool = True
) -> Tuple[bool, str, int]:
    """
    尝试奖励积分，失败时不抛出异常
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        action: 积分行为类型
        source_id: 来源ID
        source_type: 来源类型
        silent: 是否静默处理异常（默认True）
    
    Returns:
        (success, message, points_awarded)
    """
    try:
        from app.services.star_point_service import get_star_point_service
        service = get_star_point_service(db)
        return service.award_points(user_id, action, source_id, source_type)
    except Exception as e:
        if not silent:
            raise e
        return False, f"积分奖励失败: {str(e)}", 0


def try_spend_points(
    db: Session, 
    user_id: int, 
    points: int, 
    description: str,
    source_id: str = None,
    source_type: SourceType = None,
    silent: bool = True
) -> Tuple[bool, str]:
    """
    尝试消费积分，失败时不抛出异常
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        points: 消费积分数量
        description: 消费描述
        source_id: 来源ID
        source_type: 来源类型
        silent: 是否静默处理异常（默认True）
    
    Returns:
        (success, message)
    """
    try:
        from app.services.star_point_service import get_star_point_service
        service = get_star_point_service(db)
        return service.spend_points(user_id, points, description, source_id, source_type)
    except Exception as e:
        if not silent:
            raise e
        return False, f"积分消费失败: {str(e)}"


def get_user_current_points(db: Session, user_id: int) -> int:
    """获取用户当前积分数量"""
    try:
        from app.services.star_point_service import get_star_point_service
        service = get_star_point_service(db)
        user_points = service.get_or_create_user_points(user_id)
        return user_points.current_points
    except Exception:
        return 0


# 常用的积分奖励函数
def award_daily_login(db: Session, user_id: int) -> Tuple[bool, str, int]:
    """每日登录积分"""
    return try_award_points(db, user_id, StarPointAction.DAILY_LOGIN, source_type=SourceType.LOGIN)


def award_mood_tracking(db: Session, user_id: int, mood_id: str = None) -> Tuple[bool, str, int]:
    """心情记录积分"""
    return try_award_points(db, user_id, StarPointAction.MOOD_TRACKING, source_id=mood_id, source_type=SourceType.MOOD)


def award_diary_points(db: Session, user_id: int, diary_id: str, is_first: bool = True) -> Tuple[bool, str, int]:
    """日记积分"""
    action = StarPointAction.DIARY_FIRST if is_first else StarPointAction.DIARY_ADDITIONAL
    return try_award_points(db, user_id, action, source_id=diary_id, source_type=SourceType.DIARY)


def award_background_change(db: Session, user_id: int, background_id: str = None) -> Tuple[bool, str, int]:
    """背景修改积分"""
    return try_award_points(db, user_id, StarPointAction.BACKGROUND_CHANGE, source_id=background_id, source_type=SourceType.DIARY)


def award_emotion_chat(db: Session, user_id: int, session_id: str, is_premium: bool = True) -> Tuple[bool, str, int]:
    """情感对话积分"""
    action = StarPointAction.EMOTION_CHAT_PREMIUM if is_premium else StarPointAction.EMOTION_CHAT_NORMAL
    return try_award_points(db, user_id, action, source_id=session_id, source_type=SourceType.CHAT)


def award_skill_training(db: Session, user_id: int, skill_id: str = None) -> Tuple[bool, str, int]:
    """技能训练积分"""
    return try_award_points(db, user_id, StarPointAction.SKILL_TRAINING, source_id=skill_id, source_type=SourceType.SKILL)


def award_skill_favorite(db: Session, user_id: int, skill_id: str) -> Tuple[bool, str, int]:
    """技能收藏积分（50%概率）"""
    return try_award_points(db, user_id, StarPointAction.SKILL_FAVORITE, source_id=skill_id, source_type=SourceType.SKILL)


def award_scenario_practice(db: Session, user_id: int, session_id: str) -> Tuple[bool, str, int]:
    """情景演练积分"""
    return try_award_points(db, user_id, StarPointAction.SCENARIO_PRACTICE, source_id=session_id, source_type=SourceType.PRACTICE)


def award_tree_hole_interaction(db: Session, user_id: int, interaction_id: str) -> Tuple[bool, str, int]:
    """树洞互动积分"""
    return try_award_points(db, user_id, StarPointAction.TREE_HOLE_INTERACTION, source_id=interaction_id, source_type=SourceType.TREE_HOLE)


def award_tree_hole_whisper(db: Session, user_id: int, whisper_id: str) -> Tuple[bool, str, int]:
    """发表悄悄话积分"""
    return try_award_points(db, user_id, StarPointAction.TREE_HOLE_WHISPER, source_id=whisper_id, source_type=SourceType.TREE_HOLE)
