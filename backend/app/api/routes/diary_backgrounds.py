"""
日记背景图片管理API
"""

import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.diary_background import DiaryBackground

router = APIRouter(prefix="/diary-backgrounds", tags=["日记背景图片"])

# 确保上传目录存在
BACKGROUND_UPLOAD_DIR = os.path.join("uploads", "diary-backgrounds")
if not os.path.exists(BACKGROUND_UPLOAD_DIR):
    os.makedirs(BACKGROUND_UPLOAD_DIR)

# 允许的图片格式
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/webp",
}

# 最大文件大小 (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload_background_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传日记背景图片"""

    # 检查文件类型
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400, detail="只支持JPEG、PNG、GIF、WEBP格式的图片"
        )

    # 检查文件大小
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="图片文件不能超过5MB")

    # 检查用户已上传的背景图片数量
    user_bg_count = (
        db.query(DiaryBackground)
        .filter(
            DiaryBackground.user_id == current_user.user_id,
            DiaryBackground.is_active == True,
        )
        .count()
    )

    if user_bg_count >= 9:
        raise HTTPException(status_code=400, detail="最多只能上传9张背景图片")

    # 生成唯一文件名
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"{current_user.user_id}_{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(BACKGROUND_UPLOAD_DIR, unique_filename)

    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # 保存到数据库
        db_background = DiaryBackground(
            user_id=current_user.user_id,
            filename=unique_filename,
            original_filename=file.filename or "unknown",
            file_path=f"/uploads/diary-backgrounds/{unique_filename}",
            file_size=len(file_content),
            mime_type=file.content_type,
            is_active=True,
        )

        db.add(db_background)
        db.commit()
        db.refresh(db_background)

        return {
            "id": db_background.id,
            "url": db_background.file_path,
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_size": len(file_content),
            "created_at": db_background.created_at,
        }

    except Exception as e:
        # 如果数据库操作失败，删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@router.get("/list")
async def get_user_backgrounds(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """获取用户的背景图片列表"""

    backgrounds = (
        db.query(DiaryBackground)
        .filter(
            DiaryBackground.user_id == current_user.user_id,
            DiaryBackground.is_active == True,
        )
        .order_by(DiaryBackground.created_at.desc())
        .all()
    )

    return [
        {
            "id": bg.id,
            "url": bg.file_path,
            "filename": bg.filename,
            "original_filename": bg.original_filename,
            "file_size": bg.file_size,
            "created_at": bg.created_at,
        }
        for bg in backgrounds
    ]


@router.delete("/{background_id}")
async def delete_background_image(
    background_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除用户的背景图片"""

    # 查找背景图片记录
    background = (
        db.query(DiaryBackground)
        .filter(
            DiaryBackground.id == background_id,
            DiaryBackground.user_id == current_user.user_id,
            DiaryBackground.is_active == True,
        )
        .first()
    )

    if not background:
        raise HTTPException(status_code=404, detail="背景图片不存在")

    try:
        # 删除文件
        full_file_path = os.path.join(BACKGROUND_UPLOAD_DIR, background.filename)
        if os.path.exists(full_file_path):
            os.remove(full_file_path)

        # 标记为删除（软删除）
        background.is_active = False
        db.commit()

        return {"message": "背景图片删除成功"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@router.get("/default")
async def get_default_backgrounds():
    """获取默认背景选项"""
    default_backgrounds = [
        {"id": "default_1", "name": "粉色心情", "color": "#ffafcc", "type": "color"},
        {"id": "default_2", "name": "蓝色忧郁", "color": "#a2d2ff", "type": "color"},
        {"id": "default_3", "name": "温柔时光", "color": "#ffcad4", "type": "color"},
        {"id": "default_4", "name": "紫色梦境", "color": "#cdb4db", "type": "color"},
    ]
    return default_backgrounds


@router.delete("/restore-default")
async def restore_default_backgrounds(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """恢复默认背景（删除所有用户自定义背景）"""

    try:
        # 获取用户所有激活的背景图片
        backgrounds = (
            db.query(DiaryBackground)
            .filter(
                DiaryBackground.user_id == current_user.user_id,
                DiaryBackground.is_active == True,
            )
            .all()
        )

        # 删除所有文件
        for background in backgrounds:
            full_file_path = os.path.join(BACKGROUND_UPLOAD_DIR, background.filename)
            if os.path.exists(full_file_path):
                try:
                    os.remove(full_file_path)
                except Exception as e:
                    print(f"删除文件失败: {full_file_path}, 错误: {e}")

        # 软删除所有记录
        db.query(DiaryBackground).filter(
            DiaryBackground.user_id == current_user.user_id,
            DiaryBackground.is_active == True,
        ).update({"is_active": False})

        db.commit()

        return {"message": "已恢复默认背景", "deleted_count": len(backgrounds)}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"恢复默认背景失败: {str(e)}")
