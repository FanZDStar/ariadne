import requests
import json
from datetime import date

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_mood_tracker():
    """测试心情晴雨表功能"""
    print("=== 心情晴雨表功能测试 ===")
    
    # 这里需要一个有效的token，实际使用时需要先登录获取
    token = "your_access_token_here"  # 需要替换为实际的token
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试记录心情
    print("\n1. 测试记录心情...")
    mood_data = {
        "mood_level": 4,
        "mood_date": str(date.today())
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/mood-tracker/mood",
            headers=headers,
            json=mood_data
        )
        print(f"记录心情响应: {response.status_code}")
        if response.status_code == 200:
            print(f"响应内容: {response.json()}")
        else:
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试获取7天数据
    print("\n2. 测试获取7天心情数据...")
    try:
        response = requests.get(
            f"{BASE_URL}/mood-tracker/mood/weekly",
            headers=headers
        )
        print(f"获取数据响应: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"7天数据: {data}")
            print("\n7天心情表格:")
            for i, date_str in enumerate(data.get("dates", [])):
                level = data.get("levels", [])[i]
                print(f"{date_str}: {level if level else '--'}")
        else:
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_mood_tracker()
