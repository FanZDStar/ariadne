# backend/app/api/routes/user_diary_backgrounds.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil
from datetime import datetime

from app.database.session import get_db
from app.models.user import User
from app.models.user_diary_backgrounds import UserDiaryBackground
from app.schemas.user_diary_backgrounds import UserDiaryBackgroundResponse, UserDiaryBackgroundWithStarResponse
from app.api.deps import get_current_user
from app.services.star_point_service import StarPointService
from app.utils.star_point_types import StarPointAction, SourceType

router = APIRouter(prefix="/user-diary-backgrounds", tags=["用户日记背景图片"])

# 允许的图片文件类型和最大文件大小
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_USER_BACKGROUNDS = 4  # 每个用户最多4张背景图片

# 确保上传目录存在
UPLOAD_DIR = "uploads/diary-backgrounds"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

async def delete_image_file(file_path: str):
    """删除图片文件（图床或本地）"""
    try:
        if file_path.startswith('http'):
            # 图床URL - 暂时跳过删除，因为PICUI API可能不支持删除或需要特殊key格式
            print(f"[删除] ⚠️  跳过图床图片删除（API不支持）: {file_path}")
            # TODO: 如果找到正确的删除API，可以重新启用
        else:
            # 本地文件
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[删除] ✅ 本地文件删除成功: {file_path}")
            else:
                print(f"[删除] ⚠️  本地文件不存在: {file_path}")
    except Exception as e:
        print(f"[删除] ❌ 删除图片失败: {str(e)}")
        # 不抛出异常，避免阻塞数据库删除


@router.get("/", response_model=List[UserDiaryBackgroundResponse])
def get_user_backgrounds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有背景图片"""
    backgrounds = db.query(UserDiaryBackground)\
                   .filter(UserDiaryBackground.user_id == current_user.user_id)\
                   .filter(UserDiaryBackground.is_active == True)\
                   .order_by(UserDiaryBackground.upload_time.desc())\
                   .all()
    
    return [UserDiaryBackgroundResponse(**bg.to_dict()) for bg in backgrounds]


@router.post("/upload", response_model=UserDiaryBackgroundWithStarResponse)
async def upload_background(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传新的背景图片"""
    
    # 检查用户背景图片数量限制
    existing_count = db.query(UserDiaryBackground)\
                      .filter(UserDiaryBackground.user_id == current_user.user_id)\
                      .filter(UserDiaryBackground.is_active == True)\
                      .count()
    
    if existing_count >= MAX_USER_BACKGROUNDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"每个用户最多只能上传{MAX_USER_BACKGROUNDS}张背景图片"
        )
    
    # 验证文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型。支持的格式：{', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 读取文件内容以验证文件大小
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大{MAX_FILE_SIZE // 1024 // 1024}MB）"
        )
    
    try:
        # 导入图床服务
        from app.services.picui_service import picui_service
        
        # 上传到图床
        upload_result = await picui_service.upload_image(
            file_content=file_content,
            filename=file.filename,
            permission=0  # 私有图片，仅上传者可见
        )
        
        if upload_result["success"]:
            # 图床上传成功，使用图床URL
            print(f"[存储] ✅ 图片已上传到图床，使用图床URL")
            data = upload_result["data"]
            file_path = data["url"]  # 使用图床URL作为文件路径
            unique_filename = data["name"]
        else:
            # 图床上传失败，回退到本地存储
            print(f"[存储] ⚠️  图床上传失败，回退到本地存储: {upload_result.get('message', '未知错误')}")
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            local_file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(local_file_path, "wb") as buffer:
                buffer.write(file_content)
            
            file_path = local_file_path
        
        # 创建数据库记录
        db_background = UserDiaryBackground(
            user_id=current_user.user_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,  # 这里现在是图床URL或本地路径
            file_size=len(file_content),
            upload_time=datetime.now(),
            is_active=True
        )
        
        db.add(db_background)
        db.commit()
        db.refresh(db_background)
        
        # 尝试奖励星星点数
        star_service = StarPointService(db)
        star_result = star_service.award_points(
            user_id=current_user.user_id,
            action=StarPointAction.BACKGROUND_CHANGE,
            source_type=SourceType.DIARY,
            source_id=str(db_background.id)
        )
        
        # 准备响应数据
        response_data = db_background.to_dict()
        response_data.update({
            "star_awarded": star_result["awarded"],
            "star_points": star_result["points_awarded"],
            "star_message": star_result["message"]
        })
        
        return UserDiaryBackgroundWithStarResponse(**response_data)
        
    except Exception as e:
        # 如果数据库操作失败，删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败：{str(e)}"
        )


@router.delete("/{background_id}")
async def delete_background(
    background_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除指定的背景图片"""
    
    # 查找背景图片记录
    background = db.query(UserDiaryBackground)\
                  .filter(UserDiaryBackground.id == background_id)\
                  .filter(UserDiaryBackground.user_id == current_user.user_id)\
                  .first()
    
    if not background:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="背景图片不存在"
        )
    
    try:
        # 删除图片（图床或本地文件）
        await delete_image_file(background.file_path)
        
        # 删除数据库记录
        db.delete(background)
        db.commit()
        
        return {"message": "背景图片删除成功"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )


@router.post("/restore-default")
async def restore_default_backgrounds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """恢复默认背景（删除所有用户自定义背景）"""
    
    # 获取用户所有背景图片
    backgrounds = db.query(UserDiaryBackground)\
                   .filter(UserDiaryBackground.user_id == current_user.user_id)\
                   .all()
    
    if not backgrounds:
        return {"message": "没有需要删除的背景图片"}
    
    try:
        # 删除所有图片文件和数据库记录
        deleted_count = 0
        for background in backgrounds:
            # 删除图片（图床或本地文件）
            await delete_image_file(background.file_path)
            
            # 删除数据库记录
            db.delete(background)
            deleted_count += 1
        
        db.commit()
        
        return {"message": f"成功删除{deleted_count}张自定义背景图片，已恢复默认背景"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"恢复默认背景失败：{str(e)}"
        )