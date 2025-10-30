# file: ariadne/backend/app/core/personalized_prompt.py
"""
个性化Prompt生成服务
根据用户档案动态生成个性化的系统提示词
"""

from typing import Optional, Dict, Any, List
from datetime import datetime


class PersonalizedPromptService:
    """
    个性化提示词生成服务
    根据用户的个人档案信息生成定制化的AI系统提示词
    """
    
    @staticmethod
    def build_user_context_prefix(user_profile: Dict[str, Any]) -> str:
        """
        构建用户上下文前缀
        在每个系统提示词的开头添加用户的个人信息背景
        
        Args:
            user_profile: 用户档案数据字典
            
        Returns:
            个性化的用户背景上下文字符串
        """
        context_parts = ["## 用户个人背景信息"]
        
        # 基本信息
        if user_profile.get('birth_date'):
            age = PersonalizedPromptService._calculate_age(user_profile['birth_date'])
            context_parts.append(f"👤 **年龄**: {age}岁")
        
        if user_profile.get('zodiac_sign'):
            context_parts.append(f"♈ **星座**: {user_profile['zodiac_sign']}")
        
        # 性格特征
        personality_summary = PersonalizedPromptService._build_personality_summary(
            user_profile.get('personality_tags', []),
            user_profile.get('personality_custom_description')
        )
        if personality_summary:
            context_parts.append(f"✨ **性格特征**: {personality_summary}")
        
        # 爱好兴趣
        hobby_summary = PersonalizedPromptService._build_hobby_summary(
            user_profile.get('hobby_tags', []),
            user_profile.get('hobby_custom_description')
        )
        if hobby_summary:
            context_parts.append(f"🎯 **兴趣爱好**: {hobby_summary}")
        
        # 专业职业
        profession_summary = PersonalizedPromptService._build_profession_summary(
            user_profile.get('profession_tags', []),
            user_profile.get('job_title'),
            user_profile.get('profession_custom_description')
        )
        if profession_summary:
            context_parts.append(f"💼 **专业背景**: {profession_summary}")
        
        # 生活阶段
        if user_profile.get('life_stage'):
            context_parts.append(f"📍 **生活阶段**: {user_profile['life_stage']}")
        
        # 地理位置
        if user_profile.get('location'):
            context_parts.append(f"🌍 **城市地区**: {user_profile['location']}")
        
        # 个人座右铭
        if user_profile.get('personal_motto'):
            context_parts.append(f"💭 **个人座右铭**: \"{user_profile['personal_motto']}\"")
        
        # 关注领域
        if user_profile.get('main_focus_areas'):
            focus_areas = ", ".join(user_profile['main_focus_areas'])
            context_parts.append(f"🔍 **当前关注**: {focus_areas}")
        
        return "\n".join(context_parts) + "\n\n"
    
    @staticmethod
    def generate_personalized_system_prompt(
        base_prompt: str,
        user_profile: Dict[str, Any],
        scene: str = "general"
    ) -> str:
        """
        生成个性化系统提示词
        在原有的场景提示词基础上，插入用户的个人背景信息
        
        Args:
            base_prompt: 基础系统提示词
            user_profile: 用户档案数据
            scene: 交互场景
            
        Returns:
            个性化的完整系统提示词
        """
        if not user_profile or not any(user_profile.values()):
            # 如果用户档案为空，返回原始提示词
            return base_prompt
        
        # 构建用户背景前缀
        user_context = PersonalizedPromptService.build_user_context_prefix(user_profile)
        
        # 根据场景添加特定的个性化指导
        personalization_guidance = PersonalizedPromptService._get_scene_specific_guidance(
            user_profile, scene
        )
        
        # 组合完整的提示词
        personalized_prompt = (
            user_context +
            personalization_guidance +
            "\n---\n\n" +
            base_prompt
        )
        
        return personalized_prompt
    
    @staticmethod
    def _build_personality_summary(tags: List[str], custom_desc: Optional[str]) -> str:
        """构建性格特征摘要"""
        parts = []
        
        if tags:
            parts.append(", ".join(tags))
        
        if custom_desc:
            parts.append(custom_desc)
        
        return " | ".join(parts) if parts else ""
    
    @staticmethod
    def _build_hobby_summary(tags: List[str], custom_desc: Optional[str]) -> str:
        """构建爱好兴趣摘要"""
        parts = []
        
        if tags:
            parts.append(", ".join(tags))
        
        if custom_desc:
            parts.append(custom_desc)
        
        return " | ".join(parts) if parts else ""
    
    @staticmethod
    def _build_profession_summary(
        tags: List[str],
        job_title: Optional[str],
        custom_desc: Optional[str]
    ) -> str:
        """构建职业专业摘要"""
        parts = []
        
        if tags:
            parts.append(", ".join(tags))
        
        if job_title:
            parts.append(f"职位: {job_title}")
        
        if custom_desc:
            parts.append(custom_desc)
        
        return " | ".join(parts) if parts else ""
    
    @staticmethod
    def _calculate_age(birth_date: str) -> int:
        """计算年龄 (格式: YYYY-MM-DD)"""
        try:
            birth = datetime.strptime(birth_date, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return age
        except (ValueError, TypeError):
            return 0
    
    @staticmethod
    def _get_scene_specific_guidance(user_profile: Dict[str, Any], scene: str) -> str:
        """
        根据场景和用户特征生成特定的个性化指导
        """
        guidance = "## 个性化交互建议\n"
        
        # 基于性格特征的调整
        personality_tags = user_profile.get('personality_tags', [])
        if "内向" in personality_tags:
            guidance += "- 用户偏向内向，建议提供一对一的深度对话而非群体建议\n"
        if "敏感" in personality_tags:
            guidance += "- 用户较为敏感，请避免过于直接或生硬的表述\n"
        if "理性" in personality_tags:
            guidance += "- 用户倾向理性，建议提供数据支持和逻辑清晰的论证\n"
        if "感性" in personality_tags:
            guidance += "- 用户倾向感性，建议从情感共鸣和故事案例出发\n"
        
        # 基于职业背景的调整
        profession_tags = user_profile.get('profession_tags', [])
        if "学生" in profession_tags:
            guidance += "- 用户是学生，可以结合学习场景和学业压力来对话\n"
        if "工程师" in profession_tags or "技术" in profession_tags:
            guidance += "- 用户具有技术背景，可以使用更专业的术语和逻辑框架\n"
        if "创意工作者" in profession_tags or "艺术" in profession_tags:
            guidance += "- 用户从事创意工作，建议鼓励创新思维和个性表达\n"
        
        # 基于生活阶段的调整
        life_stage = user_profile.get('life_stage', '')
        if "大学" in life_stage:
            guidance += "- 用户处于大学阶段，可关注学业、人际关系、自我探索等相关话题\n"
        if "工作" in life_stage:
            guidance += "- 用户处于工作阶段，可关注职业发展、工作平衡等问题\n"
        
        # 基于关注领域的调整
        main_focus = user_profile.get('main_focus_areas', [])
        if main_focus:
            guidance += f"- 用户主要关注: {', '.join(main_focus)}，可以在对话中融入相关观点\n"
        
        return guidance if guidance != "## 个性化交互建议\n" else ""
    
    @staticmethod
    def generate_ai_context_string(user_profile: Dict[str, Any]) -> str:
        """
        生成简洁的用户背景字符串，用于在messages中直接使用
        
        Example output:
        "用户是一位25岁的双子座，性格外向、理性、有创意，
        爱好编程和设计，是一名UI设计师，主要关注产品设计和用户体验。"
        """
        parts = []
        
        # 年龄和星座
        age_zodiac = ""
        if user_profile.get('birth_date'):
            age = PersonalizedPromptService._calculate_age(user_profile['birth_date'])
            age_zodiac = f"{age}岁"
        
        if user_profile.get('zodiac_sign'):
            age_zodiac += f"的{user_profile['zodiac_sign']}" if age_zodiac else user_profile['zodiac_sign']
        
        if age_zodiac:
            parts.append(f"用户是一位{age_zodiac}")
        
        # 性格
        personality = PersonalizedPromptService._build_personality_summary(
            user_profile.get('personality_tags', []),
            user_profile.get('personality_custom_description')
        )
        if personality:
            parts.append(f"性格上{personality}")
        
        # 爱好
        hobby = PersonalizedPromptService._build_hobby_summary(
            user_profile.get('hobby_tags', []),
            None
        )
        if hobby:
            parts.append(f"爱好{hobby}")
        
        # 职业
        job_title = user_profile.get('job_title')
        profession_tags = user_profile.get('profession_tags', [])
        
        if job_title or profession_tags:
            profession_str = job_title if job_title else "、".join(profession_tags)
            parts.append(f"是一名{profession_str}")
        
        # 关注领域
        focus = user_profile.get('main_focus_areas', [])
        if focus:
            parts.append(f"主要关注{', '.join(focus)}")
        
        # 组合
        if parts:
            context = "，".join(parts)
            if not context.endswith("。"):
                context += "。"
            return context
        
        return ""
