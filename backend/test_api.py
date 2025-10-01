#!/usr/bin/env python3
"""
测试API端点
"""
import requests
import json

# 测试数据
test_data = {
    "session_title": "测试会话",
    "practice_scenario": "workplace_communication",
    "practice_scenario_name": "职场沟通",
    "messages": [
        {
            "role": "assistant",
            "content": "你好，欢迎开始练习！",
            "timestamp": "2024-10-01T10:00:00"
        },
        {
            "role": "user", 
            "content": "你好！",
            "timestamp": "2024-10-01T10:01:00"
        }
    ],
    "practice_duration": 60,
    "practice_type": "ai_dialog",
    "difficulty_level": "beginner",
    "completion_status": "completed",
    "skills_practiced": ["沟通技巧"],
    "strengths": [],
    "improvements": []
}

# 模拟登录获取token（这里需要替换为实际的token）
token = "your_access_token_here"

try:
    # 测试创建会话
    response = requests.post(
        "http://localhost:8000/interpersonal-practice/sessions",
        json=test_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"创建会话响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        print("✅ 创建会话成功！")
        session_data = response.json()
        session_id = session_data.get('id')
        
        # 测试获取会话列表
        list_response = requests.get(
            "http://localhost:8000/interpersonal-practice/sessions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"获取列表响应状态码: {list_response.status_code}")
        print(f"列表响应内容: {list_response.text}")
        
    else:
        print("❌ 创建会话失败")
        
except Exception as e:
    print(f"测试出错: {str(e)}")
