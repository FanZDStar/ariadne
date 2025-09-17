import requests
import json

def test_corrected_role_play():
    """测试修正后的角色扮演逻辑"""
    
    base_url = "http://127.0.0.1:8000"
    
    # 登录获取token
    login_data = {"username": "testuser917", "password": "test123456"}
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            print("🎭 测试修正后的角色扮演逻辑")
            print("="*60)
            
            # 测试案例：不同技能的角色设定
            test_cases = [
                {
                    "name": "主动倾听",
                    "skill_id": 1,
                    "user_response": "你好，我看你好像心情不太好，想聊聊吗？",
                    "scenario_context": "朋友心情不好，需要有人倾听",
                    "expected_ai_role": "心情不好、需要倾诉的朋友",
                    "expected_user_role": "练习主动倾听技巧的倾听者"
                },
                {
                    "name": "失望处理", 
                    "skill_id": 29,
                    "user_response": "我注意到你最近好像有点沮丧，发生什么事了吗？",
                    "scenario_context": "室友考试失利，感到失望",
                    "expected_ai_role": "考试失利、感到失望的室友",
                    "expected_user_role": "练习安慰和支持技巧的朋友"
                },
                {
                    "name": "清晰表达",
                    "skill_id": 2, 
                    "user_response": "我想和你谈一下我们之间的一个问题",
                    "scenario_context": "需要向朋友表达内心想法和感受",
                    "expected_ai_role": "不太理解状况、需要别人表达清楚的朋友",
                    "expected_user_role": "练习清晰表达技巧的表达者"
                }
            ]
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n🧪 测试案例 {i}: {test_case['name']}")
                print(f"📋 期望AI角色: {test_case['expected_ai_role']}")
                print(f"👤 期望用户角色: {test_case['expected_user_role']}")
                
                test_data = {
                    "skill_id": test_case["skill_id"],
                    "user_response": test_case["user_response"],
                    "scenario_context": test_case["scenario_context"],
                    "is_first_message": True,
                    "chat_history": []
                }
                
                response = requests.post(
                    f"{base_url}/social-skills/skills/interactive-practice",
                    json=test_data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('ai_response', '')
                    
                    print(f"✅ 请求成功")
                    print(f"🤖 AI回复: {ai_response}")
                    
                    # 分析AI回复是否符合"需要帮助的人"角色
                    help_indicators = ["我", "感觉", "困难", "不知道", "难受", "失望", "沮丧", "压力", "迷茫"]
                    helper_indicators = ["你应该", "建议你", "我觉得你", "你需要", "最好"]
                    
                    help_count = sum(1 for word in help_indicators if word in ai_response)
                    helper_count = sum(1 for word in helper_indicators if word in ai_response)
                    
                    if help_count > helper_count:
                        print(f"✅ 角色正确：AI表现为需要帮助的人")
                    else:
                        print(f"⚠️ 角色可能有问题：AI可能在提供建议而不是寻求帮助")
                        
                else:
                    print(f"❌ 请求失败: {response.status_code}")
                    
            print(f"\n📌 角色验证说明：")
            print(f"✅ 正确的角色设定：")
            print(f"   🤖 AI = 需要帮助、支持、倾听的人")
            print(f"   👤 用户 = 练习技能的帮助者")
            print(f"⚠️ 之前错误的设定：")
            print(f"   🤖 AI = 提供帮助的专家")
            print(f"   👤 用户 = 被帮助的人")
                
        else:
            print(f"❌ 登录失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_corrected_role_play()
