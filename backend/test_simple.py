import requests
import json

def test_interactive_practice_simple():
    """简化测试 - 直接发送请求，无认证"""
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试数据
    test_data = {
        "skill_id": 1,  # 数字ID，应该被映射为 "listen_actively"
        "user_message": "我想学习如何更好地倾听朋友的心声",
        "context": "朋友最近心情不好，想要找我聊天",
        "is_first_message": True
    }
    
    print(f"🧪 测试数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送请求
        response = requests.post(
            f"{base_url}/social-skills/skills/interactive-practice",
            json=test_data,
            timeout=30
        )
        
        print(f"\n📡 响应状态: {response.status_code}")
        print(f"📡 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 请求成功!")
            print(f"🔧 技能信息: {result.get('skill', {}).get('title', 'N/A')}")
            
            ai_response = result.get('ai_response', '')
            print(f"🤖 AI回复长度: {len(ai_response)} 字符")
            
            if ai_response and ai_response != "我明白你的意思，让我们继续聊聊吧":
                print(f"✅ AI功能正常 - 收到个性化回复")
                print(f"🤖 AI回复预览: {ai_response[:200]}...")
            else:
                print(f"❌ AI功能异常 - 收到通用回复: {ai_response}")
                
        elif response.status_code == 401:
            print(f"🔐 需要认证，这是预期的")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"📄 错误详情: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

def test_skill_database():
    """测试技能数据库接口"""
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # 获取技能分类（不需要认证）
        response = requests.get(f"{base_url}/social-skills/skills/categories")
        
        print(f"\n🗃️ 技能数据库测试")
        print(f"📡 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功获取技能分类")
            print(f"📊 技能分类: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 获取技能分类失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 技能数据库测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始简化测试...")
    test_skill_database()
    test_interactive_practice_simple()
