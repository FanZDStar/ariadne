from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import random
from typing import List, Dict, Any, Optional

from app.database.session import get_db
from app.core.ai_service import AIService
from app.core.prompts import PROMPTS
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# 交往小技巧数据库（可以后续移至数据库）
SOCIAL_SKILLS_DATABASE = {
    "communication": {
        "name": "沟通交流",
        "skills": [
            {
                "id": "listen_actively",
                "title": "主动倾听",
                "content": "真正的倾听不只是听到声音，而是理解对方的情感和需求。保持眼神接触，适时点头回应，重复对方的关键信息来确认理解。",
                "difficulty": "basic",
                "tags": ["倾听", "理解", "共情"],
                "scenarios": ["朋友倾诉烦恼", "恋人分享心事", "同学讨论问题"]
            },
            {
                "id": "express_clearly",
                "title": "清晰表达",
                "content": "用'我'开头的句式表达感受，避免指责性语言。比如说'我感到...'而不是'你总是...'，这样能减少对方的防御心理。",
                "difficulty": "basic",
                "tags": ["表达", "沟通", "情感"],
                "scenarios": ["表达不满", "提出需求", "分享感受"]
            },
            {
                "id": "topic_transition",
                "title": "话题延续",
                "content": "通过提问和分享相关经历来延续话题。使用'这让我想到...'或'你刚说的...很有趣'等过渡语，让对话自然流动。",
                "difficulty": "intermediate",
                "tags": ["话题", "聊天", "技巧"],
                "scenarios": ["初次约会", "朋友聚会", "课堂讨论"]
            }
        ]
    },
    "emotional_expression": {
        "name": "情感表达",
        "skills": [
            {
                "id": "sincere_gratitude",
                "title": "真诚感谢",
                "content": "具体说出对方帮助你的地方和你的感受，比如'谢谢你昨天陪我到很晚，让我感觉没那么孤单'比简单的'谢谢'更有力量。",
                "difficulty": "basic",
                "tags": ["感谢", "真诚", "情感"],
                "scenarios": ["朋友帮忙", "恋人关怀", "他人善意"]
            },
            {
                "id": "romantic_expression",
                "title": "浪漫表达",
                "content": "浪漫不在于华丽的词藻，而在于细节的观察和真实的感受。注意对方的喜好，在合适的时机表达你的在意。",
                "difficulty": "intermediate",
                "tags": ["浪漫", "恋爱", "表达"],
                "scenarios": ["情人节", "纪念日", "日常惊喜"]
            },
            {
                "id": "emotion_sharing",
                "title": "情绪分享",
                "content": "学会在适当的时候分享自己的脆弱，这会增进彼此的信任。选择安全的人和合适的时机，坦诚分享内心的感受。",
                "difficulty": "advanced",
                "tags": ["信任", "分享", "深度"],
                "scenarios": ["深度交流", "关系深化", "情感支持"]
            }
        ]
    },
    "relationship_building": {
        "name": "关系建立",
        "skills": [
            {
                "id": "ice_breaking",
                "title": "破冰技巧",
                "content": "从环境、共同话题或轻松话题开始。观察对方的兴趣点，用开放性问题引导对话，让对方有分享的欲望。",
                "difficulty": "basic",
                "tags": ["破冰", "初见", "社交"],
                "scenarios": ["新同学", "聚会认识", "社团活动"]
            },
            {
                "id": "trust_building",
                "title": "信任建立",
                "content": "信任需要时间积累。始终保持诚实，遵守承诺，在小事上展现可靠性，逐步建立深度信任关系。",
                "difficulty": "intermediate",
                "tags": ["信任", "可靠", "深度"],
                "scenarios": ["友谊深化", "恋爱关系", "团队合作"]
            },
            {
                "id": "boundary_setting",
                "title": "边界设立",
                "content": "健康的关系需要清晰的边界。温和但坚定地表达你的底线，尊重对方的边界，在尊重中建立安全感。",
                "difficulty": "advanced",
                "tags": ["边界", "尊重", "健康"],
                "scenarios": ["关系界定", "个人空间", "价值坚持"]
            }
        ]
    },
    "special_scenarios": {
        "name": "特殊场景",
        "skills": [
            {
                "id": "conflict_resolution",
                "title": "冲突处理",
                "content": "冲突时保持冷静，先理解对方的立场，再表达自己的观点。寻找共同点，用合作而非对抗的方式解决问题。",
                "difficulty": "advanced",
                "tags": ["冲突", "解决", "沟通"],
                "scenarios": ["恋人争吵", "朋友分歧", "团队矛盾"]
            },
            {
                "id": "digital_communication",
                "title": "数字社交",
                "content": "线上聊天时注意语气和表情包的使用，及时回复显示尊重，重要的话题最好面对面或语音交流。",
                "difficulty": "intermediate",
                "tags": ["线上", "社交媒体", "聊天"],
                "scenarios": ["微信聊天", "社交软件", "远程关系"]
            },
            {
                "id": "group_social",
                "title": "群体社交",
                "content": "在群体中要平衡参与度，既不要过于抢风头，也不要过于沉默。学会倾听不同观点，做好话题的引导者和连接者。",
                "difficulty": "intermediate",
                "tags": ["群体", "聚会", "领导力"],
                "scenarios": ["朋友聚会", "班级活动", "社团讨论"]
            }
        ]
    }
}

@router.get("/skills/categories")
async def get_skill_categories():
    """获取所有技能分类"""
    categories = []
    for category_id, category_data in SOCIAL_SKILLS_DATABASE.items():
        categories.append({
            "id": category_id,
            "name": category_data["name"],
            "skill_count": len(category_data["skills"])
        })
    return {"categories": categories}

@router.get("/skills/recommend")
async def get_recommended_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """基于用户画像智能推荐技能"""
    try:
        # 简化版推荐逻辑，后续可根据用户聊天记录、风险评估等数据优化
        # 这里随机推荐3-5个技能作为演示
        
        all_skills = []
        for category_data in SOCIAL_SKILLS_DATABASE.values():
            all_skills.extend(category_data["skills"])
        
        # 随机选择3-5个技能
        recommended_count = min(5, len(all_skills))
        recommended_skills = random.sample(all_skills, recommended_count)
        
        return {
            "recommended_skills": recommended_skills,
            "recommendation_reason": "基于您的个人特点，为您推荐以下交往技巧"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐技能失败: {str(e)}")

@router.post("/skills/{skill_id}/generate-scenario")
async def generate_skill_scenario(
    skill_id: str,
    request_data: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """为特定技能生成AI练习场景"""
    try:
        # 查找技能
        skill = None
        for category_data in SOCIAL_SKILLS_DATABASE.values():
            for s in category_data["skills"]:
                if s["id"] == skill_id:
                    skill = s
                    break
            if skill:
                break
        
        if not skill:
            raise HTTPException(status_code=404, detail="技能不存在")
        
        # 构建AI请求
        ai_service = AIService()
        
        # 创建场景生成提示词
        scenario_prompt = f"""
基于以下交往技巧为用户生成一个具体的练习场景：

技能名称：{skill['title']}
技能内容：{skill['content']}
适用场景：{', '.join(skill['scenarios'])}

请为用户创建一个具体、真实、可操作的练习场景，包括：
1. 场景描述（背景、人物、情况）
2. 目标对话者的可能反应
3. 具体的实践建议
4. 预期效果说明

场景要贴近大学生的实际生活，让用户能够真实地练习这个技能。
"""

        messages = [{"role": "user", "content": scenario_prompt}]
        ai_response = await ai_service.get_response(messages, "social-skills")
        
        return {
            "skill": skill,
            "scenario": {
                "content": ai_response,
                "generated_at": "刚刚生成"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成场景失败: {str(e)}")

@router.post("/skills/interactive-practice")
async def interactive_skill_practice(
    practice_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """交互式技能练习（用户与AI对话练习）"""
    try:
        skill_id = practice_data.get("skill_id")
        user_response = practice_data.get("user_response")
        scenario_context = practice_data.get("scenario_context", "")
        
        if not skill_id or not user_response:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        # 查找技能
        skill = None
        for category_data in SOCIAL_SKILLS_DATABASE.values():
            for s in category_data["skills"]:
                if s["id"] == skill_id:
                    skill = s
                    break
            if skill:
                break
        
        if not skill:
            raise HTTPException(status_code=404, detail="技能不存在")
        
        # 构建AI反馈提示词
        feedback_prompt = f"""
你正在指导用户练习"{skill['title']}"这个交往技巧。

技能要点：{skill['content']}
练习场景：{scenario_context}
用户的回应：{user_response}

请对用户的回应进行专业评估和指导：
1. 分析用户回应的优点（具体指出做得好的地方）
2. 指出可以改进的地方（温和建议）
3. 提供具体的优化建议
4. 给出下一步练习建议

请保持鼓励的语气，记住这是练习环境，用户需要支持和具体指导。
"""

        ai_service = AIService()
        messages = [{"role": "user", "content": feedback_prompt}]
        ai_feedback = await ai_service.get_response(messages, "social-skills")
        
        return {
            "skill": skill,
            "user_response": user_response,
            "ai_feedback": ai_feedback,
            "practice_completed": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"练习反馈失败: {str(e)}")

@router.get("/skills/{category_id}")
async def get_skills_by_category(category_id: str):
    """获取指定分类的所有技能"""
    if category_id not in SOCIAL_SKILLS_DATABASE:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    category_data = SOCIAL_SKILLS_DATABASE[category_id]
    return {
        "category": {
            "id": category_id,
            "name": category_data["name"]
        },
        "skills": category_data["skills"]
    }

@router.post("/skills/personalized-tips")
async def get_personalized_tips(
    request_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """基于用户当前情况生成个性化建议"""
    try:
        user_situation = request_data.get("situation", "")
        emotional_state = request_data.get("emotional_state", "")
        specific_need = request_data.get("specific_need", "")
        
        # 构建个性化建议提示词
        personalized_prompt = f"""
用户当前情况：{user_situation}
情感状态：{emotional_state}
具体需求：{specific_need}

请基于用户的具体情况，从交往技巧的角度给出3-4个个性化建议：
1. 针对当前情况的具体技巧推荐
2. 可以立即实践的小建议
3. 情感支持和鼓励
4. 后续发展建议

建议要具体、可操作、温暖鼓励，适合大学生的情况。
"""

        ai_service = AIService()
        messages = [{"role": "user", "content": personalized_prompt}]
        ai_response = await ai_service.get_response(messages, "social-skills")
        
        return {
            "personalized_tips": ai_response,
            "generated_for": {
                "situation": user_situation,
                "emotional_state": emotional_state,
                "specific_need": specific_need
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成个性化建议失败: {str(e)}")