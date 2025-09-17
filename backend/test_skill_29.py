import requests
import json

def test_skill_29():
    """测试技能ID 29的映射和AI回复"""
    
    base_url = "http://127.0.0.1:8000"
    
    # 登录获取token
    login_data = {
        "username": "testuser917",
        "password": "test123456"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试技能ID 29
            test_data = {
                "skill_id": 29,  # disappointment_handling
                "user_response": "我今天考试考砸了，感觉很失望",
                "scenario_context": "期末考试成绩不理想，心情低落",
                "is_first_message": True
            }
            
            print(f"🧪 测试技能ID 29...")
            print(f"📝 测试数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                f"{base_url}/social-skills/skills/interactive-practice",
                json=test_data,
                headers=headers,
                timeout=30
            )
            
            print(f"\n📡 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                skill_info = result.get('skill', {})
                print(f"✅ 请求成功")
                print(f"🔧 技能标题: {skill_info.get('title', 'N/A')}")
                print(f"🔧 技能ID: {skill_info.get('id', 'N/A')}")
                print(f"🔧 技能内容: {skill_info.get('content', 'N/A')}")
                
                ai_response = result.get('ai_response', '')
                print(f"🤖 AI回复长度: {len(ai_response)} 字符")
                print(f"🤖 AI回复: {ai_response}")
                
                if ai_response and ai_response != "我明白你的意思，让我们继续聊聊吧":
                    print(f"✅ AI功能正常 - 收到个性化回复")
                else:
                    print(f"❌ AI功能异常 - 收到通用回复")
                    
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"📄 错误详情: {response.text}")
                
        else:
            print(f"❌ 登录失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_skill_29()
