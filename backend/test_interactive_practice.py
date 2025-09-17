#!/usr/bin/env python3
"""测试交互式技能练习API"""

import asyncio
import sys
import os
import httpx

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_interactive_practice():
    """测试交互式技能练习"""
    print("测试交互式技能练习API...")
    
    # 测试数据
    test_data = {
        "skill_id": 1,  # 使用数字ID
        "user_response": "你好，我想练习一下倾听技巧",
        "scenario_context": "朋友倾诉烦恼的场景",
        "chat_history": [],
        "is_first_message": True
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # 首先需要登录获取token（这里简化处理）
            response = await client.post(
                "http://localhost:8000/social-skills/skills/interactive-practice",
                json=test_data,
                headers={
                    "Authorization": "Bearer fake_token_for_test",  # 实际需要真实token
                    "Content-Type": "application/json"
                }
            )
            
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"响应类型: {result.get('response_type')}")
                print(f"AI回应: {result.get('ai_response', '')[:200]}...")
                print("✅ 交互式练习API测试通过")
            else:
                print(f"❌ API调用失败: {response.text}")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_interactive_practice())
