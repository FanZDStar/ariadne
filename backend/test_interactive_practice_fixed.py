import asyncio
import aiohttp
import json

async def test_interactive_practice():
    """测试修复后的交互式练习功能"""
    
    # 测试数据 - 使用数字ID（前端发送的格式）
    test_cases = [
        {
            "skill_id": 1,  # 对应 "listen_actively"
            "user_message": "我想学习如何更好地倾听朋友的心声",
            "context": "朋友最近心情不好，想要找我聊天"
        },
        {
            "skill_id": 2,  # 对应 "express_clearly" 
            "user_message": "我经常不知道怎么表达自己的想法",
            "context": "在团队讨论中，我总是说不清楚自己的观点"
        },
        {
            "skill_id": 3,  # 对应 "topic_transition"
            "user_message": "聊天时经常冷场，不知道怎么继续话题",
            "context": "第一次约会，气氛有点尴尬"
        }
    ]
    
    base_url = "http://127.0.0.1:8000"
    
    # 首先测试登录获取token（如果需要）
    login_data = {
        "username": "test@example.com",
        "password": "test123"
    }
    
    async with aiohttp.ClientSession() as session:
        # 尝试登录
        try:
            async with session.post(f"{base_url}/auth/login", data=login_data) as response:
                if response.status == 200:
                    result = await response.json()
                    token = result.get("access_token")
                    print(f"✅ 登录成功，获取到token")
                    headers = {"Authorization": f"Bearer {token}"}
                else:
                    print(f"❌ 登录失败: {response.status}")
                    headers = {}
        except Exception as e:
            print(f"⚠️ 登录接口测试失败，使用无认证模式: {e}")
            headers = {}
        
        # 测试每个技能
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 测试案例 {i}: 技能ID {test_case['skill_id']}")
            
            try:
                async with session.post(
                    f"{base_url}/social-skills/skills/interactive-practice",
                    json=test_case,
                    headers=headers
                ) as response:
                    
                    print(f"📡 响应状态: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ 请求成功")
                        print(f"🔧 技能信息: {result.get('skill', {}).get('title', 'N/A')}")
                        
                        ai_response = result.get('ai_response', '')
                        if ai_response and ai_response != "我明白你的意思，让我们继续聊聊吧":
                            print(f"🤖 AI回复: {ai_response[:100]}...")
                            print(f"✅ AI功能正常 - 收到个性化回复")
                        else:
                            print(f"❌ AI功能异常 - 收到通用回复: {ai_response}")
                            
                    else:
                        error_text = await response.text()
                        print(f"❌ 请求失败: {error_text}")
                        
            except Exception as e:
                print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    print("🚀 开始测试修复后的交互式练习功能...")
    asyncio.run(test_interactive_practice())
