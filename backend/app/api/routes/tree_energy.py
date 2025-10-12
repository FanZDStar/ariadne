"""
树洞能量系统API
用户可以通过浇水获得能量，升级解锁不同背景
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.models import User
from app.core.database import get_db_connection
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# 浇水冷却时间（分钟）
WATERING_COOLDOWN_MINUTES = 20


def get_or_create_tree_energy(user_id: int):
    """获取或创建用户树洞能量记录"""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # 查询用户能量记录
            cursor.execute(
                "SELECT energy, level FROM user_tree_energy WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                return result['energy'], result['level']
            
            # 如果没有记录，创建初始记录
            cursor.execute(
                "INSERT INTO user_tree_energy (user_id, energy, level) VALUES (%s, 0, 1)",
                (user_id,)
            )
            conn.commit()
            return 0, 1
            
        except Exception as e:
            logger.error(f"获取或创建能量记录失败: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()


def get_watering_cooldown_info(user_id: int):
    """获取浇水冷却信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # 查询最后浇水时间
            cursor.execute(
                "SELECT last_watering_time FROM user_watering_cooldown WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                # 没有记录，说明从未浇水，可以浇水
                return {
                    "can_water": True,
                    "remaining_seconds": 0,
                    "next_watering_time": None
                }
            
            last_watering_time = result['last_watering_time']
            now = datetime.now()
            
            # 计算下次可以浇水的时间
            next_watering_time = last_watering_time + timedelta(minutes=WATERING_COOLDOWN_MINUTES)
            
            if now >= next_watering_time:
                # 冷却时间已过，可以浇水
                return {
                    "can_water": True,
                    "remaining_seconds": 0,
                    "next_watering_time": None
                }
            else:
                # 还在冷却中
                remaining_seconds = int((next_watering_time - now).total_seconds())
                return {
                    "can_water": False,
                    "remaining_seconds": remaining_seconds,
                    "next_watering_time": next_watering_time.isoformat()
                }
                
        except Exception as e:
            logger.error(f"获取冷却信息失败: {e}")
            raise
        finally:
            cursor.close()


def update_watering_time(user_id: int):
    """更新用户最后浇水时间"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            now = datetime.now()
            # 使用 INSERT ... ON DUPLICATE KEY UPDATE 来插入或更新
            cursor.execute(
                """
                INSERT INTO user_watering_cooldown (user_id, last_watering_time)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE last_watering_time = %s
                """,
                (user_id, now, now)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"更新浇水时间失败: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()


@router.get("/tree-energy/status")
def get_tree_energy_status(current_user: User = Depends(get_current_user)):
    """获取当前用户的树洞能量和等级，以及浇水冷却状态"""
    try:
        energy, level = get_or_create_tree_energy(current_user.user_id)
        cooldown_info = get_watering_cooldown_info(current_user.user_id)
        
        return {
            "energy": energy,
            "level": level,
            "energy_to_next_level": 100 - (energy % 100),
            "can_water": cooldown_info["can_water"],
            "remaining_seconds": cooldown_info["remaining_seconds"],
            "next_watering_time": cooldown_info["next_watering_time"]
        }
    except Exception as e:
        logger.error(f"获取能量状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取能量状态失败"
        )


@router.post("/tree-energy/water")
def water_tree(current_user: User = Depends(get_current_user)):
    """浇水增加能量，满100升级，每20分钟可浇水一次"""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # 检查冷却时间
            cooldown_info = get_watering_cooldown_info(current_user.user_id)
            if not cooldown_info["can_water"]:
                remaining_minutes = cooldown_info["remaining_seconds"] // 60
                remaining_seconds = cooldown_info["remaining_seconds"] % 60
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"浇水冷却中，还需等待 {remaining_minutes}分{remaining_seconds}秒"
                )
            
            # 获取当前能量和等级
            energy, level = get_or_create_tree_energy(current_user.user_id)
            
            # 检查是否已达到最大等级
            if level >= 30:
                return {
                    "energy": energy,
                    "level": level,
                    "leveled_up": False,
                    "message": "已达到最高等级！"
                }
            
            # 增加能量
            energy += 20
            leveled_up = False
            level_up_count = 0
            
            # 检查是否升级（满100能量升1级）
            while energy >= 100 and level < 30:
                level += 1
                energy -= 100
                leveled_up = True
                level_up_count += 1
            
            # 更新能量数据库
            cursor.execute(
                "UPDATE user_tree_energy SET energy = %s, level = %s WHERE user_id = %s",
                (energy, level, current_user.user_id)
            )
            conn.commit()
            
            # 更新浇水时间
            update_watering_time(current_user.user_id)
            
            message = "浇水成功！"
            if leveled_up:
                message = f"恭喜升级！当前等级：{level}"
                if level == 10:
                    message += "🎉 解锁新背景 sun2/moon2！"
                elif level == 20:
                    message += "🎉 解锁最高级背景 sun3/moon3！"
            
            return {
                "energy": energy,
                "level": level,
                "leveled_up": leveled_up,
                "level_up_count": level_up_count,
                "message": message,
                "energy_to_next_level": 100 - energy if level < 30 else 0,
                "can_water": False,
                "remaining_seconds": WATERING_COOLDOWN_MINUTES * 60
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"浇水失败: {e}")
            conn.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="浇水失败"
            )
        finally:
            cursor.close()
