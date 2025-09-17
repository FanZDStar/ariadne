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
from app.core.skills_data import skills_manager, get_legacy_database

router = APIRouter()

# 创建logger实例
logger = logging.getLogger(__name__)

# 使用新的统一数据源（向后兼容）
SOCIAL_SKILLS_DATABASE = get_legacy_database()

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
        # 查找技能 - 使用新的数据管理器
        skill = skills_manager.get_skill_by_id(skill_id)
        
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
        
        # 添加调试日志
        logger.info(f"收到交互式练习请求 - skill_id: {skill_id}, user_response: {user_response[:50] if user_response else 'None'}")
        logger.info(f"scenario_context: {scenario_context[:100] if scenario_context else 'None'}")
        logger.info(f"is_first_message: {is_first_message}, chat_history length: {len(chat_history) if chat_history else 0}")
        
        if not skill_id or not user_response:
            logger.error(f"缺少必要参数 - skill_id: {skill_id}, user_response: {user_response}")
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        # 查找技能 - 使用新的数据管理器
        skill = skills_manager.get_skill_by_id(skill_id)
        
        # 如果找不到技能，记录日志但继续处理
        if not skill:
            logger.warning(f"未找到技能 {skill_id}，使用默认技能信息")
            # 创建一个基本的技能对象作为后备
            skill = {
                "id": str(skill_id),
                "title": "人际交往技巧",
                "content": "通过练习提升人际交往能力",
                "difficulty": "intermediate",
                "tags": ["人际交往", "练习"],
                "scenarios": ["日常交流", "社交场合", "人际互动"]
            }
        
        logger.info(f"找到技能: {skill.get('title', 'Unknown')}")
        
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
        
        # 检查AI响应是否包含错误信息
        if ai_response and any(error_word in ai_response for error_word in ["AI服务", "配置错误", "不可用", "暂时不可用", "技术问题"]):
            logger.warning(f"AI服务返回错误响应: {ai_response}")
            raise Exception(f"AI服务异常: {ai_response}")
        
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
        logger.error(f"异常详情: {type(e).__name__}")
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        
        # 返回备用回应
        fallback_responses = {
            "conflict_resolution": "我理解你的想法，但我们是不是可以找个都能接受的解决方案？",
            "listen_actively": "谢谢你愿意听我说这些，我真的需要有人理解我...",
            "express_clearly": "我感觉你好像有话要对我说，是不是我做错了什么？",
            "romantic_expression": "你这样说让我很开心，我也很在意我们的关系。"
        }
        
        fallback_content = fallback_responses.get(skill_id, "我明白你的意思，让我们继续聊聊吧。")
        logger.info(f"使用备用回应: {fallback_content}")
        
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
        
        # 查找技能 - 使用新的数据管理器
        skill = skills_manager.get_skill_by_id(skill_id)
        
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