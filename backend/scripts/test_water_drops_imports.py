""
测试水滴系统的所有导入是否正确
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_imports():
    """测试所有必要的导入"""
    print("🧪 开始测试导入...")
    
    try:
        print("\n1️⃣ 测试 UserWaterDrops 模型...")
        from app.models.water_drops import UserWaterDrops
        print("   ✅ UserWaterDrops 导入成功")
        
        print("\n2️⃣ 测试 TreeEnergy 模型...")
        from app.models.tree_energy import TreeEnergy
        print("   ✅ TreeEnergy 导入成功")
        
        print("\n3️⃣ 测试 UserWateringCooldown 模型...")
        from app.models.user_watering_cooldown import UserWateringCooldown
        print("   ✅ UserWateringCooldown 导入成功")
        
        print("\n4️⃣ 测试 water_drops 路由...")
        from app.api.routes import water_drops
        print("   ✅ water_drops 路由导入成功")
        
        print("\n5️⃣ 测试 API router...")
        from app.api import api_router
        print("   ✅ api_router 导入成功")
        
        print("\n✅ 所有导入测试通过！")
        print("\n📋 模型信息:")
        print(f"   - UserWaterDrops 表名: {UserWaterDrops.__tablename__}")
        print(f"   - TreeEnergy 表名: {TreeEnergy.__tablename__}")
        print(f"   - UserWateringCooldown 表名: {UserWateringCooldown.__tablename__}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
