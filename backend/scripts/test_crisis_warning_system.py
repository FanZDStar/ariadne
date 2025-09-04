#file:ariadne/backend/scripts/test_crisis_warning_system.py
"""
心理危机预警系统功能测试脚本
"""
import sys
import os
import asyncio
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.crisis_warning_service import CrisisWarningService, RiskLevel, WarningType
from app.models.user import User
from app.models.emotional_diary import EmotionalDiary
from app.models.diary_image import DiaryImage
from app.models.chat_history import ChatSession, ChatMessage
from app.models.crisis_warning import CrisisWarning
from app.models.tree_hole import TreeHoleWhisper  # 添加这个导入

def create_test_session():
    """创建测试数据库会话"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def test_keyword_detection():
    """测试关键词检测功能"""
    print("🔍 测试关键词检测功能...")
    
    db = create_test_session()
    service = CrisisWarningService(db)
    
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
    
    db.close()

def test_mood_trend_analysis():
    """测试心情趋势分析（需要先有用户和心情数据）"""
    print("📈 测试心情趋势分析...")
    
    db = create_test_session()
    
    # 检查是否有用户数据
    user = db.query(User).first()
    if not user:
        print("⚠️  没有找到用户数据，跳过心情趋势测试")
        print("   请先通过前端注册用户并记录一些心情日记")
        db.close()
        return
    
    service = CrisisWarningService(db)
    
    try:
        # 分析用户心情趋势
        assessment = service.analyze_user_risk(user.user_id, days=30)
        
        print(f"✅ 用户 {user.username} 的风险评估:")
        print(f"   风险等级: {assessment.risk_level.value}")
        print(f"   风险评分: {assessment.score:.1f}/100")
        print(f"   风险原因: {'; '.join(assessment.reasons) if assessment.reasons else '无'}")
        print(f"   建议: {'; '.join(assessment.recommendations) if assessment.recommendations else '无'}")
        
    except Exception as e:
        print(f"❌ 心情趋势分析失败: {str(e)}")
    
    db.close()

def test_crisis_warning_creation():
    """测试危机预警创建"""
    print("⚠️  测试危机预警创建...")
    
    db = create_test_session()
    
    # 检查是否有用户数据
    user = db.query(User).first()
    if not user:
        print("⚠️  没有找到用户数据，跳过预警创建测试")
        db.close()
        return
    
    service = CrisisWarningService(db)
    
    try:
        # 创建模拟的风险评估结果
        from app.services.crisis_warning_service import RiskAssessmentResult
        
        mock_assessment = RiskAssessmentResult(
            risk_level=RiskLevel.HIGH,
            score=75.0,
            reasons=["测试检测到高风险关键词", "心情趋势下降"],
            recommendations=["建议寻求专业心理咨询", "保持与亲友联系"]
        )
        
        # 创建预警记录
        warning = service.create_warning(
            user_id=user.user_id,
            assessment=mock_assessment,
            warning_type=WarningType.AI_ANALYSIS,
            source_data="这是一个测试预警"
        )
        
        print(f"✅ 成功创建预警记录:")
        print(f"   预警ID: {warning.warning_id}")
        print(f"   风险等级: {warning.risk_level.value}")
        print(f"   预警类型: {warning.warning_type.value}")
        print(f"   创建时间: {warning.created_at}")
        
        # 获取用户的预警记录
        warnings = service.get_user_warnings(user.user_id, days=7)
        print(f"   用户总预警数: {len(warnings)}")
        
    except Exception as e:
        print(f"❌ 预警创建失败: {str(e)}")
    
    db.close()

def test_database_tables():
    """测试数据库表是否正确创建"""
    print("🗄️  测试数据库表结构...")
    
    db = create_test_session()
    
    try:
        # 测试查询各个表
        warnings_count = db.query(CrisisWarning).count()
        print(f"✅ crisis_warnings 表: {warnings_count} 条记录")
        
        # 查看是否有关键词表
        result = db.execute("SHOW TABLES LIKE 'crisis_keywords'")
        if result.fetchone():
            keywords_count = db.execute("SELECT COUNT(*) FROM crisis_keywords").fetchone()[0]
            print(f"✅ crisis_keywords 表: {keywords_count} 条记录")
        else:
            print("⚠️  crisis_keywords 表不存在（正常，关键词存储在代码中）")
        
        print("✅ 数据库表结构测试通过")
        
    except Exception as e:
        print(f"❌ 数据库表测试失败: {str(e)}")
    
    db.close()

def show_system_overview():
    """显示系统功能概览"""
    print("\n" + "="*60)
    print("🧠 心理危机预警系统功能概览")
    print("="*60)
    print("""
📊 核心功能:
   1. 关键词检测 - 实时监控用户输入的危险词汇
   2. 心情趋势分析 - 分析用户心情变化模式
   3. 风险评估 - 综合多维度数据进行风险评分
   4. 预警管理 - 创建、查看、解决预警记录
   5. 定时监控 - 后台自动检查用户风险状态

🔧 API端点:
   • POST /api/crisis/assess-risk - 执行风险评估
   • GET  /api/crisis/warnings - 获取预警记录
   • POST /api/crisis/warnings/{id}/resolve - 解决预警
   • GET  /api/crisis/statistics - 获取风险统计
   • POST /api/crisis/background-check - 触发后台检查

🚨 风险等级:
   • LOW (低风险) - 正常状态，无明显风险信号
   • MEDIUM (中等风险) - 存在一些负面情绪，需要关注
   • HIGH (高风险) - 多种风险因素，建议专业干预
   • CRITICAL (紧急风险) - 存在自伤倾向，需要立即干预

📱 前端组件:
   • CrisisWarning.vue - 风险评估和预警显示组件
   • crisisApi.js - API调用工具函数
   • 支持实时关键词检测和预警提醒

🔒 隐私保护:
   • 敏感数据加密存储
   • 用户授权访问
   • 符合隐私保护规范
""")

def main():
    """主测试函数"""
    print("🔬 心理危机预警系统测试")
    print("=" * 50)
    
    try:
        # 1. 测试数据库表
        test_database_tables()
        print()
        
        # 2. 测试关键词检测
        test_keyword_detection()
        
        # 3. 测试心情趋势分析
        test_mood_trend_analysis()
        print()
        
        # 4. 测试预警创建
        test_crisis_warning_creation()
        print()
        
        # 5. 显示系统概览
        show_system_overview()
        
        print("\n🎉 测试完成！")
        print("\n💡 接下来的步骤:")
        print("1. 启动后端服务: uvicorn app.main:app --reload")
        print("2. 在前端页面中集成 CrisisWarning 组件")
        print("3. 测试实际的风险评估和预警功能")
        print("4. 根据需要调整关键词配置和风险阈值")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
