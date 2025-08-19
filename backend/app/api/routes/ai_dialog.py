from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import httpx
import logging
from app.core.config import settings
from app.core.prompts import PROMPTS

router = APIRouter()
logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class DialogRequest(BaseModel):
    messages: list[Message]
    scene: str = "self-dialog"  # 场景标识，默认自我对话

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
    
    def build_payload(self, messages: list, scene: str):
        """构建请求负载，支持不同 AI 模型的参数格式"""
        system_prompt = PROMPTS.get(scene, PROMPTS["self-dialog"])
        
        # 确保 system_prompt 是字符串类型
        if not isinstance(system_prompt, str):
            system_prompt = str(system_prompt)
        
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }
        
        # 添加历史对话（最多8条）
        for msg in messages[-8:]:
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
            
            payload["messages"].append({"role": role, "content": content})
        
        return payload

ai_config = AIConfig()

@router.post("/ai-dialog", response_model=DialogResponse)
async def ai_dialog(data: DialogRequest, request: Request):
    """AI 对话接口，支持多种 AI 模型"""
    try:
        # 构造请求负载
        payload = ai_config.build_payload(data.messages, data.scene)
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
                    # 内容优化过滤
                    optimized = optimize_ai_response(content)
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
