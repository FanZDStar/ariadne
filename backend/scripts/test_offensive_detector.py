"""
测试冒犯性内容检测服务

运行方式:
cd backend
python scripts/test_offensive_detector.py
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.offensive_content_detector import check_offensive_content


def test_offensive_detection():
    """测试冒犯性内容检测"""
    
    print("=" * 60)
    print("🛡️  冒犯性内容检测测试")
    print("=" * 60)
    print()
    
    # 测试用例
    test_cases = [
        ("你这个观点真是太棒了，学到了很多！", False, "正常的积极评论"),
        ("今天天气不错，心情很好", False, "正常的日常评论"),
        ("我觉得这个想法不太合适，可以再改进一下", False, "正常的建议评论"),
        ("你是不是脑子有病？", True, "直接侮辱"),
        ("傻逼，滚出去", True, "脏话侮辱"),
        ("NMSL", True, "网络用语侮辱"),
        ("垃圾东西", True, "贬低性词汇"),
        ("你妈的", True, "粗俗脏话"),
    ]
    
    print("开始检测评论...\n")
    
    passed = 0
    failed = 0
    
    for i, (text, expected_offensive, description) in enumerate(test_cases, 1):
        print(f"测试 {i}: {description}")
        print(f"内容: \"{text}\"")
        
        result = check_offensive_content(text, threshold=0.7)
        
        is_offensive = result["is_offensive"]
        confidence = result["confidence"]
        label = result["label"]
        
        # 判断是否通过测试
        test_passed = (is_offensive == expected_offensive)
        status = "✅ 通过" if test_passed else "❌ 失败"
        
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"结果: {label} | 冒犯性: {is_offensive} | 置信度: {confidence:.2%}")
        print(f"状态: {status}")
        print(f"提示: {result['message']}")
        print("-" * 60)
        print()
    
    print("=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️  有 {failed} 个测试失败，可能需要调整阈值或检查模型")


def test_batch_detection():
    """测试批量检测"""
    print("\n")
    print("=" * 60)
    print("📦 批量检测测试")
    print("=" * 60)
    print()
    
    from app.services.offensive_content_detector import get_offensive_detector
    
    detector = get_offensive_detector()
    
    comments = [
        "这个想法真不错！",
        "你是傻子吗？",
        "感谢分享，很有帮助",
        "滚蛋，垃圾"
    ]
    
    print("批量检测以下评论:")
    for i, comment in enumerate(comments, 1):
        print(f"{i}. {comment}")
    print()
    
    results = detector.batch_check(comments, threshold=0.7)
    
    print("检测结果:")
    for i, (comment, result) in enumerate(zip(comments, results), 1):
        status = "🚫 拦截" if result["is_offensive"] else "✅ 通过"
        print(f"{i}. {status} | {comment}")
        print(f"   置信度: {result['confidence']:.2%} | {result['message']}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    print("\n⏳ 模型首次加载可能需要几分钟时间，请耐心等待...\n")
    
    try:
        # 单条检测测试
        test_offensive_detection()
        
        # 批量检测测试
        test_batch_detection()
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
