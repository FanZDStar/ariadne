"""
星星积分系统行为类型定义
"""
from enum import Enum
from typing import Dict, NamedTuple


class PointReward(NamedTuple):
    """积分奖励配置"""
    points: int
    description: str
    daily_limit: int = None  # None表示无限制
    probability: float = 1.0  # 获得概率，1.0表示100%


class StarPointAction(Enum):
    """星星积分行为类型枚举"""
    
    # 每日登录
    DAILY_LOGIN = "daily_login"
    
    # 晴雨表相关
    MOOD_TRACKING = "mood_tracking"
    
    # 日记相关
    DIARY_FIRST = "diary_first"          # 当日第一篇日记 3星
    DIARY_ADDITIONAL = "diary_additional"  # 当日第2-3篇日记 各1星
    
    # 背景修改
    BACKGROUND_CHANGE = "background_change"
    
    # 情感对话
    EMOTION_CHAT_PREMIUM = "emotion_chat_premium"  # 前3次 各2星
    EMOTION_CHAT_NORMAL = "emotion_chat_normal"    # 第4-10次 各1星
    
    # 人际智慧 - 技能学习
    SKILL_TRAINING = "skill_training"           # 综合训练 1星
    SKILL_FAVORITE = "skill_favorite"           # 收藏技能 50%概率1星
    SCENARIO_PRACTICE = "scenario_practice"     # 情景演练 1星
    
    # 人际智慧 - 防护指南
    RELATIONSHIP_ASSESSMENT = "relationship_assessment"  # 关系评估 1星
    PERSONALIZED_ADVICE = "personalized_advice"        # 个性化建议 1星
    
    # 人际智慧 - 实战练习
    AI_SCENARIO_TRAINING = "ai_scenario_training"       # AI情景训练 2星
    PROTECTION_TRAINING = "protection_training"         # 防护技能训练 2星
    
    # 心灵树洞
    TREE_HOLE_INTERACTION = "tree_hole_interaction"     # 互动(点赞评论) 前3次各1星
    TREE_HOLE_WHISPER = "tree_hole_whisper"            # 发表悄悄话 2星
    
    # 消费相关
    MASCOT_PURCHASE = "mascot_purchase"                 # 购买看板娘服装
    
    # 系统相关
    INITIAL_REWARD = "initial_reward"                   # 初始奖励


# 积分奖励配置
STAR_POINT_REWARDS: Dict[StarPointAction, PointReward] = {
    # 每日登录
    StarPointAction.DAILY_LOGIN: PointReward(
        points=1, 
        description="每日首次登录奖励", 
        daily_limit=1
    ),
    
    # 晴雨表
    StarPointAction.MOOD_TRACKING: PointReward(
        points=1, 
        description="每日首次心情记录", 
        daily_limit=1
    ),
    
    # 日记
    StarPointAction.DIARY_FIRST: PointReward(
        points=3, 
        description="今日第一篇日记", 
        daily_limit=1
    ),
    StarPointAction.DIARY_ADDITIONAL: PointReward(
        points=1, 
        description="今日额外日记", 
        daily_limit=2
    ),
    
    # 背景修改
    StarPointAction.BACKGROUND_CHANGE: PointReward(
        points=1, 
        description="修改日记背景", 
        daily_limit=1
    ),
    
    # 情感对话
    StarPointAction.EMOTION_CHAT_PREMIUM: PointReward(
        points=2, 
        description="情感对话(前3次)", 
        daily_limit=3
    ),
    StarPointAction.EMOTION_CHAT_NORMAL: PointReward(
        points=1, 
        description="情感对话(第4-10次)", 
        daily_limit=7
    ),
    
    # 技能学习
    StarPointAction.SKILL_TRAINING: PointReward(
        points=1, 
        description="技能综合训练", 
        daily_limit=1
    ),
    StarPointAction.SKILL_FAVORITE: PointReward(
        points=1, 
        description="收藏技能", 
        probability=0.5
    ),
    StarPointAction.SCENARIO_PRACTICE: PointReward(
        points=1, 
        description="技能情景演练"
    ),
    
    # 防护指南
    StarPointAction.RELATIONSHIP_ASSESSMENT: PointReward(
        points=1, 
        description="关系健康评估", 
        daily_limit=1
    ),
    StarPointAction.PERSONALIZED_ADVICE: PointReward(
        points=1, 
        description="个性化建议", 
        daily_limit=1
    ),
    
    # 实战练习
    StarPointAction.AI_SCENARIO_TRAINING: PointReward(
        points=2, 
        description="AI情景模拟训练", 
        daily_limit=1
    ),
    StarPointAction.PROTECTION_TRAINING: PointReward(
        points=2, 
        description="防护技能训练", 
        daily_limit=1
    ),
    
    # 心灵树洞
    StarPointAction.TREE_HOLE_INTERACTION: PointReward(
        points=1, 
        description="树洞互动", 
        daily_limit=3
    ),
    StarPointAction.TREE_HOLE_WHISPER: PointReward(
        points=2, 
        description="发表悄悄话", 
        daily_limit=1
    ),
    
    # 系统奖励
    StarPointAction.INITIAL_REWARD: PointReward(
        points=10, 
        description="系统初始化奖励"
    ),
}


class SourceType(Enum):
    """积分来源类型"""
    SYSTEM = "system"           # 系统
    LOGIN = "login"             # 登录
    DIARY = "diary"             # 日记
    MOOD = "mood"               # 心情
    CHAT = "chat"               # 对话
    SKILL = "skill"             # 技能
    ASSESSMENT = "assessment"   # 评估
    PRACTICE = "practice"       # 练习
    TREE_HOLE = "tree_hole"     # 树洞
    PURCHASE = "purchase"       # 购买


def get_reward_config(action: StarPointAction) -> PointReward:
    """获取行为的积分奖励配置"""
    return STAR_POINT_REWARDS.get(action)


def get_action_display_name(action: StarPointAction) -> str:
    """获取行为的显示名称"""
    reward = get_reward_config(action)
    return reward.description if reward else action.value


def is_daily_limited(action: StarPointAction) -> bool:
    """检查行为是否有每日限制"""
    reward = get_reward_config(action)
    return reward and reward.daily_limit is not None
