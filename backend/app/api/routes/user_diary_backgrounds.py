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
from app.schemas.user_diary_backgrounds import UserDiaryBackgroundResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/user-diary-backgrounds", tags=["用户日记背景图片"])

# 允许的图片文件类型和最大文件大小
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_USER_BACKGROUNDS = 4  # 每个用户最多4张背景图片

# 确保上传目录存在
UPLOAD_DIR = "uploads/diary-backgrounds"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)


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


@router.post("/upload", response_model=UserDiaryBackgroundResponse)
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
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # 创建数据库记录
        db_background = UserDiaryBackground(
            user_id=current_user.user_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(file_content),
            upload_time=datetime.now(),
            is_active=True
        )
        
        db.add(db_background)
        db.commit()
        db.refresh(db_background)
        
        return UserDiaryBackgroundResponse(**db_background.to_dict())
        
    except Exception as e:
        # 如果数据库操作失败，删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败：{str(e)}"
        )


@router.delete("/{background_id}")
def delete_background(
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
        # 删除物理文件
        if os.path.exists(background.file_path):
            os.remove(background.file_path)
        
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


@router.delete("/restore-default")
def restore_default_backgrounds(
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
        # 删除所有物理文件和数据库记录
        deleted_count = 0
        for background in backgrounds:
            # 删除物理文件
            if os.path.exists(background.file_path):
                os.remove(background.file_path)
            
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