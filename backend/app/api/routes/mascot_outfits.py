"""
看板娘服装相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.mascot import MascotOutfitResponse, UserCurrentOutfitResponse, SetCurrentOutfitRequest
from sqlalchemy import text

router = APIRouter(prefix="/mascot-outfits", tags=["看板娘服装"])


@router.get("/", response_model=List[MascotOutfitResponse])
def get_all_outfits(db: Session = Depends(get_db)):
    """获取所有可用的看板娘服装"""
    query = text("""
        SELECT id, name, description, preview_image, mascot_image, 
               star_cost, is_default, is_active, sort_order
        FROM mascot_outfits 
        WHERE is_active = 1 
        ORDER BY sort_order ASC, id ASC
    """)
    
    result = db.execute(query)
    outfits = []
    
    for row in result:
        outfits.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "preview_image": row[3],
            "mascot_image": row[4],
            "star_cost": row[5],
            "is_default": bool(row[6]),
            "is_active": bool(row[7]),
            "sort_order": row[8]
        })
    
    return outfits


@router.get("/user-outfits", response_model=List[MascotOutfitResponse])
def get_user_outfits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户拥有的看板娘服装"""
    query = text("""
        SELECT mo.id, mo.name, mo.description, mo.preview_image, mo.mascot_image, 
               mo.star_cost, mo.is_default, mo.is_active, mo.sort_order,
               umo.is_equipped, umo.purchased_at
        FROM mascot_outfits mo
        INNER JOIN user_mascot_outfits umo ON mo.id = umo.outfit_id
        WHERE umo.user_id = :user_id AND mo.is_active = 1
        ORDER BY mo.sort_order ASC, mo.id ASC
    """)
    
    result = db.execute(query, {"user_id": current_user.user_id})
    outfits = []
    
    for row in result:
        outfits.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "preview_image": row[3],
            "mascot_image": row[4],
            "star_cost": row[5],
            "is_default": bool(row[6]),
            "is_active": bool(row[7]),
            "sort_order": row[8],
            "is_equipped": bool(row[9]) if row[9] is not None else False,
            "purchased_at": row[10]
        })
    
    return outfits


@router.get("/current", response_model=UserCurrentOutfitResponse)
def get_current_outfit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户当前选择的看板娘服装"""
    query = text("""
        SELECT mo.id, mo.name, mo.description, mo.preview_image, mo.mascot_image, 
               mo.star_cost, mo.is_default, mo.is_active, mo.sort_order
        FROM mascot_outfits mo
        INNER JOIN user_mascot_outfits umo ON mo.id = umo.outfit_id
        WHERE umo.user_id = :user_id AND umo.is_equipped = 1
        LIMIT 1
    """)
    
    result = db.execute(query, {"user_id": current_user.user_id})
    row = result.fetchone()
    
    if not row:
        # 如果用户没有当前服装，返回默认服装并设置为当前
        default_query = text("""
            SELECT id, name, description, preview_image, mascot_image, 
                   star_cost, is_default, is_active, sort_order
            FROM mascot_outfits 
            WHERE is_default = 1 
            LIMIT 1
        """)
        
        default_result = db.execute(default_query)
        default_row = default_result.fetchone()
        
        if not default_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No default outfit found"
            )
        
        # 为用户添加默认服装记录
        insert_query = text("""
            INSERT IGNORE INTO user_mascot_outfits (user_id, outfit_id, is_equipped, purchased_at)
            VALUES (:user_id, :outfit_id, 1, NOW())
        """)
        
        db.execute(insert_query, {
            "user_id": current_user.user_id,
            "outfit_id": default_row[0]
        })
        db.commit()
        
        row = default_row
    
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "preview_image": row[3],
        "mascot_image": row[4],
        "star_cost": row[5],
        "is_default": bool(row[6]),
        "is_active": bool(row[7]),
        "sort_order": row[8]
    }


@router.post("/set-current")
def set_current_outfit(
    request: SetCurrentOutfitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """设置用户当前的看板娘服装"""
    
    # 检查用户是否拥有该服装
    check_query = text("""
        SELECT COUNT(*) FROM user_mascot_outfits 
        WHERE user_id = :user_id AND outfit_id = :outfit_id
    """)
    
    result = db.execute(check_query, {
        "user_id": current_user.user_id,
        "outfit_id": request.outfit_id
    })
    
    if result.scalar() == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not own this outfit"
        )
    
    # 取消当前装备的服装
    unequip_query = text("""
        UPDATE user_mascot_outfits 
        SET is_equipped = 0 
        WHERE user_id = :user_id AND is_equipped = 1
    """)
    
    db.execute(unequip_query, {"user_id": current_user.user_id})
    
    # 设置新的当前服装
    equip_query = text("""
        UPDATE user_mascot_outfits 
        SET is_equipped = 1 
        WHERE user_id = :user_id AND outfit_id = :outfit_id
    """)
    
    db.execute(equip_query, {
        "user_id": current_user.user_id,
        "outfit_id": request.outfit_id
    })
    
    db.commit()
    
    return {"message": "Current outfit updated successfully"}


@router.post("/purchase/{outfit_id}")
def purchase_outfit(
    outfit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """购买看板娘服装"""
    
    # 检查服装是否存在且可购买
    outfit_query = text("""
        SELECT id, name, star_cost, is_default 
        FROM mascot_outfits 
        WHERE id = :outfit_id AND is_active = 1
    """)
    
    result = db.execute(outfit_query, {"outfit_id": outfit_id})
    outfit_row = result.fetchone()
    
    if not outfit_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outfit not found"
        )
    
    # 检查用户是否已经拥有该服装
    owned_query = text("""
        SELECT COUNT(*) FROM user_mascot_outfits 
        WHERE user_id = :user_id AND outfit_id = :outfit_id
    """)
    
    result = db.execute(owned_query, {
        "user_id": current_user.user_id,
        "outfit_id": outfit_id
    })
    
    if result.scalar() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already owns this outfit"
        )
    
    outfit_name = outfit_row[1]
    star_cost = outfit_row[2]
    is_default = outfit_row[3]
    
    # 如果是免费服装或默认服装，直接添加
    if star_cost == 0 or is_default:
        purchase_query = text("""
            INSERT INTO user_mascot_outfits (user_id, outfit_id, is_equipped, purchased_at)
            VALUES (:user_id, :outfit_id, 0, NOW())
        """)
        
        db.execute(purchase_query, {
            "user_id": current_user.user_id,
            "outfit_id": outfit_id
        })
        db.commit()
        
        return {"message": f"Successfully obtained {outfit_name}"}
    
    # 检查用户星星积分是否足够
    points_query = text("""
        SELECT current_points FROM user_star_points 
        WHERE user_id = :user_id
    """)
    
    points_result = db.execute(points_query, {"user_id": current_user.user_id})
    points_row = points_result.fetchone()
    
    if not points_row:
        # 如果用户没有积分记录，创建一个初始记录
        create_points_query = text("""
            INSERT INTO user_star_points (user_id, current_points, total_earned, total_spent, updated_at)
            VALUES (:user_id, 0, 0, 0, NOW())
        """)
        db.execute(create_points_query, {"user_id": current_user.user_id})
        current_points = 0
    else:
        current_points = points_row[0]
    
    # 检查积分是否足够
    if current_points < star_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient star points. Required: {star_cost}, Available: {current_points}"
        )
    
    # 开始事务：扣除积分并添加服装
    try:
        # 扣除星星积分
        if star_cost > 0:
            update_points_query = text("""
                UPDATE user_star_points 
                SET current_points = current_points - :cost,
                    total_spent = total_spent + :cost,
                    updated_at = NOW()
                WHERE user_id = :user_id
            """)
            
            db.execute(update_points_query, {
                "user_id": current_user.user_id,
                "cost": star_cost
            })
            
            # 记录积分交易
            transaction_query = text("""
                INSERT INTO star_point_logs (user_id, action_type, points_change, description, source_type, created_at)
                VALUES (:user_id, :action_type, :points_change, :description, :source_type, NOW())
            """)
            
            db.execute(transaction_query, {
                "user_id": current_user.user_id,
                "action_type": "purchase",
                "points_change": -star_cost,
                "description": f"Purchase outfit: {outfit_name}",
                "source_type": "mascot_outfit"
            })
        
        # 添加服装到用户库存
        purchase_query = text("""
            INSERT INTO user_mascot_outfits (user_id, outfit_id, is_equipped, purchased_at)
            VALUES (:user_id, :outfit_id, 0, NOW())
        """)
        
        db.execute(purchase_query, {
            "user_id": current_user.user_id,
            "outfit_id": outfit_id
        })
        
        # 获取更新后的积分
        updated_points_query = text("""
            SELECT current_points FROM user_star_points 
            WHERE user_id = :user_id
        """)
        
        updated_result = db.execute(updated_points_query, {"user_id": current_user.user_id})
        updated_points = updated_result.fetchone()[0]
        
        # 奖励购买服装好感度
        affection_awarded = False
        affection_points = 0
        affection_message = ""
        affection_level_up = False
        
        try:
            from app.services.mascot_affection_service import MascotAffectionService
            
            affection_service = MascotAffectionService(db)
            result = affection_service.award_outfit_purchase_affection(
                user_id=current_user.user_id,
                star_cost=star_cost,
                source_id=str(outfit_id)
            )
            
            if result.rewarded:
                affection_awarded = True
                affection_points = result.affection_awarded
                affection_message = f"看板娘好感度 +{result.affection_awarded}"
                affection_level_up = result.level_up
                
                if result.level_up:
                    affection_message += f"，恭喜升级到{result.new_level}级！"
                    
        except Exception as e:
            # 好感度奖励失败不影响购买
            print(f"购买服装好感度奖励失败: {e}")
        
        db.commit()
        
        return {
            "message": f"Successfully purchased {outfit_name}",
            "outfit_id": outfit_id,
            "outfit_name": outfit_name,
            "cost": star_cost,
            "remaining_points": updated_points,
            "affection_awarded": affection_awarded,
            "affection_points": affection_points,
            "affection_message": affection_message,
            "affection_level_up": affection_level_up
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete purchase"
        )
