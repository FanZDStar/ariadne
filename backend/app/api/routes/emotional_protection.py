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

# 感情防护知识库
PROTECTION_DATABASE = {
    "risk_signals": {
        "name": "风险信号识别",
        "items": [
            {
                "id": "control_behavior",
                "title": "控制行为识别",
                "description": "识别伴侣或朋友的过度控制行为",
                "risk_level": "high",
                "signals": [
                    "经常查看你的手机或社交媒体",
                    "限制你与朋友家人的联系",
                    "控制你的穿着打扮",
                    "不允许你参加社交活动",
                    "要求随时汇报行踪"
                ],
                "scenarios": ["恋爱关系", "亲密友谊", "室友关系"]
            },
            {
                "id": "emotional_manipulation",
                "title": "情感操控识别",
                "description": "识别PUA、煤气灯效应等情感操控手段",
                "risk_level": "critical",
                "signals": [
                    "让你怀疑自己的记忆和判断",
                    "用冷暴力惩罚你的行为",
                    "威胁自伤来控制你",
                    "贬低你的自我价值",
                    "忽冷忽热的情感态度"
                ],
                "scenarios": ["恋爱关系", "网恋", "暧昧关系"]
            },
            {
                "id": "boundary_violation",
                "title": "边界侵犯识别",
                "description": "识别他人对你个人边界的侵犯",
                "risk_level": "high",
                "signals": [
                    "无视你明确表达的拒绝",
                    "强迫你做不愿意的事",
                    "侵犯你的隐私空间",
                    "不尊重你的决定",
                    "用各种理由施压"
                ],
                "scenarios": ["亲密关系", "朋友关系", "同学关系"]
            },
            {
                "id": "deception_behavior",
                "title": "欺骗行为识别",
                "description": "识别谎言、隐瞒和虚假承诺",
                "risk_level": "medium",
                "signals": [
                    "前后说法不一致",
                    "隐瞒重要信息",
                    "承诺后经常不兑现",
                    "编造借口逃避责任",
                    "对质疑反应过激"
                ],
                "scenarios": ["恋爱关系", "友谊关系", "网络交友"]
            }
        ]
    },
    "protection_strategies": {
        "name": "防护策略",
        "items": [
            {
                "id": "boundary_setting",
                "title": "边界设立技巧",
                "description": "学会建立和维护健康的人际边界",
                "difficulty": "intermediate",
                "strategies": [
                    "明确表达自己的底线和原则",
                    "学会温和但坚定地说'不'",
                    "不为拒绝他人而感到内疚",
                    "逐步建立边界，不要一次性过于严格",
                    "坚持自己的边界，不轻易妥协"
                ],
                "scenarios": ["设立约会边界", "维护个人空间", "拒绝不合理要求"]
            },
            {
                "id": "trust_evaluation",
                "title": "信任度评估",
                "description": "科学评估他人的可信度",
                "difficulty": "advanced",
                "strategies": [
                    "观察言行是否一致",
                    "关注对方如何对待其他人",
                    "测试小承诺的履行情况",
                    "注意对方处理冲突的方式",
                    "相信自己的直觉感受"
                ],
                "scenarios": ["新认识的朋友", "网恋对象", "潜在合作伙伴"]
            },
            {
                "id": "support_network",
                "title": "支持网络建设",
                "description": "建立和维护健康的社交支持系统",
                "difficulty": "basic",
                "strategies": [
                    "保持与多个朋友的联系",
                    "定期与家人沟通",
                    "参加健康的社交活动",
                    "建立应急联系人名单",
                    "寻找专业帮助渠道"
                ],
                "scenarios": ["社交圈建设", "应急支持", "情感困难时期"]
            },
            {
                "id": "self_worth_protection",
                "title": "自我价值保护",
                "description": "维护和提升自我价值感",
                "difficulty": "intermediate",
                "strategies": [
                    "定期进行自我肯定练习",
                    "记录自己的优点和成就",
                    "避免过度依赖他人的评价",
                    "培养独立的兴趣爱好",
                    "学会自我安慰和鼓励"
                ],
                "scenarios": ["受到贬低时", "自信心低落", "被操控后的恢复"]
            }
        ]
    },
    "emergency_responses": {
        "name": "应急响应",
        "items": [
            {
                "id": "immediate_safety",
                "title": "即时安全措施",
                "description": "面临即时威胁时的应对方法",
                "urgency": "critical",
                "actions": [
                    "立即脱离危险环境",
                    "联系信任的朋友或家人",
                    "必要时报警或寻求专业帮助",
                    "保存相关证据",
                    "寻找安全的临时住所"
                ],
                "scenarios": ["受到威胁", "被跟踪", "暴力风险"]
            },
            {
                "id": "emotional_recovery",
                "title": "情感恢复计划",
                "description": "从有害关系中恢复的步骤",
                "urgency": "high",
                "actions": [
                    "承认并接受受到的伤害",
                    "寻求专业心理咨询",
                    "重建自我价值认知",
                    "逐步恢复社交活动",
                    "制定未来关系的标准"
                ],
                "scenarios": ["分手后恢复", "被操控后", "信任重建"]
            }
        ]
    }
}

@router.get("/protection/categories")
async def get_protection_categories():
    """获取所有防护分类"""
    categories = []
    for category_id, category_data in PROTECTION_DATABASE.items():
        categories.append({
            "id": category_id,
            "name": category_data["name"],
            "item_count": len(category_data["items"])
        })
    return {"categories": categories}

@router.get("/protection/risk-assessment")
async def get_risk_assessment_test(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取风险评估测试题目"""
    try:
        # 构建风险评估测试
        assessment_questions = [
            {
                "id": "control_check",
                "question": "对方是否经常要求知道你的行踪？",
                "options": ["从不", "偶尔", "经常", "总是"],
                "risk_weights": [0, 1, 3, 5]
            },
            {
                "id": "isolation_check",
                "question": "对方是否试图阻止你与朋友见面？",
                "options": ["从不", "偶尔", "经常", "总是"],
                "risk_weights": [0, 2, 4, 5]
            },
            {
                "id": "manipulation_check",
                "question": "对方是否让你怀疑自己的记忆或判断？",
                "options": ["从不", "偶尔", "经常", "总是"],
                "risk_weights": [0, 2, 4, 5]
            },
            {
                "id": "boundary_check",
                "question": "当你说'不'时，对方的反应如何？",
                "options": ["尊重我的决定", "试图说服我", "表现不高兴", "强迫我改变主意"],
                "risk_weights": [0, 1, 3, 5]
            },
            {
                "id": "emotional_support",
                "question": "对方是否在你情绪低落时给予支持？",
                "options": ["总是支持", "经常支持", "偶尔支持", "很少支持"],
                "risk_weights": [0, 1, 3, 4]
            }
        ]
        
        return {
            "assessment_questions": assessment_questions,
            "instructions": "请根据您当前或最近的关系情况，诚实回答以下问题"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取风险评估失败: {str(e)}")

@router.post("/protection/risk-assessment/analyze")
async def analyze_risk_assessment(
    assessment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """分析风险评估结果"""
    try:
        answers = assessment_data.get("answers", {})
        relationship_type = assessment_data.get("relationship_type", "恋爱关系")
        
        if not answers:
            raise HTTPException(status_code=400, detail="缺少评估答案")
        
        # 计算风险分数（简化版算法）
        total_score = 0
        max_score = 25  # 5个问题，每题最高5分
        
        risk_weights = {
            "control_check": [0, 1, 3, 5],
            "isolation_check": [0, 2, 4, 5],
            "manipulation_check": [0, 2, 4, 5],
            "boundary_check": [0, 1, 3, 5],
            "emotional_support": [0, 1, 3, 4]
        }
        
        for question_id, answer_index in answers.items():
            if question_id in risk_weights:
                total_score += risk_weights[question_id][answer_index]
        
        # 计算风险等级
        risk_percentage = (total_score / max_score) * 100
        
        if risk_percentage >= 70:
            risk_level = "critical"
            risk_text = "高危"
        elif risk_percentage >= 50:
            risk_level = "high"
            risk_text = "较高"
        elif risk_percentage >= 30:
            risk_level = "medium"
            risk_text = "中等"
        else:
            risk_level = "low"
            risk_text = "较低"
        
        # 使用AI生成个性化分析报告
        ai_service = AIService()
        analysis_prompt = f"""
基于用户的风险评估结果，生成个性化的情感安全分析报告：

关系类型：{relationship_type}
风险分数：{total_score}/{max_score} ({risk_percentage:.1f}%)
风险等级：{risk_text}

用户回答情况：{json.dumps(answers, ensure_ascii=False)}

请提供：
1. 当前关系状况的专业分析
2. 具体的风险点识别
3. 个性化的防护建议
4. 后续行动建议
5. 必要时的求助资源

分析要客观、专业、温暖，避免过度恐慌但也要重视真实风险。
"""

        messages = [{"role": "user", "content": analysis_prompt}]
        ai_analysis = await ai_service.get_response(messages, "emotional-protection")
        
        return {
            "risk_assessment": {
                "total_score": total_score,
                "max_score": max_score,
                "risk_percentage": risk_percentage,
                "risk_level": risk_level,
                "risk_text": risk_text
            },
            "ai_analysis": ai_analysis,
            "recommendations": await get_personalized_recommendations(risk_level, relationship_type)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析风险评估失败: {str(e)}")

@router.post("/protection/scenario-simulation")
async def simulate_protection_scenario(
    scenario_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """模拟情感防护场景"""
    try:
        scenario_type = scenario_data.get("scenario_type", "random")
        difficulty_level = scenario_data.get("difficulty_level", "basic")
        
        # 使用AI生成情景模拟
        ai_service = AIService()
        scenario_prompt = f"""
请生成一个情感防护场景模拟，用于训练用户的风险识别能力：

场景类型：{scenario_type}
难度等级：{difficulty_level}

请创建一个具体的情景，包括：
1. 场景背景描述（人物、环境、情况）
2. 对话或互动过程
3. 需要识别的风险信号
4. 3-4个应对选项（包括正确和错误的选择）
5. 每个选项的后果说明

场景要贴近大学生的实际生活，让用户能够从中学习风险识别和应对技巧。
"""

        messages = [{"role": "user", "content": scenario_prompt}]
        scenario_content = await ai_service.get_response(messages, "emotional-protection")
        
        return {
            "scenario": {
                "content": scenario_content,
                "type": scenario_type,
                "difficulty": difficulty_level,
                "generated_at": "刚刚生成"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成情景模拟失败: {str(e)}")

@router.post("/protection/scenario-response")
async def evaluate_scenario_response(
    response_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """评估用户对情景的回应"""
    try:
        scenario_id = response_data.get("scenario_id")
        user_choice = response_data.get("user_choice")
        scenario_context = response_data.get("scenario_context", "")
        
        if not user_choice:
            raise HTTPException(status_code=400, detail="缺少用户选择")
        
        # 使用AI评估用户的选择
        ai_service = AIService()
        evaluation_prompt = f"""
用户刚刚完成了一个情感防护场景练习：

场景内容：{scenario_context}
用户选择：{user_choice}

请对用户的选择进行专业评估：
1. 分析用户选择的优点和风险
2. 解释正确的应对方式
3. 提供具体的改进建议
4. 给出学习要点总结
5. 推荐相关的防护技巧

评估要具体、客观、有教育意义，帮助用户提升风险识别和应对能力。
"""

        messages = [{"role": "user", "content": evaluation_prompt}]
        evaluation_result = await ai_service.get_response(messages, "emotional-protection")
        
        return {
            "evaluation": {
                "content": evaluation_result,
                "user_choice": user_choice,
                "evaluated_at": "刚刚评估"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评估回应失败: {str(e)}")

@router.get("/protection/{category_id}")
async def get_protection_items_by_category(category_id: str):
    """获取指定分类的防护内容"""
    if category_id not in PROTECTION_DATABASE:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    category_data = PROTECTION_DATABASE[category_id]
    return {
        "category": {
            "id": category_id,
            "name": category_data["name"]
        },
        "items": category_data["items"]
    }

@router.post("/protection/personalized-advice")
async def get_personalized_protection_advice(
    request_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取个性化防护建议"""
    try:
        situation_description = request_data.get("situation", "")
        relationship_type = request_data.get("relationship_type", "")
        specific_concerns = request_data.get("concerns", "")
        urgency_level = request_data.get("urgency", "normal")
        
        # 构建个性化建议提示词
        advice_prompt = f"""
用户寻求个性化的情感防护建议：

情况描述：{situation_description}
关系类型：{relationship_type}
具体担忧：{specific_concerns}
紧急程度：{urgency_level}

请提供：
1. 当前情况的风险评估
2. 具体的防护策略建议
3. 可以立即采取的行动
4. 长期的关系健康建议
5. 必要时的求助资源

建议要实用、可操作，适合大学生的实际情况，既要重视风险也要保持理性。
"""

        ai_service = AIService()
        messages = [{"role": "user", "content": advice_prompt}]
        personalized_advice = await ai_service.get_response(messages, "emotional-protection")
        
        return {
            "personalized_advice": personalized_advice,
            "advice_for": {
                "situation": situation_description,
                "relationship_type": relationship_type,
                "concerns": specific_concerns,
                "urgency": urgency_level
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成个性化建议失败: {str(e)}")

@router.get("/protection/emergency-resources")
async def get_emergency_resources():
    """获取应急求助资源"""
    resources = {
        "hotlines": [
            {
                "name": "全国心理危机干预热线",
                "number": "400-161-9995",
                "description": "24小时心理危机干预服务",
                "availability": "全天候"
            },
            {
                "name": "妇女维权热线",
                "number": "12338",
                "description": "妇女权益保护和法律咨询",
                "availability": "工作时间"
            },
            {
                "name": "法律援助热线",
                "number": "12348",
                "description": "免费法律咨询和援助",
                "availability": "工作时间"
            }
        ],
        "online_resources": [
            {
                "name": "中国心理学会",
                "type": "专业机构",
                "description": "心理咨询师查找和专业服务"
            },
            {
                "name": "壹心理",
                "type": "在线平台",
                "description": "在线心理咨询和测评"
            }
        ],
        "safety_planning": [
            "制定安全计划，包括安全的朋友联系方式",
            "准备应急包（重要证件、现金、药物）",
            "确定安全的临时住所",
            "了解当地的保护资源和法律援助",
            "建立支持网络，定期与信任的人联系"
        ]
    }
    
    return {"emergency_resources": resources}

async def get_personalized_recommendations(risk_level: str, relationship_type: str) -> List[Dict[str, Any]]:
    """根据风险等级获取个性化推荐"""
    recommendations = []
    
    if risk_level in ["critical", "high"]:
        recommendations.extend([
            {
                "type": "immediate_action",
                "title": "立即行动建议",
                "content": "考虑寻求专业帮助，与信任的朋友或家人分享情况",
                "priority": "urgent"
            },
            {
                "type": "safety_planning",
                "title": "安全计划制定",
                "content": "制定详细的安全计划，包括应急联系人和安全场所",
                "priority": "high"
            }
        ])
    
    if risk_level in ["medium", "high"]:
        recommendations.append({
            "type": "boundary_strengthening",
            "title": "边界强化训练",
            "content": "学习更有效的边界设立和维护技巧",
            "priority": "medium"
        })
    
    recommendations.append({
        "type": "support_network",
        "title": "支持网络建设",
        "content": "扩大和加强你的社交支持网络",
        "priority": "medium"
    })
    
    return recommendations