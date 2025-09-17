import requests
import json

def test_unified_data_source():
    """测试统一数据源的完整性"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 测试统一数据源...")
    
    try:
        # 测试技能分类接口
        response = requests.get(f"{base_url}/social-skills/skills/categories")
        
        print(f"📡 分类接口状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            categories = result.get("categories", [])
            
            print(f"✅ 成功获取技能分类")
            total_skills = 0
            
            for category in categories:
                print(f"📂 {category['name']}: {category['skill_count']} 个技能")
                total_skills += category['skill_count']
            
            print(f"📊 总技能数: {total_skills}")
            
            if total_skills == 65:
                print("✅ 技能数量正确 - 所有65个技能已加载")
            else:
                print(f"⚠️ 技能数量不匹配 - 期望65个，实际{total_skills}个")
                
        else:
            print(f"❌ 分类接口失败: {response.text}")
            
        # 测试几个不同分类的技能
        test_skills = [1, 29, 45, 60]  # 不同分类的技能
        
        # 需要登录才能测试交互式练习
        login_data = {"username": "testuser917", "password": "test123456"}
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            print(f"\n🧪 测试不同分类的技能...")
            
            for skill_id in test_skills:
                test_data = {
                    "skill_id": skill_id,
                    "user_response": f"我想练习技能{skill_id}",
                    "scenario_context": "测试场景",
                    "is_first_message": True
                }
                
                response = requests.post(
                    f"{base_url}/social-skills/skills/interactive-practice",
                    json=test_data,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    skill_info = result.get('skill', {})
                    print(f"✅ 技能{skill_id}: {skill_info.get('title', 'N/A')} (ID: {skill_info.get('id', 'N/A')})")
                else:
                    print(f"❌ 技能{skill_id}测试失败: {response.status_code}")
        else:
            print("⚠️ 无法登录，跳过交互式练习测试")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_unified_data_source()
