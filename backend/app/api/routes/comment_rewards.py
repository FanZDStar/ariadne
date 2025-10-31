"""
每日评论奖励相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.daily_comment_reward import DailyCommentReward
from app.models.water_drops import UserWaterDrops
from pydantic import BaseModel

router = APIRouter()


class CommentRewardResponse(BaseModel):
    """评论奖励响应"""
    success: bool
    message: str
    water_drops_earned: int
    total_comments_today: int
    remaining_rewards_today: int
    current_water_drops: int


@router.post("/reward-comment", response_model=CommentRewardResponse)
async def reward_for_comment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    评论奖励接口
    每次评论可获得3个水滴，每天最多可获得4次奖励
    """
    try:
        today = date.today()
        
        print(f"🔍 评论奖励请求 - 用户ID: {current_user.user_id}, 今日日期: {today}")
        
        # 查询今日评论奖励记录
        daily_reward = db.query(DailyCommentReward).filter(
            and_(
                DailyCommentReward.user_id == current_user.user_id,
                DailyCommentReward.comment_date == today
            )
        ).first()
        
        if daily_reward:
            print(f"📊 找到今日记录 - 日期: {daily_reward.comment_date}, 已评论次数: {daily_reward.comment_count}")
        else:
            print(f"📊 未找到今日记录，将创建新记录")
        
        # 检查今日是否已达到奖励上限
        if daily_reward and daily_reward.comment_count >= 4:
            # 查询当前水滴数
            user_drops = db.query(UserWaterDrops).filter(
                UserWaterDrops.user_id == current_user.user_id
            ).first()
            
            return CommentRewardResponse(
                success=False,
                message="今日评论奖励已达上限（4次）",
                water_drops_earned=0,
                total_comments_today=daily_reward.comment_count,
                remaining_rewards_today=0,
                current_water_drops=user_drops.water_drops if user_drops else 0
            )
        
        # 如果没有今日记录，创建新记录
        if not daily_reward:
            print(f"✨ 创建新的每日奖励记录")
            daily_reward = DailyCommentReward(
                user_id=current_user.user_id,
                comment_date=today,
                comment_count=0,
                comment_rewards_earned=0,
                whisper_count=0,
                whisper_rewards_earned=0
            )
            db.add(daily_reward)
            db.flush()  # 先刷新以获取ID
            print(f"✅ 新记录已创建 - ID: {daily_reward.id}")
        
        # 增加评论次数和奖励
        REWARD_PER_COMMENT = 3
        daily_reward.comment_count += 1
        daily_reward.comment_rewards_earned += REWARD_PER_COMMENT
        
        print(f"💧 发放奖励 - 评论次数: {daily_reward.comment_count}, 本次奖励: {REWARD_PER_COMMENT}")
        
        # 更新用户水滴数
        user_drops = db.query(UserWaterDrops).filter(
            UserWaterDrops.user_id == current_user.user_id
        ).first()
        
        if not user_drops:
            # 如果用户没有水滴记录，创建新记录
            user_drops = UserWaterDrops(
                user_id=current_user.user_id,
                water_drops=REWARD_PER_COMMENT,
                total_earned=REWARD_PER_COMMENT,
                total_used=0
            )
            db.add(user_drops)
        else:
            # 增加水滴数
            user_drops.water_drops += REWARD_PER_COMMENT
            user_drops.total_earned += REWARD_PER_COMMENT
        
        db.commit()
        db.refresh(daily_reward)
        db.refresh(user_drops)
        
        return CommentRewardResponse(
            success=True,
            message=f"评论成功！获得{REWARD_PER_COMMENT}个水滴",
            water_drops_earned=REWARD_PER_COMMENT,
            total_comments_today=daily_reward.comment_count,
            remaining_rewards_today=4 - daily_reward.comment_count,
            current_water_drops=user_drops.water_drops
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"奖励发放失败: {str(e)}")


@router.get("/comment-status")
async def get_comment_reward_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查询今日评论奖励状态
    """
    try:
        today = date.today()
        
        # 查询今日评论奖励记录
        daily_reward = db.query(DailyCommentReward).filter(
            and_(
                DailyCommentReward.user_id == current_user.user_id,
                DailyCommentReward.comment_date == today
            )
        ).first()
        
        if not daily_reward:
            return {
                "total_comments_today": 0,
                "rewards_earned_today": 0,
                "remaining_rewards_today": 4
            }
        
        return {
            "total_comments_today": daily_reward.comment_count,
            "rewards_earned_today": daily_reward.comment_rewards_earned,
            "remaining_rewards_today": max(0, 4 - daily_reward.comment_count)
        }
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.post("/reward-whisper")
async def reward_for_whisper(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    发布悄悄话奖励接口
    每次发布可获得3个水滴，每天最多可获得4次奖励
    """
    try:
        today = date.today()
        
        print(f"🔍 发布悄悄话奖励请求 - 用户ID: {current_user.user_id}, 今日日期: {today}")
        
        # 查询今日奖励记录
        daily_reward = db.query(DailyCommentReward).filter(
            and_(
                DailyCommentReward.user_id == current_user.user_id,
                DailyCommentReward.comment_date == today
            )
        ).first()
        
        if daily_reward:
            print(f"📊 找到今日记录 - 已发布次数: {daily_reward.whisper_count}")
        else:
            print(f"📊 未找到今日记录，将创建新记录")
        
        # 检查今日是否已达到奖励上限
        if daily_reward and daily_reward.whisper_count >= 4:
            # 查询当前水滴数
            user_drops = db.query(UserWaterDrops).filter(
                UserWaterDrops.user_id == current_user.user_id
            ).first()
            
            return {
                "success": False,
                "message": "今日发布奖励已达上限（4次）",
                "water_drops_earned": 0,
                "total_whispers_today": daily_reward.whisper_count,
                "remaining_rewards_today": 0,
                "current_water_drops": user_drops.water_drops if user_drops else 0
            }
        
        # 如果没有今日记录，创建新记录
        if not daily_reward:
            print(f"✨ 创建新的每日奖励记录")
            daily_reward = DailyCommentReward(
                user_id=current_user.user_id,
                comment_date=today,
                comment_count=0,
                comment_rewards_earned=0,
                whisper_count=0,
                whisper_rewards_earned=0
            )
            db.add(daily_reward)
            db.flush()
            print(f"✅ 新记录已创建 - ID: {daily_reward.id}")
        
        # 增加发布次数和奖励
        REWARD_PER_WHISPER = 3
        daily_reward.whisper_count += 1
        daily_reward.whisper_rewards_earned += REWARD_PER_WHISPER
        
        print(f"💧 发放奖励 - 发布次数: {daily_reward.whisper_count}, 本次奖励: {REWARD_PER_WHISPER}")
        
        # 更新用户水滴数
        user_drops = db.query(UserWaterDrops).filter(
            UserWaterDrops.user_id == current_user.user_id
        ).first()
        
        if not user_drops:
            # 如果用户没有水滴记录，创建新记录
            user_drops = UserWaterDrops(
                user_id=current_user.user_id,
                water_drops=REWARD_PER_WHISPER,
                total_earned=REWARD_PER_WHISPER,
                total_used=0
            )
            db.add(user_drops)
        else:
            # 增加水滴数
            user_drops.water_drops += REWARD_PER_WHISPER
            user_drops.total_earned += REWARD_PER_WHISPER
        
        db.commit()
        db.refresh(daily_reward)
        db.refresh(user_drops)
        
        return {
            "success": True,
            "message": f"发布成功！获得{REWARD_PER_WHISPER}个水滴",
            "water_drops_earned": REWARD_PER_WHISPER,
            "total_whispers_today": daily_reward.whisper_count,
            "remaining_rewards_today": 4 - daily_reward.whisper_count,
            "current_water_drops": user_drops.water_drops
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"奖励发放失败: {str(e)}")


@router.get("/debug/all-records")
async def debug_all_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    调试接口：查看当前用户的所有评论奖励记录
    """
    records = db.query(DailyCommentReward).filter(
        DailyCommentReward.user_id == current_user.user_id
    ).order_by(DailyCommentReward.comment_date.desc()).all()
    
    today = date.today()
    
    return {
        "current_date": str(today),
        "total_records": len(records),
        "records": [
            {
                "id": r.id,
                "comment_date": str(r.comment_date),
                "is_today": r.comment_date == today,
                "comment_count": r.comment_count,
                "comment_rewards_earned": r.comment_rewards_earned,
                "whisper_count": r.whisper_count,
                "whisper_rewards_earned": r.whisper_rewards_earned,
                "created_at": str(r.created_at) if hasattr(r, 'created_at') else None,
            }
            for r in records
        ]
    }
