"""
看板娘好感度系统行为类型定义
"""
from enum import Enum
from typing import Dict, NamedTuple


class AffectionReward(NamedTuple):
    """好感度奖励配置"""
    affection: int
    description: str
    daily_limit: int = None  # None表示无限制
    probability: float = 1.0  # 获得概率，1.0表示100%


class MascotAffectionAction(Enum):
    """看板娘好感度行为类型枚举"""
    
    # 每日登录
    DAILY_LOGIN = "daily_login"
    
    # 购买相关
    OUTFIT_PURCHASE_CHEAP = "outfit_purchase_cheap"      # 购买便宜服装 +10
    OUTFIT_PURCHASE_NORMAL = "outfit_purchase_normal"    # 购买普通服装 +20
    OUTFIT_PURCHASE_PREMIUM = "outfit_purchase_premium"  # 购买高级服装 +30
    OUTFIT_PURCHASE_LUXURY = "outfit_purchase_luxury"    # 购买豪华服装 +50
    
    # 情感对话
    EMOTION_CHAT = "emotion_chat"
    
    # 日记相关
    DIARY_COMPLETE = "diary_complete"
    
    # 心情记录
    MOOD_TRACKING = "mood_tracking"
    
    # 互动相关
    MASCOT_INTERACTION = "mascot_interaction"  # 与看板娘互动
    
    # 系统相关
    INITIAL_AFFECTION = "initial_affection"   # 初始好感度


# 好感度奖励配置
MASCOT_AFFECTION_REWARDS: Dict[MascotAffectionAction, AffectionReward] = {
    # 每日登录
    MascotAffectionAction.DAILY_LOGIN: AffectionReward(
        affection=10, 
        description="每日首次登录", 
        daily_limit=1
    ),
    
    # 购买服装
    MascotAffectionAction.OUTFIT_PURCHASE_CHEAP: AffectionReward(
        affection=10, 
        description="购买便宜服装(0-50星星)", 
    ),
    MascotAffectionAction.OUTFIT_PURCHASE_NORMAL: AffectionReward(
        affection=20, 
        description="购买普通服装(51-100星星)", 
    ),
    MascotAffectionAction.OUTFIT_PURCHASE_PREMIUM: AffectionReward(
        affection=30, 
        description="购买高级服装(101-200星星)", 
    ),
    MascotAffectionAction.OUTFIT_PURCHASE_LUXURY: AffectionReward(
        affection=50, 
        description="购买豪华服装(201+星星)", 
    ),
    
    # 情感对话
    MascotAffectionAction.EMOTION_CHAT: AffectionReward(
        affection=3, 
        description="情感对话", 
        daily_limit=5
    ),
    
    # 日记
    MascotAffectionAction.DIARY_COMPLETE: AffectionReward(
        affection=5, 
        description="完成日记", 
        daily_limit=1
    ),
    
    # 心情记录
    MascotAffectionAction.MOOD_TRACKING: AffectionReward(
        affection=3, 
        description="心情记录", 
        daily_limit=1
    ),
    
    # 互动
    MascotAffectionAction.MASCOT_INTERACTION: AffectionReward(
        affection=1, 
        description="与看板娘互动", 
        daily_limit=10
    ),
    
    # 系统奖励
    MascotAffectionAction.INITIAL_AFFECTION: AffectionReward(
        affection=0, 
        description="系统初始化"
    ),
}


class AffectionSourceType(Enum):
    """好感度来源类型"""
    SYSTEM = "system"           # 系统
    LOGIN = "login"             # 登录
    PURCHASE = "purchase"       # 购买
    CHAT = "chat"               # 对话
    DIARY = "diary"             # 日记
    MOOD = "mood"               # 心情
    INTERACTION = "interaction" # 互动


# 好感度等级配置
AFFECTION_LEVELS = [
    {"level": 1, "name": "陌生", "required_affection": 0, "max_affection": 99},
    {"level": 2, "name": "熟悉", "required_affection": 100, "max_affection": 299},
    {"level": 3, "name": "友好", "required_affection": 300, "max_affection": 599},
    {"level": 4, "name": "亲密", "required_affection": 600, "max_affection": 999},
    {"level": 5, "name": "挚友", "required_affection": 1000, "max_affection": 1499},
    {"level": 6, "name": "密友", "required_affection": 1500, "max_affection": 2099},
    {"level": 7, "name": "知己", "required_affection": 2100, "max_affection": 2799},
]


def get_affection_reward_config(action: MascotAffectionAction) -> AffectionReward:
    """获取行为的好感度奖励配置"""
    return MASCOT_AFFECTION_REWARDS.get(action)


def get_affection_action_display_name(action: MascotAffectionAction) -> str:
    """获取行为的显示名称"""
    reward = get_affection_reward_config(action)
    return reward.description if reward else action.value


def is_affection_daily_limited(action: MascotAffectionAction) -> bool:
    """检查行为是否有每日限制"""
    reward = get_affection_reward_config(action)
    return reward and reward.daily_limit is not None


def get_outfit_affection_by_cost(star_cost: int) -> MascotAffectionAction:
    """根据服装价格获取对应的好感度行为类型"""
    if star_cost <= 50:
        return MascotAffectionAction.OUTFIT_PURCHASE_CHEAP
    elif star_cost <= 100:
        return MascotAffectionAction.OUTFIT_PURCHASE_NORMAL
    elif star_cost <= 200:
        return MascotAffectionAction.OUTFIT_PURCHASE_PREMIUM
    else:
        return MascotAffectionAction.OUTFIT_PURCHASE_LUXURY


def get_level_by_affection(affection: int) -> dict:
    """根据好感度值获取等级信息"""
    for level_info in reversed(AFFECTION_LEVELS):
        if affection >= level_info["required_affection"]:
            return level_info
    return AFFECTION_LEVELS[0]  # 默认返回第一级


def get_next_level_info(current_level: int) -> dict:
    """获取下一等级信息"""
    for level_info in AFFECTION_LEVELS:
        if level_info["level"] == current_level + 1:
            return level_info
    return None  # 已达到最高级


def calculate_level_progress(current_affection: int, current_level: int) -> float:
    """计算当前等级的进度百分比"""
    current_level_info = None
    next_level_info = None
    
    for level_info in AFFECTION_LEVELS:
        if level_info["level"] == current_level:
            current_level_info = level_info
        elif level_info["level"] == current_level + 1:
            next_level_info = level_info
            break
    
    if not current_level_info or not next_level_info:
        return 100.0  # 已达到最高级
    
    current_min = current_level_info["required_affection"]
    next_min = next_level_info["required_affection"]
    
    if current_affection >= next_min:
        return 100.0
    
    progress = ((current_affection - current_min) / (next_min - current_min)) * 100
    return max(0.0, min(100.0, progress))
