"""
星星积分系统服务
"""
import random
from datetime import date, datetime
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from dataclasses import dataclass

from app.models.star_points import UserStarPoints, StarPointLog, DailyStarLimits
from app.models.user import User
from app.utils.star_point_types import (
    StarPointAction, SourceType, PointReward,
    get_reward_config, get_action_display_name, is_daily_limited
)

@dataclass
class StarPointResult:
    """星点奖励结果"""
    rewarded: bool
    message: str
    points_awarded: int


class StarPointService:
    """星星积分服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_points(self, user_id: int) -> Optional[UserStarPoints]:
        """获取用户积分信息"""
        return self.db.query(UserStarPoints).filter(UserStarPoints.user_id == user_id).first()
    
    def create_user_points(self, user_id: int, initial_points: int = 10) -> UserStarPoints:
        """为用户创建积分记录"""
        user_points = UserStarPoints(
            user_id=user_id,
            current_points=initial_points,
            total_earned=initial_points,
            total_spent=0
        )
        self.db.add(user_points)
        self.db.commit()
        self.db.refresh(user_points)
        
        # 添加初始积分日志
        self.add_point_log(
            user_id=user_id,
            action=StarPointAction.INITIAL_REWARD,
            points_change=initial_points,
            source_type=SourceType.SYSTEM
        )
        
        return user_points
    
    def get_or_create_user_points(self, user_id: int) -> UserStarPoints:
        """获取或创建用户积分记录"""
        user_points = self.get_user_points(user_id)
        if not user_points:
            user_points = self.create_user_points(user_id)
        return user_points
    
    def get_daily_limits(self, user_id: int, target_date: date = None) -> DailyStarLimits:
        """获取或创建用户每日限制记录"""
        if target_date is None:
            target_date = date.today()
            
        daily_limits = self.db.query(DailyStarLimits).filter(
            DailyStarLimits.user_id == user_id,
            DailyStarLimits.date == target_date
        ).first()
        
        if not daily_limits:
            daily_limits = DailyStarLimits(user_id=user_id, date=target_date)
            self.db.add(daily_limits)
            self.db.commit()
            self.db.refresh(daily_limits)
            
        return daily_limits
    
    def add_point_log(self, user_id: int, action: StarPointAction, points_change: int, 
                      source_id: str = None, source_type: SourceType = None, 
                      description: str = None) -> StarPointLog:
        """添加积分变动日志"""
        if description is None:
            description = get_action_display_name(action)
            
        log = StarPointLog(
            user_id=user_id,
            action_type=action.value,
            points_change=points_change,
            description=description,
            source_id=source_id,
            source_type=source_type.value if source_type else None
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
    
    def has_rewarded_today_for_source(self, user_id: int, action: StarPointAction, source_id: str) -> bool:
        """检查今天是否已经为特定来源ID奖励过积分"""
        today = date.today()
        return self.db.query(StarPointLog).filter(
            StarPointLog.user_id == user_id,
            StarPointLog.action_type == action.value,
            StarPointLog.source_id == source_id,
            func.date(StarPointLog.created_at) == today
        ).first() is not None

    def can_earn_points(self, user_id: int, action: StarPointAction, source_id: str = None) -> Tuple[bool, str]:
        """检查用户是否可以获得积分"""
        reward_config = get_reward_config(action)
        if not reward_config:
            return False, "未知的行为类型"
        
        # 检查每日限制
        if is_daily_limited(action):
            daily_limits = self.get_daily_limits(user_id)
            
            # 根据不同的行为类型检查限制
            if action == StarPointAction.DAILY_LOGIN and daily_limits.daily_login:
                return False, "今日已经获得登录积分"
            elif action == StarPointAction.MOOD_TRACKING and daily_limits.mood_tracking:
                return False, "今日已经获得心情记录积分"
            elif action == StarPointAction.DIARY_FIRST and daily_limits.diary_count >= 1:
                return False, "今日第一篇日记积分已获得"
            elif action == StarPointAction.DIARY_ADDITIONAL and daily_limits.diary_count >= 3:
                return False, "今日日记积分已达上限"
            elif action == StarPointAction.BACKGROUND_CHANGE and daily_limits.background_change:
                return False, "今日已经获得背景修改积分"
            elif action == StarPointAction.EMOTION_CHAT_PREMIUM and daily_limits.emotion_chat_count >= 3:
                return False, "今日情感对话高级积分已获得"
            elif action == StarPointAction.EMOTION_CHAT_NORMAL and daily_limits.emotion_chat_points >= 10:
                return False, "今日情感对话积分已达上限"
            elif action == StarPointAction.SKILL_TRAINING and daily_limits.skill_training:
                return False, "今日已经获得技能训练积分"
            elif action == StarPointAction.RELATIONSHIP_ASSESSMENT and daily_limits.relationship_assessment:
                return False, "今日已经获得关系评估积分"
            elif action == StarPointAction.PERSONALIZED_ADVICE and daily_limits.personalized_advice:
                return False, "今日已经获得个性化建议积分"
            elif action == StarPointAction.AI_SCENARIO_TRAINING and daily_limits.ai_scenario_training:
                return False, "今日已经获得AI情景训练积分"
            elif action == StarPointAction.PROTECTION_TRAINING and daily_limits.protection_training:
                return False, "今日已经获得防护技能训练积分"
            elif action == StarPointAction.TREE_HOLE_INTERACTION:
                # 检查今日互动次数是否已达上限
                if daily_limits.tree_hole_interaction_count >= 3:
                    return False, "今日树洞互动积分已达上限"
                # 检查今天是否已经为这个悄悄话ID奖励过
                if source_id and self.has_rewarded_today_for_source(user_id, action, source_id):
                    return False, "今日已为此悄悄话获得过互动积分"
            elif action == StarPointAction.TREE_HOLE_WHISPER and daily_limits.tree_hole_whisper:
                return False, "今日已经获得悄悄话积分"
            elif action == StarPointAction.SKILL_FAVORITE and daily_limits.skill_favorite:
                return False, "今日已经获得技能收藏积分"
        
        # 检查概率
        if reward_config.probability < 1.0:
            if random.random() > reward_config.probability:
                return False, f"未达到获得积分的概率要求 ({reward_config.probability*100}%)"
        
        return True, "可以获得积分"
    
    def award_points(self, user_id: int, action: StarPointAction, 
                     source_id: str = None, source_type: SourceType = None) -> StarPointResult:
        """奖励用户积分"""
        # 检查是否可以获得积分
        can_earn, message = self.can_earn_points(user_id, action, source_id)
        if not can_earn:
            return StarPointResult(rewarded=False, message=message, points_awarded=0)
        
        reward_config = get_reward_config(action)
        points = reward_config.points
        
        # 获取或创建用户积分记录
        user_points = self.get_or_create_user_points(user_id)
        
        # 更新积分
        user_points.current_points += points
        user_points.total_earned += points
        
        # 更新每日限制
        if is_daily_limited(action):
            daily_limits = self.get_daily_limits(user_id)
            self._update_daily_limits(daily_limits, action, points)
        
        # 添加日志
        self.add_point_log(
            user_id=user_id,
            action=action,
            points_change=points,
            source_id=source_id,
            source_type=source_type
        )
        
        self.db.commit()
        return StarPointResult(
            rewarded=True, 
            message=f"获得 {points} 个星星！{reward_config.description}", 
            points_awarded=points
        )
    
    def spend_points(self, user_id: int, points: int, description: str, 
                     source_id: str = None, source_type: SourceType = None) -> Tuple[bool, str]:
        """消费积分"""
        user_points = self.get_user_points(user_id)
        if not user_points:
            return False, "用户积分记录不存在"
        
        if user_points.current_points < points:
            return False, f"积分不足，当前积分: {user_points.current_points}，需要: {points}"
        
        # 扣除积分
        user_points.current_points -= points
        user_points.total_spent += points
        
        # 添加消费日志
        self.add_point_log(
            user_id=user_id,
            action=StarPointAction.MASCOT_PURCHASE,  # 或其他消费类型
            points_change=-points,
            source_id=source_id,
            source_type=source_type,
            description=description
        )
        
        self.db.commit()
        return True, f"成功消费 {points} 个星星"
    
    def get_point_logs(self, user_id: int, limit: int = 50) -> List[StarPointLog]:
        """获取用户积分日志"""
        return self.db.query(StarPointLog).filter(
            StarPointLog.user_id == user_id
        ).order_by(StarPointLog.created_at.desc()).limit(limit).all()
    
    def _update_daily_limits(self, daily_limits: DailyStarLimits, action: StarPointAction, points: int):
        """更新每日限制记录"""
        if action == StarPointAction.DAILY_LOGIN:
            daily_limits.daily_login = True
        elif action == StarPointAction.MOOD_TRACKING:
            daily_limits.mood_tracking = True
        elif action in [StarPointAction.DIARY_FIRST, StarPointAction.DIARY_ADDITIONAL]:
            daily_limits.diary_count += 1
        elif action == StarPointAction.BACKGROUND_CHANGE:
            daily_limits.background_change = True
        elif action in [StarPointAction.EMOTION_CHAT_PREMIUM, StarPointAction.EMOTION_CHAT_NORMAL]:
            daily_limits.emotion_chat_count += 1
            daily_limits.emotion_chat_points += points
        elif action == StarPointAction.SKILL_TRAINING:
            daily_limits.skill_training = True
        elif action == StarPointAction.RELATIONSHIP_ASSESSMENT:
            daily_limits.relationship_assessment = True
        elif action == StarPointAction.PERSONALIZED_ADVICE:
            daily_limits.personalized_advice = True
        elif action == StarPointAction.AI_SCENARIO_TRAINING:
            daily_limits.ai_scenario_training = True
        elif action == StarPointAction.PROTECTION_TRAINING:
            daily_limits.protection_training = True
        elif action == StarPointAction.TREE_HOLE_INTERACTION:
            daily_limits.tree_hole_interaction_count += 1
        elif action == StarPointAction.TREE_HOLE_WHISPER:
            daily_limits.tree_hole_whisper = True
        elif action == StarPointAction.SKILL_FAVORITE:
            daily_limits.skill_favorite = True


def get_star_point_service(db: Session) -> StarPointService:
    """获取星星积分服务实例"""
    return StarPointService(db)
