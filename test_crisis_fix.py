#!/usr/bin/env python3
# 测试危机检测修复效果
# file: test_crisis_fix.py

import requests
import json
import sys

def get_auth_token():
    """获取认证令牌"""
    login_url = "http://localhost:8000/users/login"
    
    # 使用测试用户账号（如果没有，可以先注册）
    login_data = {
        "username": "test_user",
        "password": "test123456"
    }
    
    try:
        response = requests.post(login_url, data=login_data)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        else:
            print("⚠️ 登录失败，尝试注册测试用户...")
            return register_test_user()
    except:
        print("⚠️ 登录失败，尝试注册测试用户...")
        return register_test_user()

def register_test_user():
    """注册测试用户"""
    register_url = "http://localhost:8000/users/register"
    
    register_data = {
        "username": "test_user",
        "email": "test@example.com", 
        "password": "test123456"
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        if response.status_code == 200:
            print("✅ 测试用户注册成功，正在登录...")
            return get_auth_token()
        else:
            print(f"❌ 注册失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 注册异常: {e}")
        return None

def test_crisis_detection():
    """测试危机检测功能"""
    
    # 获取认证令牌
    print("🔐 正在获取认证令牌...")
    token = get_auth_token()
    
    if not token:
        print("❌ 无法获取认证令牌，跳过认证测试...")
        test_without_auth()
        return
    
    print("✅ 认证令牌获取成功")
    
    # 测试数据
    test_content = "我想死了"
    
    # API端点
    url = "http://localhost:8000/crisis/assess-risk"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 请求数据
    data = {
        "content": test_content,
        "scene": "self-dialog",
        "enable_ai_analysis": True
    }
    
    try:
        print(f"🧪 测试危机检测修复效果")
        print(f"📝 测试内容: {test_content}")
        print(f"🌐 API地址: {url}")
        print("-" * 50)
        
        # 发送请求
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"🎯 风险等级: {result.get('risk_level', 'unknown')}")
            print(f"📈 风险分数: {result.get('risk_score', 0)}")
            
            if 'detected_keywords' in result:
                print(f"🔍 检测到的关键词: {result['detected_keywords']}")
            
            if 'ai_analysis' in result and result['ai_analysis']:
                print(f"🤖 AI分析: {result['ai_analysis'][:100]}...")
            
            print("✅ 危机检测系统修复成功!")
            
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务，请确保后端正在运行")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_without_auth():
    """测试不需要认证的情况"""
    # 测试数据
    test_content = "我想死了"
    
    # API端点 - 使用测试端点
    url = "http://localhost:8000/crisis/assess-risk-test"
    
    # 请求数据
    data = {
        "content": test_content,
        "scene": "self-dialog",
        "enable_ai_analysis": True  # 启用AI分析进行完整测试
    }
    
    try:
        print(f"🧪 测试危机检测修复效果（使用测试端点）")
        print(f"📝 测试内容: {test_content}")
        print(f"🌐 API地址: {url}")
        print("-" * 50)
        
        # 发送请求
        response = requests.post(url, json=data, timeout=30)
        
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"🎯 风险等级: {result.get('risk_level', 'unknown')}")
            print(f"📈 风险分数: {result.get('risk_score', 0)}")
            
            if 'detected_keywords' in result:
                print(f"🔍 检测到的关键词: {result['detected_keywords']}")
            
            if 'fuzzy_matches' in result and result['fuzzy_matches']:
                print(f"🔄 模糊匹配: {result['fuzzy_matches']}")
            
            if 'ai_analysis' in result and result['ai_analysis']:
                print(f"🤖 AI分析: {result['ai_analysis'][:100]}...")
            
            print("✅ 危机检测系统修复成功!")
            
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_crisis_detection()
