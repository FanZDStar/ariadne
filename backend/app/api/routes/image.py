#file:ariadne/backend/app/api/routes/image.py
import os
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import shutil
from app.api.deps import get_current_user
from app.models.user import User
from app.services.picui_service import picui_service

router = APIRouter(prefix="/image", tags=["图片上传"])

# 确保上传目录存在（作为备用方案）
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传图片"""
    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 验证文件扩展名
    if not picui_service.is_valid_image_type(file.filename):
        raise HTTPException(status_code=400, detail="不支持的图片格式")
    
    try:
        # 读取文件内容
        file_content = await file.read()
        
        # 检查文件大小
        if not picui_service.is_valid_file_size(len(file_content), 10):
            raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
        
        # 上传到图床
        upload_result = await picui_service.upload_image(
            file_content=file_content,
            filename=file.filename,
            permission=1  # 公开
        )
        
        if upload_result["success"]:
            print(f"[存储] ✅ 图片已上传到图床，使用图床URL")
            data = upload_result["data"]
            return {
                "url": data["url"],
                "filename": data["name"],
                "thumbnail_url": data.get("thumbnail_url"),
                "size": data.get("size"),
                "key": data.get("key")
            }
        else:
            # 如果图床上传失败，回退到本地存储
            print(f"[存储] ⚠️  图床上传失败，回退到本地存储: {upload_result.get('message', '未知错误')}")
            file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            full_url = f"/uploads/{unique_filename}"
            
            return {
                "url": full_url,
                "filename": unique_filename,
                "fallback": True,
                "message": "图床上传失败，已保存到本地"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")