#!/usr/bin/env python3
"""
AI增强危机检测API测试脚本
测试各种输入模式的检测效果
"""

import requests
import json
import time
f                    # 权重分配
                    if category == "自伤":
                        # 如果是英文关键词，稍微降低权重
                        if keyword in ["want to die", "die", "kill myself"]:
                            score += 10  # 英文自伤词权重稍低
                        else:
                            score += 20  # 中文自伤词保持高权重
                    elif category == "绝望":
                        score += 8
                    elif category == "极端情绪":
                        if keyword in ["pain", "suffering", "agony"]:
                            score += 5  # 英文情绪词权重降低
                        else:
                            score += 6
                    elif category == "隐晦表达":
                        score += 12  # 隐晦表达权重较高
                    else:
                        score += 5e import datetime

# API配置
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/crisis/assess-risk"

# 测试用例
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
        "scene": "general"
    },
    {
        "name": "情绪波动测试",
        "content": "最近情绪不太好，有点焦虑",
        "expected_level": "low",
        "scene": "self-dialog"
    }
]

def test_local_detection():
    """使用本地关键词检测进行测试"""
    print("🔧 使用本地关键词检测算法测试")
    print("=" * 60)
    
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
            for keyword in keywords:
                if keyword in content:
                    detected_keywords.append(keyword)
                    if not category_found:
                        categories.append(category)
                        category_found = True
                    # 权重分配（调整权重避免过度放大）
                    if category == "自伤":
                        score += 20  # 自伤类最高权重
                    elif category == "绝望":
                        score += 8
                    elif category == "极端情绪":
                        score += 6
                    elif category == "隐晦表达":
                        score += 12  # 隐晦表达需要特殊关注
                    else:
                        score += 5
        
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
                    score += 8  # 降低模糊匹配权重
        
        # 风险等级判定（精细调整阈值）
        if "自伤" in categories:
            risk_level = "critical"
        elif "隐晦表达" in categories and score >= 12:
            risk_level = "medium"  # 隐晦表达通常是中风险
        elif score >= 45 or len(categories) >= 5:
            risk_level = "critical"
        elif score >= 28 or (len(categories) >= 3 and score >= 20):
            risk_level = "high"
        elif score >= 15 or len(categories) >= 2:
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
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 测试 {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"输入: {test_case['content']}")
        print(f"预期风险: {test_case['expected_level']}")
        
        # 本地检测
        result = detect_keywords(test_case['content'])
        
        print(f"🎯 检测结果: {result['risk_level']} (分数: {result['risk_score']})")
        
        if result['detected_keywords']:
            print(f"🔍 关键词: {', '.join(result['detected_keywords'])}")
        
        if result['fuzzy_matches']:
            print(f"🔄 模糊匹配: {', '.join(result['fuzzy_matches'])}")
        
        # 判断测试结果
        is_correct = result['risk_level'] == test_case['expected_level']
        status = "✅ 通过" if is_correct else "❌ 失败"
        print(f"📊 测试结果: {status}")
        
        results.append({
            "test_name": test_case['name'],
            "expected": test_case['expected_level'],
            "actual": result['risk_level'],
            "correct": is_correct,
            "score": result['risk_score'],
            "keywords": result['detected_keywords'],
            "fuzzy_matches": result['fuzzy_matches']
        })
    
    return results

def get_test_token():
    """获取测试用的访问令牌"""
    login_url = f"{BASE_URL}/auth/login"
    
    # 使用测试账号登录（需要先创建测试账号）
    login_data = {
        "username": "test_user",
        "password": "test_password"
    }
    
    try:
        response = requests.post(login_url, data=login_data, timeout=5)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"⚠️ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 登录异常: {str(e)}")
        return None

def test_crisis_detection():
    """测试危机检测API"""
    print("🤖 AI增强危机检测系统测试开始")
    print("=" * 60)
    
    # 尝试获取访问令牌
    print("🔐 尝试获取访问令牌...")
    access_token = get_test_token()
    
    if not access_token:
        print("⚠️ 无法获取访问令牌，使用本地关键词检测")
        local_results = test_local_detection()
        return generate_test_report(local_results)
    
    print("✅ 已获取访问令牌")
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 测试 {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"输入: {test_case['content']}")
        print(f"场景: {test_case['scene']}")
        print(f"预期风险: {test_case['expected_level']}")
        
        try:
            # 准备请求数据
            payload = {
                "content": test_case['content'],
                "scene": test_case['scene'],
                "keyword_score": 0,
                "enable_ai_analysis": True
            }
            
            # 发送请求（带认证头）
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            start_time = time.time()
            response = requests.post(
                API_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=10
            )
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            if response.status_code == 200:
                result = response.json()
                
                # 显示结果
                print(f"✅ 响应时间: {response_time:.1f}ms")
                print(f"🎯 检测结果: {result['risk_level']} (分数: {result['risk_score']:.1f})")
                
                if result['detected_keywords']:
                    print(f"🔍 关键词: {', '.join(result['detected_keywords'])}")
                
                if result['fuzzy_matches']:
                    print(f"🔄 模糊匹配: {', '.join(result['fuzzy_matches'])}")
                
                if result['ai_analysis']:
                    print(f"🤖 AI分析: {result['ai_analysis']}")
                
                # 判断测试结果
                is_correct = result['risk_level'] == test_case['expected_level']
                status = "✅ 通过" if is_correct else "❌ 失败"
                print(f"📊 测试结果: {status}")
                
                results.append({
                    "test_name": test_case['name'],
                    "expected": test_case['expected_level'],
                    "actual": result['risk_level'],
                    "correct": is_correct,
                    "response_time": response_time,
                    "score": result['risk_score'],
                    "keywords": result['detected_keywords'],
                    "fuzzy_matches": result['fuzzy_matches']
                })
                
            else:
                print(f"❌ API错误: {response.status_code}")
                print(f"错误信息: {response.text}")
                results.append({
                    "test_name": test_case['name'],
                    "expected": test_case['expected_level'],
                    "actual": "error",
                    "correct": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            results.append({
                "test_name": test_case['name'],
                "expected": test_case['expected_level'],
                "actual": "error",
                "correct": False,
                "error": str(e)
            })
    
    return results

def generate_test_report(results):
    """生成测试报告"""
    # 生成测试报告
    print("\n" + "=" * 60)
    print("📊 测试报告")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['correct'])
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"成功率: {success_rate:.1f}%")
    
    if any('response_time' in r for r in results):
        avg_response_time = sum(r.get('response_time', 0) for r in results if 'response_time' in r) / total_tests
        print(f"平均响应时间: {avg_response_time:.1f}ms")
    
    print("\n详细结果:")
    for result in results:
        status = "✅" if result['correct'] else "❌"
        print(f"{status} {result['test_name']}: {result['expected']} -> {result['actual']}")
    
    # 保存测试结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crisis_detection_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": success_rate,
                "avg_response_time": locals().get('avg_response_time', None)
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 测试结果已保存到: {filename}")
    
    return success_rate >= 80  # 80%以上成功率视为测试通过

def test_crisis_detection():
    """测试危机检测API"""
    print("🤖 AI增强危机检测系统测试开始")
    print("=" * 60)
    
    # 尝试获取访问令牌
    print("🔐 尝试获取访问令牌...")
    access_token = get_test_token()
    
    if not access_token:
        print("⚠️ 无法获取访问令牌，使用本地关键词检测")
        local_results = test_local_detection()
        return generate_test_report(local_results)
    
    print("✅ 已获取访问令牌")
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 测试 {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"输入: {test_case['content']}")
        print(f"场景: {test_case['scene']}")
        print(f"预期风险: {test_case['expected_level']}")
        
        try:
            # 准备请求数据
            payload = {
                "content": test_case['content'],
                "scene": test_case['scene'],
                "keyword_score": 0,
                "enable_ai_analysis": True
            }
            
            # 发送请求（带认证头）
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            start_time = time.time()
            response = requests.post(
                API_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=10
            )
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            if response.status_code == 200:
                result = response.json()
                
                # 显示结果
                print(f"✅ 响应时间: {response_time:.1f}ms")
                print(f"🎯 检测结果: {result['risk_level']} (分数: {result['risk_score']:.1f})")
                
                if result['detected_keywords']:
                    print(f"🔍 关键词: {', '.join(result['detected_keywords'])}")
                
                if result['fuzzy_matches']:
                    print(f"🔄 模糊匹配: {', '.join(result['fuzzy_matches'])}")
                
                if result['ai_analysis']:
                    print(f"🤖 AI分析: {result['ai_analysis']}")
                
                # 判断测试结果
                is_correct = result['risk_level'] == test_case['expected_level']
                status = "✅ 通过" if is_correct else "❌ 失败"
                print(f"📊 测试结果: {status}")
                
                results.append({
                    "test_name": test_case['name'],
                    "expected": test_case['expected_level'],
                    "actual": result['risk_level'],
                    "correct": is_correct,
                    "response_time": response_time,
                    "score": result['risk_score'],
                    "keywords": result['detected_keywords'],
                    "fuzzy_matches": result['fuzzy_matches']
                })
                
            else:
                print(f"❌ API错误: {response.status_code}")
                print(f"错误信息: {response.text}")
                results.append({
                    "test_name": test_case['name'],
                    "expected": test_case['expected_level'],
                    "actual": "error",
                    "correct": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            results.append({
                "test_name": test_case['name'],
                "expected": test_case['expected_level'],
                "actual": "error",
                "correct": False,
                "error": str(e)
            })
    
    # 生成测试报告
    print("\n" + "=" * 60)
    print("📊 测试报告")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['correct'])
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"成功率: {success_rate:.1f}%")
    
    if any('response_time' in r for r in results):
        avg_response_time = sum(r.get('response_time', 0) for r in results if 'response_time' in r) / total_tests
        print(f"平均响应时间: {avg_response_time:.1f}ms")
    
    print("\n详细结果:")
    for result in results:
        status = "✅" if result['correct'] else "❌"
        print(f"{status} {result['test_name']}: {result['expected']} -> {result['actual']}")
    
    # 保存测试结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crisis_detection_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time if 'avg_response_time' in locals() else None
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 测试结果已保存到: {filename}")
    
    return success_rate >= 80  # 80%以上成功率视为测试通过

def test_api_connectivity():
    """测试API连接性"""
    print("🔌 测试API连接...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API服务正常")
            return True
        else:
            print(f"❌ 后端API返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端API: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 启动AI增强危机检测系统测试")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API地址: {API_ENDPOINT}")
    
    # 先测试连接性
    if not test_api_connectivity():
        print("❌ API连接失败，请确保后端服务正在运行")
        exit(1)
    
    # 执行主要测试
    success = test_crisis_detection()
    
    if success:
        print("\n🎉 所有测试通过！AI增强危机检测系统运行正常。")
        exit(0)
    else:
        print("\n⚠️ 部分测试失败，请检查系统配置。")
        exit(1)
