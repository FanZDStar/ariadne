#!/usr/bin/env python3
"""
模拟前端请求以捕获500错误
"""
import requests
import json
import time

def simulate_frontend_request():
    """模拟前端的确切请求"""
    
    print("============================================================")
    print("🔍 模拟前端请求以捕获500错误")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. 首先尝试用一个存在的用户登录
        print("🔑 使用已知用户登录...")
        
        # 尝试几个可能的用户名和密码组合
        users_to_try = [
            ("testuser", "123456"),
            ("peppa", "123456"),
            ("hello", "123456"),
            ("root", "admin"),
            ("apitest", "test123")
        ]
        
        access_token = None
        for username, password in users_to_try:
            login_data = {
                "username": username,
                "password": password
            }
            
            try:
                login_response = requests.post(f"{base_url}/auth/login", json=login_data)
                if login_response.status_code == 200:
                    token_data = login_response.json()
                    access_token = token_data.get("access_token")
                    print(f"✅ 成功登录用户: {username}")
                    break
                else:
                    print(f"   {username} 登录失败: {login_response.status_code}")
            except Exception as e:
                print(f"   {username} 登录异常: {e}")
        
        if not access_token:
            print("❌ 所有用户登录都失败")
            return False
        
        # 2. 模拟前端的确切请求
        print(f"\n📋 模拟前端请求...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        # 添加OPTIONS请求（前端会先发送）
        print("   发送OPTIONS请求...")
        options_response = requests.options(
            f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
            headers=headers
        )
        print(f"   OPTIONS状态码: {options_response.status_code}")
        
        # 稍微等待
        time.sleep(0.1)
        
        # 发送GET请求
        print("   发送GET请求...")
        get_response = requests.get(
            f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
            headers=headers
        )
        print(f"   GET状态码: {get_response.status_code}")
        
        if get_response.status_code == 500:
            print(f"🚨 500错误详情:")
            print(f"响应头: {dict(get_response.headers)}")
            print(f"响应体: {get_response.text}")
        elif get_response.status_code == 200:
            print(f"✅ 请求成功: {get_response.json()}")
        else:
            print(f"其他状态码 {get_response.status_code}: {get_response.text}")
        
        # 3. 也测试统计端点
        print(f"\n📊 测试统计端点...")
        stats_response = requests.get(
            f"{base_url}/risk-assessment/statistics",
            headers=headers
        )
        print(f"   统计端点状态码: {stats_response.status_code}")
        if stats_response.status_code == 500:
            print(f"   统计端点500错误: {stats_response.text}")
        elif stats_response.status_code == 200:
            print(f"   统计端点成功: {stats_response.json()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simulate_frontend_request()
    if success:
        print("\n" + "="*60)
        print("🎉 前端请求模拟完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
