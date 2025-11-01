# 多模态AI对话路由（支持图片上传和数据库存储）
# file: ariadne/backend/app/api/routes/multimodal_chat.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
from sqlalchemy.orm import Session
import logging
import base64

from app.core.multimodal_ai_service import MultimodalAIService
from app.services.picui_service import picui_service
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.chat_history import ChatMessage, ChatSession

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

class ImageBase64ChatRequest(BaseModel):
    text: str
    image_base64: str
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

@router.post("/chat/image-upload-base64", response_model=ChatResponse)
async def image_upload_base64_chat(request: ImageBase64ChatRequest):
    """接收base64图片进行多模态对话（H5环境使用）"""
    try:
        logger.info("[多模态] 收到base64图片上传请求")
        logger.info(f"[多模态] base64长度: {len(request.image_base64)}")
        
        # 验证base64数据
        if not request.image_base64:
            raise HTTPException(status_code=400, detail="缺少图片数据")
        
        # 调用多模态AI服务
        result = await multimodal_service.chat_with_image(
            text=request.text,
            image_data=request.image_base64,
            scene=request.scene
        )
        
        logger.info("[多模态] base64图片分析完成")
        
        return ChatResponse(
            content=result["content"],
            scene=request.scene,
            model_used=multimodal_service.vision_model
        )
        
    except Exception as e:
        logger.error(f"base64图片上传对话异常: {e}")
        raise HTTPException(status_code=500, detail="图片上传对话服务异常")

@router.get("/models/status")
async def get_models_status():
    """获取当前模型配置状态"""
    return {
        "text_model": multimodal_service.text_model,
        "vision_model": multimodal_service.vision_model,
        "status": "active"
    }

# ==================== 新增：支持数据库存储的多模态消息接口 ====================

@router.post("/chat/message")
async def send_multimodal_message(
    session_id: int = Form(...),
    content: str = Form(""),
    msg_type: str = Form("text"),
    files: Optional[Union[List[UploadFile], UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发送多模态消息到会话（保存到数据库）
    支持纯文本、纯图片、图文混合三种类型
    """
    try:
        logger.info("=" * 80)
        logger.info("[多模态] 收到多模态消息发送请求")
        logger.info(f"[多模态] 用户ID: {current_user.user_id}")
        logger.info(f"[多模态] 会话ID: {session_id}")
        logger.info(f"[多模态] 内容: {content}")
        
        # 处理文件：统一转换为列表
        file_list = []
        if files:
            if isinstance(files, list):
                file_list = files
            else:
                file_list = [files]
        
        logger.info(f"[多模态] 文件数量: {len(file_list)}")
        
        # 1. 验证会话
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.user_id
        ).first()
        
        if not session:
            logger.error(f"[多模态] 会话不存在: session_id={session_id}, user_id={current_user.user_id}")
            raise HTTPException(status_code=404, detail="会话不存在")
        
        logger.info(f"[多模态] 会话验证成功，场景: {session.scene}")
        
        # 2. 上传图片
        img_urls = []
        image_base64_for_ai = []  # 保存原始数据用于AI分析
        
        if file_list:
            logger.info(f"[多模态] 开始上传图片，共 {len(file_list)} 个文件")
            for idx, file in enumerate(file_list):
                logger.info(f"[多模态] 处理第 {idx+1} 个文件: {file.filename}")
                
                if not picui_service.is_valid_image_type(file.filename):
                    logger.warning(f"[多模态] 文件类型不支持: {file.filename}")
                    continue
                
                file_content = await file.read()
                logger.info(f"[多模态] 文件大小: {len(file_content)} bytes")
                
                if not picui_service.is_valid_file_size(len(file_content)):
                    logger.warning(f"[多模态] 文件过大: {len(file_content)} bytes")
                    continue
                
                # 转换为base64用于AI分析（阿里百炼需要）
                image_b64 = base64.b64encode(file_content).decode('utf-8')
                image_base64_for_ai.append(image_b64)
                logger.info(f"[多模态] 图片转换为base64完成")
                
                result = await picui_service.upload_image(
                    file_content=file_content,
                    filename=file.filename,
                    permission=1
                )
                
                if result.get("success") and result.get("data"):
                    img_url = result["data"].get("url")
                    img_urls.append(img_url)
                    logger.info(f"[多模态] 图片上传成功: {img_url}")
                else:
                    logger.error(f"[多模态] 图片上传失败: {result.get('message')}")
        
        logger.info(f"[多模态] 图片上传完成，成功: {len(img_urls)} 张")
        
        # 3. 确定消息类型
        has_text = bool(content.strip())
        has_img = bool(img_urls)
        
        if has_text and has_img:
            actual_msg_type = "multimodal"
        elif has_img:
            actual_msg_type = "img"
        else:
            actual_msg_type = "text"
        
        logger.info(f"[多模态] 消息类型: {actual_msg_type} (has_text={has_text}, has_img={has_img})")
        
        # 4. 创建用户消息
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            msg_type=actual_msg_type,
            content=content or "",
            img_urls=img_urls if img_urls else None
        )
        db.add(user_message)
        db.flush()
        logger.info(f"[多模态] 用户消息已创建，ID: {user_message.id}")
        
        # 5. 生成AI回复
        ai_content = ""
        if actual_msg_type in ["img", "multimodal"]:
            # 多模态响应 - 使用base64格式（阿里百炼需要）
            prompt = content if content else "请分析这张图片"
            logger.info(f"[多模态] 调用多模态AI，prompt长度: {len(prompt)}")
            logger.info(f"[多模态] 使用Base64格式发送图片给AI")
            
            # 使用base64数据而不是URL
            image_data_for_ai = image_base64_for_ai[0] if image_base64_for_ai else ""
            
            result = await multimodal_service.chat_with_image(
                text=prompt,
                image_data=image_data_for_ai,
                scene=session.scene
            )
            ai_content = result.get("content", "抱歉，我暂时无法分析这张图片。")
            logger.info(f"[多模态] AI回复生成成功，长度: {len(ai_content)}")
        else:
            # 纯文本响应
            logger.info("[多模态] 调用文本AI")
            history = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.created_at.desc()).limit(8).all()
            
            messages = []
            for msg in reversed(history):
                messages.append({
                    "role": "user" if msg.role == "user" else "assistant",
                    "content": msg.content
                })
            messages.append({"role": "user", "content": content})
            
            ai_content = await multimodal_service.chat_with_text(
                messages=messages,
                scene=session.scene
            )
            logger.info(f"[多模态] AI回复生成成功，长度: {len(ai_content)}")
        
        # 6. 创建AI回复消息
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            msg_type="text",
            content=ai_content,
            img_urls=None
        )
        db.add(assistant_message)
        
        # 7. 提交
        db.commit()
        db.refresh(user_message)
        db.refresh(assistant_message)
        
        logger.info(f"[多模态] 消息保存成功")
        logger.info("=" * 80)
        
        return {
            "success": True,
            "user_message": {
                "id": user_message.id,
                "role": user_message.role,
                "msg_type": str(user_message.msg_type),
                "content": user_message.content,
                "img_urls": user_message.img_urls,
                "created_at": user_message.created_at.isoformat()
            },
            "assistant_message": {
                "id": assistant_message.id,
                "role": assistant_message.role,
                "msg_type": str(assistant_message.msg_type),
                "content": assistant_message.content,
                "created_at": assistant_message.created_at.isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"[多模态] 发送消息失败: {type(e).__name__}")
        logger.error(f"[多模态] 错误详情: {str(e)}")
        import traceback
        logger.error(f"[多模态] 异常堆栈: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"发送失败: {str(e)}")


@router.get("/chat/messages/{session_id}")
async def get_multimodal_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取会话的所有消息（包含多模态）"""
    try:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.user_id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()
        
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "role": msg.role,
                "msg_type": str(msg.msg_type) if msg.msg_type else "text",
                "content": msg.content,
                "img_urls": msg.img_urls,
                "created_at": msg.created_at.isoformat()
            })
        
        return {"success": True, "messages": result}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取消息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")
