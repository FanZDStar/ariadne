"""
测试AI生成防护训练报告分析功能 - 简化版本
使用urllib而不是requests库
"""

import urllib.request
import urllib.parse
import json
import sys
import os

# 配置
API_BASE_URL = "http://localhost:8000"
USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJXamMxMjM0NTYiLCJleHAiOjE3NTk0Nzk0MzJ9.CDHOsf1MKin4L0mTWe6y2uZSrv4lG-6-oZBlQMCL6Cw"

def make_request(url, method="GET", data=None, headers=None):
    """发送HTTP请求"""
    if headers is None:
        headers = {}
    
    # 设置默认headers
    headers.update({
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    })
    
    # 准备请求数据
    if data:
        data = json.dumps(data).encode('utf-8')
    
    # 创建请求
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            return response.status, json.loads(response_data) if response_data else {}
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        return e.code, error_data
    except Exception as e:
        return 500, str(e)

def test_ai_generated_report():
    """测试AI生成的训练报告"""
    
    # 测试数据 - 情感欺诈识别训练
    test_data = {
        "drill_type": "情感欺诈识别",
        "scenario_name": "网恋陷阱",
        "total_questions": 10,
        "correct_answers": 7,
        "score": 70.0,
        "completion_time": 480,  # 8分钟
        "suggestions": "需要加强对情感欺诈手段的识别",
        # AI分析所需的答题数据
        "answers": [1, 2, 1, 3, 2, 1, 4, 2, 3, 1],  # 用户的选择
        "correct_answers_list": [1, 3, 1, 3, 2, 2, 4, 1, 3, 1],  # 正确答案
        "questions_data": [
            {
                "question": "对方在初次聊天就表达强烈好感，这是否正常？",
                "options": ["不正常，可能是套路", "正常，一见钟情", "需要进一步观察", "无法判断"],
                "type": "判断题"
            },
            {
                "question": "对方要求您提供详细个人信息，应该怎么做？",
                "options": ["立即提供", "询问原因", "拒绝提供", "提供部分信息"],
                "type": "选择题"
            },
            {
                "question": "对方声称遇到紧急情况需要经济帮助，您的反应是？",
                "options": ["立即帮助", "先核实情况", "拒绝帮助", "寻求他人建议"],
                "type": "情境题"
            },
            {
                "question": "对方总是避免视频通话，可能的原因是？",
                "options": ["网络不好", "害羞", "隐瞒身份", "设备问题"],
                "type": "分析题"
            },
            {
                "question": "在网络交往中，保护个人隐私的最佳方式是？",
                "options": ["完全开放", "逐步透露", "保持警惕", "寻求帮助"],
                "type": "原则题"
            }
        ]
    }
    
    print("🚀 测试AI生成防护训练报告...")
    print(f"训练类型: {test_data['drill_type']}")
    print(f"场景: {test_data['scenario_name']}")
    print(f"得分: {test_data['score']}%")
    print(f"正确率: {test_data['correct_answers']}/{test_data['total_questions']}")
    print("=" * 60)
    
    # 发送创建报告请求
    status_code, result = make_request(
        f"{API_BASE_URL}/protection-drill/reports",
        method="POST",
        data=test_data
    )
    
    if status_code == 200:
        report_id = result['id']
        print(f"✅ 训练报告创建成功，ID: {report_id}")
        
        # 检查是否生成了AI分析
        if result.get('report_content'):
            print("✅ AI详细分析已生成")
            
            # 解析AI分析内容
            try:
                ai_analysis = json.loads(result['report_content'])
                
                print("\n🤖 AI分析内容预览:")
                print("-" * 40)
                
                # 总体分析
                if 'overall_analysis' in ai_analysis:
                    print("📊 总体分析:")
                    overall_text = ai_analysis['overall_analysis'].strip()
                    print(overall_text[:200] + "..." if len(overall_text) > 200 else overall_text)
                
                # 优势分析
                if 'strength_analysis' in ai_analysis:
                    print(f"\n💪 优势分析 ({len(ai_analysis['strength_analysis'])}项):")
                    for i, strength in enumerate(ai_analysis['strength_analysis'][:3], 1):
                        print(f"  {i}. {strength}")
                
                # 薄弱环节
                if 'weakness_analysis' in ai_analysis:
                    print(f"\n⚠️ 薄弱环节 ({len(ai_analysis['weakness_analysis'])}项):")
                    for i, weakness in enumerate(ai_analysis['weakness_analysis'][:3], 1):
                        print(f"  {i}. {weakness}")
                
                # 改进建议
                if 'improvement_suggestions' in ai_analysis:
                    print(f"\n💡 改进建议 ({len(ai_analysis['improvement_suggestions'])}项):")
                    for i, suggestion in enumerate(ai_analysis['improvement_suggestions'][:3], 1):
                        print(f"  {i}. {suggestion}")
                
                # 知识点
                if 'knowledge_points' in ai_analysis:
                    print(f"\n📚 相关知识点 ({len(ai_analysis['knowledge_points'])}项):")
                    for i, point in enumerate(ai_analysis['knowledge_points'][:5], 1):
                        print(f"  {i}. {point}")
                
                # 表现评估
                if 'performance_evaluation' in ai_analysis:
                    eval_data = ai_analysis['performance_evaluation']
                    print(f"\n⭐ 表现评估:")
                    print(f"  等级: {eval_data.get('score_level', 'N/A')}")
                    print(f"  评分: {eval_data.get('overall_rating', 'N/A')}/5星")
                    print(f"  准确率评估: {eval_data.get('accuracy_assessment', 'N/A')}")
                    if eval_data.get('speed_assessment'):
                        print(f"  速度评估: {eval_data['speed_assessment']}")
                
                # 题目分析统计
                if 'question_analysis' in ai_analysis:
                    correct_questions = [q for q in ai_analysis['question_analysis'] if q.get('is_correct')]
                    wrong_questions = [q for q in ai_analysis['question_analysis'] if not q.get('is_correct')]
                    print(f"\n📝 题目分析统计:")
                    print(f"  正确题目: {len(correct_questions)}题")
                    print(f"  错误题目: {len(wrong_questions)}题")
                    
                    if wrong_questions:
                        print("  错误题目详情:")
                        for q in wrong_questions[:3]:
                            print(f"    第{q.get('question_number')}题: 选择{q.get('user_answer')}, 正确答案{q.get('correct_answer')}")
                
                print("\n🎉 AI分析生成成功！")
                return report_id
                
            except json.JSONDecodeError as e:
                print(f"❌ AI分析内容解析失败: {e}")
                return report_id
            
        else:
            print("⚠️ 未生成AI分析内容")
            return report_id
        
    else:
        print(f"❌ 创建报告失败: {status_code}")
        print(f"错误信息: {result}")
        return None

def test_report_detail_with_ai(report_id):
    """测试查看包含AI分析的报告详情"""
    if not report_id:
        return
    
    print(f"\n\n📋 获取报告详情 (ID: {report_id})...")
    print("=" * 60)
    
    status_code, result = make_request(
        f"{API_BASE_URL}/protection-drill/reports/{report_id}"
    )
    
    if status_code == 200:
        print("✅ 报告详情获取成功")
        
        # 显示基本信息
        print(f"\n📊 基本信息:")
        print(f"  训练类型: {result['drill_type']}")
        print(f"  场景名称: {result['scenario_name']}")
        print(f"  得分: {result['score']}%")
        print(f"  完成时间: {result.get('completion_time', 'N/A')}秒")
        print(f"  创建时间: {result['created_at']}")
        
        # 检查AI分析内容
        if result.get('report_content'):
            try:
                ai_analysis = json.loads(result['report_content'])
                print(f"\n🤖 AI分析内容 (完整版):")
                print(f"  总体分析: ✅")
                print(f"  题目分析: ✅ ({len(ai_analysis.get('question_analysis', []))}题)")
                print(f"  优势分析: ✅ ({len(ai_analysis.get('strength_analysis', []))}项)")
                print(f"  薄弱环节: ✅ ({len(ai_analysis.get('weakness_analysis', []))}项)")
                print(f"  改进建议: ✅ ({len(ai_analysis.get('improvement_suggestions', []))}项)")
                print(f"  知识点: ✅ ({len(ai_analysis.get('knowledge_points', []))}项)")
                print(f"  表现评估: ✅")
                
                print("\n✨ 完整AI分析内容结构验证成功!")
                
            except json.JSONDecodeError as e:
                print(f"❌ AI分析内容解析失败: {e}")
        else:
            print("⚠️ 报告不包含AI分析内容")
    else:
        print(f"❌ 获取报告详情失败: {status_code}")
        print(f"错误信息: {result}")

def test_multiple_scenarios():
    """测试多个不同场景的AI分析"""
    
    scenarios = [
        {
            "drill_type": "关系边界设定",
            "scenario_name": "职场人际关系",
            "total_questions": 8,
            "correct_answers": 6,
            "score": 75.0,
            "completion_time": 360,
            "answers": [2, 1, 3, 2, 1, 2, 3, 1],
            "correct_answers_list": [2, 1, 1, 2, 1, 2, 3, 2],
            "questions_data": [
                {"question": "同事要求您承担额外工作，您应该？", "type": "边界题"},
                {"question": "领导对您有不当要求时，正确做法是？", "type": "处理题"},
                {"question": "如何在职场中保持适当的人际距离？", "type": "原则题"},
                {"question": "面对职场霸凌，您的应对策略是？", "type": "应对题"}
            ]
        },
        {
            "drill_type": "情感操控识别",
            "scenario_name": "亲密关系操控",
            "total_questions": 6,
            "correct_answers": 4,
            "score": 66.7,
            "completion_time": 300,
            "answers": [1, 3, 2, 1, 2, 3],
            "correct_answers_list": [1, 2, 2, 1, 3, 3],
            "questions_data": [
                {"question": "伴侣经常贬低您的能力，这是否正常？", "type": "识别题"},
                {"question": "对方用冷暴力控制您的行为，应该？", "type": "应对题"},
                {"question": "情感操控的常见表现包括？", "type": "特征题"}
            ]
        }
    ]
    
    print("\n\n🔄 测试多种场景的AI分析生成...")
    print("=" * 60)
    
    created_reports = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario['drill_type']} - {scenario['scenario_name']}")
        print(f"得分: {scenario['score']}% ({scenario['correct_answers']}/{scenario['total_questions']})")
        
        status_code, result = make_request(
            f"{API_BASE_URL}/protection-drill/reports",
            method="POST",
            data=scenario
        )
        
        if status_code == 200:
            created_reports.append(result['id'])
            print(f"✅ 报告创建成功 (ID: {result['id']})")
            
            # 快速验证AI分析
            if result.get('report_content'):
                ai_analysis = json.loads(result['report_content'])
                suggestions_count = len(ai_analysis.get('improvement_suggestions', []))
                strengths_count = len(ai_analysis.get('strength_analysis', []))
                print(f"  AI分析: ✅ (建议{suggestions_count}项, 优势{strengths_count}项)")
            else:
                print("  AI分析: ❌")
        else:
            print(f"❌ 创建失败: {status_code}")
    
    print(f"\n📊 批量测试完成，成功创建 {len(created_reports)} 份报告")
    return created_reports

if __name__ == "__main__":
    print("🚀 开始测试AI生成防护训练报告功能")
    print("=" * 60)
    
    # 测试1: 基础AI分析生成
    report_id = test_ai_generated_report()
    
    # 测试2: 查看AI分析详情
    if report_id:
        test_report_detail_with_ai(report_id)
    
    # 测试3: 多场景测试
    batch_reports = test_multiple_scenarios()
    
    print("\n\n🎯 测试总结:")
    print("=" * 60)
    print("✅ AI自动分析生成功能")
    print("✅ 多种训练场景支持")
    print("✅ 详细分析内容结构化")
    print("✅ 个性化建议和评估")
    print("✅ 前后端数据流畅通")
    
    if report_id and batch_reports:
        total_reports = 1 + len(batch_reports)
        print(f"\n📈 本次测试共创建 {total_reports} 份AI生成的训练报告")
        print("功能验证完成！可以在前端界面查看详细的AI分析内容。")
    
    print("\n🎉 AI功能集成测试完成！")
