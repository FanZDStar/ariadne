"""
水滴系统数据库表初始化脚本
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import engine, SessionLocal
from app.models.water_drops import UserWaterDrops
from sqlalchemy import text

def init_water_drops_table():
    """初始化水滴系统表"""
    print("🚀 开始初始化水滴系统表...")
    
    try:
        # 创建表
        UserWaterDrops.__table__.create(engine, checkfirst=True)
        print("✅ user_water_drops 表创建成功")
        
        # 验证表是否存在
        db = SessionLocal()
        try:
            result = db.execute(text("SHOW TABLES LIKE 'user_water_drops'"))
            if result.fetchone():
                print("✅ 验证：user_water_drops 表已存在")
                
                # 显示表结构
                result = db.execute(text("DESCRIBE user_water_drops"))
                print("\n📋 表结构:")
                for row in result:
                    print(f"  - {row}")
            else:
                print("❌ 错误：表创建失败")
        finally:
            db.close()
        
        print("\n✅ 水滴系统表初始化完成！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        raise

if __name__ == "__main__":
    init_water_drops_table()
