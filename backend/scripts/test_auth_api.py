#!/usr/bin/env python3
"""
测试带认证的API请求
"""
import requests
import json

def test_with_auth():
    """测试带认证的API请求"""
    
    print("============================================================")
    print("🔐 带认证的API测试")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. 先尝试注册一个新用户
        print("👤 注册新用户...")
        register_data = {
            "username": "test_api_user",
            "password": "test123",
            "email": "test_api@example.com",
            "nickname": "测试API用户"
        }
        
        try:
            register_response = requests.post(f"{base_url}/auth/register", json=register_data)
            print(f"   注册状态码: {register_response.status_code}")
            if register_response.status_code != 200:
                print(f"   注册响应: {register_response.text}")
        except Exception as e:
            print(f"   注册失败: {e}")
        
        # 2. 登录获取token (使用已存在的用户)
        print("\n🔑 用户登录...")
        login_data = {
            "username": "testuser",  # 使用已存在的用户
            "password": "123456"    # 尝试常见密码
        }
        
        try:
            login_response = requests.post(f"{base_url}/auth/login", json=login_data)
            print(f"   登录状态码: {login_response.status_code}")
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                access_token = token_data.get("access_token")
                print(f"   获取到token: {access_token[:20]}...")
                
                # 3. 使用token测试reports-history端点
                print("\n📋 测试报告历史端点（带认证）...")
                headers = {"Authorization": f"Bearer {access_token}"}
                
                url = f"{base_url}/risk-assessment/reports-history?page=1&page_size=10"
                print(f"   请求URL: {url}")
                print(f"   认证头: Authorization: Bearer {access_token[:20]}...")
                
                response = requests.get(url, headers=headers)
                print(f"   状态码: {response.status_code}")
                
                if response.status_code == 500:
                    print(f"   🚨 500错误详情: {response.text}")
                    print(f"   响应头: {dict(response.headers)}")
                elif response.status_code == 200:
                    print(f"   ✅ 成功响应: {response.json()}")
                else:
                    print(f"   其他响应: {response.text}")
                    
                # 4. 测试统计端点
                print("\n📊 测试统计端点（带认证）...")
                stats_response = requests.get(f"{base_url}/risk-assessment/statistics", headers=headers)
                print(f"   统计端点状态码: {stats_response.status_code}")
                
                if stats_response.status_code == 500:
                    print(f"   🚨 统计端点500错误: {stats_response.text}")
                elif stats_response.status_code == 200:
                    print(f"   ✅ 统计端点成功: {stats_response.json()}")
                else:
                    print(f"   统计端点其他响应: {stats_response.text}")
                    
            else:
                print(f"   登录失败: {login_response.text}")
                
        except Exception as e:
            print(f"   登录请求异常: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_auth()
    if success:
        print("\n" + "="*60)
        print("🎉 认证API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
