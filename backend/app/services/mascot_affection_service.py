"""
看板娘好感度系统服务
"""
import random
from datetime import date, datetime
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from dataclasses import dataclass

from app.models.mascot_affection import (
    UserMascotAffection, MascotAffectionLog, MascotAffectionLevel, 
    DailyAffectionLimits, UserAffectionRewards
)
from app.models.user import User
from app.utils.affection_types import (
    MascotAffectionAction, AffectionSourceType, AffectionReward,
    get_affection_reward_config, get_affection_action_display_name, 
    is_affection_daily_limited, get_level_by_affection, 
    get_next_level_info, calculate_level_progress,
    get_outfit_affection_by_cost
)

@dataclass
class AffectionResult:
    """好感度奖励结果"""
    rewarded: bool
    message: str
    affection_awarded: int
    level_up: bool = False
    old_level: int = 1
    new_level: int = 1


class MascotAffectionService:
    """看板娘好感度服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_affection(self, user_id: int) -> Optional[UserMascotAffection]:
        """获取用户好感度信息"""
        return self.db.query(UserMascotAffection).filter(
            UserMascotAffection.user_id == user_id
        ).first()
    
    def create_user_affection(self, user_id: int, initial_affection: int = 0) -> UserMascotAffection:
        """为用户创建好感度记录"""
        user_affection = UserMascotAffection(
            user_id=user_id,
            current_affection=initial_affection,
            total_earned_affection=initial_affection,
            current_level=1,
            level_progress=0.0,
            next_level_required=100
        )
        self.db.add(user_affection)
        self.db.commit()
        self.db.refresh(user_affection)
        
        # 添加初始好感度日志
        if initial_affection > 0:
            self.add_affection_log(
                user_id=user_id,
                action=MascotAffectionAction.INITIAL_AFFECTION,
                affection_change=initial_affection,
                source_type=AffectionSourceType.SYSTEM
            )
        
        return user_affection
    
    def get_or_create_user_affection(self, user_id: int) -> UserMascotAffection:
        """获取或创建用户好感度记录"""
        user_affection = self.get_user_affection(user_id)
        if not user_affection:
            user_affection = self.create_user_affection(user_id)
        return user_affection
    
    def get_daily_affection_limits(self, user_id: int, target_date: date = None) -> DailyAffectionLimits:
        """获取或创建用户每日好感度限制记录"""
        if target_date is None:
            target_date = date.today()
            
        daily_limits = self.db.query(DailyAffectionLimits).filter(
            DailyAffectionLimits.user_id == user_id,
            DailyAffectionLimits.date == target_date
        ).first()
        
        if not daily_limits:
            daily_limits = DailyAffectionLimits(user_id=user_id, date=target_date)
            self.db.add(daily_limits)
            self.db.commit()
            self.db.refresh(daily_limits)
            
        return daily_limits
    
    def add_affection_log(self, user_id: int, action: MascotAffectionAction, 
                         affection_change: int, source_id: str = None, 
                         source_type: AffectionSourceType = None, 
                         description: str = None,
                         before_affection: int = 0, after_affection: int = 0,
                         before_level: int = 1, after_level: int = 1,
                         is_level_up: bool = False) -> MascotAffectionLog:
        """添加好感度变动日志"""
        if description is None:
            description = get_affection_action_display_name(action)
            
        log = MascotAffectionLog(
            user_id=user_id,
            action_type=action.value,
            affection_change=affection_change,
            before_affection=before_affection,
            after_affection=after_affection,
            before_level=before_level,
            after_level=after_level,
            is_level_up=is_level_up,
            description=description,
            source_id=source_id,
            source_type=source_type.value if source_type else None
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
    
    def check_daily_limit(self, user_id: int, action: MascotAffectionAction, 
                         source_id: str = None) -> Tuple[bool, str]:
        """检查用户今日是否可以获得好感度"""
        if not is_affection_daily_limited(action):
            return True, "无限制"
        
        daily_limits = self.get_daily_affection_limits(user_id)
        reward_config = get_affection_reward_config(action)
        
        if action == MascotAffectionAction.DAILY_LOGIN:
            if daily_limits.daily_login:
                return False, "今日已经获得登录好感度"
        elif action == MascotAffectionAction.EMOTION_CHAT:
            if daily_limits.emotion_chat_count >= reward_config.daily_limit:
                return False, "今日情感对话好感度已达上限"
        elif action == MascotAffectionAction.DIARY_COMPLETE:
            if daily_limits.diary_complete:
                return False, "今日已经获得日记好感度"
        elif action == MascotAffectionAction.MOOD_TRACKING:
            if daily_limits.mood_tracking:
                return False, "今日已经获得心情记录好感度"
        
        return True, "可以获得好感度"
    
    def update_daily_limits(self, user_id: int, action: MascotAffectionAction, 
                           affection_awarded: int):
        """更新每日限制记录"""
        daily_limits = self.get_daily_affection_limits(user_id)
        
        if action == MascotAffectionAction.DAILY_LOGIN:
            daily_limits.daily_login = True
        elif action == MascotAffectionAction.EMOTION_CHAT:
            daily_limits.emotion_chat_count += 1
            daily_limits.emotion_chat_affection += affection_awarded
        elif action == MascotAffectionAction.DIARY_COMPLETE:
            daily_limits.diary_complete = True
        elif action == MascotAffectionAction.MOOD_TRACKING:
            daily_limits.mood_tracking = True
        elif action in [MascotAffectionAction.OUTFIT_PURCHASE_CHEAP,
                       MascotAffectionAction.OUTFIT_PURCHASE_NORMAL,
                       MascotAffectionAction.OUTFIT_PURCHASE_PREMIUM,
                       MascotAffectionAction.OUTFIT_PURCHASE_LUXURY]:
            daily_limits.outfit_purchase_count += 1
            daily_limits.outfit_purchase_affection += affection_awarded
        
        daily_limits.total_daily_affection += affection_awarded
        self.db.commit()
    
    def calculate_level_change(self, current_affection: int, new_affection: int) -> dict:
        """计算等级变化"""
        old_level_info = get_level_by_affection(current_affection)
        new_level_info = get_level_by_affection(new_affection)
        
        old_level = old_level_info["level"]
        new_level = new_level_info["level"]
        is_level_up = new_level > old_level
        
        # 计算新的等级进度
        level_progress = calculate_level_progress(new_affection, new_level)
        
        # 获取下一等级所需好感度
        next_level_info = get_next_level_info(new_level)
        next_level_required = next_level_info["required_affection"] if next_level_info else new_affection
        
        return {
            "old_level": old_level,
            "new_level": new_level,
            "is_level_up": is_level_up,
            "level_progress": level_progress,
            "next_level_required": next_level_required
        }
    
    def award_affection(self, user_id: int, action: MascotAffectionAction,
                       source_id: str = None, source_type: AffectionSourceType = None,
                       custom_affection: int = None) -> AffectionResult:
        """奖励好感度"""
        # 检查是否可以获得好感度
        can_reward, reason = self.check_daily_limit(user_id, action, source_id)
        if not can_reward:
            return AffectionResult(
                rewarded=False,
                message=reason,
                affection_awarded=0,
                level_up=False
            )
        
        # 获取奖励配置
        reward_config = get_affection_reward_config(action)
        if not reward_config:
            return AffectionResult(
                rewarded=False,
                message="未知的好感度行为类型",
                affection_awarded=0,
                level_up=False
            )
        
        # 确定奖励好感度值
        affection_to_award = custom_affection if custom_affection is not None else reward_config.affection
        
        # 概率检查
        if random.random() > reward_config.probability:
            return AffectionResult(
                rewarded=False,
                message="概率未命中",
                affection_awarded=0,
                level_up=False
            )
        
        # 获取用户当前好感度
        user_affection = self.get_or_create_user_affection(user_id)
        old_affection = user_affection.current_affection
        old_level = user_affection.current_level
        
        # 计算新的好感度
        new_affection = old_affection + affection_to_award
        
        # 计算等级变化
        level_change = self.calculate_level_change(old_affection, new_affection)
        
        # 更新用户好感度
        user_affection.current_affection = new_affection
        user_affection.total_earned_affection += affection_to_award
        user_affection.current_level = level_change["new_level"]
        user_affection.level_progress = level_change["level_progress"]
        user_affection.next_level_required = level_change["next_level_required"]
        user_affection.last_interaction_at = datetime.now()
        
        self.db.commit()
        
        # 添加日志
        self.add_affection_log(
            user_id=user_id,
            action=action,
            affection_change=affection_to_award,
            source_id=source_id,
            source_type=source_type,
            before_affection=old_affection,
            after_affection=new_affection,
            before_level=old_level,
            after_level=level_change["new_level"],
            is_level_up=level_change["is_level_up"]
        )
        
        # 更新每日限制
        self.update_daily_limits(user_id, action, affection_to_award)
        
        # 如果升级了，处理升级奖励
        if level_change["is_level_up"]:
            self.process_level_up_rewards(user_id, level_change["new_level"])
        
        return AffectionResult(
            rewarded=True,
            message=f"获得{affection_to_award}点好感度！",
            affection_awarded=affection_to_award,
            level_up=level_change["is_level_up"],
            old_level=old_level,
            new_level=level_change["new_level"]
        )
    
    def award_outfit_purchase_affection(self, user_id: int, star_cost: int, 
                                       source_id: str = None) -> AffectionResult:
        """购买服装时奖励好感度"""
        action = get_outfit_affection_by_cost(star_cost)
        return self.award_affection(
            user_id=user_id,
            action=action,
            source_id=source_id,
            source_type=AffectionSourceType.PURCHASE
        )
    
    def process_level_up_rewards(self, user_id: int, new_level: int):
        """处理升级奖励"""
        # 查询等级配置中的奖励
        level_config = self.db.query(MascotAffectionLevel).filter(
            MascotAffectionLevel.level == new_level,
            MascotAffectionLevel.is_active == True
        ).first()
        
        if level_config and level_config.unlock_rewards:
            # 创建奖励记录
            reward = UserAffectionRewards(
                user_id=user_id,
                reward_type="level_reward",
                reward_category="level_up",
                reward_content=level_config.unlock_rewards,
                trigger_level=new_level,
                is_claimed=False
            )
            self.db.add(reward)
            self.db.commit()
    
    def get_user_affection_summary(self, user_id: int) -> dict:
        """获取用户好感度概览"""
        user_affection = self.get_or_create_user_affection(user_id)
        level_info = get_level_by_affection(user_affection.current_affection)
        next_level_info = get_next_level_info(user_affection.current_level)
        
        return {
            "current_affection": user_affection.current_affection,
            "total_earned_affection": user_affection.total_earned_affection,
            "current_level": user_affection.current_level,
            "level_name": level_info["name"],
            "level_progress": user_affection.level_progress,
            "next_level_required": user_affection.next_level_required,
            "next_level_name": next_level_info["name"] if next_level_info else "已达到最高级",
            "last_interaction_at": user_affection.last_interaction_at
        }
    
    def get_affection_logs(self, user_id: int, limit: int = 20) -> List[MascotAffectionLog]:
        """获取用户好感度变动记录"""
        return self.db.query(MascotAffectionLog).filter(
            MascotAffectionLog.user_id == user_id
        ).order_by(MascotAffectionLog.created_at.desc()).limit(limit).all()
    
    def get_unclaimed_rewards(self, user_id: int) -> List[UserAffectionRewards]:
        """获取用户未领取的好感度奖励"""
        return self.db.query(UserAffectionRewards).filter(
            UserAffectionRewards.user_id == user_id,
            UserAffectionRewards.is_claimed == False
        ).all()
    
    def claim_reward(self, user_id: int, reward_id: int) -> bool:
        """领取好感度奖励"""
        reward = self.db.query(UserAffectionRewards).filter(
            UserAffectionRewards.id == reward_id,
            UserAffectionRewards.user_id == user_id,
            UserAffectionRewards.is_claimed == False
        ).first()
        
        if reward:
            reward.is_claimed = True
            reward.claimed_at = datetime.now()
            self.db.commit()
            return True
        
        return False
