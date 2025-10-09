"""
测试心情记录积分奖励功能
"""
import sys
import os
from datetime import date

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import sessionmaker
from app.database.session import engine
from app.models.user import User
from app.services.mood_tracker_service import MoodTrackerService
from app.schemas.mood_tracker import MoodTrackerCreate

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_mood_tracking_reward():
    """测试心情记录奖励功能"""
    db = SessionLocal()
    try:
        # 获取第一个用户进行测试
        user = db.query(User).first()
        if not user:
            print("❌ 没有找到测试用户")
            return
            
        print(f"🧪 测试用户: {user.username} (ID: {user.user_id})")
        
        # 测试心情记录
        mood_data = MoodTrackerCreate(mood_level=4, mood_date=date.today())
        
        print("\n🎯 测试心情记录积分奖励...")
        result = MoodTrackerService.create_mood_record(db, user.user_id, mood_data)
        
        print(f"📝 心情记录ID: {result['mood_record'].id}")
        print(f"😊 心情等级: {result['mood_record'].mood_level}")
        print(f"📅 记录日期: {result['mood_record'].mood_date}")
        print(f"✨ 奖励结果: {result['star_awarded']}")
        print(f"⭐ 获得积分: {result['star_points']}")
        print(f"💬 消息: {result['star_message']}")
        
        # 测试重复记录（更新现有记录）
        print("\n🔄 测试重复心情记录...")
        mood_data2 = MoodTrackerCreate(mood_level=5, mood_date=date.today())
        result2 = MoodTrackerService.create_mood_record(db, user.user_id, mood_data2)
        
        print(f"📝 更新记录ID: {result2['mood_record'].id}")
        print(f"😊 新心情等级: {result2['mood_record'].mood_level}")
        print(f"✨ 奖励结果: {result2['star_awarded']}")
        print(f"⭐ 获得积分: {result2['star_points']}")
        print(f"💬 消息: {result2['star_message']}")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始测试心情记录积分奖励功能...")
    test_mood_tracking_reward()
    print("✅ 测试完成！")
