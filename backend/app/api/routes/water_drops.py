"""
水滴系统API路由
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.water_drops import UserWaterDrops
from app.models.user_watering_cooldown import UserWateringCooldown
from app.models.tree_energy import TreeEnergy

router = APIRouter()


@router.get("/status")
async def get_water_drops_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户水滴状态
    返回：
    - water_drops: 当前水滴数量
    - can_claim: 是否可以领取
    - remaining_seconds: 距离下次领取的剩余秒数
    """
    # 获取或创建用户水滴记录
    water_drops_record = db.query(UserWaterDrops).filter(
        UserWaterDrops.user_id == current_user.user_id
    ).first()
    
    if not water_drops_record:
        water_drops_record = UserWaterDrops(
            user_id=current_user.user_id,
            water_drops=0,
            total_earned=0,
            total_used=0
        )
        db.add(water_drops_record)
        db.commit()
        db.refresh(water_drops_record)
    
    # 获取领取冷却记录
    cooldown_record = db.query(UserWateringCooldown).filter(
        UserWateringCooldown.user_id == current_user.user_id
    ).first()
    
    can_claim = True
    remaining_seconds = 0
    
    if cooldown_record and cooldown_record.last_watering_time:
        # 计算距离上次领取的时间（使用本地时间）
        now = datetime.now()
        time_since_last_claim = now - cooldown_record.last_watering_time
        cooldown_duration = timedelta(hours=1)
        
        if time_since_last_claim < cooldown_duration:
            can_claim = False
            remaining_seconds = int((cooldown_duration - time_since_last_claim).total_seconds())
    
    return {
        "water_drops": water_drops_record.water_drops,
        "total_earned": water_drops_record.total_earned,
        "total_used": water_drops_record.total_used,
        "can_claim": can_claim,
        "remaining_seconds": remaining_seconds,
        "claim_amount": 10  # 每次领取10个水滴
    }


@router.post("/claim")
async def claim_water_drops(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    领取水滴（每小时10个）
    """
    # 获取或创建用户水滴记录
    water_drops_record = db.query(UserWaterDrops).filter(
        UserWaterDrops.user_id == current_user.user_id
    ).first()
    
    if not water_drops_record:
        water_drops_record = UserWaterDrops(
            user_id=current_user.user_id,
            water_drops=0,
            total_earned=0,
            total_used=0
        )
        db.add(water_drops_record)
        db.commit()
        db.refresh(water_drops_record)
    
    # 检查冷却时间
    cooldown_record = db.query(UserWateringCooldown).filter(
        UserWateringCooldown.user_id == current_user.user_id
    ).first()
    
    if cooldown_record and cooldown_record.last_watering_time:
        now = datetime.now()
        time_since_last_claim = now - cooldown_record.last_watering_time
        cooldown_duration = timedelta(hours=1)
        
        if time_since_last_claim < cooldown_duration:
            remaining_seconds = int((cooldown_duration - time_since_last_claim).total_seconds())
            raise HTTPException(
                status_code=400,
                detail=f"冷却中，还需等待 {remaining_seconds} 秒"
            )
    
    # 领取水滴
    claim_amount = 10
    water_drops_record.water_drops += claim_amount
    water_drops_record.total_earned += claim_amount
    
    # 更新或创建冷却记录
    if not cooldown_record:
        cooldown_record = UserWateringCooldown(
            user_id=current_user.user_id,
            last_watering_time=datetime.now()
        )
        db.add(cooldown_record)
    else:
        cooldown_record.last_watering_time = datetime.now()
    
    db.commit()
    db.refresh(water_drops_record)
    
    return {
        "message": f"成功领取 {claim_amount} 个水滴！",
        "water_drops": water_drops_record.water_drops,
        "claimed_amount": claim_amount,
        "can_claim": False,
        "remaining_seconds": 3600  # 1小时后可再次领取
    }


@router.post("/convert-to-energy")
async def convert_water_drops_to_energy(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    将水滴转换为能量（1:1）
    """
    # 获取用户水滴记录
    water_drops_record = db.query(UserWaterDrops).filter(
        UserWaterDrops.user_id == current_user.user_id
    ).first()
    
    if not water_drops_record or water_drops_record.water_drops <= 0:
        raise HTTPException(
            status_code=400,
            detail="水滴不足，无法转换"
        )
    
    # 获取或创建树能量记录
    tree_energy = db.query(TreeEnergy).filter(
        TreeEnergy.user_id == current_user.user_id
    ).first()
    
    if not tree_energy:
        tree_energy = TreeEnergy(
            user_id=current_user.user_id,
            energy=0,
            level=1
        )
        db.add(tree_energy)
        db.commit()
        db.refresh(tree_energy)
    
    # 转换水滴为能量
    drops_to_convert = water_drops_record.water_drops
    water_drops_record.water_drops = 0
    water_drops_record.total_used += drops_to_convert
    
    old_level = tree_energy.level
    tree_energy.energy += drops_to_convert
    
    # 检查是否升级（每100能量升1级，最高30级）
    leveled_up = False
    while tree_energy.energy >= 100 and tree_energy.level < 30:
        tree_energy.energy -= 100
        tree_energy.level += 1
        leveled_up = True
    
    # 如果已达到30级，能量上限为100
    if tree_energy.level >= 30:
        tree_energy.energy = min(tree_energy.energy, 100)
    
    db.commit()
    db.refresh(tree_energy)
    db.refresh(water_drops_record)
    
    message = f"成功转换 {drops_to_convert} 个水滴为能量！"
    if leveled_up:
        message += f" 恭喜升级到 Lv.{tree_energy.level}！"
    
    return {
        "message": message,
        "converted_drops": drops_to_convert,
        "water_drops": water_drops_record.water_drops,
        "energy": tree_energy.energy,
        "level": tree_energy.level,
        "leveled_up": leveled_up,
        "old_level": old_level
    }
