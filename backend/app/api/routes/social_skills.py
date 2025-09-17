from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import random
import logging
from typing import List, Dict, Any, Optional

from app.database.session import get_db
from app.core.ai_service import AIService
from app.core.prompts import PROMPTS
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# 创建logger实例
logger = logging.getLogger(__name__)


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
        # recommended_count = min(5, len(all_skills))
        recommended_count = 3;
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
        
        # 确保ai_response是字符串
        if isinstance(ai_response, str):
            scenario_content = ai_response
        else:
            # 如果不是字符串，尝试提取内容或使用默认值
            scenario_content = str(ai_response) if ai_response else "AI生成场景时出现问题，请重试"
        
        return {
            "skill": skill,
            "scenario": {
                "content": scenario_content,
                "type": "ai_generated",
                "source": "api_service",
                "generated_at": "刚刚生成"
            }
        }
        
    except Exception as e:
        logger.error(f"生成场景失败: {str(e)}")
        # 返回备用场景
        fallback_scenarios = {
            "conflict_resolution": "你和室友因为生活习惯产生了分歧。TA经常在深夜听音乐，影响你休息，而TA认为这是自己的自由。现在你们需要心平气和地解决这个问题...",
            "listen_actively": "你的好朋友最近工作压力很大，今天TA主动找你聊天，看起来很疲惫，说：'我觉得我快撑不下去了...'",
            "express_clearly": "你的恋人经常晚回信息，这让你感到被忽视。你们终于有机会面对面交流，你想表达你的感受..."
        }
        
        fallback_content = fallback_scenarios.get(skill_id, "这是一个练习场景，请根据所学技能进行练习。")
        
        return {
            "skill": skill if 'skill' in locals() else {"id": skill_id, "title": "交往技巧", "content": "练习人际交往技能"},
            "scenario": {
                "content": fallback_content,
                "type": "fallback",
                "source": "local_template",
                "generated_at": "刚刚生成"
            }
        }


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
        chat_history = practice_data.get("chat_history", [])  # 新增：对话历史
        is_first_message = practice_data.get("is_first_message", False)  # 新增：是否首次消息
        
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
        
        # 构建角色扮演对话提示词
        if is_first_message:
            # 首次对话，AI介绍场景并开始扮演
            roleplay_prompt = f"""
你现在要与用户进行"{skill['title']}"技能的情景练习。请你完全进入角色扮演模式。

练习场景：{scenario_context}

重要指示：
1. 你要扮演场景中的相关角色（如：朋友、恋人、室友、同学等）
2. 完全代入角色，用第一人称与用户对话
3. 不要进行分析或指导，只要自然地对话
4. 根据场景情况合理回应用户
5. 保持角色的情感状态和个性特点
6. 以自然、友善的方式与用户对话

用户刚说：{user_response}

请作为场景中的角色自然回应，不要说教或分析。
"""
        else:
            # 继续对话，基于历史记录
            history_text = "\n".join([f"{'用户' if msg.get('role') == 'user' else '角色'}：{msg.get('content', '')}" for msg in chat_history[-6:]])  # 最近6条历史
            
            roleplay_prompt = f"""
你正在与用户进行"{skill['title']}"技能的情景角色扮演练习。

练习场景：{scenario_context}

最近的对话历史：
{history_text}

用户刚说：{user_response}

重要指示：
1. 继续扮演场景中的角色，保持角色一致性
2. 用第一人称自然回应，不要跳出角色
3. 不要进行技能分析或指导
4. 根据对话历史和当前情况用自然、友善的方式回应合理回应
5. 适当推进情景发展

请作为角色继续对话：
"""

        ai_service = AIService()
        logger.info(f"正在调用AI服务，技能ID: {skill_id}")
        logger.debug(f"AI提示词: {roleplay_prompt[:200]}...")
        
        messages = [{"role": "user", "content": roleplay_prompt}]
        ai_response = await ai_service.get_response(messages, "social-skills")
        
        logger.info(f"AI服务响应: {ai_response[:100] if ai_response else 'None'}")
        
        # 确保ai_response是字符串
        if isinstance(ai_response, str):
            response_content = ai_response
        else:
            response_content = str(ai_response) if ai_response else "对话出现问题，请重试"
        
        # 随机决定是否结束练习（对话进行8轮以上且30%概率）
        should_end = len(chat_history) > 8 and random.random() < 0.3
        
        return {
            "skill": skill,
            "ai_response": response_content,
            "response_type": "roleplay",  # 标识这是角色扮演回应
            "practice_completed": should_end,
            "continue_conversation": not should_end
        }
        
    except Exception as e:
        logger.error(f"角色扮演对话失败: {str(e)}")
        # 返回备用回应
        fallback_responses = {
            "conflict_resolution": "我理解你的想法，但我们是不是可以找个都能接受的解决方案？",
            "listen_actively": "谢谢你愿意听我说这些，我真的需要有人理解我...",
            "express_clearly": "我感觉你好像有话要对我说，是不是我做错了什么？",
            "romantic_expression": "你这样说让我很开心，我也很在意我们的关系。"
        }
        
        fallback_content = fallback_responses.get(skill_id, "我明白你的意思，让我们继续聊聊吧。")
        
        return {
            "skill": skill if 'skill' in locals() else {"id": skill_id, "title": "交往技巧"},
            "ai_response": fallback_content,
            "response_type": "fallback",
            "practice_completed": False,
            "continue_conversation": True
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
        
        # 保留原有的反馈评估接口，重命名
@router.post("/skills/practice-feedback")
async def get_practice_feedback(
    practice_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取技能练习反馈和指导"""
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
        
        # 确保ai_feedback是字符串
        if isinstance(ai_feedback, str):
            feedback_content = ai_feedback
        else:
            feedback_content = str(ai_feedback) if ai_feedback else "AI反馈生成失败，请继续练习"
        
        return {
            "skill": skill,
            "user_response": user_response,
            "ai_feedback": feedback_content,
            "practice_completed": len(user_response) > 20  # 简单的完成条件
        }
        
    except Exception as e:
        logger.error(f"练习反馈失败: {str(e)}")
        # 返回备用反馈
        fallback_feedback = f"很好的尝试！继续练习'{skill.get('title', '这个技能')}'能让你的人际交往能力更上一层楼。"
        
        return {
            "skill": skill if 'skill' in locals() else {"id": skill_id, "title": "交往技巧"},
            "user_response": user_response,
            "ai_feedback": fallback_feedback,
            "practice_completed": True
        }