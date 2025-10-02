#!/usr/bin/env python3
"""
测试导入问题
"""
import sys
import os

# 添加后端路径到sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# 设置环境变量
os.environ['DATABASE_URL'] = 'mysql+pymysql://root:123456@localhost:3306/ariadne'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['AI_API_URL'] = 'https://test.com'
os.environ['AI_API_KEY'] = 'test-key'
os.environ['AI_MODEL'] = 'test-model'

try:
    print("尝试导入ProtectionDrillService...")
    from app.services.protection_drill_service import ProtectionDrillService
    print("✓ ProtectionDrillService导入成功")
    
    print("尝试导入verify_user...")
    from app.middleware.auth import verify_user
    print("✓ verify_user导入成功")
    
    print("测试服务...")
    service = ProtectionDrillService()
    types = service.get_training_types()
    print(f"✓ 服务工作正常，获取到 {len(types)} 个训练类型")
    
except ImportError as e:
    print(f"✗ 导入错误: {e}")
    print("这解释了为什么API路由使用了空的临时实现")
except Exception as e:
    print(f"✗ 其他错误: {e}")
    import traceback
    traceback.print_exc()
