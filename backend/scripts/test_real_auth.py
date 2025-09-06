#!/usr/bin/env python3
"""
创建测试用户并测试API
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.utils.password import get_password_hash
import requests

def create_test_user():
    """创建测试用户"""
    
    print("============================================================")
    print("👤 创建测试用户")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == "apitest").first()
        if existing_user:
            print("✅ 测试用户已存在")
            db.close()
            return "apitest", "test123"
        
        # 创建新用户
        test_user = User(
            username="apitest",
            password_hash=get_password_hash("test123"),
            email="apitest@example.com",
            nickname="API测试",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ 测试用户创建成功: {test_user.user_id}")
        
        return "apitest", "test123"
        
    except Exception as e:
        print(f"❌ 创建用户失败: {str(e)}")
        db.rollback()
        return None, None
    finally:
        db.close()

def test_api_with_real_auth():
    """使用真实认证测试API"""
    
    # 1. 创建测试用户
    username, password = create_test_user()
    if not username:
        print("❌ 无法创建测试用户")
        return False
        
    print(f"\n🔑 使用用户 {username} 测试...")
    
    base_url = "http://localhost:8000"
    
    try:
        # 2. 登录获取token
        login_data = {
            "username": username,
            "password": password
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"登录状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 获取到token: {access_token[:20]}...")
            
            # 3. 测试风险评估API
            headers = {"Authorization": f"Bearer {access_token}"}
            
            print("\n📋 测试报告历史端点...")
            url = f"{base_url}/risk-assessment/reports-history?page=1&page_size=10"
            response = requests.get(url, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 500:
                print(f"🚨 500错误详情:")
                print(response.text)
            elif response.status_code == 200:
                reports = response.json()
                print(f"✅ 成功获取 {len(reports)} 个报告")
            else:
                print(f"其他响应: {response.text}")
                
        else:
            print(f"❌ 登录失败: {login_response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_with_real_auth()
    if success:
        print("\n" + "="*60)
        print("🎉 API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
