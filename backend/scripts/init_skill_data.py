#file:ariadne/backend/app/scripts/init_skill_data.py
import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.insert(0, backend_dir)

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models import SkillCategory, Skill, Achievement

def init_skill_categories(db: Session):
    """初始化技能分类"""
    categories = [
        {
            "name": "沟通表达",
            "description": "学会清晰、准确、有效的表达自己的想法和感受",
            "icon": "💬",
            "sort_order": 1
        },
        {
            "name": "情感理解",
            "description": "理解自己和他人的情感，提升情感智慧",
            "icon": "💝",
            "sort_order": 2
        },
        {
            "name": "关系建立",
            "description": "建立和维护健康、积极的人际关系",
            "icon": "🤝",
            "sort_order": 3
        },
        {
            "name": "特殊情境",
            "description": "应对特殊场合和复杂人际情境",
            "icon": "🎯",
            "sort_order": 4
        }
    ]
    
    for cat_data in categories:
        category = SkillCategory(**cat_data)
        db.add(category)
    
    db.commit()

def init_basic_skills(db: Session):
    """初始化基础技能"""
    # 获取分类
    comm_category = db.query(SkillCategory).filter(SkillCategory.name == "沟通表达").first()
    
    skills = [
        {
            "name": "主动倾听",
            "brief": "学会用心倾听对方的话语和情感",
            "description": "主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。",
            "difficulty": "basic",
            "estimated_time": 15,
            "category_id": comm_category.id,
            "objectives": [
                "学会集中注意力倾听对方说话",
                "理解言语背后的情感和需求", 
                "通过肢体语言展现倾听态度",
                "运用复述和确认技巧验证理解"
            ],
            "key_points": [
                {
                    "icon": "👀",
                    "title": "眼神交流",
                    "content": "保持适当的眼神交流，表达对对方的关注和尊重",
                    "example": "看着对方的眼睛，偶尔点头表示理解"
                },
                {
                    "icon": "🤐", 
                    "title": "避免打断",
                    "content": "让对方完整表达想法，不要急于插话或给建议",
                    "example": "等对方说完后再回应：\"我理解你的意思是...\""
                }
            ],
            "practice_steps": [
                {
                    "title": "营造倾听环境",
                    "description": "选择安静、舒适的环境，放下手机等干扰物",
                    "tips": "将手机调至静音模式，身体面向对方"
                }
            ],
            "scenarios": [
                {
                    "id": 1,
                    "title": "朋友倾诉工作压力",
                    "description": "朋友向你抱怨工作中的困难和压力，需要你的倾听和理解",
                    "difficulty": "基础"
                }
            ],
            "tags": ["倾听", "沟通基础", "理解"],
            "sort_order": 1
        }
    ]
    
    for skill_data in skills:
        skill = Skill(**skill_data)
        db.add(skill)
    
    db.commit()

def init_achievements(db: Session):
    """初始化成就系统"""
    achievements = [
        {
            "name": "入门学习者",
            "description": "完成第一个技能学习",
            "icon": "🌱",
            "category": "learning",
            "unlock_conditions": {"completed_skills": 1},
            "reward_points": 10,
            "sort_order": 1
        },
        {
            "name": "倾听达人", 
            "description": "掌握所有倾听技巧",
            "icon": "🎧",
            "category": "skill_master",
            "unlock_conditions": {"mastered_listening_skills": True},
            "reward_points": 50,
            "sort_order": 2
        },
        {
            "name": "学习之星",
            "description": "连续学习7天",
            "icon": "⭐",
            "category": "consistency", 
            "unlock_conditions": {"consecutive_days": 7},
            "reward_points": 30,
            "sort_order": 3
        }
    ]
    
    for achievement_data in achievements:
        achievement = Achievement(**achievement_data)
        db.add(achievement)
    
    db.commit()

def main():
    """运行初始化"""
    db = SessionLocal()
    try:
        print("开始初始化人际智慧模块数据...")
        
        init_skill_categories(db)
        print("✅ 技能分类初始化完成")
        
        init_basic_skills(db)
        print("✅ 基础技能初始化完成")
        
        init_achievements(db)
        print("✅ 成就系统初始化完成")
        
        print("🎉 人际智慧模块数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()