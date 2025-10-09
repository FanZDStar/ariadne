from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta, date
from app.database.session import get_db
from app.models.user import User
from app.models.emotional_diary import EmotionalDiary
from app.models.diary_image import DiaryImage
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.api.deps import get_current_user
from app.services.privacy_service import privacy_service

router = APIRouter(prefix="/diary", tags=["碎碎念"])

async def delete_diary_image(image_url: str):
    """删除日记图片（图床或本地）"""
    try:
        if image_url.startswith('http'):
            # 图床URL - 暂时跳过删除，因为PICUI API可能不支持删除或需要特殊key格式
            print(f"[删除] ⚠️  跳过图床图片删除（API不支持）: {image_url}")
            # TODO: 如果找到正确的删除API，可以重新启用
            # from app.services.picui_service import picui_service
            # if '/free/' in image_url:
            #     key = image_url.split('/free/')[-1].replace('/', '_')
            #     delete_result = await picui_service.delete_image(key)
            #     if delete_result["success"]:
            #         print(f"[删除] ✅ 日记图床图片删除成功: {image_url}")
            #     else:
            #         print(f"[删除] ⚠️  日记图床图片删除失败: {delete_result.get('message', '未知错误')}")
        else:
            # 本地文件URL，转换为文件路径
            if image_url.startswith('/uploads/'):
                import os
                file_path = image_url[1:]  # 移除开头的 '/'
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[删除] ✅ 日记本地文件删除成功: {file_path}")
                else:
                    print(f"[删除] ⚠️  日记本地文件不存在: {file_path}")
            else:
                print(f"[删除] ⚠️  无法解析日记本地URL格式: {image_url}")
    except Exception as e:
        print(f"[删除] ❌ 删除日记图片失败: {str(e)}")
        # 不抛出异常，避免阻塞数据库删除


# ... (保留原有的创建、获取、更新、删除日记的接口) ...
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建新的碎碎念"""
    # 创建日记，不再使用加密功能
    db_diary = EmotionalDiary(
        user_id=current_user.user_id,
        mood=diary.mood,
        is_private=False,  # 固定为False，不再支持私密日记
        image_count=len(diary.images),
        tags=diary.tags,  # 添加标签支持
    )

    # 已移除加密功能，直接设置原始属性
    db_diary.title = diary.title
    db_diary.content = diary.content

    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)

    # 添加图片
    for i, image_data in enumerate(diary.images):
        db_image = DiaryImage(
            diary_id=db_diary.diary_id, image_url=image_data.image_url, image_order=i
        )
        db.add(db_image)

    db.commit()
    db.refresh(db_diary)

    # 返回原始数据（已移除加密功能）
    result = DiaryResponse(
        diary_id=db_diary.diary_id,
        user_id=db_diary.user_id,
        title=db_diary.title,
        content=db_diary.content,
        mood=db_diary.mood,
        created_at=db_diary.created_at,
        updated_at=db_diary.updated_at,
        is_private=db_diary.is_private,
        image_count=db_diary.image_count,
        tags=db_diary.tags,  # 添加标签支持
        images=[],
    )

    return result


@router.get("/", response_model=List[DiaryResponse])
def get_user_diaries(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取当前用户的所有碎碎念，按时间倒序排列"""
    query = (
        db.query(EmotionalDiary)
        .filter(EmotionalDiary.user_id == current_user.user_id)
        .order_by(EmotionalDiary.created_at.desc())
    )
    if limit is not None:
        query = query.offset(skip).limit(limit)
    else:
        query = query.offset(skip)

    diaries = query.all()

    # 返回解密后的数据
    result = []
    for diary in diaries:
        # 获取该日记的所有图片
        images = (
            db.query(DiaryImage)
            .filter(DiaryImage.diary_id == diary.diary_id)
            .order_by(DiaryImage.image_order)
            .all()
        )
        
        diary_response = DiaryResponse(
            diary_id=diary.diary_id,
            user_id=diary.user_id,
            title=diary.title,
            content=diary.content,
            mood=diary.mood,
            created_at=diary.created_at,
            updated_at=diary.updated_at,
            is_private=diary.is_private,
            image_count=diary.image_count,
            tags=diary.tags,
            images=[{
                "image_id": img.image_id,
                "diary_id": img.diary_id,
                "image_url": img.image_url,
                "image_order": img.image_order,
                "created_at": img.created_at
            } for img in images],
        )
        result.append(diary_response)

    return result


@router.get("/{diary_id}", response_model=DiaryResponse)
def get_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取特定的碎碎念"""
    diary = (
        db.query(EmotionalDiary)
        .filter(EmotionalDiary.diary_id == diary_id)
        .filter(EmotionalDiary.user_id == current_user.user_id)
        .first()
    )

    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="日记不存在")

    # 获取该日记的所有图片
    images = (
        db.query(DiaryImage)
        .filter(DiaryImage.diary_id == diary.diary_id)
        .order_by(DiaryImage.image_order)
        .all()
    )

    # 返回原始数据（已移除加密功能）
    return DiaryResponse(
        diary_id=diary.diary_id,
        user_id=diary.user_id,
        title=diary.title,
        content=diary.content,
        mood=diary.mood,
        created_at=diary.created_at,
        updated_at=diary.updated_at,
        is_private=diary.is_private,
        image_count=diary.image_count,
        tags=diary.tags,
        images=[{
            "image_id": img.image_id,
            "diary_id": img.diary_id,
            "image_url": img.image_url,
            "image_order": img.image_order,
            "created_at": img.created_at
        } for img in images],
    )


@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新碎碎念"""
    db_diary = (
        db.query(EmotionalDiary)
        .filter(EmotionalDiary.diary_id == diary_id)
        .filter(EmotionalDiary.user_id == current_user.user_id)
        .first()
    )

    if not db_diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found"
        )

    update_data = diary_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "images":
            setattr(db_diary, key, value)

    if diary_update.images is not None:
        # 删除旧图片（包括图床上的图片）
        old_images = db.query(DiaryImage).filter(DiaryImage.diary_id == diary_id).all()
        for old_image in old_images:
            await delete_diary_image(old_image.image_url)
        
        # 删除数据库记录
        db.query(DiaryImage).filter(DiaryImage.diary_id == diary_id).delete()
        
        # 添加新图片
        for i, image_data in enumerate(diary_update.images):
            db_image = DiaryImage(
                diary_id=diary_id, image_url=image_data.image_url, image_order=i
            )
            db.add(db_image)
        db_diary.image_count = len(diary_update.images)

    db.commit()
    db.refresh(db_diary)
    return db_diary


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除碎碎念"""
    db_diary = (
        db.query(EmotionalDiary)
        .filter(EmotionalDiary.diary_id == diary_id)
        .filter(EmotionalDiary.user_id == current_user.user_id)
        .first()
    )

    if not db_diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Diary not found"
        )

    # 删除日记相关的图片
    diary_images = db.query(DiaryImage).filter(DiaryImage.diary_id == diary_id).all()
    for image in diary_images:
        await delete_diary_image(image.image_url)
    
    # 手动删除图片记录，避免级联删除冲突
    db.query(DiaryImage).filter(DiaryImage.diary_id == diary_id).delete()
    
    # 删除日记记录
    db.delete(db_diary)
    db.commit()
    return


@router.get("/mood-stats/{period}")
def get_mood_statistics(
    period: str,  # "3days", "7days", "30days", "60days"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取心情统计数据，补全缺失日期的默认值"""
    # 确保查询范围覆盖当天的所有时间
    end_date = datetime.utcnow().replace(hour=23, minute=59, second=59)
    days = 0
    if period == "3days":
        days = 3
    elif period == "7days":
        days = 7
    elif period == "30days":
        days = 30
    elif period == "60days":
        days = 60
    else:
        raise HTTPException(status_code=400, detail="Invalid period")

    # 计算起始日期
    start_date = (end_date - timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0
    )

    mood_score_case = EmotionalDiary.get_mood_score_case()

    stats_query = (
        db.query(
            func.date(EmotionalDiary.created_at).label("date"),
            func.avg(mood_score_case).label("avg_mood"),
        )
        .filter(
            and_(
                EmotionalDiary.user_id == current_user.user_id,
                EmotionalDiary.created_at >= start_date,
                EmotionalDiary.created_at <= end_date,
            )
        )
        .group_by("date")
        .order_by("date")
        .all()
    )

    stats_map = {stat.date: round(float(stat.avg_mood), 2) for stat in stats_query}

    result = []
    current_date = start_date.date()
    end_date_date = end_date.date()

    while current_date <= end_date_date:
        result.append(
            {
                "time": current_date.strftime("%Y-%m-%d"),
                "mood_score": stats_map.get(current_date, 3.0),
            }
        )
        current_date += timedelta(days=1)

    return {"period": period, "data": result}
