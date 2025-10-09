"""
初始化所有现有用户的星星积分系统
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import sessionmaker
from app.database.session import engine
from app.models.user import User
from app.services.star_point_service import StarPointService

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_user_star_points():
    """初始化所有现有用户的积分记录"""
    db = SessionLocal()
    try:
        service = StarPointService(db)
        
        # 获取所有用户
        users = db.query(User).all()
        
        print(f"找到 {len(users)} 个用户，开始初始化积分记录...")
        
        initialized_count = 0
        skipped_count = 0
        
        for user in users:
            # 检查用户是否已有积分记录
            existing_points = service.get_user_points(user.user_id)
            
            if existing_points:
                print(f"用户 {user.username} (ID: {user.user_id}) 已有积分记录，跳过")
                skipped_count += 1
                continue
            
            # 创建积分记录
            try:
                user_points = service.create_user_points(user.user_id, initial_points=10)
                print(f"✅ 为用户 {user.username} (ID: {user.user_id}) 创建积分记录，初始积分: {user_points.current_points}")
                initialized_count += 1
            except Exception as e:
                print(f"❌ 为用户 {user.username} (ID: {user.user_id}) 创建积分记录失败: {e}")
        
        print(f"\n初始化完成:")
        print(f"  - 新创建: {initialized_count} 个用户积分记录")
        print(f"  - 已跳过: {skipped_count} 个用户（已有记录）")
        print(f"  - 总用户数: {len(users)}")
        
    except Exception as e:
        print(f"初始化过程中发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化用户星星积分系统...")
    initialize_user_star_points()
    print("初始化完成！")
