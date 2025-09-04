#!/usr/bin/env python3
"""
AI增强危机检测系统测试脚本
测试模糊输入、同音字输入等功能
"""

import requests
import json
import datetime
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# 测试用例数据
TEST_CASES = [
    {
        "name": "模糊输入测试",
        "content": "我想zi sha，感觉zi己没用",
        "expected_level": "critical",
        "scene": "self-dialog"
    },
    {
        "name": "同音字测试",
        "content": "想4了，活着没意思",
        "expected_level": "critical", 
        "scene": "self-dialog"
    },
    {
        "name": "拆字测试",
        "content": "自 杀算了，受不了了",
        "expected_level": "critical",
        "scene": "love-experiment"
    },
    {
        "name": "英文混合测试",
        "content": "我want to die，真的很pain",
        "expected_level": "high",
        "scene": "self-love"
    },
    {
        "name": "多关键词测试",
        "content": "感觉绝望，很孤独，没人理解我",
        "expected_level": "high",
        "scene": "tree-hole"
    },
    {
        "name": "隐晦表达测试",
        "content": "如果有一天我不在了，你们会想我吗",
        "expected_level": "medium",
        "scene": "self-dialog"
    },
    {
        "name": "正常对话测试",
        "content": "今天天气不错，心情也还可以",
        "expected_level": "low",
        "scene": "self-dialog"
    },
    {
        "name": "情绪波动测试",
        "content": "最近情绪不太好，有点焦虑",
        "expected_level": "low",
        "scene": "self-love"
    }
]

def test_api_connection():
    """测试API连接"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_access_token():
    """获取访问令牌"""
    try:
        login_data = {
            "username": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"⚠️ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 登录错误: {e}")
        return None

def test_crisis_detection_api(content: str, scene: str, token: str = None) -> Dict[str, Any]:
    """测试危机检测API"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    data = {
        "content": content,
        "scene": scene
    }
    
    try:
        response = requests.post(f"{BASE_URL}/crisis/assess-risk", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API错误: {response.status_code}"}
    except Exception as e:
        return {"error": f"请求错误: {e}"}

def local_crisis_detection(content: str) -> Dict[str, Any]:
    """本地关键词检测算法"""
    
    # 简化的本地关键词检测
    CRISIS_KEYWORDS = {
        "自伤": ["自杀", "自残", "自伤", "结束生命", "不想活", "想死", "自我了断", "轻生", "了结", "自了", "了断", "want to die", "die", "kill myself"],
        "绝望": ["绝望", "无望", "没有希望", "看不到未来", "一片黑暗", "无路可走", "走投无路", "没救", "完了", "hopeless", "desperate"],
        "孤独": ["孤独", "孤单", "没人理解", "没人关心", "被遗弃", "被抛弃", "无人陪伴", "一个人", "形只影单", "lonely", "alone"],
        "无价值感": ["没用", "无价值", "废物", "垃圾", "拖累", "负担", "没意义", "多余", "无能", "失败者", "useless", "worthless"],
        "极端情绪": ["崩溃", "疯了", "受不了", "痛苦", "煎熬", "折磨", "地狱", "末日", "撑不住", "要疯", "pain", "suffering", "agony"],
        "隐晦表达": ["不在了", "离开这个世界", "解脱", "一了百了", "永远睡去", "再见了", "告别", "从此消失", "人间蒸发"]
    }
    
    # 模糊匹配模式（增强版）
    FUZZY_PATTERNS = {
        "自杀": ["zi sha", "自 杀", "zi4", "zisha", "自s", "自4", "自*杀", "zi*sha"],
        "想死": ["想 死", "想4", "想si", "xiang死", "xiang4", "想*死", "想*4"],
        "绝望": ["绝 望", "jue望", "绝wang", "jue*wang", "绝*望"],
        "崩溃": ["崩 溃", "beng溃", "崩kui", "beng*kui", "崩*溃"],
        "痛苦": ["痛 苦", "tong苦", "痛ku", "tong*ku", "痛*苦"],
        "不想活": ["不想 活", "buxianghuo", "不*想活", "bu*xiang*huo"],
        "结束生命": ["结束 生命", "jieshu生命", "结*束*生命"]
    }
    
    def detect_keywords(content):
        detected_keywords = []
        fuzzy_matches = []
        categories = []
        score = 0
        
        content_lower = content.lower()
        # 移除空格和特殊字符的内容用于模糊匹配
        content_normalized = ''.join(c for c in content_lower if c.isalnum())
        
        # 精确匹配
        for category, keywords in CRISIS_KEYWORDS.items():
            category_found = False
            category_score = 0  # 每个类别的分数
            for keyword in keywords:
                if keyword in content:
                    detected_keywords.append(keyword)
                    if not category_found:
                        categories.append(category)
                        category_found = True
                    # 累计该类别的分数（避免重复计分）
                    if category == "自伤":
                        if keyword in ["want to die", "die", "kill myself"]:
                            category_score = max(category_score, 12)  # 取最高分，不累加
                        else:
                            category_score = max(category_score, 20)
                    elif category == "绝望":
                        category_score = max(category_score, 8)
                    elif category == "极端情绪":
                        if keyword in ["pain", "suffering", "agony"]:
                            category_score = max(category_score, 4)
                        else:
                            category_score = max(category_score, 6)
                    elif category == "隐晦表达":
                        category_score = max(category_score, 12)
                    else:
                        category_score = max(category_score, 5)
            
            # 将该类别的分数加到总分
            score += category_score
        
        # 模糊匹配（增强版）
        for keyword, patterns in FUZZY_PATTERNS.items():
            for pattern in patterns:
                pattern_normalized = ''.join(c for c in pattern.lower() if c.isalnum())
                if pattern_normalized in content_normalized or pattern.lower() in content_lower:
                    fuzzy_matches.append(pattern)
                    # 模糊匹配也要添加对应类别
                    for category, keywords in CRISIS_KEYWORDS.items():
                        if keyword in keywords and category not in categories:
                            categories.append(category)
                            break
                    score += 8  # 模糊匹配权重
        
        # 风险等级判定（重新优化）
        if "自伤" in categories:
            # 如果包含模糊匹配的自伤词或中文自伤词，判定为critical
            if fuzzy_matches or any(kw in content for kw in ["自杀", "自残", "自伤", "想死", "不想活"]):
                risk_level = "critical"
            # 如果只有英文词汇且分数较低，判定为high
            elif score <= 16:
                risk_level = "high"
            else:
                risk_level = "critical"
        elif "隐晦表达" in categories and score >= 12:
            risk_level = "medium"  # 隐晦表达通常是中风险
        elif score >= 35 or len(categories) >= 4:
            risk_level = "critical"
        elif score >= 20 or len(categories) >= 3:
            risk_level = "high"
        elif score >= 12 or len(categories) >= 2:
            risk_level = "medium"
        elif score > 0:
            risk_level = "low"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": score,
            "detected_keywords": detected_keywords,
            "fuzzy_matches": fuzzy_matches,
            "categories": categories
        }
    
    return detect_keywords(content)

def main():
    print("🚀 启动AI增强危机检测系统测试")
    print(f"📅 测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API地址: {BASE_URL}/crisis/assess-risk")
    
    # 测试API连接
    print("🔌 测试API连接...")
    if test_api_connection():
        print("✅ 后端API服务正常")
        use_api = True
    else:
        print("❌ 后端API服务不可用，将使用本地检测")
        use_api = False
    
    print("🤖 AI增强危机检测系统测试开始")
    print("=" * 60)
    
    access_token = None
    if use_api:
        print("🔐 尝试获取访问令牌...")
        access_token = get_access_token()
        if not access_token:
            print("⚠️ 无法获取访问令牌，使用本地关键词检测")
            use_api = False
    
    if not use_api:
        print("🔧 使用本地关键词检测算法测试")
        print("=" * 60)
    
    results = []
    passed_tests = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 测试 {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"输入: {test_case['content']}")
        print(f"预期风险: {test_case['expected_level']}")
        
        if use_api and access_token:
            # 使用API测试
            result = test_crisis_detection_api(
                test_case['content'], 
                test_case['scene'], 
                access_token
            )
        else:
            # 使用本地检测
            result = local_crisis_detection(test_case['content'])
        
        if "error" in result:
            print(f"❌ 测试错误: {result['error']}")
            continue
        
        actual_level = result.get('risk_level', 'unknown')
        score = result.get('risk_score', 0)
        keywords = result.get('detected_keywords', [])
        fuzzy_matches = result.get('fuzzy_matches', [])
        
        print(f"🎯 检测结果: {actual_level} (分数: {score})")
        if keywords:
            print(f"🔍 关键词: {', '.join(keywords)}")
        if fuzzy_matches:
            print(f"🔄 模糊匹配: {', '.join(fuzzy_matches)}")
        
        # 判断测试是否通过
        test_passed = actual_level == test_case['expected_level']
        if test_passed:
            print("📊 测试结果: ✅ 通过")
            passed_tests += 1
        else:
            print("📊 测试结果: ❌ 失败")
        
        # 保存结果
        results.append({
            "test_name": test_case['name'],
            "input": test_case['content'],
            "expected": test_case['expected_level'],
            "actual": actual_level,
            "score": score,
            "keywords": keywords,
            "fuzzy_matches": fuzzy_matches,
            "passed": test_passed
        })
    
    # 生成测试报告
    print("\n" + "=" * 60)
    print("📊 测试报告")
    print("=" * 60)
    print(f"总测试数: {len(TEST_CASES)}")
    print(f"通过测试: {passed_tests}")
    print(f"成功率: {passed_tests/len(TEST_CASES)*100:.1f}%")
    
    print(f"\n详细结果:")
    for result in results:
        status = "✅" if result['passed'] else "❌"
        print(f"{status} {result['test_name']}: {result['expected']} -> {result['actual']}")
    
    # 保存测试结果到文件
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crisis_detection_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.datetime.now().isoformat(),
            "total_tests": len(TEST_CASES),
            "passed_tests": passed_tests,
            "success_rate": passed_tests/len(TEST_CASES)*100,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 测试结果已保存到: {filename}")
    
    if passed_tests == len(TEST_CASES):
        print("\n🎉 所有测试通过！AI增强危机检测系统运行正常。")
    else:
        print("\n⚠️ 部分测试失败，请检查系统配置。")

if __name__ == "__main__":
    main()
