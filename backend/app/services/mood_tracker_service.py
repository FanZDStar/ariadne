from typing import List, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.mood_tracker import MoodTracker
from app.schemas.mood_tracker import MoodTrackerCreate, WeeklyMoodResponse

class MoodTrackerService:
    """心情晴雨表服务"""
    
    @staticmethod
    def create_mood_record(db: Session, user_id: int, mood_data: MoodTrackerCreate) -> dict:
        """创建或更新心情记录"""
        mood_date = mood_data.mood_date or date.today()
        is_first_record = False
        
        # 查找是否已存在记录
        existing_record = db.query(MoodTracker).filter(
            MoodTracker.user_id == user_id,
            MoodTracker.mood_date == mood_date
        ).first()
        
        if existing_record:
            # 更新现有记录
            existing_record.mood_level = mood_data.mood_level
            db.commit()
            db.refresh(existing_record)
            mood_record = existing_record
        else:
            # 创建新记录
            is_first_record = True
            mood_record = MoodTracker(
                user_id=user_id,
                mood_date=mood_date,
                mood_level=mood_data.mood_level
            )
            db.add(mood_record)
            db.commit()
            db.refresh(mood_record)
        
        # 尝试奖励积分（仅在首次记录时）
        star_awarded = False
        star_points = 0
        star_message = ""
        
        if is_first_record:
            try:
                from app.utils.star_point_helpers import award_mood_tracking
                success, message, points = award_mood_tracking(db, user_id, str(mood_record.id))
                
                if success:
                    star_awarded = True
                    star_points = points
                    star_message = "心情记录成功，获得星星奖励 ⭐"
                    print(f"用户 {user_id} 心情记录获得 {points} 个星星")
                else:
                    print(f"用户 {user_id} 今日已获得心情记录积分: {message}")
            except Exception as e:
                print(f"心情记录积分奖励失败: {e}")
        
        return {
            "mood_record": mood_record,
            "star_awarded": star_awarded,
            "star_points": star_points,
            "star_message": star_message or "心情记录成功 💫"
        }
    
    @staticmethod
    def get_weekly_mood_data(db: Session, user_id: int) -> WeeklyMoodResponse:
        """获取最近7天的心情数据"""
        today = date.today()
        start_date = today - timedelta(days=6)  # 包括今天在内的7天
        
        # 获取数据库中的记录
        records = db.query(MoodTracker).filter(
            MoodTracker.user_id == user_id,
            MoodTracker.mood_date >= start_date,
            MoodTracker.mood_date <= today
        ).order_by(MoodTracker.mood_date).all()
        
        # 创建日期到心情档位的映射
        record_dict = {record.mood_date: record.mood_level for record in records}
        
        # 生成7天的数据
        dates = []
        levels = []
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            dates.append(current_date.strftime("%m/%d"))
            levels.append(record_dict.get(current_date))
        
        return WeeklyMoodResponse(dates=dates, levels=levels)
