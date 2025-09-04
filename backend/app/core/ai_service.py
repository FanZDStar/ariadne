# AI服务模块
# file: ariadne/backend/app/core/ai_service.py

import httpx
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import PROMPTS

logger = logging.getLogger(__name__)

class AIService:
    """AI服务类，用于危机检测等场景的AI分析"""
    
    def __init__(self):
        self.api_url = settings.ai_api_url
        self.api_key = settings.ai_api_key  
        self.model = settings.ai_model
        self.temperature = settings.ai_temperature
        self.max_tokens = settings.ai_max_tokens
        self.top_p = settings.ai_top_p
        self.timeout = settings.ai_timeout
    
    def get_headers(self):
        """获取请求头"""
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
    
    async def get_response(self, messages: List[Dict[str, str]], scene: str = "crisis_analysis") -> str:
        """
        获取AI分析响应
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            scene: 分析场景，默认为危机分析
            
        Returns:
            str: AI分析结果
        """
        try:
            # 构造请求负载
            payload = self._build_payload(messages, scene)
            headers = self.get_headers()
            
            # 检查 API Key 是否配置
            if not self.api_key:
                logger.error("AI API Key 未配置")
                return "AI服务配置错误，无法进行分析。"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    resp = await client.post(
                        self.api_url,
                        headers=headers,
                        json=payload
                    )
                    resp.raise_for_status()
                    
                    response_data = resp.json()
                    if response_data.get("choices") and len(response_data["choices"]) > 0:
                        content = response_data["choices"][0]["message"]["content"]
                        return content.strip()
                    else:
                        logger.warning("AI响应格式异常")
                        return "AI分析响应格式异常。"
                        
                except httpx.HTTPStatusError as e:
                    logger.error(f"AI API HTTP错误: {e.response.status_code} - {e.response.text}")
                    return "AI服务暂时不可用，建议人工评估。"
                except httpx.TimeoutException:
                    logger.error("AI API请求超时")
                    return "AI分析超时，建议关注用户状态。"
                except Exception as e:
                    logger.error(f"AI API请求异常: {e}")
                    return "AI分析遇到技术问题。"
                    
        except Exception as e:
            logger.error(f"AI服务调用失败: {e}")
            return "AI分析服务不可用。"
    
    def _build_payload(self, messages: List[Dict[str, str]], scene: str) -> Dict[str, Any]:
        """构建API请求负载"""
        # 根据场景选择系统提示词
        system_prompt = self._get_system_prompt(scene)
        
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "messages": []
        }
        
        # 添加系统提示词
        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        
        # 添加用户消息
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            # 数据清理
            if content is None:
                content = ""
            elif not isinstance(content, str):
                content = str(content)
            
            # 确保 content 不为空
            if content.strip():
                payload["messages"].append({"role": role, "content": content})
        
        return payload
    
    def _get_system_prompt(self, scene: str) -> str:
        """根据场景获取系统提示词"""
        if scene == "crisis_analysis":
            return """你是一位专业的心理健康顾问，专门进行心理危机评估。请客观、专业地分析用户输入的内容，识别潜在的心理健康风险。

分析重点：
1. 自伤或自杀倾向
2. 极端负面情绪
3. 绝望或无助感
4. 社会支持缺失
5. 危机干预需求

请用简洁、专业的语言给出评估，控制在100字以内。如果没有明显风险，请给出积极的心理支持建议。"""
        
        # 可以根据需要添加其他场景的提示词
        return PROMPTS.get(scene, {}).get("system", "")
