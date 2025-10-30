# 多模态AI对话路由（简化版）
# file: ariadne/backend/app/api/routes/multimodal_chat.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import base64
from app.core.multimodal_ai_service import MultimodalAIService

router = APIRouter()
logger = logging.getLogger(__name__)

# 创建服务实例
multimodal_service = MultimodalAIService()

class TextChatRequest(BaseModel):
    message: str
    scene: str = "general"
    history: List[Dict[str, str]] = []

class ImageChatRequest(BaseModel):
    text: str
    image_url: Optional[str] = None
    scene: str = "image_analysis"

class ChatResponse(BaseModel):
    content: str
    scene: str
    model_used: str

@router.post("/chat/text", response_model=ChatResponse)
async def text_chat(request: TextChatRequest):
    """纯文本对话"""
    try:
        # 构建消息历史
        messages = request.history + [{"role": "user", "content": request.message}]
        
        # 调用AI服务
        response = await multimodal_service.chat_with_text(
            messages=messages,
            scene=request.scene
        )
        
        return ChatResponse(
            content=response,
            scene=request.scene,
            model_used=multimodal_service.text_model
        )
        
    except Exception as e:
        logger.error(f"文本对话异常: {e}")
        raise HTTPException(status_code=500, detail="对话服务异常")

@router.post("/chat/image", response_model=ChatResponse)
async def image_chat(request: ImageChatRequest):
    """图像+文本多模态对话"""
    try:
        if not request.image_url:
            raise HTTPException(status_code=400, detail="缺少图像数据")
        
        # 调用多模态AI服务
        result = await multimodal_service.chat_with_image(
            text=request.text,
            image_data=request.image_url,
            scene=request.scene
        )
        
        return ChatResponse(
            content=result["content"],
            scene=request.scene,
            model_used=multimodal_service.vision_model
        )
        
    except Exception as e:
        logger.error(f"图像对话异常: {e}")
        raise HTTPException(status_code=500, detail="图像对话服务异常")

@router.post("/chat/image-upload", response_model=ChatResponse)
async def image_upload_chat(
    text: str = Form(...),
    image: UploadFile = File(...),
    scene: str = Form("image_analysis")
):
    """上传图片进行多模态对话"""
    try:
        # 验证图片格式
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="请上传图片文件")
        
        # 读取图片并转换为base64
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 调用多模态AI服务
        result = await multimodal_service.chat_with_image(
            text=text,
            image_data=image_base64,
            scene=scene
        )
        
        return ChatResponse(
            content=result["content"],
            scene=scene,
            model_used=multimodal_service.vision_model
        )
        
    except Exception as e:
        logger.error(f"图片上传对话异常: {e}")
        raise HTTPException(status_code=500, detail="图片上传对话服务异常")

@router.get("/models/status")
async def get_models_status():
    """获取当前模型配置状态"""
    return {
        "text_model": multimodal_service.text_model,
        "vision_model": multimodal_service.vision_model,
        "status": "active"
    }
