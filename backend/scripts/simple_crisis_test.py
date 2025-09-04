#file:ariadne/backend/scripts/simple_crisis_test.py
"""
心理危机预警系统简单测试
"""
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.crisis_warning_service import CrisisWarningService, RiskLevel

def test_keyword_detection_only():
    """仅测试关键词检测功能（不依赖数据库）"""
    print("🔍 测试关键词检测功能...")
    
    # 创建一个模拟的数据库会话（None）
    service = CrisisWarningService(None)
    
    # 测试用例
    test_cases = [
        {
            "text": "我今天心情很好，阳光明媚",
            "expected_level": RiskLevel.LOW,
            "description": "正常积极内容"
        },
        {
            "text": "感觉有点孤独，但还能应对",
            "expected_level": RiskLevel.LOW,
            "description": "轻微负面情绪"
        },
        {
            "text": "我觉得自己没用，是个废物，活着没意义",
            "expected_level": RiskLevel.MEDIUM,
            "description": "中等风险 - 无价值感"
        },
        {
            "text": "我绝望了，看不到希望，感觉孤独无助",
            "expected_level": RiskLevel.HIGH,
            "description": "高风险 - 多种负面情绪"
        },
        {
            "text": "我不想活了，想要自杀，结束这痛苦",
            "expected_level": RiskLevel.CRITICAL,
            "description": "紧急风险 - 自伤倾向"
        }
    ]
    
    print("\n测试结果：")
    print("-" * 60)
    
    for i, case in enumerate(test_cases, 1):
        result = service._analyze_text_for_crisis(case["text"], "测试")
        
        status = "✅" if result.risk_level == case["expected_level"] else "❌"
        
        print(f"{status} 测试 {i}: {case['description']}")
        print(f"   文本: {case['text']}")
        print(f"   预期风险: {case['expected_level'].value}")
        print(f"   实际风险: {result.risk_level.value}")
        print(f"   风险评分: {result.score:.1f}")
        if result.reasons:
            print(f"   检测原因: {'; '.join(result.reasons)}")
        print()

def test_crisis_keywords():
    """测试危机关键词配置"""
    print("📝 测试危机关键词配置...")
    
    keywords = CrisisWarningService.CRISIS_KEYWORDS
    
    print(f"✅ 关键词类别数量: {len(keywords)}")
    for category, words in keywords.items():
        print(f"   {category}: {len(words)} 个关键词")
        print(f"      示例: {', '.join(words[:3])}{'...' if len(words) > 3 else ''}")
    
    print()

def show_api_examples():
    """显示API使用示例"""
    print("🚀 API 使用示例")
    print("-" * 40)
    print("""
1. 风险评估 API:
   POST /api/crisis/assess-risk?days=14
   
   响应示例:
   {
     "risk_level": "medium",
     "score": 65.0,
     "reasons": ["近14天平均心情偏低", "检测到孤独相关表达"],
     "recommendations": ["建议寻求专业心理咨询", "保持与亲友联系"]
   }

2. 获取预警记录 API:
   GET /api/crisis/warnings?days=30&unresolved_only=false
   
3. 解决预警 API:
   POST /api/crisis/warnings/{warning_id}/resolve
   
4. 前端组件使用:
   <CrisisWarning :auto-assess="true" :show-history="true" />
""")

def show_integration_guide():
    """显示集成指南"""
    print("🔧 集成指南")
    print("-" * 40)
    print("""
1. 后端集成:
   • 在日记提交时调用危机检测
   • 在AI对话时进行实时监控
   • 设置定时任务进行周期性风险评估

2. 前端集成:
   • 在个人中心添加风险评估模块
   • 在日记页面集成实时关键词检测
   • 添加紧急求助快捷入口

3. 风险响应流程:
   • 低风险: 无需特殊处理
   • 中等风险: 温和提醒，提供自助资源
   • 高风险: 主动推送关怀信息和专业建议
   • 紧急风险: 立即显示求助信息，记录紧急事件

4. 隐私保护:
   • 预警数据加密存储
   • 用户可选择关闭监控功能
   • 严格控制数据访问权限
""")

def main():
    """主函数"""
    print("🧠 心理危机预警系统 - 核心功能测试")
    print("=" * 50)
    
    # 1. 测试关键词检测
    test_keyword_detection_only()
    
    # 2. 测试关键词配置
    test_crisis_keywords()
    
    # 3. 显示API示例
    show_api_examples()
    
    # 4. 显示集成指南
    show_integration_guide()
    
    print("\n✅ 核心功能测试完成！")
    print("\n💡 下一步:")
    print("1. 启动后端服务测试完整API")
    print("2. 在前端页面中集成危机预警组件")
    print("3. 根据实际使用情况调整风险阈值")

if __name__ == "__main__":
    main()
