import requests
import json

def test_auth_and_practice():
    """测试认证流程和交互式练习"""
    
    base_url = "http://127.0.0.1:8000"
    
    # 注册测试用户
    register_data = {
        "username": "testuser917",
        "password": "test123456",
        "email": "test917@example.com",
        "nickname": "测试用户"
    }
    
    print("🔐 1. 尝试注册测试用户...")
    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        
        if response.status_code == 201:
            print("✅ 注册成功")
        elif response.status_code == 400:
            print("ℹ️ 用户已存在，继续登录")
        else:
            print(f"❌ 注册失败: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 注册错误: {e}")
    
    # 登录获取token
    print("\n🔐 2. 登录获取token...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"✅ 登录成功，token: {token[:20]}...")
            
            # 设置认证头
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试交互式练习
            print("\n🧪 3. 测试交互式练习 (ID映射)...")
            test_cases = [
                {
                    "skill_id": 1,  # 应该映射到 "listen_actively"
                    "user_response": "我想学习如何更好地倾听朋友的心声",
                    "scenario_context": "朋友最近心情不好，想要找我聊天",
                    "is_first_message": True
                },
                {
                    "skill_id": 2,  # 应该映射到 "express_clearly"
                    "user_response": "我经常不知道怎么表达自己的想法",
                    "scenario_context": "在团队讨论中，我总是说不清楚自己的观点",
                    "is_first_message": True
                }
            ]
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n🧪 测试案例 {i}: 技能ID {test_case['skill_id']}")
                
                try:
                    response = requests.post(
                        f"{base_url}/social-skills/skills/interactive-practice",
                        json=test_case,
                        headers=headers,
                        timeout=30
                    )
                    
                    print(f"📡 响应状态: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        skill_info = result.get('skill', {})
                        print(f"✅ 请求成功")
                        print(f"🔧 技能标题: {skill_info.get('title', 'N/A')}")
                        print(f"🔧 技能ID: {skill_info.get('id', 'N/A')}")
                        
                        ai_response = result.get('ai_response', '')
                        print(f"🤖 AI回复长度: {len(ai_response)} 字符")
                        
                        if ai_response and ai_response != "我明白你的意思，让我们继续聊聊吧":
                            print(f"✅ AI功能正常 - 收到个性化回复")
                            print(f"🤖 AI回复预览: {ai_response[:150]}...")
                        else:
                            print(f"❌ AI功能异常 - 收到通用回复: {ai_response}")
                            
                    else:
                        print(f"❌ 请求失败: {response.status_code}")
                        print(f"📄 错误详情: {response.text}")
                        
                except requests.exceptions.Timeout:
                    print(f"⏰ 请求超时 - AI服务可能需要更长时间")
                except Exception as e:
                    print(f"❌ 请求异常: {e}")
            
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 登录错误: {e}")

if __name__ == "__main__":
    print("🚀 开始完整认证和功能测试...")
    test_auth_and_practice()
