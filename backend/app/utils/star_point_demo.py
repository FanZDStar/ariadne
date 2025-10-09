"""
星星积分系统演示和测试
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from datetime import datetime
from app.utils.star_point_types import StarPointAction, SourceType, get_reward_config

def demonstrate_star_point_system():
    """演示星星积分系统的功能"""
    
    print("🌟 念念有声星星积分系统演示")
    print("=" * 50)
    
    print("\n📋 积分获取场景配置:")
    print("-" * 30)
    
    # 显示所有积分规则
    for action in StarPointAction:
        config = get_reward_config(action)
        if config:
            limit_info = f"（每日限制: {config.daily_limit}次）" if config.daily_limit else "（无每日限制）"
            prob_info = f" - 概率: {config.probability*100}%" if config.probability < 1.0 else ""
            print(f"• {config.description}: {config.points}星星 {limit_info}{prob_info}")
    
    print("\n🎯 积分获取规则详细说明:")
    print("-" * 30)
    
    scenarios = {
        "每日登录": "每日第一次登录获得1个星星",
        "晴雨表打卡": "每日第一次保存心情获得1个星星", 
        "写日记": "第一篇3星星，第2-3篇各1星星（每日最多3篇）",
        "修改背景": "每日第一次修改日记背景获得1个星星",
        "情感对话": "前3次各2星星，第4-10次各1星星（每日最多10星星）",
        "技能训练": "每日第一次综合训练获得1个星星",
        "技能收藏": "50%概率获得1个星星",
        "情景演练": "每次演练获得1个星星",
        "关系评估": "每日第一次评估获得2个星星",
        "个性化建议": "每日第一次建议获得2个星星",
        "AI情景训练": "每日第一次训练获得2个星星",
        "防护技能训练": "每日第一次训练获得2个星星",
        "树洞互动": "前3次互动各2星星",
        "发表悄悄话": "每日第一次发表获得2个星星"
    }
    
    for scenario, description in scenarios.items():
        print(f"• {scenario}: {description}")
    
    print(f"\n💫 系统特性:")
    print("-" * 30)
    print("• 所有用户初始积分: 10个星星")
    print("• 每日限制自动重置")
    print("• 完整的积分变动日志")
    print("• 积分可用于购买看板娘服装")
    print("• 支持概率性奖励（如技能收藏）")
    
    print(f"\n🔧 技术实现:")
    print("-" * 30)
    print("• 数据库表: user_star_points, star_point_logs, daily_star_limits")
    print("• 服务类: StarPointService")  
    print("• API路由: /star-points/*")
    print("• 工具函数: star_point_helpers.py")
    
    print(f"\n📱 前端展示:")
    print("-" * 30)
    print("• 个人主页显示当前星星数量")
    print("• 积分变动提示")
    print("• 积分历史记录")
    print("• 每日任务状态")

def show_integration_examples():
    """展示如何在其他模块中集成积分系统"""
    
    print(f"\n🔗 集成示例代码:")
    print("=" * 50)
    
    examples = [
        {
            "场景": "用户登录",
            "位置": "auth.py - login_user()",
            "代码": """
from app.utils.star_point_helpers import award_daily_login

# 在登录成功后
success, message, points = award_daily_login(db, user.user_id)
if success:
    print(f"获得每日登录奖励: {points}星星")
"""
        },
        {
            "场景": "发表日记", 
            "位置": "diary.py - create_diary()",
            "代码": """
from app.utils.star_point_helpers import award_diary_points

# 判断是否为当日第一篇日记
is_first_today = check_if_first_diary_today(db, user_id)
success, message, points = award_diary_points(
    db, user_id, diary.diary_id, is_first=is_first_today
)
"""
        },
        {
            "场景": "情感对话",
            "位置": "ai_dialog.py - send_message()",
            "代码": """
from app.utils.star_point_helpers import award_emotion_chat

# 判断是否为前3次对话
is_premium = get_today_chat_count(db, user_id) < 3
success, message, points = award_emotion_chat(
    db, user_id, session.id, is_premium=is_premium
)
"""
        },
        {
            "场景": "树洞互动",
            "位置": "tree_hole.py - like_whisper()",
            "代码": """
from app.utils.star_point_helpers import award_tree_hole_interaction

success, message, points = award_tree_hole_interaction(
    db, user_id, interaction_id
)
"""
        },
        {
            "场景": "购买服装",
            "位置": "mascot.py - purchase_outfit()",
            "代码": """
from app.utils.star_point_helpers import try_spend_points
from app.utils.star_point_types import SourceType

success, message = try_spend_points(
    db, user_id, outfit.price, 
    f"购买服装: {outfit.name}",
    source_id=outfit.id,
    source_type=SourceType.PURCHASE
)
"""
        }
    ]
    
    for example in examples:
        print(f"\n📍 {example['场景']} - {example['位置']}")
        print(example['代码'])

if __name__ == "__main__":
    demonstrate_star_point_system()
    show_integration_examples()
    
    print(f"\n✨ 积分系统已完整实现！")
    print("下一步: 在各功能模块中集成积分奖励逻辑")
    print("建议: 先运行 backend/scripts/init_star_points.py 初始化现有用户积分")
