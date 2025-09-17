import requests
import json

def test_console_output():
    """测试控制台输出功能"""
    
    base_url = "http://127.0.0.1:8000"
    
    # 登录获取token
    login_data = {"username": "testuser917", "password": "test123456"}
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            print("🧪 测试控制台输出功能...")
            print("请查看后端控制台的详细输出信息\n")
            
            # 测试案例1：首次对话
            print("📝 发送测试案例1：首次对话")
            test_data_1 = {
                "skill_id": 1,  # listen_actively
                "user_response": "朋友，我今天心情真的很糟糕，可以听我说说吗？",
                "scenario_context": "好朋友心情不好，想要倾诉",
                "is_first_message": True,
                "chat_history": []
            }
            
            response1 = requests.post(
                f"{base_url}/social-skills/skills/interactive-practice",
                json=test_data_1,
                headers=headers,
                timeout=30
            )
            
            if response1.status_code == 200:
                result1 = response1.json()
                print(f"✅ 首次对话成功")
                print(f"🤖 AI回复预览: {result1.get('ai_response', '')[:100]}...")
                
                # 测试案例2：继续对话
                print(f"\n📝 发送测试案例2：继续对话")
                test_data_2 = {
                    "skill_id": 1,
                    "user_response": "谢谢你愿意听我说，我今天被室友误解了，感觉很委屈",
                    "scenario_context": "好朋友心情不好，想要倾诉", 
                    "is_first_message": False,
                    "chat_history": [
                        {"role": "user", "content": test_data_1["user_response"]},
                        {"role": "assistant", "content": result1.get('ai_response', '')[:100]}
                    ]
                }
                
                response2 = requests.post(
                    f"{base_url}/social-skills/skills/interactive-practice",
                    json=test_data_2,
                    headers=headers,
                    timeout=30
                )
                
                if response2.status_code == 200:
                    result2 = response2.json()
                    print(f"✅ 继续对话成功")
                    print(f"🤖 AI回复预览: {result2.get('ai_response', '')[:100]}...")
                else:
                    print(f"❌ 继续对话失败: {response2.status_code}")
                    
            else:
                print(f"❌ 首次对话失败: {response1.status_code}")
                
            print(f"\n🎯 测试完成！请查看后端控制台的详细输出信息")
            print(f"后端控制台应该显示:")
            print(f"  📋 技能信息")
            print(f"  👤 用户消息")
            print(f"  📜 完整AI提示词")
            print(f"  🤖 AI服务调用过程")
            print(f"  ✨ 最终回复结果")
                
        else:
            print(f"❌ 登录失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_console_output()
