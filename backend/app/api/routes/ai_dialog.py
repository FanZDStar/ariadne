from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import httpx
import logging
from app.core.config import settings
from app.core.prompts import PROMPTS
from typing import Optional, List

router = APIRouter()
logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class UserProfile(BaseModel):
    """用户模板信息，用于个性化对话"""
    name: Optional[str] = Field(None, description="用户名字")
    gender: Optional[str] = Field(None, description="用户性别")
    star_sign: Optional[str] = Field(None, description="用户星座")
    personality_tags: Optional[List[str]] = Field(None, description="性格特点标签")
    hobby_tags: Optional[List[str]] = Field(None, description="兴趣爱好标签")
    personal_motto: Optional[str] = Field(None, description="个人座右铭")

class DialogRequest(BaseModel):
    messages: list[Message]
    scene: str = "self-dialog"  # 场景标识，默认自我对话
    user_profile: Optional[UserProfile] = Field(None, description="用户模板信息（可选）")

class DialogResponse(BaseModel):
    content: str

class AIConfig:
    """AI 服务配置类，便于未来更换不同的 AI 模型"""
    
    def __init__(self):
        # 从配置文件读取，不再使用硬编码默认值
        self.api_url = settings.ai_api_url
        self.api_key = settings.ai_api_key  
        self.model = settings.ai_model
        self.temperature = settings.ai_temperature
        self.max_tokens = settings.ai_max_tokens
        self.top_p = settings.ai_top_p
        self.timeout = settings.ai_timeout
    
    def get_headers(self):
        """获取请求头，支持不同 AI 服务的认证方式"""
        if "openai" in self.api_url.lower():
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        elif "suanli" in self.api_url.lower():
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        else:
            # 默认 OpenAI 兼容格式
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
    
    def build_payload(self, messages: list, scene: str, user_profile=None):
        """构建请求负载，支持不同 AI 模型的参数格式"""
        logger.info(f"📝 构建 AI 请求负载")
        logger.info(f"📌 场景: {scene}")
        logger.info(f"📌 消息条数: {len(messages)}")
        logger.info(f"📌 用户模板信息: {user_profile}")
        
        system_prompt = PROMPTS.get(scene, PROMPTS["self-dialog"])
        
        # 确保 system_prompt 是字符串类型
        if not isinstance(system_prompt, str):
            system_prompt = str(system_prompt)
        
        logger.info(f"🎯 基础 System Prompt 长度: {len(system_prompt)} 字符")
        
        # 如果提供了用户模板信息，则进行动态调整
        if user_profile:
            logger.info(f"✨ 检测到用户模板信息，正在进行 Prompt 动态调整...")
            system_prompt = self._enhance_prompt_with_user_profile(system_prompt, user_profile)
            logger.info(f"✨ 增强后的 System Prompt 长度: {len(system_prompt)} 字符")
        
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }
        
        # 添加历史对话（最多8条）
        for i, msg in enumerate(messages[-8:]):
            # 处理角色映射
            role = msg.role
            if role == "ai":
                role = "assistant"
            
            # 确保 content 是字符串类型，处理各种可能的类型
            content = msg.content
            if content is None:
                content = ""
            elif not isinstance(content, str):
                content = str(content)
            
            # 确保 content 不为空
            if not content.strip():
                continue  # 跳过空消息
            
            logger.info(f"  📤 消息 {i+1}: [{role.upper()}] {content[:50]}..." if len(content) > 50 else f"  📤 消息 {i+1}: [{role.upper()}] {content}")
            payload["messages"].append({"role": role, "content": content})
        
        return payload
    
    def _enhance_prompt_with_user_profile(self, base_prompt: str, user_profile):
        """根据用户模板信息动态调整 System Prompt"""
        logger.info("=" * 80)
        logger.info("🎨 开始动态调整 System Prompt")
        logger.info("=" * 80)
        
        # 构建用户信息部分
        user_info_section = "\n## 用户个人信息（用于个性化对话）\n"
        
        if user_profile.name:
            user_info_section += f"- 名字：{user_profile.name}\n"
            logger.info(f"  ✅ 用户名字: {user_profile.name}")
        
        if user_profile.gender:
            user_info_section += f"- 性别：{user_profile.gender}\n"
            logger.info(f"  ✅ 性别: {user_profile.gender}")
        
        if user_profile.star_sign:
            user_info_section += f"- 星座：{user_profile.star_sign}\n"
            logger.info(f"  ✅ 星座: {user_profile.star_sign}")
        
        if user_profile.personality_tags:
            tags_str = "、".join(user_profile.personality_tags)
            user_info_section += f"- 性格特点：{tags_str}\n"
            logger.info(f"  ✅ 性格特点: {tags_str}")
        
        if user_profile.hobby_tags:
            hobbies_str = "、".join(user_profile.hobby_tags)
            user_info_section += f"- 兴趣爱好：{hobbies_str}\n"
            logger.info(f"  ✅ 兴趣爱好: {hobbies_str}")
        
        if user_profile.personal_motto:
            user_info_section += f"- 座右铭：{user_profile.personal_motto}\n"
            logger.info(f"  ✅ 座右铭: {user_profile.personal_motto}")
        
        # 构建个性化建议部分
        personalization_advice = "\n## 个性化对话建议\n"
        
        if user_profile.personality_tags:
            tags_str = "、".join(user_profile.personality_tags)
            personalization_advice += f"根据{tags_str}的性格特点，调整你的对话风格，使用相关的例子和参考。\n"
        
        if user_profile.hobby_tags:
            hobbies_str = "、".join(user_profile.hobby_tags)
            personalization_advice += f"当提供建议时，可以结合用户对{hobbies_str}的热情来举例。\n"
        
        if user_profile.personal_motto:
            personalization_advice += f"用户的座右铭是'{user_profile.personal_motto}'，在对话中可以提及这体现了怎样的价值观。\n"
        
        if user_profile.star_sign:
            personalization_advice += f"可以适当参考{user_profile.star_sign}座的性格特点来深化对话。\n"
        
        personalization_advice += "总体原则：在保持专业态度的前提下，让用户感到被看见和理解。\n"
        
        logger.info("📋 个性化建议:")
        logger.info(personalization_advice)
        
        # 组合最终的 prompt
        enhanced_prompt = base_prompt + user_info_section + personalization_advice
        
        logger.info("=" * 80)
        logger.info(f"✨ Prompt 增强完成！总长度: {len(enhanced_prompt)} 字符")
        logger.info("=" * 80)
        
        return enhanced_prompt

ai_config = AIConfig()

@router.post("/ai-dialog", response_model=DialogResponse)
async def ai_dialog(data: DialogRequest, request: Request):
    """AI 对话接口，支持多种 AI 模型"""
    try:
        logger.info("=" * 80)
        logger.info("🚀 收到 AI 对话请求")
        logger.info("=" * 80)
        logger.info(f"📌 场景: {data.scene}")
        logger.info(f"📌 消息总数: {len(data.messages)}")
        logger.info(f"📌 用户模板信息提供: {'是' if data.user_profile else '否'}")
        
        if data.user_profile:
            logger.info("📋 用户模板详情:")
            logger.info(f"  - 名字: {data.user_profile.name}")
            logger.info(f"  - 性别: {data.user_profile.gender}")
            logger.info(f"  - 星座: {data.user_profile.star_sign}")
            logger.info(f"  - 性格标签: {data.user_profile.personality_tags}")
            logger.info(f"  - 兴趣标签: {data.user_profile.hobby_tags}")
            logger.info(f"  - 座右铭: {data.user_profile.personal_motto}")
        
        logger.info("💬 消息内容:")
        for i, msg in enumerate(data.messages):
            content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            logger.info(f"  [{i+1}] {msg.role.upper()}: {content_preview}")
        
        # 构造请求负载，传递用户模板信息
        payload = ai_config.build_payload(
            data.messages, 
            data.scene,
            user_profile=data.user_profile  # ◄─ 传递用户模板信息
        )
        headers = ai_config.get_headers()
        
        # 检查 API Key 是否配置
        if not ai_config.api_key:
            logger.error("AI API Key 未配置")
            return DialogResponse(content="AI 服务配置错误，请联系管理员。")
        
        async with httpx.AsyncClient(timeout=ai_config.timeout) as client:
            try:
                resp = await client.post(
                    ai_config.api_url,
                    headers=headers,
                    json=payload
                )
                resp.raise_for_status()
                
                response_data = resp.json()
                if response_data.get("choices") and len(response_data["choices"]) > 0:
                    content = response_data["choices"][0]["message"]["content"]
                    logger.info("=" * 80)
                    logger.info("✅ AI 响应成功")
                    logger.info("=" * 80)
                    logger.info(f"📝 原始响应长度: {len(content)} 字符")
                    logger.info(f"📝 原始响应预览: {content[:100]}...")
                    
                    # 内容优化过滤
                    optimized = optimize_ai_response(content)
                    logger.info(f"✨ 优化后响应长度: {len(optimized)} 字符")
                    logger.info(f"✨ 优化后响应内容: {optimized}")
                    logger.info("=" * 80)
                    return DialogResponse(content=optimized)
                else:
                    logger.warning(f"AI 响应格式异常: {response_data}")
                    return DialogResponse(content="AI 响应异常，请稍后再试。")
                    
            except httpx.TimeoutException:
                logger.error("AI 服务超时")
                return DialogResponse(content="AI 服务响应超时，请稍后再试。")
            except httpx.HTTPStatusError as e:
                logger.error(f"AI 服务 HTTP 错误: {e.response.status_code} - {e.response.text}")
                return DialogResponse(content="AI 服务暂时不可用，请稍后再试。")
            except Exception as e:
                logger.error(f"AI 服务请求异常: {str(e)}")
                return DialogResponse(content="AI 服务异常，请稍后再试。")
                
    except Exception as e:
        logger.error(f"AI 对话处理异常: {str(e)}")
        return DialogResponse(content="系统异常，请稍后再试。")

# AI回复内容优化，去除标签、无关信息，保证体验
def optimize_ai_response(content: str) -> str:
    import re
    optimized = re.sub(r"<think>[\s\S]*?</think>", "", content)
    optimized = re.sub(r"<think>[\s\S]*", "", optimized)
    optimized = re.sub(r"我不想展示.*?因为这会影响用户体验", "", optimized)
    optimized = re.sub(r"^(AI|助手|阿德涅)[:：]\s*", "", optimized)
    optimized = re.sub(r"^(我是|作为)[^，。]*[，。]\s*", "", optimized)
    optimized = re.sub(r"\[.*?\]", "", optimized)
    optimized = re.sub(r"（.*?思考.*?）", "", optimized)
    optimized = re.sub(r"\*.*?思考.*?\*", "", optimized)
    optimized = re.sub(r"【.*?】", "", optimized)
    optimized = re.sub(r"^\s*[-*•]\s*", "", optimized, flags=re.MULTILINE)
    optimized = re.sub(r"\n\s*\n", "\n", optimized)
    optimized = optimized.strip()
    if len(optimized) < 20:
        optimized = "我理解你的感受。能告诉我更多关于这个情况的细节吗？这样我能更好地陪伴你进行这场自我对话。"
    if len(optimized) > 500:
        optimized = optimized[:500] + "..."
    if not optimized or len(optimized) < 5:
        optimized = "我正在认真思考你的话。你能再详细说说这个情况吗？我想更好地理解你的感受。"
    return optimized
