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
        # 人际关系测评题库 - 4种关系类型，每种20个问题
        relationship_assessment_questions = {
            "family": {
                "name": "家庭关系",
                "description": "评估与家人的沟通、理解和情感连接",
                "questions": [
                    {
                        "id": "family_1",
                        "question": "当家人批评我时，我通常会：",
                        "options": ["冷静倾听，尝试理解他们的观点", "解释自己的想法，寻求理解", "感到不满但不说出来", "立即反驳或争吵"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "family_2", 
                        "question": "我与父母讨论我的未来规划时：",
                        "options": ["开诚布公，详细分享我的想法", "会分享，但有所保留", "很少主动讨论这些话题", "通常避免这类谈话"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "family_3",
                        "question": "家人需要帮助时，我的反应是：",
                        "options": ["主动询问需要什么帮助", "在被要求时积极帮助", "偶尔帮助，取决于心情", "很少主动提供帮助"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "支持理解"
                    },
                    {
                        "id": "family_4",
                        "question": "面对家人的不同观念时，我会：",
                        "options": ["尊重差异，寻找共同点", "尝试理解但有时感到困难", "表面接受但内心不认同", "经常因为观念不同产生冲突"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "相互尊重"
                    },
                    {
                        "id": "family_5",
                        "question": "我感到沮丧或困扰时，会：",
                        "options": ["主动与家人分享并寻求支持", "在合适的时候告诉家人", "很少与家人分享负面情绪", "从不让家人知道我的困扰"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感纽带"
                    },
                    {
                        "id": "family_6",
                        "question": "关于个人隐私和家庭分享之间，我认为：",
                        "options": ["能够很好地平衡个人空间和家庭亲密", "大部分情况下能找到平衡", "有时感到边界不清晰", "经常因为隐私问题产生矛盾"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "独立成长"
                    },
                    {
                        "id": "family_7",
                        "question": "家庭聚餐或聚会时，我通常：",
                        "options": ["积极参与，享受家庭时光", "愿意参加，但不总是很主动", "被动参与，更多时候在看手机", "尽量避免或提早离开"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "情感纽带"
                    },
                    {
                        "id": "family_8",
                        "question": "当家人对我的选择表示担心时：",
                        "options": ["耐心解释，理解他们的担心", "会解释但有时显得不耐烦", "觉得被过度干预，很少解释", "认为他们不理解我，经常争吵"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "family_9",
                        "question": "我对家人的期待和要求：",
                        "options": ["理解他们的期待，但坚持自己的判断", "大部分时候能接受，偶尔有分歧", "感到压力很大，但不敢表达", "完全反对，经常因此产生矛盾"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互尊重"
                    },
                    {
                        "id": "family_10",
                        "question": "我在做重要决定时：",
                        "options": ["会听取家人意见但最终自己决定", "通常会征求家人的意见", "很大程度上依赖家人的建议", "完全按照家人的意见来做"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "独立成长"
                    },
                    {
                        "id": "family_11",
                        "question": "当家人情绪激动或生气时，我会：",
                        "options": ["保持冷静，尝试安抚和沟通", "等他们冷静下来再交流", "感到紧张，不知道怎么应对", "也会变得情绪化，容易争吵"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "family_12",
                        "question": "家人给我经济支持时，我的感受是：",
                        "options": ["心存感激，会合理使用", "感谢但有时感到压力", "认为这是理所当然的", "不喜欢依赖家人，尽量拒绝"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "支持理解"
                    },
                    {
                        "id": "family_13",
                        "question": "当我在外遇到困难时：",
                        "options": ["会第一时间告诉家人寻求帮助", "先自己尝试解决，必要时求助", "不愿意让家人担心，很少求助", "认为家人帮不了什么忙"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "支持理解"
                    },
                    {
                        "id": "family_14",
                        "question": "家人关心我的感情生活时：",
                        "options": ["愿意适度分享，寻求建议", "会简单告知，但保留隐私", "觉得这是私事，不愿多说", "完全拒绝讨论，认为他们不该管"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感纽带"
                    },
                    {
                        "id": "family_15",
                        "question": "当家人的生活习惯与我不同时：",
                        "options": ["尊重差异，寻找和谐相处的方法", "大多数时候能容忍", "经常感到不适应或烦躁", "坚持按自己的方式，不愿妥协"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互尊重"
                    },
                    {
                        "id": "family_16",
                        "question": "家人对我的朋友有意见时：",
                        "options": ["会倾听他们的担心，但保持自己的判断", "考虑他们的意见，适当调整", "感到为难，不知道该听谁的", "完全不理会，坚持自己的社交"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "独立成长"
                    },
                    {
                        "id": "family_17",
                        "question": "在家庭责任分担方面：",
                        "options": ["主动承担自己应尽的责任", "被提醒时会积极参与", "偶尔参与，但不够主动", "很少主动承担家庭责任"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "支持理解"
                    },
                    {
                        "id": "family_18",
                        "question": "当家人生病或需要照顾时：",
                        "options": ["会主动关心和照顾", "在能力范围内提供帮助", "有心但不知道怎么帮", "觉得有其他人会照顾，很少参与"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感纽带"
                    },
                    {
                        "id": "family_19",
                        "question": "家人表达对我的爱和关心时：",
                        "options": ["能够自然地接受并回应", "感到温暖但有时不知如何回应", "感到有些不自在或压力", "觉得他们过于黏人，希望保持距离"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感纽带"
                    },
                    {
                        "id": "family_20",
                        "question": "我对家庭未来的期望是：",
                        "options": ["希望关系更加和谐，互相支持", "维持现状，偶尔改善一些问题", "希望减少冲突，各自独立一些", "希望尽快独立，减少家庭束缚"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "独立成长"
                    }
                ]
            },
            
            "friendship": {
                "name": "友情关系",
                "description": "评估与朋友的互动、信任和友谊维护",
                "questions": [
                    {
                        "id": "friend_1",
                        "question": "朋友向我倾诉烦恼时，我会：",
                        "options": ["专心倾听，给予情感支持和建议", "认真倾听，主要给予情感支持", "听着但有时会分心", "不太喜欢处理朋友的负面情绪"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互支持"
                    },
                    {
                        "id": "friend_2",
                        "question": "当朋友和我有不同意见时：",
                        "options": ["开放讨论，尊重彼此的观点", "会表达自己的想法但避免争执", "通常选择避免争论", "坚持自己的观点，很难妥协"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通表达"
                    },
                    {
                        "id": "friend_3",
                        "question": "朋友需要我保守秘密时：",
                        "options": ["绝对保密，从不透露给任何人", "通常能保密，但偶尔可能说漏", "会告诉我认为可信的其他朋友", "很难保守秘密，经常无意中说出"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_4",
                        "question": "朋友向我借钱时，我的反应是：",
                        "options": ["根据情况和能力合理决定", "通常会借，但会考虑金额", "很难拒绝，即使自己也紧张", "从不借钱给朋友"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "边界把握"
                    },
                    {
                        "id": "friend_5",
                        "question": "当朋友的行为让我感到不舒服时：",
                        "options": ["会直接但温和地表达我的感受", "暗示或间接表达不满", "忍受不快，不愿意直接面对", "会生气但不说原因"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "沟通表达"
                    },
                    {
                        "id": "friend_6",
                        "question": "朋友取得成就时，我的感受是：",
                        "options": ["真心为他们高兴，主动祝贺", "为他们高兴，但有时会有一点羡慕", "表面祝贺，内心有些复杂情绪", "很难真心为朋友的成功感到高兴"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互支持"
                    },
                    {
                        "id": "friend_7",
                        "question": "在朋友群体中，我通常：",
                        "options": ["积极参与讨论，善于调节气氛", "愿意参与，但不总是很主动", "更多时候选择倾听", "很少主动参与群体活动"],
                        "risk_weights": [5, 4, 3, 1],
                        "dimension": "沟通表达"
                    },
                    {
                        "id": "friend_8",
                        "question": "朋友向我求助时：",
                        "options": ["尽我所能提供帮助", "在能力范围内会帮助", "偶尔帮助，取决于具体情况", "很少主动提供帮助"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互支持"
                    },
                    {
                        "id": "friend_9",
                        "question": "关于朋友的隐私，我认为：",
                        "options": ["严格尊重，不主动打听私事", "尊重但有时会好奇", "认为好朋友应该分享一切", "经常打听朋友的私人事务"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "边界把握"
                    },
                    {
                        "id": "friend_10",
                        "question": "当朋友犯错误时，我会：",
                        "options": ["温和地指出，给予支持和理解", "私下提醒，但不会过度干预", "选择不说，避免破坏关系", "直接批评或疏远"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_11",
                        "question": "朋友邀请我参加我不感兴趣的活动时：",
                        "options": ["会诚实表达想法，寻找折中方案", "通常会参加，不愿意拒绝朋友", "直接拒绝，认为朋友应该理解", "经常找借口推脱"],
                        "risk_weights": [5, 3, 4, 2],
                        "dimension": "边界把握"
                    },
                    {
                        "id": "friend_12",
                        "question": "当朋友需要情感支持时：",
                        "options": ["放下手头事情，专心陪伴", "会安排时间给予支持", "有时间就帮忙，没时间就算了", "觉得每个人都应该自己解决问题"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "相互支持"
                    },
                    {
                        "id": "friend_13",
                        "question": "朋友之间产生误会时：",
                        "options": ["主动沟通，努力解决误会", "等待合适的机会澄清", "希望时间能自然化解误会", "不愿意主动解释，认为清者自清"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通表达"
                    },
                    {
                        "id": "friend_14",
                        "question": "当朋友的价值观与我差异很大时：",
                        "options": ["尊重差异，在共同点上维持友谊", "尝试理解，但保持自己的立场", "感到不舒服，减少深入交流", "认为三观不合无法做朋友"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_15",
                        "question": "朋友在背后谈论我时（无恶意）：",
                        "options": ["理解这是正常的社交行为", "有些介意但不会直接面对", "感到被背叛，很难接受", "会直接质问朋友"],
                        "risk_weights": [5, 3, 2, 2],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_16",
                        "question": "我对友谊的期待是：",
                        "options": ["相互理解支持，共同成长", "开心时一起分享，困难时相互帮助", "主要是一起玩乐和消遣", "不期待太多，保持简单的关系"],
                        "risk_weights": [5, 4, 3, 2],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_17",
                        "question": "当朋友的行为影响到我的其他关系时：",
                        "options": ["会与朋友沟通，寻求解决方案", "暗示朋友注意影响", "忍受这种情况，不愿意说出来", "选择疏远，避免进一步影响"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "边界把握"
                    },
                    {
                        "id": "friend_18",
                        "question": "朋友向我抱怨其他朋友时：",
                        "options": ["倾听但保持中立，不参与评判", "会适当给出建议", "跟着一起抱怨，表示支持", "不愿意听这些负面内容"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "信任建立"
                    },
                    {
                        "id": "friend_19",
                        "question": "当我需要独处空间时：",
                        "options": ["会坦诚告诉朋友我需要一些个人时间", "找合适的理由暂时疏远", "强迫自己继续社交，不愿意让朋友失望", "直接消失一段时间，不做解释"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "边界把握"
                    },
                    {
                        "id": "friend_20",
                        "question": "我对长期友谊的维护：",
                        "options": ["主动联系，定期关心朋友近况", "节日或特殊时刻会联系", "通常等朋友先联系我", "觉得好朋友不需要刻意维护"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "相互支持"
                    }
                ]
            },
            
            "romantic": {
                "name": "恋爱关系",
                "description": "评估恋爱中的沟通、信任和情感管理",
                "questions": [
                    {
                        "id": "romantic_1",
                        "question": "在恋爱关系中，我对分享个人感受的态度是：",
                        "options": ["愿意开诚布公地分享内心想法", "会分享，但需要时间建立信任", "只分享一些表面的感受", "很难向伴侣敞开心扉"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感亲密"
                    },
                    {
                        "id": "romantic_2",
                        "question": "当伴侣心情不好时，我通常：",
                        "options": ["主动询问并给予陪伴和支持", "给他们一些空间，然后再关心", "不知道该怎么办，感到无措", "认为他们会自己处理好"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感亲密"
                    },
                    {
                        "id": "romantic_3",
                        "question": "当我们发生争执时，我倾向于：",
                        "options": ["冷静下来后主动沟通解决", "等待合适的时机再讨论", "希望对方先道歉或主动和解", "冷战或逃避问题"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "冲突处理"
                    },
                    {
                        "id": "romantic_4",
                        "question": "关于伴侣的过去，我的态度是：",
                        "options": ["尊重过去，专注现在和未来", "有时会好奇但不会深究", "经常想知道更多细节", "无法接受伴侣有过去的感情经历"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_5",
                        "question": "当伴侣与异性朋友交往时：",
                        "options": ["完全信任，支持他们的友谊", "基本信任，但偶尔会有些在意", "经常感到不安或担心", "强烈反对或要求断绝来往"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_6",
                        "question": "我表达对伴侣的爱意时：",
                        "options": ["经常用言语和行动表达爱意", "会表达，但不总是很直接", "更多通过行动而非言语", "很难直接表达爱意"],
                        "risk_weights": [5, 4, 3, 1],
                        "dimension": "情感亲密"
                    },
                    {
                        "id": "romantic_7",
                        "question": "在做重要决定时，我会：",
                        "options": ["一定会和伴侣讨论并征求意见", "通常会告知并听取想法", "偶尔会征求意见", "习惯自己做决定"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "romantic_8",
                        "question": "当伴侣批评我时，我的反应是：",
                        "options": ["冷静接受，反思自己的问题", "有时能接受，有时会辩解", "感到被攻击，很难平静接受", "立即反击或冷战"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "romantic_9",
                        "question": "关于个人空间和独处时间：",
                        "options": ["认为每个人都需要个人空间", "理解但有时希望更多陪伴", "经常希望和伴侣在一起", "不理解为什么需要个人空间"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_10",
                        "question": "当我们的观念有分歧时：",
                        "options": ["尊重差异，寻找平衡点", "尝试说服对方接受我的观点", "避免讨论有争议的话题", "坚持己见，很难妥协"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "冲突处理"
                    },
                    {
                        "id": "romantic_11",
                        "question": "当伴侣需要独处时：",
                        "options": ["完全理解并给予空间", "理解但有时会感到失落", "很难理解，觉得被冷落", "认为这是关系出问题的信号"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_12",
                        "question": "我对关系的期待是：",
                        "options": ["共同成长，相互支持的伙伴关系", "希望有稳定的情感依靠", "希望对方能满足我的大部分需求", "希望完全融合，没有秘密"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感亲密"
                    },
                    {
                        "id": "romantic_13",
                        "question": "当伴侣犯错误时：",
                        "options": ["会沟通讨论，寻求解决方案", "会原谅但需要时间消化", "很难原谅，会长时间记住", "立即选择分手或报复"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "冲突处理"
                    },
                    {
                        "id": "romantic_14",
                        "question": "关于查看伴侣的手机或社交媒体：",
                        "options": ["完全尊重隐私，不会偷看", "偶尔会好奇但克制自己", "有时会偷偷查看", "认为情侣之间不应该有秘密"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_15",
                        "question": "当伴侣与我意见不同时：",
                        "options": ["尊重不同观点，开放讨论", "会据理力争但保持理性", "感到沮丧，不愿意继续讨论", "坚持自己是对的，要求对方改变"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "romantic_16",
                        "question": "在关系中遇到困难时：",
                        "options": ["会与伴侣一起面对和解决", "主要靠自己解决，偶尔寻求帮助", "希望伴侣能主动解决", "考虑是否要结束关系"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "冲突处理"
                    },
                    {
                        "id": "romantic_17",
                        "question": "当伴侣不回复消息时：",
                        "options": ["理解可能在忙，耐心等待", "会有些担心但不会催促", "感到焦虑，会频繁发消息", "立即生气，认为被忽视"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "信任安全"
                    },
                    {
                        "id": "romantic_18",
                        "question": "我对关系中的浪漫的看法：",
                        "options": ["重视但不认为是关系的全部", "希望有一些浪漫元素", "非常重视浪漫的表达", "觉得浪漫不重要，实际更重要"],
                        "risk_weights": [5, 4, 3, 4],
                        "dimension": "情感亲密"
                    },
                    {
                        "id": "romantic_19",
                        "question": "当朋友对我的伴侣有负面看法时：",
                        "options": ["会听取意见但保持自己的判断", "感到困扰，会认真考虑", "不愿意听到任何批评", "立即与朋友争论或疏远"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "沟通交流"
                    },
                    {
                        "id": "romantic_20",
                        "question": "我对长期关系的期望：",
                        "options": ["希望建立稳定、成熟的长期关系", "先享受当下，再考虑未来", "不确定自己是否适合长期关系", "觉得长期关系会失去自由"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "情感亲密"
                    }
                ]
            },
            
            "mentor": {
                "name": "师生关系",
                "description": "评估与老师、导师的互动和学习关系",
                "questions": [
                    {
                        "id": "mentor_1",
                        "question": "课堂上老师提问时，我通常：",
                        "options": ["积极举手回答，不怕答错", "知道答案时会举手", "很少主动举手回答", "从不主动回答问题"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "主动学习"
                    },
                    {
                        "id": "mentor_2",
                        "question": "当我对课程内容有疑问时：",
                        "options": ["会主动向老师请教", "下课后会询问老师", "更倾向于问同学或自己查资料", "很少主动寻求帮助"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通请教"
                    },
                    {
                        "id": "mentor_3",
                        "question": "老师给我学术建议时，我会：",
                        "options": ["认真倾听并积极采纳", "仔细考虑后选择性采纳", "表面接受但不一定会做", "很难接受与我想法不同的建议"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "反馈接受"
                    },
                    {
                        "id": "mentor_4",
                        "question": "在师生交流中，我的态度是：",
                        "options": ["保持尊重但不感到拘束", "尊重老师但有时感到紧张", "非常拘谨，很少表达想法", "过于随意，缺乏基本礼貌"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_5",
                        "question": "当老师批评我的学习态度时：",
                        "options": ["虚心接受并努力改进", "听取建议但有时感到委屈", "表面接受但内心不服", "感到被针对，很难接受"],
                        "risk_weights": [5, 3, 2, 1],
                        "dimension": "反馈接受"
                    },
                    {
                        "id": "mentor_6",
                        "question": "我对老师的课后时间的态度是：",
                        "options": ["理解老师也需要休息，不会随意打扰", "紧急情况下会联系，但会道歉", "有问题就联系，不太考虑时间", "认为老师随时应该为学生服务"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_7",
                        "question": "在小组讨论或课堂展示时：",
                        "options": ["积极参与，勇于表达观点", "会参与但不总是很主动", "更愿意听别人发言", "尽量避免发言或展示"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "主动学习"
                    },
                    {
                        "id": "mentor_8",
                        "question": "当我与老师的观点不同时：",
                        "options": ["礼貌地表达不同看法并讨论", "会质疑但保持尊重的态度", "内心有不同想法但不敢说出", "完全不敢质疑老师的观点"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通请教"
                    },
                    {
                        "id": "mentor_9",
                        "question": "老师给予我额外学习机会时：",
                        "options": ["积极把握，全力以赴", "会参与但担心自己能力不够", "考虑很久才决定是否参与", "通常会拒绝或找借口推脱"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "主动学习"
                    },
                    {
                        "id": "mentor_10",
                        "question": "我对老师的期望是：",
                        "options": ["希望获得知识指导和人生启发", "主要希望学好课程内容", "希望老师更多关注我的学习", "只希望顺利通过考试"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_11",
                        "question": "当老师的教学方式不适合我时：",
                        "options": ["会主动寻找适应的方法", "私下向老师请教学习方法", "抱怨但不主动改变", "放弃努力，得过且过"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "主动学习"
                    },
                    {
                        "id": "mentor_12",
                        "question": "老师布置的作业或任务：",
                        "options": ["认真完成，力求高质量", "按时完成基本要求", "经常拖延或匆忙完成", "能不做就不做，能拖就拖"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "反馈接受"
                    },
                    {
                        "id": "mentor_13",
                        "question": "当老师表扬我时：",
                        "options": ["感到鼓励，继续努力", "高兴但不会过分在意", "觉得是应该的，没什么特别", "怀疑老师的真实想法"],
                        "risk_weights": [5, 4, 3, 1],
                        "dimension": "反馈接受"
                    },
                    {
                        "id": "mentor_14",
                        "question": "关于向老师寻求学习以外的建议：",
                        "options": ["在合适的时候会寻求人生指导", "偶尔会咨询学术相关的问题", "很少向老师寻求额外建议", "认为老师只应该管学习"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通请教"
                    },
                    {
                        "id": "mentor_15",
                        "question": "当其他同学与老师关系很好时：",
                        "options": ["不嫉妒，努力建立自己与老师的关系", "有些羡慕但不会嫉妒", "感到嫉妒，认为老师偏心", "无所谓，不在意这些"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_16",
                        "question": "老师给我写推荐信或提供帮助时：",
                        "options": ["非常感激，会主动表达谢意", "心存感激但不知如何表达", "觉得这是老师应该做的", "担心给老师添麻烦"],
                        "risk_weights": [5, 4, 2, 3],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_17",
                        "question": "在学术讨论中表达不同观点时：",
                        "options": ["基于事实和逻辑，理性讨论", "会表达但担心被认为不尊重", "很少表达不同意见", "情绪化地表达反对"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通请教"
                    },
                    {
                        "id": "mentor_18",
                        "question": "当老师忙碌时我需要帮助：",
                        "options": ["理解并等待合适的时机", "会询问何时方便交流", "坚持立即得到帮助", "觉得被忽视，感到不满"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_19",
                        "question": "我对师生关系的理解是：",
                        "options": ["既是师长又是学术伙伴的关系", "主要是知识传授与学习的关系", "希望老师像朋友一样对待我", "严格的等级关系，保持距离"],
                        "risk_weights": [5, 4, 3, 2],
                        "dimension": "尊重态度"
                    },
                    {
                        "id": "mentor_20",
                        "question": "毕业后与老师的联系：",
                        "options": ["会保持联系，汇报近况", "节日时会问候", "很少主动联系", "毕业就不再联系"],
                        "risk_weights": [5, 4, 2, 1],
                        "dimension": "沟通请教"
                    }
                ]
            }
        }
        
        return {
            "relationship_types": relationship_assessment_questions,
            "instructions": "请选择您要测评的关系类型，系统将随机选择20道题目进行测评"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取风险评估失败: {str(e)}")

@router.post("/protection/relationship-assessment/start")
async def start_relationship_assessment(
    assessment_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """开始人际关系测评，随机选择20道题"""
    try:
        relationship_type = assessment_data.get("relationship_type")
        
        # 获取关系测评题库
        relationship_assessment_questions = await get_risk_assessment_test(current_user, db)
        relationship_types = relationship_assessment_questions["relationship_types"]
        
        if not relationship_type or relationship_type not in relationship_types:
            raise HTTPException(status_code=400, detail="无效的关系类型")
        
        type_data = relationship_types[relationship_type]
        all_questions = type_data["questions"]
        
        # 随机选择8道题（确保题目多样性）
        if len(all_questions) <= 8:
            selected_questions = all_questions
        else:
            # 为了确保覆盖不同维度，先按维度分组，然后随机选择
            dimension_questions = {}
            for q in all_questions:
                dimension = q["dimension"]
                if dimension not in dimension_questions:
                    dimension_questions[dimension] = []
                dimension_questions[dimension].append(q)
            
            selected_questions = []
            # 尽量从每个维度都选择题目
            questions_per_dimension = max(1, 8 // len(dimension_questions))
            remaining_count = 8
            
            for dimension, questions in dimension_questions.items():
                if remaining_count <= 0:
                    break
                # 从该维度随机选择题目
                count_to_select = min(questions_per_dimension, len(questions), remaining_count)
                selected_from_dimension = random.sample(questions, count_to_select)
                selected_questions.extend(selected_from_dimension)
                remaining_count -= count_to_select
            
            # 如果还没选够8题，从剩余题目中随机补充
            if remaining_count > 0:
                all_remaining = [q for q in all_questions if q not in selected_questions]
                if all_remaining:
                    additional_count = min(remaining_count, len(all_remaining))
                    selected_questions.extend(random.sample(all_remaining, additional_count))
        
        # 生成session token
        import uuid
        session_token = str(uuid.uuid4())
        
        # 准备返回的问题数据（不包含答案权重）
        questions_for_user = []
        for q in selected_questions:
            questions_for_user.append({
                "id": q["id"],
                "question": q["question"],
                "options": [opt for opt in q["options"]],  # 只返回选项文本
                "dimension": q["dimension"]
            })
        
        return {
            "session_token": session_token,
            "relationship_type": relationship_type,
            "relationship_info": {
                "name": type_data["name"],
                "description": type_data["description"]
            },
            "questions": questions_for_user,
            "total_questions": len(questions_for_user)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"开始测评失败: {str(e)}")

@router.post("/protection/relationship-assessment/submit")
async def submit_relationship_assessment(
    submission_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交人际关系测评答案并生成分析报告"""
    try:
        session_token = submission_data.get("session_token")
        relationship_type = submission_data.get("relationship_type")
        answers = submission_data.get("answers", {})  # 格式: {question_id: selected_option_index}
        
        if not all([session_token, relationship_type, answers]):
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        # 获取关系测评题库
        relationship_assessment_questions = await get_risk_assessment_test(current_user, db)
        relationship_types = relationship_assessment_questions["relationship_types"]
        
        if relationship_type not in relationship_types:
            raise HTTPException(status_code=400, detail="无效的关系类型")
        
        type_data = relationship_types[relationship_type]
        
        # 计算分数和维度统计 - 优化版本
        dimension_scores = {}
        dimension_counts = {}
        dimension_names = {}
        total_score = 0
        max_possible_score = 0
        
        # 首先获取实际出题的问题列表（从session中获取，这里简化处理）
        # 实际应用中应该保存用户的具体题目，这里重新生成作为演示
        answered_questions = []
        for question in type_data["questions"]:
            if question["id"] in answers:
                answered_questions.append(question)
        
        # 初始化维度信息（只针对实际回答的题目涉及的维度）
        for question in answered_questions:
            dimension = question["dimension"]
            if dimension not in dimension_scores:
                dimension_scores[dimension] = 0
                dimension_counts[dimension] = 0
                dimension_names[dimension] = dimension
        
        # 计算实际回答题目的分数
        for question in answered_questions:
            question_id = question["id"]
            option_index = answers[question_id]
            
            if 0 <= option_index < len(question["risk_weights"]):
                score = question["risk_weights"][option_index]
                dimension = question["dimension"]
                
                dimension_scores[dimension] += score
                dimension_counts[dimension] += 1
                total_score += score
                max_possible_score += 5  # 每题最高5分
        
        # 计算维度百分比得分（基于加权平均）
        dimension_percentages = {}
        dimension_weights = {}
        
        # 为每种关系类型定义维度权重
        relationship_dimension_weights = {
            "family": {
                "沟通交流": 0.25,
                "情感纽带": 0.25, 
                "相互尊重": 0.2,
                "支持理解": 0.2,
                "独立成长": 0.1
            },
            "friendship": {
                "信任建立": 0.3,
                "沟通表达": 0.25,
                "相互支持": 0.25,
                "边界把握": 0.2
            },
            "romantic": {
                "情感亲密": 0.3,
                "沟通交流": 0.25,
                "信任安全": 0.25,
                "冲突处理": 0.2
            },
            "mentor": {
                "尊重态度": 0.3,
                "沟通请教": 0.25,
                "主动学习": 0.25,
                "反馈接受": 0.2
            }
        }
        
        current_weights = relationship_dimension_weights.get(relationship_type, {})
        
        for dim, total_score_for_dim in dimension_scores.items():
            if dimension_counts[dim] > 0:
                max_score_for_dim = dimension_counts[dim] * 5
                dimension_percentages[dim] = (total_score_for_dim / max_score_for_dim) * 100
                dimension_weights[dim] = current_weights.get(dim, 1.0 / len(dimension_scores))
            else:
                dimension_percentages[dim] = 0
                dimension_weights[dim] = 0
        
        # 计算加权总体百分比得分
        if dimension_scores:
            weighted_total = sum(dimension_percentages[dim] * dimension_weights[dim] 
                               for dim in dimension_percentages.keys())
            total_weight = sum(dimension_weights[dim] for dim in dimension_percentages.keys() 
                             if dimension_counts[dim] > 0)
            overall_percentage = weighted_total / total_weight if total_weight > 0 else 0
        else:
            overall_percentage = 0
        
        # 生成评价等级 - 优化评级标准
        def get_score_level(percentage):
            if percentage >= 85:
                return {"level": "优秀", "color": "#52C41A", "description": "表现非常出色，值得继续保持"}
            elif percentage >= 70:
                return {"level": "良好", "color": "#1890FF", "description": "表现良好，有提升空间"}
            elif percentage >= 55:
                return {"level": "一般", "color": "#FAAD14", "description": "基本合格，需要一些改进"}
            elif percentage >= 40:
                return {"level": "待提升", "color": "#FF7A45", "description": "需要重点关注和改进"}
            else:
                return {"level": "需要帮助", "color": "#F5222D", "description": "建议寻求专业指导"}
        
        overall_level = get_score_level(overall_percentage)
        
        # 生成维度分析
        dimension_analysis = {}
        for dim, percentage in dimension_percentages.items():
            dimension_analysis[dim] = {
                "name": dimension_names[dim],
                "percentage": percentage,  # 前端期望这个字段名
                "score": percentage,      # 保留兼容性
                "level": get_score_level(percentage),
                "question_count": dimension_counts[dim]
            }
        
        # 使用AI生成个性化分析报告
        ai_service = AIService()
        analysis_prompt = f"""
请为用户的人际关系测评结果生成详细的分析报告：

关系类型：{type_data['name']}
总体得分：{overall_percentage:.1f}%
总体等级：{overall_level['level']}

各维度得分：
{json.dumps(dimension_analysis, ensure_ascii=False, indent=2)}

用户回答了{len(answers)}道题目

请提供：
1. 总体关系状况分析
2. 各维度的详细解读
3. 具体的优势和不足
4. 个性化的改进建议
5. 实用的行动计划

分析要客观、温暖、具有指导性，适合大学生的实际情况。
"""

        messages = [{"role": "user", "content": analysis_prompt}]
        ai_analysis = await ai_service.get_response(messages, "relationship-assessment")
        
        # 生成个性化建议
        recommendations = []
        
        # 基于总体得分的建议
        if overall_percentage >= 80:
            recommendations.append({
                "type": "congratulations",
                "title": "关系维护得很好！",
                "content": f"您在{type_data['name']}方面表现出色，继续保持这种良好的互动模式。",
                "priority": "info"
            })
        elif overall_percentage < 50:
            recommendations.append({
                "type": "improvement_focus",
                "title": "需要重点关注",
                "content": f"您的{type_data['name']}需要一些改进，建议优先提升得分较低的维度。",
                "priority": "urgent"
            })
        
        # 基于维度得分的具体建议
        for dim, dim_data in dimension_analysis.items():
            if dim_data["score"] < 60:
                recommendations.append({
                    "type": "dimension_improvement",
                    "title": f"提升{dim_data['name']}",
                    "content": f"您在{dim_data['name']}方面得分为{dim_data['score']:.1f}%，建议重点关注这个方面。",
                    "priority": "high",
                    "dimension": dim
                })
        
        return {
            "assessment_result": {
                "session_token": session_token,
                "relationship_type": relationship_type,
                "relationship_name": type_data["name"],
                "total_score": overall_percentage,
                "total_level": overall_level,
                "dimension_scores": dimension_analysis,
                "questions_answered": len(answers),
                "completed_at": "刚刚完成"
            },
            "ai_analysis": ai_analysis,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交测评失败: {str(e)}")

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

回复格式要求：请用段落形式回复，每个要点用一个段落表述，段落之间不要有空行，不要使用Markdown格式或编号列表，用自然流畅的文字表达，不要过长，讲明白道理就行。
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