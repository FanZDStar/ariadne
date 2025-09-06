#!/usr/bin/env python3
"""
测试风险评估API端点
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.models.risk_assessment_report import RiskAssessmentReport
from app.services.risk_assessment_service import RiskAssessmentService

async def test_risk_api():
    """测试风险评估API相关功能"""
    
    print("============================================================")
    print("🔍 风险评估API测试")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 1. 检查数据库中的报告
        print("📊 检查数据库中的风险评估报告...")
        reports = db.query(RiskAssessmentReport).all()
        print(f"✅ 数据库中共有 {len(reports)} 条报告")
        
        for report in reports:
            print(f"   报告ID: {report.report_id}, 用户ID: {report.user_id}, 会话ID: {report.session_id}")
            print(f"   风险等级: {report.overall_risk_level}, 生成时间: {report.report_generated_time}")
        
        # 2. 检查用户
        print("\n👤 检查用户...")
        users = db.query(User).all()
        print(f"✅ 数据库中共有 {len(users)} 个用户")
        
        # 3. 测试服务方法
        if users:
            user = users[0]
            print(f"\n🔬 测试用户 {user.user_id} 的报告历史...")
            service = RiskAssessmentService(db)
            user_reports = service.get_user_reports_history(user.user_id, limit=10)
            print(f"✅ 用户 {user.user_id} 的报告数量: {len(user_reports)}")
            
            for report in user_reports:
                print(f"   - 报告ID: {report.report_id}, 标题: {report.report_title}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_risk_api())
    if success:
        print("\n" + "="*60)
        print("🎉 风险评估API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
