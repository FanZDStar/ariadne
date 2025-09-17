from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SkillFavoriteCreate(BaseModel):
    skill_id: str
    category: str
    skill_name: str

class SkillFavoriteResponse(BaseModel):
    favorite_id: int
    skill_id: str
    category: str
    skill_name: str
    created_at: str

class FavoriteCheckResponse(BaseModel):
    is_favorited: bool

class FavoritesListResponse(BaseModel):
    favorites: List[SkillFavoriteResponse]
    total: int

@router.post("/add", status_code=status.HTTP_200_OK)
async def add_skill_favorite(
    favorite_data: SkillFavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加技能收藏"""
    try:
        # 检查是否已经收藏
        check_query = text("""
            SELECT favorite_id FROM skill_favorites 
            WHERE user_id = :user_id AND skill_id = :skill_id
        """)
        
        existing = db.execute(check_query, {
            "user_id": current_user.user_id,
            "skill_id": favorite_data.skill_id
        }).fetchone()
        
        if existing:
            return {"message": "已收藏该技能", "status": "already_exists"}
        
        # 添加收藏记录
        insert_query = text("""
            INSERT INTO skill_favorites (user_id, skill_id, category, skill_name, created_at)
            VALUES (:user_id, :skill_id, :category, :skill_name, NOW())
        """)
        
        db.execute(insert_query, {
            "user_id": current_user.user_id,
            "skill_id": favorite_data.skill_id,
            "category": favorite_data.category,
            "skill_name": favorite_data.skill_name
        })
        db.commit()
        
        logger.info(f"用户 {current_user.user_id} 收藏了技能 {favorite_data.skill_id}: {favorite_data.skill_name}")
        
        return {"message": "收藏成功", "status": "success"}
        
    except Exception as e:
        logger.error(f"添加技能收藏失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="添加收藏失败"
        )

@router.post("/remove", status_code=status.HTTP_200_OK)
async def remove_skill_favorite(
    favorite_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """移除技能收藏"""
    try:
        skill_id = favorite_data.get("skill_id")
        if not skill_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="缺少技能ID"
            )
        
        # 删除收藏记录
        delete_query = text("""
            DELETE FROM skill_favorites 
            WHERE user_id = :user_id AND skill_id = :skill_id
        """)
        
        result = db.execute(delete_query, {
            "user_id": current_user.user_id,
            "skill_id": skill_id
        })
        db.commit()
        
        if result.rowcount == 0:
            return {"message": "该技能未被收藏", "status": "not_found"}
        
        logger.info(f"用户 {current_user.user_id} 取消收藏技能 {skill_id}")
        
        return {"message": "取消收藏成功", "status": "success"}
        
    except Exception as e:
        logger.error(f"移除技能收藏失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="取消收藏失败"
        )

@router.get("/check", response_model=FavoriteCheckResponse)
async def check_skill_favorite(
    skill_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查技能是否已收藏"""
    try:
        query = text("""
            SELECT favorite_id FROM skill_favorites 
            WHERE user_id = :user_id AND skill_id = :skill_id
        """)
        
        result = db.execute(query, {
            "user_id": current_user.user_id,
            "skill_id": skill_id
        }).fetchone()
        
        return FavoriteCheckResponse(is_favorited=result is not None)
        
    except Exception as e:
        logger.error(f"检查技能收藏状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="检查收藏状态失败"
        )

@router.get("/list", response_model=FavoritesListResponse)
async def get_skill_favorites(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户收藏的技能列表"""
    try:
        base_query = """
            SELECT favorite_id, skill_id, category, skill_name, created_at
            FROM skill_favorites 
            WHERE user_id = :user_id
        """
        
        params = {"user_id": current_user.user_id}
        
        if category and category != 'all':
            base_query += " AND category = :category"
            params["category"] = category
        
        base_query += " ORDER BY created_at DESC"
        
        query = text(base_query)
        results = db.execute(query, params).fetchall()
        
        favorites = []
        for row in results:
            favorites.append(SkillFavoriteResponse(
                favorite_id=row.favorite_id,
                skill_id=row.skill_id,
                category=row.category,
                skill_name=row.skill_name,
                created_at=row.created_at.isoformat() if row.created_at else ""
            ))
        
        return FavoritesListResponse(
            favorites=favorites,
            total=len(favorites)
        )
        
    except Exception as e:
        logger.error(f"获取技能收藏列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取收藏列表失败"
        )

@router.get("/stats")
async def get_favorite_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取收藏统计信息"""
    try:
        stats_query = text("""
            SELECT 
                category,
                COUNT(*) as count
            FROM skill_favorites 
            WHERE user_id = :user_id
            GROUP BY category
        """)
        
        results = db.execute(stats_query, {"user_id": current_user.user_id}).fetchall()
        
        stats = {}
        total = 0
        for row in results:
            stats[row.category] = row.count
            total += row.count
        
        return {
            "total": total,
            "by_category": stats
        }
        
    except Exception as e:
        logger.error(f"获取收藏统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计信息失败"
        )
