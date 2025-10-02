#!/usr/bin/env python3
"""
测试防护训练服务
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

from app.services.protection_drill_service import ProtectionDrillService
import json

def test_protection_service():
    """测试防护训练服务"""
    print("测试防护训练服务...")
    
    try:
        # 测试获取训练类型
        service = ProtectionDrillService()
        training_types = service.get_training_types()
        
        print(f"✓ 获取到 {len(training_types)} 个训练类型")
        
        if training_types:
            print("第一个训练类型:")
            print(json.dumps(training_types[0], ensure_ascii=False, indent=2))
            
            # 测试获取训练题目
            first_type_id = training_types[0]['id']
            questions = service.get_training_questions(first_type_id, 3)
            print(f"✓ 获取到 {len(questions)} 个训练题目")
            
            if questions:
                print("第一个题目:")
                print(json.dumps(questions[0], ensure_ascii=False, indent=2))
        else:
            print("✗ 没有获取到训练类型")
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_protection_service()
