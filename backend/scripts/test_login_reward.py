"""
测试积分系统登录奖励功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import sessionmaker
from app.database.session import engine
from app.models.user import User
from app.services.star_point_service import StarPointService
from app.utils.star_point_types import StarPointAction, SourceType

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_login_reward():
    """测试登录奖励功能"""
    db = SessionLocal()
    try:
        service = StarPointService(db)
        
        # 获取第一个用户进行测试
        user = db.query(User).first()
        if not user:
            print("❌ 没有找到测试用户")
            return
            
        print(f"🧪 测试用户: {user.username} (ID: {user.user_id})")
        
        # 获取当前积分
        user_points = service.get_or_create_user_points(user.user_id)
        print(f"📊 当前积分: {user_points.current_points}")
        
        # 测试第一次登录奖励
        print("\n🎯 测试每日登录奖励...")
        success, message, points = service.award_points(
            user_id=user.user_id,
            action=StarPointAction.DAILY_LOGIN,
            source_type=SourceType.LOGIN
        )
        
        print(f"✨ 奖励结果: {success}")
        print(f"📝 消息: {message}")
        print(f"⭐ 获得积分: {points}")
        
        # 刷新积分信息
        db.refresh(user_points)
        print(f"📊 更新后积分: {user_points.current_points}")
        
        # 测试第二次登录（应该失败）
        print("\n🔄 测试重复登录奖励...")
        success2, message2, points2 = service.award_points(
            user_id=user.user_id,
            action=StarPointAction.DAILY_LOGIN,
            source_type=SourceType.LOGIN
        )
        
        print(f"✨ 奖励结果: {success2}")
        print(f"📝 消息: {message2}")
        print(f"⭐ 获得积分: {points2}")
        
        # 查看积分日志
        print("\n📋 最近的积分日志:")
        logs = service.get_point_logs(user.user_id, limit=5)
        for log in logs:
            print(f"  - {log.created_at.strftime('%Y-%m-%d %H:%M:%S')}: {log.description} ({log.points_change:+d})")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始测试积分系统登录奖励功能...")
    test_login_reward()
    print("✅ 测试完成！")
