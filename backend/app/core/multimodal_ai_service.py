# 多模态AI服务模块
# file: ariadne/backend/app/core/multimodal_ai_service.py

import httpx
import base64
import logging
import json
from typing import List, Dict, Any, Optional, Union
from app.core.config import settings
from app.core.prompts import PROMPTS

logger = logging.getLogger(__name__)

class MultimodalAIService:
    """多模态AI服务类，支持文本、图像理解"""
    
    def __init__(self):
        self.api_url = settings.ai_api_url
        self.api_key = settings.ai_api_key
        self.text_model = settings.ai_model
        self.vision_model = getattr(settings, 'ai_vision_model', 'qwen-vl-max')
        self.temperature = settings.ai_temperature
        self.max_tokens = settings.ai_max_tokens
        self.vision_max_tokens = getattr(settings, 'ai_vision_max_tokens', 1500)
        self.top_p = settings.ai_top_p
        self.timeout = settings.ai_timeout
    
    async def chat_with_text(self, messages: List[Dict[str, str]], scene: str = "general") -> str:
        """
        纯文本对话
        
        Args:
            messages: 消息列表
            scene: 场景类型
            
        Returns:
            str: AI回复内容
        """
        try:
            # 构建消息
            formatted_messages = self._format_text_messages(messages, scene)
            
            # 构建请求负载
            payload = {
                "model": self.text_model,
                "messages": formatted_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                if data.get("choices") and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    return content.strip()
                else:
                    return "AI响应格式异常"
            
        except Exception as e:
            logger.error(f"文本对话服务异常: {e}")
            return "抱歉，我暂时无法回应。请稍后再试。"
    
    async def chat_with_image(self, 
                            text: str, 
                            image_data: Union[str, bytes], 
                            scene: str = "image_analysis",
                            use_thinking: bool = False) -> Dict[str, str]:
        """
        图像+文本多模态对话
        
        Args:
            text: 文本内容
            image_data: 图像数据（URL或base64编码）
            scene: 场景类型
            use_thinking: 是否启用思维链推理
            
        Returns:
            Dict: 包含回复内容的字典
        """
        try:
            logger.info(f"[多模态AI] 开始处理图片对话")
            logger.info(f"[多模态AI] 文本内容: {text}")
            logger.info(f"[多模态AI] 图片数据类型: {type(image_data)}")
            logger.info(f"[多模态AI] 场景: {scene}")
            
            # 处理图像数据
            image_content = self._process_image_data(image_data)
            logger.info(f"[多模态AI] 图片内容处理完成: {image_content.get('type')}")
            
            # 构建消息
            messages = self._format_vision_messages(text, image_content, scene)
            logger.info(f"[多模态AI] 消息构建完成，消息数: {len(messages)}")
            
            # 构建请求参数
            payload = {
                "model": self.vision_model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.vision_max_tokens,
                "top_p": self.top_p
            }
            
            if use_thinking:
                payload["max_tokens"] = min(self.vision_max_tokens * 2, 4000)
                logger.info(f"[多模态AI] 启用思维链推理")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            logger.info(f"[多模态AI] 发送请求到: {self.api_url}")
            logger.info(f"[多模态AI] 使用模型: {self.vision_model}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                logger.info(f"[多模态AI] 收到响应，状态码: {response.status_code}")
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"[多模态AI] 响应解析成功")
                
                if data.get("choices") and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    logger.info(f"[多模态AI] 提取内容长度: {len(content)}")
                    return {
                        "content": content.strip(),
                        "reasoning": ""
                    }
                else:
                    logger.warning(f"[多模态AI] AI响应格式异常: {data}")
                    return {
                        "content": "AI响应格式异常",
                        "reasoning": ""
                    }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"[多模态AI] HTTP错误: {e.response.status_code} - {e.response.text}")
            return {
                "content": "抱歉，我暂时无法分析这张图片。服务异常，请稍后再试。",
                "reasoning": ""
            }
        except httpx.TimeoutException as e:
            logger.error(f"[多模态AI] 请求超时: {e}")
            return {
                "content": "抱歉，分析图片耗时过长，请稍后再试。",
                "reasoning": ""
            }
        except Exception as e:
            logger.error(f"[多模态AI] 服务异常: {type(e).__name__} - {str(e)}")
            import traceback
            logger.error(f"[多模态AI] 异常堆栈: {traceback.format_exc()}")
            return {
                "content": "抱歉，我暂时无法分析这张图片。请稍后再试。",
                "reasoning": ""
            }
    
    async def analyze_emotion_image(self, image_data: Union[str, bytes], context: str = "") -> Dict[str, Any]:
        """
        情感图片分析（专门用于心理健康场景）
        
        Args:
            image_data: 图像数据
            context: 上下文信息
            
        Returns:
            Dict: 情感分析结果
        """
        prompt = f"""
        请分析这张图片中体现的情感状态，重点关注：
        1. 情感类型（开心、悲伤、焦虑、愤怒等）
        2. 情感强度（1-10级）
        3. 可能的心理状态
        4. 建议的关怀方式
        
        上下文信息：{context}
        
        请用温暖、专业的语调回复，避免过度解读。
        """
        
        result = await self.chat_with_image(
            text=prompt,
            image_data=image_data,
            scene="emotion_analysis",
            use_thinking=True
        )
        
        return {
            "emotion_analysis": result["content"],
            "reasoning_process": result["reasoning"],
            "scene": "emotion_analysis"
        }
    
    def _format_text_messages(self, messages: List[Dict[str, str]], scene: str) -> List[Dict[str, str]]:
        """格式化文本消息"""
        formatted = []
        
        # 添加系统提示词
        system_prompt = self._get_system_prompt(scene)
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        
        # 添加历史消息
        for msg in messages[-8:]:  # 限制上下文长度
            role = msg.get("role", "user")
            if role == "ai":
                role = "assistant"
            
            content = str(msg.get("content", "")).strip()
            if content:
                formatted.append({"role": role, "content": content})
        
        return formatted
    
    def _format_vision_messages(self, text: str, image_content: Dict, scene: str) -> List[Dict[str, Any]]:
        """格式化多模态消息"""
        messages = []
        
        # 添加系统提示词
        system_prompt = self._get_system_prompt(scene)
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加用户消息（文本+图像）
        user_content = [
            {"type": "text", "text": text},
            image_content
        ]
        
        messages.append({
            "role": "user", 
            "content": user_content
        })
        
        return messages
    
    def _process_image_data(self, image_data: Union[str, bytes]) -> Dict[str, Any]:
        """处理图像数据"""
        if isinstance(image_data, str):
            if not image_data:
                raise ValueError("图片数据为空")
            
            if image_data.startswith(('http://', 'https://')):
                # URL格式
                logger.info(f"[图片处理] 使用URL格式: {image_data[:50]}...")
                return {
                    "type": "image_url",
                    "image_url": {"url": image_data}
                }
            else:
                # Base64格式
                logger.info(f"[图片处理] 使用Base64格式")
                return {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
        elif isinstance(image_data, bytes):
            # 字节数据转base64
            logger.info(f"[图片处理] 转换字节数据为Base64")
            if not image_data:
                raise ValueError("图片字节数据为空")
            
            encoded = base64.b64encode(image_data).decode('utf-8')
            return {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
            }
        else:
            raise ValueError(f"不支持的图像数据格式: {type(image_data)}")
    

    
    def _get_system_prompt(self, scene: str) -> str:
        """获取系统提示词"""
        # 优先使用PROMPTS中的场景提示词
        if scene in PROMPTS:
            logger.info(f"[系统提示词] 使用场景: {scene}")
            return PROMPTS[scene]
        
        # 多模态特定场景
        multimodal_prompts = {
            "emotion_analysis": """你是一位专业的心理健康顾问，擅长通过图像分析用户的情感状态。
请用温暖、专业的语调提供分析，避免过度诊断。重点关注情感支持和积极引导。""",
            "image_analysis": "你是一个专业的图像分析助手，能够准确理解和描述图像内容。",
            "crisis_analysis": """你是一位专业的心理危机评估专家。请客观分析潜在风险，
重点关注自伤倾向、极端情绪、绝望感等。给出专业建议但避免过度反应。""",
            "general": "你是一个温暖、专业的AI助手，擅长理解和分析图像内容，并用专业的态度回应用户。"
        }
        
        return multimodal_prompts.get(scene, multimodal_prompts["general"])

# 创建全局实例
multimodal_ai_service = MultimodalAIService()
